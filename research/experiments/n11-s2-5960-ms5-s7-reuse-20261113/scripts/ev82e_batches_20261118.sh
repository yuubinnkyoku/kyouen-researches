#!/bin/sh
# Batch driver for the cost82e fresh v17 depth-10 sweep (census v19 rank-1 row
# 00000000020000003800000090000000; batch plan: 63 open bits as 7x9 plus
# 1 confirmation batch of 19 bits, engine cap 1e9 per bit, andclose 1,
# pilot_d6 control per batch; same shape as the cost-82d run).
# Usage: ev82e_batches_20261118.sh <n>        # batch 1..8 (8 = confirmation)
set -e
CHILD=00000000020000003800000090000000
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
B1=0,2,3,4,6,7,8,10,12
B2=14,16,17,18,19,21,29,33,34
B3=36,38,39,42,43,44,49,50,53
B4=54,66,67,69,70,71,72,76,77
B5=78,80,81,82,83,84,86,87,91
B6=92,94,95,99,101,102,103,104,106
B7=108,110,112,113,114,116,117,118,120
B8=5,11,15,30,32,35,41,45,46,74,75,79,85,88,90,93,105,109,115
case "$1" in
  1) run17 class2-lane-cost82e-raw-batch1-20261118.jsonl "$B1";;
  2) run17 class2-lane-cost82e-raw-batch2-20261118.jsonl "$B2";;
  3) run17 class2-lane-cost82e-raw-batch3-20261118.jsonl "$B3";;
  4) run17 class2-lane-cost82e-raw-batch4-20261118.jsonl "$B4";;
  5) run17 class2-lane-cost82e-raw-batch5-20261118.jsonl "$B5";;
  6) run17 class2-lane-cost82e-raw-batch6-20261118.jsonl "$B6";;
  7) run17 class2-lane-cost82e-raw-batch7-20261118.jsonl "$B7";;
  8) run17 class2-lane-cost82e-raw-batch8-confirmation-20261118.jsonl "$B8";;
  det1) run17 class2-lane-cost82e-det-batch1-20261118.jsonl "$B1";;
  det7) run17 class2-lane-cost82e-det-batch7-20261118.jsonl "$B7";;
  v15a) run15 class2-lane-cost82e-v15-crosscheck-a-20261118.jsonl "$B8";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
