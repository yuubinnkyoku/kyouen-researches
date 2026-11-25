#!/bin/sh
# Batch driver for the cost82d fresh v17 depth-10 sweep (census v18 rank-1 row
# 00000000020000003800000080000800; batch plan: 65 open bits as 7x9 + 1x2 plus
# 1 confirmation batch of 17 bits, engine cap 1e9 per bit, andclose 1,
# pilot_d6 control per batch; same shape as the cost81 run).
# Usage: ev82d_batches_20261118.sh <n>        # batch 1..9 (9 = confirmation)
set -e
CHILD=00000000020000003800000080000800
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
B1=2,3,4,6,7,8,10,14,16
B2=17,18,19,26,28,29,33,34,36
B3=37,38,39,40,42,43,44,49,50
B4=51,53,54,66,67,69,70,71,72
B5=76,77,78,81,82,83,84,86,87
B6=91,92,94,95,99,101,102,103,104
B7=106,108,109,110,112,113,114,116,117
B8=118,120
B9=5,15,27,30,32,35,41,45,46,74,75,79,85,90,93,105,115
case "$1" in
  1) run17 class2-lane-cost82d-raw-batch1-20261118.jsonl "$B1";;
  2) run17 class2-lane-cost82d-raw-batch2-20261118.jsonl "$B2";;
  3) run17 class2-lane-cost82d-raw-batch3-20261118.jsonl "$B3";;
  4) run17 class2-lane-cost82d-raw-batch4-20261118.jsonl "$B4";;
  5) run17 class2-lane-cost82d-raw-batch5-20261118.jsonl "$B5";;
  6) run17 class2-lane-cost82d-raw-batch6-20261118.jsonl "$B6";;
  7) run17 class2-lane-cost82d-raw-batch7-20261118.jsonl "$B7";;
  8) run17 class2-lane-cost82d-raw-batch8-20261118.jsonl "$B8";;
  9) run17 class2-lane-cost82d-raw-batch9-confirmation-20261118.jsonl "$B9";;
  det1) run17 class2-lane-cost82d-det-batch1-20261118.jsonl "$B1";;
  det8) run17 class2-lane-cost82d-det-batch8-20261118.jsonl "$B8";;
  v15a) run15 class2-lane-cost82d-v15-crosscheck-a-20261118.jsonl "$B9";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
