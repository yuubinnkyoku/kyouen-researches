#!/bin/sh
# Batch driver for the cost73l fresh v17 depth-10 sweep (head-1473 census v8
# rank-1 row 00000000000000c09002000000400000; same batch plan shape as the
# cost73k run: 66 open bits as 7x9 + 1x3 + 1 confirmation batch of 7 bits,
# engine cap 1e9 per bit, andclose 1, pilot_d6 control per batch).
# Usage: ev73l_batches_20261117.sh <n>            # batch 1..9 (9 = confirmation)
#        ev73l_batches_20261117.sh det1|det4      # determinism reruns (batch 1 + heaviest batch 4, bit 47)
#        ev73l_batches_20261117.sh v15a..v15d     # v15 cross-engine chunks (WIN bits)
set -e
CHILD=00000000000000c09002000000400000
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
B1=0,1,2,3,4,6,7,8,9
B2=10,14,17,18,19,21,23,24,25
B3=26,28,29,30,32,33,34,35,41
B4=42,44,45,47,53,54,58,61,62
B5=64,66,68,76,78,79,80,81,85
B6=87,89,91,92,95,96,98,100,101
B7=102,105,107,109,111,112,113,114,116
B8=117,119,120
B9=65,86,90,94,97,106,110
V15A=1,2,3,4,6,8,9,18,21
V15B=23,25,28,29,32,34,41,42,44
V15C=47,53,54,61,62,64,66,80
V15D=95,105,106,110,112,113,116,119
case "$1" in
  1) run17 class2-lane-cost73l-raw-batch1-20261117.jsonl "$B1";;
  2) run17 class2-lane-cost73l-raw-batch2-20261117.jsonl "$B2";;
  3) run17 class2-lane-cost73l-raw-batch3-20261117.jsonl "$B3";;
  4) run17 class2-lane-cost73l-raw-batch4-20261117.jsonl "$B4";;
  5) run17 class2-lane-cost73l-raw-batch5-20261117.jsonl "$B5";;
  6) run17 class2-lane-cost73l-raw-batch6-20261117.jsonl "$B6";;
  7) run17 class2-lane-cost73l-raw-batch7-20261117.jsonl "$B7";;
  8) run17 class2-lane-cost73l-raw-batch8-20261117.jsonl "$B8";;
  9) run17 class2-lane-cost73l-raw-batch9-confirmation-20261117.jsonl "$B9";;
  det1) run17 class2-lane-cost73l-det-batch1-20261117.jsonl "$B1";;
  det4) run17 class2-lane-cost73l-det-batch4-20261117.jsonl "$B4";;
  v15a) run15 class2-lane-cost73l-v15-crosscheck-a-20261117.jsonl "$V15A";;
  v15b) run15 class2-lane-cost73l-v15-crosscheck-b-20261117.jsonl "$V15B";;
  v15c) run15 class2-lane-cost73l-v15-crosscheck-c-20261117.jsonl "$V15C";;
  v15d) run15 class2-lane-cost73l-v15-crosscheck-d-20261117.jsonl "$V15D";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
