#!/bin/sh
# Batch driver for the cost78c fresh v17 depth-10 sweep (head-1473 census v11
# rank-1 row 00000000000000403800000008000008; same batch plan shape as the
# cost74i/75f runs: 66 open bits as 7x9 + 1x3 + 1 confirmation batch of 12
# bits, engine cap 1e9 per bit, andclose 1, pilot_d6 control per batch).
# NOTE: this file is a post-sandbox-reset reconstruction of the original
# driver (the reset destroyed the local workspace after batch 6); the batch
# plan is the one actually executed across the two sandbox lifetimes and is
# fully recoverable from the published raw batch JSONLs and the sweep audit.
# Usage: ev78c_batches_20261117.sh <n>            # batch 1..9 (9 = confirmation)
set -e
CHILD=00000000000000403800000008000008
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
B1=1,2,4,9,10,16,17,18,19
B2=21,23,24,25,29,30,31,32,33
B3=35,38,41,42,43,44,45,49,52
B4=53,54,66,68,69,74,75,76,78
B5=79,82,83,85,86,87,88,89,90
B6=91,92,95,96,98,99,100,101,102
B7=105,106,107,109,111,112,113,114,116
B8=117,119,120
B9=5,13,14,20,34,46,97,103,108,110,115,118
case "$1" in
  1) run17 class2-lane-cost78c-raw-batch1-20261117.jsonl "$B1";;
  2) run17 class2-lane-cost78c-raw-batch2-20261117.jsonl "$B2";;
  3) run17 class2-lane-cost78c-raw-batch3-20261117.jsonl "$B3";;
  4) run17 class2-lane-cost78c-raw-batch4-20261117.jsonl "$B4";;
  5) run17 class2-lane-cost78c-raw-batch5-20261117.jsonl "$B5";;
  6) run17 class2-lane-cost78c-raw-batch6-20261117.jsonl "$B6";;
  7) run17 class2-lane-cost78c-raw-batch7-20261117.jsonl "$B7";;
  8) run17 class2-lane-cost78c-raw-batch8-20261117.jsonl "$B8";;
  9) run17 class2-lane-cost78c-raw-batch9-confirmation-20261117.jsonl "$B9";;
  det1) run17 class2-lane-cost78c-det-batch1-20261117.jsonl "$B1";;
  det8) run17 class2-lane-cost78c-det-batch8-20261117.jsonl "$B8";;
  v15a) run15 class2-lane-cost78c-v15-crosscheck-a-20261117.jsonl "$B9";;
  v15b) run15 class2-lane-cost78c-v15-crosscheck-b-20261117.jsonl "34,116,41,25,99";;
  *) echo "unknown batch $1"; exit 1;;
esac
echo "done $1"
