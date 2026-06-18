#!/usr/bin/env python3

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import defaultdict
from pathlib import Path

from _audit_utils import (
    extract_acceptance_criteria,
    extract_flows,
    extract_screen_names,
    extract_user_stories,
    feature_stem,
    format_table,
    keyword_overlap,
    read_text,
    write_text,
)


ENDPOINT_RE = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=-]+)")
CONSTANT_RE = re.compile(r"(?P<label>[A-Za-z][A-Za-z0-9 _/-]{2,40})\s*[:=]\s*(?P<value>\d+(?:\.\d+)?\s?(?:ms|s|sec|seconds|min|minutes|%|kb|mb|gb|users|items|requests?)?)", re.IGNORECASE)
STATE_LINE_RE = re.compile(r"(?i)\b(state|status|statuses|states)\b")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cross-feature integration audit for Step 6.")
    parser.add_argument("--roadmap", required=True)
    parser.add_argument("--architecture", required=True)
    parser.add_argument("--prd-glob", required=True)
    parser.add_argument("--interface-glob", required=True)
    parser.add_argument("--ui-glob")
    parser.add_argument("--feature", action="append", dest="features", default=[])
    parser.add_argument("--newest-feature", help="Newest completed feature for incremental runs")
    parser.add_argument("--final-run", action="store_true", help="Require full PRD/UI coverage for every audited feature")
    parser.add_argument("--output", required=True)
    return parser


def read_many(pattern: str) -> dict[str, tuple[Path, str]]:
    docs: dict[str, tuple[Path, str]] = {}
    for path_str in sorted(glob.glob(pattern)):
        path = Path(path_str)
        docs[feature_stem(path)] = (path, read_text(path))
    return docs


def extract_constants(text: str, source: str) -> list[tuple[str, str, str]]:
    return [
        (re.sub(r"[^a-z0-9]+", "_", match.group("label").strip().lower()).strip("_"), match.group("value").strip(), source)
        for match in CONSTANT_RE.finditer(text)
    ]


def extract_endpoints(text: str, source: str) -> list[tuple[str, str]]:
    return [(f"{method} {path}", source) for method, path in ENDPOINT_RE.findall(text)]


def extract_state_signatures(text: str, source: str) -> list[tuple[str, str]]:
    signatures: list[tuple[str, str]] = []
    for line in text.splitlines():
        if STATE_LINE_RE.search(line):
            normalized = re.sub(r"\s+", " ", line.strip())
            signatures.append((normalized, source))
    return signatures


def roadmap_mentions_feature(feature: str, roadmap_text: str) -> bool:
    roadmap_lower = roadmap_text.lower()
    normalized_roadmap = re.sub(r"[^a-z0-9]+", " ", roadmap_lower)
    feature_lower = feature.lower()
    feature_slug = re.sub(r"^\d+-", "", feature_lower)
    candidates = {
        feature_lower,
        feature_lower.replace("-", " "),
        feature_slug,
        feature_slug.replace("-", " "),
    }
    return any(candidate and (candidate in roadmap_lower or candidate.replace("-", " ") in normalized_roadmap) for candidate in candidates)


