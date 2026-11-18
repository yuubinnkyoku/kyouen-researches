#!/bin/bash
# sweep_driver_5xq7.sh — five-row-q7 band-closure resume sweep driver (2026-11-18).
# Band: (5,7) def-mode UNSAT sweep of m=35..157 (genfast3 chord-pair census + kissat 4.0.4, 230s cap).
# Resume-safe: skips widths already present in records.jsonl; appends one JSON record per width
# in the exact published schema. Curves meta is checked against output/ts-census-fullband.json
# (third-system predicted table) before each solve; CURVES-MISMATCH is printed on failure.
# Usage: SEVEN_SCRIPTS=<dir with sat.js/sat2.js> bash sweep_driver_5xq7.sh <m_lo> <m_hi>
set -u
CAP=230
for m in $(seq "$1" "$2"); do
  if grep -q "\"m\":$m," records.jsonl 2>/dev/null; then continue; fi
  node genfast3.js 5 "$m" 7 --deficient cnf/c5x${m}q7_def.cnf > meta_m${m}.json 2>&1
  curves=$(python3 -c "import json;print(json.load(open('meta_m${m}.json'))['curves'])")
  pred=$(python3 - "ts-census-fullband.json" "$m" <<'EOF'
import json,sys
d=json.load(open(sys.argv[1]))
print(d['counts'].get(sys.argv[2]) if isinstance(d['counts'],dict) else None)
EOF
)
  if [ "$curves" != "$pred" ]; then echo "CURVES-MISMATCH m=$m meta=$curves pred=$pred"; fi
  st=$(date +%s)
  timeout $CAP ./kissat-4.0.4-linux-amd64 cnf/c5x${m}q7_def.cnf > raw_m${m}.txt 2>&1
  rc=$?
  en=$(date +%s)
  wall=$((en-st))
  res="INDET"
  if [ $rc -eq 20 ]; then res="UNSAT"; fi
  python3 - "$m" "$res" "$rc" "$wall" meta_m${m}.json <<'EOF'
import json, sys, re, datetime
m, res, rc, wall = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
meta = json.load(open(sys.argv[5]))
log = open('raw_m%s.txt' % m).read()
cf = re.search(r'^c conflicts:\s+(\d+)', log, re.M)
pt = re.search(r"^c process-time:.*?(\S+)\s+seconds", log, re.M)
conf = int(cf.group(1)) if cf else None
sec = float(pt.group(1)) if pt else float(wall)
rec = {"w":5,"m":int(m),"q":7,"lex":"none","generator":"genfast3",
       "vars":meta["vars"],"clauses":meta["clauses"],"curves":meta["curves"],
       "kissat":{"result":res,"rc":rc,"conflicts":conf,"sec":sec},
       "date":datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")}
with open('records.jsonl','a') as f:
    f.write(json.dumps(rec, separators=(',',':')) + "\n")
json.dump(rec, open('raw_m%s.json' % m, 'w'), separators=(',',':'))
print("DONE m=%s %s conflicts=%s sec=%s curves=%s" % (m, res, conf, sec, meta["curves"]))
EOF
done
echo "SWEEP-BATCH-COMPLETE"
