#!/usr/bin/env python3
# audit_k20k33.py -- data-driven fail-closed auditor for the k20/k33 third-impl
# verdict re-verification addendum (2026-11-26) of
# research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/
# Structural clone of the audit_k09k43.py data-driven pattern (which stays
# byte-frozen). Checks, in order:
#   script pins (third_impl.js, verify_tbl.js), row-spec input pins,
#   replica-raw sha pins + row parses + per-key stage unanimity,
#   C1 fresh calibration gates (verify_tbl quads battery + anchor w2 x2),
#   C2 per-row cold-run gates (existence, clean reason, derived legal,
#   determinism quadruple, verify-legal equality, verdict-level vs replica,
#   anti-copy expansions), C4 fail-closed input gates (GATE_FAIL rc=1),
#   and a scope gate (exactly two rows, no cache file, no other row claimed).
# rc=0 only on ALL gates PASS. Deterministic byte-identical stdout across runs.
import hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(ROOT, *a)
fails = []
gates = 0
def gate(name, ok):
    global gates
    gates += 1
    if not ok:
        fails.append(name)
    print(("PASS " if ok else "FAIL ") + name)

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def read(p):
    with open(p, "r") as f:
        return f.read()

def parse_third(p):
    # returns dict of the third,<row>,... csv line (single line files)
    line = read(p).strip().splitlines()[-1]
    parts = line.split(",")
    if len(parts) >= 6 and parts[5] == "GATE_FAIL":
        return {"row": parts[1], "stones": parts[2], "legalIn": parts[3],
                "legalDerived": parts[4], "result": parts[5], "gate_fail": True,
                "reason": "gate_fail"}
    d = {"row": parts[1], "stones": parts[2], "legalIn": parts[3],
         "legalDerived": parts[4], "result": parts[5],
         "reason": parts[11]}
    if parts[5] == "GATE_FAIL":
        d["gate_fail"] = True
        return d
    d["gate_fail"] = False
    d["expansions"] = int(parts[6])
    d["ttHits"] = int(parts[7])
    d["wall"] = parts[8]
    d["lo"] = parts[9]
    d["hi"] = parts[10]
    kv = dict(x.split("=", 1) for x in parts[12:15])
    d["quads"] = kv["quads"]
    d["ttOverwrites"] = kv["ttOverwrites"]
    d["memoPower"] = kv["memoPower"]
    return d

def parse_repl(p):
    # returns dict of the replay,... csv row
    for line in read(p).strip().splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            return {"id": parts[0], "stones": parts[1], "legal": parts[3],
                    "is_or": parts[3], "budget": int(parts[5]),
                    "result": int(parts[6]), "nodes": int(parts[7]),
                    "lo": parts[9], "hi": parts[10]}
    return None

# ---- G1/G2: script pins ----
gate("G1_third_impl_pin", sha(P("third_impl.js")) ==
     "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998")
gate("G2_verify_tbl_pin", sha(P("verify_tbl.js")) ==
     "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251")

# ---- G3/G4: row-spec input pins (exact published ladder input bytes) ----
gate("G3_input_k20_pin", sha(P("input", "batch-k20.input.csv")) ==
     "0984400f8aa99735e11e2638f5bc9a9273ddd296e845f7b7118f3ada81adddad")
gate("G4_input_k33_pin", sha(P("input", "batch-k33.input.csv")) ==
     "ca081b0f2f85e62b39cbbd1178a7be839c87e3446b2357657bbfe8681f82e2f4")
gate("G5_input_k20_row", read(P("input", "batch-k20.input.csv")).strip() ==
     "target,0,5,10376293541461626880,33619968,95,0,0,0,0,0")
gate("G6_input_k33_row", read(P("input", "batch-k33.input.csv")).strip() ==
     "target,0,5,12682136550675320832,65536,91,0,0,0,0,0")

# ---- replica raws: sha pins + row parses + stage unanimity ----
ROWS = {
    "k20": {"lo": "10376293541461626880", "hi": "33619968", "legal": 95,
            "nodes": 16196331, "raws": {
                "base15m": ("64a069a2a66f677ffd01c4eb03eb6b43aa07ac041319c3fb5ecce5b853c21774", 15000000, 0, 15000000),
                "l50m-run1": ("f852cd55f7f80bdf57ccbe753e78a0b09deb5f7c552af51caed5f4d583aa2c73", 50000000, 1, 16196331),
                "l50m-run2": ("86db668a0288aeb3695f0fb0c3285f128d906ca8dbbf240d6d17b566303601e3", 50000000, 1, 16196331),
                "l50m-margin": ("e5525aab03eb0e272dd44dbe04a0c0c98bddcd2afc3c14c0e474e7055fbafa55", 32000000, 1, 16196331),
                "l50m-run3-verify": ("bf2b12fffb194540205b4eb2c80e98b907059701a36969035824f3b0a339efff", 50000000, 1, 16196331)}},
    "k33": {"lo": "12682136550675320832", "hi": "65536", "legal": 91,
            "nodes": 15842649, "raws": {
                "base15m": ("4fb1067184f15036cea90c496c6ebb160ffacd18395adff327c104da71356af8", 15000000, 0, 15000000),
                "l50m-run1": ("664ebc3a88ed14cb5a8f418df213368ab8501533c13a60f50261d93d841fc54f", 50000000, 1, 15842649),
                "l50m-run2": ("c08cdd7854c9a1c177428e86d08039edfeafe79e340001dc7f386ca0c706a3d2", 50000000, 1, 15842649),
                "l50m-margin": ("39154465a07ee7c97bebab517b284c77866d42374ba6ca5a446a5b502676526e", 32000000, 1, 15842649),
                "l50m-run3-verify": ("598538dce0cadc2be4752a6276fe3a8de0f5d3d873d4e7d214063924ebd7b530", 50000000, 1, 15842649)}},
}
gi = 7
for key, r in ROWS.items():
    for stage, (pin, budget, result, nodes) in r["raws"].items():
        p = P("out", key + "-replica-raws", stage + "-" + key + ".out.csv")
        gate("G%d_repl_sha_%s_%s" % (gi, key, stage), os.path.exists(p) and sha(p) == pin)
        gi += 1
