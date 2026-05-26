#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from _audit_utils import (
    detect_placeholders,
    extract_acceptance_criteria,
    extract_flows,
    format_table,
    is_testable_acceptance_criterion,
    list_items,
    read_text,
    section_text,
    write_text,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate handoff readiness for Step 9.")
    parser.add_argument("--handoff", required=True, help="Path to the feature handoff")
    parser.add_argument("--output", required=True, help="Markdown report output path")
    return parser


def extract_task_blocks(section: str) -> list[str]:
    matches = list(re.finditer(r"^###\s+Task\s+\d+:.*$", section, re.MULTILINE))
    blocks: list[str] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        blocks.append(section[start:end].strip())
    return blocks


def main() -> int:
    args = build_parser().parse_args()

    handoff_path = Path(args.handoff)
    handoff_text = read_text(handoff_path)

    ac_lines = extract_acceptance_criteria(handoff_text)
    flows = extract_flows(handoff_text)
    build_tasks = extract_task_blocks(section_text(handoff_text, ["Build Tasks"]))
    out_of_scope_items = list_items(section_text(handoff_text, ["Out of Scope"]))
    open_questions = list_items(section_text(handoff_text, ["Open Questions", "Unresolved Items"]))
    ui_direction = section_text(handoff_text, ["UI Direction"])
    dcr_protocol = section_text(handoff_text, ["DCR Protocol"])
    placeholders = detect_placeholders(handoff_text)

    ac_failures = [item for item in ac_lines if not is_testable_acceptance_criterion(item)]
    ac_ok = bool(ac_lines) and not ac_failures

    mapped_tasks = [task for task in build_tasks if "user story:" in task.lower()]
    task_mapping_ok = bool(build_tasks) and len(mapped_tasks) == len(build_tasks)

    unresolved_items = open_questions + placeholders
    unresolved_ok = not unresolved_items

    flow_failures = [flow for flow in flows if "->" not in flow and "→" not in flow]
    flow_ok = bool(flows) and not flow_failures

    ui_signals = ("screen", "ui", "button", "form", "modal", "dashboard", "page")
    interactive_required = any(signal in handoff_text.lower() for signal in ui_signals)
    if interactive_required:
        ui_ok = bool(ui_direction.strip())
        ui_status = "PASS" if ui_ok else "FAIL"
        ui_notes = "UI direction present" if ui_ok else "Interactive scope implied but UI Direction is empty"
    else:
        ui_ok = True
        ui_status = "N/A"
        ui_notes = "No interactive scope detected from handoff"

    non_goals_ok = bool(out_of_scope_items)
    dcr_ok = "docs/feedback/" in dcr_protocol or "design change request" in dcr_protocol.lower()

    rows = [
        ("1", "All AC are testable", "✅" if ac_ok else "❌", "All AC lines are measurable" if ac_ok else f"{len(ac_failures)} AC lines need tightening"),
        ("2", "Build Tasks map to user stories", "✅" if task_mapping_ok else "❌", "Each task cites a user story" if task_mapping_ok else "One or more tasks are missing a 'User story:' reference"),
        ("3", "No unresolved product decisions", "✅" if unresolved_ok else "❌", "No placeholders/open questions remain" if unresolved_ok else f"{len(unresolved_items)} unresolved items remain"),
        ("4", "User flows have no dead ends", "✅" if flow_ok else "❌", "Flows show explicit start/end movement" if flow_ok else "One or more flows lack clear transitions"),
        ("5", "UI brief covers all interactive features (if applicable)", "✅" if ui_status == "PASS" else ("❌" if ui_status == "FAIL" else "N/A"), ui_notes),
        ("6", "Non-goals clear enough to prevent scope creep", "✅" if non_goals_ok else "❌", "Out of Scope section is populated" if non_goals_ok else "Out of Scope is empty"),
        ("7", "DCR protocol specified", "✅" if dcr_ok else "❌", "Feedback loop documented" if dcr_ok else "DCR protocol section missing or incomplete"),
    ]

    verdict = "PASS" if all(row[2] in {"✅", "N/A"} for row in rows) else "FAIL"

    lines = [
        f"# Readiness Check: {handoff_path.stem}",
        "",
        f"**Version**: {handoff_path.parent.name}",
        f"**Date**: generated-by-script",
        f"**Handoff**: `{handoff_path}`",
        "",
        "## Checklist",
        "",
        format_table(["#", "Criterion", "Status", "Notes"], rows),
        "",
        "## Unresolved Items",
        "",
    ]

    if unresolved_items:
        lines.extend(f"- {item} — resolve before engineering handoff" for item in unresolved_items)
    else:
        lines.append("- None")
    lines.extend(["", "## Verdict", "", f"**{verdict}**"])

    write_text(args.output, "\n".join(lines).rstrip() + "\n")

    print(
        json.dumps(
            {
                "verdict": verdict,
                "failing_rows": [row[0] for row in rows if row[2] == "❌"],
                "unresolved_items": unresolved_items,
                "report_path": str(Path(args.output)),
            },
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
