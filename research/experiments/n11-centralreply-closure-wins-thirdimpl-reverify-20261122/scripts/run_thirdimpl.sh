#!/bin/bash
# run_thirdimpl.sh <key_id> <runtag> <kind>  -- kind: target|anchor|negative
# One third-implementation solver process per row (1 solver / 1 row / 1 process).
# Result appended to output/status.log. Determinism pairs are (a, b).
set -u
KEY="$1"; TAG="$2"; KIND="$3"
cd "$(dirname "$0")/.."
WITNESS_ROWS="$(node -e '
const fs=require("fs");
const j=JSON.parse(fs.readFileSync("input/rows.json","utf8"));
const all=[...j.targets,...j.anchors,...j.negatives];
const r=all.find(x=>x.key_id===process.argv[1]);
if(!r){process.exit(9)}
if(r.stones) console.log("--stones="+r.stones);
if(r.legal!=null&&r.legal>=0) console.log("--legal="+r.legal);
console.log("--lo="+r.lo); console.log("--hi="+r.hi);
' "$KEY")" || { echo "ROW-LOOKUP-FAIL $KEY" >> output/status.log; exit 47; }
DIR=output/targets; [ "$KIND" = "anchor" ] && DIR=output/anchors; [ "$KIND" = "negative" ] && DIR=output/negative
mkdir -p "$DIR"
OUTF="$DIR/$KEY.$TAG.out"
SRC="input/$KEY.input.csv"
# source-input linkage gate: the machine-derived input must carry the same lo/hi/legal
node -e '
const fs=require("fs");
const csv=fs.readFileSync(process.argv[1],"utf8").trim().split(",");
const j=JSON.parse(fs.readFileSync("input/rows.json","utf8"));
const r=[...j.targets,...j.anchors,...j.negatives].find(x=>x.key_id===process.argv[2]);
if(!r){process.exit(9)}
if(BigInt(csv[3])!==BigInt(r.lo)||BigInt(csv[4])!==BigInt(r.hi)||parseInt(csv[5])!==r.legal||parseInt(csv[2])!==r.stones){console.error("INPUT-LINK MISMATCH");process.exit(46)}
' "$SRC" "$KEY" || { echo "INPUT-LINK-FAIL $KEY" >> output/status.log; exit 46; }
# shellcheck disable=SC2086
node scripts/third_impl.js $WITNESS_ROWS --row="$KEY$TAG" --cap=300000000 --wallcap=240 --memo-power=22 > "$OUTF" 2>&1
RC=$?
echo "RUN key=$KEY tag=$TAG kind=$KIND rc=$RC out=$OUTF $(grep -o '^third,.*' "$OUTF" | head -1)" >> output/status.log
exit $RC
