#!/usr/bin/env python3
"""make_adoption.py -- fresh maker for the n11 ultra-cheap u03 canonical
adoption kit (2026-11-27).

Machine-derived structural descendant of the published ultra-cheap u02
adoption maker (research/experiments/n11-ultra-cheap-u02-win-adoption-20261127
/scripts/make_adoption.py): the single adopted row, all kit paths, all pinned
shas, the head basis (82b52577), the pre-registered merged shape (6,893 rows
WIN 211 / LOSS 6,682) and the comment blocks are re-derived for this Part.
Because this lane's pillar kit combines the C++ gate and the
third-implementation raws (and ships the runner instead of a separate
audit script), the live pillar re-check is a LIVE re-run of the published
gate_runner.sh on a scratch copy of the pillar kit (2 fresh-cold C++
passes, node-exact vs the published raws), with the gate source/headers
sha-pinned and the binary provenance disclosed.

Fail-closed: every gate aborts before any output is written.
Verdicts are NOT consumed here.  11x11 stays UNKNOWN.
"""
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE
KIT = ROOT / "kitout" / "research" / "experiments" / "n11-ultra-cheap-u03-win-adoption-20261127"
REPL = ROOT / "kitbuild" / "research" / "experiments" / "n11-ultra-cheap-u03-escalation-15m-20261127"
PILLAR = ROOT / "kitbuild" / "research" / "experiments" / "n11-ultra-cheap-u03-win-pillars-20261127"
BASE = ROOT / "head.cache"
QUAR = ROOT / "results" / "n11-s5-evidence-quarantine.json"
POLICY = ROOT / "a" / "b" / "c" / "d" / "s5_evidence_policy.py"
MERGER = ROOT / "s5_union_merge.py"
GATE_SRC = ROOT / "gate" / "kyouen_dfpn_root.cpp"
GATE_HPP1 = ROOT / "gate" / "kyouen_residual_micro.hpp"
GATE_HPP2 = ROOT / "gate" / "n11_s5_quarantine.hpp"

SHA = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def die(msg):
    print("GATE FAILED: " + msg, file=sys.stderr); sys.exit(1)

ROWS = [
    ("u03", 1153202979851993088, 272, 1, 2909040, 78),
]
BASE_SHA = "82b525777843ecb44c3857b034f7a135284c2587b42dbaa94aa295b01adc7509"
BASE_ROWS, BASE_WIN, BASE_LOSS = 6892, 210, 6682
MERGER_SHA = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
POLICY_SHA = "78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2"
QUAR_SHA = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"
GATE_SRC_SHA = "9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e"
GATE_HPP1_SHA = "5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5"
GATE_HPP2_SHA = "2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5"
OUT_ROWS, OUT_WIN, OUT_LOSS = 6893, 211, 6682
EXPECT_QUAD = "78,15000000,1,2909040"
CLASS_INDEX = 16371

# ---- G0 pins -----------------------------------------------------------
for p, want in [(MERGER, MERGER_SHA), (POLICY, POLICY_SHA), (QUAR, QUAR_SHA),
                (BASE, BASE_SHA), (GATE_SRC, GATE_SRC_SHA),
                (GATE_HPP1, GATE_HPP1_SHA), (GATE_HPP2, GATE_HPP2_SHA)]:
    if SHA(p) != want: die(f"pin sha drift: {p}")
# published kit MANIFEST self-verification
for kit in (REPL, PILLAR):
    man = kit / "MANIFEST-sha256.txt"
    if not man.exists(): die(f"missing MANIFEST in {kit}")
    for line in man.read_text().strip().split("\n"):
        sha, path = line.split()
        f = kit / path
        if not f.exists() or SHA(f) != sha: die(f"kit MANIFEST mismatch: {kit.name}/{path}")

# ---- G1 live re-run of the published C++ gate (runner, scratch copy) ---
scratch = ROOT / "gaterun"
if scratch.exists():
    die("gaterun scratch already exists (stale)")
subprocess.run(["cp", "-r", str(PILLAR), str(scratch)], check=True)
for p in ("u03.p1.out", "u03.p2.out"):
    (scratch / "output" / "raw" / p).unlink()
env = dict(os.environ)
env["GATE_BIN"] = os.environ.get("GATE_BIN", str(ROOT / "gate_bin"))
r = subprocess.run(["bash", str(scratch / "scripts" / "gate_runner.sh"),
                    "u03", "15000000", EXPECT_QUAD],
                   capture_output=True, text=True, env=env, cwd=str(scratch))
if r.returncode != 0: die("live gate re-run rc!=0: " + r.stdout + r.stderr)
if r.stdout.strip() != f"u03 GATE-PASS {EXPECT_QUAD}":
    die(f"live gate re-run output: {r.stdout!r}")
live1 = (scratch / "output" / "raw" / "u03.p1.out").read_text()
pub1 = (PILLAR / "output" / "raw" / "u03.p1.out").read_text()
lg = lambda t: re.search(r"^replay,0,5,(\d+),0,(\d+),(\d+),(\d+),\d+,(\d+),(\d+)$", t, re.M).groups()
if lg(live1) != lg(pub1): die("live gate raw != published raw")

# ---- G2 re-parse of the three pillars ----------------------------------
def quad(path):
    t = Path(path).read_text()
    m = re.search(r"^replay,0,5,(\d+),0,(\d+),(\d+),(\d+),\d+,(\d+),(\d+)$", t, re.M)
    if not m: die(f"bad replica raw: {path}")
    return (m.group(1), m.group(2), m.group(3), m.group(4)), (m.group(5), m.group(6))

