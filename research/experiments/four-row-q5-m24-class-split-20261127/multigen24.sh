#!/bin/bash
# (4,24,5) multi-class krow-pinned decomposition driver (m21-rule for INDET multis).
# Direct multi pieces c01/c02/c03/c12 were INDET at CAP=220s (honest negatives).
# Decomposition per multi class D={a,b} (a<b, both deficient rows):
#   - exact stone-count pieces (k0,k1) in {0..3}^2 on rows a,b: 16 pieces,
#     disjoint and exhaustive (each deficient row has a unique count 0..3).
#   - a k0>=1 piece that resists CAP is decided by the sound H-split minpos
#     sub-pieces p=0..11 (sat3.js --minpos pins the leftmost stone of row a;
#     sound: min(x1, 23-x_k0) <= 11, same split as the single-class buckets).
#   - k0=0 pieces (row a empty): direct only; minpos is not applicable.
# Records schema identical to runner24.sh (append-only, resumable; INDET rows
# are skipped on re-run unless their sub-pieces are incomplete).
# Usage: bash multigen24.sh [classes]   e.g. \"01\" or \"01 02 03 12\" (default all 4)
set -u
KIT=\"$(cd \"$(dirname \"$0\")\" && pwd)\"
OUT=\"$KIT/output\"
KS=/tmp/kissat_run/kissat
mkdir -p \"$OUT\" /tmp/kissat_run
[ -x \"$KS\" ] || { cp \"$KIT/kissat-4.0.4-linux-amd64\" \"$KS\" && chmod +x \"$KS\"; }
CAP=${CAP:-220}
BUDGET=${BUDGET:-55}
T0=$(date +%s)
SATFOUND=0
recfile=\"$OUT/records24.jsonl\"
anyrow() { grep -s \"\\\"key\\\":\\\"$1\\\",\\\"w\\\":4,\\\"m\\\":24\" \"$recfile\"; }
has_unsat() { anyrow \"$1\" | grep -s -q '"result":"UNSAT"'; }
has_sat()   { anyrow \"$1\" | grep -s -q '"result":"SAT"'; }
timelp() { [ $(( $(date +%s) - T0 )) -ge \"$BUDGET\" ]; }
# run <key> <classspec> <extra args...>; returns 0 decided, 9 budget, 1 genfail
run() {
  local key=$1 cls=$2; shift 2
  local extra=\"$*\"
  timelp && return 9
  local cnf=\"$OUT/${key}.cnf\" log=\"$OUT/${key}.txt\"
  local meta
  meta=$(node \"$KIT/scripts/sat3.js\" 4 24 5 --class=\"$cls\" $extra \"$cnf\") || {
    echo \"{\\\"key\\\":\\\"$key\\\",\\\"genfail\\\":true,\\\"date\\\":\\\"$(date -u +%FT%TZ)\\\"}\" >> \"$recfile\"; return 1; }
  local md5=$(md5sum \"$cnf\" | awk '{print $1}')
  local t0=$(date +%s.%N)
  timeout \"$CAP\" \"$KS\" \"$cnf\" > \"$log\" 2>&1
  local rc=$?
  local t1=$(date +%s.%N)
  local sec=$(echo \"$t1 $t0\" | awk '{printf \"%.1f\", $1-$2}')
  local conf=$(grep -a -E \"^c conflicts\" \"$log\" | tail -1 | awk '{print $3}')
  local res=INDET; [ \"$rc\" = \"10\" ] && res=SAT; [ \"$rc\" = \"20\" ] && res=UNSAT
  echo \"{\\\"key\\\":\\\"$key\\\",\\\"w\\\":4,\\\"m\\\":24,\\\"q\\\":5,\\\"class\\\":\\\"$cls\\\",\\\"extra\\\":\\\"$extra\\\",\\\"cnf_md5\\\":\\\"$md5\\\",\\\"cap\\\":$CAP,\\\"kissat\\\":{\\\"result\\\":\\\"$res\\\",\\\"rc\\\":$rc,\\\"conflicts\\\":${conf:-null},\\\"sec\\\":$sec},\\\"date\\\":\\\"$(date -u +%FT%TZ)\\\"}\" >> \"$recfile\"
  if [ \"$res\" = \"SAT\" ]; then
    SATFOUND=1
    grep \"^v \" \"$log\" > \"$OUT/${key}.model.txt\"
    node \"$KIT/scripts/sat3.js\" decode 4 24 5 \"$OUT/${key}.model.txt\" --json=\"$OUT/${key}.witness.json\" > \"$OUT/${key}.decode.txt\" 2>&1
    jq -c '.stones' \"$OUT/${key}.witness.json\" | python3 \"$KIT/scripts/verify_witness.py\" 4 24 5 > \"$OUT/${key}.pyverify.json\" 2>&1 || true
    echo \"SAT_FOUND $key $(date -u +%FT%TZ)\"
  fi
  rm -f \"$cnf\"
  return 0
}
piece() { # <D> <k0> <k1>  ; D like 01 -> rows a=0 b=1
  local D=$1 k0=$2 k1=$3
  local a=${D:0:1} b=${D:1:1}
  local cls=\"$a,$b\"
  local key=\"c${D}r${k0}s${k1}\"
  has_sat \"$key\" && { SATFOUND=1; return 0; }
  if has_unsat \"$key\"; then return 0; fi
  if [ \"$(anyrow \"$key\" | wc -l)\" -gt 0 ]; then
    # direct already attempted (INDET); go to sub-split when applicable
    if [ \"$k0\" -ge 1 ]; then
      local P
      for P in $(seq 0 11); do
        run \"c${D}r${k0}s${k1}p${P}\" \"$cls\" \"--krow=$a:$k0 --krow=$b:$k1 --minpos=$P\" || { [ $? = 9 ] && return 9; }
        has_sat \"c${D}r${k0}s${k1}p${P}\" && { SATFOUND=1; return 0; }
      done
    fi
    return 0
  fi
  run \"$key\" \"$cls\" \"--krow=$a:$k0 --krow=$b:$k1\" || { [ $? = 9 ] && return 9; }
  return 0
}
for D in ${1:-01 02 03 12}; do
  for k0 in 0 1 2 3; do
    for k1 in 0 1 2 3; do
      [ \"$SATFOUND\" = \"1\" ] && break 3
      piece \"$D\" \"$k0\" \"$k1\" || { [ $? = 9 ] && break 3; }
    done
  done
done
echo \"MULTIGEN24_CHUNK_DONE satfound=$SATFOUND rows=$(wc -l < \"$recfile\") $(date -u +%FT%TZ)\"
