#!/usr/bin/env python3
# Tamper battery for crosscheck_sy.py (scratch copies only, never published).
import json, subprocess, os, shutil, sys
BASE = os.environ.get("CC_BASE", "/home/user/work/sy")
T = f"{BASE}/tamper"
shutil.rmtree(T, ignore_errors=True)
os.makedirs(T, exist_ok=True)
for d in ("probe","syinput","sw","sx"):
    shutil.copytree(f"{BASE}/{d}", f"{T}/{d}")
shutil.copy(f"{BASE}/third_impl.js", T); shutil.copy(f"{BASE}/jsreplay_lane.js", T)
shutil.copy(f"{BASE}/verify_tbl.js", T); shutil.copy(f"{BASE}/crosscheck_sy.py", T)
orig = open(f"{BASE}/gate-rows.json").read()

def run(tag, gr_text):
    open(f"{T}/gate-rows.json","w").write(gr_text)
    r = subprocess.run(["python3", f"{T}/crosscheck_sy.py"], cwd=T, capture_output=True, text=True, env={**os.environ, "CC_BASE": T})
    fails = [l for l in r.stdout.splitlines() if l.startswith("FAIL:")]
    print(f"{tag}: rc={r.returncode} first_fail={fails[0] if fails else 'NONE'}")
    return r.returncode, fails

import copy
g = json.loads(orig)
# T1: flip expected_result of k07 (2 -> 1)
g1 = copy.deepcopy(g); g1["targets"]["k07"]["expected_result"] = "1"
rc1, f1 = run("T1 expected_result flip k07", json.dumps(g1))
# T2: phantom budget flip on k20 stage_budget
g2 = copy.deepcopy(g); g2["targets"]["k20"]["stage_budget"] = "2000000"
rc2, f2 = run("T2 stage_budget flip k20", json.dumps(g2))
# T3: tamper a raw byte (k15 15m nodes)
p = f"{T}/probe/raw/at15m-run1-k15.out.csv"
b = open(p).read().replace("4499006","4499007")
open(p,"w").write(b)
rc3, f3 = run("T3 raw nodes edit k15", orig)
ok = rc1==1 and rc2==1 and rc3==1
print("TAMPER-BATTERY", "PASS 3/3 fail-closed" if ok else "FAIL")
sys.exit(0 if ok else 1)