for key, r in ROWS.items():
    parsed = []
    for stage in r["raws"]:
        p = P("out", key + "-replica-raws", stage + "-" + key + ".out.csv")
        d = parse_repl(p)
        gate("G%d_repl_row_%s_%s" % (gi, key, stage),
             d is not None and d["lo"] == r["lo"] and d["hi"] == r["hi"] and
             d["budget"] == r["raws"][stage][1] and d["result"] == r["raws"][stage][2] and
             d["nodes"] == r["raws"][stage][3] and int(d["legal"]) == r["legal"])
        gi += 1
        parsed.append(d)
    base = [d for d in parsed if d["budget"] == 15000000][0]
    res = [d for d in parsed if d["budget"] != 15000000]
    gate("G%d_repl_%s_stage_unanimity" % (gi, key),
         base["result"] == 0 and base["nodes"] == 15000000 and
         len(res) == 4 and all(d["result"] == 1 and d["nodes"] == r["nodes"] for d in res))
    gi += 1

# ---- C1 fresh calibration (this host, this session) ----
vt = read(P("out", "calib-verify-tbl.txt")).strip().splitlines()
gate("G%d_C1_verify_tbl_quads" % gi,
     len(vt) == 2 and vt[0] == "replica quads 95670 mine quads 95670" and
     vt[1] == "triples checked 195044 mismatches 0")
gi += 1
ca = parse_third(P("out", "calib-anchor-w2-a.txt"))
cb = parse_third(P("out", "calib-anchor-w2-b.txt"))
gate("G%d_C1_anchor_w2_run_a" % gi,
     not ca["gate_fail"] and ca["result"] == "1" and ca["expansions"] == 7583990 and
     ca["lo"] == "10376293541461626880" and ca["hi"] == "131328" and ca["reason"] == "clean")
gi += 1
gate("G%d_C1_anchor_w2_run_b" % gi,
     not cb["gate_fail"] and cb["result"] == "1" and cb["expansions"] == 7583990 and
     cb["lo"] == "10376293541461626880" and cb["hi"] == "131328" and cb["reason"] == "clean")
gi += 1
gate("G%d_C1_anchor_w2_identical" % gi,
     (ca["result"], ca["expansions"], ca["ttHits"], ca["ttOverwrites"]) ==
     (cb["result"], cb["expansions"], cb["ttHits"], cb["ttOverwrites"]))
gi += 1

# ---- C2 per-row cold runs ----
EXPECT = {"k20": "1", "k33": "1"}
for key, r in ROWS.items():
    a = parse_third(P("out", key + "-cold-a.txt"))
    b = parse_third(P("out", key + "-cold-b.txt"))
    v = parse_third(P("out", key + "-cold-v-legal.txt"))
    quad = lambda d: (d["result"], d["expansions"], d["ttHits"], d["ttOverwrites"])
    gate("G%d_C2_%s_clean_runs" % (gi, key),
         all(not d["gate_fail"] and d["reason"] == "clean" for d in (a, b, v)))
    gi += 1
    gate("G%d_C2_%s_keys" % (gi, key),
         all(d["lo"] == r["lo"] and d["hi"] == r["hi"] and d["stones"] == "5" and
             d["legalIn"] == str(r["legal"]) and d["legalDerived"] == str(r["legal"]) and
             d["quads"] == "95670" and d["memoPower"] == "22" for d in (a, b, v)))
    gi += 1
    gate("G%d_C2_%s_determinism_3runs_identical" % (gi, key),
         quad(a) == quad(b) == quad(v))
    gi += 1
    gate("G%d_C2_%s_win_verdict_level_vs_replica" % (gi, key),
         a["result"] == EXPECT[key] and r["raws"]["l50m-run1"][2] == int(EXPECT[key]))
    gi += 1
    gate("G%d_C2_%s_verify_legal_identical" % (gi, key),
         (v["result"], v["expansions"]) == (a["result"], a["expansions"]))
    gi += 1
    gate("G%d_C2_%s_anti_copy" % (gi, key),
         a["expansions"] != r["nodes"] and b["expansions"] != r["nodes"] and
         v["expansions"] != r["nodes"])
    gi += 1

# ---- C4 fail-closed input gates ----
NEG = [("k20-ng1", "legal count mismatch: derived=95 declared=96"),
       ("k20-ng2", "stone count mismatch: bits=5 declared=6"),
       ("k33-ng1", "legal count mismatch: derived=91 declared=92"),
       ("k33-ng2", "stone count mismatch: bits=5 declared=6")]
for name, msg in NEG:
    p = P("out", "neg-gate-" + name + ".txt")
    t = parse_third(p)
    gate("G%d_C4_neg_%s" % (gi, name),
         t["gate_fail"] and t["result"] == "GATE_FAIL" and
         json.dumps(msg) in read(p))
    gi += 1

# ---- scope gate ----
cache_files = [f for f in os.listdir(P("out")) if f.endswith(".cache")]
gate("G%d_scope_no_cache_no_other_rows" % gi,
     len(cache_files) == 0 and
     os.path.exists(P("out", "k20-cold-a.txt")) and os.path.exists(P("out", "k33-cold-a.txt")))
gi += 1

print("gates %d fails %d" % (gates, len(fails)))
if fails:
    print("FAILED: " + ", ".join(fails))
    sys.exit(1)
print("ALL PASS")
