#!/usr/bin/env python3
"""Validate SKILL.md against Anthropic's Agent Skills specification.

Checks:
- YAML frontmatter exists and parses cleanly
- `name` is present, ≤64 chars, lowercase + hyphens/numbers only,
  doesn't contain XML tags or reserved words ("anthropic", "claude")
- `description` is present, non-empty, ≤1024 chars, no XML tags
- Body length is reasonable (warn at >500 lines per Anthropic guidance)
- All references/*.md files mentioned in SKILL.md actually exist

Run: python scripts/validate_skill.py [path/to/SKILL.md]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
RESERVED_WORDS = {"anthropic", "claude"}
XML_TAG_PATTERN = re.compile(r"<[^>]+>")
MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024
SOFT_BODY_LINES = 500


class ValidationError(Exception):
    pass


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    """Parse YAML-ish frontmatter without requiring PyYAML.

    Returns (fields, body_lines). Frontmatter is the block between the
    first two `---` lines. Multi-line values are joined.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValidationError("SKILL.md must start with '---' frontmatter delimiter")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValidationError("frontmatter missing closing '---' delimiter")

    fields: dict[str, str] = {}
    current_key: str | None = None
    for raw in lines[1:end_idx]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", raw)
        if match and not raw.startswith((" ", "\t")):
            key, value = match.group(1), match.group(2)
            fields[key] = value.strip().strip("'\"")
            current_key = key
        elif current_key is not None:
            fields[current_key] += " " + raw.strip()

    return fields, lines[end_idx + 1 :]


def validate_name(name: str) -> list[str]:
    errors: list[str] = []
    if not name:
        errors.append("name: missing or empty")
        return errors
    if len(name) > MAX_NAME_LEN:
        errors.append(f"name: too long ({len(name)} > {MAX_NAME_LEN})")
    if not SKILL_NAME_PATTERN.match(name):
        errors.append(
            f"name: must match {SKILL_NAME_PATTERN.pattern} "
            "(lowercase letters, numbers, hyphens only)"
        )
    if XML_TAG_PATTERN.search(name):
        errors.append("name: must not contain XML tags")
    lower = name.lower()
    for reserved in RESERVED_WORDS:
        if reserved in lower:
            errors.append(f"name: must not contain reserved word '{reserved}'")
    return errors


def validate_description(desc: str) -> list[str]:
    errors: list[str] = []
    if not desc:
        errors.append("description: missing or empty")
        return errors
    if len(desc) > MAX_DESC_LEN:
        errors.append(f"description: too long ({len(desc)} > {MAX_DESC_LEN})")
    if XML_TAG_PATTERN.search(desc):
        errors.append("description: must not contain XML tags")
    return errors


def validate_references(skill_path: Path, body_lines: list[str]) -> list[str]:
    """Check that every references/*.md file mentioned in SKILL.md exists."""
    body = "\n".join(body_lines)
    pattern = re.compile(r"`(references/[^`]+\.md)`")
    referenced = set(pattern.findall(body))
    errors: list[str] = []
    for ref in sorted(referenced):
        full_path = skill_path.parent / ref
        if not full_path.exists():
            errors.append(f"references: SKILL.md mentions `{ref}` but file does not exist")
    return errors


def validate_body_length(body_lines: list[str]) -> list[str]:
    n = len(body_lines)
    if n > SOFT_BODY_LINES:
        return [
            f"body: {n} lines exceeds Anthropic's recommended {SOFT_BODY_LINES}-line "
            "soft cap. Consider moving detail into references/ files (progressive disclosure)."
        ]
    return []


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    skill_path = Path(args[0]) if args else Path("SKILL.md")

    if not skill_path.exists():
        print(f"error: SKILL.md not found at {skill_path}", file=sys.stderr)
        return 2

    text = skill_path.read_text(encoding="utf-8")
    try:
        fields, body_lines = parse_frontmatter(text)
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(validate_name(fields.get("name", "")))
    errors.extend(validate_description(fields.get("description", "")))
    errors.extend(validate_references(skill_path, body_lines))
    warnings.extend(validate_body_length(body_lines))

    if errors:
        print(f"FAIL: {skill_path} has {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: {skill_path}")
    print(f"  name: {fields.get('name')}")
    print(f"  description: {len(fields.get('description', ''))} chars")
    print(f"  body: {len(body_lines)} lines")
    if warnings:
        print(f"  {len(warnings)} warning(s):")
        for warn in warnings:
            print(f"    ! {warn}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
