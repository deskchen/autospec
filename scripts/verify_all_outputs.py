#!/usr/bin/env python3
"""
Verify all generated C files under the outputs directory and emit a simple
summary table with Program and Success columns.
"""

import argparse
from pathlib import Path

from autospec.pipeline.autospec_runner import AutoSpecRunner


def format_success(verdict_type: str) -> str:
    """Return a simple PASS/FAIL string for the verdict type."""
    return "PASS" if verdict_type.lower() == "valid" else "FAIL"


def main():
    parser = argparse.ArgumentParser(description="Verify all generated C files in outputs.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/annotated"),
        help="Root directory containing generated/annotated C files.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="Verification timeout in seconds (passed to Frama-C).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each verdict message as it is produced.",
    )
    args = parser.parse_args()

    if not args.output_dir.exists():
        raise SystemExit(f"Output directory not found: {args.output_dir}")

    files = sorted(args.output_dir.rglob("*.c"))
    if not files:
        raise SystemExit(f"No C files found under {args.output_dir}")

    runner = AutoSpecRunner(timeout=args.timeout)

    results = []
    for c_file in files:
        verdict = runner.run(c_file)
        results.append((c_file, verdict))
        if args.verbose:
            print(f"[VERDICT] {c_file}: {verdict}")

    # Print consolidated table.
    print("\nProgram\tSuccess")
    for c_file, verdict in results:
        rel = c_file.relative_to(args.output_dir)
        print(f"{rel}\t{format_success(verdict.verdict_type.value)}")

    total = len(results)
    passed = sum(1 for _, v in results if v.is_valid())
    print(f"\nSummary: {passed}/{total} passed")


if __name__ == "__main__":
    main()

