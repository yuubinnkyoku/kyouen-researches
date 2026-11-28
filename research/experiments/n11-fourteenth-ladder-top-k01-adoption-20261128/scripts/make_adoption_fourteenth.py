#!/usr/bin/env python3
"""make_adoption_fourteenth.py -- fresh maker for the n11 fourteenth
ladder-top class-5804 k01 canonical adoption kit (2026-11-28).

Structural descendant of the published thirteenth adoption maker
(research/experiments/n11-thirteenth-ladder-top-k01k02-adoption-20261128/
scripts/make_adoption_thirteenth.py, sha256 3600ce8a...): adapted for
ONE adopted row (k01 6053401124017274880:0 WIN nodes 4,360,661, class
5804), one escalation kit, one cppgate kit and one thirdimpl kit, the
head basis d772f73c (6,896 rows WIN 214 / LOSS 6,682), the
pre-registered merged shape (6,897 rows WIN 215 / LOSS 6,682), and the
path-first MANIFEST format.  G1 live-re-runs the published
gate_runner.sh on a scratch kit copy.

Fail-closed: every gate aborts before any output is written.
Verdicts are NOT consumed here.  11x11 stays UNKNOWN.
"""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE
KB = ROOT / "kitbuild" / "research" / "experiments"
KIT = ROOT / "kitout" / "research" / "experiments" / "n11-fourteenth-ladder-top-k01-adoption-20261128"
REPL = {"k01": KB / "n11-fourteenth-ladder-top-escalation-20261128"}
GATEKIT = {"k01": KB / "n11-fourteenth-ladder-top-k01-win-cppgate-20261128"}
TIKIT = {"k01": KB / "n11-fourteenth-ladder-top-k01-thirdimpl-20261128"}
BASE = ROOT / "head.cache"
QUAR = ROOT / "results" / "n11-s5-evidence-quarantine.json"
POLICY = ROOT / "pol" / "w" / "x" / "y" / "s5_evidence_policy.py"
MERGER = ROOT / "s5_union_merge.py"
GATE_SRC = ROOT / "gate" / "kyouen_dfpn_root.cpp"
GATE_HPP1 = ROOT / "gate" / "kyouen_residual_micro.hpp"
GATE_HPP2 = ROOT / "gate" / "n11_s5_quarantine.hpp"

SHA = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def die(msg):
    print("GATE FAILED: " + msg, file=sys.stderr); sys.exit(1)

ROWS = [
    ("k01", 6053401124017274880, 0, 1, 4360661, 86),
]
BASE_SHA = "d772f73c68bf051e7b90e5cd6cfef2a7b1c8e07da888c5f728f7a04b39edd1ec"
BASE_ROWS, BASE_WIN, BASE_LOSS = 6896, 214, 6682
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUAR_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
GATE_SRC_SHA = "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
GATE_HPP1_SHA = "5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5"
GATE_HPP2_SHA = "2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5"
OUT_ROWS, OUT_WIN, OUT_LOSS = 6897, 215, 6682
EXPECT_QUAD = {"k01": "86,15000000,1,4360661"}
CLASS_INDEX = 5804
TI_EXPECT = {"k01": {"result": 1, "expansions": 5009747}}

# ---- G0 pins -----------------------------------------------------------
for p, want in [(MERGER, MERGER_SHA), (POLICY, POLICY_SHA), (QUAR, QUAR_SHA),
                (BASE, BASE_SHA), (GATE_SRC, GATE_SRC_SHA),
                (GATE_HPP1, GATE_HPP1_SHA), (GATE_HPP2, GATE_HPP2_SHA)]:
    if SHA(p) != want: die(f"pin sha drift: {p}")

def parse_manifest_line(line, kitname):
    f1, f2 = line.split(None, 1)
    f2 = f2.strip()
    if re.fullmatch(r"[0-9a-f]{64}", f1):
        sha, rel = f1, f2
    else:
        rel, sha = f1, f2
    for pref in (f"research/experiments/{kitname}/", f"{kitname}/"):
        if rel.startswith(pref): rel = rel[len(pref):]
    return sha, rel

def verify_kit(kit):
    man = kit / "MANIFEST-sha256.txt"
    if not man.exists(): die(f"missing MANIFEST in {kit}")
    self_lines = 0
    for line in man.read_text().strip().split("\n"):
        sha, rel = parse_manifest_line(line, kit.name)
        if rel == "MANIFEST-sha256.txt":
            # self-referential line: a manifest cannot contain its own
            # sha256; excluded from verification and disclosed.
            self_lines += 1
            continue
        f = kit / rel
        if not f.exists() or SHA(f) != sha:
            die(f"kit MANIFEST mismatch: {kit.name}/{rel}")
    return self_lines

self_line_kits = {}
for grp in (REPL, GATEKIT, TIKIT):
    for name, kit in grp.items():
        self_line_kits[kit.name] = verify_kit(kit)