for name, lo, hi, res, nodes, legal in ROWS:
    q1, k1 = quad(REPL / "raws" / f"at15m-{name}-p1.raw")
    q2, k2 = quad(REPL / "raws" / f"at15m-{name}-p2.raw")
    if q1 != q2 or k1 != k2: die(f"replica pair mismatch {name}")
    if q1 != (str(legal), "15000000", str(res), str(nodes)): die(f"replica quad {name}: {q1}")
    if k1 != (str(lo), str(hi)): die(f"replica key {name}")
    g1 = (PILLAR / "output" / "raw" / f"{name}.p1.out").read_text()
    g2 = (PILLAR / "output" / "raw" / f"{name}.p2.out").read_text()
    gg = lambda t: re.search(r"^replay,0,5,(\d+),0,(\d+),(\d+),(\d+),\d+,(\d+),(\d+)$", t, re.M).groups()
    if gg(g1) != gg(g2): die(f"gate pair mismatch {name}")
    if gg(g1) != (str(legal), "15000000", str(res), str(nodes), str(lo), str(hi)):
        die(f"gate quad {name}: {gg(g1)}")
    t1 = (PILLAR / "output" / "ti" / f"{name}.p1.txt").read_text().split("\n")[0].split(",")
    t2 = (PILLAR / "output" / "ti" / f"{name}.p2.txt").read_text().split("\n")[0].split(",")
    if t1[0:8] != t2[0:8] or t1[9:] != t2[9:]: die(f"third-impl pair mismatch {name}")
    if t1[5] != str(res) or t1[11] != "clean": die(f"third-impl result {name}")
    if t1[3] != t1[4] or t1[3] != str(legal): die(f"third-impl legal {name}")

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
comment = """# n11 ultra-cheap u03 canonical adoption increment
#   (n11-ultra-cheap-u03-win-adoption-20261127, 2026-11-27) - fresh
#   1-row increment: 1 WIN (u03 1153202979851993088:272, class 16371).
#   The canonical head of record advances from merged-exact-s5-chain-
#   plus-ultra-cheap-u02 (sha256 82b52577..., 6,892 rows WIN 210 /
#   LOSS 6,682) by consuming exactly the 1 published ultra-cheap u03
#   escalation row.  Sources of record (all re-verified live by this
#   maker against published bytes): the ultra-cheap u03 escalation kit
#   (replica 15M cold pair WIN(1) nodes 2,909,040), the pillars kit
#   (C++ scrutiny gate 4/4 GATE-PASS with a live runner re-run,
#   third_impl.js pin 08ea958f corroboration WIN(1) x2).
# Every adopted key is fresh to BASE 82b52577... (absent from the
#   canonical head), quarantine-free and canonical-safe per
#   s5_evidence_policy; adopted node total 2,909,040
#   (bookkeeping, never verdicts).
# NO root verdict is consumed, NO class freed, NO class
#   excluded; nodes are bookkeeping, never verdicts; the standard
#   11x11 empty board, every central-reply root, the two-stone
#   root {60,27} and its remaining third moves {100,108} stay
#   UNKNOWN.
"""
inc = comment + "".join(f"s5verdict,{lo},{hi},5,{res},{nodes}\n" for _, lo, hi, res, nodes, legal in ROWS)
(KIT / "output" / "increment-ultra-cheap-u03-adoption-20261127.cache").write_text(inc)

man = {
 "schema": "n11-ultra-cheap-u03-win-adoption-manifest-v1",
 "base": {"path": "merged-exact-s5-chain-plus-ultra-cheap-u02-20261127.cache", "sha256": BASE_SHA,
          "rows": BASE_ROWS, "win": BASE_WIN, "loss": BASE_LOSS},
 "rows": [{"name": n, "key": f"{lo}:{hi}", "result": res, "nodes": nodes, "class_index": CLASS_INDEX} for n, lo, hi, res, nodes, legal in ROWS],
 "expected_merged_shape": {"rows": OUT_ROWS, "win": OUT_WIN, "loss": OUT_LOSS},
 "merger_sha256": MERGER_SHA,
 "kits": {"replica": "n11-ultra-cheap-u03-escalation-15m-20261127 (36f0cd2c)",
          "pillars": "n11-ultra-cheap-u03-win-pillars-20261127 (d6577e97)"},
 "nodes_total_bookkeeping": 2909040,
 "status_guard": "adoption bookkeeping only; NO verdict consumed; 11x11 UNKNOWN",
}
(KIT / "adoption-manifest.json").write_text(json.dumps(man, indent=1) + "\n")

# ---- G6 merge x3 -------------------------------------------------------
outname = "merged-exact-s5-chain-plus-ultra-cheap-u03-20261127.cache"
outs = []
for i in (1, 2, 3):
    outp = ROOT / f"merged-run{i}.cache"
    audp = ROOT / f"merge-audit-run{i}.json"
    rc = subprocess.run([sys.executable, str(MERGER), "merge", "--out", str(outp),
                         "--audit", str(audp), str(BASE),
                         str(KIT / "output" / "increment-ultra-cheap-u03-adoption-20261127.cache")],
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

print(json.dumps({"verdict": "MAKER-PASS", "increment_sha256": SHA(KIT / "output" / "increment-ultra-cheap-u03-adoption-20261127.cache"),
                  "merged_sha256": hashlib.sha256(outs[0]).hexdigest(),
                  "rows": OUT_ROWS, "win": OUT_WIN, "loss": OUT_LOSS}))
