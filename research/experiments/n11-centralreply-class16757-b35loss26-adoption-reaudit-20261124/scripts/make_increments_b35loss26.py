#!/usr/bin/env python3
"""Build the batch-35 (class 16757) 26-LOSS canonical-adoption increment, fail-closed.

Prepared for the Part DW adoption (declared 2026-11-24, publish-then-execute):
the published batch-35 (Part DV probe drive) cumulative evidence is
byte-pinned through the single batch-35 kit
(research/experiments/n11-centralreply-closure-class16757-batch35-20261124,
MANIFEST 791996c1ad86a..., whose 109 listed files are input 29 (28 target
CSV b021-b048 + batch-keys-b35.json) + output/raw 56 (28 primary pairs, NO
sidecars) + output/status.log 1 + scripts 3 + sources 7 + val-gate 12, the
MANIFEST itself excluded). Every listed kit file is sha256-verified here
file-by-file. jsreplay.js 84585617... is the pinned solver image shared with
the earlier kits and val-gates.

The batch is FULLY probed: all 28 of 28 clean (never-probed) keys carry
honest two-pass fresh-cold labels at budget 15M (the drive honest-label
statuses: 26 PASS result=2 LOSS, 2 PASS result=1 WIN with pre-registered
WIN-HALT markers {b032, b048}, EXHAUSTED 0, MISMATCH 0, no retry sidecars).
ONLY the 26 LOSS rows ARE adopted here. The 2 WIN rows are consumed NOWHERE
by this Part: WIN row adoption belongs to the scrutiny-owner C++
second-implementation gate (pin 9193f5b6...). The batch-1 (2026-11-22)
probe-level WIN b018 (15000000,1,3549602, status
2026-11-22T02:39:43Z) likewise stays unconsumed, is NOT part of this batch
(excluded from the batch-35 key set, probe_order 28) and counts as an
unknown child of class 16757 everywhere.  Loss-only adoption does NOT by
itself assert any root verdict, and any class-16757 scheduling effect is
derived only later by the reaudit refresh + delta extractor (Board
fail-closed child verification), not by this maker.

The adoption base is the canonical exact-S5 verdict chain head = the Part DT
merged 6,547-row cache sha256
973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b
(BASE through the Part DT b33loss45 adoption), byte-pinned here; this maker
ABORTS against anything else. Every adopted key is asserted fresh (absent
from the BASE) and absent from the quarantine registry
(81d231604d3a...).

The drive status.log is HONEST HISTORY (30 lines = exactly 28 PASS verdict
rows, one per key, plus 2 WIN-HALT marker lines {b032, b048}; EXHAUSTED
marker lines 0; RETRY marker lines 0; MISMATCH lines 0): the per-key honest
labels are (15000000, result, nodes) with result in {1,2} pinned row-by-row
here.

Fail-closed gates: kit MANIFEST sha-verified file-by-file (109 files); 28
two-pass fresh-cold raw re-verification with '# replay_done' on both passes
and (budget,result,nodes) agreement with the status verdict row-by-row;
raw/batch-keys agreement on (legal, lo, hi) and pins on
(s5_index, membership_class_count); raw inventory == 28 x {p1,p2} primaries
and NOTHING else in output/raw; val-gate node-exact across the two
published host outputs per gate molecule (4 molecules x published-baseline
+ dv-host); the 26 adopted keys distinct, ABSENT from the canonical BASE
(6,547 rows) and from the quarantine registry; the derived WIN set equal to
the pinned marker set; adopted-row per-pass node total 67593391 on both
passes (all-28 total 73757659).  Verdicts are byte-taken from the raws.
The 26 LOSS rows ARE the only thing consumed into the canonical cache by
this Part; 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.
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
KIT1_DIR = ROOT / "research/experiments/n11-centralreply-closure-class16757-batch35-20261124"
KIT1_RAW = KIT1_DIR / "output/raw"
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class34908-b33loss45-adoption-reaudit-20261124/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-20261124.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
MERGER = EXP / "scripts/s5_union_merge.py"

MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
BASE_CACHE_SHA_EXPECTED = "973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b"
BASE_CACHE_ROWS_EXPECTED = 6547
BASE_CACHE_WIN_EXPECTED = 158
BASE_CACHE_LOSS_EXPECTED = 6389
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
QUARANTINE_SHA_EXPECTED = "81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9"

# --- published kit pins -------------------------------------------------------
KIT1_MANIFEST_SHA = "791996c1ad86a75cdc630434d2dff6e559583f804527f04dfe377ce123d4155c"
KIT1_FILES = 109
KIT1_KEYS_SHA = "d5bd4c89838f36b509e5283c2c8965d94be37888fea9f86fdce76195299bd90b"
KIT1_STATUS_SHA = "d7c3b42cc2ac3d8e32e517eaf08e90d646420a324d9b74357864a8916c37db1e"

# --- status.log honest-history pins ----------------------------------------------
KIT1_STATUS_LINES = 30
KIT1_STATUS_FIRST_LINE = "2026-11-24T21:38:56Z b021 PASS 15000000,2,2770116"
KIT1_STATUS_FINAL_LINE = "2026-11-24T21:51:39Z b048 WIN-HALT"
WIN_HALT_LINES = [
    "2026-11-24T21:43:44Z b032 WIN-HALT",
    "2026-11-24T21:51:39Z b048 WIN-HALT",
]
EXHAUSTED_LINES = []
RETRY_LINES = []
TRUNCATED_SIDECARS = []
BUDGET_KIT1 = 15000000

# --- adopted packet (class 16757; the batch-1 WIN b018 is NOT in this packet) ----
PROBED_IDS = [f"b{i:03d}" for i in range(21, 49)]
WIN_IDS = ["b032", "b048"]
EXH_IDS = []
ADOPTED_LOSS_IDS = [k for k in PROBED_IDS if k not in WIN_IDS and k not in EXH_IDS]
ADOPTED_KEYS = {
    'b021': {'key': (1153204079095218176, 65536), 'legal': 83, 'nodes': 2770116, 's5': 535179, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b022': {'key': (1153204079095316480, 65536), 'legal': 79, 'nodes': 2713847, 's5': 537545, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b023': {'key': (1153204079095447552, 65536), 'legal': 76, 'nodes': 720025, 's5': 539592, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b024': {'key': (1153204079095709696, 65536), 'legal': 83, 'nodes': 3705880, 's5': 541610, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b025': {'key': (1153204079097282560, 65536), 'legal': 87, 'nodes': 3468028, 's5': 545364, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b026': {'key': (1153204079111962624, 65536), 'legal': 72, 'nodes': 1067011, 's5': 546902, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b027': {'key': (1153204079128739840, 65536), 'legal': 75, 'nodes': 1974075, 's5': 548070, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b028': {'key': (1153204079162294272, 65536), 'legal': 83, 'nodes': 1173126, 's5': 549153, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b029': {'key': (1153204079632056320, 65536), 'legal': 81, 'nodes': 2722700, 's5': 551777, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b030': {'key': (1153204081242669056, 65536), 'legal': 87, 'nodes': 4019890, 's5': 554104, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b031': {'key': (1153204083390152704, 65536), 'legal': 86, 'nodes': 2770498, 's5': 555161, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b033': {'key': (1153206278118440960, 65536), 'legal': 83, 'nodes': 2517807, 's5': 558018, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b034': {'key': (1153208477141696512, 65536), 'legal': 84, 'nodes': 1461826, 's5': 558054, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b035': {'key': (1153212875188207616, 65536), 'legal': 83, 'nodes': 1871250, 's5': 558079, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b036': {'key': (1171218477604667392, 65536), 'legal': 84, 'nodes': 3697849, 's5': 558120, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b037': {'key': (1157707678722555904, 65536), 'legal': 72, 'nodes': 1372777, 's5': 558183, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b038': {'key': (1152922604118507520, 65792), 'legal': 86, 'nodes': 5301385, 's5': 558228, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b039': {'key': (1152922604185583616, 65792), 'legal': 82, 'nodes': 1109565, 's5': 558261, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b040': {'key': (1152922741557428224, 65792), 'legal': 81, 'nodes': 1939794, 's5': 558283, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b041': {'key': (1152922604118474756, 65792), 'legal': 88, 'nodes': 4022755, 's5': 558334, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b042': {'key': (1152922604118474754, 65792), 'legal': 88, 'nodes': 3914018, 's5': 558367, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b043': {'key': (1152922604118474753, 65792), 'legal': 78, 'nodes': 2503635, 's5': 558393, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b044': {'key': (1152922604118491136, 65792), 'legal': 80, 'nodes': 3184076, 's5': 558410, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b045': {'key': (1152922604118482944, 65792), 'legal': 87, 'nodes': 4325847, 's5': 558443, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b046': {'key': (1152922604152029184, 65792), 'legal': 81, 'nodes': 1811583, 's5': 558486, 'mcc': 4, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
    'b047': {'key': (1152922604135251968, 65792), 'legal': 74, 'nodes': 1454028, 's5': 558506, 'mcc': 3, 'decisive_budget': 15000000, 'raw_kit': 'KIT1'},
}
ADOPTED_TOTAL_NODES = 67593391
ALL28_TOTAL_NODES = 73757659

# --- val-gate pins ---------------------------------------------------------------
VAL_GATES = {
    "at2m-s5-1152921504606851072-536870946": (2000000, 0, 2000000),
    "at2m-s5-1188950301626860544-536870912": (2000000, 0, 2000000),
    "first-15m-s5-1152921504606851072-536870946": (15000000, 2, 3651923),
    "second-15m-s5-1188950301626860544-536870912": (15000000, 2, 5040200),
}
VAL_HOSTS = ["published-baseline", "dv-host"]


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


PRIMARY_RE = re.compile(r"^b\d{3}\.p[12]\.out$")


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
        m = re.match(r"^(\S+) (b\d{3}) PASS (\d+),(\d+),(\d+)$", line)
        if m:
            kid = m.group(2)
            if kid in got_pass:
                sys_exit(f"kit status duplicate verdict row for {kid}")
            got_pass[kid] = (int(m.group(3)), int(m.group(4)), int(m.group(5)))
            continue
        m = re.match(r"^(\S+) (b\d{3}) WIN-HALT$", line)
        if m:
            win_halt.append(line)
            continue
        m = re.match(r"^(\S+) (b\d{3}) EXHAUSTED (\d+),(\d+),(\d+)$", line)
        if m:
            exh.append(line)
            continue
        m = re.match(r"^(\S+) (b\d{3}) P2-TRUNCATED-RETRY$", line)
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
    if sha(KIT1_DIR / "input/batch-keys-b35.json") != KIT1_KEYS_SHA:
        sys_exit("batch-keys sha drift in the kit")
    if sha(KIT1_DIR / "output/status.log") != KIT1_STATUS_SHA:
        sys_exit("status.log sha drift in the kit")

    # --- batch-keys gates (b35 selection packet, frozen at kit selection) --------
    bk_all = json.loads((KIT1_DIR / "input/batch-keys-b35.json").read_text())
    if bk_all["schema"] != "n11-centralreply-closure-batch35-keys-v1":
        sys_exit("batch-keys schema drift")
    if bk_all["batch"] != "batch-35" or bk_all["target_key_count"] != 28 or len(bk_all["keys"]) != 28:
        sys_exit("batch-keys batch/target count drift")
    if int(bk_all["canonical_cache_s5verdict_rows"]) != BASE_CACHE_ROWS_EXPECTED:
        sys_exit("batch-keys canonical cache rows drift (kit frozen at selection)")
    if bk_all["consumed_into_canonical_cache"] is not False:
        sys_exit("batch-keys consumption flag drift")
    if bk_all["excluded_unconsumed_win"]["key_id"] != "b018":
        sys_exit("batch-keys excluded_unconsumed_win drift (b018 pinned)")
    if bk_all["pins"]["canonical_cache"] != BASE_CACHE_SHA_EXPECTED:
        sys_exit("batch-keys canonical cache pin drift (kit frozen at selection)")
    if bk_all["pins"]["closure_classes"] != "6cc33dd731c5d2237291552a91c3f7d60947bba875867fcab10394b533f1a68d":
        sys_exit("batch-keys closure-classes pin drift")
    if bk_all["pins"]["refresh_summary"] != "38fc4e193cf08cf4efb7830a8bad3d2245bc732380f44c4ee2913e05d5644732":
        sys_exit("batch-keys refresh-summary pin drift")
    if bk_all["pins"]["jsreplay"] != JSREPLAY_SHA_EXPECTED or bk_all["pins"]["quarantine"] != QUARANTINE_SHA_EXPECTED:
        sys_exit("batch-keys jsreplay/quarantine pin drift")
    if bk_all["pins"]["runbatch"] != "f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84":
        sys_exit("batch-keys runbatch pin drift")
    if bk_all["pins"]["batch1_audit"] != "9929bd9f83a1774f00a3791a340b6084a3109b565f482556c7d1f90f88b68abd" \
            or bk_all["pins"]["batch1_batch_keys"] != "2aaccc941d7aec35c416b27d5cdd10f7fbb82c9801bcf560b61e20be88c331f8" \
            or bk_all["pins"]["batch1_status"] != "559a0884d4c728c05a992bcf144661fbd8212bc09d2c8b56341aebe7b94348b1":
        sys_exit("batch-keys batch-1 kit pin drift")
    by_id = {k["key_id"]: k for k in bk_all["keys"]}
    if set(by_id) != set(PROBED_IDS):
        sys_exit("batch-keys key ids != the 28 probed keys")
    for e in bk_all["keys"]:
        if e["serving_class"] != 16757 or e["class_unknown_now_at_selection"] != 29:
            sys_exit("batch-keys serving class / selection-time unknown drift")

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
        if ref["legal"] != int(e["legal"]) or ref["lo"] != str(e["lo"]) or ref["hi"] != str(e["hi"]):
            sys_exit(f"{kid}: legal/key disagreement raw vs batch-keys")
        if (ref["budget"], ref["result"], ref["nodes"]) != got_pass[kid]:
            sys_exit(f"{kid}: raw (budget,result,nodes) row != status verdict row")
        raws15[kid] = ref
    loss_set = sorted(kid for kid in PROBED_IDS if raws15[kid]["result"] == 2)
    win_set = sorted(kid for kid in PROBED_IDS if raws15[kid]["result"] == 1)
    exh_set = sorted(kid for kid in PROBED_IDS if raws15[kid]["result"] == 0)
    if loss_set != sorted(ADOPTED_LOSS_IDS):
        sys_exit("decisive LOSS set != the 26 adopted candidates")
    if win_set != sorted(WIN_IDS):
        sys_exit(f"probe-level WIN set != the pinned 2 unconsumed WIN keys (b032, b048): {win_set}")
    if exh_set != sorted(EXH_IDS):
        sys_exit(f"probe-level EXHAUSTED set non-empty (batch-35 has NO EXHAUSTED keys): {exh_set}")
    if len(ADOPTED_LOSS_IDS) != 26 or len(WIN_IDS) != 2 or len(EXH_IDS) != 0:
        sys_exit("packet decomposition 26+2+0 != 28 drift")
    all28_nodes = sum(raws15[kid]["nodes"] for kid in PROBED_IDS)
    if all28_nodes != ALL28_TOTAL_NODES:
        sys_exit(f"all-28 node total drift {all28_nodes} != {ALL28_TOTAL_NODES}")

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
        "# n11 central-reply closure batch-35 (class 16757) 26-LOSS",
        "#   canonical-adoption increment (Part DW, 2026-11-24).",
        "# The published batch-35 kit (Part DV probe drive) probed",
        "#   ALL 28 of 28 clean keys honest two-pass fresh-cold at budget 15M:",
        "#   26 LOSS (adopted here), 2 probe-level WIN (b032/b048,",
        "#   pre-registered WIN-HALT markers, consumed NOWHERE by this Part -",
        "#   scrutiny-owner C++ gate 9193f5b6...), 0 EXHAUSTED, MISMATCH 0.",
        "#   The batch-1 probe-level WIN b018 is likewise unconsumed and is",
        "#   NOT part of this packet.  ONLY the 26 fresh LOSS rows are",
        "#   consumed into the canonical cache by this increment.",
        "# 2-pass node-exact exact-S5 verdicts, fresh cold, pinned",
        "#   jsreplay.js sha256",
        "#   845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# gates: kit MANIFEST sha-verified file-by-file (109 files);",
        "#   28 two-pass fresh-cold raw re-verification with",
        "#   '# replay_done' on both passes; (budget,result,nodes)",
        "#   agreement with the 30-line honest-history status pins;",
        "#   raw/batch-keys agreement on (legal,lo,hi) and",
        "#   (s5_index, membership_class_count); raw inventory == 56",
        "#   primaries and nothing else; val-gate node-exact across the",
        "#   two published host outputs per molecule; adopted keys",
        "#   distinct, absent from BASE 973bcd19... (6,547 rows, WIN 158 /",
        "#   LOSS 6,389) and from the quarantine registry; derived WIN set",
        "#   equal to the pinned marker set; adopted per-pass node total",
        "#   67593391 (all-28 total 73757659).",
        "# Loss-only adoption asserts no root verdict; any class-16757",
        "#   scheduling effect is derived only by the reaudit refresh",
        "#   (Board fail-closed child verification) and the delta",
        "#   extractor, never by this maker.  11x11 stays UNKNOWN;",
        "#   nodes are bookkeeping, never verdicts.",
    ]
    rows_for_sort = [(ADOPTED_KEYS[k]["key"][0], ADOPTED_KEYS[k]["key"][1], ADOPTED_KEYS[k]["nodes"]) for k in ADOPTED_LOSS_IDS]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_path = OUT / "increment-b35loss26-20261124.cache"
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
        "schema": "b35loss26-increments-manifest-v1",
        "batches": [{
            "batch": 35,
            "class_index": 16757,
            "keys_total": 28,
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
            "stop_rule": "batch-35 probe-complete (28/28 clean keys carry honest two-pass labels: 26 LOSS @15M adopted + 2 probe-level WIN unconsumed pending the scrutiny-owner C++ gate + 0 EXHAUSTED; the batch-1 WIN b018 stays unconsumed outside this packet; verdict not consumed)",
            "fragment_state": {},
        }],
        "resolved_ids": list(ADOPTED_LOSS_IDS),
        "loss_ids": list(ADOPTED_LOSS_IDS),
        "win_ids": list(WIN_IDS),
        "unadopted_win_ids": list(WIN_IDS),
        "unadopted_win_rows": win_rows,
        "exhausted_excluded_ids": list(EXH_IDS),
        "exhausted_rows": exh_rows,
        "row_counts": {"probed_rows": 28, "adopted_loss_rows": 26, "prior_adopted_loss_rows": 0,
                        "wins": 2, "exhausted_excluded": 0, "fragments_unprobed": 0, "fileless_unprobed": 0},
        "sha256": {"loss": incr_sha},
        "full_packet_eq_loss_only": False,
        "win_scenario_exists": True,
        "win_scenario_note": "exactly two probe-level WIN rows exist (b032/b048, each carrying its pre-registered WIN-HALT marker) and each stays unconsumed by this adoption (scrutiny owner C++ second-implementation gate pin 9193f5b6...); together with the batch-1 probe-level WIN b018 (excluded from this batch and likewise unconsumed), loss-only adoption NEVER frees class 16757 while any of the three WIN children remains verdict-unconsumed",
        "full_packet_eq_loss_only_rationale":
            "the batch is probe-complete (28/28 honest labels) but the packet is NOT loss-only: "
            "two probe-level WIN rows stay UNCONSUMED and are NOT adopted; the adopted packet is "
            "the 26 fresh LOSS rows plus nothing else; no batch-35 row was adopted before; "
            "class 16757 is NOT freed (three verdict-pending WIN children remain: b018, b032, b048)",
        "fragment_rows_note":
            "batch-35 is probe-complete with NO fragment keys: the raw inventory is exactly the "
            "28 x {p1,p2} primary pairs (56 files) with NO sidecars",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "base_cache_prior_adoption_confirmed": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 26-LOSS adoption increment: only the 26 fresh LOSS rows are consumed into "
            "the canonical cache via the fail-closed union merger; the two probe-level WINs are "
            "consumed NOWHERE (no verdict claim, no exclusion claim) and belong to the scrutiny "
            "owner; the batch-1 probe-level WIN b018 likewise stays unconsumed and is not in this "
            "packet; all 28 batch-35 keys stay UNKNOWN as verdicts; adopting 26 LOSS rows does "
            "NOT free class 16757 (three unconsumed WIN children remain: b018, b032, b048); "
            "class 16757 stays unknown as a class; loss-only adoption asserts no root verdict "
            "and no coverage claim; any scheduling effect is derived only by the reaudit refresh "
            "(Board fail-closed child verification); 11x11 stays UNKNOWN; nodes are bookkeeping, "
            "never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INCREMENT rows=26 loss_nodes={ADOPTED_TOTAL_NODES} -> {incr_path}")


if __name__ == "__main__":
    main()
