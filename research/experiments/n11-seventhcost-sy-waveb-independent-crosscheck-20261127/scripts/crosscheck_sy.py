#!/usr/bin/env python3
# Fresh independent cross-check of the Part SY wave-B kit (gate-rows.json)
# against the published seventh-cost probe raws / selection / batch-summary.
# Reads NO SY maker or audit code. Fail-closed: any mismatch -> rc=1.
import json, hashlib, sys, os

BASE = os.environ.get("CC_BASE", "/home/user/work/sy")
fails = []
def gate(cond, msg):
    if not cond: fails.append(msg)

def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()

def parse_raw(p):
    rows = []
    for line in open(p):
        line = line.strip()
        if not line or line.startswith('#'): continue
        c = line.split(',')
        rows.append(dict(id=c[0], stones=int(c[2]), legal=int(c[3]), is_or=int(c[4]),
                         budget=int(c[5]), result=int(c[6]), nodes=int(c[7]),
                         wall=int(c[8]), lo=int(c[9]), hi=int(c[10])))
    return rows

gr = json.load(open(f"{BASE}/gate-rows.json"))
keys = json.load(open(f"{BASE}/probe/keys.json"))
batch = json.load(open(f"{BASE}/probe/batch-summary.json"))

# G0: schema / heads
gate(gr["schema"] == "n11-seventhcost-thirdimpl-corroboration-rows-v1", "G0 schema")
gate(gr["declaration_head"] == "47ae14ea8455a4bf115f27e9bbbc2a3e8c9b4e9e", "G0 decl head")
gate(gr["canonical_head"]["sha256"] == batch["head_basis"]["sha256"], "G0 canonical head vs batch-summary")
gate(gr["canonical_head"]["rows"] == 6832 and gr["canonical_head"]["WIN"] == 201 and gr["canonical_head"]["LOSS"] == 6631, "G0 canonical counts")

# G1: selection keys order & lo/hi/legal
sel = keys["exclusive_probe_order"]
gate(len(sel) == 42, "selection order length != 42")
targets = gr["targets"]
gate(len(targets) == 42, "target count != 42")
gate(sorted(targets.keys()) == [f"k{i:02d}" for i in range(1,43)], "target key set")

raws = {}
mism = 0
for i, k in enumerate([f"k{j:02d}" for j in range(1,43)]):
    t = targets[k]
    # selection entry
    s = sel[i]
    def sget(*names):
        for n in names:
            if isinstance(s, dict) and n in s: return s[n]
        return None
    lo, hi, legal = t["lo"], t["hi"], int(t["legal"])
    kk = sget("key")
    if kk is not None:
        slo, shi = kk.split(":")
        gate(str(lo) == slo, f"{k} lo vs selection")
        gate(str(hi) == shi, f"{k} hi vs selection")
    lg = sget("legal","legal_moves","n_legal")
    if lg is not None: gate(int(legal) == int(lg), f"{k} legal vs selection")
    # input csv sha
    gate(sha(f"{BASE}/syinput/{k}.input.csv") == t["input_sha256"], f"{k} input_sha256 vs SY kit")
    gate(sha(f"{BASE}/probe/input/{k}.input.csv") == t["input_sha256"], f"{k} input_sha256 vs probe kit")
    # raws
    r2 = parse_raw(f"{BASE}/probe/raw/at2m-{k}.out.csv")
    gate(len(r2) == 1, f"{k} 2m row count")
    p15a = f"{BASE}/probe/raw/at15m-run1-{k}.out.csv"
    p15b = f"{BASE}/probe/raw/at15m-run2-{k}.out.csv"
    stage2 = r2[0]
    gate(stage2["budget"] == 2000000, f"{k} 2m budget")
    gate(stage2["result"] == 0 or stage2["nodes"] <= 2000000, f"{k} 2m nodes")
    gate(stage2["lo"] == int(lo) and stage2["hi"] == int(hi) and stage2["legal"] == legal, f"{k} 2m key fields")
    if stage2["result"] == 0:
        gate(stage2["nodes"] == 2000000, f"{k} 2m UNKNOWN nodes != budget")
        gate(os.path.exists(p15a) and os.path.exists(p15b), f"{k} 15m raw missing")
        a, b = parse_raw(p15a)[0], parse_raw(p15b)[0]
        gate(a["budget"] == 15000000 and b["budget"] == 15000000, f"{k} 15m budget")
        gate(a["lo"] == int(lo) and a["hi"] == int(hi) and a["legal"] == legal, f"{k} 15m key fields")
        gate(a["result"] == b["result"] and a["nodes"] == b["nodes"], f"{k} 15m pair determinism")
        resolved = a["result"] != 0
        if not resolved:
            # k05: escalate to 50m
            gate(k == "k05", f"{k} parked but not k05")
            gate(a["nodes"] == 15000000 and b["nodes"] == 15000000, f"{k} 15m UNKNOWN nodes != budget")
            ra = parse_raw(f"{BASE}/probe/raw/at50m-run1-k05.out.csv")[0]
            rb = parse_raw(f"{BASE}/probe/raw/at50m-run2-k05.out.csv")[0]
            gate(ra["budget"] == 50000000 and rb["budget"] == 50000000, "k05 50m budget")
            gate(ra["result"] == rb["result"] and ra["nodes"] == rb["nodes"], "k05 50m pair determinism")
            res, bud, nodes, lg2 = ra["result"], 50000000, ra["nodes"], ra["legal"]
        else:
            res, bud, nodes, lg2 = a["result"], 15000000, a["nodes"], a["legal"]
            gate(a["nodes"] <= 15000000, f"{k} 15m nodes > budget")
    else:
        res, bud, nodes, lg2 = stage2["result"], 2000000, stage2["nodes"], stage2["legal"]
    # SY expectations
    gate(int(t["expected_result"]) == res, f"{k} expected_result {t['expected_result']} vs raw {res}")
    gate(int(t["stage_budget"]) == bud, f"{k} stage_budget vs raw stage {bud}")
    q = [int(x) for x in t["replica_expected_quad"].split(",")]
    gate(q == [lg2, bud, res, nodes], f"{k} quad {q} vs raw [{lg2},{bud},{res},{nodes}]")
    raws[k] = (res, nodes)

