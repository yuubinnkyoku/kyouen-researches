#!/usr/bin/env python3
"""Fresh independent re-audit of the Part SY wave-C official outputs
(third host). Reads NO Part SY audit/maker code. Independently parses the
84 official target raws + 3 calibration raws, re-derives every expectation
from gate-rows.json and the published probe raws carried in the wave-B
cross-check kit, and checks the third-impl pillar against the replica and
C++ pillars at verdict level. Fail-closed: any mismatch -> rc=1.

Host: this lane. Disclosed: the author of this script had read the first 40
lines of the published audit_sy.py docstring before writing it (disclosure
in the log); parsing, gate design and the raw-to-expectation derivation here
are fresh.
"""
import json, hashlib, os, sys, re

SY = os.environ.get("SY_BASE", "/home/user/work/sy/sykit")
CC = os.environ.get("CC_BASE", "/home/user/work/sy/cckit")
fails = []

def gate(cond, msg):
    if not cond:
        fails.append(msg)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def parse_third(p):
    """Fresh parser for third-impl raw lines:
    third,<row>,5,<legal>,<legal>,<result>,<expansions>,<ttHits>,<wall>,<lo>,<hi>,clean,...
    followed by an rc=0 line."""
    lines = [l.rstrip("\n") for l in open(p) if l.strip()]
    gate(lines[-1] == "rc=0", f"{p}: missing rc=0 trailer")
    c = lines[0].split(",")
    gate(c[0] == "third", f"{p}: token0 != third")
    gate(c[11].startswith("clean"), f"{p}: not clean")
    return {
        "row": c[1], "stones": int(c[2]), "legal": int(c[3]),
        "legal2": int(c[4]), "result": int(c[5]), "expansions": int(c[6]),
        "ttHits": int(c[7]), "wall": float(c[8]), "lo": int(c[9]),
        "hi": int(c[10]),
    }

def parse_probe_raw(p):
    """Fresh parser for the seventh-cost probe replica raws (CSV):
    ...,legal=c[3],is_or=c[4],budget=c[5],result=c[6],nodes=c[7],wall=c[8],lo=c[9],hi=c[10]."""
    rows = []
    for line in open(p):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        c = line.split(",")
        rows.append(dict(stones=int(c[2]), legal=int(c[3]), is_or=int(c[4]),
                         budget=int(c[5]), result=int(c[6]), nodes=int(c[7]),
                         lo=int(c[9]), hi=int(c[10])))
    return rows

# --- load expectations ---
gr = json.load(open(f"{SY}/input/gate-rows.json"))
targets = gr["targets"]
gate(gr["schema"] == "n11-seventhcost-thirdimpl-corroboration-rows-v1", "H0 schema")
gate(gr["declaration_head"].startswith("47ae14ea"), "H0 declaration head")
gate(gr["canonical_head"]["sha256"].startswith("42dbb58f"), "H0 canonical head")
gate(gr["canonical_head"]["rows"] == 6832, "H0 canonical rows")

# kit pins: SY kit scripts must equal the cross-check kit byte-clones
gate(sha(f"{SY}/scripts/third_impl.js") == sha(f"{CC}/third_impl.js"), "H1 third_impl vs crosscheck clone")
gate(sha(f"{SY}/scripts/verify_tbl.js") == sha(f"{CC}/verify_tbl.js"), "H1 verify_tbl vs crosscheck clone")
gate(sha(f"{SY}/scripts/jsreplay_lane.js") == sha(f"{CC}/jsreplay_lane.js"), "H1 jsreplay vs crosscheck clone")
gate(sha(f"{SY}/input/gate-rows.json") == sha(f"{CC}/gate-rows.json"), "H1 gate-rows vs crosscheck clone")
for k in range(1, 43):
    kk = f"k{k:02d}"
    gate(sha(f"{SY}/input/{kk}.input.csv") == sha(f"{CC}/syinput/{kk}.input.csv"), f"H1 input {kk} vs crosscheck clone")

# --- calibration ---
c1a = open(f"{SY}/output/c1a-verify-tbl.txt").read().splitlines()
gate(c1a[0] == "replica quads 95670 mine quads 95670", "H2 c1a quads")
gate(c1a[1] == "triples checked 195044 mismatches 0", "H2 c1a triples")
gate(c1a[2] == "rc=0", "H2 c1a rc")
k06 = parse_third(f"{SY}/output/c1b-k06.txt")
k38 = parse_third(f"{SY}/output/c1b-k38.txt")
gate(k06["result"] == 2 and k06["expansions"] == 9474431, "H2 calib-k06 LOSS(2) 9,474,431")
gate(k38["result"] == 2 and k38["expansions"] == 25898941, "H2 calib-k38 LOSS(2) 25,898,941")
gate(k06["lo"] == 10376293541462675456 and k06["hi"] == 65536, "H2 calib-k06 key")
gate(k38["lo"] == 10376293541461626880 and k38["hi"] == 66048, "H2 calib-k38 key")

