#!/bin/bash
set -eu
cd /home/user/kr28/w5x28
OUT=output
for D in 2 0,1 0,2 0,3 0,4 1,2 1,3 0,1,2 0,1,3 0,1,4 0,2,3 0,2,4 1,2,3 0,1,2,3 0,1,2,4 0,1,3,4 0,1,2,3,4; do
  N=$(echo "$D" | tr -d ',')
  node sat3.js 5 28 7 --class="$D" "$OUT/c5x28q7_$N.cnf" > /dev/null
done
for y in 0 1; do
  for k in 0 1 2 3 4; do
    node sat3.js 5 28 7 --class=$y --krow=$y:$k "$OUT/c5x28q7_${y}k${k}.cnf" > /dev/null
  done
  for p in 0 1 2 3 4 5 6 7 8 9 10 11 12 13; do
    node sat3.js 5 28 7 --class=$y --krow=$y:5 --minpos=$p "$OUT/c5x28q7_${y}k5p${p}.cnf" > /dev/null
  done
done
node sat3.js 5 28 7 --class=0,1 --lex=H "$OUT/c5x28q7_01_lexH.cnf" > /dev/null
node sat3.js 5 28 7 --class=2 --lex=H "$OUT/c5x28q7_2_lexH.cnf" > /dev/null
node sat3.js 5 18 7 --class=0 "$OUT/c5x18q7_0.cnf" > /dev/null
ls $OUT/*.cnf | wc -l
