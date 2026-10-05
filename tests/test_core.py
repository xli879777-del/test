import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from app.__main__ import main
from app.core import summarize_csv


class SummaryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "input.csv"

    def write_csv(self, text):
        self.path.write_text(text, encoding="utf-8")

    def test_decimal_sum_with_bom_and_negative_value(self):
        self.write_csv("\ufeffname,amount\na,0.10\nb,0.20\nc,-0.05\n")
        self.assertEqual(
            summarize_csv(self.path),
            {"column": "amount", "rows": 3, "total": "0.25"},
        )

    def test_custom_column_and_empty_dataset(self):
        self.write_csv("value\n")
        self.assertEqual(
            summarize_csv(self.path, "value"),
            {"column": "value", "rows": 0, "total": "0"},
        )

    def test_rejects_bad_headers_and_record_shapes(self):
        for content in ("", "name\na\n", "amount,amount\n1,2\n",
                        "amount,\n1,2\n", "name,amount\na\n", "amount\n1,2\n"):
            with self.subTest(content=content):
                self.write_csv(content)
                with self.assertRaises(ValueError):
                    summarize_csv(self.path)

    def test_rejects_invalid_and_nonfinite_numbers(self):
        for value in ("", "abc", "NaN", "Infinity", "-Infinity"):
            with self.subTest(value=value):
                self.write_csv(f"name,amount\na,{value}\n")
                with self.assertRaises(ValueError):
                    summarize_csv(self.path)

    def test_rejects_silent_precision_loss(self):
        self.write_csv("amount\n10000000000000000000000000000\n0.01\n")
        with self.assertRaisesRegex(ValueError, "precision/range"):
            summarize_csv(self.path)

    def test_cli_returns_json(self):
        self.write_csv("amount\n1.25\n")
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(["--input", str(self.path)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["total"], "1.25")

    def test_cli_error_has_no_partial_json(self):
        self.write_csv("amount\n1.25\ninvalid\n")
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = main(["--input", str(self.path)])
        self.assertEqual(code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("Error:", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