# --- 42 targets: two cold passes each ---
wins, losses = [], []
bill = 0
for k in range(1, 43):
    kk = f"k{k:02d}"
    t = targets[kk]
    p1 = parse_third(f"{SY}/output/raw/{kk}.p1.txt")
    p2 = parse_third(f"{SY}/output/raw/{kk}.p2.txt")
    for p, tag in ((p1, "p1"), (p2, "p2")):
        gate(p["row"] == f"{kk}.{tag}", f"{kk} {tag} row label")
        gate(p["stones"] == 5, f"{kk} {tag} stones")
        gate(p["legal"] == int(t["legal"]) and p["legal2"] == int(t["legal"]), f"{kk} {tag} legal")
        gate(p["lo"] == int(t["lo"]) and p["hi"] == int(t["hi"]), f"{kk} {tag} lo/hi vs gate-rows")
        gate(p["result"] == int(t["expected_result"]), f"{kk} {tag} result {p['result']} vs expected {t['expected_result']}")
        gate(p["legal"] == int(t["replica_expected_quad"].split(",")[0]), f"{kk} {tag} quad legal")
        gate(p["result"] == int(t["replica_expected_quad"].split(",")[2]), f"{kk} {tag} quad result")
    # cold pair identity (result + expansions + ttHits)
    gate(p1["result"] == p2["result"], f"{kk} pair result")
    gate(p1["expansions"] == p2["expansions"], f"{kk} pair expansions")
    gate(p1["ttHits"] == p2["ttHits"], f"{kk} pair ttHits")
    bill += p1["expansions"] + p2["expansions"]
    # raw file count integrity: exactly k01..k42 p1/p2 exist
    if p1["result"] == 2:
        losses.append(kk)
    elif p1["result"] == 1:
        wins.append(kk)
    else:
        fails.append(f"{kk} result not in {{1,2}}")

gate(sorted(wins) == ["k05"], f"H3 win set {wins}")
gate(len(losses) == 41, f"H3 loss count {len(losses)}")
gate(sorted(losses + wins) == [f"k{i:02d}" for i in range(1, 43)], "H3 key coverage")
gate(bill == 529416996, f"H4 expansion bill {bill}")

# --- pillar consistency: third-impl verdict vs replica + C++ gate pillars ---
ccgr = json.load(open(f"{CC}/gate-rows.json"))
for k in range(1, 43):
    kk = f"k{k:02d}"
    t = targets[kk]
    q = [int(x) for x in t["replica_expected_quad"].split(",")]  # legal,budget,result,nodes
    # replica pillar: re-derive from the probe raws (cross-check kit clones)
    r2 = parse_probe_raw(f"{CC}/probe/raw/at2m-{kk}.out.csv")[0]
    if r2["result"] == 0:
        a = parse_probe_raw(f"{CC}/probe/raw/at15m-run1-{kk}.out.csv")[0]
        if a["result"] == 0:
            ra = parse_probe_raw(f"{CC}/probe/raw/at50m-run1-k05.out.csv")[0] if kk == "k05" else None
            gate(kk == "k05", f"H5 {kk} parked but not k05")
            rp = (ra["result"], 50000000, ra["nodes"])
        else:
            rp = (a["result"], 15000000, a["nodes"])
    else:
        rp = (r2["result"], 2000000, r2["nodes"])
    gate(rp[0] == int(t["expected_result"]), f"H5 {kk} replica verdict vs expected")
    gate(q[2] == rp[0], f"H5 {kk} quad result vs replica")
    p1 = parse_third(f"{SY}/output/raw/{kk}.p1.txt")
    gate(p1["result"] == rp[0], f"H5 {kk} third-impl verdict {p1['result']} vs replica verdict {rp[0]}")

# C++ gate pillar: SW (41 LOSS) + SX (k05 WIN) expected quadruples
for kk in [f"k{i:02d}" for i in range(1, 43) if i != 5]:
    swq = None
    tg = json.load(open(f"{CC}/sw/gate-rows.json")).get("targets", {})
    if kk in tg and "expected_quad" in tg[kk]:
        swq = [int(x) for x in tg[kk]["expected_quad"].split(",")]
    if swq is not None:
        t = targets[kk]
        gate(swq[2] == int(t["expected_result"]), f"H6 {kk} SW C++ verdict vs expected")
        p1 = parse_third(f"{SY}/output/raw/{kk}.p1.txt")
        gate(p1["result"] == swq[2], f"H6 {kk} third-impl verdict vs SW C++ verdict")
sxt = json.load(open(f"{CC}/sx/gate-rows.json")).get("target", {})
if isinstance(sxt.get("k05"), dict) and "expected" in sxt["k05"]:
    q4 = [int(x) for x in sxt["k05"]["expected"].split(",")]
    p1 = parse_third(f"{SY}/output/raw/k05.p1.txt")
    gate(q4 == [90, 50000000, 1, 15763505], "H6 SX k05 quad value")
    gate(p1["result"] == q4[2] == 1, "H6 k05 third-impl WIN vs SX C++ WIN")

# --- raw count integrity: exactly 84 raws, no extras ---
names = sorted(os.listdir(f"{SY}/output/raw"))
want = sorted([f"k{i:02d}.{p}.txt" for i in range(1, 43) for p in ("p1", "p2")])
gate(names == want, "H7 raw set != 84 expected files")

print(f"INDEPENDENT-REAUDIT targets=42 (41 LOSS + 1 WIN) raws=84 pairs=42 "
      f"expansion_bill={bill} failures={len(fails)} verdicts_consumed=0 status=UNCONSUMED")
for f in fails:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
