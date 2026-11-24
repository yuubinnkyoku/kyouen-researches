#!/usr/bin/env python3
"""Build the batch-29 (class 2251) 16-LOSS canonical-adoption increment, fail-closed.

Prepared for the Part CU adoption: the published batch-29 cumulative evidence
is byte-pinned through the published single batch-29 kit (Part CI scaffold +
takeover drive-1 checkpoint 1/3; kit MANIFEST 7c124233..., 71 files: README 1
+ input 55 (54 per-key input csv + batch-keys.json) + scripts 3 + val-gate 12)
plus the 4 follow-up published takeover-host val-gate files (commit 8b75b786)
plus the published outputs (commit a5a159d7: 32 pass raws ab001..ab016 x p1/p2
and status.log).  The kit files are sha256-verified here file-by-file.

The batch is PARTIALLY probed: 16 of 54 keys (ab001..ab016) are probed
2-pass fresh-cold at budget 15M and ALL 16 are resolved LOSS; the remaining
38 keys (ab017..ab054) are fileless UNPROBED (no raw file exists for them in
the kit; some may hold WIN or EXHAUSTED rows in future drives).  No WIN row
and no EXHAUSTED row has been observed so far among the probed set; the
adopted packet is therefore the whole probed packet so far (full == loss on
the probed subset; the batch as a whole is NOT claimed complete).

Emits the CANONICAL-ADOPTION increment cache over the published raw replay
rows of the resolved fresh LOSS set only:

  * batch-29 (class 2251): the 16 resolved fresh LOSS rows
    ab001..ab016 (total nodes per pass 57,463,971)

The adoption base is the canonical exact-S5 verdict cache BASE =
the Part CO merged 6,301-row cache sha256 854800f3... (the closure chain
through the Part CO batch-28 7-LOSS adoption), byte-pinned here; this maker
ABORTS against anything else.  Every adopted key is asserted fresh (absent
from BASE: the batch-29 rows post-date the Part CO merge) and absent from
the quarantine registry.  No key of the batch-29 probed set is asserted
BASE-consistent because none of them is in BASE.

Fail-closed gates: kit MANIFEST sha-verified file-by-file (71 files); the
4 published takeover-host val-gate files sha-verified and their
(result, nodes) asserted node-exact against the published baselines AND the
kit-pinned batch29-host val-gate outputs (double-host node-exact cross-check
with wall_s excluded); every adopted row must come from BOTH published raw
passes with identical (stones, legal, is_or, budget, result, nodes, lo, hi)
and a completed "# replay_done" line on both passes; legal and (lo,hi) must
match the published batch-keys.json for every probed key; the status.log
(sha-pinned; 16 lines) must carry exactly one PASS row per probed key with
(budget, result, nodes) agreement, no halt rows, no EXHAUSTED rows, no
truncated-retry rows, no junk rows, no EXECUTION-COMPLETE record, and no
line mentioning any unprobed key id; the raw set must be exactly
ab001..ab016 x {p1,p2} (32 files; no sidecars, no fragments); the 16
adopted keys are distinct, ABSENT from the canonical BASE cache and from the
quarantine registry; adopted-row node totals must agree on both passes
(57,463,971); the raw LOSS set must be exactly ab001..ab016 and no raw may
carry result 1 (WIN) or 0 (EXHAUSTED).  Verdicts are byte-taken from the
raws.  The 16 LOSS rows ARE the only thing consumed into the canonical
cache by the Part CU fail-closed merger; 11x11 stays UNKNOWN; nodes are
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
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class5343-loss7-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-20261123.cache"
B29_DIR = ROOT / "research/experiments/n11-centralreply-closure-class2251-batch29-20261123"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"

B29_KEYS_SHA_EXPECTED = "330c0b9f3166e9f6e21b739a851a881d800ab9f58a14dccaa0c772118dee716c"
B29_MANIFEST_SHA_EXPECTED = "7c12423364a292844d4b49a048e910a4be3f9b45cc08a4b31d0bd35233caab84"
B29_KIT_FILES_EXPECTED = 71
B29_STATUS_SHA_EXPECTED = "6b877344b9abea348a9b221f587a771857d3c4091f88fa460ef12595722183e2"
BASE_CACHE_SHA_EXPECTED = "854800f38349277924bc77c50d92a6d5252f11bdb2b2cdb54a14ca2b4f6b087d"
BASE_CACHE_ROWS_EXPECTED = 6301
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"
JSREPLAY_SHA_EXPECTED = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"

# published takeover-host val-gate files (added by commit 8b75b786, after the
# kit MANIFEST was frozen at scaffold time) - pinned here independently
TAKEOVER_VAL_PIN = {
    "at2m-s5-1152921504606851072-536870946.takeover-host.out":
        "ff4dbb8344400c6cc629038e833110e4b5ada5bf24bfa70d07a525d159276a22",
    "at2m-s5-1188950301626860544-536870912.takeover-host.out":
        "eeafe3ac9bf3bed8a5aea5d1f652a1075771b44ab4aa51f8e83e13a4561e3c24",
    "first-15m-s5-1152921504606851072-536870946.takeover-host.out":
        "8675ae4b4904485d5ffde72578342d69668a5c8bd39b82d93193177f515ebafb",
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

ADOPTED_LOSS_IDS = [f"ab{i:03d}" for i in range(1, 17)]
ADOPTED_NODES = {
    "ab001": 4265342, "ab002": 3662776, "ab003": 4447441, "ab004": 2687012,
    "ab005": 3714648, "ab006": 3855756, "ab007": 3763776, "ab008": 2890562,
    "ab009": 1786048, "ab010": 4242063, "ab011": 4806135, "ab012": 2606954,
    "ab013": 2284195, "ab014": 4280600, "ab015": 3912106, "ab016": 4258557,
}
ADOPTED_TOTAL_NODES = 57463971
ADOPTED_S5 = {
    "ab001": 3964, "ab002": 9935, "ab003": 15659, "ab004": 21341,
    "ab005": 26610, "ab006": 33712, "ab007": 38148, "ab008": 42711,
    "ab009": 51145, "ab010": 53947, "ab011": 56596, "ab012": 60153,
    "ab013": 63620, "ab014": 67275, "ab015": 73062, "ab016": 76023,
}
ADOPTED_KEYS = {
    "ab001": (1155314042043105281, 0), "ab002": (1155314042043105282, 0),
    "ab003": (1155314042043105284, 0), "ab004": (1155314042043105288, 0),
    "ab005": (1155314042043105296, 0), "ab006": (1155314042043107328, 0),
    "ab007": (1155314042043109376, 0), "ab008": (1155314042043113472, 0),
    "ab009": (1155314042043138048, 0), "ab010": (1155314042043170816, 0),
    "ab011": (1155314042047299584, 0), "ab012": (1155314042051493888, 0),
    "ab013": (1155314042059882496, 0), "ab014": (1155314042076659712, 0),
    "ab015": (1155314050633039872, 0), "ab016": (1155314059222974464, 0),
}
ADOPTED_LEGAL = {
    "ab001": 95, "ab002": 97, "ab003": 98, "ab004": 92, "ab005": 96,
    "ab006": 96, "ab007": 83, "ab008": 93, "ab009": 87, "ab010": 88,
    "ab011": 92, "ab012": 89, "ab013": 87, "ab014": 91, "ab015": 98,
    "ab016": 96,
}
MEMBERSHIP_EXPECT = {
    "ab001": 4, "ab002": 4, "ab003": 4, "ab004": 4, "ab005": 4, "ab006": 4,
    "ab007": 4, "ab008": 4, "ab009": 4, "ab010": 3, "ab011": 4, "ab012": 4,
    "ab013": 4, "ab014": 4, "ab015": 4, "ab016": 4,
}
FILELESS_UNPROBED_IDS = [f"ab{i:03d}" for i in range(17, 55)]
STATUS_LINES_EXPECTED = 16
STATUS_FINAL_LINE = "2026-11-23T21:52:15Z ab016 PASS 15000000,2,4258557"


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
    lines = path.read_text().splitlines()
    if len(lines) != STATUS_LINES_EXPECTED:
        sys_exit(f"status lines {len(lines)} != {STATUS_LINES_EXPECTED}")
    if lines[-1] != STATUS_FINAL_LINE:
        sys_exit(f"status final line drift: {lines[-1]!r}")
    for line in lines:
        m = re.match(r"^(\S+) (ab\d{3}) PASS (\d+),(\d+),(\d+)$", line)
        if not m:
            sys_exit(f"status line not a clean PASS row: {line!r}")
        kid, b, r, n = m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
        if kid in got:
            sys_exit(f"status key {kid} appears more than once (each-once gate)")
        if kid not in ADOPTED_LOSS_IDS:
            sys_exit(f"status key {kid} is not one of the 16 probed keys")
        got[kid] = (b, r, n)
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

    # --- published takeover-host val-gate files (post-scaffold additions) ------
    takeover_verified = 0
    for name, want in TAKEOVER_VAL_PIN.items():
        p = B29_DIR / "val-gate" / name
        if not p.is_file():
            sys_exit(f"takeover-host val-gate file missing: {name}")
        if sha(p) != want:
            sys_exit(f"takeover-host val-gate sha drift: {name}")
        takeover_verified += 1
    if takeover_verified != 4:
        sys_exit(f"takeover-host val-gate files {takeover_verified} != 4")

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
    if set(status) != set(ADOPTED_LOSS_IDS) or len(status) != 16:
        sys_exit("status probed set != the 16 probed keys")
    joined = "\n".join(slines)
    if re.search(r"\b(WIN-HALT|EXHAUSTED|TRUNCATED|EXECUTION-COMPLETE|P1-FAIL)\b", joined):
        sys_exit("status.log carries an out-of-scope record")
    for uid in FILELESS_UNPROBED_IDS:
        if f" {uid} " in joined:
            sys_exit(f"status.log mentions unprobed key {uid}")

    # --- two-pass raw verification of the 16 probed keys ------------------------
    raws = {}
    for kid in ADOPTED_LOSS_IDS:
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
        if int(bk["s5_index"]) != ADOPTED_S5[kid]:
            sys_exit(f"{kid}: batch-keys s5 drift")
        if int(bk["membership_class_count"]) != MEMBERSHIP_EXPECT[kid]:
            sys_exit(f"{kid}: batch-keys membership drift")
        if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
            sys_exit(f"{kid}: status.log disagreement {status.get(kid)} vs raw {ref}")
        raws[kid] = ref
    loss_set = sorted(k for k, r in raws.items() if r["result"] == 2)
    if loss_set != sorted(ADOPTED_LOSS_IDS):
        sys_exit("the raw LOSS set over the probed keys != the 16 adopted candidates")
    win_set = [k for k, r in raws.items() if r["result"] == 1]
    exh_set = [k for k, r in raws.items() if r["result"] == 0]
    if win_set or exh_set:
        sys_exit(f"probed batch-29 set so far must be pure LOSS (got wins={win_set} exhausted={exh_set})")

    # --- raw file inventory: exactly 32 pass files, no sidecars/fragments ------
    raw_dir = B29_DIR / "output/raw"
    present = sorted(p.name for p in raw_dir.iterdir() if p.is_file())
    expected_files = sorted(f"{kid}.{tag}.out" for kid in ADOPTED_LOSS_IDS for tag in ("p1", "p2"))
    if present != expected_files:
        sys_exit(f"raw inventory drift: {sorted(set(present) ^ set(expected_files))}")

    # --- gate the adopted keys against BASE / quarantine -------------------------
    emitted_keys = set()
    for kid in ADOPTED_LOSS_IDS:
        key = (raws[kid]["lo"], raws[kid]["hi"])
        if key != ADOPTED_KEYS[kid]:
            sys_exit(f"{kid}: raw key != pinned adopted key")
        if key in quarantined:
            sys_exit(f"{kid}: quarantined key {key}")
        if key in base_keys:
            sys_exit(f"{kid}: key already in canonical BASE cache {key} "
                     f"(base={base_keys[key]}, raw=(result {raws[kid]['result']}, nodes {raws[kid]['nodes']})); "
                     "the batch-29 rows post-date the Part CO merge (fresh-increment gate)")
        if key in emitted_keys:
            sys_exit(f"{kid}: duplicate emitted key {key}")
        emitted_keys.add(key)

    # --- the 16 fresh adopted LOSS rows -----------------------------------------
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

    # --- val-gate double-host node-exact cross-check (kit + takeover) ----------
    for gate, (exp_r, exp_n) in VAL_GATE_EXPECT.items():
        for host in ("published-baseline", "batch29-host", "takeover-host"):
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
        "# n11 central-reply closure batch-29 (class 2251) 16-LOSS",
        "#   canonical-adoption increment (Part CU, 2026-11-23)",
        "# published batch-29 kit (Part CI scaffold + takeover drive-1 checkpoint 1/3):",
        "#   16 of 54 keys probed 2-pass fresh-cold at budget 15M, ALL 16 resolved",
        "#   LOSS; the remaining 38 keys ab017..ab054 are fileless UNPROBED (they",
        "#   may hold WIN or EXHAUSTED rows in future drives; the batch is NOT",
        "#   claimed complete).  No WIN row and no EXHAUSTED row is observed so",
        "#   far in this batch; the adopted packet is the whole probed packet.",
        "# 2-pass node-exact exact-S5 verdict at budget 15M, fresh cold, pinned",
        "#   jsreplay.js sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# gates: kit MANIFEST sha-verified file-by-file (71 files); the 4",
        "#   published takeover-host val-gate files pinned and verified double-",
        "#   host node-exact against the kit batch29-host outputs and the",
        "#   published baselines; all 16 probed keys two-pass node-exact with",
        "#   '# replay_done' on both passes; status.log (16 lines, sha-pinned,",
        "#   clean PASS-only picture) each-once agreement on (b,r,n); raw",
        "#   inventory exactly ab001..ab016 x {p1,p2} (no sidecars, no",
        "#   fragments); batch-keys legal/(lo,hi)/s5/membership agreement;",
        "#   adopted-row per-pass node total 57,463,971; adopted keys distinct",
        "#   and absent from BASE and from the quarantine registry.",
        "# ADOPTED set = ab001..ab016 (16 keys, s5 indices 3964..76023,",
        "#   membership 4 except ab010 (3)).  full == loss ON THE PROBED SET",
        "#   only (16/16 LOSS so far); the 38 fileless keys stay UNPROBED and",
        "#   NO completeness claim is made for the batch as a whole.",
        "# The 16 LOSS rows ARE consumed into the canonical cache by the Part",
        "#   CT fail-closed union merger; 11x11 stays UNKNOWN; nodes are",
        "#   bookkeeping, never verdicts.",
    ]
    rows_for_sort = [(ADOPTED_KEYS[k][0], ADOPTED_KEYS[k][1], ADOPTED_NODES[k])
                     for k in ADOPTED_LOSS_IDS]
    rowlines = [f"s5verdict,{lo},{hi},5,2,{nodes}" for lo, hi, nodes in sorted(rows_for_sort)]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_path = OUT / "increment-b29loss16-20261123.cache"
    incr_path.write_bytes(blob)
    incr_sha = hashlib.sha256(blob).hexdigest()

    manifest = {
        "schema": "b29loss16-increments-manifest-v1",
        "batches": [{
            "batch": 29,
            "class_index": 2251,
            "keys_total": 54,
            "adopted_loss_ids": list(ADOPTED_LOSS_IDS),
            "already_adopted_ids": [],
            "unadopted_win_ids": [],
            "exhausted_excluded_ids": [],
            "probed_ids": list(ADOPTED_LOSS_IDS),
            "fragment_ids": [],
            "fileless_unprobed_count": 38,
            "fileless_unprobed_ids": list(FILELESS_UNPROBED_IDS),
            "input_sha256": B29_KEYS_SHA_EXPECTED,
            "status_log_sha256": B29_STATUS_SHA_EXPECTED,
            "status_log_lines": STATUS_LINES_EXPECTED,
            "status_log_final_line": STATUS_FINAL_LINE,
            "kit_integrity": {
                "manifest_sha256": B29_MANIFEST_SHA_EXPECTED,
                "files_verified": kit_verified,
            },
            "takeover_val_gate_files": dict(sorted(TAKEOVER_VAL_PIN.items())),
            "val_gate_double_host_node_exact": True,
            "total_nodes_pass_one": nodes_p1_total,
            "total_nodes_pass_two": nodes_p2_total,
            "stop_rule": "takeover drive-1 checkpoint 1/3 (16/54 keys probed; the "
                         "takeover session halted after the checkpoint; probed keys "
                         "all ran to 2-pass completion; verdict not consumed)",
            "fragment_state": {},
        }],
        "resolved_ids": list(ADOPTED_LOSS_IDS),
        "loss_ids": list(ADOPTED_LOSS_IDS),
        "win_ids": [],
        "unadopted_win_ids": [],
        "exhausted_excluded_ids": [],
        "row_counts": {
            "probed_rows": 16, "adopted_loss_rows": 16, "wins": 0,
            "exhausted_excluded": 0, "fragments_unprobed": 0, "fileless_unprobed": 38,
        },
        "sha256": {"loss": incr_sha},
        "full_packet_eq_loss_only": True,
        "full_packet_eq_loss_only_rationale":
            "ON THE PROBED SET the packet is pure LOSS: all 16 probed keys resolved "
            "LOSS and all 16 are adopted, so the adopted packet == the probed packet "
            "so far; BUT the batch is NOT complete: 38 keys (ab017..ab054) are "
            "fileless UNPROBED and may contain WIN or EXHAUSTED rows in future "
            "drives, so NO completeness claim is made for the batch as a whole and "
            "class 2251 is NOT freed",
        "win_scenario_exists": False,
        "win_scenario_note":
            "no WIN row is observed among the 16 probed batch-29 keys so far; the "
            "38 fileless keys are UNPROBED and their verdicts are NOT known; a "
            "future WIN in this batch stays unconsumed by adoption parts (scrutiny "
            "owner C++ second-implementation gate pin 9193f5b6...; batch-14residual "
            "q042 / batch-26 l028 / batch-28 35-WIN precedents); loss-only adoption "
            "NEVER frees class 2251 while any unknown child remains",
        "unadopted_win_rows": [],
        "exhausted_rows": [],
        "fragment_rows_note":
            "batch-29 drive-1 has NO fragment keys and NO truncated sidecars: the "
            "raw inventory is exactly ab001..ab016 x {p1,p2} (32 files)",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_sha256": BASE_CACHE_SHA_EXPECTED,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "base_cache_absent_hits_for_emitted": 0,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical 16-LOSS adoption increment: only the 16 fresh LOSS rows "
            "(ab001..ab016) are consumed into the canonical cache via the "
            "fail-closed union merger; the 38 remaining batch-29 keys are fileless "
            "UNPROBED (no verdict claimed); adopting 16 of 54 keys does NOT free "
            "class 2251 (38 unknown children remain); 11x11 stays UNKNOWN; nodes "
            "are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INCREMENT rows=16 loss_nodes={ADOPTED_TOTAL_NODES} -> {incr_path}")


if __name__ == "__main__":
    main()