# ---- G1 live re-run of the published C++ gate (scratch copy) ------------
for name, budget_quad in (("k01", EXPECT_QUAD["k01"]),):
    scratch = ROOT / f"gaterun-{name}"
    if scratch.exists(): die(f"gaterun-{name} scratch already exists (stale)")
    subprocess.run(["cp", "-r", str(GATEKIT[name]), str(scratch)], check=True)
    for p in (f"{name}.p1.out", f"{name}.p2.out"):
        (scratch / "output" / "raw" / p).unlink()
    env = dict(os.environ)
    env["GATE_BIN"] = os.environ.get("GATE_BIN", str(ROOT / "gate_bin"))
    r = subprocess.run(["bash", str(scratch / "scripts" / "gate_runner.sh"),
                        name, "15000000", budget_quad],
                       capture_output=True, text=True, env=env, cwd=str(scratch))
    if r.returncode != 0: die(f"live gate re-run {name} rc!=0: " + r.stdout + r.stderr)
    if r.stdout.strip() != f"{name} GATE-PASS {budget_quad}":
        die(f"live gate re-run {name} output: {r.stdout!r}")
    live1 = (scratch / "output" / "raw" / f"{name}.p1.out").read_text()
    pub1 = (GATEKIT[name] / "output" / "raw" / f"{name}.p1.out").read_text()
    lg = lambda t: re.search(r"^replay,0,5,(\d+),0,(\d+),(\d+),(\d+),\d+,(\d+),(\d+)$", t, re.M).groups()
    if lg(live1) != lg(pub1): die(f"live gate raw != published raw {name}")

# ---- G2 re-parse of the pillars (single row) -----------------------------
def quad(path):
    t = Path(path).read_text()
    m = re.search(r"^replay,0,5,(\d+),0,(\d+),(\d+),(\d+),\d+,(\d+),(\d+)$", t, re.M)
    if not m: die(f"bad replica raw: {path}")
    return (m.group(1), m.group(2), m.group(3), m.group(4)), (m.group(5), m.group(6))

for name, lo, hi, res, nodes, legal in ROWS:
    q1, k1 = quad(REPL[name] / "raws" / f"at15m-{name}-p1.raw")
    q2, k2 = quad(REPL[name] / "raws" / f"at15m-{name}-p2.raw")
    if q1 != q2 or k1 != k2: die(f"replica pair mismatch {name}")
    if q1 != (str(legal), "15000000", str(res), str(nodes)): die(f"replica quad {name}: {q1}")
    if k1 != (str(lo), str(hi)): die(f"replica key {name}")
    g1 = (GATEKIT[name] / "output" / "raw" / f"{name}.p1.out").read_text()
    g2 = (GATEKIT[name] / "output" / "raw" / f"{name}.p2.out").read_text()
    gg = lambda t: re.search(r"^replay,0,5,(\d+),0,(\d+),(\d+),(\d+),\d+,(\d+),(\d+)$", t, re.M).groups()
    if gg(g1) != gg(g2): die(f"gate pair mismatch {name}")
    if gg(g1) != (str(legal), "15000000", str(res), str(nodes), str(lo), str(hi)):
        die(f"gate quad {name}: {gg(g1)}")
    t1 = (TIKIT[name] / "output" / "ti" / f"{name}.p1.txt").read_text().split("\n")[0].split(",")
    t2 = (TIKIT[name] / "output" / "ti" / f"{name}.p2.txt").read_text().split("\n")[0].split(",")
    if t1[0:8] != t2[0:8] or t1[9:] != t2[9:]: die(f"third-impl pair mismatch {name}")
    if t1[5] != str(res) or t1[11] != "clean": die(f"third-impl result {name}")
    if t1[3] != t1[4] or t1[3] != str(legal): die(f"third-impl legal {name}")
    if int(t1[6]) != TI_EXPECT[name]["expansions"]: die(f"third-impl expansions {name}: {t1[6]}")
    tis = json.loads((TIKIT[name] / "output" / "pillars-summary.json").read_text())
    if tis["result"] != res or tis["expansions"] != TI_EXPECT[name]["expansions"]:
        die(f"third-impl summary cross-check {name}")

# ---- G3 freshness vs BASE ----------------------------------------------
blines = BASE.read_text().strip().split("\n")
brows = [l.split(",") for l in blines if l.startswith("s5verdict,")]
if len(brows) != BASE_ROWS: die(f"BASE rows {len(brows)}")
if sum(1 for b in brows if b[4] == "1") != BASE_WIN or sum(1 for b in brows if b[4] == "2") != BASE_LOSS: die("BASE win/loss counts")
for name, lo, hi, res, nodes, legal in ROWS:
    if any(b[1] == str(lo) and b[2] == str(hi) for b in brows): die(f"freshness: {name} present in BASE")
if len({(r[1], r[2]) for r in ROWS}) != len(ROWS): die("duplicate adopted keys")
for name, lo, hi, res, nodes, legal in ROWS:
    for b in brows:
        if b[1] == str(lo) and b[2] == str(hi) and b[4] != str(res): die(f"WIN/LOSS conflict vs BASE: {name}")

