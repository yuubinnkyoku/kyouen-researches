#!/bin/bash
CLS="$1"; WALL="${2:-200000}"; BUDGET="${3:-265}"
OUT="output/class_$(echo $CLS | tr -d '[], ').jsonl"
mkdir -p output
T0=$(date +%s)
while true; do
  START=$(tail -1 "$OUT" 2>/dev/null | node -e 'let d="";process.stdin.on("data",c=>d+=c).on("end",()=>{try{const j=JSON.parse(d);console.log(j.cappedCase===-1?"DONE":(j.cappedCase===-2?j.nextIdx:"SLICE_CAP"))}catch(e){console.log(0)}})')
  if [ "$START" = "DONE" ]; then echo "CLASS $CLS COMPLETE"; break; fi
  if [ "$START" = "SLICE_CAP" ]; then echo "CLASS $CLS NODE_CAP-interrupted"; break; fi
  EL=$(( $(date +%s) - T0 )); if [ $EL -ge $BUDGET ]; then echo "CLASS $CLS budget reached at START=$START"; break; fi
  timeout 280 node m20_runner.ts "$CLS" "$START" "$WALL" 20 > /tmp/slice.json || { echo "runner failed rc=$?"; break; }
  node -e "const j=JSON.parse(require('fs').readFileSync('/tmp/slice.json','utf8'));j.class='$CLS';j.start=$START;j.wall=$WALL;console.log(JSON.stringify(j))" >> "$OUT"
  tail -1 "$OUT" | node -e 'let d="";process.stdin.on("data",c=>d+=c).on("end",()=>{const j=JSON.parse(d);console.error("slice: start="+j.start+" done="+j.done+" nextIdx="+j.nextIdx+" cappedCase="+j.cappedCase+" witnesses="+j.witnesses+" maxCase="+j.maxCaseNodes)})'
  if grep -q '"witnesses":[1-9]' "$OUT"; then echo "WITNESS FOUND in $CLS"; break; fi
done
