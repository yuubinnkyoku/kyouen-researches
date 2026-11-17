#!/bin/sh
# Batch driver for the cost75f fresh v17 depth-10 sweep (head-1473 census v10
# rank-1 row 00000000020000003800020080000000; same batch plan shape as the
# cost74i run: 71 open bits as 7x9 + 1x8 + 1 confirmation batch of 4 bits,
# engine cap 1e9 per bit, andclose 1, pilot_d6 control per batch).
# Usage: ev75f_batches_20261117.sh <n>            # batch 1..9 (9 = confirmation)
set -e
CHILD=00000000020000003800020080000000
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
B1=0,2,3,4,7,8,10,11,12
B2=14,15,16,17,18,26,28,29,32
B3=33,37,38,39,40,42,43,44,45
B4=46,48,49,50,53,54,66,67,69
B5=70,72,74,75,76,77,78,79,80
B6=82,83,84,85,86,87,88,92,94
B7=95,99,102,103,104,105,106,108,109
B8=110,112,113,114,116,117,118,120
B9=27,90,93,115
case "$1" in
  1) run17 class2-lane-cost75f-raw-batch1-20261117.jsonl "$B1";;
  2) run17 class2-lane-cost75f-raw-batch2-20261117.jsonl "$B2";;
  3) run17 class2-lane-cost75f-raw-batch3-20261117.jsonl "$B3";;
  4) run17 class2-lane-cost75f-raw-batch4-20261117.jsonl "$B4";;
  5) run17 class2-lane-cost75f-raw-batch5-20261117.jsonl "$B5";;
  6) run17 class2-lane-cost75f-raw-batch6-20261117.jsonl "$B6";;
  7) run17 class2-lane-cost75f-raw-batch7-20261117.jsonl "$B7";;
  8) run17 class2-lane-cost75f-raw-batch8-20261117.jsonl "$B8";;
  9) run17 class2-lane-cost75f-raw-batch9-confirmation-20261117.jsonl "$B9";;
  det1) run17 class2-lane-cost75f-det-batch1-20261117.jsonl "$B1";;
  det8) run17 class2-lane-cost75f-det-batch8-20261117.jsonl "$B8";;
  v15a) run15 class2-lane-cost75f-v15-crosscheck-a-20261117.jsonl "27,90,93,115";;
  v15b) run15 class2-lane-cost75f-v15-crosscheck-b-20261117.jsonl "7,15,66,86,105";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
