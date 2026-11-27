#!/usr/bin/env python3
"""make_kit_tenthcost2_adoption_20261127.py -- fresh maker for the
n11 tenth-cost k01/k02 canonical adoption kit (2026-11-27).

Machine-derived structural descendant of the published ninth-cost
adoption maker (make_kit_ninthcost12_adoption_20261127.py, sha256
03523c15...): the two adopted rows, all kit paths, all pinned shas,
the head basis (47280073), the pre-registered merged shape (6,889
rows WIN 207 / LOSS 6,682) and the comment blocks are re-derived for
this Part.  Disclosed deviation from the ninth maker: the C++ gate
audit is re-run live from the published gate kit's own
scripts/audit_gate.py (the ninth maker re-ran its gate kits' audits
the same way); no ninth-cost kit is read.

Fail-closed: every gate aborts before any output is written.
Verdicts are NOT consumed here.  11x11 stays UNKNOWN.
"""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE                              # work tree root (this lane layout; see README disclosure)
KIT = ROOT / "kitbuild" / "research" / "experiments" / "n11-tenthcost-k01k02-adoption-20261127"
REPL = ROOT / "kitbuild" / "research" / "experiments" / "n11-tenthcost-batch-stage1-2m-20261127"
GATEKIT = ROOT / "kitbuild" / "research" / "experiments" / "n11-tenthcost-k01k02-cppgate-20261127"
TI = ROOT / "kitbuild" / "research" / "experiments" / "n11-tenthcost-k01k02-thirdimpl-corroboration-20261127"
BASE = ROOT / "head.cache"               # merged-exact-s5-chain-plus-ninthcost12-20261127.cache
QUAR = ROOT / "quarantine.json"
POLICY = ROOT / "s5_evidence_policy.py"
MERGER = ROOT / "s5_union_merge.py"

SHA = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def die(msg):
    print("GATE FAILED: " + msg, file=sys.stderr); sys.exit(1)

ROWS = [
    ("k01", 1297036692683751424, 131074, 2, 6783438),
    ("k02", 1297036692683751424, 131136, 1, 8799140),
]
BASE_SHA = "4728007306598298f7fdb43d0368bc4e5fbd6c9435a38f8d1732d1df8368a622"
BASE_ROWS, BASE_WIN, BASE_LOSS = 6887, 206, 6681
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUAR_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
AUDIT1_SHA = None  # unused; live-vs-published equality is asserted below
OUT_ROWS, OUT_WIN, OUT_LOSS = 6889, 207, 6682

# ---- G0 pins -----------------------------------------------------------
for p, want in [(MERGER, MERGER_SHA), (POLICY, POLICY_SHA), (QUAR, QUAR_SHA), (BASE, BASE_SHA)]:
    if SHA(p) != want: die(f"pin sha drift: {p}")
# published kit MANIFEST self-verification (raw CDN bytes fetched to kitbuild copies)
for kit in (REPL, GATEKIT, TI):
    man = kit / "MANIFEST-sha256.txt"
    if not man.exists(): die(f"missing MANIFEST in {kit}")
    for line in man.read_text().strip().split("\n"):
        sha, path = line.split()
        f = ROOT / "kitbuild" / path
        if not f.exists() or SHA(f) != sha: die(f"kit MANIFEST mismatch: {path}")

# ---- G1 live re-run of the published C++ gate audit --------------------
r = subprocess.run([sys.executable, str(GATEKIT / "scripts" / "audit_gate.py")],
                   capture_output=True, text=True, cwd=str(GATEKIT))
if r.returncode != 0: die("live cppgate audit rc!=0: " + r.stdout + r.stderr)
live = r.stdout.strip()
pub = (GATEKIT / "output" / "audit_gate_run1.json").read_text().strip()
if live != pub: die("live audit output != published audit_gate_run1.json")
try:
    o = json.loads(live)
except Exception: die("live audit json parse")
if o.get("verdict") != "AUDIT-PASS" or o.get("head_sha256") != BASE_SHA: die("live audit verdict/head")

# ---- G2 re-parse of the three pillars ----------------------------------
def quad(path):
    t = Path(path).read_text()
    m = re.search(r"^replay,0,5,(\d+),0,(\d+),(\d+),(\d+),\d+,(\d+),(\d+)$", t, re.M)
    if not m: die(f"bad replica raw: {path}")
    return (m.group(1), m.group(2), m.group(3), m.group(4)), (m.group(5), m.group(6))

