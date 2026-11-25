#!/bin/sh
# Batch driver for the cost81 fresh v17 depth-10 sweep (census v17 rank-1 row
# 00000000020000003800000080008000; batch plan: 66 open bits as 7x9 + 1x3 plus
# 1 confirmation batch of 15 bits, engine cap 1e9 per bit, andclose 1,
# pilot_d6 control per batch; same shape as the cost80f run).
# Usage: ev81_batches_20261118.sh <n>        # batch 1..9 (9 = confirmation)
set -e
CHILD=00000000020000003800000080008000
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
B2=12,14,19,21,26,28,33,34,36
B3=37,38,39,40,42,43,44,48,49
B4=50,54,66,67,69,70,71,72,76
B5=77,78,80,81,82,83,84,86,87
B6=91,92,94,95,99,101,102,103,104
B7=105,106,108,109,110,112,113,114,116
B8=117,118,120
B9=27,30,32,35,41,45,46,74,75,79,85,88,90,93,115
case "$1" in
  1) run17 class2-lane-cost81-raw-batch1-20261118.jsonl "$B1";;
  2) run17 class2-lane-cost81-raw-batch2-20261118.jsonl "$B2";;
  3) run17 class2-lane-cost81-raw-batch3-20261118.jsonl "$B3";;
  4) run17 class2-lane-cost81-raw-batch4-20261118.jsonl "$B4";;
  5) run17 class2-lane-cost81-raw-batch5-20261118.jsonl "$B5";;
  6) run17 class2-lane-cost81-raw-batch6-20261118.jsonl "$B6";;
  7) run17 class2-lane-cost81-raw-batch7-20261118.jsonl "$B7";;
  8) run17 class2-lane-cost81-raw-batch8-20261118.jsonl "$B8";;
  9) run17 class2-lane-cost81-raw-batch9-confirmation-20261118.jsonl "$B9";;
  det1) run17 class2-lane-cost81-det-batch1-20261118.jsonl "$B1";;
  det8) run17 class2-lane-cost81-det-batch8-20261118.jsonl "$B8";;
  v15a) run15 class2-lane-cost81-v15-crosscheck-a-20261118.jsonl "$B9";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
