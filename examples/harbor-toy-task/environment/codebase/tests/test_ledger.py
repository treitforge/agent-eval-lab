from __future__ import annotations

import unittest

from scan_ledger import ScanLedger, normalize_scan_id


class ScanLedgerTests(unittest.TestCase):
    def test_normalizes_identifiers(self) -> None:
        self.assertEqual(normalize_scan_id(" pkg-100 \n"), "PKG-100")

    def test_ignores_duplicates_within_one_batch(self) -> None:
        ledger = ScanLedger()

        total = ledger.ingest(["PKG-100", "pkg-100", "PKG-101", ""])

        self.assertEqual(total, 2)
        self.assertEqual(ledger.snapshot(), ("PKG-100", "PKG-101"))


if __name__ == "__main__":
    unittest.main()
