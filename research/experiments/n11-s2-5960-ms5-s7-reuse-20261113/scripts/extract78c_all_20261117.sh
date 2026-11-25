#!/bin/sh
# Blind certificate extraction for the 11 sweep WIN7-D10 roots of cost78c
# (bits 1, 4, 9, 30, 49, 69, 75, 79, 100, 114, 116). One argument: the bit to extract.
# Per-bit fresh process, MS=1<<23 (single-line substitution on the
# repo-verbatim extractor_exact; published prescription, ~-30% extraction
# nodes vs MS=1<<18, same extracted row set).
# Certificates land in output/class2-lane-cost78c-certificates/bitN.cert
set -e
CHILD=00000000000000403800000008000008
BIT="$1"
OUT=output/class2-lane-cost78c-certificates/bit${BIT}.cert
ROOT=$(python3 -c "print('%032x' % (int('$CHILD',16) | (1 << $BIT)))")
python3 scripts/legal_candidates.py "$ROOT" \
  | node --experimental-strip-types scripts/cert_driver78c.ts "$CHILD" "$BIT" "$OUT"
