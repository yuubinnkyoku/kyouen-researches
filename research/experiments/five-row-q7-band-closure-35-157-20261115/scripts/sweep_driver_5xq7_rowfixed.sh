#!/bin/bash
# sweep57split.sh — rowfixed-split-first band-closure sweep for (5,7) widths.
# deficient-mode = OR over rowY in {0..4} of rowfixed instances; V-mirror y<->4-y
# makes rows {0,1,2} a complete cover. rowfixed UNSAT for Y=0,1,2 => complete
# nonexistence proof for the width. Usage: bash sweep57split.sh <m_lo> [m_hi]
set -u
export SEVEN_SCRIPTS=${SEVEN_SCRIPTS:-/home/user/work/f57band/seven/scripts}
cd /home/user/work/f57band
CAP=${CAP:-230}
for m in $(seq "$1" "${2:-$1}"); do
  for y in 2 1 0; do
    if grep -q "\"m\":$m,\"q\":7,\"mode\":\"rowfixed\",\"rowY\":$y," records-split.jsonl 2>/dev/null; then continue; fi
    node genfast3.js 5 "$m" 7 --rowY=$y cnf/c5x${m}q7_rY${y}.cnf > meta_m${m}_rY${y}.json 2>&1
    curves=$(python3 -c "import json;print(json.load(open('meta_m${m}_rY${y}.json'))['curves'])")
    pred=$(python3 -c "
import json
d=json.load(open('ts-census-fullband.json'))
print(d['counts'].get('$m') if isinstance(d['counts'],dict) else None)")
    if [ "$curves" != "$pred" ]; then echo "CURVES-MISMATCH m=$m meta=$curves pred=$pred"; fi
    timeout $CAP ./kissat-4.0.4-linux-amd64 cnf/c5x${m}q7_rY${y}.cnf > raw_m${m}_rY${y}.txt 2>&1
    rc=$?
    res="INDET"; if [ $rc -eq 20 ]; then res="UNSAT"; fi
    python3 - "$m" "$y" "$res" "$rc" meta_m${m}_rY${y}.json <<'EOF'
import json, sys, re, datetime
m, y, res, rc = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
meta = json.load(open(sys.argv[5]))
log = open('raw_m%s_rY%s.txt' % (m, y)).read()
cf = re.search(r'^c conflicts:\s+(\d+)', log, re.M)
pt = re.search(r"^c process-time:.*?(\S+)\s+seconds", log, re.M)
conf = int(cf.group(1)) if cf else None
sec = float(pt.group(1)) if pt else None
rec = {"w":5,"m":int(m),"q":7,"mode":"rowfixed","rowY":int(y),"lex":"none","generator":"genfast3",
       "vars":meta["vars"],"clauses":meta["clauses"],"curves":meta["curves"],
       "kissat":{"result":res,"rc":rc,"conflicts":conf,"sec":sec},
       "date":datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")}
with open('records-split.jsonl','a') as f:
    f.write(json.dumps(rec, separators=(',',':')) + "\n")
json.dump(rec, open('raw_m%s_rY%s.json' % (m, y), 'w'), separators=(',',':'))
print("DONE m=%s rY=%s %s conflicts=%s sec=%s" % (m, y, res, conf, sec))
EOF
    if [ "$res" != "UNSAT" ]; then echo "SPLIT-INDET m=$m rY=$y — width needs manual attention"; fi
  done
  echo "WIDTH m=$m complete"
done
echo "SPLIT-SWEEP-COMPLETE"
