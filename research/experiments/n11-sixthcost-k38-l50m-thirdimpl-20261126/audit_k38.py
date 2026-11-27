#!/usr/bin/env python3
# audit_k38.py -- data-driven fail-closed auditor for the k38 L50M third-impl
# verdict re-verification (2026-11-26) of
# research/experiments/n11-sixthcost-k38-l50m-thirdimpl-20261126/.
# Structural clone of the audit_k20k33.py data-driven pattern (which stays
# byte-frozen). Checks, in order:
#   script pins (third_impl.js, verify_tbl.js, jsreplay.js), row-spec input pin,
#   canonical-head byte-clone pin + k38 freshness (pair absent),
#   replica-raw sha pins + row parses + stage structure,
#   C1 fresh calibration gates (verify_tbl quads battery + anchor w2 x2),
#   C2 k38 cold-run gates (clean reason, derived legal, determinism quadruple,
#   verify-legal equality, verdict-level vs replica, anti-copy expansions),
#   C4 fail-closed input gates (GATE_FAIL rc=1),
#   and a scope gate (exactly one target row, no cache file in out/).
# rc=0 only on ALL gates PASS. Deterministic byte-identical stdout across runs.
import hashlib, json, os, sys

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
    line = read(p).strip().splitlines()[-1]
    parts = line.split(",")
    if len(parts) >= 6 and parts[5] == "GATE_FAIL":
        return {"row": parts[1], "stones": parts[2], "legalIn": parts[3],
                "legalDerived": parts[4], "result": parts[5], "gate_fail": True,
                "reason": "gate_fail"}
    d = {"row": parts[1], "stones": parts[2], "legalIn": parts[3],
         "legalDerived": parts[4], "result": parts[5],
         "reason": parts[11]}
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
    for line in read(p).strip().splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            return {"id": parts[0], "stones": parts[1], "legal": parts[3],
                    "budget": int(parts[5]),
                    "result": int(parts[6]), "nodes": int(parts[7]),
                    "lo": parts[9], "hi": parts[10]}
    return None

# ---- G1..G3: script pins ----
gate("G1_third_impl_pin", sha(P("scripts", "third_impl.js")) ==
     "08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998")
gate("G2_verify_tbl_pin", sha(P("scripts", "verify_tbl.js")) ==
     "c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251")
gate("G3_jsreplay_pin", sha(P("scripts", "jsreplay.js")) ==
     "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df")

# ---- G4/G5: row-spec input pin (exact published probe-kit input bytes) ----
gate("G4_input_k38_pin", sha(P("input", "k38.input.csv")) ==
     "b6ef9f439ee0b6c9a35af08ff065a9323d0bec627beabb4defb9426a11d6600e")
gate("G5_input_k38_row", read(P("input", "k38.input.csv")).strip() ==
     "target,0,5,10376293541461626880,66048,100,0,0,0,0,0")

# ---- G6: canonical head byte-clone pin + G7 k38 freshness ----
gate("G6_canonical_head_pin", sha(P("input", "canonical-head.cache")) ==
     "dade15780ce6625cc70d93ba77b1560145dd2b9f096a53dce556d2fccf7e312b")
LO, HI = "10376293541461626880", "66048"
gate("G7_k38_fresh_vs_head",
     (LO + "," + HI) not in read(P("input", "canonical-head.cache")))

# ---- replica raws: sha pins + row parses + stage structure ----
RAWS = {
    "at2m": ("fbb16943aae1e72023c3417970444915b43606c4318f51c756521db7f2ba0f00", 2000000, 0, 2000000),
    "at15m-run1": ("fb93014e5553e2f175904134174f4c5937de7ac874c9f5ce2052097083944d65", 15000000, 0, 15000000),
    "at15m-run2": ("a38dc147d237f6416d96dcf93eeb4355d2d2ac2e72498cad335b86c56d34face", 15000000, 0, 15000000),
    "at50m-run1": ("f7e519586d8e9dd7c8378aef2c96ccd70479816056954e93ffdf16732178bfcc", 50000000, 2, 21839049),
    "at50m-run2": ("53d0f69d03d0b04520f9f832e517f177ed9b0e33c917db3f114a5a77a602fe03", 50000000, 2, 21839049),
}
gi = 8
for stage, (pin, budget, result, nodes) in RAWS.items():
    p = P("out", "k38-replica-raws", stage + "-k38.out.csv")
    gate("G%d_repl_sha_%s" % (gi, stage), os.path.exists(p) and sha(p) == pin)
    gi += 1
