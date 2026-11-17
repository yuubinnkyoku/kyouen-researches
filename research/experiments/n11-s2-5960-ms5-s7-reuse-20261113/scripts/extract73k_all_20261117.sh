#!/bin/sh
# Blind certificate extraction for the 22 sweep WIN7-D10 roots of cost73k.
# One argument: the bit to extract. Certificates land in
# output/class2-lane-cost73k-certificates/bitN.cert
set -e
CHILD=00000000000000801206000000000400
BIT="$1"
OUT=output/class2-lane-cost73k-certificates/bit${BIT}.cert
ROOT=$(python3 -c "print('%032x' % (int('$CHILD',16) | (1 << $BIT)))")
python3 scripts/legal_candidates.py "$ROOT" \
  | node --experimental-strip-types scripts/cert_driver73k.ts "$CHILD" "$BIT" "$OUT"
