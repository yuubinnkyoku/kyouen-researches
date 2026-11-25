#!/bin/sh
# Blind certificate extraction for the 32 sweep WIN7-D10 roots of cost73l
# (bits 106/110 excluded: covered by the published cost73j bit 118 and
# cost73k bit 98 certificates). One argument: the bit to extract.
# Per-bit fresh process, MS=1<<23 (single-line substitution on the
# repo-verbatim extractor_exact; published prescription, ~-30% extraction
# nodes vs MS=1<<18, same extracted row set).
# Certificates land in output/class2-lane-cost73l-certificates/bitN.cert
set -e
CHILD=00000000000000c09002000000400000
BIT="$1"
OUT=output/class2-lane-cost73l-certificates/bit${BIT}.cert
ROOT=$(python3 -c "print('%032x' % (int('$CHILD',16) | (1 << $BIT)))")
python3 scripts/legal_candidates.py "$ROOT" \
  | node --experimental-strip-types scripts/cert_driver73l.ts "$CHILD" "$BIT" "$OUT"
