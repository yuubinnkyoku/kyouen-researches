#!/bin/sh
# Batch driver for the cost73k fresh v17 depth-10 sweep (regeneration after a
# sandbox reset; same batch plan as the original run: 66 open bits as
# 7x9 + 1x3 + 1 confirmation batch of 7 bits, engine cap 1e9 per bit,
# andclose 1, pilot_d6 control per batch).
# Usage: ev73k_batches_20261117.sh <n>            # batch 1..9 (9 = confirmation)
#        ev73k_batches_20261117.sh det1|det7     # determinism reruns
#        ev73k_batches_20261117.sh v15a..v15d     # v15 cross-engine chunks
set -e
CHILD=00000000000000801206000000000400
V17=scripts/class4_child1_runner_v17.ts
V15=scripts/class4_child1_runner.ts
OUT=output
CAP=1000000000
run17() { # $1=outfile $2=bits
  rm -f "$OUT/$1"
  node --experimental-strip-types "$V17" --bits "$2" --depth 10 --cap $CAP --andclose 1 --child $CHILD --out "$OUT/$1" >/dev/null
}
run15() { # $1=outfile $2=bits
  rm -f "$OUT/$1"
  node --experimental-strip-types "$V15" --bits "$2" --depth 10 --cap $CAP --child $CHILD --out "$OUT/$1" >/dev/null
}
B1=0,3,4,6,7,8,11,13,15
B2=18,19,21,22,24,25,28,29,31
B3=32,33,35,39,41,42,43,44,52
B4=54,56,58,59,62,65,66,67,73
B5=75,76,78,79,85,86,87,88,89
B6=91,92,94,95,96,97,98,99,101
B7=102,103,105,106,111,112,113,114,116
B8=117,118,119
B9=14,23,26,34,53,55,107
V15A=0,7,11,15,35,39,41,44
V15B=58,62,73,76,87,89,94
V15C=95,97,98,103,105,112,117
V15D=14,26,55
case "$1" in
  1) run17 class2-lane-cost73k-raw-batch1-20261117.jsonl "$B1";;
  2) run17 class2-lane-cost73k-raw-batch2-20261117.jsonl "$B2";;
  3) run17 class2-lane-cost73k-raw-batch3-20261117.jsonl "$B3";;
  4) run17 class2-lane-cost73k-raw-batch4-20261117.jsonl "$B4";;
  5) run17 class2-lane-cost73k-raw-batch5-20261117.jsonl "$B5";;
  6) run17 class2-lane-cost73k-raw-batch6-20261117.jsonl "$B6";;
  7) run17 class2-lane-cost73k-raw-batch7-20261117.jsonl "$B7";;
  8) run17 class2-lane-cost73k-raw-batch8-20261117.jsonl "$B8";;
  9) run17 class2-lane-cost73k-raw-batch9-confirmation-20261117.jsonl "$B9";;
  det1) run17 class2-lane-cost73k-det-batch1-20261117.jsonl "$B1";;
  det7) run17 class2-lane-cost73k-det-batch7-20261117.jsonl "$B7";;
  v15a) run15 class2-lane-cost73k-v15-crosscheck-a-20261117.jsonl "$V15A";;
  v15b) run15 class2-lane-cost73k-v15-crosscheck-b-20261117.jsonl "$V15B";;
  v15c) run15 class2-lane-cost73k-v15-crosscheck-c-20261117.jsonl "$V15C";;
  v15d) run15 class2-lane-cost73k-v15-crosscheck-d-20261117.jsonl "$V15D";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
