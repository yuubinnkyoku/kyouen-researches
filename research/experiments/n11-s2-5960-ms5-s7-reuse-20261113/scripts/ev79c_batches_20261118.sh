#!/bin/sh
# Batch driver for the cost79c fresh v17 depth-10 sweep (census v12 rank-1 row
# 00000000000000c09002000200000000; same batch plan shape as the cost78c run:
# 68 open bits as 7x9 + 1x5 + 1 confirmation batch of 11 bits, engine cap 1e9
# per bit, andclose 1, pilot_d6 control per batch).
# Usage: ev79c_batches_20261118.sh <n>            # batch 1..9 (9 = confirmation)
set -e
CHILD=00000000000000c09002000200000000
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
B2=10,11,14,15,17,18,19,21,23
B3=24,25,26,28,29,30,31,32,34
B4=35,41,44,45,47,53,54,55,58
B5=61,62,64,68,76,78,79,80,81
B6=85,89,90,91,92,95,96,98,99
B7=100,101,102,105,107,109,111,112,113
B8=114,116,117,119,120
B9=12,20,22,65,67,86,87,94,97,106,110
case "$1" in
  1) run17 class2-lane-cost79c-raw-batch1-20261118.jsonl "$B1";;
  2) run17 class2-lane-cost79c-raw-batch2-20261118.jsonl "$B2";;
  3) run17 class2-lane-cost79c-raw-batch3-20261118.jsonl "$B3";;
  4) run17 class2-lane-cost79c-raw-batch4-20261118.jsonl "$B4";;
  5) run17 class2-lane-cost79c-raw-batch5-20261118.jsonl "$B5";;
  6) run17 class2-lane-cost79c-raw-batch6-20261118.jsonl "$B6";;
  7) run17 class2-lane-cost79c-raw-batch7-20261118.jsonl "$B7";;
  8) run17 class2-lane-cost79c-raw-batch8-20261118.jsonl "$B8";;
  9) run17 class2-lane-cost79c-raw-batch9-confirmation-20261118.jsonl "$B9";;
  det1) run17 class2-lane-cost79c-det-batch1-20261118.jsonl "$B1";;
  det8) run17 class2-lane-cost79c-det-batch8-20261118.jsonl "$B8";;
  v15a) run15 class2-lane-cost79c-v15-crosscheck-a-20261118.jsonl "$B9";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
