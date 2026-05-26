#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Sequence

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "if",
    "in",
    "into",
    "is",
    "it",
    "no",
    "not",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "then",
    "this",
    "to",
    "when",
    "with",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+(.*\S)\s*$", re.MULTILINE)
CHECKLIST_RE = re.compile(r"^\s*[-*]\s+\[[ xX]\]\s+(.*\S)\s*$", re.MULTILINE)


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str | Path, content: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def collect_sections(text: str) -> list[tuple[int, str, str]]:
    matches = list(HEADING_RE.finditer(text))
    sections: list[tuple[int, str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((len(match.group(1)), match.group(2).strip(), text[start:end].strip()))
    return sections


def section_text(text: str, titles: Sequence[str]) -> str:
    wanted = {title.lower() for title in titles}
    chunks = [content for _, title, content in collect_sections(text) if title.lower() in wanted]
    return "\n\n".join(chunk for chunk in chunks if chunk)


def list_items(text: str) -> list[str]:
    return [match.group(1).strip() for match in BULLET_RE.finditer(text)]


def checklist_items(text: str) -> list[str]:
    return [match.group(1).strip() for match in CHECKLIST_RE.finditer(text)]


def normalize_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"[*_#>|]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9][a-z0-9_-]{1,}", normalize_inline(text).lower())
    return {token for token in tokens if token not in STOPWORDS}


def keyword_overlap(left: str, right: str) -> float:
    left_tokens = tokenize(left)
    right_tokens = tokenize(right)
    if not left_tokens or not right_tokens:
        return 0.0
    shared = left_tokens & right_tokens
    return len(shared) / max(min(len(left_tokens), len(right_tokens)), 1)


def extract_user_stories(text: str) -> list[str]:
    stories: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        normalized = normalize_inline(stripped)
        if re.search(r"\bas a[n]?\b", normalized, re.IGNORECASE) and re.search(
            r"\bI want to\b", normalized, re.IGNORECASE
        ):
            stories.append(normalized)
    return dedupe(stories)


def extract_acceptance_criteria(text: str) -> list[str]:
    extracted: list[str] = []
    for _, title, content in collect_sections(text):
        if "acceptance criteria" in title.lower():
            extracted.extend(checklist_items(content))
            extracted.extend(
                normalize_inline(line)
                for line in content.splitlines()
                if "given" in line.lower() and "when" in line.lower() and "then" in line.lower()
            )

    if not extracted:
        extracted.extend(
            normalize_inline(item)
            for item in list_items(text)
            if re.search(r"\bgiven\b", item, re.IGNORECASE)
            and re.search(r"\bwhen\b", item, re.IGNORECASE)
            and re.search(r"\bthen\b", item, re.IGNORECASE)
        )
    return dedupe([item for item in extracted if item])


def extract_flows(text: str) -> list[str]:
    flows: list[str] = []
    candidate = section_text(text, ["User Flows", "Key Flows", "Flows"])
    source = candidate or text
    for item in list_items(source):
        if "->" in item or "→" in item:
            flows.append(normalize_inline(item))
    for line in source.splitlines():
        stripped = normalize_inline(line)
        if re.match(r"^\d+\.\s", stripped) and ("->" in stripped or "→" in stripped):
            flows.append(stripped)
    return dedupe(flows)


def extract_non_goals(text: str) -> list[str]:
    return dedupe([normalize_inline(item) for item in list_items(section_text(text, ["Non-Goals", "Out of Scope"]))])


def extract_screen_names(text: str) -> list[str]:
    names: list[str] = []
    for _, title, _ in collect_sections(text):
        lowered = title.lower()
        if lowered.startswith("screen "):
            names.append(title.split(":", 1)[-1].strip() if ":" in title else title)
    primary = section_text(text, ["Primary Screens / Surfaces", "Surface Inventory"])
    for line in primary.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and not re.search(r"-{3,}", stripped):
            parts = [part.strip() for part in stripped.strip("|").split("|")]
            if parts and parts[0].lower() not in {"surface", "component", "screen", "role"}:
                names.append(parts[0])
        elif re.match(r"^\d+\.\s", stripped):
            names.append(re.sub(r"^\d+\.\s*", "", stripped).split(" - ", 1)[0].split(" — ", 1)[0].strip())
    return dedupe([normalize_inline(name) for name in names if name])


def detect_placeholders(text: str) -> list[str]:
    patterns = [r"\[NEEDS CLARIFICATION:[^\]]+\]", r"\bTBD\b", r"\bTODO\b", r"\[ASSUMPTION\]"]
    matches: list[str] = []
    for pattern in patterns:
        matches.extend(match.group(0) for match in re.finditer(pattern, text, re.IGNORECASE))
    return dedupe(matches)


def is_testable_acceptance_criterion(item: str) -> bool:
    normalized = normalize_inline(item)
    if re.search(r"\bgiven\b", normalized, re.IGNORECASE) and re.search(r"\bwhen\b", normalized, re.IGNORECASE) and re.search(
        r"\bthen\b", normalized, re.IGNORECASE
    ):
        return True
    if re.search(r"\b\d+(\.\d+)?\b", normalized):
        return True
    measurable_terms = ("within", "less than", "more than", "at least", "under", "no more than")
    return any(term in normalized.lower() for term in measurable_terms)


def format_table(headers: Sequence[str], rows: Iterable[Sequence[str]]) -> str:
    row_list = list(rows)
    header_line = "| " + " | ".join(headers) + " |"
    divider = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in row_list]
    return "\n".join([header_line, divider, *body])


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def feature_stem(path: str | Path) -> str:
    stem = Path(path).stem
    for suffix in ("-requirements", "-ui-brief", "-analyze-report", "-readiness"):
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem
