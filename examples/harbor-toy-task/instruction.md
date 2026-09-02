# Fix duplicate parcel totals across upload batches

Operations reports that the parcel total can increase when a handheld scanner uploads one shift in more than one batch. The same parcel can occur in a later batch because a device retries an upload.

Diagnose the problem in the scan ledger and implement a fix. Preserve the existing identifier normalization and first-seen order. Add or update tests for the behavior that you change. Run the relevant checks before you finish.
