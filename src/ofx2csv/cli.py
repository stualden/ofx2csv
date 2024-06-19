import argparse
import csv
import json

from ofx2csv import Ofx2Csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--overrides",
        type=argparse.FileType("r"),
        help="Optional overrides JSON file",
    )
    parser.add_argument(
        "-a",
        "--accounts",
        type=argparse.FileType("w"),
        help="Accounts CSV output",
        default="accounts.csv",
    )
    parser.add_argument(
        "-t",
        "--transactions",
        type=argparse.FileType("w"),
        help="Transactions CSV output",
        default="transactions.csv",
    )
    parser.add_argument(
        "tag_filename_pairs",
        nargs="+",
        help="One or more pairs of tag:filename.[ofx|qfx] to process",
    )
    args = parser.parse_args()
    overrides = json.load(args.overrides) if args.overrides else {}
    converter = Ofx2Csv(overrides=overrides)
    for pair in args.tag_filename_pairs:
        tag, filename = pair.split(":")
        converter.add_ofx(tag, filename)
    converter.write_accounts(csv.writer(args.accounts))
    converter.write_transactions(csv.writer(args.transactions))
    print(f"Wrote {len(converter.accounts)} accounts to {args.accounts.name}")
    print(
        f"Wrote {len(converter.transactions)} transactions to {args.transactions.name}"
    )


if __name__ == "__main__":
    main()
