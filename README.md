# ofx2csv

Convert OFX to CSV

## Purpose
This package is intended to help merge and normalize one or more QFX/OFX files (Quicken/Quickbooks) into CSV for import into a spreadsheet.

CSV export formats tend to vary between financial institutions and financial applications. Quicken exports have a consistent format, but are obviously not directly importable into a spreadsheet program.

ofx2csv also helps you merge transactions from multiple exports into a single CSV, like you'd do with Mint, YNAB, or other budgeting programs.

This class takes as input one or more OFX files and outputs two CSV files: one for accounts and one for transactions.

Transactions and accounts are assigned unique tags for easy reference.

## Usage

```bash
ofx2csv [-h] [-o overrides.json] [-a accounts.csv] [-t transactions.csv] tag1:file1.ofx [tag2:file2.ofx ...]
```

```python
converter = Ofx2Csv()
converter.add_ofx("mybank", "bank_transactions.qfx")
converter.add_ofx("myvisa", "visa_statement.qfx")
converter.write_accounts(csv.writer(open("accounts.csv", "w")))
converter.write_transactions(csv.writer(open("transactions.csv", "w")))
```

## Overrides

Sometimes you need to apply adjustments to the data. For example, you might want to change the date of a transaction or exclude it from the import.

To do this, you can maintain set of overrides for specific transactions. Use the tag and the transaction ID to adjust one or more properties, or to exclude it. This file can be passed to ofx2csv with the `-o` option, or passed in as a dict to the `Ofx2Csv` constructor.

```json
{
    "tag1:123": {
        "date": "2024-06-01"
    },
    "tag2:456": {
        "amount": "123.45"
    },
    "tag4:012": {
        "exclude": true
    }
}
```