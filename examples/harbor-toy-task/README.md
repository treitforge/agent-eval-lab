# Scan Ledger public toy task

This directory is a complete Harbor teaching fixture. It demonstrates the file layout, agent environment, independent verifier, patch collection, and result flow.

The code models parcel scan uploads. The baseline handles duplicate identifiers within one upload batch. It does not keep the correct state across multiple batches.

The public codebase tests pass in the baseline image. The task verifier fails in the baseline image. A successful agent change makes both test sets pass.

The instruction and verifier are public. This makes the task unsuitable for model comparison. Use it only to test an installation and learn the workflow.
