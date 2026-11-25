#!/usr/bin/env python3
"""Build the batch-29 (class 2251) 37-LOSS canonical-adoption increment, fail-closed.

Prepared for the Part DA adoption: the published batch-29 cumulative evidence
is byte-pinned through the published single batch-29 kit (Part CI scaffold +
takeover drives; kit MANIFEST 7c124233..., 71 files: README 1 + input 55
(54 per-key input csv + batch-keys.json) + scripts 3 + val-gate 12) plus the
8 follow-up published post-scaffold val-gate host files (4 takeover-host by
commit 8b75b786 + 4 d2-host by the drive-2 checkpoints) plus the published
outputs (108 pass raws ab001..ab054 x p1/p2 and status.log, 55 lines).  The
kit files are sha256-verified here file-by-file.

The batch is FULLY probed at probe level: all 54 of 54 keys are probed
2-pass fresh-cold at budget 15M.  53 keys are resolved LOSS; 1 key (ab028)
is a probe-level WIN (result 1, nodes 3,167,121) that stays UNCONSUMED:
it is NOT adopted here, NOT emitted into any increment, and NOT written
into any canonical cache (WIN-row adoption is the separate scrutiny-owner
C++ second-implementation lane, pin 9193f5b6...).  The adopted packet is
the 37 fresh LOSS rows ab017..ab054 except ab028; the 16 keys ab001..ab016
were already adopted canonically by Part CU (already_adopted; asserted
present in the BASE cache with verdict 2 and the node counts of the CU
increment).  No EXHAUSTED row and no fragment row exists in this batch.

Emits the CANONICAL-ADOPTION increment cache over the published raw replay
rows of the resolved fresh LOSS set only:

  * batch-29 (class 2251): the 37 fresh LOSS rows
    ab017..ab054 except ab028 (total nodes per pass 159,325,566)

The adoption base is the canonical exact-S5 verdict cache BASE = the Part CU
merged 6,317-row cache sha256 30ddad9d... (the closure chain through the
Part CU batch-29 16-LOSS adoption), byte-pinned here; this maker ABORTS
against anything else.  Every adopted key is asserted fresh (absent from
BASE) and absent from the quarantine registry.  The unconsumed WIN key
ab028 is likewise asserted absent from BASE (its verdict is consumed nowhere).

Fail-closed gates: kit MANIFEST sha-verified file-by-file (71 files); the
8 post-scaffold val-gate host files sha-verified and their (result, nodes)
asserted node-exact against the published baselines on all four hosts
(published-baseline / batch29-host / takeover-host / d2-host; wall_s
excluded); every adopted row must come from BOTH published raw passes with
identical (stones, legal, is_or, budget, result, nodes, lo, hi) and a
completed "# replay_done" line on both passes; the unconsumed WIN row
ab028 must be two-pass node-exact with the pinned WIN pin; legal and
(lo,hi) must match the published batch-keys.json for every probed key; the
status.log (sha-pinned; 55 lines) must reproduce the CU-pinned drive-1
16-line prefix byte-exactly (append-only chain gate, 6b877344...), carry
exactly one PASS row per probed key with (budget, result, nodes) agreement,
exactly one WIN-HALT row (ab028, pinned), no EXHAUSTED rows, no
truncated-retry rows, no junk rows, no EXECUTION-COMPLETE record; the raw
set must be exactly ab001..ab054 x {p1,p2} (108 files; no sidecars, no
fragments); the 37 adopted keys are distinct, ABSENT from the canonical
BASE cache and from the quarantine registry while the 16 CU keys are
PRESENT in BASE as LOSS with the CU nodes (chain continuity gate);
adopted-row node totals must agree on both passes (159,325,566); the raw
LOSS set over the fresh keys must be exactly the 37 adopted candidates and
the only non-LOSS raw of the batch is the pinned ab028 WIN row.  Verdicts
are byte-taken from the raws.  The 37 LOSS rows ARE the only thing
consumed into the canonical cache by this Part; 11x11 stays UNKNOWN;
nodes are bookkeeping, never verdicts; class 2251 is NOT freed here (the
unconsumed WIN child ab028 remains, verdict-unconsumed).
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OUT = EXP / "output"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class2251-loss16-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-20261123.cache"
B29_DIR = ROOT / "research/experiments/n11-centralreply-closure-class2251-batch29-20261123"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

B29_KEYS_SHA_EXPECTED = "330c0b9f3166e9f6e21b739a851a881d800ab9f58a14dccaa0c772118dee716c"
B29_MANIFEST_SHA_EXPECTED = "7c12423364a292844d4b49a048e910a4be3f9b45cc08a4b31d0bd35233caab84"
B29_KIT_FILES_EXPECTED = 71
B29_STATUS_SHA_EXPECTED = "b49322d9ed8cd63e9bba20e10acd52b89849b408d19496931d5545b5ec99a6a0"
B29_STATUS_DRIVE1_PREFIX_SHA = "6b877344b9abea348a9b221f587a771857d3c4091f88fa460ef12595722183e2"
BASE_CACHE_SHA_EXPECTED = "30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4"
BASE_CACHE_ROWS_EXPECTED = 6317
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"

# post-scaffold published val-gate host files (takeover-host added by commit
# 8b75b786, d2-host added by the drive-2 checkpoints) - pinned independently
HOST_PIN = {
    "at2m-s5-1152921504606851072-536870946.d2-host.out":
        "ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22",
    "at2m-s5-1152921504606851072-536870946.takeover-host.out":
        "ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22",
    "at2m-s5-1188950301626860544-536870912.d2-host.out":
        "eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24",
    "at2m-s5-1188950301626860544-536870912.takeover-host.out":
        "eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24",
    "first-15m-s5-1152921504606851072-536870946.d2-host.out":
        "8675ae4b4904485d5ffde72578342d69668a5c8bd39b82d93193177f515ebafb",
    "first-15m-s5-1152921504606851072-536870946.takeover-host.out":
        "8675ae4b4904485d5ffde72578342d69668a5c8bd39b82d93193177f515ebafb",
    "second-15m-s5-1188950301626860544-536870912.d2-host.out":
        "45cb1348c0a805ddff4b7d7a9db39cf56cd91f0669dae8f385f0ee7c33d2e4e2",
    "second-15m-s5-1188950301626860544-536870912.takeover-host.out":
        "7fd4454283b2b6d62f7381a239b97b3eba63830a72d870107622e936157c43ed",
}
VAL_GATE_EXPECT = {
    "at2m-s5-1152921504606851072-536870946": (0, 2000000),
    "at2m-s5-1188950301626860544-536870912": (0, 2000000),
    "first-15m-s5-1152921504606851072-536870946": (2, 3651923),
    "second-15m-s5-1188950301626860544-536870912": (2, 5040200),
}

BUDGET = 15000000

ADOPTED_LOSS_IDS = ['ab017', 'ab018', 'ab019', 'ab020', 'ab021', 'ab022', 'ab023', 'ab024', 'ab025', 'ab026', 'ab027', 'ab029', 'ab030', 'ab031', 'ab032', 'ab033', 'ab034', 'ab035', 'ab036', 'ab037', 'ab038', 'ab039', 'ab040', 'ab041', 'ab042', 'ab043', 'ab044', 'ab045', 'ab046', 'ab047', 'ab048', 'ab049', 'ab050', 'ab051', 'ab052', 'ab053', 'ab054']
ADOPTED_NODES = {
    "ab017": 3366331,
    "ab018": 6998686,
    "ab019": 2623573,
    "ab020": 3020397,
    "ab021": 3748592,
    "ab022": 4620753,
    "ab023": 8695465,
    "ab024": 4131850,
    "ab025": 3832650,
    "ab026": 1835150,
    "ab027": 4364868,
    "ab029": 2583183,
    "ab030": 7694235,
    "ab031": 2973520,
    "ab032": 3320290,
    "ab033": 5737514,
    "ab034": 2421190,
    "ab035": 3712073,
    "ab036": 5512708,
    "ab037": 3582387,
    "ab038": 7949979,
    "ab039": 3343978,
    "ab040": 3796441,
    "ab041": 4746725,
    "ab042": 1926643,
    "ab043": 3003611,
    "ab044": 4719146,
    "ab045": 3978891,
    "ab046": 4979936,
    "ab047": 5604561,
    "ab048": 3457154,
    "ab049": 4332757,
    "ab050": 4127068,
    "ab051": 6906311,
    "ab052": 5830122,
    "ab053": 2832769,
    "ab054": 3014059,
}
ADOPTED_TOTAL_NODES = 159325566
ADOPTED_S5 = {
    "ab017": 78838,
    "ab018": 84223,
    "ab019": 86005,
    "ab020": 87025,
    "ab021": 89372,
    "ab022": 91588,
    "ab023": 93761,
    "ab024": 93811,
    "ab025": 93812,
    "ab026": 93813,
    "ab027": 93814,
    "ab029": 93816,
    "ab030": 93817,
    "ab031": 93818,
    "ab032": 93819,
    "ab033": 93820,
    "ab034": 93821,
    "ab035": 93822,
    "ab036": 93823,
    "ab037": 93824,
    "ab038": 93825,
    "ab039": 93826,
    "ab040": 93827,
    "ab041": 93828,
    "ab042": 93829,
    "ab043": 93830,
    "ab044": 93831,
    "ab045": 93832,
    "ab046": 93833,
    "ab047": 93834,
    "ab048": 93835,
    "ab049": 93836,
    "ab050": 93837,
    "ab051": 93838,
    "ab052": 93839,
    "ab053": 93840,
    "ab054": 93841,
}
ADOPTED_KEYS = {
    "ab017": (1155314076402843648, 0),
    "ab018": (1299429230118961152, 0),
    "ab019": (1155314316921012224, 0),
    "ab020": (1155331634229149696, 0),
    "ab021": (1155349226415194112, 0),
    "ab022": (1155384410787282944, 0),
    "ab023": (1155876991996526592, 0),
    "ab024": (1155314042043105280, 32),
    "ab025": (1155314042043105280, 64),
    "ab026": (5908722848549044224, 131072),
    "ab027": (1297036830121656832, 131072),
    "ab029": (1155314042043105280, 16),
    "ab030": (1191342839062069248, 0),
    "ab031": (1227371636081033216, 0),
    "ab032": (1443544418194817024, 0),
    "ab033": (1155314042043105280, 4),
    "ab034": (1155314042043105280, 16384),
    "ab035": (1155314042043105280, 32768),
    "ab036": (1297036830121656320, 131073),
    "ab037": (1297036830121657344, 131072),
    "ab038": (1297036830121656576, 131072),
    "ab039": (1155314042043105280, 65536),
    "ab040": (1297045626214678528, 131072),
    "ab041": (1315051228631138304, 131072),
    "ab042": (1155314042043105280, 131072),
    "ab043": (1155314042043105280, 8),
    "ab044": (1297036831195398144, 131072),
    "ab045": (1297039029144911872, 131072),
    "ab046": (1301540429749026816, 131072),
    "ab047": (1297036832269139968, 131072),
    "ab048": (1297041228168167424, 131072),
    "ab049": (1155314042043105280, 8192),
    "ab050": (1306044029376397312, 131072),
    "ab051": (1297036834416623616, 131072),
    "ab052": (1297036830122180608, 131072),
    "ab053": (1297036830122704896, 131072),
    "ab054": (1297036830123753472, 131072),
}
ADOPTED_LEGAL = {
    "ab017": 93,
    "ab018": 83,
    "ab019": 88,
    "ab020": 85,
    "ab021": 89,
    "ab022": 79,
    "ab023": 86,
    "ab024": 90,
    "ab025": 93,
    "ab026": 86,
    "ab027": 101,
    "ab029": 97,
    "ab030": 88,
    "ab031": 94,
    "ab032": 93,
    "ab033": 99,
    "ab034": 94,
    "ab035": 97,
    "ab036": 84,
    "ab037": 96,
    "ab038": 100,
    "ab039": 87,
    "ab040": 96,
    "ab041": 99,
    "ab042": 84,
    "ab043": 84,
    "ab044": 95,
    "ab045": 87,
    "ab046": 94,
    "ab047": 90,
    "ab048": 96,
    "ab049": 88,
    "ab050": 98,
    "ab051": 101,
    "ab052": 95,
    "ab053": 95,
    "ab054": 95,
}
MEMBERSHIP_EXPECT = {
    "ab017": 4,
    "ab018": 4,
    "ab019": 3,
    "ab020": 4,
    "ab021": 4,
    "ab022": 4,
    "ab023": 3,
    "ab024": 4,
    "ab025": 4,
    "ab026": 3,
    "ab027": 4,
    "ab029": 4,
    "ab030": 4,
    "ab031": 4,
    "ab032": 4,
    "ab033": 4,
    "ab034": 4,
    "ab035": 4,
    "ab036": 2,
    "ab037": 4,
    "ab038": 4,
    "ab039": 4,
    "ab040": 4,
    "ab041": 4,
    "ab042": 4,
    "ab043": 4,
    "ab044": 4,
    "ab045": 4,
    "ab046": 4,
    "ab047": 4,
    "ab048": 4,
    "ab049": 4,
    "ab050": 4,
    "ab051": 4,
    "ab052": 4,
    "ab053": 4,
    "ab054": 4,
}
PRIOR_ADOPTED_IDS = ['ab001', 'ab002', 'ab003', 'ab004', 'ab005', 'ab006', 'ab007', 'ab008', 'ab009', 'ab010', 'ab011', 'ab012', 'ab013', 'ab014', 'ab015', 'ab016']
PRIOR_ADOPTED_NODES = {
    "ab001": 4265342,
    "ab002": 3662776,
    "ab003": 4447441,
    "ab004": 2687012,
    "ab005": 3714648,
    "ab006": 3855756,
    "ab007": 3763776,
    "ab008": 2890562,
    "ab009": 1786048,
    "ab010": 4242063,
    "ab011": 4806135,
    "ab012": 2606954,
    "ab013": 2284195,
    "ab014": 4280600,
    "ab015": 3912106,
    "ab016": 4258557,
}
WIN_UNCONSUMED_IDS = ["ab028"]
WIN_UNCONSUMED = {
    "ab028": {"nodes": 3167121, "result": 1, "legal": 80,
               "lo": 1297036830121656320, "hi": 131074,
               "s5_index": 93815, "membership_class_count": 3},
}
PROBED_IDS = ['ab001', 'ab002', 'ab003', 'ab004', 'ab005', 'ab006', 'ab007', 'ab008', 'ab009', 'ab010', 'ab011', 'ab012', 'ab013', 'ab014', 'ab015', 'ab016', 'ab017', 'ab018', 'ab019', 'ab020', 'ab021', 'ab022', 'ab023', 'ab024', 'ab025', 'ab026', 'ab027', 'ab028', 'ab029', 'ab030', 'ab031', 'ab032', 'ab033', 'ab034', 'ab035', 'ab036', 'ab037', 'ab038', 'ab039', 'ab040', 'ab041', 'ab042', 'ab043', 'ab044', 'ab045', 'ab046', 'ab047', 'ab048', 'ab049', 'ab050', 'ab051', 'ab052', 'ab053', 'ab054']
FILELESS_UNPROBED_IDS = []
STATUS_LINES_EXPECTED = 55
STATUS_FINAL_LINE = "2026-11-24T01:58:20Z ab054 PASS 15000000,2,3014059"
STATUS_DRIVE1_LINES = 16
WIN_HALT_LINE = "2026-11-24T01:36:42Z ab028 WIN-HALT"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sys_exit(msg: str):
    print(f"ABORT {msg}", file=sys.stderr)
    raise SystemExit(1)


def parse_replay(path: Path):
    row = None
    rows_seen = 0
    for line in path.read_text().splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            rows_seen += 1
            row = {
                "stones": int(parts[2]), "legal": int(parts[3]),
                "is_or": int(parts[4]),
                "budget": int(parts[5]), "result": int(parts[6]),
                "nodes": int(parts[7]),
                "lo": int(parts[9]), "hi": int(parts[10]),
            }
    if rows_seen != 1 or row is None:
        sys_exit(f"expected exactly one replay row in {path}")
    return row


def verify_kit(dirp: Path, manifest_sha: str, kit_files: int):
    if not dirp.is_dir():
        sys_exit(f"kit dir missing {dirp}")
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        sys_exit(f"kit {dirp.name} MANIFEST sha drift")
    verified = 0
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        want, rel = line.split(None, 1)
        p = dirp / rel
        if not p.is_file():
            sys_exit(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"kit {dirp.name} file sha drift: {rel}")
        verified += 1
    if verified != kit_files:
        sys_exit(f"kit {dirp.name} files verified {verified} != {kit_files}")
    return verified


def two_pass(kid: str):
    variants = {}
    for tag in ("p1", "p2"):
        p = B29_DIR / f"output/raw/{kid}.{tag}.out"
        if not p.is_file():
            sys_exit(f"missing raw {p}")
        txt = p.read_text()
        if "# replay_done" not in txt:
            sys_exit(f"raw {p} lacks the '# replay_done' completeness guard")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys_exit(f"{kid}: pass mismatch {tag} {r} vs p1 {ref}")
    return ref


def parse_status(path: Path):
    got = {}
    win_halt_seen = 0
    lines = path.read_text().splitlines()
    if len(lines) != STATUS_LINES_EXPECTED:
        sys_exit(f"status lines {len(lines)} != {STATUS_LINES_EXPECTED}")
    if lines[-1] != STATUS_FINAL_LINE:
        sys_exit(f"status final line drift: {lines[-1]!r}")
    # append-only drive-1 prefix gate: the first 16 lines byte-reproduce the
    # CU-pinned drive-1 status.log (6b877344...)
    prefix = ("\n".join(lines[:STATUS_DRIVE1_LINES]) + "\n").encode("utf-8")
    if hashlib.sha256(prefix).hexdigest() != B29_STATUS_DRIVE1_PREFIX_SHA:
        sys_exit("status.log drive-1 prefix does not byte-reproduce the CU pin")
    joined = "\n".join(lines)
    if re.search(r"\b(EXHAUSTED|TRUNCATED|EXECUTION-COMPLETE|P1-FAIL)\b", joined):
        sys_exit("status.log carries an out-of-scope record")
    if joined.count(WIN_HALT_LINE) != 1:
        sys_exit("status.log must carry exactly the one pinned ab028 WIN-HALT row")
    for line in lines:
        if line == WIN_HALT_LINE:
            win_halt_seen += 1
            continue
        m = re.match(r"^(\S+) (ab\d{3}) PASS (\d+),(\d+),(\d+)$", line)
        if not m:
            sys_exit(f"status line not a clean PASS row: {line!r}")
        kid, b, r, n = m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
        if kid in got:
            sys_exit(f"status key {kid} appears more than once (each-once gate)")
        if kid not in PROBED_IDS:
            sys_exit(f"status key {kid} is not one of the 54 probed keys")
        got[kid] = (b, r, n)
    if win_halt_seen != 1:
        sys_exit(f"WIN-HALT lines {win_halt_seen} != 1")
    if set(got) != set(PROBED_IDS) or len(got) != 54:
        sys_exit("status probed set != the 54 probed keys")
    return got, lines


def main() -> None:
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache sha drift")
    merger = EXP / "scripts/s5_union_merge.py"
    if sha(merger) != MERGER_SHA_EXPECTED:
        sys_exit("fail-closed union merger (scripts/s5_union_merge.py) sha drift: "
                 "this Part must use the pinned merger byte-for-byte")
    if sha(B29_DIR / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED:
        sys_exit("batch-29 kit jsreplay.js sha drift (pinned solver image)")

    base_keys = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    if len(base_keys) != BASE_CACHE_ROWS_EXPECTED:
        sys_exit(f"base cache rows {len(base_keys)} != {BASE_CACHE_ROWS_EXPECTED}")
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    # --- kit integrity: the published batch-29 kit, file-by-file ---------------
    kit_verified = verify_kit(B29_DIR, B29_MANIFEST_SHA_EXPECTED, B29_KIT_FILES_EXPECTED)
    if sha(B29_DIR / "input/batch-keys.json") != B29_KEYS_SHA_EXPECTED:
        sys_exit("batch-keys.json sha drift")

    # --- post-scaffold published val-gate host files ---------------------------
    host_verified = 0
    for name, want in sorted(HOST_PIN.items()):
        p = B29_DIR / "val-gate" / name
        if not p.is_file():
            sys_exit(f"post-scaffold val-gate file missing: {name}")
        if sha(p) != want:
            sys_exit(f"post-scaffold val-gate sha drift: {name}")
        host_verified += 1
    if host_verified != 8:
        sys_exit(f"post-scaffold val-gate files {host_verified} != 8")

    # --- batch-keys -----------------------------------------------------------
    bk_all = json.loads((B29_DIR / "input/batch-keys.json").read_text())
    if bk_all["schema"] != "n11-centralreply-closure-class2251-batch29-input-v1":
        sys_exit(f"batch-keys schema drift: {bk_all['schema']}")
    if bk_all["class_index"] != 2251 or bk_all["budget"] != BUDGET:
        sys_exit("batch-keys class/budget drift")
    if bk_all["closure_class_rank_in_published_base"] != 35:
        sys_exit("batch-keys closure rank drift (kit frozen at selection)")
    if int(bk_all["published_base_canonical_rows"]) != 6294:
        sys_exit("batch-keys published_base_canonical_rows drift (kit frozen at selection)")
    if bk_all["class_mask"] != ["1155314042043105280", "0"]:
        sys_exit("batch-keys class mask drift")
    by_id = {k["key_id"]: k for k in bk_all["keys"]}
    if len(by_id) != 54:
        sys_exit(f"batch-keys key count {len(by_id)} != 54")

    # --- status.log picture -----------------------------------------------------
    if sha(B29_DIR / "output/status.log") != B29_STATUS_SHA_EXPECTED:
        sys_exit("status.log sha drift")
    status, slines = parse_status(B29_DIR / "output/status.log")

    # --- two-pass raw verification of all 54 probed keys ------------------------
    raws = {}
    for kid in PROBED_IDS:
        ref = two_pass(kid)
        if ref["budget"] != BUDGET or ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/budget {ref}")
        bk = by_id.get(kid)
        if bk is None:
            sys_exit(f"batch-keys.json missing {kid}")
        if ref["legal"] != int(bk["legal"]):
            sys_exit(f"{kid}: legal mismatch raw={ref['legal']} keys={bk['legal']}")
        if (ref["lo"], ref["hi"]) != (int(bk["lo"]), int(bk["hi"])):
            sys_exit(f"{kid}: key mismatch raw=({ref['lo']},{ref['hi']}) keys=({bk['lo']},{bk['hi']})")
        if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
            sys_exit(f"{kid}: status.log disagreement {status.get(kid)} vs raw {ref}")
        raws[kid] = ref
    loss_set = sorted(k for k, r in raws.items() if r["result"] == 2)
    win_set = sorted(k for k, r in raws.items() if r["result"] == 1)
    exh_set = sorted(k for k, r in raws.items() if r["result"] == 0)
    if win_set != WIN_UNCONSUMED_IDS:
        sys_exit(f"the only WIN over the probed batch must be {WIN_UNCONSUMED_IDS}, got {win_set}")
    if exh_set:
        sys_exit(f"probed batch must carry no EXHAUSTED row, got {exh_set}")
    if loss_set != sorted(ADOPTED_LOSS_IDS + PRIOR_ADOPTED_IDS):
        sys_exit("the raw LOSS set != the 53 resolved LOSS keys (37 new + 16 prior)")

    # --- raw file inventory: exactly 108 pass files, no sidecars/fragments ------
    raw_dir = B29_DIR / "output/raw"
    present = sorted(p.name for p in raw_dir.iterdir() if p.is_file())
    expected_files = sorted(f"{kid}.{tag}.out" for kid in PROBED_IDS for tag in ("p1", "p2"))
    if present != expected_files:
        sys_exit(f"raw inventory drift: {sorted(set(present) ^ set(expected_files))}")

    # --- gate the adopted keys against BASE / quarantine -------------------------
    emitted_keys = set()
    for kid in ADOPTED_LOSS_IDS:
        key = (raws[kid]["lo"], raws[kid]["hi"])
        if key != ADOPTED_KEYS[kid]:
            sys_exit(f"{kid}: raw key != pinned adopted key")
        if int(by_id[kid]["s5_index"]) != ADOPTED_S5[kid]:
            sys_exit(f"{kid}: batch-keys s5 drift")
        if int(by_id[kid]["membership_class_count"]) != MEMBERSHIP_EXPECT[kid]:
            sys_exit(f"{kid}: batch-keys membership drift")
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE cache {key} "
                     "(base=(%s, %s), raw=(result %s, nodes %s)); the batch-29 "
                     "fresh rows post-date the Part CU merge (fresh-increment gate)"
                     % (base_keys[key][0], base_keys[key][1],
                        raws[kid]["result"], raws[kid]["nodes"]))
        if key in emitted_keys:
            sys_exit(f"{kid}: duplicate emitted key {key}")
        emitted_keys.add(key)
    # chain continuity: the 16 Part CU rows must be present in BASE as LOSS
    for kid in PRIOR_ADOPTED_IDS:
        key = (raws[kid]["lo"], raws[kid]["hi"])
        row = base_keys.get(key)
        if row is None:
            sys_exit(f"{kid}: prior CU-adopted key missing from BASE (chain drift) {key}")
        if row != (2, PRIOR_ADOPTED_NODES[kid]):
            sys_exit(f"{kid}: BASE row {row} != prior CU adoption pin (2, {PRIOR_ADOPTED_NODES[kid]})")
    # the unconsumed WIN key must be fresh (consumed nowhere)
    w = WIN_UNCONSUMED["ab028"]
    wkey = (w["lo"], w["hi"])
    if (raws["ab028"]["lo"], raws["ab028"]["hi"]) != wkey:
        sys_exit("ab028 raw key != pinned WIN key")
    if raws["ab028"]["result"] != 1 or raws["ab028"]["nodes"] != w["nodes"]:
        sys_exit(f"ab028 raw row != pinned WIN pin: {raws['ab028']}")
    if raws["ab028"]["legal"] != w["legal"]:
        sys_exit("ab028 raw legal != pinned WIN legal")
    if int(by_id["ab028"]["s5_index"]) != w["s5_index"]:
        sys_exit("ab028 batch-keys s5 drift")
    if int(by_id["ab028"]["membership_class_count"]) != w["membership_class_count"]:
        sys_exit("ab028 batch-keys membership drift")
    if wkey in base_keys or wkey in quarantined or wkey in emitted_keys:
        sys_exit("the unconsumed WIN key must appear in no canonical cache/increment/quarantine here")

    # --- the 37 fresh adopted LOSS rows -----------------------------------------
    nodes_p1_total = 0
    nodes_p2_total = 0
    for kid in ADOPTED_LOSS_IDS:
        ref = raws[kid]
        if ref["result"] != 2:
            sys_exit(f"{kid}: adopted row must be result 2, got {ref['result']}")
        if ref["nodes"] != ADOPTED_NODES[kid]:
            sys_exit(f"{kid}: adopted-row nodes drift {ref['nodes']} != {ADOPTED_NODES[kid]}")
        if ref["legal"] != ADOPTED_LEGAL[kid]:
            sys_exit(f"{kid}: adopted-row legal drift")
        nodes_p1_total += ref["nodes"]
        n_p2 = sum(int(line.split(",")[7])
                   for line in (B29_DIR / f"output/raw/{kid}.p2.out").read_text().splitlines()
                   if line.startswith("replay,"))
        nodes_p2_total += n_p2
        if n_p2 != ref["nodes"]:
            sys_exit(f"{kid}: adopted-row pass node totals disagree: {n_p2} vs {ref['nodes']}")
    if nodes_p1_total != ADOPTED_TOTAL_NODES or nodes_p2_total != ADOPTED_TOTAL_NODES:
        sys_exit(f"adopted packet node totals drift p1={nodes_p1_total} p2={nodes_p2_total} "
                 f"!= {ADOPTED_TOTAL_NODES}")

    # --- val-gate four-host node-exact cross-check -----------------------------
    for gate, (exp_r, exp_n) in sorted(VAL_GATE_EXPECT.items()):
        for host in ("published-baseline", "batch29-host", "takeover-host", "d2-host"):
            p = B29_DIR / f"val-gate/{gate}.{host}.out"
            if not p.is_file():
                sys_exit(f"val-gate file missing for {gate} host {host}")
            row = parse_replay(p)
            if (row["result"], row["nodes"]) != (exp_r, exp_n):
                sys_exit(f"val-gate {gate} host {host} not node-exact "
                         f"({row['result']},{row['nodes']}) != ({exp_r},{exp_n})")

    # --- emit the increment + manifest ------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = [
        "# n11 central-reply closure batch-29 (class 2251) 37-LOSS",
        "#   canonical-adoption increment (Part DA, 2026-11-24)",
        "# published batch-29 kit (Part CI scaffold + takeover drives):",
        "#   ALL 54 of 54 keys probed 2-pass fresh-cold at budget 15M.",
        "#   53 keys resolved LOSS (16 of them ab001..ab016 were already",
        "#   adopted canonically by Part CU and are NOT re-emitted here);",
        "#   the 37 fresh rows ab017..ab054 except ab028 ARE this increment.",
        "#   1 key (ab028) is a probe-level WIN (nodes 3,167,121) that stays",
        "#   UNCONSUMED: not adopted, not emitted, not in any canonical cache",
        "#   (WIN-row scrutiny is the separate C++ owner lane, pin 9193f5b6...",
        "#   no completeness claim is made beyond the two-pass raw labels).",
        "# 2-pass node-exact exact-S5 verdict at budget 15M, fresh cold, pinned",
        "#   jsreplay.js sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# gates: kit MANIFEST sha-verified file-by-file (71 files); the 8",
        "#   post-scaffold val-gate host files pinned and verified four-host",
        "#   node-exact against the kit batch29-host outputs and the",
        "#   published baselines; all 54 probed keys two-pass node-exact with",
        "#   '# replay_done' on both passes; status.log (55 lines, sha-pinned,",
        "#   CU drive-1 16-line prefix byte-pinned, one ab028 WIN-HALT row)",
        "#   each-once agreement on (b,r,n); raw inventory exactly",
        "#   ab001..ab054 x {p1,p2} (108 files; no sidecars, no fragments);",
        "#   batch-keys legal/(lo,hi)/s5/membership agreement; adopted-row",
        "#   per-pass node total 159,325,566; adopted keys distinct and",
        "#   absent from BASE 30ddad9d... (6,317 rows) while the 16 CU rows",
        "#   are present as LOSS with their CU nodes (chain continuity);",
        "#   adopted keys absent from the quarantine registry.",
        "# ADOPTED set = ab017..ab054 except ab028 (37 keys, s5 indices",
        "#   78838..93841, membership 4 except ab019/ab023/ab026 (3) and",
        "#   ab036 (2)).  The batch is probe-complete; full != loss because",
        "#   ab028 IS a WIN row at probe level and stays unconsumed.",
        "# The 37 LOSS rows ARE consumed into the canonical cache by the",
        "#   fail-closed union merger; 11x11 stays UNKNOWN; nodes are",
        "#   bookkeeping, never verdicts; class 2251 is NOT freed (its last",
        "#   unknown child is the unconsumed WIN ab028).",
    ]
    rows_for_sort = [(ADOPTED_KEYS[k][0], ADOPTED_KEYS[k][1], ADOPTED_NODES[k])
                     for k in ADOPTED_LOSS_IDS]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_path = OUT / "increment-b29loss37-20261124.cache"
    incr_path.write_bytes(blob)
    incr_sha = hashlib.sha256(blob).hexdigest()

    manifest = {
        "schema": "b29loss37-increments-manifest-v1",
        "batches": [{
            "batch": 29,
            "class_index": 2251,
            "keys_total": 54,
            "adopted_loss_ids": list(ADOPTED_LOSS_IDS),
            "already_adopted_ids": list(PRIOR_ADOPTED_IDS),
            "unadopted_win_ids": list(WIN_UNCONSUMED_IDS),
            "exhausted_excluded_ids": [],
            "probed_ids": list(PROBED_IDS),
            "fragment_ids": [],
            "fileless_unprobed_count": 0,
            "fileless_unprobed_ids": [],
            "input_sha256": B29_KEYS_SHA_EXPECTED,
            "status_log_sha256": B29_STATUS_SHA_EXPECTED,
            "status_log_lines": STATUS_LINES_EXPECTED,
            "status_log_final_line": STATUS_FINAL_LINE,
            "status_log_drive1_prefix_sha256": B29_STATUS_DRIVE1_PREFIX_SHA,
            "win_halt_line": WIN_HALT_LINE,
            "kit_integrity": {
                "manifest_sha256": B29_MANIFEST_SHA_EXPECTED,
                "files_verified": kit_verified,
            },
            "post_scaffold_val_gate_files": dict(sorted(HOST_PIN.items())),
            "val_gate_multi_host_node_exact": True,
            "total_nodes_pass_one": nodes_p1_total,
            "total_nodes_pass_two": nodes_p2_total,
            "stop_rule": "batch-29 probe-complete (54/54 keys probed 2-pass fresh-cold "
                         "budget 15M across Part CI drive-1 + takeover drive-2; loss-only "
                         "adoption of the 37 fresh rows; the probe-level WIN ab028 stays "
                         "unconsumed pending the scrutiny-owner C++ gate; verdict not consumed)",
            "fragment_state": {},
        }],
        "resolved_ids": list(ADOPTED_LOSS_IDS),
        "loss_ids": list(ADOPTED_LOSS_IDS),
        "win_ids": list(WIN_UNCONSUMED_IDS),
        "unadopted_win_ids": list(WIN_UNCONSUMED_IDS),
        "exhausted_excluded_ids": [],
        "row_counts": {
            "probed_rows": 54, "adopted_loss_rows": 37, "prior_adopted_loss_rows": 16,
            "wins": 1, "exhausted_excluded": 0, "fragments_unprobed": 0,
            "fileless_unprobed": 0,
        },
        "sha256": {"loss": incr_sha},
        "full_packet_eq_loss_only": False,
        "full_packet_eq_loss_only_rationale":
            "the batch is probe-complete (54/54 two-pass fresh-cold at budget 15M) but "
            "the packet is NOT loss-only: ab028 is a probe-level WIN (result 1, nodes "
            "3,167,121) that stays UNCONSUMED and is NOT adopted; the adopted packet is "
            "the 37 fresh LOSS rows (ab017..ab054 except ab028) plus nothing else; the "
            "16 prior rows ab001..ab016 were already adopted by Part CU and are not "
            "re-emitted; class 2251 is NOT freed (an unconsumed WIN child remains and "
            "no LOSS-only adoption can consume it)",
        "win_scenario_exists": True,
        "win_scenario_note":
            "exactly one WIN row (ab028) exists in the batch and it stays unconsumed by "
            "this adoption (scrutiny owner C++ second-implementation gate pin "
            "9193f5b6...; Part CZ published the three-implementation corroboration for "
            "it on 2026-11-24); loss-only adoption NEVER frees class 2251 while the "
            "ab028 child verdict remains unconsumed",
        "unadopted_win_rows": [{"key_id": "ab028",
                                "result": 1, "nodes": WIN_UNCONSUMED["ab028"]["nodes"],
                                "legal": WIN_UNCONSUMED["ab028"]["legal"],
                                "lo": WIN_UNCONSUMED["ab028"]["lo"],
                                "hi": WIN_UNCONSUMED["ab028"]["hi"],
                                "s5_index": WIN_UNCONSUMED["ab028"]["s5_index"]}],
        "exhausted_rows": [],
        "fragment_rows_note":
            "batch-29 is probe-complete with NO fragment keys and NO truncated sidecars: "
            "the raw inventory is exactly ab001..ab054 x {p1,p2} (108 files)",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "base_cache_prior_adoption_confirmed": 16,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 37-LOSS adoption increment: only the 37 fresh LOSS rows "
            "(ab017..ab054 except ab028) are consumed into the canonical cache via "
            "the fail-closed union merger; the probe-level WIN ab028 is consumed "
            "NOWHERE (no verdict claim, no exclusion claim); all 54 batch-29 keys "
            "stay UNKNOWN as verdicts; adopting 37 LOSS rows does NOT free class "
            "2251 (the unconsumed ab028 child remains); 11x11 stays UNKNOWN; nodes "
            "are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INCREMENT rows=37 loss_nodes={ADOPTED_TOTAL_NODES} -> {incr_path}")


if __name__ == "__main__":
    main()
