# Scan Ledger public toy task

This directory contains a complete Harbor teaching fixture. It shows the file layout, agent environment, verifier, patch collection, and result flow.

The code models parcel scan uploads. The baseline handles duplicate identifiers in one batch. It does not keep the correct state across multiple batches.

The public tests pass in the baseline image. The task verifier fails in the same image. A correct change makes both test sets pass.

The instruction and verifier are public. Therefore, do not use this task for a model comparison. Use it to test an installation and learn Harbor.
