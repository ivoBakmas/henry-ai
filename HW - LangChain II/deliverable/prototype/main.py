"""Prototype CLI runner

Usage examples (PowerShell):
  python main.py csv --id V-91827364
  python main.py kb --query "Como abro una cuenta?"
  python main.py llm --query "Cual es el sentido de la vida?"
"""
import argparse
import json
import sys
from typing import Optional

from csv_lookup import find_balance_by_id
from kb_retriever import simple_kb_retrieve
from llm_client import ask_openai


def action_csv(id_value: str):
    res = find_balance_by_id(id_value)
    if not res:
        print("No record found. Ensure the reference CSV exists at ../../solution/data/saldos.csv")
        return
    print(json.dumps(res, ensure_ascii=False, indent=2))


def action_kb(query: str):
    res = simple_kb_retrieve(query)
    print(json.dumps(res, ensure_ascii=False, indent=2))


def action_llm(query: str):
    res = ask_openai(query)
    print(res)


def main(argv: Optional[list] = None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")

    p_csv = subparsers.add_parser("csv")
    p_csv.add_argument("--id", required=True)

    p_kb = subparsers.add_parser("kb")
    p_kb.add_argument("--query", required=True)

    p_llm = subparsers.add_parser("llm")
    p_llm.add_argument("--query", required=True)

    args = parser.parse_args(argv)
    if args.cmd == "csv":
        action_csv(args.id)
    elif args.cmd == "kb":
        action_kb(args.query)
    elif args.cmd == "llm":
        action_llm(args.query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
