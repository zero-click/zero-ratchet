#!/usr/bin/env python3

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import defaultdict
from pathlib import Path

from _audit_utils import extract_screen_names, extract_user_stories, feature_stem, format_table, keyword_overlap, read_text, write_text


ENDPOINT_RE = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=-]+)")
CONSTANT_RE = re.compile(r"(?P<label>[A-Za-z][A-Za-z0-9 _/-]{2,40})\s*[:=]\s*(?P<value>\d+(?:\.\d+)?\s?(?:ms|s|sec|seconds|min|minutes|%|kb|mb|gb|users|items|requests?)?)", re.IGNORECASE)
STATE_LINE_RE = re.compile(r"(?i)\b(state|status|statuses|states)\b")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cross-feature integration audit for Step 10.")
    parser.add_argument("--roadmap", required=True)
    parser.add_argument("--architecture", required=True)
    parser.add_argument("--requirements-glob", required=True)
    parser.add_argument("--prd-glob", required=True)
    parser.add_argument("--handoff-glob", required=True)
    parser.add_argument("--ui-glob")
    parser.add_argument("--feature", action="append", dest="features", default=[])
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


def main() -> int:
    args = build_parser().parse_args()

    roadmap_path = Path(args.roadmap)
    architecture_path = Path(args.architecture)
    roadmap_text = read_text(roadmap_path)
    architecture_text = read_text(architecture_path)

    requirements_docs = read_many(args.requirements_glob)
    prd_docs = read_many(args.prd_glob)
    handoff_docs = read_many(args.handoff_glob)
    ui_docs = read_many(args.ui_glob) if args.ui_glob else {}

    features = args.features or sorted(set(requirements_docs) | set(prd_docs) | set(handoff_docs) | set(ui_docs))

    constant_sources: dict[str, list[tuple[str, str]]] = defaultdict(list)
    endpoint_sources: dict[str, list[str]] = defaultdict(list)
    state_lines: list[tuple[str, str]] = []

    for label, value, source in extract_constants(architecture_text, f"architecture:{architecture_path.name}"):
        constant_sources[label].append((value, source))
    for endpoint, source in extract_endpoints(architecture_text, f"architecture:{architecture_path.name}"):
        endpoint_sources[endpoint].append(source)
    state_lines.extend(extract_state_signatures(architecture_text, f"architecture:{architecture_path.name}"))

    for doc_group in (requirements_docs, prd_docs, handoff_docs, ui_docs):
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
    missing_requirements = []
    missing_prd = []
    missing_handoff = []
    missing_ui = []

    for feature in features:
        in_roadmap = feature.replace("-", " ") in roadmap_text.lower() or feature in roadmap_text.lower()
        req_exists = feature in requirements_docs
        prd_exists = feature in prd_docs
        handoff_exists = feature in handoff_docs
        ui_exists = feature in ui_docs
        feature_rows.append(
            (
                feature,
                "✅" if in_roadmap else "❌",
                "✅" if req_exists else "❌",
                "✅" if prd_exists else "❌",
                "✅" if handoff_exists else "❌",
                "✅" if ui_exists else "N/A",
            )
        )
        if not in_roadmap:
            missing_roadmap.append(feature)
        if not req_exists:
            missing_requirements.append(feature)
        if req_exists and not prd_exists:
            missing_prd.append(feature)
        if prd_exists and not handoff_exists:
            missing_handoff.append(feature)
        if feature in ui_docs and feature not in prd_docs:
            missing_ui.append(feature)

    ui_traceability_gaps = []
    for feature, (ui_path, ui_text) in ui_docs.items():
        prd_text = prd_docs.get(feature, (None, ""))[1]
        if not prd_text:
            continue
        screens = extract_screen_names(ui_text)
        stories = extract_user_stories(prd_text)
        unmatched = [screen for screen in screens if not any(keyword_overlap(screen, story) >= 0.25 for story in stories)]
        if unmatched:
            ui_traceability_gaps.append((feature, ", ".join(unmatched)))

    verdict = "PASS"
    if constant_conflicts or missing_roadmap or missing_requirements or missing_prd or missing_handoff or ui_traceability_gaps:
        verdict = "CONFLICTS_FOUND"

    lines = [
        f"# Version Integration Audit — {Path(args.output).parent.name or 'version'}",
        "",
        "## Summary",
        f"- Features audited: {', '.join(features)}",
        f"- Documents read: {2 + len(requirements_docs) + len(prd_docs) + len(handoff_docs) + len(ui_docs)}",
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
        "## Part B — Traceability",
        format_table(["Feature", "Roadmap", "Requirements", "PRD", "Handoff", "UI"], feature_rows),
        "",
    ]

    if missing_roadmap or missing_requirements or missing_prd or missing_handoff or missing_ui:
        lines.append("### Coverage Gaps")
        lines.extend(f"- Feature missing from roadmap selection: {feature}" for feature in missing_roadmap)
        lines.extend(f"- Missing requirements file: {feature}" for feature in missing_requirements)
        lines.extend(f"- Missing PRD file: {feature}" for feature in missing_prd)
        lines.extend(f"- Missing handoff file: {feature}" for feature in missing_handoff)
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
            "## Verdict",
            f"- **{verdict}**",
            "",
            "## Recommended Fix Order",
        ]
    )

    fix_order = []
    if constant_conflicts:
        fix_order.append("1. Resolve shared constant mismatches across architecture/feature docs")
    if missing_roadmap or missing_requirements or missing_prd or missing_handoff:
        fix_order.append(f"{len(fix_order) + 1}. Restore missing file coverage before engineering handoff")
    if ui_traceability_gaps:
        fix_order.append(f"{len(fix_order) + 1}. Align UI surfaces with PRD user stories")
    if not fix_order:
        fix_order.append("1. No deterministic conflicts found")
    lines.extend(fix_order)

    write_text(args.output, "\n".join(lines).rstrip() + "\n")

    print(
        json.dumps(
            {
                "verdict": verdict,
                "constant_conflicts": [label for label, _, _ in constant_conflicts],
                "missing_roadmap": missing_roadmap,
                "missing_requirements": missing_requirements,
                "missing_prd": missing_prd,
                "missing_handoff": missing_handoff,
                "ui_traceability_gaps": [feature for feature, _ in ui_traceability_gaps],
                "report_path": str(Path(args.output)),
            },
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
