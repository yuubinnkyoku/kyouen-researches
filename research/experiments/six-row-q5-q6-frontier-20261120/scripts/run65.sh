#!/bin/bash
set -u
W=$1; M=$2; Q=$3; OUT=$4; TAG=$5; CAP=$6; MODE=$7; ROWY=${8:-null}
EXTRA=${9:-}
KCFG=${10:-}
ROOT=/home/user/kr65
FW=$ROOT/work/frontier
SATJS=$ROOT/scripts/sat2.js
SAT3=$ROOT/scripts/sat3.js
KISSAT=$ROOT/bin/kissat-4.0.4-linux-amd64
mkdir -p "$OUT"
CNF="$OUT/$TAG.cnf"
LOG="$OUT/$TAG.kissat.log"
MODEL="$OUT/$TAG.model.txt"
WIT="$OUT/$TAG.witness.json"
STO="$OUT/$TAG.stones.json"
export R_W=$W R_M=$M R_Q=$Q R_MODE="$MODE" R_ROWY="$ROWY"
export R_RECORDS="$OUT/records.jsonl" R_CAP=$CAP
export R_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
G0=$(date +%s.%N)
if [ "$MODE" = def ]; then
  export R_MODE=deficient
  META=$(node "$SATJS" "$W" "$M" "$Q" --deficient $EXTRA "$CNF") || { echo "GEN FAIL"; exit 3; }
else
  export R_MODE=rowfixed
  META=$(node "$SATJS" "$W" "$M" "$Q" --rowY="$ROWY" $EXTRA "$CNF") || { echo "GEN FAIL"; exit 3; }
fi
G1=$(date +%s.%N)
export R_G0=$G0 R_G1=$G1
export R_VARS=$(echo "$META" | python3 -c "import json,sys;print(json.load(sys.stdin)['vars'])")
export R_CLAUSES=$(echo "$META" | python3 -c "import json,sys;print(json.load(sys.stdin)['clauses'])")
export R_CURVES=$(echo "$META" | python3 -c "import json,sys;print(json.load(sys.stdin)['curves'])")
export R_CNFMD5=$(md5sum "$CNF" | cut -d' ' -f1)
T0=$(date +%s.%N)
"$KISSAT" $KCFG --time="$CAP" "$CNF" > "$LOG" 2>&1
RC=$?
T1=$(date +%s.%N)
export R_T0=$T0 R_T1=$T1 R_RC=$RC
RESULT=$(grep -m1 -oE "^s (SATISFIABLE|UNSATISFIABLE|INDETERMINATE|UNKNOWN)" "$LOG" | cut -d' ' -f2)
CONFLICTS=$(grep -oE "c +conflicts: *[0-9]+" "$LOG" | head -1 | grep -oE "[0-9]+")
if [ -z "$CONFLICTS" ]; then CONFLICTS=$(grep -oE "conflicts[: ]+[0-9]+" "$LOG" | head -1 | grep -oE "[0-9]+"); fi
export R_RESULT=${RESULT:-UNKNOWN} R_CONFLICTS=${CONFLICTS:-}
export R_EXTRA_LABEL="${EXTRA:-}" R_KCFG_LABEL="${KCFG:-}"
if [ "$RESULT" = SATISFIABLE ]; then
  grep '^v ' "$LOG" > "$MODEL"
  node "$SAT3" decode "$W" "$M" "$Q" "$MODEL" --json="$WIT" > "$OUT/$TAG.decode.out" 2>&1
  node -e "const d=JSON.parse(require('fs').readFileSync('$WIT','utf8'));require('fs').writeFileSync('$STO',JSON.stringify(d.stones))"
  JS=$(node "$FW/jsverify.cjs" "$W" "$M" "$Q" "$STO" 2>&1); JSRC=$?
  PY=$(python3 "$FW/pyverify.py" "$W" "$M" "$Q" "$STO" 2>&1); PYRC=$?
  TS=$(node --experimental-strip-types "$FW/tsverify.mjs" "$W" "$M" "$Q" "$STO" 2>&1); TSRC=$?
  export R_WIT="$WIT" R_VJS="$JS" R_VJSRC=$JSRC R_VPY="$PY" R_VPYRC=$PYRC R_VTS="$TS" R_VTSRC=$TSRC
  printf '%s\n' "$JS" > "$OUT/$TAG.verify_js.out"
  printf '%s\n' "$PY" > "$OUT/$TAG.verify_py.out"
  printf '%s\n' "$TS" > "$OUT/$TAG.verify_ts.out"
  python3 "$FW/recorder.py"
elif [ "$RESULT" = UNSATISFIABLE ]; then
  python3 "$FW/recorder.py"
else
  rm -f "$CNF"
  python3 "$FW/recorder.py"
fi
