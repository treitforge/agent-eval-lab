from __future__ import annotations

import unittest

from scan_ledger import ScanLedger


class CrossBatchScanTests(unittest.TestCase):
    def test_retry_in_later_batch_does_not_increase_total(self) -> None:
        ledger = ScanLedger()
        self.assertEqual(ledger.ingest(["PKG-100", "PKG-101"]), 2)

        total = ledger.ingest(["pkg-100", "PKG-102"])

        self.assertEqual(total, 3)
        self.assertEqual(ledger.snapshot(), ("PKG-100", "PKG-101", "PKG-102"))

    def test_multiple_retries_preserve_first_seen_order(self) -> None:
        ledger = ScanLedger()
        ledger.ingest(["A-2", "A-1"])
        ledger.ingest(["A-1", "a-2", "A-3"])
        ledger.ingest(["A-3", "A-1"])

        self.assertEqual(ledger.total, 3)
        self.assertEqual(ledger.snapshot(), ("A-2", "A-1", "A-3"))

    def test_empty_batches_do_not_change_state(self) -> None:
        ledger = ScanLedger()
        ledger.ingest(["PKG-900"])

        self.assertEqual(ledger.ingest([]), 1)
        self.assertEqual(ledger.ingest([" ", "\t"]), 1)
        self.assertEqual(ledger.snapshot(), ("PKG-900",))


if __name__ == "__main__":
    unittest.main()
