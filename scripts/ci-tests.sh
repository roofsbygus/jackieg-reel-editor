#!/usr/bin/env bash
# Runs every test file on its own with a time limit, so one hung test (a leftover Chrome holding the output pipe open)
# can't stall the whole run. Output goes to a log file first, then is printed. Exit 1 if any test failed.
set -u
cd "$(dirname "$0")/.."
export CHROME="${CHROME:-$(command -v google-chrome || command -v chromium || true)}"
fail=0; n=0
for t in tests/test_*.py tests/test_*.mjs; do
  [ -e "$t" ] || continue; n=$((n + 1))
  case "$t" in *.py) cmd=(python3 "$t");; *.mjs) cmd=(node --test-force-exit "$t");; esac
  timeout -k 10 300 "${cmd[@]}" < /dev/null > test.log 2>&1; rc=$?
  cat test.log
  pkill -f -- '--user-data-dir=.*thumb-ui-' 2>/dev/null || true   # only the Chrome the UI test started
  if [ $rc -ne 0 ]; then echo "FAILED: $t (exit $rc)"; fail=$((fail + 1)); else echo "ok: $t"; fi
done
echo "tests: $((n - fail)) of $n passed"
[ $fail -eq 0 ]
