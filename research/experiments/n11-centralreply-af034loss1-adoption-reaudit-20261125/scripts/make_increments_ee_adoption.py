"""Build the af034loss1 (Part ED af034 60M-resolved) canonical-adoption
increment, fail-closed.

Part EE (2026-11-25).  BASE = the published Part EC canonical merged cache
(6,665 rows, sha cecc1a0f...; WIN 158 / LOSS 6,507).  The single adopted
pool is the published Part ED af034 60M reprobe kit (class 34908,
2026-11-25, 36 files, MANIFEST rev2 1dfe02ca...): exactly the 1 fresh LOSS
row af034 (s5 930660), resolved at the pre-declared higher budget condition
60,000,000 where the key was published EXHAUSTED (honest UNKNOWN) at 15M
(batch-33 status 1f66...) and again at 30M (Part EA status db7c7017...);
budget-condition ladder 15M -> 30M -> 60M, one fresh declared condition
upgrade per Part.  The Part ED packet is exactly this single key: loss-only,
no probe-level WIN row, no still-EXHAUSTED row (full packet == adopted rows).
No WIN verdict is consumed; no root verdict is asserted; 11x11 stays UNKNOWN.

Every gate is fail-closed: any drift aborts with rc=1 and no output is
written.  The published Part ED kit is verified file-by-file (byte-pins
against the kit MANIFEST rev2), the adopted row is verified two-pass
fresh-cold node-exact at budget 60M against the published raw replay files
and the honest-history status log (5 lines), the anchors af001 / af039 /
af029 are re-verified against BASE canonical rows (af001 / af039 verbatim,
af029 absent), the published EXHAUSTED source raws of af034 at both the 15M
and 30M conditions are pinned, and the adopted key is proven absent from
BASE (fresh-increment gate) and from the quarantine registry.
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
MERGER = EXP / "scripts/s5_union_merge.py"

EC_EXP = "n11-centralreply-b33exh5loss2-adoption-reaudit-20261125"
ED_EXP = "n11-centralreply-closure-class34908-af034-reprobe60m-20261125"
BASE_CACHE = ROOT / "research/experiments" / EC_EXP / (
    "output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-"
    "plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-"
    "plus-b35loss26-plus-b4loss1-plus-b36loss40-plus-b37loss46-plus-b3loss3-"
    "plus-b33exh5loss2-20261125.cache")
ED_DIR = ROOT / "research/experiments" / ED_EXP
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "cecc1a0fae126d98d8e5f23e041657b86e4d7128f80cc1182f4f9830ed1e8626"
BASE_CACHE_ROWS_EXPECTED = 6665
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6507
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

ED_MANIFEST_SHA = "1dfe02cae61e9f410e24bbafe7386a0958da4deddd92456faad12b8f755546ac"
ED_KIT_FILES = 36
ED_STATUS_SHA = "26a97e0297c9db720c8c051db1498508bd24c038b1b3c37e69ac28fe65be226c"
ED_AUDIT_SHA = "5473eafb277867344dbba851110c4d671b1fc04f906f3c12b9dc75cf7b15a533"
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
RUNNER60M_SHA_EXPECTED = "b0c5f714f926a923d35692672fbfc6aaf2da0081cdf4217c074e0f64d3a29f92"
B33_STATUS_SHA = "1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52"
EA_STATUS_SHA = "db7c7017d7bfeef2d0c17c646b22f77b8bfd52a66796433b86e88444741c0438"
BUDGET = 60000000
BUDGET_30M = 30000000
BUDGET_15M = 15000000

# --- published Part ED 60M re-probe raw replay files (byte-pinned) ----------
ED_RAW_SHAS = {
    "af001.p1.out": "9124225f73963f40ace05e20b47ec1c5e6156fc82a7f677a2f4afded9f0c52e0",
    "af001.p2.out": "9124225f73963f40ace05e20b47ec1c5e6156fc82a7f677a2f4afded9f0c52e0",
    "af029.p1.out": "971a9b29888f0a86e48c4fde21f9a06255116d8917e5cb5e40bebbfcdee5472d",
    "af029.p2.out": "21c7b21853b67c99e5369434f4baf40831f32b590083cf09d70897a16739d457",
    "af034.p1.out": "63860f94341477e77429624891c7e9d39a5c122487aa85c1b6dbb59fa547a7ab",
    "af034.p2.out": "eb64725fa72a2ca66af1da74fcbf6a531fd279b90f151e76be08a94b7a6a9fdd",
    "af039.p1.out": "da227971f7fee97128920784cb12f24b343557b9cec762e68a602d187e9fff43",
    "af039.p2.out": "15abe72fafa95af72e56bfcbe090b423398cdcee87f829a10c5d82b6b16b94b9",
}

# --- published EXHAUSTED source raws of the adopted key (ladder pins) ------
ED_EXH30M_SHAS = {
    "af034.p1.out": "9ecfdc770c0b8a6eab027c097051ae2731ee15f1ede0babbc619e38acf2fca74",
    "af034.p2.out": "3978990d5821850476e7b38d1de98fbe7a56738cfd48a8b03cf8ed3350d1b290",
}

# --- published Part ED input rows (byte-pinned; 1 line each) --------------
ED_INPUT_CSV_SHAS = {
    "af001": "b2ef3588267694aff51b5ec7aa9940064c5199db2b5f00644a9ed27fca2a127b",
    "af029": "b5500b8d98cd3cbef56f6177245d8e3c21c31081f2252c6454f1aee73ce30c10",
    "af034": "a4bff56606cbb11107b77dac677b1e1151f59686174bddcf7e08c0558f590326",
    "af039": "e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691",
}

# --- status.log honest-history pins (5 lines) ------------------------------
ED_STATUS_LINES = 5
ED_STATUS_FIRST = "2026-11-25T05:07:10Z af001 PASS 60000000,2,2952432"
ED_STATUS_FINAL = "2026-11-25T05:18:47Z af034 PASS 60000000,2,32012059"
ED_STATUS_WIN_HALT_LINES = [
    "2026-11-25T05:07:58Z af029 WIN-HALT",
]
ED_STATUS_RETRY_LINES: list = []
ED_STATUS_EXHAUSTED_LINES: list = []

# --- adopted packet ----------------------------------------------------------
ADOPTED_IDS = ["af034"]
WIN_IDS_UNCONSUMED: list = []
EXHAUSTED_EXCLUDED_IDS: list = []
PACKET_IDS = ["af034"]
ANCHOR_IDS = ["af001", "af029", "af039"]

ADOPTED_NODES = 32012059
PACKET_NODES = 32012059

# --- pinned per-key fields (frozen at Part ED kit build; kit-crosschecked) -
KEY_PINS = {
    "af001": {"lo": 1152921504742113281, "hi": 68719476736, "legal": 91,
              "s5_index": 1176, "membership_class_count": 2},
    "af029": {"lo": 1152921504607895553, "hi": 68720525312, "legal": 86,
              "s5_index": 900646, "membership_class_count": 2},
    "af034": {"lo": 1152921504607911937, "hi": 68719476736, "legal": 95,
              "s5_index": 930660, "membership_class_count": 4},
    "af039": {"lo": 1152921504607895681, "hi": 68719476736, "legal": 89,
              "s5_index": 950512, "membership_class_count": 4},
}
LABEL_PINS = {
    "af001": (2, 2952432),      # node-exact vs the BASE (EB) canonical row
    "af029": (1, 4862485),      # unconsumed probe-level WIN: must sit in NO cache
    "af034": (2, 32012059),    # ADOPTED (fresh at BASE; ladder 15M/30M EXHAUSTED)
    "af039": (2, 19234232),    # node-exact vs the BASE (EC-adopted) canonical row
}
VALGATE_PINS = {
    "at2m-s5-1152921504606851072-536870946": (2000000, 0, 2000000),
    "at2m-s5-1188950301626860544-536870912": (2000000, 0, 2000000),
    "first-15m-s5-1152921504606851072-536870946": (15000000, 2, 3651923),
    "second-15m-s5-1188950301626860544-536870912": (15000000, 2, 5040200),
}

ADOPTED_TABLE_DIGEST = "aab6262a8cba4ecba4d82ccb197bb08c8a50dddb72931044a17b65f2f0ecf8dc"
ADOPTED_INCREMENT_SHA = "cc9c474627ec8f6fc98c0ebeb7600707021e8cd598b3be6799d39c104289e162"

INCREMENT_NAME = "increment-af034loss1-20261125.cache"
EE_SCHEMA = "af034loss1-increments-manifest-v1"


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


def two_pass(rawdir: Path, kid: str, shas: dict):
    variants = {}
    for tag in ("p1", "p2"):
        p = rawdir / f"{kid}.{tag}.out"
        if not p.is_file():
            sys_exit(f"missing raw {p}")
        psha = sha(p)
        if psha != shas[p.name]:
            sys_exit(f"raw {p.name} sha drift vs the pinned published bytes")
        txt = p.read_text()
        if "# replay_done" not in txt:
            sys_exit(f"raw {p} lacks the '# replay_done' completeness guard")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys_exit(f"{kid}: pass mismatch {tag} vs p1 (fresh two-pass node-exact gate)")
    return ref


def verify_kit(dirp: Path, manifest_sha: str, kit_files: int):
    if not dirp.is_dir():
        sys_exit(f"kit dir missing {dirp}")
    if sha(dirp / "MANIFEST-sha256.txt") != manifest_sha:
        sys_exit(f"kit {dirp.name} MANIFEST sha drift")
    verified = 0
    for line in (dirp / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) >= 4:    # 4-column: sha blobsha size relpath
            want, rel = fields[0], fields[3]
        elif len(fields) == 3:  # 3-column: sha blobsha relpath
            want, rel = fields[0], fields[2]
        else:                   # ED MANIFEST rev2: sha256 relpath
            want, rel = fields[0], fields[1]
        p = dirp / rel
        if not p.is_file():
            sys_exit(f"kit {dirp.name} file missing: {rel}")
        if sha(p) != want:
            sys_exit(f"kit {dirp.name} file sha drift: {rel}")
        verified += 1
    if verified != kit_files:
        sys_exit(f"kit {dirp.name} files verified {verified} != {kit_files}")
    return verified


def parse_status(path: Path):
    lines = path.read_text().splitlines()
    if len(lines) != ED_STATUS_LINES:
        sys_exit(f"{path.name} status lines {len(lines)} != {ED_STATUS_LINES}")
    if lines[0] != ED_STATUS_FIRST or lines[-1] != ED_STATUS_FINAL:
        sys_exit(f"{path.name} status first/final line drift")
    pat = re.compile(r"^(\S+) (af\d{3}) PASS (\d+),(\d+),(\d+)$")
    hw = re.compile(r"^(\S+) (af\d{3}) WIN-HALT$")
    rt = re.compile(r"^(\S+) (af\d{3}) P2-TRUNCATED-RETRY$")
    ex = re.compile(r"^(\S+) (af\d{3}) EXHAUSTED (\d+),(\d+),(\d+)$")
    got_pass, win_halt, retry, exh, others = {}, [], [], [], []
    for line in lines:
        m = pat.match(line)
        if m:
            kid = m.group(2)
            if kid in got_pass:
                sys_exit(f"{path.name} duplicate verdict row for {kid}")
            got_pass[kid] = (int(m.group(3)), int(m.group(4)), int(m.group(5)))
            continue
        if hw.match(line):
            win_halt.append(line)
            continue
        if rt.match(line):
            retry.append(line)
            continue
        if ex.match(line):
            exh.append(line)
            continue
        others.append(line)
    if others:
        sys_exit(f"{path.name} status has UNEXPECTED rows: {others[:3]}")
    if win_halt != ED_STATUS_WIN_HALT_LINES:
        sys_exit(f"{path.name} status WIN-HALT lines != pinned halt history: {win_halt}")
    if retry != ED_STATUS_RETRY_LINES:
        sys_exit(f"{path.name} status P2-TRUNCATED-RETRY lines != pinned (empty): {retry}")
    if exh != ED_STATUS_EXHAUSTED_LINES:
        sys_exit(f"{path.name} status EXHAUSTED lines != pinned (empty): {exh}")
    return got_pass


def main() -> None:
    # --- base cache, merger, quarantine anchors -------------------------------
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache (Part EC canonical) sha drift")
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

    # --- Part ED kit integrity (the published af034 60M reprobe kit) ---------
    ed_files = verify_kit(ED_DIR, ED_MANIFEST_SHA, ED_KIT_FILES)
    if sha(ED_DIR / "scripts/jsreplay.js") != JSREPLAY_SHA_EXPECTED:
        sys_exit("jsreplay.js sha drift in the Part ED kit (pinned solver image 8458...)")
    if sha(ED_DIR / "scripts/runbatch_af034-60m.sh") != RUNNER60M_SHA_EXPECTED:
        sys_exit("runbatch_af034-60m.sh sha drift in the Part ED kit (pinned 60M runner b0c5f714...)")
    if sha(ED_DIR / "output/status.log") != ED_STATUS_SHA:
        sys_exit("Part ED status.log sha drift")
    if sha(ED_DIR / "output/audit_ed.json") != ED_AUDIT_SHA:
        sys_exit("Part ED audit_ed.json sha drift")
    if sha(ED_DIR / "sources/b33-status.log") != B33_STATUS_SHA:
        sys_exit("published batch-33 honest-history status sha drift (source 1f66...)")
    if sha(ED_DIR / "sources/ea-status.log") != EA_STATUS_SHA:
        sys_exit("published Part EA honest-history status sha drift (source db7c7017...)")

    # --- input rows (no reprobe-keys/batch-keys registry in the ED kit; the
    #     published 1-line input csv per probed key is pinned byte-for-byte) --
    for kid, want_sha in ED_INPUT_CSV_SHAS.items():
        p = ED_DIR / "input" / f"{kid}.input.csv"
        if sha(p) != want_sha:
            sys_exit(f"input csv {kid} sha drift vs the pinned published bytes")
        e = KEY_PINS[kid]
        want_line = f"target,0,5,{e['lo']},{e['hi']},{e['legal']},0,0,0,0,0"
        lines = [l for l in p.read_text().splitlines() if l.strip()]
        if lines != [want_line]:
            sys_exit(f"input csv {kid} body drift: {lines}")

    # --- audit_ed.json honesty pins ------------------------------------------
    audit = json.loads((ED_DIR / "output/audit_ed.json").read_text())
    if audit["schema"] != "n11-ed-af034-reprobe60m-audit-v1" \
            or audit["gates_total"] != 58 or audit["gates_total"] != len(audit["gates"]) \
            or audit["gates_failed"] != [] or audit["all_gates_pass"] is not True:
        sys_exit("audit_ed.json header pin drift (58 gates / all pass / none failed)")
    if audit["verdict_consumed"] is not False:
        sys_exit("audit_ed.json verdict_consumed must be false (probe-time honesty)")
    mp = audit["main_probe_af034"]
    if mp["label"] != "LOSS" or (mp["result"], mp["nodes"]) != LABEL_PINS["af034"] \
            or mp["p1_wall_s"] != 176.0 or mp["p2_wall_s"] != 180.0:
        sys_exit("audit main_probe_af034 label/nodes/wall pin drift")
    for kid in ANCHOR_IDS:
        a = audit["anchors"].get(kid)
        if a is None or a["budget"] != BUDGET:
            sys_exit(f"audit anchor {kid} missing or budget drift")
        if (a["result"], a["nodes"]) != LABEL_PINS[kid]:
            sys_exit(f"audit anchor {kid} label drift")
    if sorted(audit["valgate"]) != sorted(VALGATE_PINS):
        sys_exit("audit valgate key set drift")
    for name, (b, r, n) in VALGATE_PINS.items():
        v = audit["valgate"][name]
        if (v["budget"], v["result"], v["nodes"]) != (b, r, n):
            sys_exit(f"audit valgate {name} (budget,result,nodes) pin drift")

    # --- status log (honest history, 5 lines) ---------------------------------
    st = parse_status(ED_DIR / "output/status.log")
    if sorted(st) != sorted(PACKET_IDS + ANCHOR_IDS):
        sys_exit("Part ED status verdict keys != the 4 targets+anchors keys")
    for kid, (r, n) in LABEL_PINS.items():
        if st[kid] != (BUDGET, r, n):
            sys_exit(f"{kid} status verdict vs pinned honest label drift")

    # --- two-pass raw verification (the target + 3 anchors) ------------------
    raws = {}
    for kid in PACKET_IDS + ANCHOR_IDS:
        ref = two_pass(ED_DIR / "output/raw", kid, ED_RAW_SHAS)
        if ref["stones"] != 5 or ref["is_or"] != 0:
            sys_exit(f"{kid}: wrong depth/or bit")
        if ref["budget"] != BUDGET:
            sys_exit(f"{kid}: budget drift (expected pre-declared 60M)")
        e = KEY_PINS[kid]
        if (ref["legal"] != int(e["legal"])
                or ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"])):
            sys_exit(f"{kid}: legal/key disagreement raw vs pinned key fields")
        if (ref["budget"], ref["result"], ref["nodes"]) != st[kid]:
            sys_exit(f"{kid}: raw (budget,result,nodes) row != status verdict row")
        raws[kid] = ref
    loss_set = sorted(k for k in PACKET_IDS if raws[k]["result"] == 2)
    win_set = sorted(k for k in PACKET_IDS if raws[k]["result"] == 1)
    exh_set = sorted(k for k in PACKET_IDS if raws[k]["result"] == 0)
    if loss_set != sorted(ADOPTED_IDS):
        sys_exit(f"60M decisive LOSS set != the adopted candidates: {loss_set}")
    if win_set != sorted(WIN_IDS_UNCONSUMED):
        sys_exit(f"60M probe-level WIN set != pinned (empty): {win_set}")
    if exh_set != sorted(EXHAUSTED_EXCLUDED_IDS):
        sys_exit(f"60M still-EXHAUSTED set != pinned (empty): {exh_set}")
    n = sum(raws[k]["nodes"] for k in ADOPTED_IDS)
    if n != ADOPTED_NODES:
        sys_exit(f"adopted node total drift {n} != {ADOPTED_NODES}")
    p = sum(raws[k]["nodes"] for k in PACKET_IDS)
    if p != PACKET_NODES:
        sys_exit(f"whole-packet node total drift {p} != {PACKET_NODES}")

    # --- EXHAUSTED source raws of the adopted key (condition ladder) --------
    for kid in ADOPTED_IDS:
        ref30 = two_pass(ED_DIR / "sources/exh30m", kid, ED_EXH30M_SHAS)
        if ref30["budget"] != BUDGET_30M or ref30["result"] != 0 \
                or ref30["nodes"] != BUDGET_30M:
            sys_exit(f"{kid}: 30M source raw must be the published EXHAUSTED honest-UNKNOWN run")
        if (ref30["lo"], ref30["hi"], ref30["legal"]) != (raws[kid]["lo"], raws[kid]["hi"], raws[kid]["legal"]):
            sys_exit(f"{kid}: 30M source raw key/legal disagreement vs the 60M raw")

    # --- b33-status.log (15M rung) and ea-status.log (30M rung) --------------
    b33_lines = (ED_DIR / "sources/b33-status.log").read_text().splitlines()
    if len(b33_lines) != 66:
        sys_exit(f"b33-status lines {len(b33_lines)} != 66")
    for kid in PACKET_IDS:
        pair = [l for l in b33_lines
                if (f" {kid} PASS {BUDGET_15M},0,{BUDGET_15M}" in l)
                or (f" {kid} EXHAUSTED {BUDGET_15M},0,{BUDGET_15M}" in l)]
        if len(pair) != 2:
            sys_exit(f"b33-status EXHAUSTED pair for {kid} not found (15M honest history)")
    ea_lines = (ED_DIR / "sources/ea-status.log").read_text().splitlines()
    if len(ea_lines) != 13:
        sys_exit(f"ea-status lines {len(ea_lines)} != 13")
    for kid in PACKET_IDS:
        pair = [l for l in ea_lines
                if (f" {kid} PASS {BUDGET_30M},0,{BUDGET_30M}" in l)
                or (f" {kid} EXHAUSTED {BUDGET_30M},0,{BUDGET_30M}" in l)]
        if len(pair) != 2:
            sys_exit(f"ea-status EXHAUSTED pair for {kid} not found (30M honest history)")

    adopted_rows = [(int(raws[k]["lo"]), int(raws[k]["hi"]), int(raws[k]["legal"]),
                     raws[k]["result"], raws[k]["nodes"]) for k in ADOPTED_IDS]
    if len(adopted_rows) != 1 or any(r[3] != 2 for r in adopted_rows):
        sys_exit("adopted rows must be exactly the 1 fresh exact-LOSS row")
    digest = hashlib.sha256("\n".join(
        f"{lo},{hi},{legal},{result},{nodes}"
        for lo, hi, legal, result, nodes in sorted(adopted_rows)).encode()).hexdigest()
    if digest != ADOPTED_TABLE_DIGEST:
        sys_exit(f"adopted-table digest drift {digest}")

    # --- freshness: BASE / quarantine / anchors ------------------------------
    emitted = set()
    for kid in PACKET_IDS:
        key = (int(raws[kid]["lo"]), int(raws[kid]["hi"]))
        if key in emitted:
            sys_exit(f"{kid}: duplicate key across the probed packet")
        emitted.add(key)
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE {key}; fresh-increment gate")
    for kid in ANCHOR_IDS:
        key = (int(raws[kid]["lo"]), int(raws[kid]["hi"]))
        if key in quarantined:
            sys_exit(f"{kid}: quarantined anchor key {key}")
    # anchor identity gates: af001 is the published b33 exact-LOSS row adopted
    # into BASE at Part EB (node-exact reproduction expected); af039 is the
    # b33exh5 30M-resolved exact-LOSS row adopted into BASE at Part EC
    # (node-exact reproduction expected); af029 is the unconsumed b33
    # probe-level WIN (must sit in NO cache).
    key_af001 = (int(raws["af001"]["lo"]), int(raws["af001"]["hi"]))
    if base_keys.get(key_af001) != (2, 2952432):
        sys_exit(f"af001 anchor must reproduce the published BASE row verbatim: {base_keys.get(key_af001)}")
    key_af039 = (int(raws["af039"]["lo"]), int(raws["af039"]["hi"]))
    if base_keys.get(key_af039) != (2, 19234232):
        sys_exit(f"af039 anchor must reproduce the published BASE row verbatim: {base_keys.get(key_af039)}")
    key_af029 = (int(raws["af029"]["lo"]), int(raws["af029"]["hi"]))
    if key_af029 in base_keys:
        sys_exit("af029 anchor is an unconsumed probe-level WIN: must sit in NO cache")

    # --- emit increment + manifest --------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = HDR_LINES
    rows_for_sort = [(lo, hi, nodes) for lo, hi, legal, result, nodes in adopted_rows]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_sha = hashlib.sha256(blob).hexdigest()
    if incr_sha != ADOPTED_INCREMENT_SHA:
        sys_exit(f"emitted increment sha drift {incr_sha} != pinned {ADOPTED_INCREMENT_SHA}")
    incr_path = OUT / INCREMENT_NAME
    incr_path.write_bytes(blob)

    adopted_table = [
        {"lo": lo, "hi": hi, "legal": legal, "result": 2, "nodes": nodes}
        for lo, hi, legal, result, nodes in sorted(adopted_rows)]

    manifest = {
        "schema": EE_SCHEMA,
        "batches": [
            {"pool": "af034loss1",
             "adopted_loss_ids": list(ADOPTED_IDS),
             "probed_ids": list(PACKET_IDS),
             "anchor_ids": list(ANCHOR_IDS),
             "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
             "exhausted_excluded_ids": list(EXHAUSTED_EXCLUDED_IDS),
             "adopted_nodes_per_pool": ADOPTED_NODES,
             "whole_packet_nodes": PACKET_NODES,
             "target_input_sha256": ED_INPUT_CSV_SHAS["af034"],
             "anchor_input_sha256": {k: v for k, v in ED_INPUT_CSV_SHAS.items()
                                     if k in ANCHOR_IDS},
             "status_log_sha256": ED_STATUS_SHA,
             "status_log_lines": ED_STATUS_LINES,
             "status_log_first_line": ED_STATUS_FIRST,
             "status_log_final_line": ED_STATUS_FINAL,
             "status_log_win_halt_lines": list(ED_STATUS_WIN_HALT_LINES),
             "status_log_retry_lines": list(ED_STATUS_RETRY_LINES),
             "status_log_exhausted_lines": list(ED_STATUS_EXHAUSTED_LINES),
             "reprobe_budget": BUDGET,
             "source_budget_30m": BUDGET_30M,
             "origin_budget_15m": BUDGET_15M,
             "kit_integrity": {
                 "kit_manifest_sha256": ED_MANIFEST_SHA,
                 "kit_files_verified": ed_files,
                 "raw_file_sha256_pins": ED_RAW_SHAS,
                 "exh30m_source_sha256_pins": ED_EXH30M_SHAS,
                 "b33_status_sha256": B33_STATUS_SHA,
                 "ea_status_sha256": EA_STATUS_SHA,
                 "note": "the Part ED af034 60M kit is PUBLISHED (36 files, "
                         "byte-pinned above; fetch-verified against the kit "
                         "MANIFEST rev2 1dfe02ca...); the adopted key is fresh "
                         "at BASE (EXHAUSTED honest-UNKNOWN at 15M and 30M in "
                         "the declared budget-condition ladder, resolved exact "
                         "LOSS only at the pre-declared 60M condition)"}},
        ],
        "resolved_ids": list(ADOPTED_IDS),
        "loss_ids": list(ADOPTED_IDS),
        "win_ids": list(WIN_IDS_UNCONSUMED),
        "unadopted_win_ids": list(WIN_IDS_UNCONSUMED),
        "unadopted_win_rows": [],
        "exhausted_excluded_ids": list(EXHAUSTED_EXCLUDED_IDS),
        "exhausted_rows": [],
        "row_counts": {
            "adopted_loss_rows": 1,
            "wins_unconsumed": 0,
            "exhausted_excluded": 0,
            "prior_adopted_loss_rows_base": 2,
        },
        "adopted_table": adopted_table,
        "adopted_table_digest_sha256": digest,
        "sha256": {"loss_increment": incr_sha},
        "full_packet_eq_loss_only": True,
        "win_scenario_exists": False,
        "win_scenario_note":
            "the Part ED packet is exactly the single af034 key, resolved "
            "exact LOSS at 60M: no probe-level WIN row and no still-EXHAUSTED "
            "row exists in this Part; the 6 previously-unconsumed probe-level "
            "WIN children of class 34908 ({af029 s5 900646, af047 961976, "
            "af050 962386, af053 962470, af023 810351, af048 962172}) remain "
            "globally unconsumed and untouched by this Part (scrutiny-owner "
            "C++ second-implementation gate pin 9193f5b6...)",
        "full_packet_eq_loss_only_rationale":
            "the re-probed Part ED packet is probe-complete at the pre-declared "
            "60M condition and IS loss-only: the single fresh exact-LOSS row "
            "af034 is simultaneously the adopted row and the whole packet; no "
            "WIN row and no EXHAUSTED row stays unconsumed or excluded; the "
            "key was never adopted before (fresh-increment gate against BASE "
            "cecc1a0f...)",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "base_cache_prior_adoption_confirmed": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 1-LOSS adoption increment: only the fresh af034 "
            "exact-LOSS row (budget-condition ladder 15M -> 30M -> 60M, each "
            "rung its own declared Part) is consumed into the canonical cache "
            "via the fail-closed union merger; nodes are bookkeeping, never "
            "verdicts; the standard 11x11 empty board stays UNKNOWN; no class "
            "is freed or excluded by this Part",
        "provenance": {
            "ed_kit_files": ed_files,
            "b33_status_lines": 66,
            "ea_status_lines": 13,
            "ed_status_lines": ED_STATUS_LINES,
            "raws_published": True,
        },
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "increment_sha256": incr_sha,
        "rows": len(rowlines),
        "adopted_total_nodes_per_pass": ADOPTED_NODES,
        "digest": digest,
        "manifest_sha256": hashlib.sha256(
            (OUT / "increments-manifest.json").read_bytes()).hexdigest(),
    }))


HDR_LINES = [
 "# n11 central-reply closure af034 1-LOSS canonical-adoption increment",
 "#   (Part EE, 2026-11-25) - single key, loss-only, fresh increment.",
 "#   class-34908 batch-33 EXHAUSTED target af034 (s5 930660, legal 95,",
 "#   lo/hi 1152921504607911937/68719476736) was honestly EXHAUSTED",
 "#   (UNKNOWN) at the declared 15M condition (b33 status 1f66...),",
 "#   again EXHAUSTED at the declared 30M condition (Part EA status",
 "#   db7c7017...), and is resolved exact LOSS only at the pre-declared",
 "#   60M condition (Part ED, 2026-11-25): budget-condition ladder",
 "#   15M -> 30M -> 60M, one fresh condition upgrade per declared Part.",
 "#   The whole Part ED packet is exactly this 1 key (loss-only; no",
 "#   probe-level WIN row and no still-EXHAUSTED row exists in it).",
 "# 2-pass fresh-cold node-exact exact-S5 verdict at budget 60M",
 "#   ((30M,60M] interval of the declared condition ladder); published",
 "#   raws with '# replay_done' on both passes (176 s / 180 s wall);",
 "#   the Part ED kit (36 files, MANIFEST rev2 1dfe02ca...) verified",
 "#   byte-for-byte; the 15M/30M EXHAUSTED source raws and statuses",
 "#   pinned (b33-status 66 lines 1f66..., ea-status 13 lines",
 "#   db7c7017..., exh30m raws 9ecfdc77... / 3978990d...).",
 "#   Adopted per-pass node total 32012059 (= the whole probed packet).",
 "# Loss-only adoption asserts no root verdict, frees no class,",
 "#   excludes no class; scheduling effects are derived only by the",
 "#   reaudit refresh (Board fail-closed child verification) and the",
 "#   delta extractor.  11x11 stays UNKNOWN; nodes are bookkeeping,",
 "#   never verdicts."
]


if __name__ == "__main__":
    main()
