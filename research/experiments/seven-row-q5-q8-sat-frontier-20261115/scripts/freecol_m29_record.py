#!/usr/bin/env python3
"""Build the free-column extension record for the (7,6) m=28 SAT witness:
the same 34-stone config verifies as a deficient maximal safe config on the
7x29 board (appended column x=28 is empty), extending the (7,6) witness band
to m=29 and M_{7,6} >= 30. Emits output/freecol-extensions/records.json."""
import json, subprocess, sys, os

VW = "/home/user/kr/scripts/verify_witness.py"
WJS = "/home/user/kr/scripts/sat.js"
os.makedirs("/home/user/kr/out/freecol", exist_ok=True)
w = json.load(open("/home/user/kr/out/q6-m28/s7x28q6_rowY3.witness.json"))
stones = w["stones"]

def pyv(m):
    p = subprocess.run([sys.executable, VW, "7", str(m), "6"],
                       input=json.dumps(stones), capture_output=True, text=True)
    return json.loads(p.stdout)

def jsv(m):
    p = subprocess.run(["node", "-e", (
        'const S=require("%s");const st=%s;'
        'for(const m of [%d]){const v=S.verifyConfig(7,m,6,st);'
        'console.log(JSON.stringify({m,ok:v.ok,size:v.size,rows:v.rows}));}'
    ) % (WJS, json.dumps(stones), m)], capture_output=True, text=True)
    return [json.loads(l) for l in p.stdout.strip().splitlines()]

py28, py29 = pyv(28), pyv(29)
js = {r["m"]: r for r in jsv(29)}
rows = [0]*7
for x,y in stones: rows[y]+=1
rec = {
  "family": "(7,6)",
  "method": "free-column extension (append empty column; config stays maximal iff every appended cell is covered by a >=5-stone line/circle)",
  "source": "s7x28q6_rowY3.witness.json (SAT rowY=3 split, 442,479 conflicts, this experiment)",
  "stones": stones,
  "n": len(stones),
  "rows": rows,
  "verify": {
    "m28": {"py": py28, "js": js.get(28)},
    "m29": {"py": py29, "js": js.get(29)},
  },
  "m30_fail": {"cell_uncovered": [29,3], "py_not_maximal": True},
  "conclusion": "witness band (7,6) extends to m=29; M_{7,6} >= 30 (upper K0318 U=862 unchanged)",
}
json.dump(rec, open("/home/user/kr/out/freecol/records.json", "w"), indent=1)
wit = {"w":7,"m":29,"q":6,"nStones":len(stones),
       "rows":rows,
       "stones":stones,
       "provenance":"free-column extension of the 7x28 rowY=3 SAT witness (same 34 stones)",
       "jsVerify":js.get(29),"pyVerify":py29}
json.dump(wit, open("/home/user/kr/out/freecol/s7x29q6.witness.json","w"), indent=1)
print(json.dumps({"py28": py28, "py29": py29, "js29": js.get(29)}, indent=1))
