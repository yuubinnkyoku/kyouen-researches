#!/usr/bin/env python3
"""Build the batch-28 (class 5343) 7-LOSS canonical-adoption increment, fail-closed.

Prepared for the Part CO adoption: the published batch-28 cumulative
evidence is byte-pinned through TWO published drive kits - drive-4 (Part CK,
kit MANIFEST 1e4024f8, 150 files) and drive-5 (Part CN, kit MANIFEST
e2d81055, 200 files, cumulative: it carries all 54 keys' p1/p2 raws, the 8
truncated sidecars and the disclosed empty-key junk artifact
output/raw/.p1.out).  Both kits are sha256-verified here file-by-file.
The 54 keys are ALL probed to completion (Part CN drive-5): 35 WIN rows,
11 EXHAUSTED rows, 8 LOSS rows.  aa003 (the 8th LOSS) was ALREADY adopted
by the Part CH 1-LOSS adoption into the canonical BASE cache (6,294 rows
sha256 3124461b...); this maker asserts that BASE row is EXACTLY the
aa003 raw evidence (result 2, nodes 4,070,373) and does NOT re-emit it.

Emits the CANONICAL-ADOPTION increment cache over the published raw replay
rows of the resolved fresh LOSS set only:

  * batch-28 (class 5343): the 7 resolved fresh LOSS rows
    aa015 / aa017 / aa018 / aa023 / aa024 / aa029 / aa036
    (total nodes per pass 38,784,669)

The 35 WIN rows (including aa001/aa002/aa006/aa007/aa008/aa009
third-implementation cross-verified in Parts CC/CG/CM; the remaining 29
await cross-verification) are HONEST LABELS ONLY and are NOT adopted: they
stay unconsumed (scrutiny owner C++ second-implementation gate pin
9193f5b6...), like the batch-14residual q042 / batch-26 l028 precedents
(loss-only adoption with in-batch WINs left unconsumed).  full != loss
here (machine-stated): the adopted packet is the 7-LOSS packet of a
fully-probed batch whose remaining 46 non-adopted keys are 35 WIN honest
labels + 11 EXHAUSTED honest-UNKNOWN rows.  The 11 EXHAUSTED rows carry
NO verdict and are excluded (budget exhaustion at 15M, same-condition
re-probe not performed).

The adoption base is the canonical exact-S5 verdict cache BASE =
the Part CH merged 6,294-row cache sha256 3124461b... (Part BZ chain +
the aa003 increment), byte-pinned here; this maker ABORTS against
anything else.  The EXHAUSTED rows are asserted absent from BASE;
every WIN key and every adopted key is asserted fresh (absent from
BASE: the batch-28 rows post-date both the Part BZ and Part CH merges -
with the single declared exception of aa003, which IS in BASE and is
asserted byte-consistent, never re-emitted).

Fail-closed gates: BOTH kit MANIFESTs sha-verified file-by-file (150 +
200 files); every adopted row must come from BOTH published raw passes
with identical (stones, legal, is_or, budget, result, nodes, lo, hi) and
a completed "# replay_done" line - enforced for ALL 54 keys (two-pass
node-exact over the whole batch); legal and (lo,hi) must match the
published batch-keys.json for every key; every status.log PASS row
(drive-5 cumulative picture, sha-pinned) must agree with the raws on
(budget, result, nodes), each key exactly once; halt rows must be exactly
the 35 WIN-HALT 2-line pairs and 11 EXHAUSTED 2-line pairs with direct
adjacency; the drive-4 status.log is sha-pinned AND asserted to be the
exact 61-line prefix of the drive-5 status.log; the truncated-retry lines
must be exactly the published 8; the 8 truncated sidecars and the junk
.p1.out artifact must carry NO replay evidence and NO replay_done; the
final status.log line must be exactly the disclosed workbook junk row
"P1-FAIL " (no key id, not a verdict record; the completion log of Part
CN discloses the empty-key invocation that produced it and that no
aaNNN pass file was affected); no EXECUTION-COMPLETE row anywhere; the
published row-audit pictures (drive-4 winhalt + drive-5 full-v2) must
agree with the derived picture (loss/win/exhausted sets, mismatches 0,
input pins); adopted-row node totals must agree on both passes
(38,784,669); the 7 adopted keys are distinct, ABSENT from the canonical
BASE cache, and absent from the quarantine registry; aa003's BASE row
must be exactly (2, 4,070,373).  Verdicts are byte-taken from the raws.
The 7 LOSS rows IS the only thing consumed into the canonical cache by
the Part CO fail-closed merger; no WIN verdict is consumed anywhere.
11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.
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
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class5343-loss1-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-plus-batch24loss2-plus-batch27loss4-plus-batch28loss1-20261123.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
D4_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5343-batch28-drive4-20261123"
D5_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5343-batch28-drive5-20261123"

B28_KEYS_SHA_EXPECTED = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
D4_MANIFEST_SHA_EXPECTED = "1e4024f861e0080d63bc606d8d53a02bd909d97708aca0b3933dc3dff1041475"
D4_STATUS_SHA_EXPECTED = "598174447fa878c2e0a6d6db6f892c5c279063174d763746456476e3051633f8"
D4_ROW_AUDIT_SHA_EXPECTED = "dcf078aab8f05dea3dde25da517393de9b851cf1042c7a05ff489203ba284358"
D4_KIT_FILES_EXPECTED = 150
D5_MANIFEST_SHA_EXPECTED = "e2d81055c19945d4f0a4e29a3c521381c31f540f12537a4daddf5dfb1b597a3c"
D5_STATUS_SHA_EXPECTED = "ca1e98ccd952b29e8295147add50e6b4a3ff3732748bf544b9c3a7018d495df0"
D5_ROW_AUDIT_SHA_EXPECTED = "00c323835f9ebc048b6ffea81a8fd556e3e8146adf1c562c34aa89d9d7bb69c0"
D5_KIT_FILES_EXPECTED = 200
BASE_CACHE_SHA_EXPECTED = "3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e"
BASE_CACHE_ROWS_EXPECTED = 6294
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"

BUDGET = 15000000

ADOPTED_LOSS_IDS = ["aa015", "aa017", "aa018", "aa023", "aa024", "aa029", "aa036"]
ADOPTED_NODES = {
    "aa015": 6152494, "aa017": 11446358, "aa018": 214968,
    "aa023": 5000770, "aa024": 5003631, "aa029": 10010789,
    "aa036": 955659,
}
ADOPTED_TOTAL_NODES = 38784669
AA003 = {"key_id": "aa003", "s5": 104943, "lo": 1152921504741064704, "hi": 4228,
         "legal": 86, "nodes": 4070373}
WIN_IDS = ["aa001", "aa002", "aa006", "aa007", "aa008", "aa009", "aa010",
           "aa011", "aa012", "aa013", "aa014", "aa016", "aa019", "aa020",
           "aa022", "aa025", "aa026", "aa027", "aa033", "aa034", "aa037",
           "aa038", "aa039", "aa040", "aa041", "aa042", "aa043", "aa044",
           "aa045", "aa046", "aa048", "aa049", "aa051", "aa052", "aa054"]
EXHAUSTED_IDS = ["aa004", "aa005", "aa021", "aa028", "aa030", "aa031",
                 "aa032", "aa035", "aa047", "aa050", "aa053"]
TRUNCATED_SIDECARS = [
    "output/raw/aa004.p2.truncated.160858.out",
    "output/raw/aa005.p1.truncated.161058.out",
    "output/raw/aa006.p2.truncated.161949.out",
    "output/raw/aa007.p2.truncated.161949.out",
    "output/raw/aa030.p2.truncated.181550.out",
    "output/raw/aa031.p2.truncated.181550.out",
    "output/raw/aa034.p2.truncated.184933.out",
    "output/raw/aa035.p2.truncated.184933.out",
]
TRUNCATED_RETRY_ROWS = {
    ("aa004", "P2"), ("aa005", "P1"), ("aa006", "P2"), ("aa007", "P2"),
    ("aa030", "P2"), ("aa031", "P2"), ("aa034", "P2"), ("aa035", "P2"),
}
D5_STATUS_LINES_EXPECTED = 109
D4_STATUS_LINES_EXPECTED = 61
D5_FINAL_VERDICT_ROW = "2026-11-23T19:24:56Z aa054 WIN-HALT"
JUNK_ROW = "P1-FAIL "


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
    texts = {}
    for tag in ("p1", "p2"):
        p = D5_DIR / f"output/raw/{kid}.{tag}.out"
        if not p.is_file():
            sys_exit(f"missing raw {p}")
        txt = p.read_text()
        if "# replay_done" not in txt:
            sys_exit(f"raw {p} lacks the '# replay_done' completeness guard")
        variants[tag] = parse_replay(p)
        texts[tag] = txt
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys_exit(f"{kid}: pass mismatch {tag} {r} vs p1 {ref}")
    return ref


def parse_status(path: Path):
    got = {}
    for line in path.read_text().splitlines():
        m = re.match(r"^(\S+) (\S+) PASS (\d+),(\d+),(\d+)$", line)
        if m:
            kid, b, r, n = m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
            if kid in got:
                sys_exit(f"status key {kid} appears more than once (each-once gate)")
            got[kid] = (b, r, n)
    return got


def main() -> None:
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys_exit("base cache sha drift")
    merger = EXP / "scripts/s5_union_merge.py"
    if sha(merger) != MERGER_SHA_EXPECTED:
        sys_exit("fail-closed union merger (scripts/s5_union_merge.py) sha drift: "
                 "this Part must use the pinned merger byte-for-byte")

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

    # --- kit integrity: BOTH published drive kits, file-by-file ---------------
    d4_verified = verify_kit(D4_DIR, D4_MANIFEST_SHA_EXPECTED, D4_KIT_FILES_EXPECTED)
    d5_verified = verify_kit(D5_DIR, D5_MANIFEST_SHA_EXPECTED, D5_KIT_FILES_EXPECTED)
    for tag, dirp in (("d4", D4_DIR), ("d5", D5_DIR)):
        if sha(dirp / "input/batch-keys.json") != B28_KEYS_SHA_EXPECTED:
            sys_exit(f"{tag} batch-keys.json sha drift")

    # --- batch-keys -----------------------------------------------------------
    bkd = D5_DIR / "input/batch-keys.json"
    bk_all = json.loads(bkd.read_text())
    if bk_all["schema"] != "n11-centralreply-closure-class5343-batch28-input-v1":
        sys_exit(f"batch-keys schema drift: {bk_all['schema']}")
    if bk_all["class_index"] != 5343 or bk_all["budget"] != BUDGET:
        sys_exit("batch-keys class/budget drift")
    if bk_all["closure_class_rank_in_published_base"] != 27:
        sys_exit("batch-keys closure rank drift")
    if int(bk_all["published_base_canonical_rows"]) != 6293:
        sys_exit("batch-keys published_base_canonical_rows drift (kit frozen at CB)")
    by_id = {k["key_id"]: k for k in bk_all["keys"]}
    if len(by_id) != 54:
        sys_exit(f"batch-keys key count {len(by_id)} != 54")

    # --- status.log pictures ---------------------------------------------------
    if sha(D4_DIR / "output/status.log") != D4_STATUS_SHA_EXPECTED:
        sys_exit("drive-4 status.log sha drift")
    if sha(D5_DIR / "output/status.log") != D5_STATUS_SHA_EXPECTED:
        sys_exit("drive-5 status.log sha drift")
    d4_lines = (D4_DIR / "output/status.log").read_text().splitlines()
    d5_lines = (D5_DIR / "output/status.log").read_text().splitlines()
    if len(d4_lines) != D4_STATUS_LINES_EXPECTED:
        sys_exit(f"drive-4 status lines {len(d4_lines)} != {D4_STATUS_LINES_EXPECTED}")
    if len(d5_lines) != D5_STATUS_LINES_EXPECTED:
        sys_exit(f"drive-5 status lines {len(d5_lines)} != {D5_STATUS_LINES_EXPECTED}")
    if d5_lines[:len(d4_lines)] != d4_lines:
        sys_exit("drive-4 status.log is NOT the exact prefix of the drive-5 picture")
    if d5_lines[-2] != D5_FINAL_VERDICT_ROW:
        sys_exit(f"drive-5 final verdict row drift: {d5_lines[-2]}")
    if d5_lines[-1] != JUNK_ROW:
        sys_exit(f"drive-5 last line must be the disclosed junk row {JUNK_ROW!r}: {d5_lines[-1]!r}")
    if re.search(r"aa\d{3}", d5_lines[-1]):
        sys_exit("junk row must carry no key id (disclosed bookkeeping, not a verdict)")
    if "EXECUTION-COMPLETE" in "\n".join(d5_lines):
        sys_exit("unexpected EXECUTION-COMPLETE record")
    status = parse_status(D5_DIR / "output/status.log")
    expected_probed = [f"aa{i:03d}" for i in range(1, 55)]
    if set(status) != set(expected_probed) or len(status) != 54:
        sys_exit(f"status probed set != all 54 keys: "
                 f"{sorted(set(status) ^ set(expected_probed))}")
    # retry rows exactly the published 8
    retry_rows = set()
    for ln in d5_lines:
        m = re.match(r"^(\S+) (aa\d{3}) (P[12])-TRUNCATED-RETRY$", ln)
        if m:
            retry_rows.add((m.group(2), m.group(3)))
    if retry_rows != TRUNCATED_RETRY_ROWS:
        sys_exit(f"truncated-retry rows {sorted(retry_rows)} != published 8")
    # halt/EXHAUSTED adjacency: 35 WIN-HALT pairs + 11 EXHAUSTED pairs
    pass_rows = [ln for ln in d5_lines if " PASS " in ln]
    if len(pass_rows) != 54:
        sys_exit(f"PASS rows {len(pass_rows)} != 54")
    halts = {}
    for ln in d5_lines:
        m = re.match(r"^(\S+) (aa\d{3}) (WIN-HALT|EXHAUSTED)( |$)", ln)
        if m:
            if m.group(2) in halts:
                sys_exit(f"multiple halt rows for {m.group(2)}")
            halts[m.group(2)] = (m.group(1), m.group(3))
    for ln in pass_rows:
        m = re.match(r"^(\S+) (aa\d{3}) PASS (\d+),(\d+),(\d+)$", ln)
        kid, r = m.group(2), int(m.group(4))
        idx = d5_lines.index(ln)
        nxt = d5_lines[idx + 1] if idx + 1 < len(d5_lines) else ""
        if r == 1:
            if halts.get(kid, ("", ""))[1] != "WIN-HALT":
                sys_exit(f"WIN row {kid} lacks its WIN-HALT row")
            if not re.match(rf"^\S+ {kid} WIN-HALT( |$)", nxt):
                sys_exit(f"WIN PASS row of {kid} not directly followed by its WIN-HALT row")
        elif r == 0:
            if halts.get(kid, ("", ""))[1] != "EXHAUSTED":
                sys_exit(f"EXHAUSTED row {kid} lacks its EXHAUSTED record")
            if not re.match(rf"^\S+ {kid} EXHAUSTED( |$)", nxt):
                sys_exit(f"EXHAUSTED PASS row of {kid} not directly followed by its EXHAUSTED row")
        elif r == 2:
            if kid in halts and not nxt.startswith("#"):
                sys_exit(f"LOSS row {kid} unexpectedly halted: {nxt}")
        else:
            sys_exit(f"PASS row with unknown result at {ln}")
    if len(halts) != 46:
        sys_exit(f"halt rows {len(halts)} != 35 WIN + 11 EXHAUSTED = 46")
    # truncated sidecars + junk artifact carry no evidence
    for rel in TRUNCATED_SIDECARS:
        sp = D5_DIR / rel
        if not sp.is_file():
            sys_exit(f"truncated sidecar missing: {rel}")
        stxt = sp.read_text()
        if "# replay_done" in stxt or re.search(r"^replay,", stxt, re.M):
            sys_exit(f"truncated sidecar carries evidence: {rel}")
    junk = (D5_DIR / "output/raw/.p1.out").read_text()
    if "# replay_done" in junk or re.search(r"^replay,", junk, re.M):
        sys_exit("junk artifact .p1.out carries evidence")
    if "ENOENT" not in junk or "input/.input.csv" not in junk:
        sys_exit("junk artifact .p1.out is not the disclosed empty-key ENOENT record")

    # --- published row-audit pictures -----------------------------------------
    ra4 = json.loads((D4_DIR / "output/row-audit-winhalt.json").read_text())
    if ra4["schema"] != "n11-centralreply-closure-class5343-batch28-rowaudit-winhalt-v1":
        sys_exit("drive-4 row-audit schema drift")
    if (ra4["class_index"] != 5343 or ra4["batch"] != 28 or ra4["keys_total"] != 54
            or ra4["probed"] != 31 or ra4["pass_rows"] != 7 or ra4["mismatches"] != 0
            or ra4["fragment_keys"] != {} or ra4["input_sha256"] != B28_KEYS_SHA_EXPECTED
            or ra4["unprobed_count"] != 23):
        sys_exit("drive-4 row-audit header drift")
    if sorted(ra4["loss_rows"]) != sorted(["aa003"] + ADOPTED_LOSS_IDS[:6]):
        sys_exit(f"drive-4 row-audit loss set drift: {ra4['loss_rows']}")
    if sorted(ra4["win_rows"]) != sorted(WIN_IDS[:18]):
        sys_exit("drive-4 row-audit win set drift (first 18 drive-4 keys)")
    if sorted(ra4["exhausted_rows"]) != sorted(EXHAUSTED_IDS[:6]):
        sys_exit("drive-4 row-audit exhausted set drift")
    ra5 = json.loads((D5_DIR / "output/row-audit.json").read_text())
    if ra5["schema"] != "n11-centralreply-closure-class5343-batch28-rowaudit-full-v2":
        sys_exit("drive-5 row-audit schema drift")
    if (ra5["class_index"] != 5343 or ra5["batch"] != 28 or ra5["keys_total"] != 54
            or ra5["probed"] != 54 or ra5["mismatches"] != 0
            or ra5["input_sha256"] != B28_KEYS_SHA_EXPECTED):
        sys_exit("drive-5 row-audit header drift")
    if sorted(ra5["loss_rows"]) != sorted(ADOPTED_LOSS_IDS + ["aa003"]):
        sys_exit("drive-5 row-audit loss set drift")
    if sorted(ra5["win_rows"]) != sorted(WIN_IDS):
        sys_exit("drive-5 row-audit win set drift")
    if sorted(ra5["exhausted_rows"]) != sorted(EXHAUSTED_IDS):
        sys_exit("drive-5 row-audit exhausted set drift")

    # --- two-pass raw verification of ALL 54 keys ------------------------------
    raws = {}
    for i in range(1, 55):
        kid = f"aa{i:03d}"
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
    if sorted(k for k, r in raws.items() if r["result"] == 2) != sorted(ADOPTED_LOSS_IDS + ["aa003"]):
        sys_exit("the raw LOSS set over all 54 keys != adopted 7 + already-adopted aa003")
    if sorted(k for k, r in raws.items() if r["result"] == 1) != sorted(WIN_IDS):
        sys_exit("the raw WIN set over all 54 keys != the 35 honest labels")
    if sorted(k for k, r in raws.items() if r["result"] == 0) != sorted(EXHAUSTED_IDS):
        sys_exit("the raw EXHAUSTED set over all 54 keys != the 11 honest UNKNOWNs")

    # --- gate every batch-28 key against the BASE cache ------------------------
    for i in range(1, 55):
        kid = f"aa{i:03d}"
        key = (raws[kid]["lo"], raws[kid]["hi"])
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if kid == "aa003":
            continue
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE cache {key} "
                     f"(base={base_keys[key]}, raw=(result {raws[kid]['result']}, nodes {raws[kid]['nodes']})); "
                     "the batch-28 rows post-date the Part BZ and Part CH merges "
                     "(aa003 excepted)")

    # --- aa003: already adopted by Part CH; BASE row must byte-match the raw ---
    a3 = raws["aa003"]
    if (a3["result"], a3["nodes"]) != (2, AA003["nodes"]):
        sys_exit("aa003 raw is not the published Part CH adopted record")
    if a3["legal"] != AA003["legal"] or (a3["lo"], a3["hi"]) != (AA003["lo"], AA003["hi"]):
        sys_exit("aa003 raw key/legal drift")
    if int(by_id["aa003"]["s5_index"]) != AA003["s5"]:
        sys_exit("aa003 batch-keys s5 drift")
    base_row = base_keys.get((AA003["lo"], AA003["hi"]))
    if base_row != (2, AA003["nodes"]):
        sys_exit(f"aa003 BASE row {base_row} != the raw evidence (2, {AA003['nodes']}) "
                 "(Part CH adoption consistency gate)")

    # --- the 7 fresh adopted LOSS rows -----------------------------------------
    emitted_keys = set()
    nodes_p1_total = 0
    nodes_p2_total = 0
    for kid in ADOPTED_LOSS_IDS:
        ref = raws[kid]
        if ref["result"] != 2:
            sys_exit(f"{kid}: adopted row must be result 2, got {ref['result']}")
        if ref["nodes"] != ADOPTED_NODES[kid]:
            sys_exit(f"{kid}: adopted-row nodes drift {ref['nodes']} != {ADOPTED_NODES[kid]}")
        key = (ref["lo"], ref["hi"])
        if key in emitted_keys:
            sys_exit(f"{kid}: duplicate emitted key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: adopted key already in BASE (fresh-increment gate)")
        emitted_keys.add(key)
        nodes_p1_total += ref["nodes"]
        # independent second-pass node recomputation
        n_p2 = sum(int(line.split(",")[7])
                   for line in (D5_DIR / f"output/raw/{kid}.p2.out").read_text().splitlines()
                   if line.startswith("replay,"))
        nodes_p2_total += n_p2
        if n_p2 != ref["nodes"]:
            sys_exit(f"{kid}: adopted-row pass node totals disagree: {n_p2} vs {ref['nodes']}")
    if nodes_p1_total != ADOPTED_TOTAL_NODES or nodes_p2_total != ADOPTED_TOTAL_NODES:
        sys_exit(f"adopted packet node totals drift p1={nodes_p1_total} p2={nodes_p2_total} "
                 f"!= {ADOPTED_TOTAL_NODES}")

    # --- bookkeeping rows (NOT emitted) ----------------------------------------
    win_rows = []
    for kid in WIN_IDS:
        w = raws[kid]
        if w["result"] != 1:
            sys_exit(f"{kid}: WIN row not the published honest label: result {w['result']}")
        cross = ("third-implementation cross-verified"
                 if kid in ("aa001", "aa002", "aa006", "aa007", "aa008", "aa009")
                 else "cross-verification pending (honest label only)")
        win_rows.append({
            "key_id": kid, "batch": 28, "class_index": 5343,
            "s5_index": int(by_id[kid]["s5_index"]), "lo": w["lo"], "hi": w["hi"],
            "legal": w["legal"], "result": 1, "nodes": w["nodes"],
            "two_pass_node_exact": True,
            "note": f"honest label only, never adopted in this Part ({cross}; "
                    "stays unconsumed)",
        })
    exhausted_rows = []
    for kid in EXHAUSTED_IDS:
        e = raws[kid]
        if e["result"] != 0 or e["nodes"] != BUDGET:
            sys_exit(f"{kid}: EXHAUSTED row not the published budget-exhaustion record: {e}")
        exhausted_rows.append({
            "key_id": kid, "batch": 28, "class_index": 5343,
            "s5_index": int(by_id[kid]["s5_index"]), "lo": e["lo"], "hi": e["hi"],
            "legal": e["legal"], "result": 0, "nodes": BUDGET,
            "two_pass_node_exact": True,
            "note": "budget exhaustion at 15M on both passes (honest UNKNOWN; "
                    "same-condition re-probe not performed; NOT adopted, NOT emitted; "
                    "nodes are bookkeeping",
        })

    # --- emit the increment + manifest ------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = [
        "# n11 central-reply closure batch-28 (class 5343) 7-LOSS",
        "#   canonical-adoption increment (Part CO, 2026-11-23)",
        "# published Part CO declaration (single-owner note; loss-only adoption:",
        "#   all 54 batch-28 keys are probed to completion (Part CN drive-5).  The",
        "#   35 WIN rows (aa001/aa002/aa006/aa007/aa008/aa009 third-implementation",
        "#   cross-verified in Parts CC/CG/CM; the other 29 honest labels) and the",
        "#   11 EXHAUSTED rows are NOT adopted here.  aa003 was ALREADY adopted by",
        "#   Part CH and is asserted BASE-consistent, never re-emitted.",
        "# 2-pass node-exact exact-S5 verdict at budget 15M, fresh cold, pinned",
        "#   jsreplay.js sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# gates: BOTH drive kits (drive-4 Part CK: 150 files, drive-5 Part CN:",
        "#   200 files) sha-verified file-by-file; ALL 54 keys two-pass node-exact;",
        "#   status.log (drive-5 cumulative, sha-pinned; drive-4 asserted exact",
        "#   61-line prefix) each-once agreement (b,r,n); 35 WIN-HALT + 11",
        "#   EXHAUSTED 2-line pair adjacency; 8 truncated sidecars + the disclosed",
        "#   empty-key junk artifact '.p1.out' carry NO evidence; row-audit",
        "#   pictures (winhalt + full-v2) agreement; batch-keys legal/(lo,hi)",
        "#   agreement; adopted-row per-pass node total 38,784,669; adopted keys",
        "#   distinct and absent from BASE and quarantine; aa003 BASE==raw (2,",
        "#   4,070,373) consistency gate; WIN/EXHAUSTED rows asserted NOT emitted.",
        "# ADOPTED set = {aa015, aa017, aa018, aa023, aa024, aa029, aa036}.  full !=",
        "#   loss here (machine-stated): the fully-probed batch additionally holds",
        "#   the 35 WIN rows and the 11 EXHAUSTED rows; the WIN verdicts stay",
        "#   UNCONSUMED (scrutiny owner C++ second-implementation gate pin",
        "#   9193f5b6...; batch-14residual q042 / batch-26 l028 precedents); no",
        "#   WIN verdict is consumed anywhere by this Part; the unconsumed closure",
        "#   WIN candidates are untouched.",
        "# The 7 LOSS rows ARE consumed into the canonical cache by the Part CO",
        "#   fail-closed union merger; 11x11 stays UNKNOWN; nodes are bookkeeping,",
        "#   never verdicts.",
    ]
    rows_for_sort = [(raws[k]["lo"], raws[k]["hi"], raws[k]["nodes"]) for k in ADOPTED_LOSS_IDS]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_path = OUT / "increment-b28loss7-20261123.cache"
    incr_path.write_bytes(blob)
    incr_sha = hashlib.sha256(blob).hexdigest()

    manifest = {
        "schema": "b28loss7-increments-manifest-v1",
        "batches": [{
            "batch": 28,
            "class_index": 5343,
            "keys_total": 54,
            "adopted_loss_ids": list(ADOPTED_LOSS_IDS),
            "already_adopted_ids": ["aa003"],
            "unadopted_win_ids": list(WIN_IDS),
            "exhausted_excluded_ids": list(EXHAUSTED_IDS),
            "probed_ids": list(status.keys()),
            "fragment_ids": [],
            "fileless_unprobed_count": 0,
            "input_sha256": B28_KEYS_SHA_EXPECTED,
            "row_audit_sha256": {
                "drive4_winhalt": D4_ROW_AUDIT_SHA_EXPECTED,
                "drive5_full_v2": D5_ROW_AUDIT_SHA_EXPECTED,
            },
            "status_log_sha256": {
                "drive4": D4_STATUS_SHA_EXPECTED,
                "drive5": D5_STATUS_SHA_EXPECTED,
                "drive4_is_exact_prefix_of_drive5": True,
            },
            "status_log_final_verdict_row": D5_FINAL_VERDICT_ROW,
            "status_log_junk_row": {
                "row": JUNK_ROW,
                "note": "disclosed empty-key invocation artifact (Part CN completion log); "
                        "no key id, not a verdict record; '.p1.out' node ENOENT record "
                        "(no replay row, no replay_done); all 54 aaNNN pass files unaffected",
            },
            "kit_integrity": {
                "drive4": {"manifest_sha256": D4_MANIFEST_SHA_EXPECTED,
                            "files_verified": d4_verified},
                "drive5": {"manifest_sha256": D5_MANIFEST_SHA_EXPECTED,
                            "files_verified": d5_verified},
            },
            "truncated_sidecars": list(TRUNCATED_SIDECARS),
            "truncated_retry_rows": sorted(f"{kid}.{p}" for kid, p in TRUNCATED_RETRY_ROWS),
            "total_nodes_pass_one": nodes_p1_total,
            "total_nodes_pass_two": nodes_p2_total,
            "stop_rule": "WIN-CONTINUE (Part CK drive-4 + Part CN drive-5 pre-registered; "
                         "verdict not consumed; all 54 keys probed to completion)",
            "fragment_state": {},
        }],
        "resolved_ids": [f"aa{i:03d}" for i in range(1, 55)],
        "loss_ids": list(ADOPTED_LOSS_IDS),
        "win_ids": list(WIN_IDS),
        "unadopted_win_ids": list(WIN_IDS),
        "exhausted_excluded_ids": list(EXHAUSTED_IDS),
        "row_counts": {
            "probed_rows": 54, "adopted_loss_rows": 7, "wins": 35,
            "exhausted_excluded": 11, "fragments_unprobed": 0, "fileless_unprobed": 0,
        },
        "sha256": {"loss": incr_sha},
        "full_packet_eq_loss_only": False,
        "full_packet_eq_loss_only_rationale":
            "the fully-probed batch-28 packet holds 35 WIN rows (honest labels, NOT "
            "adopted) and 11 EXHAUSTED rows (honest UNKNOWN, NOT adopted), so the "
            "adopted packet (7 fresh LOSS rows) != the resolved probed set; aa003 was "
            "already adopted by Part CH and is not re-emitted",
        "win_scenario_exists": True,
        "win_scenario_note":
            "the 35 in-batch WIN rows (aa001/aa002 Parts CC cross-verified, aa006/"
            "aa007 Part CG lane (takeover declared, pending output), aa008/aa009 Part "
            "CM cross-verified; the remaining 29 honest labels) are NOT adopted by "
            "this Part; they stay unconsumed (scrutiny owner C++ second-implementation "
            "gate pin 9193f5b6...; batch-14residual q042 / batch-26 l028 precedents); "
            "loss-only adoption NEVER frees class 5343 while its WIN children stay "
            "unconsumed",
        "unadopted_win_rows": win_rows,
        "exhausted_rows": exhausted_rows,
        "fragment_rows_note":
            "batch-28 has NO fragment keys: the 8 truncated sidecars (aa004.p2 / "
            "aa005.p1 / aa006.p2 / aa007.p2 / aa030.p2 / aa031.p2 / aa034.p2 / aa035.p2) "
            "are bookkeeping only and were re-run fresh-cold by the published "
            "completeness guard; the empty-key junk row + .p1.out artifact of the final "
            "drive-5 invocation are bookkeeping only (no aaNNN verdict row affected)",
        "aa003_base_consistency": {
            "key_id": "aa003", "s5_index": AA003["s5"],
            "key": [AA003["lo"], AA003["hi"]], "legal": AA003["legal"],
            "base_row": [2, AA003["nodes"]],
            "raw_row": [2, AA003["nodes"]],
            "adopted_by": "Part CH (1-LOSS adoption; base cache 6,294 rows 3124461b)",
            "re_emitted": False,
        },
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 7-LOSS adoption increment: only the 7 fresh LOSS rows "
            "(aa015/aa017/aa018/aa023/aa024/aa029/aa036) are consumed into the "
            "canonical cache via the fail-closed union merger; aa003 is asserted "
            "BASE-consistent and not re-emitted; the 35 WIN verdicts are NOT consumed "
            "(unconsumed closure WIN candidates); the 11 EXHAUSTED rows stay honest "
            "UNKNOWN; 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INCREMENT rows=7 loss_nodes={ADOPTED_TOTAL_NODES} -> {incr_path}")


if __name__ == "__main__":
    main()
