#!/usr/bin/env python3
"""Build the batch-33 (class 34908) 45-LOSS canonical-adoption increment, fail-closed.

Prepared for the Part DT adoption (declared 2026-11-24, publish-then-execute):
the published batch-33 cumulative evidence is byte-pinned through the single
batch-33 kit (Part DQ/DR/DS drive-1+2+3, MANIFEST
f2603e3a12d291579f02b81b7c388b5c952b90125df53756c91812368f16dbcb, whose
186 listed files are input 55 + output/raw 111 (108 primary pairs + 3 pinned
truncated-retry sidecars) + output/status.log 1 + scripts 6 + val-gate 12 +
README 1, the MANIFEST itself excluded).  Every listed kit file is
sha256-verified here file-by-file.
jsreplay.js 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df is
the pinned solver image shared with the earlier kits and val-gates.

The batch is FULLY probed: all 54 of 54 keys carry honest two-pass fresh-cold
labels at budget 15M (the drive honest-label statuses: 45 PASS result=2 LOSS,
4 PASS result=1 WIN with pre-registered WIN-HALT markers
{af029, af047, af050, af053}, 5 PASS result=0 EXHAUSTED honest UNKNOWN
{af003, af023, af034, af039, af048}, MISMATCH 0, and 3 pinned
P2-TRUNCATED-RETRY markers {af008, af039, af048} each resolved by a completed
retry).  ONLY the 45 LOSS rows ARE adopted here.  The 4 WIN rows and the
5 EXHAUSTED rows are consumed NOWHERE by this Part: WIN row adoption belongs
to the scrutiny-owner C++ second-implementation gate (pin 9193f5b6...) and
the EXHAUSTED rows stay honest UNKNOWN (high-budget reprobe is a separate
declaration condition).  Loss-only adoption does NOT by itself assert any
root verdict, and any class-34908 scheduling effect is derived only later by
the reaudit refresh + delta extractor (Board fail-closed child
verification), not by this maker.

The adoption base is the canonical exact-S5 verdict chain head = the Part DP
merged 6,502-row cache sha256
1ded9a083feabc095dd998c92002b47efc05b8666adf030501bcffc2873a9dd6
(BASE through the Part DP b32loss54 adoption), byte-pinned here; this maker
ABORTS against anything else.  Every adopted key is asserted fresh (absent
from the BASE) and absent from the quarantine registry
(81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9).

The drive status.log is HONEST HISTORY (66 lines = exactly 54 PASS verdict
rows, one per key, plus 4 WIN-HALT marker lines {af029, af047, af050, af053},
5 EXHAUSTED marker lines {af003, af023, af034, af039, af048} and 3
P2-TRUNCATED-RETRY marker lines {af008, af039, af048} each resolved by a
later completed verdict, MISMATCH lines 0): the per-key honest labels are
(15000000, result, nodes) with result in {0,1,2} pinned row-by-row here.

Fail-closed gates: kit MANIFEST sha-verified file-by-file (186 files); 54
two-pass fresh-cold raw re-verification with '# replay_done' on both passes
and (budget,result,nodes) agreement with the status verdict row-by-row;
raw/batch-keys agreement on (legal, lo, hi) and pins on
(s5_index, membership_class_count); raw inventory == 54 x {p1,p2} primaries +
exactly the 3 pinned truncated-retry sidecars (retry artifacts, never verdict
rows, and must NOT carry the '# replay_done' guard); val-gate node-exact
across the two published host outputs per gate molecule (4 molecules x
published-baseline + b33-host); the 45 adopted keys distinct, ABSENT from the
canonical BASE (6,502 rows) and from the quarantine registry; the derived
WIN/EXHAUSTED sets equal to the pinned marker sets; adopted-row per-pass node
total 281411183 on both passes (all-54 total 383609606).  Verdicts are
byte-taken from the raws.  The 45 LOSS rows ARE the only thing consumed into
the canonical cache by this Part; 11x11 stays UNKNOWN; nodes are
bookkeeping, never verdicts.
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
KIT1_DIR = ROOT / "research/experiments/n11-centralreply-closure-class34908-batch33-20261124"
KIT1_RAW = KIT1_DIR / "output/raw"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class8730-b32loss54-adoption-reaudit-20261124/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-20261124.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
MERGER = EXP / "scripts/s5_union_merge.py"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "1ded9a083feabc095dd998c92002b47efc05b8666adf030501bcffc2873a9dd6"
BASE_CACHE_ROWS_EXPECTED = 6502
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6344
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

# --- published kit pins -------------------------------------------------------
KIT1_MANIFEST_SHA = "f2603e3a12d291579f02b81b7c388b5c952b90125df53756c91812368f16dbcb"
KIT1_FILES = 186
KIT1_KEYS_SHA = "8a863381454fcfec3cb190db7130ce6801accf56170ee3a1b944402491fecbaa"
KIT1_STATUS_SHA = "1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52"

# --- status.log honest-history pins ----------------------------------------------
KIT1_STATUS_LINES = 66
KIT1_STATUS_FIRST_LINE = "2026-11-24T17:04:25Z af001 PASS 15000000,2,2952432"
KIT1_STATUS_FINAL_LINE = "2026-11-24T18:41:47Z af054 PASS 15000000,2,4283588"
WIN_HALT_LINES = [
    "2026-11-24T17:46:03Z af029 WIN-HALT",
    "2026-11-24T18:22:34Z af047 WIN-HALT",
    "2026-11-24T18:37:06Z af050 WIN-HALT",
    "2026-11-24T18:38:40Z af053 WIN-HALT",
]
EXHAUSTED_LINES = [
    "2026-11-24T17:10:15Z af003 EXHAUSTED 15000000,0,15000000",
    "2026-11-24T17:41:01Z af023 EXHAUSTED 15000000,0,15000000",
    "2026-11-24T17:59:53Z af034 EXHAUSTED 15000000,0,15000000",
    "2026-11-24T18:09:46Z af039 EXHAUSTED 15000000,0,15000000",
    "2026-11-24T18:34:34Z af048 EXHAUSTED 15000000,0,15000000",
]
RETRY_LINES = [
    "2026-11-24T17:17:04Z af008 P2-TRUNCATED-RETRY",
    "2026-11-24T18:07:16Z af039 P2-TRUNCATED-RETRY",
    "2026-11-24T18:32:15Z af048 P2-TRUNCATED-RETRY",
]
TRUNCATED_SIDECARS = [
    "af008.p2.truncated.171704.out",
    "af039.p2.truncated.180716.out",
    "af048.p2.truncated.183215.out",
]
BUDGET_KIT1 = 15000000

# --- adopted packet ------------------------------------------------------------
PROBED_IDS = [f"af{i:03d}" for i in range(1, 55)]
WIN_IDS = ["af029", "af047", "af050", "af053"]
EXH_IDS = ["af003", "af023", "af034", "af039", "af048"]
ADOPTED_LOSS_IDS = [k for k in PROBED_IDS if k not in WIN_IDS and k not in EXH_IDS]
ADOPTED_KEYS = {
    'af001': {'key': (1152921504742113281, 68719476736), 'legal': 91, 'nodes': 2952432, 's5': 1176, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af002': {'key': (10376293541462671361, 68719476736), 'legal': 93, 'nodes': 10550283, 's5': 38614, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af004': {'key': (1152921779485802497, 68719476736), 'legal': 96, 'nodes': 3318813, 's5': 225112, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af005': {'key': (5764607523035283457, 68719476736), 'legal': 98, 'nodes': 5078821, 's5': 259539, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af006': {'key': (1152921504607961089, 68719476736), 'legal': 98, 'nodes': 5970933, 's5': 325164, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af007': {'key': (1152921504607895553, 68719476737), 'legal': 99, 'nodes': 7700082, 's5': 356884, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af008': {'key': (1152921504607895585, 68719476736), 'legal': 91, 'nodes': 14364852, 's5': 415399, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af009': {'key': (1152921504607895553, 68719476738), 'legal': 93, 'nodes': 3618250, 's5': 442092, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af010': {'key': (1153202979584606209, 68719476736), 'legal': 84, 'nodes': 5558617, 's5': 494504, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af011': {'key': (1152921504607895553, 68719476992), 'legal': 84, 'nodes': 9514618, 's5': 544291, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af012': {'key': (1152921642046849025, 68719476736), 'legal': 91, 'nodes': 9240870, 's5': 564062, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af013': {'key': (1152922054363709441, 68719476736), 'legal': 94, 'nodes': 6573273, 's5': 597227, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af014': {'key': (1155173304421580801, 68719476736), 'legal': 98, 'nodes': 9869039, 's5': 605532, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af015': {'key': (1152921504607895553, 68719477248), 'legal': 96, 'nodes': 5884486, 's5': 625618, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af016': {'key': (1152921504675004417, 68719476736), 'legal': 97, 'nodes': 5920144, 's5': 682541, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af017': {'key': (1152921504876331009, 68719476736), 'legal': 93, 'nodes': 6520712, 's5': 709725, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af018': {'key': (1157425104235266049, 68719476736), 'legal': 93, 'nodes': 4504991, 's5': 716543, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af019': {'key': (1152921504607895553, 68719477760), 'legal': 100, 'nodes': 4140443, 's5': 732262, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af020': {'key': (1152921504607928321, 68719476736), 'legal': 96, 'nodes': 6989622, 's5': 772553, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af021': {'key': (1152921504608026625, 68719476736), 'legal': 96, 'nodes': 5619693, 's5': 794839, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af022': {'key': (1161928703862636545, 68719476736), 'legal': 95, 'nodes': 4329388, 's5': 800281, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af024': {'key': (1152921504607895569, 68719476736), 'legal': 87, 'nodes': 6089162, 's5': 839602, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af025': {'key': (1152921504607895617, 68719476736), 'legal': 97, 'nodes': 2894174, 's5': 854635, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af026': {'key': (1170935903117377537, 68719476736), 'legal': 100, 'nodes': 4299814, 's5': 858969, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af027': {'key': (1152921504607895553, 68719480832), 'legal': 90, 'nodes': 2601444, 's5': 866321, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af028': {'key': (1152921573327372289, 68719476736), 'legal': 86, 'nodes': 3569293, 's5': 887040, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af030': {'key': (1152921504641449985, 68719476736), 'legal': 101, 'nodes': 4462892, 's5': 904339, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af031': {'key': (1152921505144766465, 68719476736), 'legal': 97, 'nodes': 4165016, 's5': 913616, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af032': {'key': (1152923703631151105, 68719476736), 'legal': 97, 'nodes': 5132691, 's5': 916477, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af033': {'key': (1152921504607895553, 68721573888), 'legal': 101, 'nodes': 11737990, 's5': 921203, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af035': {'key': (1152921504608157697, 68719476736), 'legal': 97, 'nodes': 6690990, 's5': 937328, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af036': {'key': (1152925902654406657, 68719476736), 'legal': 93, 'nodes': 3982739, 's5': 939215, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af037': {'key': (1152921504607895553, 68723671040), 'legal': 97, 'nodes': 10047387, 's5': 941383, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af038': {'key': (1152921504607895561, 68719476736), 'legal': 98, 'nodes': 8731665, 's5': 946835, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af040': {'key': (1152930300700917761, 68719476736), 'legal': 94, 'nodes': 5576569, 's5': 951758, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af041': {'key': (1152921504607895553, 68727865344), 'legal': 101, 'nodes': 7100779, 's5': 953035, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af042': {'key': (1152921504607903745, 68719476736), 'legal': 86, 'nodes': 10487546, 's5': 958529, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af043': {'key': (1152921504608419841, 68719476736), 'legal': 97, 'nodes': 6467873, 's5': 960072, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af044': {'key': (1152921506755379201, 68719476736), 'legal': 95, 'nodes': 11691718, 's5': 960568, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af045': {'key': (1152921504607895553, 77309411328), 'legal': 91, 'nodes': 3895802, 's5': 960786, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af046': {'key': (1152921504607895557, 68719476736), 'legal': 99, 'nodes': 5382774, 's5': 961459, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af049': {'key': (1152921504607895553, 85899345920), 'legal': 99, 'nodes': 4811237, 's5': 962233, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af051': {'key': (1152921504609992705, 68719476736), 'legal': 96, 'nodes': 5475786, 's5': 962410, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af052': {'key': (1152921504606852096, 17626545782784), 'legal': 90, 'nodes': 3611892, 's5': 962450, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'af054': {'key': (1152921504606852096, 87960930222080), 'legal': 88, 'nodes': 4283588, 's5': 962471, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
}
ADOPTED_TOTAL_NODES = 281411183
ALL54_TOTAL_NODES = 383609606

# --- val-gate pins ---------------------------------------------------------------
VAL_GATES = {
    "at2m-s5-1152921504606851072-536870946": (2000000, 0, 2000000),
    "at2m-s5-1188950301626860544-536870912": (2000000, 0, 2000000),
    "first-15m-s5-1152921504606851072-536870946": (15000000, 2, 3651923),
    "second-15m-s5-1188950301626860544-536870912": (15000000, 2, 5040200),
}
VAL_HOSTS = ["published-baseline", "b33-host"]


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
                "lo": parts[9], "hi": parts[10],
            }
    if rows_seen != 1 or row is None:
        sys_exit(f"expected exactly one replay row in {path}")
    return row


def norm_key(row):
    return (int(row["lo"]), int(row["hi"]))


def _kit_candidates(kit_dir: Path, rel: str) -> list:
    cands = []
    cands.append(kit_dir / rel)
    cands.append(ROOT / rel)
    stripped = rel.split("research/experiments/", 1)[-1]
    stripped = stripped[stripped.index("/") + 1:] if stripped.startswith("n11") else stripped
    cands.append(kit_dir / stripped)
    cands.append(kit_dir / "output" / stripped)
    return cands


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
        p = None
        for cand in _kit_candidates(dirp, rel):
            if cand.is_file():
                p = cand
                break
        if p is None:
            sys_exit(f"kit {dirp.name} file missing: {rel} (resolved candidates tried)")
        if sha(p) != want:
            sys_exit(f"kit {dirp.name} file sha drift: {rel}")
        verified += 1
    if verified != kit_files:
        sys_exit(f"kit {dirp.name} files verified {verified} != {kit_files}")
    return verified


def two_pass(rawdir: Path, kid: str):
    variants = {}
    for tag in ("p1", "p2"):
        p = rawdir / f"{kid}.{tag}.out"
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
            sys_exit(f"{kid}: pass mismatch {tag} vs p1")
    return ref


PRIMARY_RE = re.compile(r"^af\d{3}\.p[12]\.out$")


def parse_status1(path: Path):
    lines = path.read_text().splitlines()
    if len(lines) != KIT1_STATUS_LINES:
        sys_exit(f"kit status lines {len(lines)} != {KIT1_STATUS_LINES}")
    if lines[0] != KIT1_STATUS_FIRST_LINE or lines[-1] != KIT1_STATUS_FINAL_LINE:
        sys_exit("kit status first/final line drift")
    got_pass = {}
    win_halt, exh, retry = [], [], []
    mismatch = []
    for line in lines:
        m = re.match(r"^(\S+) (af\d{3}) PASS (\d+),(\d+),(\d+)$", line)
        if m:
            kid = m.group(2)
            if kid in got_pass:
                sys_exit(f"kit status duplicate verdict row for {kid}")
            got_pass[kid] = (int(m.group(3)), int(m.group(4)), int(m.group(5)))
            continue
        m = re.match(r"^(\S+) (af\d{3}) WIN-HALT$", line)
        if m:
            win_halt.append(line)
            continue
        m = re.match(r"^(\S+) (af\d{3}) EXHAUSTED (\d+),(\d+),(\d+)$", line)
        if m:
            exh.append(line)
            continue
        m = re.match(r"^(\S+) (af\d{3}) P2-TRUNCATED-RETRY$", line)
        if m:
            retry.append(line)
            continue
        mismatch.append(line)
    if mismatch:
        sys_exit(f"kit status has unmatched/MISMATCH rows: {mismatch[:3]}")
    if win_halt != WIN_HALT_LINES:
        sys_exit("kit status WIN-HALT lines != the pinned 4-marker pre-registered halt history")
    if exh != EXHAUSTED_LINES:
        sys_exit("kit status EXHAUSTED lines != the pinned 5-marker honest-UNKNOWN history")
    if retry != RETRY_LINES:
        sys_exit("kit status TRUNCATED-RETRY lines != the pinned 3-marker history")
    if set(got_pass) != set(PROBED_IDS):
        sys_exit("kit status verdict keys != the 54 probed keys")
    return got_pass


def main() -> None:
    # --- base cache, merger, quarantine anchors -------------------------------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache sha drift")
    if sha(MERGER) != MERGER_SHA_EXPECTED:
        sys_exit("fail-closed union merger (scripts/s5_union_merge.py) sha drift: "
                 "this Part must use the pinned merger byte-for-byte")
    if sha(QUARANTINE) != QUARANTINE_SHA_EXPECTED:
        sys_exit("quarantine registry sha drift")
    base_keys = {}
    wins = losss = 0
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
            if int(row[4]) == 1:
                wins += 1
            elif int(row[4]) == 2:
                losss += 1
    if len(base_keys) != BASE_CACHE_ROWS_EXPECTED:
        sys_exit(f"base cache rows {len(base_keys)} != {BASE_CACHE_ROWS_EXPECTED}")
    if wins != BASE_CACHE_WIN_EXPECTED or losss != BASE_CACHE_LOSS_EXPECTED:
        sys_exit(f"base cache WIN/LOSS {wins}/{losss} != pinned")
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    # --- kit integrity -----------------------------------------------------------
    k1 = verify_kit(KIT1_DIR, KIT1_MANIFEST_SHA, KIT1_FILES)
    if sha(KIT1_DIR / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED:
        sys_exit("jsreplay.js sha drift in the kit (pinned solver image 8458...)")
    if sha(KIT1_DIR / "input/batch-keys.json") != KIT1_KEYS_SHA:
        sys_exit("batch-keys sha drift in the kit")
    if sha(KIT1_DIR / "output/status.log") != KIT1_STATUS_SHA:
        sys_exit("status.log sha drift in the kit")

    # --- batch-keys gates --------------------------------------------------------
    bk_all = json.loads((KIT1_DIR / "input/batch-keys.json").read_text())
    if bk_all["schema"] != "n11-centralreply-closure-class34908-batch33-input-v1":
        sys_exit("batch-keys schema drift")
    if bk_all["class_index"] != 34908 or bk_all["budget"] != BUDGET_KIT1:
        sys_exit("batch-keys class/budget drift")
    if len(bk_all["keys"]) != 54:
        sys_exit("batch-keys key count != 54")
    if bk_all["closure_class_rank_in_published_base"] != 36:
        sys_exit("batch-keys closure rank drift (kit frozen at selection)")
    if bk_all["runner_up_class"] != 11490:
        sys_exit("batch-keys runner_up_class drift (kit frozen at selection)")
    if int(bk_all["published_base_canonical_rows"]) != 6502:
        sys_exit("batch-keys published_base_canonical_rows drift (kit frozen at selection)")
    if bk_all["class_mask"] != ["1152921504607895553", "68719476736"]:
        sys_exit("batch-keys class mask drift")
    if bk_all["groups_served_count"] != 4 or len(bk_all["groups_served_full"]) != 4:
        sys_exit("batch-keys groups_served drift")
    if [tuple(g.items()) for g in bk_all["groups_served_full"]] != [
            (("first", 0), ("third", 20)), (("first", 0), ("third", 100)),
            (("first", 12), ("third", 10)), (("first", 12), ("third", 110))]:
        sys_exit("batch-keys groups_served_full drift")
    by_id = {k["key_id"]: k for k in bk_all["keys"]}

    # --- status log (honest history) ---------------------------------------------
    got_pass = parse_status1(KIT1_DIR / "output/status.log")

    # --- two-pass raw verification -----------------------------------------------
    raws15 = {}
    for kid in PROBED_IDS:
        ref = two_pass(KIT1_RAW, kid)
        if ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/or bit")
        if ref["budget"] != BUDGET_KIT1:
            sys_exit(f"{kid}: kit budget drift")
        e = by_id.get(kid)
        if e is None:
            sys_exit(f"batch-keys missing {kid}")
        if ref["legal"] != int(e["legal"]) or ref["lo"] != e["lo"] or ref["hi"] != e["hi"]:
            sys_exit(f"{kid}: legal/key disagreement raw vs batch-keys")
        if (ref["budget"], ref["result"], ref["nodes"]) != got_pass[kid]:
            sys_exit(f"{kid}: raw (budget,result,nodes) row != status verdict row")
        raws15[kid] = ref
    loss_set = sorted(kid for kid in PROBED_IDS if raws15[kid]["result"] == 2)
    win_set = sorted(kid for kid in PROBED_IDS if raws15[kid]["result"] == 1)
    exh_set = sorted(kid for kid in PROBED_IDS if raws15[kid]["result"] == 0)
    if loss_set != sorted(ADOPTED_LOSS_IDS):
        sys_exit("decisive LOSS set != the 45 adopted candidates")
    if win_set != sorted(WIN_IDS):
        sys_exit(f"probe-level WIN set != the pinned 4 unconsumed WIN keys: {win_set}")
    if exh_set != sorted(EXH_IDS):
        sys_exit(f"probe-level EXHAUSTED set != the pinned 5 honest-UNKNOWN keys: {exh_set}")
    if len(ADOPTED_LOSS_IDS) != 45 or len(WIN_IDS) != 4 or len(EXH_IDS) != 5:
        sys_exit("packet decomposition 45+4+5 != 54 drift")
    all54_nodes = sum(raws15[kid]["nodes"] for kid in PROBED_IDS)
    if all54_nodes != ALL54_TOTAL_NODES:
        sys_exit(f"all-54 node total drift {all54_nodes} != {ALL54_TOTAL_NODES}")

    # --- raw inventory: 108 primaries + exactly the 3 pinned truncated sidecars
    prim = sorted(p.name for p in KIT1_RAW.iterdir() if p.is_file() and PRIMARY_RE.match(p.name))
    side = sorted(p.name for p in KIT1_RAW.iterdir() if p.is_file() and not PRIMARY_RE.match(p.name))
    if prim != sorted(f"{kid}.{tag}.out" for kid in PROBED_IDS for tag in ("p1", "p2")):
        sys_exit("kit raw primary inventory drift")
    if side != sorted(TRUNCATED_SIDECARS):
        sys_exit(f"kit raw sidecar inventory drift: {side}")
    for sc in TRUNCATED_SIDECARS:
        p = KIT1_RAW / sc
        txt = p.read_text()
        if "# replay_done" in txt:
            sys_exit(f"truncated sidecar {sc} unexpectedly complete (guard present)")

    # --- val-gates node-exact across hosts ------------------------------------
    for gate, (exp_b, exp_r, exp_n) in sorted(VAL_GATES.items()):
        for host in VAL_HOSTS:
            p = KIT1_DIR / f"val-gate/{gate}.{host}.out"
            if not p.is_file():
                sys_exit(f"val-gate file missing: {gate} {host}")
            row = parse_replay(p)
            if (row["budget"], row["result"], row["nodes"]) != (exp_b, exp_r, exp_n):
                sys_exit(f"val-gate {gate} {host} not node-exact")

    # --- gate the adopted keys against BASE / quarantine ----------------------
    emitted = set()
    for kid in ADOPTED_LOSS_IDS:
        key = norm_key(raws15[kid])
        pins = ADOPTED_KEYS[kid]
        if key != pins["key"]:
            sys_exit(f"{kid}: raw key != pinned adopted key")
        if int(raws15[kid]["nodes"]) != pins["nodes"] or int(raws15[kid]["legal"]) != pins["legal"]:
            sys_exit(f"{kid}: adopted nodes/legal drift vs pins")
        if pins["decisive_budget"] != raws15[kid]["budget"]:
            sys_exit(f"{kid}: decisive budget drift")
        e = by_id[kid]
        if int(e["s5_index"]) != pins["s5"] or int(e["membership_class_count"]) != pins["mcc"]:
            sys_exit(f"{kid}: batch-keys s5/mcc drift vs pins")
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE {key}; fresh-increment gate")
        if key in emitted:
            sys_exit(f"{kid}: duplicate emitted key {key}")
        emitted.add(key)

    # --- the unconsumed WIN / EXHAUSTED keys must also be fresh (never adopted) --
    for kid in WIN_IDS + EXH_IDS:
        key = norm_key(raws15[kid])
        if key in base_keys:
            sys_exit(f"{kid} (unconsumed): key already in canonical BASE {key}")
        if key in emitted:
            sys_exit(f"{kid} (unconsumed): key collides with an adopted key")

    # --- node totals per pass ------------------------------------------------
    n1 = n2 = 0
    for kid in ADOPTED_LOSS_IDS:
        a = parse_replay(KIT1_RAW / f"{kid}.p1.out")
        b = parse_replay(KIT1_RAW / f"{kid}.p2.out")
        if (a["result"], a["nodes"]) != (2, ADOPTED_KEYS[kid]["nodes"]) or a["nodes"] != b["nodes"]:
            sys_exit(f"{kid}: adopted-row pass node disagreement")
        n1 += a["nodes"]; n2 += b["nodes"]
    if n1 != ADOPTED_TOTAL_NODES or n2 != ADOPTED_TOTAL_NODES:
        sys_exit(f"adopted packet node totals drift p1={n1} p2={n2} != {ADOPTED_TOTAL_NODES}")

    # --- emit increment + manifest ---------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = [
        "# n11 central-reply closure batch-33 (class 34908) 45-LOSS",
        "#   canonical-adoption increment (Part DT, 2026-11-24).",
        "# The published batch-33 kit (Parts DQ/DR/DS drive-1+2+3) probed",
        "#   ALL 54 of 54 keys honest two-pass fresh-cold at budget 15M:",
        "#   45 LOSS (adopted here), 4 probe-level WIN (af029/af047/",
        "#   af050/af053, pre-registered WIN-HALT markers, consumed",
        "#   NOWHERE by this Part - scrutiny-owner C++ gate 9193f5b6...),",
        "#   5 EXHAUSTED honest UNKNOWN (af003/af023/af034/af039/af048),",
        "#   MISMATCH 0, 3 pinned P2-TRUNCATED-RETRY markers each resolved",
        "#   by a completed retry.  ONLY the 45 fresh LOSS rows are",
        "#   consumed into the canonical cache by this increment.",
        "# 2-pass node-exact exact-S5 verdicts, fresh cold, pinned",
        "#   jsreplay.js sha256",
        "#   845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# gates: kit MANIFEST sha-verified file-by-file (186 files);",
        "#   54 two-pass fresh-cold raw re-verification with",
        "#   '# replay_done' on both passes; (budget,result,nodes)",
        "#   agreement with the 66-line honest-history status pins;",
        "#   raw/batch-keys agreement on (legal,lo,hi) and",
        "#   (s5_index, membership_class_count); raw inventory == 108",
        "#   primaries + exactly the 3 pinned truncated-retry sidecars;",
        "#   val-gate node-exact across the two published host outputs",
        "#   per molecule; adopted keys distinct, absent from BASE",
        "#   1ded9a08... (6,502 rows, WIN 158 / LOSS 6,344) and from",
        "#   the quarantine registry; derived WIN/EXHAUSTED sets equal",
        "#   the pinned marker sets; adopted per-pass node total",
        "#   281411183 (all-54 total 383609606).",
        "# Loss-only adoption asserts no root verdict; any class-34908",
        "#   scheduling effect is derived only by the reaudit refresh",
        "#   (Board fail-closed child verification) and the delta",
        "#   extractor, never by this maker.  11x11 stays UNKNOWN;",
        "#   nodes are bookkeeping, never verdicts.",
    ]
    rows_for_sort = [(ADOPTED_KEYS[k]["key"][0], ADOPTED_KEYS[k]["key"][1], ADOPTED_KEYS[k]["nodes"]) for k in ADOPTED_LOSS_IDS]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_path = OUT / "increment-b33loss45-20261124.cache"
    incr_path.write_bytes(blob)
    incr_sha = hashlib.sha256(blob).hexdigest()

    win_rows = []
    for kid in WIN_IDS:
        e = by_id[kid]
        win_rows.append({"key_id": kid, "s5_index": int(e["s5_index"]),
                         "verdict": "WIN", "nodes": raws15[kid]["nodes"],
                         "status": "probe-level WIN, consumed NOWHERE (scrutiny-owner C++ gate 9193f5b6...)"})
    exh_rows = []
    for kid in EXH_IDS:
        e = by_id[kid]
        exh_rows.append({"key_id": kid, "s5_index": int(e["s5_index"]),
                         "verdict": "EXHAUSTED", "nodes": raws15[kid]["nodes"],
                         "status": "honest UNKNOWN at budget 15M; high-budget reprobe is a separate declaration condition"})

    manifest = {
        "schema": "b33loss45-increments-manifest-v1",
        "batches": [{
            "batch": 33,
            "class_index": 34908,
            "keys_total": 54,
            "adopted_loss_ids": list(ADOPTED_LOSS_IDS),
            "already_adopted_ids": [],
            "unadopted_win_ids": list(WIN_IDS),
            "exhausted_excluded_ids": list(EXH_IDS),
            "probed_ids": list(PROBED_IDS),
            "fragment_ids": [],
            "fileless_unprobed_count": 0,
            "fileless_unprobed_ids": [],
            "input_sha256": KIT1_KEYS_SHA,
            "status_log_sha256": KIT1_STATUS_SHA,
            "status_log_lines": KIT1_STATUS_LINES,
            "status_log_first_line": KIT1_STATUS_FIRST_LINE,
            "status_log_final_line": KIT1_STATUS_FINAL_LINE,
            "status_log_win_halt_lines": list(WIN_HALT_LINES),
            "status_log_exhausted_lines": list(EXHAUSTED_LINES),
            "status_log_mismatch_lines": [],
            "status_log_retry_lines": list(RETRY_LINES),
            "kit_integrity": {"kit_manifest_sha256": KIT1_MANIFEST_SHA, "kit_files_verified": k1},
            "val_gate_multi_host_node_exact": True,
            "total_nodes_pass_one": n1,
            "total_nodes_pass_two": n2,
            "stop_rule": "batch-33 probe-complete (54/54 keys carry honest two-pass labels: 45 LOSS @15M adopted + 4 probe-level WIN unconsumed pending the scrutiny-owner C++ gate + 5 EXHAUSTED honest UNKNOWN; verdict not consumed)",
            "fragment_state": {},
        }],
        "resolved_ids": list(ADOPTED_LOSS_IDS),
        "loss_ids": list(ADOPTED_LOSS_IDS),
        "win_ids": list(WIN_IDS),
        "unadopted_win_ids": list(WIN_IDS),
        "unadopted_win_rows": win_rows,
        "exhausted_excluded_ids": list(EXH_IDS),
        "exhausted_rows": exh_rows,
        "row_counts": {"probed_rows": 54, "adopted_loss_rows": 45, "prior_adopted_loss_rows": 0,
                        "wins": 4, "exhausted_excluded": 5, "fragments_unprobed": 0, "fileless_unprobed": 0},
        "sha256": {"loss": incr_sha},
        "full_packet_eq_loss_only": False,
        "win_scenario_exists": True,
        "win_scenario_note": "exactly four probe-level WIN rows exist (af029/af047/af050/af053, each carrying its pre-registered WIN-HALT marker) and each stays unconsumed by this adoption (scrutiny owner C++ second-implementation gate pin 9193f5b6...); loss-only adoption NEVER frees class 34908 while any of the four WIN children plus the five EXHAUSTED children remain verdict-unconsumed/unknown",
        "full_packet_eq_loss_only_rationale":
            "the batch is probe-complete (54/54 honest labels) but the packet is NOT loss-only: "
            "four probe-level WIN rows and five EXHAUSTED rows stay UNCONSUMED and are NOT adopted; "
            "the adopted packet is the 45 fresh LOSS rows plus nothing else; no batch-33 row was "
            "adopted before; class 34908 is NOT freed (nine verdict-pending/unknown children remain)",
        "fragment_rows_note":
            "batch-33 is probe-complete with NO fragment keys: the raw inventory is exactly the "
            "54 x {p1,p2} primary pairs plus the three pinned truncated-retry sidecars "
            "(af008.p2.truncated.171704.out / af039.p2.truncated.180716.out / "
            "af048.p2.truncated.183215.out), which are retry artifacts, never verdict rows",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "base_cache_prior_adoption_confirmed": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 45-LOSS adoption increment: only the 45 fresh LOSS rows are consumed into "
            "the canonical cache via the fail-closed union merger; the four probe-level WINs are "
            "consumed NOWHERE (no verdict claim, no exclusion claim) and belong to the scrutiny "
            "owner; the five EXHAUSTED rows stay honest UNKNOWN; all 54 batch-33 keys stay UNKNOWN "
            "as verdicts; adopting 45 LOSS rows does NOT free class 34908 (four unconsumed WIN "
            "children plus five EXHAUSTED children remain); class 34908 stays unknown as a class; "
            "loss-only adoption asserts no root verdict and no coverage claim; any scheduling "
            "effect is derived only by the reaudit refresh (Board fail-closed child verification); "
            "11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INCREMENT rows=45 loss_nodes={ADOPTED_TOTAL_NODES} -> {incr_path}")


if __name__ == "__main__":
    main()
