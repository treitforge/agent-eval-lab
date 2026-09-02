"""Stateful parcel scan accounting."""

from __future__ import annotations

from collections.abc import Iterable


def normalize_scan_id(value: str) -> str:
    """Return the canonical form of one parcel identifier."""

    return value.strip().upper()


class ScanLedger:
    """Keep unique parcel identifiers in first-seen order."""

    def __init__(self) -> None:
        self._scans: list[str] = []

    def ingest(self, scan_ids: Iterable[str]) -> int:
        """Add one upload batch and return the total unique parcel count."""

        batch_seen: set[str] = set()
        for raw_scan_id in scan_ids:
            scan_id = normalize_scan_id(raw_scan_id)
            if scan_id and scan_id not in batch_seen:
                batch_seen.add(scan_id)
                self._scans.append(scan_id)
        return self.total

    @property
    def total(self) -> int:
        """Return the current unique parcel count."""

        return len(self._scans)

    def snapshot(self) -> tuple[str, ...]:
        """Return parcel identifiers in first-seen order."""

        return tuple(self._scans)
