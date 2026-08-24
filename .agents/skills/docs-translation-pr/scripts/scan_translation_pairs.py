#!/usr/bin/env python3
"""Inventory English/Chinese MDX pairs and compare basic MDX structure."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
TAG_RE = re.compile(r"(</?)([A-Za-z][\w.-]*)\b[^<>]*?(\/?>)")


def mdx_files(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*.mdx")
        if ".git" not in path.parts
    }


def structure(path: Path) -> dict[str, list[str] | int]:
    headings: list[str] = []
    tags: list[str] = []
    fences: list[str] = []
    in_fence = False
    fence_marker = ""

    for line in path.read_text(encoding="utf-8").splitlines():
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
                fences.append(fence_match.group(2).strip())
            elif line.lstrip().startswith(fence_marker):
                in_fence = False
            continue
        if in_fence:
            continue
        heading_match = HEADING_RE.match(line)
        if heading_match:
            headings.append(heading_match.group(1))
        tags.extend(
            f"{opening}{name}{closing}"
            for opening, name, closing in TAG_RE.findall(line)
        )

    return {
        "headings": headings,
        "tags": tags,
        "fences": fences,
        "lines": len(path.read_text(encoding="utf-8").splitlines()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    english_root = root / ""
    chinese_root = root / "zh"
    english = {path for path in mdx_files(english_root) if not path.startswith("zh/")}
    chinese = {
        path.removeprefix("zh/")
        for path in mdx_files(chinese_root)
    }

    print("Bilingual MDX inventory")
    print(f"English pages: {len(english)}")
    print(f"Chinese pages: {len(chinese)}")
    print(f"Missing Chinese pages: {len(english - chinese)}")
    for path in sorted(english - chinese):
        print(f"  MISSING zh/{path}")
    print(f"Orphan Chinese pages: {len(chinese - english)}")
    for path in sorted(chinese - english):
        print(f"  ORPHAN zh/{path}")

    print("\nPaired structure differences:")
    differences = 0
    for relative_path in sorted(english & chinese):
        source = structure(root / relative_path)
        target = structure(root / "zh" / relative_path)
        differing_keys = [
            key for key in ("headings", "tags", "fences") if source[key] != target[key]
        ]
        if differing_keys:
            differences += 1
            print(f"  DIFF {relative_path}: {', '.join(differing_keys)}")
    if differences == 0:
        print("  none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())