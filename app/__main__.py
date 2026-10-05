"""Run from the project root with: python -m app."""

import argparse
import csv
import json
import sys
from pathlib import Path

from .core import summarize_csv


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize a numeric CSV column.")
    parser.add_argument("--input", type=Path, required=True, help="UTF-8 CSV file")
    parser.add_argument("--column", default="amount", help="Column name (default: amount)")
    args = parser.parse_args(argv)

    try:
        result = summarize_csv(args.input, args.column)
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
