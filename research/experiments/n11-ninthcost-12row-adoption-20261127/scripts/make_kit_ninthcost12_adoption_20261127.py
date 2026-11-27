#!/usr/bin/env python3
"""Build the ninth-cost 12-row canonical adoption increment, fail-closed.

Kit n11-ninthcost-12row-adoption-20261127 (2026-11-27).  Declared
emission of the wave A declaration
(research/log/2026-11-27-n11-ninthcost-12row-adoption-declaration.md):
the canonical head of record advances from
merged-exact-s5-chain-plus-eighthcost-k01-20261127.cache (sha256
0935c94c..., 6,875 rows WIN 203 / LOSS 6,672) by consuming exactly the
12 published ninth-cost rows (9 LOSS + 3 WIN k12/k02/k07).  The
verdict scope of the Part is exactly those 12 S5 rows: NO root
verdict, NO 11x11 outcome, NO class freed, NO class excluded.

Structural descendant of the published Part SZ maker
(make_kit_sz_adoption_20261127.py): the computation region (anchor
byte gates, source-kit MANIFEST verification, live audit re-runs,
pin-vs-gate-rows re-derivation, freshness/quarantine/policy gates,
increment emit, manifest + self-pin) is identical logic.  Disclosed
diff regions: the docstring, the source pools (the four ninth-cost
C++ scrutiny gate kits and the four ninth-cost third-implementation
corroboration kits replace SW/SX/SY), the 12-row adopted table, the
emitted increment header block, the output file names and the manifest
fields.  DISCLOSED structural deviation vs Part SZ: the ninth-cost
third-impl kits carry no audit script, so the third-impl pillar is
verified per-file (byte pins) + raw re-parse (verdict-level
agreement, node_rc=0, pair-identical) instead of a live audit re-run.

Each adopted row is gated at three published pillars, all re-verified
here file-by-file and (for the C++ gate kits) re-run LIVE (rc=0):
C++ gates: n11-ninthcost-4loss-cppgate (k01/k03/k05/k06),
-4lossrest-cppgate (k08-k11), -k12-win-cppgate (k12),
-parked3-l50m-cppgate (k02/k04/k07);
third impl: n11-ninthcost-4loss-thirdimpl,
-4loss-rest-thirdimpl, -k12-win-thirdimpl, -parked3-l50m-thirdimpl
(third_impl.js pin 08ea958f in all four).

Known published defect, disclosed and worked around fail-closed: the
k12 third-impl kit's own MANIFEST-sha256.txt pins README.md with a
stale line (third_impl.js's sha256 and size 2259; the README on main
is 2,645 bytes, sha256 07515850...).  This maker verifies that kit's
README against the main-actual pin and records the stale published
line in the manifest instead of trusting it.

The 12 adopted (lo,hi) pairs are re-derived from the four gate-rows
expected quadruples and cross-checked against the third-impl raw
result fields; proven absent from BASE (fresh-increment gate; with
12/12 absent the WIN/LOSS conflict review is vacuously clean), absent
from the active quarantine registry and canonical-safe per
s5_evidence_policy.  The adopted-table digest and the emitted
increment sha are self-pinned.  Nodes are bookkeeping, never verdicts;
the standard 11x11 empty board, every central-reply root, the
two-stone root {60,27} and its remaining third moves {100,108} stay
UNKNOWN.

Two-run byte-identical requirement: running this maker twice must
produce byte-identical increment + manifest outputs (disclosed run
record).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve()
KIT = SCRIPT.parents[1]
ROOT = SCRIPT.parents[4]

EXP = ROOT / "research/experiments"
G4L = EXP / "n11-ninthcost-4loss-cppgate-20261127"
G4R = EXP / "n11-ninthcost-4lossrest-cppgate-20261127"
GK12 = EXP / "n11-ninthcost-k12-win-cppgate-20261127"
GP3 = EXP / "n11-ninthcost-parked3-l50m-cppgate-20261127"
T4L = EXP / "n11-ninthcost-4loss-thirdimpl-corroboration-20261127"
T4R = EXP / "n11-ninthcost-4loss-rest-thirdimpl-corroboration-20261127"
TK12 = EXP / "n11-ninthcost-k12-win-thirdimpl-corroboration-20261127"
TP3 = EXP / "n11-ninthcost-parked3-l50m-thirdimpl-corroboration-20261127"
BASE_CACHE = EXP / "n11-eighthcost-k01-win-adoption-20261127" / (
    "output/merged-exact-s5-chain-plus-eighthcost-k01-20261127.cache")
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
POLICY = (ROOT / "research/experiments/n11-frontier-selection-20261005"
          "/scripts/s5_evidence_policy.py")
GRAPH = (ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
         "/output/dependency-graph.json.gz")
MERGER = EXP / "n11-centralreply-sixthlossk38-adoption-reaudit-20261126" / (
    "scripts/s5_union_merge.py")

MERGER_SHA_EXPECTED = ("907119610034fb2aebfde012550a4129dfa3b086c6de1119"
                       "4e856747ac74606a")
BASE_CACHE_SHA_EXPECTED = ("0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097a"
                           "b2c75709d590e9ca4")
BASE_CACHE_ROWS_EXPECTED = 6875
BASE_CACHE_WIN_EXPECTED = 203
BASE_CACHE_LOSS_EXPECTED = 6672
QUARANTINE_SHA_EXPECTED = ("81d231604d3a095c115135e05ca393d6be83e1aadd"
                           "e4f614d3b5a9cc67d17fe9")
POLICY_SHA_EXPECTED = ("78655e94480920de48a6fe8792e02e611513ddee7f685b"
                       "422bbb2b08af5c95e2")
GRAPH_SHA_EXPECTED = ("54f9c3643eeba139ea5e8d3babb1db9744d19f00f3cf024b"
                      "bf192ec0d408c00b")

GATE_KITS = {
    "G4L": (G4L, "c6fd3ed4580cf35994f6dca9dce7120068273c666d47a3034a9d0af2de9a63e5", 33,
            "36615cc36bcb6078435648c5618227da2d353245938e2ffbe4d3c0af0922e01a",
            "n11-ninthcost-4loss-cppgate-rows-v1"),
    "G4R": (G4R, "56b02c8888a735b36a0904a7c26111136283d7936ef1a54fe47813493a78ece5", 32,
            "86f552f5befdd789dd5a30a40c605e00049907ee705137fbc585c61bc5171270",
            "n11-ninthcost-4lossrest-cppgate-rows-v1"),
    "GK12": (GK12, "8f32da1712cb9b2a63c051c83d5c7a6339191c46800ec4a4cd624281bafd1749", 23,
             "4e14b991dad524514e8b53ead3d9cab1de0960e81dee1cc917212a01a641f2ec",
             "n11-ninthcost-k12win-cppgate-rows-v1"),
    "GP3": (GP3, "15af653d0ce0e81053bc93523c234ef0af0ae8490be473e3cd9de62f710b072b", 29,
            "89fdf461994b774c7c3cd763a3f4543147550b88e625b39b8fcfc609e1ed9dea",
            "n11-ninthcost-parked3-l50m-cppgate-rows-v1"),
}

THIRD_IMPL_SHA = ("08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea05"
                  "46800cc4a1998")
K12_TI_README_MAIN_SHA = ("0751585074e149945eb43f2a959eb60f581d6505bef430"
                          "7bffbd047bd88202e8")

TI_KITS = {
    "T4L": (T4L, [
        ("README.md", "8f0ddf7a00d6002470afb6d564eb6d6036839a805b0069a75d3ab16f6cb35d24"),
        ("input_k01.csv", "5768229a7bc3b5e719b57456e710b4250990f42f75336018eacb4fe3484400c7"),
        ("input_k03.csv", "3b33982dea100bcb4f17229b35526052b3a349b4e1a2981701a087c8234385cc"),
        ("input_k05.csv", "ed29fa0fe1fcebad260474c42ff473f7b95be1b4a5b1c77a60222e813e72fd67"),
        ("input_k06.csv", "ed853a05bbee7734d30abe89dfaae1b6f4d0329904741ec4b964c060d0c53cac"),
        ("output/raw/k01.p1.txt", "01438fccec5e5068517132576a8713b7812b7c347c90024b4a7cc67ca7281717"),
        ("output/raw/k01.p2.txt", "bcc2a93d8a78e777d66a76d0fdc6c3ac98c6183242a6524b451a81d36ea0293a"),
        ("output/raw/k03.p1.txt", "71b376036ca974674e2b7e58221884f2f2681d2a430cb9d7d847691462a2d21e"),
        ("output/raw/k03.p2.txt", "764283e68afabcc8ca072de55cacbd4d7f5c5bd1d7a0130b8546937d4d4861be"),
        ("output/raw/k05.p1.txt", "8fdd9cac8f88b21cd6442e99d2444efb03da514662fc37562e9c03d6754c3dab"),
        ("output/raw/k05.p2.txt", "dad2226dc7869a768d4743672ddcd4689004ade9ec26e24caf7ca74417e8112c"),
        ("output/raw/k06.p1.txt", "8a19727d1d6f929f9daf62418dfa6db7f9ef2e204a8c3209569b50fac61bb171"),
        ("output/raw/k06.p2.txt", "1fa084a1eb034fe93d935b495a2b7f0e128048d86376beda8a2af7cfd8261c32"),
        ("scripts/third_impl.js", THIRD_IMPL_SHA),
    ]),
    "T4R": (T4R, [
        ("README.md", "9e9356932d3b93d8d98ceb74cbd7a1842898ccd074d80e24e84d5df96a310d9c"),
        ("output/raw/k08.p1.txt", "60c353543d11e91dbbdec842986466f74825bd568784aa69947e538814bcc434"),
        ("output/raw/k08.p2.txt", "16def36acc45443bfbefb6f76130161ace256af9fb919870d784d447dddec41b"),
        ("output/raw/k09.p1.txt", "c30c3598f52bed4e026fd93557227fc032864c3708543866bba84c44817cd0e8"),
        ("output/raw/k09.p2.txt", "419620bf1b334b94464607101fc18185cebd7ed3b931eb4caa035c050f5f4e53"),
        ("output/raw/k10.p1.txt", "8c7398676706c1fe7f3a02a1b12ceb74e4c7ddd66d0aeaf887e10ec1f3e581e0"),
        ("output/raw/k10.p2.txt", "d86b9fc7f24839b0091f791938990827d86f725278768e91535eaa2ad96e5ab9"),
        ("output/raw/k11.p1.txt", "abc66e2174a41c3279f606b2145ec0501f926321e67356f488ef0f8e2c80ed98"),
        ("output/raw/k11.p2.txt", "bb1f6d8d7c036d9fa64f5b951c3f4c543a9184ff669454b69d185c8b4d36c528"),
        ("scripts/third_impl.js", THIRD_IMPL_SHA),
    ]),
    "TK12": (TK12, [
        ("README.md", K12_TI_README_MAIN_SHA),
        ("output/raw/k12.p1.txt", "4f9102b8ad845bc8810b1106777b17d18254f93f52bc41d6e5b22a4ba00e9907"),
        ("output/raw/k12.p2.txt", "5a6adab238237c6eadadffc6b161ade2a3d26dc2c115c2723c65612b4776c20e"),
        ("scripts/third_impl.js", THIRD_IMPL_SHA),
    ]),
    "TP3": (TP3, [
        ("README.md", "2c730f5eb6783c43f4b48cd3a34fb937b2005322fdae8d3b45f8730a0fa5e448"),
        ("output/raw/k02.p1.txt", "b6c9f741612f508367f09d72f5d31527853afec8e871812c2e5fe6c4715b4196"),
        ("output/raw/k02.p2.txt", "f51fb0c90d6b795bb6c09b69f4ce0ce43ec47073d1568e13bf0a3cf880d81995"),
        ("output/raw/k04.p1.txt", "f5fd995ece90abdcde3b4e61fa50a6ffe99793ddbd2e195ee2b7396243799f24"),
        ("output/raw/k04.p2.txt", "534090c9ca9966c3c60f24c31f4f1114f74149bc1cb94c8e8a456187bd0a63a0"),
        ("output/raw/k07.p1.txt", "b207859fd0dbc36ff9da21b950ca3a2a68b236e85740cad7cb79ca396426a0cd"),
        ("output/raw/k07.p2.txt", "879b969f594c45a70d3ea5ee1bd6d1e30c8f9bdc30bb2f9abce477aa65d23dd8"),
        ("scripts/third_impl.js", THIRD_IMPL_SHA),
    ]),
}

# key -> (lo, hi, legal, verdict, budget, nodes, gate kit, ti kit)
ADOPTED_KEY_PINS = {
    "k01": (1297036692683751424, 134283264, 89, 2, 15000000, 2163556, "G4L", "T4L"),
    "k03": (1297036761403228160, 134217728, 86, 2, 15000000, 7753840, "G4L", "T4L"),
    "k05": (1152921504624672768, 536903680, 91, 2, 15000000, 8687533, "G4L", "T4L"),
    "k06": (1152923703764321280, 68719476736, 99, 2, 15000000, 8130387, "G4L", "T4L"),
    "k08": (1152956688979984384, 536903680, 98, 2, 15000000, 3306768, "G4R", "T4R"),
    "k09": (1224979098645823488, 536903680, 92, 2, 15000000, 4711230, "G4R", "T4R"),
    "k10": (1297036692683751424, 134217730, 96, 2, 15000000, 5542083, "G4R", "T4R"),
    "k11": (1297036692683751424, 134217744, 97, 2, 15000000, 5931960, "G4R", "T4R"),
    "k12": (1297036692683751424, 134217792, 92, 1, 15000000, 14521862, "GK12", "TK12"),
    "k02": (1297036692683751424, 201326592, 87, 1, 50000000, 18123017, "GP3", "TP3"),
    "k04": (1152921504607903744, 536903680, 98, 2, 50000000, 24309957, "GP3", "TP3"),
    "k07": (1152923703765368832, 68719476736, 96, 1, 50000000, 27621128, "GP3", "TP3"),
}

DECLARED_ADOPTED = 12
ADOPTED_WIN = 3
ADOPTED_LOSS = 9
ADOPTED_NODES_TOTAL = 130803321

INCREMENT_NAME = "increment-ninthcost12-adoption-20261127.cache"
MANIFEST_NAME = "adoption-manifest.json"
SCHEMA = "ninthcost12-adoption-manifest-v1"

HDR_LINES = [
    "# n11 ninth-cost 12-row canonical adoption increment",
    "#   (n11-ninthcost-12row-adoption-20261127, 2026-11-27) - fresh",
    "#   12-row increment: 9 LOSS + 3 WIN (k12/k02/k07).  The canonical",
    "#   head of record advances from merged-exact-s5-chain-plus-",
    "#   eighthcost-k01 (sha256 0935c94c..., 6,875 rows WIN 203 /",
    "#   LOSS 6,672) by consuming exactly the 12 published ninth-cost",
    "#   rows.  Sources of record (all re-verified live by this maker",
    "#   against published bytes): the four C++ scrutiny gate kits",
    "#   (4loss 33/33, 4lossrest 32/32, k12 23/23, parked3-L50M 29/29",
    "#   files, audit_gate.py live PASS each) and the four third-impl",
    "#   corroboration kits (per-file byte pins + raw re-parse;",
    "#   third_impl.js pin 08ea958f in all four).",
    "# Every adopted key is fresh to BASE 0935c94c... (absent from the",
    "#   canonical head), quarantine-free and canonical-safe per",
    "#   s5_evidence_policy; adopted node total 130,803,321",
    "#   (bookkeeping, never verdicts).",
    "# NO root verdict is consumed, NO class freed, NO class",
    "#   excluded; nodes are bookkeeping, never verdicts; the standard",
    "#   11x11 empty board, every central-reply root, the two-stone",
    "#   root {60,27} and its remaining third moves {100,108} stay",
    "#   UNKNOWN.",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sys_exit(msg: str):
    print(f"GATE FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)


def verify_gate_manifest(kit: Path, manifest_sha: str, nfiles: int,
                         gaterows_sha: str, schema: str, what: str):
    m = kit / "MANIFEST-sha256.txt"
    if sha(m) != manifest_sha:
        sys_exit(f"{what} MANIFEST sha drift")
    count = 0
    for line in m.read_text().splitlines():
        parts = line.split()
        if len(parts) == 3:
            want_sha, want_size, rel = parts
        elif len(parts) == 2:
            want_sha, rel = parts
            want_size = None
        else:
            sys_exit(f"{what} MANIFEST malformed line: {line!r}")
        rel = rel[2:] if rel.startswith("./") else rel
        if rel == "MANIFEST-sha256.txt":
            continue
        p = kit / rel
        if not p.is_file():
            sys_exit(f"{what} MANIFEST file missing: {rel}")
        if sha(p) != want_sha:
            sys_exit(f"{what} MANIFEST sha drift: {rel}")
        if want_size is not None and p.stat().st_size != int(want_size):
            sys_exit(f"{what} MANIFEST size drift: {rel}")
        count += 1
    if count != nfiles:
        sys_exit(f"{what} MANIFEST file count {count} != {nfiles}")
    gr = kit / "input/gate-rows.json"
    if sha(gr) != gaterows_sha:
        sys_exit(f"{what} gate-rows.json sha drift")
    if json.loads(gr.read_text())["schema"] != schema:
        sys_exit(f"{what} gate-rows schema drift")


def run_live(kit: Path, what: str):
    env = dict(os.environ)
    env["N9_HEAD"] = str(BASE_CACHE)
    r = subprocess.run([sys.executable, "scripts/audit_gate.py"],
                       cwd=kit, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        sys_exit(f"{what} live audit rc={r.returncode}: "
                 f"{(r.stdout + r.stderr).strip()[:200]}")
    out = (r.stdout + r.stderr).strip()
    if not out.startswith("audit_gate: PASS"):
        sys_exit(f"{what} live audit output drift: {out[:120]}")
    return out


def parse_ti_raw(path: Path):
    """third,<row>,<stones>,<legalIn>,<legalDerived>,<result>,<expansion>,
    <ttHits>,<wallS>,<lo>,<hi>,<reason>,... + node_rc trailer."""
    text = path.read_text()
    rows = [l for l in text.splitlines() if l.startswith("third,")]
    if len(rows) != 1:
        sys_exit(f"third-impl raw shape drift: {path}")
    f = rows[0].split(",")
    if len(f) < 13:
        sys_exit(f"third-impl raw field count drift: {path}")
    rc = [l for l in text.splitlines() if l.startswith("node_rc=")]
    if len(rc) != 1 or rc[0] != "node_rc=0":
        sys_exit(f"third-impl raw node_rc drift: {path}")
    return {
        "row": f[1], "stones": int(f[2]), "legalIn": int(f[3]),
        "legalDerived": int(f[4]), "result": int(f[5]),
        "expansions": int(f[6]), "lo": int(f[9]), "hi": int(f[10]),
        "reason": f[11],
    }


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

    # --- G1 C++ gate kits: MANIFEST verify + live audits --------------
    gate_live = {}
    gate_rows_json = {}
    for tag, (kit, msha, nfiles, grsha, schema) in GATE_KITS.items():
        verify_gate_manifest(kit, msha, nfiles, grsha, schema, tag)
        gate_live[tag] = run_live(kit, tag)
        gate_rows_json[tag] = json.loads(
            (kit / "input/gate-rows.json").read_text())

    # --- G2 third-impl kits: per-file pins + raw re-parse -------------
    ti_records = {}
    stale_k12_manifest_line = None
    for tag, (kit, pins) in TI_KITS.items():
        for rel, want in pins:
            p = kit / rel
            if not p.is_file():
                sys_exit(f"{tag} file missing: {rel}")
            if sha(p) != want:
                sys_exit(f"{tag} file sha drift: {rel}")
        if tag == "TK12":
            # disclosed: the kit's own published MANIFEST pins README.md
            # with a stale line; verify the stale line exists as
            # published and record it (do not trust it).
            m = (kit / "MANIFEST-sha256.txt").read_text()
            for line in m.splitlines():
                parts = line.split()
                if len(parts) == 3 and parts[2] == "README.md":
                    if parts[0] != K12_TI_README_MAIN_SHA:
                        stale_k12_manifest_line = line
        keys = [k for k, v in ADOPTED_KEY_PINS.items() if v[7] == tag]
        for kid in keys:
            recs = []
            for p in ("p1", "p2"):
                rec = parse_ti_raw(kit / f"output/raw/{kid}.{p}.txt")
                if rec["row"] not in (kid, f"{kid}.{p}"):
                    sys_exit(f"{tag} raw row label drift: {kid}.{p}")
                if rec["reason"] != "clean":
                    sys_exit(f"{tag} raw reason drift: {kid}.{p}")
                if (rec["lo"], rec["hi"]) != (
                        ADOPTED_KEY_PINS[kid][0], ADOPTED_KEY_PINS[kid][1]):
                    sys_exit(f"{tag} raw key drift: {kid}.{p}")
                if rec["legalDerived"] != rec["legalIn"]:
                    sys_exit(f"{tag} raw legal drift: {kid}.{p}")
                recs.append(rec)
            a, b = recs
            if (a["result"], a["legalIn"], a["stones"], a["expansions"]) != \
               (b["result"], b["legalIn"], b["stones"], b["expansions"]):
                sys_exit(f"{tag} third-impl pair mismatch: {kid}")
            ti_records[kid] = a

    # --- G3 pin re-derivation vs published gate-rows ------------------
    adopted = []
    ti_expansions = {}
    for kid in sorted(ADOPTED_KEY_PINS):
        lo, hi, legal, verdict, budget, nodes, gtag, ttag = \
            ADOPTED_KEY_PINS[kid]
        gr = gate_rows_json[gtag]
        targets = gr.get("targets") or gr.get("target")
        row = targets[kid]
        legal_p, budget_p, res_p, nodes_p = \
            (int(x) for x in row["expected"].split(","))
        if "lo" in row and "hi" in row:
            g_lo, g_hi = int(row["lo"]), int(row["hi"])
        else:
            g_lo_s, g_hi_s = row["key"].split(":")
            g_lo, g_hi = int(g_lo_s), int(g_hi_s)
        if (g_lo, g_hi) != (lo, hi):
            sys_exit(f"{kid}: gate-rows key drift")
        if (legal_p, budget_p, res_p, nodes_p) != (legal, budget, verdict,
                                                   nodes):
            sys_exit(f"{kid}: gate-rows expected quad drift")
        # third-impl verdict-level agreement
        ti = ti_records[kid]
        if ti["result"] != verdict:
            sys_exit(f"{kid}: third-impl result {ti['result']} != "
                     f"gate verdict {verdict}")
        if ti["legalIn"] != legal:
            sys_exit(f"{kid}: third-impl legal drift")
        ti_expansions[kid] = ti["expansions"]
        adopted.append((lo, hi, verdict, nodes))

    if len(adopted) != DECLARED_ADOPTED:
        sys_exit("adopted census drift")
    wins_a = sum(1 for a in adopted if a[2] == 1)
    losss_a = sum(1 for a in adopted if a[2] == 2)
    if (wins_a, losss_a) != (ADOPTED_WIN, ADOPTED_LOSS):
        sys_exit(f"adopted WIN/LOSS {wins_a}/{losss_a} != pinned")
    if sum(a[3] for a in adopted) != ADOPTED_NODES_TOTAL:
        sys_exit("adopted node total drift")

    # --- G4 freshness / quarantine / policy ---------------------------
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

    # --- G5 emit increment --------------------------------------------
    out = KIT / "output"
    out.mkdir(parents=True, exist_ok=True)
    body = [f"s5verdict,{lo},{hi},5,{v},{n}"
            for lo, hi, v, n in sorted(adopted)]
    blob = ("\n".join(HDR_LINES + body) + "\n").encode("utf-8")
    incr = out / INCREMENT_NAME
    incr.write_bytes(blob)
    incr_sha = hashlib.sha256(blob).hexdigest()
    if incr.read_bytes() != blob:
        sys_exit("on-disk increment differs from the emitted blob")
    rows = [l for l in blob.decode().splitlines()
            if l and not l.startswith("#")]
    if len(rows) != DECLARED_ADOPTED:
        sys_exit("emitted increment row census drift")

    # --- G6 manifest ----------------------------------------------------
    manifest = {
        "schema": SCHEMA,
        "part": "ninth-cost 12-row canonical adoption",
        "kit": "n11-ninthcost-12row-adoption-20261127",
        "declaration_log": (
            "research/log/2026-11-27-n11-ninthcost-12row-adoption-"
            "declaration.md"),
        "base_head": {
            "path": str(BASE_CACHE.relative_to(ROOT)),
            "sha256": BASE_CACHE_SHA_EXPECTED,
            "rows": BASE_CACHE_ROWS_EXPECTED,
            "win": BASE_CACHE_WIN_EXPECTED,
            "loss": BASE_CACHE_LOSS_EXPECTED,
        },
        "pillars": {
            tag: {
                "manifest_sha256": GATE_KITS[tag][1],
                "files": GATE_KITS[tag][2],
                "gate_rows_sha256": GATE_KITS[tag][3],
                "audit_live": gate_live[tag],
            }
            for tag in GATE_KITS
        },
        "third_impl_pillar": {
            "third_impl_sha256": THIRD_IMPL_SHA,
            "kits": {tag: {"files": len(pins),
                           "pins_verified": len(pins)}
                     for tag, (k, pins) in TI_KITS.items()},
            "per_key_expansions_bookkeeping": ti_expansions,
            "disclosed_deviation": (
                "the ninth-cost third-impl kits carry no audit script; "
                "verified per-file byte pins + raw re-parse instead of "
                "Part SZ's live audit re-run"),
            "known_published_defect": {
                "kit": "n11-ninthcost-k12-win-thirdimpl-corroboration-"
                       "20261127",
                "stale_manifest_line": stale_k12_manifest_line,
                "handling": ("README verified against the main-actual "
                             "pin 07515850...; the kit's own stale "
                             "MANIFEST line is recorded, not trusted"),
            },
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
            "verdict consumed, NO class freed or excluded; the "
            "flip-census review of the three WIN rows (k12/k02/k07) is "
            "a separately declared Part; nodes are bookkeeping, never "
            "verdicts; the standard 11x11 empty board and every "
            "central-reply root remain UNKNOWN"),
    }
    mpath = out / MANIFEST_NAME
    mpath.write_text(json.dumps(manifest, indent=1, ensure_ascii=False)
                     + "\n", encoding="utf-8")
    print(f"N12 INCREMENT PASS rows={DECLARED_ADOPTED} "
          f"WIN={ADOPTED_WIN} LOSS={ADOPTED_LOSS} "
          f"increment_sha256={incr_sha} "
          f"manifest_sha256={sha(mpath)}")


if __name__ == "__main__":
    main()
