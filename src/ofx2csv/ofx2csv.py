import csv
import re
from datetime import datetime
from typing import IO, Union

from ofxparse import OfxParser

ACCOUNTS_HEADER = [
    "account",
    "id",
    "type",
    "balance",
    "balance_date",
    "available_balance",
    "available_balance_date",
]

TRANSACTIONS_HEADER = ["date", "account", "id", "desc", "amount"]


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
    def __init__(self, adjustments: dict[str, dict[str, str]] | None = None):
        self.adjustments = adjustments or {}
        self.accounts = []
        self.transactions = []

    def add_ofx(self, nickname: str, filename_or_fp: Union[str, IO]):
        if isinstance(filename_or_fp, str):
            with open(filename_or_fp) as fp:
                ofx = OfxParser.parse(fp)
        else:
            ofx = OfxParser.parse(filename_or_fp)
        self.accounts.append(
            [
                nickname,
                lower(ofx.account.account_id),
                lower(ofx.account.account_type),
                ofx.account.statement.balance,
                clean_date(ofx.account.statement.balance_date),
                ofx.account.statement.available_balance,
                clean_date(ofx.account.statement.available_balance_date),
            ]
        )
        for tx in ofx.account.statement.transactions:
            self.transactions.append((nickname, tx))

    def write_accounts(self, writer: csv.writer):
        writer.writerow(ACCOUNTS_HEADER)
        for account in self.accounts:
            writer.writerow(account)

    def write_transactions(self, writer: csv.writer):
        writer.writerow(TRANSACTIONS_HEADER)
        for nickname, tx in sorted(
            self.transactions, key=lambda pair: pair[1].date, reverse=True
        ):
            adjustment = self.adjustments.get(f"{nickname}:{tx.id}")
            if adjustment:
                if "exclude" in adjustment:
                    continue
                if "date" in adjustment:
                    tx.date = datetime.strptime(adjustment["date"], "%Y-%m-%d")
                if "amount" in adjustment:
                    tx.amount = adjustment["amount"]
            writer.writerow(
                [
                    clean_date(tx.date),
                    nickname,
                    tx.id,
                    clean_desc(tx.payee + " " + clean_memo(tx.memo)),
                    tx.amount,
                ]
            )
