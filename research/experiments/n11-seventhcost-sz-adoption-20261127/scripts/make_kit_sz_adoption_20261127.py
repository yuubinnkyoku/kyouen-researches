#!/usr/bin/env python3
"""Build the Part SZ seventh-cost 42-row canonical adoption increment,
fail-closed.

Part SZ kit n11-seventhcost-sz-adoption-20261127 (2026-11-27).  Declared
emission of the Part SZ wave A declaration
(research/log/2026-11-27-n11-seventhcost-sz-adoption-declaration.md):
the canonical head of record advances from
merged-exact-s5-chain-plus-sixthlossk38-20261126.cache (sha256
42dbb58f..., 6,832 rows WIN 201 / LOSS 6,631) by consuming exactly the
42 published seventh-cost rows (41 LOSS k01..k42 minus k05 + the single
WIN row k05 1152921504607932416:536870912).  The verdict scope of the
Part is exactly those 42 S5 rows: NO root verdict, NO 11x11 outcome,
NO class freed, NO class excluded.

Structural descendant of the published Part ST maker
make_increments_sixthloss30_adoption... (st_maker.py sha256
d4949f71...): the computation region (anchor byte gates, source-kit
MANIFEST verification, live audit re-runs, pin-vs-gate-rows
re-derivation, freshness/quarantine/policy gates, increment emit,
manifest + self-pin) is identical logic; the disclosed diff regions
are the docstring, the source pools (the published Part SW / Part SX
C++ scrutiny gate kits and the Part SY third-implementation
corroboration kit replace the sixth-cost probe kit / Part SR kit /
third-impl addendum), the WIN+LOSS direction of the adopted rows (k05
emits result=1 nodes=15763505), the emitted increment header block, the
output file names and the manifest fields.

Each adopted row is gated at three published pillars, all re-verified
here file-by-file (MANIFEST sha256) and re-run LIVE (rc=0):

1. the published Part SW C++ second-implementation scrutiny gate kit
   n11-seventhcost-41loss-cppgate-20261127 (41 LOSS rows + 3 anchors,
   145/145 files MANIFEST-verified, audit_gate.py re-run live PASS);
2. the published Part SX C++ gate kit n11-seventhcost-k05-l50m-cppgate
   -20261127 (the k05 WIN row, 24/24 files verified, audit_gate.py
   re-run live PASS);
3. the published Part SY third-implementation corroboration kit
   n11-seventhcost-thirdimpl-corroboration-20261127 (42 targets, 84
   raws, 143/143 files verified, audit_sy.py re-run live AUDIT-PASS,
   wave C third-host audit published at HEAD 36cb3ab7).

The 42 adopted (lo,hi) pairs are re-derived from the SW/SX gate-rows
expected quadruples and replica_verdict fields and cross-checked
against the SY gate-rows replica_expected_quad fields; proven absent
from BASE (fresh-increment gate), absent from the active quarantine
registry and canonical-safe per s5_evidence_policy.  The adopted-table
digest and the emitted increment sha are self-pinned.  Nodes are
bookkeeping, never verdicts; the standard 11x11 empty board, every
central-reply root, the two-stone root {60,27} and its remaining third
moves {100,108} stay UNKNOWN.

Two-run byte-identical requirement: running this maker twice must
produce byte-identical increment + manifest outputs (disclosed run
record).
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve()
KIT = SCRIPT.parents[1]
ROOT = SCRIPT.parents[4]

SW_EXP = "n11-seventhcost-41loss-cppgate-20261127"
SX_EXP = "n11-seventhcost-k05-l50m-cppgate-20261127"
SY_EXP = "n11-seventhcost-thirdimpl-corroboration-20261127"
BASE_EXP = "n11-centralreply-sixthlossk38-adoption-reaudit-20261126"
EXP = ROOT / "research/experiments"

SW_DIR = EXP / SW_EXP
SX_DIR = EXP / SX_EXP
SY_DIR = EXP / SY_EXP
BASE_CACHE = EXP / BASE_EXP / (
    "output/merged-exact-s5-chain-plus-sixthlossk38-20261126.cache")
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
POLICY = (ROOT / "research/experiments/n11-frontier-selection-20261005"
          "/scripts/s5_evidence_policy.py")
GRAPH = (ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
         "/output/dependency-graph.json.gz")
MERGER = EXP / BASE_EXP / "scripts/s5_union_merge.py"

MERGER_SHA_EXPECTED = ("907119610034fb2aebfde012550a4129dfa3b086c6de1119"
                       "4e856747ac74606a")
BASE_CACHE_SHA_EXPECTED = ("42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7b"
                           "f33e142120ff055bdc4")
BASE_CACHE_ROWS_EXPECTED = 6832
BASE_CACHE_WIN_EXPECTED = 201
BASE_CACHE_LOSS_EXPECTED = 6631
QUARANTINE_SHA_EXPECTED = ("81d231604d3a095c115135e05ca393d6be83e1aadd"
                            "e4f614d3b5a9cc67d17fe9")
POLICY_SHA_EXPECTED = ("78655e94480920de48a6fe8792e02e611513ddee7f685b"
                       "422bbb2b08af5c95e2")
GRAPH_SHA_EXPECTED = ("54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024b"
                      "bf192ec0d408c00b")

SW_MANIFEST_SHA = "09a8bca07a468a0e68899d8b27bd5d6f154dea449fd7e23b33e07b778c66a05f"
SW_FILES = 145
SW_GATEROWS_SHA = ("24c74bc289cac2d21c5b1ae8931207496e2682aa7c80a7fe199f"
                   "6bf2437e9f5a")
SX_MANIFEST_SHA = "68f91473d27edf227bb8ed8f9a95dedd866a2162d9017881058d41433e9570d0"
SX_FILES = 24
SX_GATEROWS_SHA = ("306030a78972725a4b45388e465c8b5f2dc933168c8fb07423e2"
                   "25d69b0421bc")
SY_MANIFEST_SHA = ("366771ff974b9826969cb05c4be6b3391ef0664e64ca82a51c5a"
                   "f5e6b19763e0")
SY_FILES = 143
SY_GATEROWS_SHA = ("fc8fc5c2a6532b4179a1182c85f8ed64cfffa65f207b7eed59c7"
                   "44a04e1f9a10")

DECLARED_ADOPTED = 42
ADOPTED_WIN = 1
ADOPTED_LOSS = 41
ADOPTED_NODES_TOTAL = 227552924

INCREMENT_NAME = "increment-seventhcost42-adoption-20261127.cache"
MANIFEST_NAME = "adoption-manifest.json"
SCHEMA = "seventhcost42-adoption-manifest-v1"

HDR_LINES = [
    "# n11 seventh-cost 42-row canonical adoption increment (Part SZ,",
    "#   n11-seventhcost-sz-adoption-20261127, 2026-11-27) - fresh",
    "#   42-row increment: 41 LOSS (k01..k42 minus k05) + 1 WIN (k05",
    "#   1152921504607932416:536870912).  Part SZ declares the",
    "#   seventh-cost canonical adoption: the canonical head of record",
    "#   advances from merged-exact-s5-chain-plus-sixthlossk38",
    "#   (sha256 42dbb58f..., 6,832 rows WIN 201 / LOSS 6,631) by",
    "#   consuming exactly the 42 published seventh-cost rows.",
    "# Sources of record (all re-verified live by this maker against",
    "#   published bytes): the Part SW C++ scrutiny gate kit (41 LOSS",
    "#   rows, 145/145 files, audit_gate.py live PASS), the Part SX",
    "#   C++ gate kit (k05 WIN row, 24/24 files, audit_gate.py live",
    "#   PASS), the Part SY third-implementation corroboration kit",
    "#   (42 targets, 84 raws, 143/143 files, audit_sy.py live",
    "#   AUDIT-PASS; wave C third-host audit at HEAD 36cb3ab7).",
    "# Every adopted key is fresh to BASE 42dbb58f... (absent from",
    "#   the canonical head), quarantine-free and canonical-safe per",
    "#   s5_evidence_policy; adopted node total 227,552,924",
    "#   (bookkeeping, never verdicts).",
    "# NO root verdict is consumed, NO class freed, NO class",
    "#   excluded; nodes are bookkeeping, never verdicts; the standard",
    "#   11x11 empty board, every central-reply root, the two-stone",
    "#   root {60,27} and its remaining third moves {100,108} stay",
    "#   UNKNOWN.",
]

ADOPTED_KEY_PINS = {
    "k01": (1297036692683882496, 536870912, 86, 2, 15000000, 2986255),
    "k02": (1306043891938492416, 65536, 80, 2, 15000000, 3113635),
    "k03": (1306043893012234240, 0, 87, 2, 15000000, 4803039),
    "k04": (10412357522852679680, 0, 85, 2, 15000000, 3045320),
    "k05": (1152921504607932416, 536870912, 90, 1, 50000000, 15763505),
    "k06": (1152921504608026624, 553648128, 99, 2, 15000000, 6557441),
    "k07": (1152956688980115456, 536870912, 95, 2, 15000000, 4841679),
    "k08": (1306043891938492416, 64, 90, 2, 15000000, 10134007),
    "k09": (1306043891938492416, 128, 97, 2, 15000000, 3009687),
    "k10": (1306043891938492416, 67108864, 90, 2, 15000000, 13100811),
    "k11": (1306043891938492416, 68719476736, 92, 2, 15000000, 8175719),
    "k12": (1306043891938492544, 0, 96, 2, 15000000, 6968873),
    "k13": (1306043891938500608, 0, 93, 2, 15000000, 2482316),
    "k14": (1306043891938557952, 0, 91, 2, 15000000, 3184572),
    "k15": (1306043891955269632, 0, 98, 2, 15000000, 4499006),
    "k16": (1306043892206927872, 0, 98, 2, 2000000, 1228696),
    "k17": (1306043960657969152, 0, 94, 2, 2000000, 1831284),
    "k18": (1306044991450120192, 0, 90, 2, 15000000, 2337950),
    "k19": (1306184629426847744, 0, 91, 2, 15000000, 7363042),
    "k20": (1306606841891913728, 0, 92, 2, 15000000, 2198801),
    "k21": (1378101485976420352, 0, 98, 2, 15000000, 6786255),
    "k22": (1594274268090204160, 0, 99, 2, 15000000, 7990013),
    "k23": (1882504644241915904, 0, 96, 2, 15000000, 4822824),
    "k24": (3611886901152186368, 0, 92, 2, 15000000, 2960039),
    "k25": (5917729910365880320, 0, 92, 2, 15000000, 2314036),
    "k26": (10376293541461623808, 68719476744, 93, 2, 15000000, 7170686),
    "k27": (10376328725833715712, 8, 93, 2, 15000000, 2535682),
    "k28": (10376328725833715712, 65536, 98, 2, 15000000, 3882046),
    "k29": (10376328725833715712, 131072, 92, 2, 15000000, 3329801),
    "k30": (10376328725833715712, 33554432, 91, 2, 15000000, 4837865),
    "k31": (10376328725833715712, 67108864, 98, 2, 15000000, 7435262),
    "k32": (10376328725833715712, 268435456, 97, 2, 15000000, 3831090),
    "k33": (1152921513197961216, 536870912, 103, 2, 15000000, 2739658),
    "k34": (1224979098645954560, 536870912, 102, 2, 15000000, 8150456),
    "k35": (1306043891938492416, 8, 102, 2, 15000000, 5484699),
    "k36": (1306043891938492416, 16, 101, 2, 15000000, 4856132),
    "k37": (1306043891938492416, 32, 102, 2, 15000000, 4695043),
    "k38": (1306043891938492416, 16384, 103, 2, 15000000, 6238916),
    "k39": (1306043891938492416, 16777216, 103, 2, 15000000, 10652524),
    "k40": (1306043891938492417, 0, 100, 2, 15000000, 5235489),
    "k41": (1306043891938496512, 0, 104, 2, 15000000, 10889302),
    "k42": (1306044166816399360, 0, 102, 2, 15000000, 3089468),}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sys_exit(msg: str):
    print(f"GATE FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)


def verify_manifest(kit: Path, manifest_sha: str, nfiles: int, what: str):
    m = kit / "MANIFEST-sha256.txt"
    if sha(m) != manifest_sha:
        sys_exit(f"{what} MANIFEST sha drift")
    count = 0
    for line in m.read_text().splitlines():
        parts = line.split()
        if len(parts) != 3:
            sys_exit(f"{what} MANIFEST malformed line: {line!r}")
        want_sha, want_size, rel = parts
        p = kit / rel
        if not p.is_file():
            sys_exit(f"{what} MANIFEST file missing: {rel}")
        if sha(p) != want_sha:
            sys_exit(f"{what} MANIFEST sha drift: {rel}")
        if p.stat().st_size != int(want_size):
            sys_exit(f"{what} MANIFEST size drift: {rel}")
        count += 1
    if count != nfiles:
        sys_exit(f"{what} MANIFEST file count {count} != {nfiles}")


def run_live(cmd, cwd, expect_prefix, what):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        sys_exit(f"{what} live audit rc={r.returncode}: "
                 f"{(r.stdout + r.stderr).strip()[:200]}")
    out = (r.stdout + r.stderr).strip()
    if not out.startswith(expect_prefix):
        sys_exit(f"{what} live audit output drift: {out[:120]}")
    return out


def main() -> None:
    # --- G0 anchors -------------------------------------------------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache (head of record) sha drift")
    if sha(MERGER) != MERGER_SHA_EXPECTED:
        sys_exit("pinned union merger sha drift")
    if sha(QUARANTINE) != QUARANTINE_SHA_EXPECTED:
        sys_exit("quarantine registry sha drift")
    if sha(POLICY) != POLICY_SHA_EXPECTED:
        sys_exit("evidence policy sha drift")
    if sha(GRAPH) != GRAPH_SHA_EXPECTED:
        sys_exit("frozen dependency graph sha drift")

    base_keys = {}
    wins = losss = 0
    for line in BASE_CACHE.read_text(encoding="utf-8-sig").splitlines():
        if not line or line.lstrip().startswith("#"):
            continue
        f = line.split(",")
        if len(f) != 6 or f[0] != "s5verdict":
            sys_exit(f"invalid base cache row: {line}")
        base_keys[(int(f[1]), int(f[2]))] = int(f[4])
        if int(f[4]) == 1:
            wins += 1
        elif int(f[4]) == 2:
            losss += 1
    if len(base_keys) != BASE_CACHE_ROWS_EXPECTED:
        sys_exit(f"base cache rows {len(base_keys)} != pinned")
    if (wins, losss) != (BASE_CACHE_WIN_EXPECTED, BASE_CACHE_LOSS_EXPECTED):
        sys_exit(f"base cache WIN/LOSS {wins}/{losss} != pinned")

    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    sys.path.insert(0, str(POLICY.parent))
    from s5_evidence_policy import is_canonical_safe_s5_key  # noqa: E402

    # --- G1/G2/G3 pillar kits: MANIFEST verify + live audits ---------
    verify_manifest(SW_DIR, SW_MANIFEST_SHA, SW_FILES, "SW")
    if sha(SW_DIR / "input/gate-rows.json") != SW_GATEROWS_SHA:
        sys_exit("SW gate-rows.json sha drift")
    if sha(SX_DIR / "MANIFEST-sha256.txt") != SX_MANIFEST_SHA:
        sys_exit("SX MANIFEST self-sha drift")
    verify_manifest(SX_DIR, SX_MANIFEST_SHA, SX_FILES, "SX")
    if sha(SX_DIR / "input/gate-rows.json") != SX_GATEROWS_SHA:
        sys_exit("SX gate-rows.json sha drift")
    if sha(SY_DIR / "MANIFEST-sha256.txt") != SY_MANIFEST_SHA:
        sys_exit("SY MANIFEST self-sha drift")
    verify_manifest(SY_DIR, SY_MANIFEST_SHA, SY_FILES, "SY")
    if sha(SY_DIR / "input/gate-rows.json") != SY_GATEROWS_SHA:
        sys_exit("SY gate-rows.json sha drift")

    sw_live = run_live([sys.executable, "scripts/audit_gate.py"],
                       SW_DIR, "audit_gate: PASS", "SW")
    sx_live = run_live([sys.executable, "scripts/audit_gate.py"],
                       SX_DIR, "audit_gate: PASS", "SX")
    sy_live = run_live([sys.executable, "scripts/audit_sy.py", "."],
                       SY_DIR, "AUDIT-PASS targets=42", "SY")

    # published audit records must agree
    sw_pub = json.loads((SW_DIR / "output/audit_gate.json").read_text())
    if sw_pub["overall"] != "PASS":
        sys_exit("SW published audit_gate.json overall drift")
    sx_pub = json.loads((SX_DIR / "output/audit_gate.json").read_text())
    if sx_pub["overall"] != "PASS":
        sys_exit("SX published audit_gate.json overall drift")
    sy_pub = (SY_DIR / "output/audit_sy.run1.txt").read_text()
    if not sy_pub.startswith("AUDIT-PASS targets=42"):
        sys_exit("SY published audit record drift")

    # --- G4 pin re-derivation vs published gate-rows ----------------
    sw_gr = json.loads((SW_DIR / "input/gate-rows.json").read_text())
    if sw_gr["schema"] != "n11-seventhcost-41loss-cppgate-rows-v1":
        sys_exit("SW gate-rows schema drift")
    sx_gr = json.loads((SX_DIR / "input/gate-rows.json").read_text())
    if sx_gr["schema"] != "n11-seventhcost-k05-l50m-cppgate-rows-v1":
        sys_exit("SX gate-rows schema drift")
    sy_gr = json.loads((SY_DIR / "input/gate-rows.json").read_text())
    if sy_gr["schema"] != "n11-seventhcost-thirdimpl-corroboration-rows-v1":
        sys_exit("SY gate-rows schema drift")

    if len(sw_gr["targets"]) != 41 or len(sx_gr["target"]) != 1 \
            or len(sy_gr["targets"]) != 42:
        sys_exit("pillar gate-rows target census drift")

    adopted = []
    for kid in sorted(ADOPTED_KEY_PINS):
        lo, hi, legal, verdict, budget, nodes = ADOPTED_KEY_PINS[kid]
        if kid == "k05":
            row = sx_gr["target"][kid]
        else:
            row = sw_gr["targets"][kid]
        legal_p, budget_p, res_p, nodes_p = \
            (int(x) for x in row["expected"].split(","))
        if (int(row["lo"]), int(row["hi"])) != (lo, hi):
            sys_exit(f"{kid}: gate-rows key drift")
        if (legal_p, budget_p, res_p, nodes_p) != (legal, budget, verdict,
                                                   nodes):
            sys_exit(f"{kid}: gate-rows expected quad drift")
        if row["replica_verdict"] != verdict:
            sys_exit(f"{kid}: gate-rows replica_verdict drift")
        sy_row = sy_gr["targets"][kid]
        if (int(sy_row["lo"]), int(sy_row["hi"])) != (lo, hi):
            sys_exit(f"{kid}: SY gate-rows key drift")
        if sy_row["replica_expected_quad"] != row["expected"]:
            sys_exit(f"{kid}: SY replica quad drift")
        if int(sy_row["expected_result"]) != verdict:
            sys_exit(f"{kid}: SY expected_result drift")
        adopted.append((lo, hi, verdict, nodes))

    if len(adopted) != DECLARED_ADOPTED:
        sys_exit("adopted census drift")
    wins_a = sum(1 for a in adopted if a[2] == 1)
    losss_a = sum(1 for a in adopted if a[2] == 2)
    if (wins_a, losss_a) != (ADOPTED_WIN, ADOPTED_LOSS):
        sys_exit(f"adopted WIN/LOSS {wins_a}/{losss_a} != pinned")
    if sum(a[3] for a in adopted) != ADOPTED_NODES_TOTAL:
        sys_exit("adopted node total drift")

    # --- G5 freshness / quarantine / policy -------------------------
    for lo, hi, verdict, nodes in adopted:
        key = (lo, hi)
        if key in base_keys:
            sys_exit(f"fresh-increment gate: {key} already in BASE")
        if key in quarantined:
            sys_exit(f"quarantined key {key}")
        if not is_canonical_safe_s5_key(key):
            sys_exit(f"noncanonical/unsafe key {key}")
    if len({(a[0], a[1]) for a in adopted}) != DECLARED_ADOPTED:
        sys_exit("adopted pairs must be distinct (duplicate gate)")

    # --- G6 emit increment -------------------------------------------
    out = KIT / "output"
    out.mkdir(parents=True, exist_ok=True)
    body = [f"s5verdict,{lo},{hi},5,{v},{n}"
            for lo, hi, v, n in sorted(adopted)]
    blob = ("\n".join(HDR_LINES + body) + "\n").encode("utf-8")
    incr = out / INCREMENT_NAME
    incr.write_bytes(blob)
    incr_sha = hashlib.sha256(blob).hexdigest()
    # re-read and re-verify (on-disk == emitted)
    if incr.read_bytes() != blob:
        sys_exit("on-disk increment differs from the emitted blob")
    rows = [l for l in blob.decode().splitlines()
            if l and not l.startswith("#")]
    if len(rows) != DECLARED_ADOPTED:
        sys_exit("emitted increment row census drift")

    # --- G7 manifest --------------------------------------------------
    manifest = {
        "schema": SCHEMA,
        "part": "SZ",
        "kit": "n11-seventhcost-sz-adoption-20261127",
        "declaration_log": ("research/log/2026-11-27-n11-seventhcost-"
                            "sz-adoption-declaration.md"),
        "base_head": {
            "path": str(BASE_CACHE.relative_to(ROOT)),
            "sha256": BASE_CACHE_SHA_EXPECTED,
            "rows": BASE_CACHE_ROWS_EXPECTED,
            "win": BASE_CACHE_WIN_EXPECTED,
            "loss": BASE_CACHE_LOSS_EXPECTED,
        },
        "pillars": {
            "SW": {"manifest_sha256": SW_MANIFEST_SHA, "files": SW_FILES,
                   "gate_rows_sha256": SW_GATEROWS_SHA,
                   "audit_live": sw_live},
            "SX": {"manifest_sha256": SX_MANIFEST_SHA, "files": SX_FILES,
                   "gate_rows_sha256": SX_GATEROWS_SHA,
                   "audit_live": sx_live},
            "SY": {"manifest_sha256": SY_MANIFEST_SHA, "files": SY_FILES,
                   "gate_rows_sha256": SY_GATEROWS_SHA,
                   "audit_live": sy_live},
        },
        "adopted": {
            "rows": DECLARED_ADOPTED,
            "win": ADOPTED_WIN,
            "loss": ADOPTED_LOSS,
            "nodes_total": ADOPTED_NODES_TOTAL,
            "freshness": DECLARED_ADOPTED,
            "win_loss_conflicts": 0,
            "duplicates": 0,
            "quarantined": 0,
            "noncanonical": 0,
        },
        "frozen_pins": {
            "quarantine_sha256": QUARANTINE_SHA_EXPECTED,
            "policy_sha256": POLICY_SHA_EXPECTED,
            "dependency_graph_sha256": GRAPH_SHA_EXPECTED,
            "merger_sha256": MERGER_SHA_EXPECTED,
        },
        "increment": {
            "name": INCREMENT_NAME,
            "sha256": incr_sha,
            "bytes": len(blob),
            "rows": DECLARED_ADOPTED,
            "row_format": "s5verdict,<lo>,<hi>,5,<verdict>,<nodes>",
        },
        "interpretation_guard": (
            "adoption of solver-trusted S5 cache rows only; NO root "
            "verdict consumed, NO class freed or excluded; nodes are "
            "bookkeeping, never verdicts; the standard 11x11 empty "
            "board and every central-reply root remain UNKNOWN"),
    }
    mpath = out / MANIFEST_NAME
    mpath.write_text(json.dumps(manifest, indent=1, ensure_ascii=False)
                     + "\n", encoding="utf-8")
    print(f"SZ INCREMENT PASS rows={DECLARED_ADOPTED} "
          f"WIN={ADOPTED_WIN} LOSS={ADOPTED_LOSS} "
          f"increment_sha256={incr_sha} "
          f"manifest_sha256={sha(mpath)}")


if __name__ == "__main__":
    main()
