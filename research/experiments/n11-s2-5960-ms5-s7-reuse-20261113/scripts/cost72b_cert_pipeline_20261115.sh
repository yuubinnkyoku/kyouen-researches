#!/bin/bash
# cost72b_cert_pipeline_20261115.sh - exact drivers used to extract and verify the 13
# cost-72b WIN7-D10 certificates on 2026-11-15 (repo-verbatim
# class4_child1_cert_extractor_exact.ts + generic independent verifier
# verify_bit7_win7_cert.ts; loser first moves enumerated by legal_candidates.py).
# Usage: extract_one.sh <bit>; assemble_verify_one.sh <bit>
# Both were run from /home/user/kr with the repo scripts fetched byte-exact.

# ===== extract_one.sh (verbatim) =====
b=$1
child=00000000000000809102000002000000
root=$(python3 -c "print(format(int('$child',16)|(1<<$b),'032x'))")
moves=$(python3 scripts/legal_candidates.py $root | tail -1)
out=output/cost72b-certs/bit$b-rows.txt
rm -f $out
t0=$(date +%s.%N)
node --experimental-strip-types scripts/class4_child1_cert_extractor_exact.ts --child $child --bit $b --moves "$moves" --out $out > output/cost72b-certs/bit$b-extract.json
rc=$?
t1=$(date +%s.%N)
echo "bit $b exit $rc wall $(echo "$t1-$t0"|bc)s"
python3 -c "
import json
d=json.load(open('output/cost72b-certs/bit$b-extract.json'))
print('nRows',d.get('nRows'),'sum',d.get('sum'),'fbt_drops',d.get('fbt_drops'),'fatal',d.get('fatal'))
pm=d.get('perMove',{})
print('moves',len(pm),'all ok',all(v['ok'] and not v['capped'] for v in pm.values()))
tr=[v['terminalRange'] for v in pm.values() if v['terminalRange']]
print('terminal range global', min(t[0] for t in tr), max(t[1] for t in tr))
"
wc -l $out

# ===== assemble_verify_one.sh (verbatim) =====
b=$1
child=00000000000000809102000002000000
root=$(python3 -c "print(format(int('$child',16)|(1<<$b),'032x'))")
rows=output/cost72b-certs/bit$b-rows.txt
cert=output/cost72b-certs/bit$b-root-$root.cert
cons=output/cost72b-certs/bit$b-consumed.txt
{ echo "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"; echo "root $root"; LC_ALL=C sort -u $rows; } > $cert
moves=$(python3 scripts/legal_candidates.py $root | tail -1)
rm -f $cons
node --experimental-strip-types scripts/verify_bit7_win7_cert.ts --cert $cert --root $root --root-check --subroots "$moves" --consumed-out $cons > output/cost72b-certs/bit$b-verify.json 2> output/cost72b-certs/bit$b-verify.err
echo "bit $b verify exit $?"
python3 - "$b" <<'PYEOF'
import json, sys
b = sys.argv[1]
root_check = None
rows = set()
with open(f"output/cost72b-certs/bit{b}-root-" + __import__('subprocess').run(
    ["python3","-c",f"print(format(int('00000000000000809102000002000000',16)|(1<<{b}),'032x'))"],
    capture_output=True,text=True).stdout.strip() + ".cert") as f:
    for ln in f:
        p = ln.split()
        if len(p) == 2 and len(p[0]) == 32 and p[1].isdigit():
            rows.add(p[0])
cons = set()
with open(f"output/cost72b-certs/bit{b}-consumed.txt") as f:
    for ln in f:
        ln = ln.strip()
        if ln: cons.add(ln)
missing = rows - cons
extra = cons - rows
print(f"bit {b}: certRows {len(rows)} consumed {len(cons)} missing {len(missing)} extra {len(extra)}")
if missing or extra:
    print("SAMPLE missing:", sorted(missing)[:3], "extra:", sorted(extra)[:3])
PYEOF
cat output/cost72b-certs/bit$b-verify.err | head -5
python3 -c "
import json
lines=[l for l in open('output/cost72b-certs/bit$b-verify.json').read().strip().split(chr(10)) if l]
rc=json.loads(lines[0]); st=json.loads(lines[1])
print('rootcheck:', rc)
print('rows:', st['rows'], 'subroots:', len(st['stats']))
tmin=min(v['range'][0] for v in st['stats'].values()); tmax=max(v['range'][1] for v in st['stats'].values())
print('terminal range:', tmin, tmax)
"
