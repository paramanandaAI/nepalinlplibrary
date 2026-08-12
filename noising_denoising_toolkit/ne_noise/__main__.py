"""
ne_noise CLI: python -m ne_noise <command>.

Commands:
  demo       run the end-to-end demo (normalization, translit tiers, noise, pairs)
  translit   transliterate a Devanagari/Roman string
  pairs      build denoising pairs from a JSONL file
"""

import argparse
import json
import sys
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _cmd_demo(args) -> None:
    from .demo.demo import run_demo

    run_demo(out_dir=Path(args.out_dir))


def _cmd_translit(args) -> None:
    from .translit.engine import TransliterationEngine

    engine = TransliterationEngine(use_model=args.model)
    out = engine.transliterate(args.text, direction=args.direction)
    print(out)


def _cmd_pairs(args) -> None:
    from .denoise.pairs import make_pairs_from_records, write_jsonl

    records = []
    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    pairs = make_pairs_from_records(
        records,
        text_field=args.field,
        ops=None,
        k=args.k,
        seed=args.seed,
    )
    write_jsonl(pairs, args.output)
    print(f"Wrote {len(pairs)} pairs -> {args.output}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="ne_noise", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_demo = sub.add_parser("demo", help="run the end-to-end demo")
    p_demo.add_argument("--out-dir", default="ne_noise/demo/output")

    p_tr = sub.add_parser("translit", help="transliterate a string")
    p_tr.add_argument("text")
    p_tr.add_argument("--direction", choices=["auto", "dev2rom", "rom2dev"], default="auto")
    p_tr.add_argument("--model", action="store_true", help="try the model tier")

    p_pairs = sub.add_parser("pairs", help="build denoising pairs from JSONL")
    p_pairs.add_argument("input")
    p_pairs.add_argument("output")
    p_pairs.add_argument("--field", default="text")
    p_pairs.add_argument("--k", type=int, default=1)
    p_pairs.add_argument("--seed", type=int, default=None)

    args = parser.parse_args()
    if args.command == "demo":
        _cmd_demo(args)
    elif args.command == "translit":
        _cmd_translit(args)
    elif args.command == "pairs":
        _cmd_pairs(args)


if __name__ == "__main__":
    main()
