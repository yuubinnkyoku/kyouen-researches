#!/bin/bash
# Auto band extension for (5,5): m=26,27,... class {0} hunt with k x minpos escalation.
# Stops at first m where all sub-instances are INDET (honest negative) or at MAXM.
cd /home/user/kr/work/scripts
KISSAT=/home/user/kr/bin/kissat
OUT=/home/user/kr/work/output
T=${T:-250}
MAXM=${MAXM:-40}
S="$OUT/extend55_status.txt"; touch "$S"
for ((m=26; m<=MAXM; m++)); do
  PMAX=$(( (m-1)/2 ))
  found=0
  run(){ local name=$1; shift
    local C="$OUT/$name.cnf"; local L="$OUT/r$name.txt"
    [ -f "$L" ] && return 2
    node /home/user/kr/work/scripts/sat3.js "$@" "$C" > "$C.meta" 2>&1
    timeout "$T" "$KISSAT" "$C" > "$L" 2>&1
    local R=$(grep -m1 "^s " "$L" || echo "INDET")
    local C2=$(grep -m1 -oP "conflicts:\s+\K[0-9]+" "$L" || echo 0)
    echo "m=$m $name $R conflicts=$C2" >> "$S"
    [[ "$R" == *"SATISFIABLE"* ]] && return 0
    return 1
  }
  if run c5x${m}q5_c0 5 $m 5 --class=0; then found=1; fi
  if [ $found -eq 0 ]; then
    for k in 0 1 2; do if run c5x${m}q5_c0k$k 5 $m 5 --class=0 --krow=0:$k; then found=1; break; fi; done
  fi
  if [ $found -eq 0 ]; then
    for ((p=0; p<=PMAX; p++)); do if run c5x${m}q5_c0k3p$p 5 $m 5 --class=0 --krow=0:3 --minpos=$p; then found=1; break; fi; done
  fi
  if [ $found -eq 1 ]; then
    echo "m=$m WITNESS-FOUND (class 0 family)" >> "$S"
    node /home/user/kr/work/scripts/sat3.js decode 5 $m 5 "$OUT/rc5x${m}q5_c0.txt" --json="$OUT/witness_5x${m}_c0.json" > "$OUT/witness_5x${m}_c0.decode.txt" 2>&1 || true
  else
    echo "m=$m STOP-ALL-INDET (honest negative, not absence)" >> "$S"
    exit 0
  fi
done
echo "REACHED-MAXM $MAXM" >> "$S"
