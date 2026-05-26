#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _audit_utils import (
    detect_placeholders,
    extract_acceptance_criteria,
    extract_flows,
    extract_non_goals,
    extract_screen_names,
    extract_user_stories,
    format_table,
    is_testable_acceptance_criterion,
    keyword_overlap,
    read_text,
    write_text,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze PRD/UI consistency for Step 7.")
    parser.add_argument("--prd", required=True, help="Path to the feature PRD")
    parser.add_argument("--ui", help="Optional path to the UI brief")
    parser.add_argument("--output", required=True, help="Markdown report output path")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    prd_path = Path(args.prd)
    ui_path = Path(args.ui) if args.ui else None

    prd_text = read_text(prd_path)
    ui_text = read_text(ui_path) if ui_path and ui_path.exists() else ""

    stories = extract_user_stories(prd_text)
    acceptance_criteria = extract_acceptance_criteria(prd_text)
    flows = extract_flows(prd_text)
    non_goals = extract_non_goals(prd_text)
    placeholders = detect_placeholders(prd_text)
    screens = extract_screen_names(ui_text) if ui_text else []

    failing_criteria = [item for item in acceptance_criteria if not is_testable_acceptance_criterion(item)]
    story_ac_ok = bool(stories) and len(acceptance_criteria) >= len(stories)
    ac_testable_ok = not failing_criteria and bool(acceptance_criteria)
    flow_notes = [flow for flow in flows if "->" not in flow and "→" not in flow]
    flow_ok = bool(flows) and not flow_notes

    non_goal_conflicts: list[str] = []
    for story in stories:
        for non_goal in non_goals:
            if keyword_overlap(story, non_goal) >= 0.6:
                non_goal_conflicts.append(f"Story '{story}' overlaps non-goal '{non_goal}'")
    non_goal_ok = not non_goal_conflicts

    screen_gaps: list[str] = []
    story_gaps: list[str] = []
    if ui_text:
        for screen in screens:
            if not any(keyword_overlap(screen, story) >= 0.25 for story in stories):
                screen_gaps.append(screen)
        for story in stories:
            if not any(keyword_overlap(story, screen) >= 0.25 for screen in screens):
                story_gaps.append(story)
        ui_ok = not screen_gaps
    else:
        ui_ok = True

    checks = [
        (
            "A1",
            "Requirement Coverage",
            "PASS" if story_ac_ok else "FAIL",
            f"{len(stories)} stories, {len(acceptance_criteria)} AC lines",
        ),
        (
            "A2",
            "AC Testability",
            "PASS" if ac_testable_ok else "FAIL",
            "All ACs are BDD/measurable" if ac_testable_ok else f"{len(failing_criteria)} AC lines need tighter wording",
        ),
        (
            "A3",
            "Flow Completeness",
            "PASS" if flow_ok else "FAIL",
            f"{len(flows)} flows extracted" if flow_ok else "Missing or malformed start/end flow definitions",
        ),
        (
            "A4",
            "Non-goal Alignment",
            "PASS" if non_goal_ok else "FAIL",
            "No lexical overlap found" if non_goal_ok else f"{len(non_goal_conflicts)} potential requirement/non-goal conflicts",
        ),
        (
            "A5",
            "UI Coverage",
            "PASS" if ui_ok else "FAIL",
            "UI screens map to user stories" if ui_ok else f"{len(screen_gaps)} screens have no matching story",
        ),
    ]

    result = "PASS" if all(check[2] == "PASS" for check in checks) and not placeholders else "GAPS_FOUND"

    lines = [
        f"# Analyze Gate Report — {prd_path.stem}",
        "",
        "## Summary",
        f"- PRD: `{prd_path}`",
        f"- UI Brief: `{ui_path}`" if ui_text else "- UI Brief: none",
        f"- Result: **{result}**",
        "",
        "## Checks",
        format_table(["#","Criterion","Status","Notes"], checks),
        "",
        "## Evidence",
        f"- User stories extracted: {len(stories)}",
        f"- Acceptance criteria extracted: {len(acceptance_criteria)}",
        f"- Flows extracted: {len(flows)}",
        f"- Non-goals extracted: {len(non_goals)}",
        f"- Screens extracted: {len(screens)}" if ui_text else "- Screens extracted: N/A",
        "",
    ]

    if failing_criteria:
        lines.extend(
            [
                "### Untestable Acceptance Criteria",
                *[f"- {item}" for item in failing_criteria],
                "",
            ]
        )

    if non_goal_conflicts:
        lines.extend(
            [
                "### Potential Requirement / Non-goal Conflicts",
                *[f"- {item}" for item in non_goal_conflicts],
                "",
            ]
        )

    if ui_text and (screen_gaps or story_gaps):
        lines.append("### UI Coverage Gaps")
        if screen_gaps:
            lines.extend(f"- Screen without clear PRD story match: {screen}" for screen in screen_gaps)
        if story_gaps:
            lines.extend(f"- Story without clear UI surface match: {story}" for story in story_gaps)
        lines.append("")

    if placeholders:
        lines.extend(
            [
                "### Unresolved Placeholders",
                *[f"- {item}" for item in placeholders],
                "",
            ]
        )

    write_text(args.output, "\n".join(lines).rstrip() + "\n")

    print(
        json.dumps(
            {
                "result": result,
                "checks": [{"code": code, "status": status} for code, _, status, _ in checks],
                "hotspots": {
                    "untestable_ac": failing_criteria,
                    "non_goal_conflicts": non_goal_conflicts,
                    "screen_gaps": screen_gaps,
                    "story_gaps": story_gaps[:5],
                    "placeholders": placeholders,
                },
                "report_path": str(Path(args.output)),
            },
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
