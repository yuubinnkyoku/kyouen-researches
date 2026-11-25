#!/bin/sh
# Blind certificate extraction for the 12 sweep WIN7-D10 roots of cost73i
# (bits 1, 9, 11, 18, 29, 38, 54, 82, 97, 100, 110, 111). One argument: the bit.
# Per-bit fresh process, MS=1<<23 (single-line substitution on the
# repo-verbatim extractor_exact; published prescription). Same pipeline as
# the 69j/66j/71e/72d/73j/73k/73l/78c certificate lanes.
# Certificates land in output/class2-lane-cost73i-certificates/bitN.cert
set -e
CHILD=00000000000000403800400008000000
BIT="$1"
OUT=output/class2-lane-cost73i-certificates/bit${BIT}.cert
ROOT=$(python3 -c "print('%032x' % (int('$CHILD',16) | (1 << $BIT)))")
python3 scripts/legal_candidates.py "$ROOT" \
  | node --experimental-strip-types scripts/cert_driver73i.ts "$CHILD" "$BIT" "$OUT"
