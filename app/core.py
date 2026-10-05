"""CSV validation and decimal aggregation, independent of the CLI."""

import csv
from decimal import Decimal, DecimalException, Inexact, localcontext
from pathlib import Path


def summarize_csv(path: Path, column: str = "amount") -> dict[str, str | int]:
    count = 0
    total = Decimal("0")

    with path.open(encoding="utf-8-sig", newline="") as source, localcontext() as context:
        context.prec = 28
        context.traps[Inexact] = True
        reader = csv.DictReader(source, strict=True)
        headers = reader.fieldnames
        if not headers or any(not header.strip() for header in headers):
            raise ValueError("CSV must have non-empty headers.")
        if len(set(headers)) != len(headers):
            raise ValueError("CSV headers must be unique.")
        if column not in headers:
            raise ValueError(f"Missing column: {column!r}.")

        for row in reader:
            line = reader.line_num
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"CSV line {line}: field count differs from headers.")
            raw = row[column].strip()
            try:
                amount = Decimal(raw)
            except DecimalException as exc:
                raise ValueError(f"CSV line {line}: invalid number {raw!r}.") from exc
            if not amount.is_finite():
                raise ValueError(f"CSV line {line}: number must be finite.")
            try:
                total += amount
            except DecimalException as exc:
                raise ValueError(
                    f"CSV line {line}: value or total exceeds decimal precision/range."
                ) from exc
            count += 1

    return {"column": column, "rows": count, "total": str(total)}
