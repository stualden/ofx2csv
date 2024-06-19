import csv
from tempfile import NamedTemporaryFile

from ofx2csv import Ofx2Csv


def test_ofx2csv():
    converter = Ofx2Csv()
    converter.add_ofx("bank", "tests/data/bank.qfx")
    converter.add_ofx("cc", "tests/data/cc.qfx")
    with NamedTemporaryFile("w+") as accounts_file:
        converter.write_accounts(csv.writer(accounts_file))
        accounts_file.flush()
        accounts_file.seek(0)
        reader = csv.reader(accounts_file)
        next(reader)  # header
        accounts = list(reader)
    with NamedTemporaryFile("w+") as transactions_file:
        converter.write_transactions(csv.writer(transactions_file))
        transactions_file.flush()
        transactions_file.seek(0)
        reader = csv.reader(transactions_file)
        next(reader)  # header
        transactions = list(reader)
    assert len(accounts) == 2
    assert len(transactions) == 5
    assert accounts[0] == [
        "bank",
        "myacc",
        "savings",
        "5992.90",
        "2024-06-19",
        "15992.90",
        "2024-06-19",
    ]
    assert transactions[0] == [
        "2024-06-18",
        "cc",
        "202417005426748",
        "jhourney meditation san francisco",
        "-388.08",
    ]
