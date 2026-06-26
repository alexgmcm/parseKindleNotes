#!/usr/bin/env python3

import argparse


def diff_files(file1, file2, output_file):
    # Read lines, stripping trailing newlines
    with open(file1, "r", encoding="utf-8") as f:
        lines1 = {line.rstrip("\n") for line in f}

    with open(file2, "r", encoding="utf-8") as f:
        lines2 = {line.rstrip("\n") for line in f}

    # Lines that appear in exactly one file
    unique_lines = sorted(lines1.symmetric_difference(lines2))

    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        for line in unique_lines:
            f.write(line + "\n")

    print(f"Wrote {len(unique_lines)} lines to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find lines that appear in exactly one of two text files."
    )
    parser.add_argument("file1", help="First input file")
    parser.add_argument("file2", help="Second input file")
    parser.add_argument("output", help="Output file")

    args = parser.parse_args()

    diff_files(args.file1, args.file2, args.output)