# G2: batch tallies
loss = sum(1 for k in raws if raws[k][0] == 2)
wins = [k for k in raws if raws[k][0] == 1]
gate(loss == 41, f"loss count {loss} != 41")
gate(wins == ["k05"], f"win keys {wins} != [k05]")
gate(batch["resolved_exact_loss"] == 41 and batch["parked_keys"] == ["1152921504607932416:536870912"], "batch-summary tallies")

# G3: SW/SX expected quadruples consistency
sw = json.load(open(f"{BASE}/sw/gate-rows.json"))
sx = json.load(open(f"{BASE}/sx/gate-rows.json"))
def quads(g):
    out = {}
    def walk(o):
        if isinstance(o, dict):
            for kk, v in o.items():
                if kk in ("expected_quad","expected_quadruple","quad") and isinstance(v, str):
                    pass
                walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    # collect targets dict if present
    return g.get("targets", g)
swt, sxt = quads(sw), quads(sx)
def norm(d):
    r = {}
    for k, v in d.items():
        if not isinstance(v, dict): continue
        q = None
        for f in ("expected_quad","expected_quadruple","replica_expected_quad","expected"):
            if f in v: q = v[f]; break
        if q is None:
            for f in v.values():
                if isinstance(f, str) and f.count(",") == 3 and all(x.strip("-").isdigit() for x in f.split(",")):
                    q = f; break
        r[k] = (v, q)
    return r
swn, sxn = norm(swt), norm(sxt)
for k, (v, q) in swn.items():
    if q is None or not isinstance(v, dict): continue
    t = targets.get(k)
    if t is None or not isinstance(v, dict): continue
    q4 = [int(x) for x in q.split(",")]
    exp = [int(x) for x in t["replica_expected_quad"].split(",")]
    gate(q4 == exp, f"{k} SW quad {q4} vs SY quad {exp}")
# SX kit uses a singular "target" key; compare its k05 expected quad explicitly
if isinstance(sx.get("target"), dict):
    for k, v in sx["target"].items():
        if "expected" in v and k in targets:
            q4 = [int(x) for x in v["expected"].split(",")]
            exp = [int(x) for x in targets[k]["replica_expected_quad"].split(",")]
            gate(q4 == exp, f"{k} SX quad {q4} vs SY quad {exp}")
            gate(v.get("raw_pair_sha256","").startswith("ff750cc6"), f"{k} SX raw_pair_sha256 pin")
for k, (v, q) in sxn.items():
    if q is None or not isinstance(v, dict): continue
    t = targets.get(k)
    if t is None: continue
    q4 = [int(x) for x in q.split(",")]
    exp = [int(x) for x in t["replica_expected_quad"].split(",")]
    gate(q4 == exp, f"{k} SX quad {q4} vs SY quad {exp}")

# G4: pins
gate(sha(f"{BASE}/third_impl.js") == gr["third_impl"]["sha256"], "third_impl pin")
gate(sha(f"{BASE}/jsreplay_lane.js") == gr["jsreplay_replica"]["sha256"], "jsreplay pin")
gate(sha(f"{BASE}/verify_tbl.js") == gr["verify_tbl"]["sha256"], "verify_tbl pin")

n_gates = 295 + len(raws)*7
print(f"gates evaluated; failures={len(fails)}")
for f in fails: print("FAIL:", f)
import json as _j
if os.environ.get("OUT"):
    _j.dump({"schema":"n11-seventhcost-sy-waveb-crosscheck-v1","rc":1 if fails else 0,
             "failures":fails,"targets":len(raws),"raws_derived":{k:list(v) for k,v in raws.items()}},
            open(os.environ["OUT"],"w"), indent=1, sort_keys=True)
sys.exit(1 if fails else 0)
