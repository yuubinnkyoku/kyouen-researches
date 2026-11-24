#!/usr/bin/env python3
"""Build the batch-32 (class 8730) 54-LOSS canonical-adoption increment, fail-closed.

Prepared for the Part DP adoption (declared 2026-11-24, publish-then-execute):
the published batch-32 cumulative evidence is byte-pinned through the single
batch-32 kit (Part DM drive-1, MANIFEST
7c2c159ae24bab8836e23a8e2502615d62650eb4fb555979513ca55f71e7dec8, 193 kit files
+ MANIFEST: input 55 + output/raw 108 + output/status.log 1 + scripts 4 +
val-gate 24 + README 1).  Every kit file is sha256-verified here file-by-file.
jsreplay.js 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df is
the pinned solver image shared with the earlier kits and val-gates.

The batch is FULLY probed: all 54 of 54 keys carry honest two-pass fresh-cold
labels, resolved LOSS at budget 15M (the drive honest-label result=2 for every
key; WIN 0 / EXHAUSTED 0 / MISMATCH 0 / TRUNCATED 0).  All 54 LOSS rows ARE
adopted here.  There is NO unconsumed WIN row in this batch (the batch-30/31
era WIN rows belong to other classes and are not touched here), so the adopted
packet is loss-only; still, loss-only adoption does NOT by itself assert any
root verdict, and the class-8730 freedom effect is derived only later by the
reaudit refresh + delta extractor (Board fail-closed child verification), not
by this maker.

The adoption base is the canonical exact-S5 verdict chain head = the Part DN
merged 6,448-row cache sha256 7bdfa2366ef9c24b48a610d078104227555dd52ec18a566082cef2f906aab0f7
(BASE through the Part DN b30loss43 adoption), byte-pinned here; this maker
ABORTS against anything else.  Every adopted key is asserted fresh (absent
from the BASE) and absent from the quarantine registry (81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9).

The drive status.log is CLEAN HISTORY (54 lines = exactly 54 PASS rows, one
per key, no WIN-HALT / EXHAUSTED / MISMATCH / TRUNCATED-RETRY rows): the
drive's per-key honest labels are (15000000, 2, nodes) for all 54 keys.

Fail-closed gates: kit MANIFEST sha-verified file-by-file (193 files); 54
two-pass fresh-cold raw re-verification with '# replay_done' on both passes and
(budget,result,nodes) agreement with the status log row-by-row; raw/batch-keys
agreement on (legal, lo, hi) and pins on (s5_index, membership_class_count);
val-gate node-exact across the five published host outputs per gate molecule
(4 molecules x published-baseline + b32-host + b32-host2 + b32-host3 +
b32-host4); the 54 adopted keys distinct, ABSENT from the canonical BASE
(6,448 rows) and from the quarantine registry; adopted-row per-pass node total
223769637 on both passes.  Verdicts are byte-taken from the raws.  The 54 LOSS
rows ARE the only thing consumed into the canonical cache by this Part; 11x11
stays UNKNOWN; nodes are bookkeeping, never verdicts.
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
KIT1_DIR = ROOT / "research/experiments/n11-centralreply-closure-class8730-batch32-20261124"
KIT1_RAW = KIT1_DIR / "output/raw"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class34269-b30loss43-adoption-reaudit-20261124/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-20261124.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
MERGER = EXP / "scripts/s5_union_merge.py"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "7bdfa2366ef9c24b48a610d078104227555dd52ec18a566082cef2f906aab0f7"
BASE_CACHE_ROWS_EXPECTED = 6448
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6290
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

# --- published kit pins -------------------------------------------------------
KIT1_MANIFEST_SHA = "7c2c159ae24bab8836e23a8e2502615d62650eb4fb555979513ca55f71e7dec8"
KIT1_FILES = 193
KIT1_KEYS_SHA = "f46e663f1676111ae67f5686f4a7807a8c1f7e4e1d9910ddb96ba61bcb5e705d"
KIT1_STATUS_SHA = "a78135d79438e5cf0d6f95378c1b68f9ca1aa06ef564d141cf03e4b93a32eed4"

# --- status.log clean-history pins ----------------------------------------------
KIT1_STATUS_LINES = 54
KIT1_STATUS_FIRST_LINE = "2026-11-24T13:34:29Z ae002 PASS 15000000,2,3127842"
KIT1_STATUS_FINAL_LINE = "2026-11-24T14:48:51Z ae054 PASS 15000000,2,5136752"
BUDGET_KIT1 = 15000000

# --- adopted packet ------------------------------------------------------------
ADOPTED_LOSS_IDS = [f"ae{i:03d}" for i in range(1, 55)]
PROBED_IDS = list(ADOPTED_LOSS_IDS)
ADOPTED_KEYS = {
    'ae001': {'key': (6052837899320164384, 0), 'legal': 96, 'nodes': 3729310, 's5': 30596, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae002': {'key': (10412322613358493696, 262144), 'legal': 94, 'nodes': 3127842, 's5': 102313, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae003': {'key': (6052837899185946657, 0), 'legal': 98, 'nodes': 5421696, 's5': 227811, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae004': {'key': (1188950576503718912, 262144), 'legal': 100, 'nodes': 2403926, 's5': 227869, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae005': {'key': (6052837899185948704, 0), 'legal': 103, 'nodes': 4773521, 's5': 233201, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae006': {'key': (1188950576503718400, 262144), 'legal': 104, 'nodes': 4450622, 's5': 233301, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae007': {'key': (6052837899190140960, 0), 'legal': 97, 'nodes': 4181208, 's5': 238388, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae008': {'key': (1188950576503718144, 262144), 'legal': 102, 'nodes': 4607542, 's5': 238453, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae009': {'key': (6052837907775881248, 0), 'legal': 103, 'nodes': 5025299, 's5': 243426, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae010': {'key': (6052837899185946656, 8192), 'legal': 104, 'nodes': 5719747, 's5': 243470, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae011': {'key': (6052855491371991072, 0), 'legal': 103, 'nodes': 3272592, 's5': 248258, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae012': {'key': (6052837899185946656, 4), 'legal': 104, 'nodes': 5664027, 's5': 248342, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae013': {'key': (6052838174063853600, 0), 'legal': 96, 'nodes': 2768066, 's5': 251425, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae014': {'key': (6052837899185946658, 0), 'legal': 105, 'nodes': 5741083, 's5': 255023, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae015': {'key': (1188950576505815040, 262144), 'legal': 104, 'nodes': 5040670, 's5': 255105, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae016': {'key': (6052837899185950752, 0), 'legal': 96, 'nodes': 2925237, 's5': 259174, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae017': {'key': (1188950576504766464, 262144), 'legal': 100, 'nodes': 5830686, 's5': 259246, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae018': {'key': (6052837899194335264, 0), 'legal': 101, 'nodes': 3637481, 's5': 263258, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae019': {'key': (1188950576504242176, 262144), 'legal': 102, 'nodes': 2693629, 's5': 263323, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae020': {'key': (6052837916365815840, 0), 'legal': 100, 'nodes': 3970119, 's5': 267197, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae021': {'key': (6052837899185946656, 16384), 'legal': 102, 'nodes': 2790531, 's5': 267253, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae022': {'key': (6052873083558035488, 0), 'legal': 98, 'nodes': 4730974, 's5': 270978, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae023': {'key': (6052837899185946656, 8), 'legal': 104, 'nodes': 4311795, 's5': 271035, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae024': {'key': (6052837899185946660, 0), 'legal': 91, 'nodes': 3956699, 's5': 276288, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae025': {'key': (1188950580798685184, 262144), 'legal': 99, 'nodes': 4984219, 's5': 276352, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae026': {'key': (6052837899185954848, 0), 'legal': 102, 'nodes': 4035462, 's5': 279610, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae027': {'key': (1188950578651201536, 262144), 'legal': 101, 'nodes': 3532465, 's5': 279678, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae028': {'key': (6052837899202723872, 0), 'legal': 93, 'nodes': 4463589, 's5': 282568, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae029': {'key': (1188950577577459712, 262144), 'legal': 97, 'nodes': 5059660, 's5': 282635, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae030': {'key': (6052837933545685024, 0), 'legal': 98, 'nodes': 3031657, 's5': 285488, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae031': {'key': (6052837899185946656, 32768), 'legal': 99, 'nodes': 6305981, 's5': 285539, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae032': {'key': (6052908267930124320, 0), 'legal': 95, 'nodes': 1981997, 's5': 288280, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae033': {'key': (6052837899185946656, 16), 'legal': 93, 'nodes': 2296664, 's5': 288347, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae034': {'key': (1188959372596740096, 262144), 'legal': 103, 'nodes': 8966840, 's5': 290817, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae035': {'key': (6052837899185963040, 0), 'legal': 93, 'nodes': 3205767, 's5': 293375, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae036': {'key': (1188954974550228992, 262144), 'legal': 97, 'nodes': 4713799, 's5': 293452, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae037': {'key': (6052837899219501088, 0), 'legal': 92, 'nodes': 3974706, 's5': 295673, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae038': {'key': (1188952775526973440, 262144), 'legal': 101, 'nodes': 3176793, 's5': 295743, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae039': {'key': (6052837967905423392, 0), 'legal': 92, 'nodes': 3910081, 's5': 297981, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae040': {'key': (6052837899185946656, 65536), 'legal': 97, 'nodes': 2667008, 's5': 298037, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae041': {'key': (6052978636674301984, 0), 'legal': 100, 'nodes': 3458396, 's5': 300134, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae042': {'key': (6052837899185946656, 32), 'legal': 99, 'nodes': 1706977, 's5': 300216, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae043': {'key': (6052837899185946672, 0), 'legal': 100, 'nodes': 5406352, 's5': 302188, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae044': {'key': (1206964975013199872, 262144), 'legal': 104, 'nodes': 3917841, 's5': 302257, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae045': {'key': (6052837899185979424, 0), 'legal': 99, 'nodes': 3360772, 's5': 304124, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae046': {'key': (1197957775758458880, 262144), 'legal': 104, 'nodes': 3905480, 's5': 304196, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae047': {'key': (6052837899253055520, 0), 'legal': 91, 'nodes': 3632700, 's5': 305925, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae048': {'key': (1193454176131088384, 262144), 'legal': 96, 'nodes': 3475879, 's5': 305986, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae049': {'key': (6052838036624900128, 0), 'legal': 100, 'nodes': 4405745, 's5': 307575, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae050': {'key': (6052837899185946656, 131072), 'legal': 102, 'nodes': 4670080, 's5': 307627, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae051': {'key': (6053119374162657312, 0), 'legal': 91, 'nodes': 6473086, 's5': 309085, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae052': {'key': (6052837899185946656, 64), 'legal': 94, 'nodes': 5156590, 's5': 309139, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae053': {'key': (5800636594931105792, 262144), 'legal': 88, 'nodes': 1981997, 's5': 311698, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'ae054': {'key': (1188950576503717888, 262146), 'legal': 96, 'nodes': 5136752, 's5': 311727, 'mcc': 2, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
}
ADOPTED_TOTAL_NODES = 223769637

# --- val-gate pins ---------------------------------------------------------------
VAL_GATES = {
    "at2m-s5-1152921504606851072-536870946": (2000000, 0, 2000000),
    "at2m-s5-1188950301626860544-536870912": (2000000, 0, 2000000),
    "first-15m-s5-1152921504606851072-536870946": (15000000, 2, 3651923),
    "second-15m-s5-1188950301626860544-536870912": (15000000, 2, 5040200),
}
VAL_HOSTS = ["published-baseline", "b32-host", "b32-host2", "b32-host3", "b32-host4"]


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


def parse_status1(path: Path):
    lines = path.read_text().splitlines()
    if len(lines) != KIT1_STATUS_LINES:
        sys_exit(f"kit status lines {len(lines)} != {KIT1_STATUS_LINES}")
    if lines[0] != KIT1_STATUS_FIRST_LINE or lines[-1] != KIT1_STATUS_FINAL_LINE:
        sys_exit("kit status first/final line drift")
    got_pass = {}
    for line in lines:
        m = re.match(r"^(\S+) (ae\d{3}) PASS (\d+),(\d+),(\d+)$", line)
        if not m:
            sys_exit(f"kit status line is not a clean PASS row: {line!r}")
        kid = m.group(2)
        if kid in got_pass:
            sys_exit(f"kit status duplicate PASS row for {kid}")
        got_pass[kid] = [(int(m.group(3)), int(m.group(4)), int(m.group(5)))]
    if set(got_pass) != set(PROBED_IDS):
        sys_exit("kit status PASS keys != the 54 probed keys")
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
    if bk_all["schema"] != "n11-centralreply-closure-class8730-batch32-input-v1":
        sys_exit("batch-keys schema drift")
    if bk_all["class_index"] != 8730 or bk_all["budget"] != BUDGET_KIT1:
        sys_exit("batch-keys class/budget drift")
    if len(bk_all["keys"]) != 54:
        sys_exit("batch-keys key count != 54")
    if bk_all["closure_class_rank_in_published_base"] != 30:
        sys_exit("batch-keys closure rank drift (kit frozen at selection)")
    if int(bk_all["published_base_canonical_rows"]) != 6405:
        sys_exit("batch-keys published_base_canonical_rows drift (kit frozen at selection)")
    if bk_all["class_mask"] != ["6052837899185946656", "0"]:
        sys_exit("batch-keys class mask drift")
    if bk_all["groups_served_count"] != 4 or len(bk_all["groups_served_full"]) != 4:
        sys_exit("batch-keys groups_served drift")
    if [tuple(g.items()) for g in bk_all["groups_served_full"]] != [
            (("first", 5), ("third", 58)), (("first", 5), ("third", 62)),
            (("first", 38), ("third", 55)), (("first", 38), ("third", 65))]:
        sys_exit("batch-keys groups_served_full drift")
    by_id = {k["key_id"]: k for k in bk_all["keys"]}

    # --- status log --------------------------------------------------------------
    got_pass = parse_status1(KIT1_DIR / "output/status.log")
    for kid in PROBED_IDS:
        triple = got_pass[kid][0]
        if triple[0] != BUDGET_KIT1 or triple[1] != 2:
            sys_exit(f"{kid}: status honest-label drift {triple}")

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
        if (ref["budget"], ref["result"], ref["nodes"]) not in got_pass[kid]:
            sys_exit(f"{kid}: raw (budget,result,nodes) row not pinned in status")
        raws15[kid] = ref
    loss_set = sorted(kid for kid in PROBED_IDS if raws15[kid]["result"] == 2)
    win_set = sorted(kid for kid in PROBED_IDS if raws15[kid]["result"] == 1)
    exh_set = sorted(kid for kid in PROBED_IDS if raws15[kid]["result"] == 0)
    if loss_set != sorted(ADOPTED_LOSS_IDS):
        sys_exit("decisive LOSS set != the 54 adopted candidates")
    if win_set or exh_set:
        sys_exit(f"batch-32 must be loss-only: WIN={win_set} EXHAUSTED={exh_set}")

    # --- raw inventory: primaries only, no sidecars ---------------------------
    prim1 = sorted(p.name for p in KIT1_RAW.iterdir() if p.is_file())
    exp1 = sorted(f"{kid}.{tag}.out" for kid in PROBED_IDS for tag in ("p1", "p2"))
    if prim1 != exp1:
        sys_exit(f"kit raw inventory drift: {sorted(set(prim1) ^ set(exp1))}")

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
        "# n11 central-reply closure batch-32 (class 8730) 54-LOSS",
        "#   canonical-adoption increment (Part DP, 2026-11-24)",
        "# published batch-32 kit (Part DM drive-1): ALL 54 of 54 keys",
        "#   carry honest two-pass fresh-cold probe labels at budget",
        "#   15M, every one resolved LOSS (status.log 54 PASS rows,",
        "#   WIN 0 / EXHAUSTED 0 / MISMATCH 0 / TRUNCATED 0) and every",
        "#   one IS this increment.  There is no unconsumed WIN row in",
        "#   this batch; the adopted packet is loss-only.  Loss-only",
        "#   adoption asserts no root verdict; the class-8730 freedom",
        "#   effect, if any, is derived only by the reaudit refresh",
        "#   (Board fail-closed child verification) and the delta",
        "#   extractor, never by this maker.",
        "# 2-pass node-exact exact-S5 verdicts, fresh cold, pinned",
        "#   jsreplay.js sha256",
        "#   845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# gates: kit MANIFEST sha-verified file-by-file (193 files);",
        "#   54 two-pass fresh-cold raw re-verification with",
        "#   '# replay_done' on both passes; (budget,result,nodes)",
        "#   agreement with the 54-line clean-history status pins;",
        "#   raw/batch-keys agreement on (legal,lo,hi) and",
        "#   (s5_index, membership_class_count); val-gate node-exact",
        "#   across the five published host outputs per molecule;",
        "#   adopted keys distinct, absent from BASE 7bdfa236...",
        "#   (6,448 rows, WIN 158 / LOSS 6,290) and from the",
        "#   quarantine registry; adopted per-pass node total {}".format(ADOPTED_TOTAL_NODES) + ",",
        "# ADOPTED set = the 54 decisive-LOSS keys; the packet is",
        "#   loss-only (54 == all probed keys).",
        "# The 54 LOSS rows ARE consumed into the canonical cache by",
        "#   the fail-closed union merger; 11x11 stays UNKNOWN; nodes",
        "#   are bookkeeping, never verdicts.",
    ]
    rows_for_sort = [(ADOPTED_KEYS[k]["key"][0], ADOPTED_KEYS[k]["key"][1], ADOPTED_KEYS[k]["nodes"]) for k in ADOPTED_LOSS_IDS]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_path = OUT / "increment-b32loss54-20261124.cache"
    incr_path.write_bytes(blob)
    incr_sha = hashlib.sha256(blob).hexdigest()

    manifest = {
        "schema": "b32loss54-increments-manifest-v1",
        "batches": [{
            "batch": 32,
            "class_index": 8730,
            "keys_total": 54,
            "adopted_loss_ids": list(ADOPTED_LOSS_IDS),
            "already_adopted_ids": [],
            "unadopted_win_ids": [],
            "exhausted_excluded_ids": [],
            "probed_ids": list(PROBED_IDS),
            "fragment_ids": [],
            "fileless_unprobed_count": 0,
            "fileless_unprobed_ids": [],
            "input_sha256": KIT1_KEYS_SHA,
            "status_log_sha256": KIT1_STATUS_SHA,
            "status_log_lines": KIT1_STATUS_LINES,
            "status_log_first_line": KIT1_STATUS_FIRST_LINE,
            "status_log_final_line": KIT1_STATUS_FINAL_LINE,
            "status_log_win_halt_lines": [],
            "status_log_exhausted_lines": [],
            "status_log_mismatch_lines": [],
            "status_log_retry_lines": [],
            "kit_integrity": {"kit_manifest_sha256": KIT1_MANIFEST_SHA, "kit_files_verified": k1},
            "val_gate_multi_host_node_exact": True,
            "total_nodes_pass_one": n1,
            "total_nodes_pass_two": n2,
            "stop_rule": "batch-32 probe-complete (54/54 keys carry honest two-pass labels, all LOSS at budget 15M; no WIN row exists in this batch; verdict not consumed)",
            "fragment_state": {},
        }],
        "resolved_ids": list(ADOPTED_LOSS_IDS),
        "loss_ids": list(ADOPTED_LOSS_IDS),
        "win_ids": [],
        "unadopted_win_ids": [],
        "exhausted_excluded_ids": [],
        "row_counts": {"probed_rows": 54, "adopted_loss_rows": 54, "prior_adopted_loss_rows": 0,
                        "wins": 0, "exhausted_excluded": 0, "fragments_unprobed": 0, "fileless_unprobed": 0},
        "sha256": {"loss": incr_sha},
        "full_packet_eq_loss_only": True,
        "win_scenario_exists": False,
        "full_packet_eq_loss_only_rationale":
            "the batch is probe-complete (54/54 honest labels) and every label is LOSS; 54 == all probed keys "
            "so the packet is loss-only",
        "fragment_rows_note":
            "batch-32 is probe-complete with NO fragment keys and NO sidecar retry artifacts: the raw "
            "inventory is exactly the 54 x {p1,p2} primary pairs",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "base_cache_prior_adoption_confirmed": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 54-LOSS adoption increment: only the 54 fresh LOSS rows are consumed into "
            "the canonical cache via the fail-closed union merger; all 54 batch-32 keys stay UNKNOWN "
            "as verdicts; loss-only adoption asserts no root verdict and no coverage claim; any "
            "class-8730 freedom effect is derived only by the reaudit refresh (Board fail-closed "
            "child verification); 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INCREMENT rows=54 loss_nodes={ADOPTED_TOTAL_NODES} -> {incr_path}")


if __name__ == "__main__":
    main()
