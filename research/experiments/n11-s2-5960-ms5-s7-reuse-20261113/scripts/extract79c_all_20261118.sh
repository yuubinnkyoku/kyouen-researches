#!/bin/sh
# Blind certificate extraction for the 19 new sweep WIN7-D10 roots of cost79c
# (bits 1,2,17,21,26,28,29,30,31,47,58,62,91,96,100,109,113,117,120;
#  confirmation bit 110 is canon-equal to cost73k bit 87 with a published certificate
#  and is not re-extracted here). One argument: the bit to extract.
# Per-bit fresh process, repo-verbatim extractor_exact_ms23 (MS=1<<23) via the
# argv-driven cert_driver78c.ts lineage (child/bit passed as argv).
set -e
CHILD=00000000000000c09002000200000000
BIT="$1"
OUT=output/class2-lane-cost79c-certificates/bit${BIT}.cert
ROOT=$(python3 -c "print('%032x' % (int('$CHILD',16) | (1 << $BIT)))")
python3 scripts/legal_candidates.py "$ROOT" \
  | node --experimental-strip-types scripts/cert_driver78c.ts "$CHILD" "$BIT" "$OUT"