parsed = []
for stage, (pin, budget, result, nodes) in RAWS.items():
    p = P("out", "k38-replica-raws", stage + "-k38.out.csv")
    d = parse_repl(p)
    gate("G%d_repl_row_%s" % (gi, stage),
         d is not None and d["lo"] == LO and d["hi"] == HI and
         d["budget"] == budget and d["result"] == result and
         d["nodes"] == nodes and int(d["legal"]) == 100)
    gi += 1
    parsed.append((stage, d))
unknown = [d for s, d in parsed if s.startswith("at2m") or s.startswith("at15m")]
resolved = [d for s, d in parsed if s.startswith("at50m")]
gate("G%d_repl_stage_structure" % gi,
     len(unknown) == 3 and all(d["result"] == 0 for d in unknown) and
     unknown[0]["nodes"] == 2000000 and
     all(d["nodes"] == 15000000 for d in unknown[1:]) and
     len(resolved) == 2 and
     all(d["result"] == 2 and d["nodes"] == 21839049 for d in resolved))
gi += 1

# ---- C1 fresh calibration (this host, this session) ----
vt = read(P("out", "calib-verify-tbl.txt")).strip().splitlines()
gate("G%d_C1_verify_tbl_quads" % gi,
     len(vt) == 2 and vt[0] == "replica quads 95670 mine quads 95670" and
     vt[1] == "triples checked 195044 mismatches 0")
gi += 1
ca = parse_third(P("out", "calib-anchor-w2-a.txt"))
cb = parse_third(P("out", "calib-anchor-w2-b.txt"))
for nm, c in (("a", ca), ("b", cb)):
    gate("G%d_C1_anchor_w2_run_%s" % (gi, nm),
         not c["gate_fail"] and c["result"] == "1" and c["expansions"] == 7583990 and
         c["lo"] == "10376293541461626880" and c["hi"] == "131328" and
         c["reason"] == "clean" and c["legalDerived"] == "80" and
         c["ttHits"] == 4157314 and c["ttOverwrites"] == "3390391")
    gi += 1
gate("G%d_C1_anchor_w2_identical" % gi,
     (ca["result"], ca["expansions"], ca["ttHits"], ca["ttOverwrites"]) ==
     (cb["result"], cb["expansions"], cb["ttHits"], cb["ttOverwrites"]))
gi += 1

# ---- C2 k38 cold runs ----
EXPECT = "2"
a = parse_third(P("out", "k38-cold-a.txt"))
b = parse_third(P("out", "k38-cold-b.txt"))
v = parse_third(P("out", "k38-cold-v-legal.txt"))
quad = lambda d: (d["result"], d["expansions"], d["ttHits"], d["ttOverwrites"])
gate("G%d_C2_k38_clean_runs" % gi,
     all(not d["gate_fail"] and d["reason"] == "clean" for d in (a, b, v)))
gi += 1
gate("G%d_C2_k38_keys" % gi,
     all(d["lo"] == LO and d["hi"] == HI and d["stones"] == "5" and
         d["legalIn"] == "100" and d["legalDerived"] == "100" and
         d["quads"] == "95670" and d["memoPower"] == "22" for d in (a, b, v)))
gi += 1
gate("G%d_C2_k38_determinism_3runs_identical" % gi,
     quad(a) == quad(b) == quad(v))
gi += 1
gate("G%d_C2_k38_loss_verdict_level_vs_replica" % gi,
     a["result"] == EXPECT and resolved[0]["result"] == int(EXPECT) and
     resolved[1]["result"] == int(EXPECT))
gi += 1
gate("G%d_C2_k38_verify_legal_identical" % gi,
     (v["result"], v["expansions"]) == (a["result"], a["expansions"]))
gi += 1
gate("G%d_C2_k38_anti_copy" % gi,
     a["expansions"] != 21839049 and b["expansions"] != 21839049 and
     v["expansions"] != 21839049)
gi += 1

# ---- C4 fail-closed input gates ----
NEG = [("k38-ng1", "legal count mismatch: derived=100 declared=101"),
       ("k38-ng2", "stone count mismatch: bits=5 declared=6")]
for name, msg in NEG:
    p = P("out", "neg-gate-" + name + ".txt")
    t = parse_third(p)
    gate("G%d_C4_neg_%s" % (gi, name),
         t["gate_fail"] and t["result"] == "GATE_FAIL" and
         json.dumps(msg) in read(p))
    gi += 1

# ---- scope gate ----
cache_files = [f for f in os.listdir(P("out")) if f.endswith(".cache")]
gate("G%d_scope_no_cache_single_target" % gi,
     len(cache_files) == 0 and
     os.path.exists(P("out", "k38-cold-a.txt")) and
     not os.path.exists(P("out", "k20-cold-a.txt")))
gi += 1

print("gates %d fails %d" % (gates, len(fails)))
if fails:
    print("FAILED: " + ", ".join(fails))
    sys.exit(1)
print("ALL PASS")
