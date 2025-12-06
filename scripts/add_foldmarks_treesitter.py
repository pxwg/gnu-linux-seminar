#!/usr/bin/env python3
"""
Add foldmarkers to markdown file for slide presentation in Neovim.
This script uses tree-sitter for reliable markdown parsing.
"""

import sys
from typing import List, Tuple
from dataclasses import dataclass

try:
    from tree_sitter import Language, Parser
    import tree_sitter_markdown
except ImportError:
    print("Error: tree-sitter dependencies not installed.", file=sys.stderr)
    print(
        "Please install: pip install tree-sitter tree-sitter-markdown", file=sys.stderr
    )
    sys.exit(1)


@dataclass
class Heading:
    """Represents a markdown heading with its metadata."""

    level: int
    line_num: int
    start_byte: int
    end_byte: int
    text: str


def extract_headings(tree, source_code: bytes) -> List[Heading]:
    """
    Extract all headings from the tree-sitter parse tree.

    Args:
        tree: Tree-sitter parse tree
        source_code: Original source code as bytes

    Returns:
        List of Heading objects
    """
    headings = []

    def traverse(node):
        # ATX heading nodes in tree-sitter-markdown
        if node.type == "atx_heading":
            # Get the heading level by counting # markers
            heading_marker = None
            heading_content = None

            for child in node.children:
                if child.type == "atx_h1_marker":
                    level = 1
                    heading_marker = child
                elif child.type == "atx_h2_marker":
                    level = 2
                    heading_marker = child
                elif child.type == "atx_h3_marker":
                    level = 3
                    heading_marker = child
                elif child.type == "atx_h4_marker":
                    level = 4
                    heading_marker = child
                elif child.type == "atx_h5_marker":
                    level = 5
                    heading_marker = child
                elif child.type == "atx_h6_marker":
                    level = 6
                    heading_marker = child
                elif child.type == "inline":
                    heading_content = child

            if heading_marker and heading_content:
                text = source_code[
                    heading_content.start_byte : heading_content.end_byte
                ].decode("utf-8")
                headings.append(
                    Heading(
                        level=level,
                        line_num=node.start_point[0],
                        start_byte=node.start_byte,
                        end_byte=node.end_byte,
                        text=text.strip(),
                    )
                )

        # Recursively traverse children
        for child in node.children:
            traverse(child)

    traverse(tree.root_node)
    return headings


def insert_foldmarkers(source_code: str, headings: List[Heading]) -> str:
    """
    Insert vim foldmarkers into the content.

    Args:
        source_code: Original source code
        headings: List of Heading objects

    Returns:
        Modified content with foldmarkers
    """
    lines = source_code.split("\n")
    result = []
    last_fold_levels = []  # Stack to track open folds

    for i, line in enumerate(lines):
        # Check if this line has a heading
        heading = None
        for h in headings:
            if h.line_num == i:
                heading = h
                break

        if heading:
            fold_level = heading.level - 1

            # Close any folds that are at the same or deeper level
            while last_fold_levels and last_fold_levels[-1] >= fold_level:
                closed_level = last_fold_levels.pop()
                result.append("<!-- " + "}" * 3 + str(closed_level) + " -->")
                result.append("")

            # Add the heading line with opening foldmarker
            result.append(line.rstrip() + " <!-- " + "{" * 3 + str(fold_level) + " -->")
            last_fold_levels.append(fold_level)
        else:
            result.append(line)

    # Close all remaining open folds at the end
    while last_fold_levels:
        closed_level = last_fold_levels.pop()
        result.append("")
        result.append("<!-- " + "}" * 3 + str(closed_level) + " -->")

    return "\n".join(result)


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
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Initialize tree-sitter parser
    try:
        MARKDOWN_LANGUAGE = Language(tree_sitter_markdown.language())
        parser = Parser(MARKDOWN_LANGUAGE)
    except Exception as e:
        print(f"Error initializing tree-sitter: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse the markdown
    tree = parser.parse(source_code.encode("utf-8"))

    # Extract headings
    headings = extract_headings(tree, source_code.encode("utf-8"))

    if not headings:
        print("Warning: No headings found in the file.", file=sys.stderr)
        return

    # Insert foldmarkers
    result = insert_foldmarkers(source_code, headings)

    # Determine output path
    if output_file is None:
        output_file = input_file

    # Write output
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Successfully added foldmarks to '{output_file}'")
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_foldmarks_treesitter.py <input_file> [output_file]")
        print("If output_file is not specified, input file will be modified in place.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    add_foldmarks(input_file, output_file)
