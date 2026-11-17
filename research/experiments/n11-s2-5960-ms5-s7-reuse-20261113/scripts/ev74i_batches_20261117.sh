#!/bin/sh
# Batch driver for the cost74i fresh v17 depth-10 sweep (head-1473 census v9
# rank-1 row 00000000020000003800000088000000; same batch plan shape as the
# cost73l run: 69 open bits as 7x9 + 1x6 + 1 confirmation batch of 5 bits,
# engine cap 1e9 per bit, andclose 1, pilot_d6 control per batch).
# Usage: ev74i_batches_20261117.sh <n>            # batch 1..9 (9 = confirmation)
set -e
CHILD=00000000020000003800000088000000
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
B2=12,14,15,16,21,25,29,32,33
B3=34,35,38,41,42,43,44,45,46
B4=54,66,67,69,70,74,75,76,77
B5=78,79,80,81,82,83,84,85,86
B6=87,88,91,92,93,94,95,99,101
B7=102,103,104,105,106,108,109,110,112
B8=113,114,116,117,118,120
B9=30,71,72,90,115
case "$1" in
  1) run17 class2-lane-cost74i-raw-batch1-20261117.jsonl "$B1";;
  2) run17 class2-lane-cost74i-raw-batch2-20261117.jsonl "$B2";;
  3) run17 class2-lane-cost74i-raw-batch3-20261117.jsonl "$B3";;
  4) run17 class2-lane-cost74i-raw-batch4-20261117.jsonl "$B4";;
  5) run17 class2-lane-cost74i-raw-batch5-20261117.jsonl "$B5";;
  6) run17 class2-lane-cost74i-raw-batch6-20261117.jsonl "$B6";;
  7) run17 class2-lane-cost74i-raw-batch7-20261117.jsonl "$B7";;
  8) run17 class2-lane-cost74i-raw-batch8-20261117.jsonl "$B8";;
  9) run17 class2-lane-cost74i-raw-batch9-confirmation-20261117.jsonl "$B9";;
  det1) run17 class2-lane-cost74i-det-batch1-20261117.jsonl "$B1";;
  det8) run17 class2-lane-cost74i-det-batch8-20261117.jsonl "$B8";;
  v15a) run15 class2-lane-cost74i-v15-crosscheck-a-20261117.jsonl "30,71,72,90,115";;
  v15b) run15 class2-lane-cost74i-v15-crosscheck-b-20261117.jsonl "4,35,88,116,120";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