for name, lo, hi, res, nodes in ROWS:
    q1, k1 = quad(REPL / "raws" / f"at15m-{name}-p1.raw")
    q2, k2 = quad(REPL / "raws" / f"at15m-{name}-p2.raw")
    if q1 != q2 or k1 != k2: die(f"replica pair mismatch {name}")
    if q1 != (str({2:'86',1:'84'}[res]), "15000000", str(res), str(nodes)): die(f"replica quad {name}: {q1}")
    if k1 != (str(lo), str(hi)): die(f"replica key {name}")
    # C++ gate raws
    g1 = (GATEKIT / "output" / "raw" / f"{name}.p1.out").read_text()
    g2 = (GATEKIT / "output" / "raw" / f"{name}.p2.out").read_text()
    gg = lambda t: re.search(r"^replay,0,5,(\d+),0,(\d+),(\d+),(\d+),\d+,(\d+),(\d+)$", t, re.M).groups()
    if gg(g1) != gg(g2): die(f"gate pair mismatch {name}")
    if gg(g1) != (str({2:'86',1:'84'}[res]), "15000000", str(res), str(nodes), str(lo), str(hi)):
        die(f"gate quad {name}: {gg(g1)}")
    # third impl
    t1 = (TI / "output" / "raw" / f"{name}.p1.txt").read_text().split("\n")[0].split(",")
    t2 = (TI / "output" / "raw" / f"{name}.p2.txt").read_text().split("\n")[0].split(",")
    if t1[0:8] != t2[0:8] or t1[9:] != t2[9:]: die(f"third-impl pair mismatch {name}")
    if t1[5] != str(res) or t1[11] != "clean": die(f"third-impl result {name}")
    if t1[3] != t1[4] or t1[3] != {2:'86',1:'84'}[res]: die(f"third-impl legal {name}")

# ---- G3 freshness vs BASE ----------------------------------------------
blines = BASE.read_text().strip().split("\n")
brows = [l.split(",") for l in blines if l.startswith("s5verdict,")]
if len(brows) != BASE_ROWS: die(f"BASE rows {len(brows)}")
if sum(1 for b in brows if b[4] == "1") != BASE_WIN or sum(1 for b in brows if b[4] == "2") != BASE_LOSS: die("BASE win/loss counts")
for name, lo, hi, res, nodes in ROWS:
    if any(b[1] == str(lo) and b[2] == str(hi) for b in brows): die(f"freshness: {name} present in BASE")
if len({(r[1], r[2]) for r in ROWS}) != len(ROWS): die("duplicate adopted keys")
# WIN/LOSS conflict review vs BASE: same (lo,hi) with different verdict aborts (also merger-enforced)
for name, lo, hi, res, nodes in ROWS:
    for b in brows:
        if b[1] == str(lo) and b[2] == str(hi) and b[4] != str(res): die(f"WIN/LOSS conflict vs BASE: {name}")

# ---- G4 quarantine + canonical safety ---------------------------------
sys.path.insert(0, str(ROOT))
import s5_evidence_policy as pol
qk = pol.quarantined_cache_keys()
for name, lo, hi, res, nodes in ROWS:
    if (lo, hi) in qk: die(f"quarantined key {name}")
    if not pol.is_canonical_safe_s5_key((lo, hi)): die(f"not canonical-safe {name}")