def expected_full_doc_features(explicit_features: list[str], newest_feature: str | None, final_run: bool) -> set[str]:
    if final_run:
        return set(explicit_features)
    return {newest_feature} if newest_feature else set()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    roadmap_path = Path(args.roadmap)
    architecture_path = Path(args.architecture)
    roadmap_text = read_text(roadmap_path)
    architecture_text = read_text(architecture_path)

    prd_docs = read_many(args.prd_glob)
    interface_docs = read_many(args.interface_glob)
    ui_docs = read_many(args.ui_glob) if args.ui_glob else {}

    if not args.features:
        parser.error("--feature must be provided for every audited feature in scope")
    features = list(dict.fromkeys(args.features))
    if args.final_run and not args.features:
        parser.error("--feature must be provided for every audited feature when --final-run is set")
    if not args.final_run and not args.newest_feature:
        parser.error("--newest-feature is required for incremental runs")
    if args.newest_feature and args.newest_feature not in features:
        parser.error("--newest-feature must be included in the audited feature scope")
    full_doc_expected = expected_full_doc_features(features, args.newest_feature, args.final_run)

    constant_sources: dict[str, list[tuple[str, str]]] = defaultdict(list)
    endpoint_sources: dict[str, list[str]] = defaultdict(list)
    state_lines: list[tuple[str, str]] = []

    for label, value, source in extract_constants(architecture_text, f"architecture:{architecture_path.name}"):
        constant_sources[label].append((value, source))
    for endpoint, source in extract_endpoints(architecture_text, f"architecture:{architecture_path.name}"):
        endpoint_sources[endpoint].append(source)
    state_lines.extend(extract_state_signatures(architecture_text, f"architecture:{architecture_path.name}"))

    for doc_group in (prd_docs, interface_docs, ui_docs):
        for feature, (path, text) in doc_group.items():
            source = f"{feature}:{path.name}"
            for label, value, extracted_source in extract_constants(text, source):
                constant_sources[label].append((value, extracted_source))
            for endpoint, extracted_source in extract_endpoints(text, source):
                endpoint_sources[endpoint].append(extracted_source)
            state_lines.extend(extract_state_signatures(text, source))

    constant_conflicts = []
    for label, entries in sorted(constant_sources.items()):
        unique_values = sorted({value for value, _ in entries})
        if len(unique_values) > 1:
            constant_conflicts.append((label, ", ".join(unique_values), "; ".join(source for _, source in entries)))

    endpoint_duplicates = [(endpoint, ", ".join(sorted(set(sources)))) for endpoint, sources in sorted(endpoint_sources.items()) if len(set(sources)) > 1]

    feature_rows = []
    missing_roadmap = []
    missing_prd = []
    missing_interface = []
    missing_ui = []

    for feature in features:
        in_roadmap = roadmap_mentions_feature(feature, roadmap_text)
        prd_exists = feature in prd_docs
        interface_exists = feature in interface_docs
        ui_exists = feature in ui_docs
        expects_full_docs = feature in full_doc_expected
        prd_cell = "✅" if prd_exists else ("summary-only" if interface_exists and not expects_full_docs else "❌")
        interface_cell = "✅" if interface_exists else ("optional" if not expects_full_docs else "❌")
        feature_rows.append((feature, "✅" if in_roadmap else "❌", prd_cell, interface_cell, "✅" if ui_exists else "N/A"))
        if not in_roadmap:
            missing_roadmap.append(feature)
        if expects_full_docs and not prd_exists:
            missing_prd.append(feature)
        if not interface_exists:
            missing_interface.append(feature)
        if feature in ui_docs and feature not in prd_docs:
            missing_ui.append(feature)

    ui_traceability_gaps = []
    for feature, (ui_path, ui_text) in ui_docs.items():
        prd_text = prd_docs.get(feature, (None, ""))[1]
        if not prd_text:
            continue
        screens = extract_screen_names(ui_text)
        trace_targets = extract_acceptance_criteria(prd_text) + extract_flows(prd_text) + extract_user_stories(prd_text)
        unmatched = [screen for screen in screens if not any(keyword_overlap(screen, target) >= 0.25 for target in trace_targets)]
        if unmatched:
            ui_traceability_gaps.append((feature, ", ".join(unmatched)))

    verdict = "SIGNALS_CLEAR"
    if (
        constant_conflicts
        or endpoint_duplicates
        or missing_roadmap
        or missing_prd
        or missing_interface
        or ui_traceability_gaps
    ):
        verdict = "HOTSPOTS_FOUND"

    lines = [
        f"# Version Integration Audit — {Path(args.output).parent.name or 'version'}",
        "",
        "## Summary",
        f"- Features audited: {', '.join(features)}",
        f"- Documents read: {2 + len(prd_docs) + len(interface_docs) + len(ui_docs)}",
        f"- Result: **{verdict}**",
        "",
        "## Part A — Shared Concepts",
        "",
        "### State Machine",
        *([f"- {line} ({source})" for line, source in state_lines[:20]] or ["- No explicit state/status lines extracted"]),
        "",
        "### Constants",
        format_table(["Constant", "Values", "Sources"], constant_conflicts or [("None", "—", "—")]),
        "",
        "### API Contracts",
        format_table(["Endpoint", "Sources"], endpoint_duplicates or [("None", "—")]),
        "",
        "## Script Evidence Map",
        format_table(
            ["Check", "Script Evidence"],
            [
                ("A1", f"{len(state_lines)} state/status lines extracted"),
                ("A2", "No constant conflicts detected" if not constant_conflicts else f"Constant conflicts: {', '.join(label for label, _, _ in constant_conflicts)}"),
                ("A3", f"Interface summaries loaded for {len(interface_docs)} features"),
                ("A4", "No duplicate endpoints detected" if not endpoint_duplicates else f"Duplicate endpoints: {len(endpoint_duplicates)}"),
                ("A5", f"Feature scope loaded for {len(features)} features; terminology requires semantic review"),
                ("B1", "Roadmap vs PRD matrix generated"),
                ("B2", "PRD vs interface-summary matrix generated"),
                ("B3", "Architecture constants/endpoints/state signatures extracted for comparison"),
                ("B4", "No UI→PRD traceability gaps detected" if not ui_traceability_gaps else f"UI→PRD gaps in {len(ui_traceability_gaps)} feature(s)"),
                ("B5", "Version-scope artifact coverage matrix generated"),
                ("C1", f"Acceptance-criteria evidence extracted from {len(prd_docs)} full PRD(s); incremental runs compare newest full PRD against prior interface summaries"),
                ("C2", f"Flow evidence extracted from {len(prd_docs)} full PRD(s); incremental runs compare newest full PRD against prior interface summaries"),
                ("C3", f"Feature coverage matrix generated for {len(features)} features"),
                ("C4", "Completed feature interface matrix generated; dependency order still needs semantic review"),
                ("C5", f"{len(state_lines)} state/error/status signals extracted for semantic review"),
            ],
        ),
        "",
        "## Part B — Traceability",
        format_table(["Feature", "Roadmap", "PRD", "Interface", "UI"], feature_rows),
        "",
    ]

    if missing_roadmap or missing_prd or missing_interface or missing_ui:
        lines.append("### Coverage Gaps")
        lines.extend(f"- Feature missing from roadmap selection: {feature}" for feature in missing_roadmap)
        lines.extend(f"- Missing PRD file: {feature}" for feature in missing_prd)
        lines.extend(f"- Missing interface summary: {feature}" for feature in missing_interface)
        lines.extend(f"- UI brief exists without PRD counterpart: {feature}" for feature in missing_ui)
        lines.append("")

    lines.extend(["## Part C — Cross-Feature", ""])
    if ui_traceability_gaps:
        lines.append("### UI → PRD Traceability Gaps")
        lines.extend(f"- {feature}: {screens}" for feature, screens in ui_traceability_gaps)
        lines.append("")
    else:
        lines.append("- No UI → PRD traceability gaps detected.")
        lines.append("")

    lines.extend(
        [
            "## Script Verdict",
            f"- **{verdict}** (script signal only — semantic gate verdict is set by the audit skill, not by this script)",
            "",
            "## Recommended Fix Order",
        ]
    )

    fix_order = []
    if constant_conflicts:
        fix_order.append("1. Resolve shared constant mismatches across architecture/feature docs")
    if missing_roadmap or missing_prd or missing_interface:
        fix_order.append(f"{len(fix_order) + 1}. Restore missing file coverage before engineering delivery")
    if ui_traceability_gaps:
        fix_order.append(f"{len(fix_order) + 1}. Align UI surfaces with PRD user stories")
    if not fix_order:
        fix_order.append("1. No deterministic conflicts found")
    lines.extend(fix_order)

    write_text(args.output, "\n".join(lines).rstrip() + "\n")

    print(
        json.dumps(
            {
                "script_result": verdict,
                "constant_conflicts": [label for label, _, _ in constant_conflicts],
                "missing_roadmap": missing_roadmap,
                "missing_prd": missing_prd,
                "missing_interface": missing_interface,
                "ui_traceability_gaps": [feature for feature, _ in ui_traceability_gaps],
                "report_path": str(Path(args.output)),
            },
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
