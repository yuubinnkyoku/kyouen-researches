#!/bin/bash
cd /home/user/kr27/w5x27
KISSAT=/home/user/kr26/kissat-4.0.4-linux-amd64
CAP=$1; MAXEL=$2; shift 2
START=$(date +%s)
for n in "$@"; do
  if [ -f "output/r5x27q7_$n.txt" ] && ! grep -q '^s ' "output/r5x27q7_$n.txt" 2>/dev/null; then rm -rf "output/claim_$n"; fi
done
worker(){
  while :; do
    NOW=$(date +%s); [ $((NOW-START)) -gt $MAXEL ] && return
    n=""
    for c in "$@"; do
      [ -d "output/claim_$c" ] && continue
      [ -f "output/r5x27q7_$c.txt" ] && grep -q '^s ' "output/r5x27q7_$c.txt" 2>/dev/null && continue
      mkdir "output/claim_$c" 2>/dev/null && { n=$c; break; }
    done
    [ -z "$n" ] && return
    cnfstem=${n#c}
    timeout "$CAP" "$KISSAT" "output/c5x27q7_$cnfstem.cnf" > "output/r5x27q7_$n.txt" 2>&1
  done
}
worker "$@" & worker "$@" & wait
echo "verdicts: $(grep -l '^s ' output/r5x27q7_*.txt 2>/dev/null | wc -l)"