# ---- G5 increment build ------------------------------------------------
KIT.mkdir(parents=True, exist_ok=True)
(KIT / "output").mkdir(exist_ok=True)
comment = """# n11 tenth-cost k01/k02 canonical adoption increment
#   (n11-tenthcost-k01k02-adoption-20261127, 2026-11-27) - fresh
#   2-row increment: 1 LOSS (k01) + 1 WIN (k02).  The canonical
#   head of record advances from merged-exact-s5-chain-plus-
#   ninthcost12 (sha256 47280073..., 6,887 rows WIN 206 /
#   LOSS 6,681) by consuming exactly the 2 published tenth-cost
#   rows.  Sources of record (all re-verified live by this maker
#   against published bytes): the tenth-cost batch stage-1 kit
#   (replica 15M cold pairs), the C++ scrutiny gate kit
#   (5/5 GATE-PASS, live audit re-run PASS) and the third-impl
#   corroboration kit (third_impl.js pin 08ea958f).
# Every adopted key is fresh to BASE 47280073... (absent from the
#   canonical head), quarantine-free and canonical-safe per
#   s5_evidence_policy; adopted node total 15,582,578
#   (bookkeeping, never verdicts).
# NO root verdict is consumed, NO class freed, NO class
#   excluded; nodes are bookkeeping, never verdicts; the standard
#   11x11 empty board, every central-reply root, the two-stone
#   root {60,27} and its remaining third moves {100,108} stay
#   UNKNOWN.
"""
inc = comment + "".join(f"s5verdict,{lo},{hi},5,{res},{nodes}\n" for _, lo, hi, res, nodes in ROWS)
(KIT / "output" / "increment-tenthcost2-adoption-20261127.cache").write_text(inc)

# adoption-manifest
man = {
 "schema": "n11-tenthcost-k01k02-adoption-manifest-v1",
 "base": {"path": "merged-exact-s5-chain-plus-ninthcost12-20261127.cache", "sha256": BASE_SHA,
          "rows": BASE_ROWS, "win": BASE_WIN, "loss": BASE_LOSS},
 "rows": [{"name": n, "key": f"{lo}:{hi}", "result": res, "nodes": nodes} for n, lo, hi, res, nodes in ROWS],
 "expected_merged_shape": {"rows": OUT_ROWS, "win": OUT_WIN, "loss": OUT_LOSS},
 "merger_sha256": MERGER_SHA,
 "kits": {"replica": "n11-tenthcost-batch-stage1-2m-20261127 (b8049d8b)",
          "cppgate": "n11-tenthcost-k01k02-cppgate-20261127 (55b65a7f)",
          "thirdimpl": "n11-tenthcost-k01k02-thirdimpl-corroboration-20261127 (232a4a52)"},
 "nodes_total_bookkeeping": 15582578,
 "status_guard": "adoption bookkeeping only; NO verdict consumed; 11x11 UNKNOWN",
}
(KIT / "adoption-manifest.json").write_text(json.dumps(man, indent=1) + "\n")

# ---- G6 merge x3 -------------------------------------------------------
outname = "merged-exact-s5-chain-plus-tenthcost-k01k02-20261127.cache"
outs = []
for i in (1, 2, 3):
    outp = ROOT / f"merged-run{i}.cache"
    audp = ROOT / f"merge-audit-run{i}.json"
    rc = subprocess.run([sys.executable, str(MERGER), "merge", "--out", str(outp),
                         "--audit", str(audp), str(BASE),
                         str(KIT / "output" / "increment-tenthcost2-adoption-20261127.cache")],
                        capture_output=True, text=True)
    if rc.returncode != 0: die(f"merger run{i} rc!=0: {rc.stdout}{rc.stderr}")
    outs.append(outp.read_bytes())
if outs[0] != outs[1] or outs[1] != outs[2]: die("merger outputs not byte-identical")
mrows = [l.split(",") for l in outs[0].decode().strip().split("\n") if l.startswith("s5verdict,")]
if len(mrows) != OUT_ROWS: die(f"merged rows {len(mrows)}")
win = sum(1 for m in mrows if m[4] == "1"); loss = sum(1 for m in mrows if m[4] == "2")
if win != OUT_WIN or loss != OUT_LOSS: die(f"merged shape {win}/{loss}")
(KIT / "output" / "merged").mkdir(exist_ok=True)
(KIT / "output" / "merged" / outname).write_bytes(outs[0])
for i in (1, 2, 3):
    (KIT / "output" / "merged" / f"merge-audit-run{i}.json").write_bytes((ROOT / f"merge-audit-run{i}.json").read_bytes())

print(json.dumps({"verdict": "MAKER-PASS", "increment_sha256": SHA(KIT / "output" / "increment-tenthcost2-adoption-20261127.cache"),
                  "merged_sha256": hashlib.sha256(outs[0]).hexdigest(),
                  "rows": OUT_ROWS, "win": OUT_WIN, "loss": OUT_LOSS}))
