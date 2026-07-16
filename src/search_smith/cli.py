"""Command line interface for search-smith."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from search_smith.exceptions import SearchSmithError
from search_smith.search import search


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="search-smith",
        description="Search the web through search-smith providers.",
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("--count", type=int, default=10, help="Number of results")
    parser.add_argument("--offset", type=int, default=0, help="Zero-based result page")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the search-smith CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        results = search(args.query, count=args.count, offset=args.offset)
    except (SearchSmithError, ValueError) as exc:
        print(f"search-smith: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps([result.to_dict() for result in results], indent=2))
        return 0

    for result in results:
        print(f"{result.rank}. {result.title}")
        print(f"   {result.url}")
        if result.snippet:
            print(f"   {result.snippet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