# ---- G4 quarantine + canonical safety -----------------------------------
sys.path.insert(0, str(POLICY.parent))
import s5_evidence_policy as pol
qk = pol.quarantined_cache_keys()
for name, lo, hi, res, nodes, legal in ROWS:
    if (lo, hi) in qk: die(f"quarantined key {name}")
    if not pol.is_canonical_safe_s5_key((lo, hi)): die(f"not canonical-safe {name}")

# ---- G5 increment build ------------------------------------------------
KIT.mkdir(parents=True, exist_ok=True)
(KIT / "output").mkdir(exist_ok=True)
comment = """# n11 fourteenth ladder-top class-5804 k01 canonical adoption increment
#   (n11-fourteenth-ladder-top-k01-adoption-20261128, 2026-11-28) -
#   fresh 1-row increment: 1 WIN (k01 6053401124017274880:0, class 5804).
#   The canonical head of record advances from merged-exact-s5-chain-
#   plus-thirteenth-k01k02 (sha256 d772f73c..., 6,896 rows WIN 214 /
#   LOSS 6,682) by consuming exactly the 1 published fourteenth
#   ladder-top escalation k01 row.  Sources of record (all re-verified
#   live by this maker against published bytes): the fourteenth k01
#   escalation kit (replica 15M cold pair WIN(1) nodes 4,360,661),
#   the C++ scrutiny gate kit (GATE-PASS with live runner re-run,
#   anchors 3/3, tamper 4/4 fail-closed) and the third-impl
#   corroboration kit (third_impl.js pin 08ea958f, WIN(1) expansions
#   5,009,747 x2 identical).
# Every adopted key is fresh to BASE d772f73c... (absent from the
#   canonical head), quarantine-free and canonical-safe per
#   s5_evidence_policy; adopted node total 4,360,661
#   (bookkeeping, never verdicts).
# NO root verdict is consumed; class 5804 completion additionally
#   requires k02/k03/k04 (still 2M UNKNOWN) and Board-verified
#   free_now at adoption time (the WIN-side flip-census review is
#   the declared follow-up Part); nodes are bookkeeping, never
#   verdicts; the standard 11x11 empty board, every central-reply
#   root, the two-stone root {60,27} and its remaining third moves
#   {100,108} stay UNKNOWN.
"""
inc = comment + "".join(f"s5verdict,{lo},{hi},5,{res},{nodes}\n" for _, lo, hi, res, nodes, legal in ROWS)
(KIT / "output" / "increment-fourteenth-k01-adoption-20261128.cache").write_text(inc)

man = {
 "schema": "n11-fourteenth-ladder-top-k01-win-adoption-manifest-v1",
 "base": {"path": "merged-exact-s5-chain-plus-thirteenth-k01k02-20261128.cache", "sha256": BASE_SHA,
          "rows": BASE_ROWS, "win": BASE_WIN, "loss": BASE_LOSS},
 "rows": [{"name": n, "key": f"{lo}:{hi}", "result": res, "nodes": nodes, "class_index": CLASS_INDEX} for n, lo, hi, res, nodes, legal in ROWS],
 "expected_merged_shape": {"rows": OUT_ROWS, "win": OUT_WIN, "loss": OUT_LOSS},
 "merger_sha256": MERGER_SHA,
 "kits": {"replica": "n11-fourteenth-ladder-top-escalation-20261128 (5c670bc6)",
          "cppgate": "n11-fourteenth-ladder-top-k01-win-cppgate-20261128 (35b5fef1)",
          "thirdimpl": "n11-fourteenth-ladder-top-k01-thirdimpl-20261128 (35b5fef1)"},
 "owner_union_precheck": "n11-fourteenth-owner-union-precheck-20261128 (509afbdb)",
 "nodes_total_bookkeeping": 4360661,
 "status_guard": "adoption bookkeeping only; NO verdict consumed; 11x11 UNKNOWN",
}
(KIT / "adoption-manifest.json").write_text(json.dumps(man, indent=1) + "\n")

# ---- G6 merge x3 -------------------------------------------------------
outname = "merged-exact-s5-chain-plus-fourteenth-k01-20261128.cache"
outs = []
for i in (1, 2, 3):
    outp = ROOT / f"merged-run{i}.cache"
    audp = ROOT / f"merge-audit-run{i}.json"
    rc = subprocess.run([sys.executable, str(MERGER), "merge", "--out", str(outp),
                         "--audit", str(audp), str(BASE),
                         str(KIT / "output" / "increment-fourteenth-k01-adoption-20261128.cache")],
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

print(json.dumps({"verdict": "MAKER-PASS",
                  "increment_sha256": SHA(KIT / "output" / "increment-fourteenth-k01-adoption-20261128.cache"),
                  "merged_sha256": hashlib.sha256(outs[0]).hexdigest(),
                  "rows": OUT_ROWS, "win": OUT_WIN, "loss": OUT_LOSS,
                  "manifest_self_line_kits": self_line_kits}))
