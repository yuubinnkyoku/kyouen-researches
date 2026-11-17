#!/bin/sh
# Batch driver for the cost79d fresh v17 depth-10 sweep (census v13 rank-1 row
# 00000000020000003800400080000000; same batch plan shape as the cost79c run:
# 72 open bits as 8x9 + 1 confirmation batch of 7 bits, engine cap 1e9
# per bit, andclose 1, pilot_d6 control per batch).
# Usage: ev79d_batches_20261118.sh <n>            # batch 1..9 (9 = confirmation)
set -e
CHILD=00000000020000003800400080000000
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
B2=14,15,16,17,18,21,25,26,28
B3=29,32,33,34,35,36,37,38,39
B4=40,42,43,44,45,48,50,54,67
B5=69,70,71,72,74,75,76,77,78
B6=80,81,82,83,84,85,86,87,88
B7=91,92,95,99,102,103,105,106,108
B8=109,110,112,113,114,116,117,118,120
B9=5,27,41,79,90,93,115
case "$1" in
  1) run17 class2-lane-cost79d-raw-batch1-20261118.jsonl "$B1";;
  2) run17 class2-lane-cost79d-raw-batch2-20261118.jsonl "$B2";;
  3) run17 class2-lane-cost79d-raw-batch3-20261118.jsonl "$B3";;
  4) run17 class2-lane-cost79d-raw-batch4-20261118.jsonl "$B4";;
  5) run17 class2-lane-cost79d-raw-batch5-20261118.jsonl "$B5";;
  6) run17 class2-lane-cost79d-raw-batch6-20261118.jsonl "$B6";;
  7) run17 class2-lane-cost79d-raw-batch7-20261118.jsonl "$B7";;
  8) run17 class2-lane-cost79d-raw-batch8-20261118.jsonl "$B8";;
  9) run17 class2-lane-cost79d-raw-batch9-confirmation-20261118.jsonl "$B9";;
  det1) run17 class2-lane-cost79d-det-batch1-20261118.jsonl "$B1";;
  det8) run17 class2-lane-cost79d-det-batch8-20261118.jsonl "$B8";;
  v15a) run15 class2-lane-cost79d-v15-crosscheck-a-20261118.jsonl "$B9";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
