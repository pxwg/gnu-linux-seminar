#!/usr/bin/env python3
"""
Add foldmarkers to markdown file for slide presentation in Neovim.
This script parses the markdown AST and adds vim foldmarkers at each heading.
"""

import re
import sys
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Heading:
    """Represents a markdown heading with its metadata."""

    level: int
    line_num: int
    text: str


def parse_headings(lines: List[str]) -> List[Heading]:
    """
    Parse markdown content and extract all headings with their positions.

    Args:
        lines: List of lines from the markdown file

    Returns:
        List of Heading objects with metadata
    """
    headings = []
    in_code_block = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Track code fence state - must check before any other processing
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        # Match ATX-style headings (# Header)
        # Only match if # is at the very start (no leading whitespace)
        if line.startswith("#"):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append(Heading(level=level, line_num=i, text=text))

    return headings


def calculate_fold_structure(headings: List[Heading]) -> List[Tuple[int, int, int]]:
    """
    Calculate fold structure based on heading hierarchy.

    Args:
        headings: List of Heading objects

    Returns:
        List of tuples (line_num, fold_level, heading_level)
    """
    fold_structure = []

    for i, heading in enumerate(headings):
        # Determine fold level based on heading level
        # Level 1 headers get fold level 0, level 2 get fold level 1, etc.
        fold_level = heading.level - 1

        fold_structure.append((heading.line_num, fold_level, heading.level))

    return fold_structure


def insert_foldmarkers(
    lines: List[str], fold_structure: List[Tuple[int, int, int]]
) -> List[str]:
    """
    Insert vim foldmarkers into the content.

    Args:
        lines: Original lines from the file
        fold_structure: List of (line_num, fold_level, heading_level) tuples

    Returns:
        Modified lines with foldmarkers
    """
    result = []
    last_fold_levels = []  # Stack to track open folds
    in_code_block = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Track code fence state - must check before any other processing
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        # Don't add foldmarkers inside code blocks
        if in_code_block:
            result.append(line)
            continue

        # Check if this line needs a foldmarker
        fold_info = None
        for line_num, fold_level, heading_level in fold_structure:
            if line_num == i:
                fold_info = (fold_level, heading_level)
                break

        if fold_info:
            fold_level, heading_level = fold_info

            # Close any folds that are at the same or deeper level
            while last_fold_levels and last_fold_levels[-1] >= fold_level:
                closed_level = last_fold_levels.pop()
                # Add closing marker before the new heading
                # Use string concatenation to avoid f-string escaping issues
                result.append("<!-- " + "}" * 3 + str(closed_level) + " -->\n")
                result.append("\n")

            # Add the heading line with opening foldmarker
            # Use string concatenation to avoid f-string escaping issues
            result.append(
                line.rstrip() + " <!-- " + "{" * 3 + str(fold_level) + " -->\n"
            )
            last_fold_levels.append(fold_level)
        else:
            result.append(line)

    # Close all remaining open folds at the end
    while last_fold_levels:
        closed_level = last_fold_levels.pop()
        result.append("\n")
        result.append("<!-- " + "}" * 3 + str(closed_level) + " -->\n")

    return result


def add_foldmarks(input_file: str, output_file: str = None) -> None:
    """
    Main function to add foldmarks to markdown file.

    Args:
        input_file: Path to input markdown file
        output_file: Path to output file (if None, will overwrite input)
    """
    # Read input file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse headings
    headings = parse_headings(lines)

    if not headings:
        print("Warning: No headings found in the file.", file=sys.stderr)
        return

    # Calculate fold structure
    fold_structure = calculate_fold_structure(headings)

    # Insert foldmarkers
    result_lines = insert_foldmarkers(lines, fold_structure)

    # Determine output path
    if output_file is None:
        output_file = input_file

    # Write output
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(result_lines)
        print(f"Successfully added foldmarks to '{output_file}'")
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_foldmarks.py <input_file> [output_file]")
        print("If output_file is not specified, input file will be modified in place.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    add_foldmarks(input_file, output_file)
