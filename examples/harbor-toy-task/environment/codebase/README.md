# Scan Ledger

Scan Ledger counts unique parcel scans from handheld scanner uploads.

```python
from scan_ledger import ScanLedger

ledger = ScanLedger()
ledger.ingest(["PKG-100", "pkg-100", "PKG-101"])
print(ledger.total)
```

Scan Ledger removes spaces at the ends of each identifier. It converts each identifier to upper case. It ignores blank identifiers.

The `snapshot()` method returns the identifiers in first-seen order.

Run the tests with this command:

```bash
python -m unittest discover -s tests -v
```
