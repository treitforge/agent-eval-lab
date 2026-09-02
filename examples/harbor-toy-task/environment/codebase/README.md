# Scan Ledger

Scan Ledger counts unique parcel scans from handheld-device uploads.

```python
from scan_ledger import ScanLedger

ledger = ScanLedger()
ledger.ingest(["PKG-100", "pkg-100", "PKG-101"])
print(ledger.total)
```

Identifiers are trimmed and converted to upper case. Blank identifiers are ignored. `snapshot()` returns identifiers in first-seen order.

Run the tests with:

```bash
python -m unittest discover -s tests -v
```
