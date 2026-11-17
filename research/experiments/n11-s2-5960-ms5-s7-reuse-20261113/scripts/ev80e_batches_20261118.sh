#!/bin/sh
# Batch driver for the cost80e fresh v17 depth-10 sweep (census v15 rank-1 row
# 00000000020000003800000180000000; same batch plan shape as the cost79d/79e
# runs: 68 open bits as 7x9 + 1x5 + 1 confirmation batch of 12 bits, engine
# cap 1e9 per bit, andclose 1, pilot_d6 control per batch).
# Usage: ev80e_batches_20261118.sh <n>            # batch 1..9 (9 = confirmation)
set -e
CHILD=00000000020000003800000180000000
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
B1=0,2,3,4,6,7,8,10,11
B2=12,14,15,16,17,18,19,21,25
B3=26,28,29,33,34,36,37,38,42
B4=43,44,48,49,50,51,53,54,66
B5=67,69,70,71,75,76,77,78,80
B6=81,82,83,84,86,87,88,92,94
B7=99,101,103,104,105,106,110,112,113
B8=114,116,117,118,120
B9=5,27,30,35,41,46,74,79,85,90,93,115
case "$1" in
  1) run17 class2-lane-cost80e-raw-batch1-20261118.jsonl "$B1";;
  2) run17 class2-lane-cost80e-raw-batch2-20261118.jsonl "$B2";;
  3) run17 class2-lane-cost80e-raw-batch3-20261118.jsonl "$B3";;
  4) run17 class2-lane-cost80e-raw-batch4-20261118.jsonl "$B4";;
  5) run17 class2-lane-cost80e-raw-batch5-20261118.jsonl "$B5";;
  6) run17 class2-lane-cost80e-raw-batch6-20261118.jsonl "$B6";;
  7) run17 class2-lane-cost80e-raw-batch7-20261118.jsonl "$B7";;
  8) run17 class2-lane-cost80e-raw-batch8-20261118.jsonl "$B8";;
  9) run17 class2-lane-cost80e-raw-batch9-confirmation-20261118.jsonl "$B9";;
  det1) run17 class2-lane-cost80e-det-batch1-20261118.jsonl "$B1";;
  det8) run17 class2-lane-cost80e-det-batch8-20261118.jsonl "$B8";;
  v15a) run15 class2-lane-cost80e-v15-crosscheck-a-20261118.jsonl "$B9";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
