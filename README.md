# ofx2csv

Convert OFX to CSV

## Purpose
This package is intended to help merge and normalize one or more QFX/OFX files (Quicken/Quickbooks format) into CSV for import into a spreadsheet.

CSV export formats tend to vary in structure between financial institutions and financial applications. Quicken exports have a consistent format, but are obviously not directly importable into a spreadsheet program.

`ofx2csv` helps you merge transactions from multiple exports into a single CSV, like you'd do with Mint, YNAB, or other budgeting programs.

This class takes as input one or more OFX files and outputs two CSV files: one for accounts and one for transactions.

Accounts are assigned unique nicknames for easy reference.

## Usage

Command line interface

```bash
ofx2csv [-h] [-j adjustments.json] [-a accounts-out.csv] [-t transactions-out.csv] nickname1:file1.ofx [nickname2:file2.ofx ...]
```

Python interface

```python
converter = Ofx2Csv()
converter.add_ofx("mybank", "bank_transactions.qfx")
converter.add_ofx("myvisa", "visa_statement.qfx")
converter.write_accounts(csv.writer(open("accounts-out.csv", "w")))
converter.write_transactions(csv.writer(open("transactions-out.csv", "w")))
```

## Adjustments

Sometimes you need to apply adjustments to the data before you import it. For example, you might want to change the date of a transaction or exclude it from the import.

To do this, you can maintain set of adjustments for specific transactions. Use the account nickname and the transaction ID to adjust one or more properties, or to exclude it. This file can be passed to ofx2csv with the `-j` option, or passed in as a `dict` to the `Ofx2Csv` constructor.

```json
{
    "nickname1:123": {
        "date": "2024-06-01"
    },
    "nickname1:456": {
        "amount": "123.45"
    },
    "nickname2:789": {
        "exclude": true
    }
}
```