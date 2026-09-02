#!/bin/bash
set -uo pipefail

mkdir -p /logs/verifier
python -m unittest discover -s /tests -p 'test_*.py' -v 2>&1 | tee /logs/verifier/test-stdout.txt
status=${PIPESTATUS[0]}
if [ "$status" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
exit 0
