import csv
import re
from datetime import datetime
from typing import IO, Union

from ofxparse import OfxParser

ACCOUNTS_HEADER = [
    "tag",
    "id",
    "type",
    "balance",
    "balance_date",
    "available_balance",
    "available_balance_date",
]

TRANSACTIONS_HEADER = ["date", "tag", "id", "desc", "amount"]


def clean_memo(s: str):
    return re.sub(r"[,;(].*$", "", s)


def clean_desc(s: str):
    s = s.lower()
    s = re.sub(r"(\w)\*+(\w)", r"\1-\2", s)
    s = re.sub(r"(\b\*+|\*+\b)", "", s)
    s = s.strip()
    return s


def clean_date(d: datetime):
    return d.strftime("%Y-%m-%d")


def lower(s: str | None):
    return s.lower() if s else None


class Ofx2Csv:
    def __init__(self, overrides: dict[str, dict[str, str]] | None = None):
        self.overrides = overrides or {}
        self.accounts = []
        self.transactions = []

    def add_ofx(self, tag: str, filename_or_fp: Union[str, IO]):
        if isinstance(filename_or_fp, str):
            with open(filename_or_fp) as fp:
                ofx = OfxParser.parse(fp)
        else:
            ofx = OfxParser.parse(filename_or_fp)
        self.accounts.append(
            [
                tag,
                lower(ofx.account.account_id),
                lower(ofx.account.account_type),
                ofx.account.statement.balance,
                clean_date(ofx.account.statement.balance_date),
                ofx.account.statement.available_balance,
                clean_date(ofx.account.statement.available_balance_date),
            ]
        )
        for tx in ofx.account.statement.transactions:
            self.transactions.append((tag, tx))

    def write_accounts(self, writer: csv.writer):
        writer.writerow(ACCOUNTS_HEADER)
        for account in self.accounts:
            writer.writerow(account)

    def write_transactions(self, writer: csv.writer):
        writer.writerow(TRANSACTIONS_HEADER)
        for tag, tx in sorted(
            self.transactions, key=lambda pair: pair[1].date, reverse=True
        ):
            override = self.overrides.get(f"{tag}:{tx.id}")
            if override:
                if "exclude" in override:
                    continue
                if "date" in override:
                    tx.date = datetime.strptime(override["date"], "%Y-%m-%d")
                if "amount" in override:
                    tx.amount = override["amount"]
            writer.writerow(
                [
                    clean_date(tx.date),
                    tag,
                    tx.id,
                    clean_desc(tx.payee + " " + clean_memo(tx.memo)),
                    tx.amount,
                ]
            )
