"""CLI: python -m llmguard run suites/owasp-llm01.txt --seed 7"""

from __future__ import annotations

import argparse

from .runner import print_summary, run_suite


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="llmguard", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="run a payload suite against the configured endpoint")
    run.add_argument("suite", help="path to payload suite (family | expect | text per line)")
    run.add_argument("--seed", type=int, default=0, help="seed for encoding rotation")
    run.add_argument("--out", default="reports", help="report directory")

    args = parser.parse_args(argv)
    if args.cmd == "run":
        report = run_suite(args.suite, seed=args.seed, out_dir=args.out)
        print_summary(report)
        failing = {f: s for f, s in report["summary"].items() if s["verdict"] != "pass"}
        return 1 if failing else 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
