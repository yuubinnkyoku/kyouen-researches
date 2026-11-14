#!/bin/bash
# $1..: cases as w,m,q,budget,seeds
OUT=/home/user/sa/results.jsonl
while IFS=, read -r w m q budget seeds; do
  [ -z "$w" ] && continue
  IFS=' ' read -ra SS <<< "$seeds"
  for s in "${SS[@]}"; do
    RES=$(node /home/user/sa/sa_machine.js "$w" "$m" "$q" "$budget" "$s")
    echo "{\"ts\":\"$(date -u +%FT%TZ)\",\"case\":\"${w}x${m}q${q}\",$RES}" >> "$OUT"
    MIN=$(echo "$RES" | sed 's/.*"min":\([0-9]*\).*/\1/')
    echo "case ${w}x${m}q${q} seed $s -> min=$MIN" >> /home/user/sa/progress.txt
  done
done < "$1"
echo DONE >> /home/user/sa/progress.txt
