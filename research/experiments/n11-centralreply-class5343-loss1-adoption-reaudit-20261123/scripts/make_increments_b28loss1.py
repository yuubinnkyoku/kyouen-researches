#!/usr/bin/env python3
"""Build the batch-28 (class 5343) 1-LOSS canonical-adoption increment, fail-closed.

Prepared for the Part CH adoption: the published batch-28 drive-2 packet
(class 5343, Part CD kit MANIFEST 2811b577, 96 files all sha256-verified
here; raws 10 = aa001..aa007 p1/p2 complete, plus 4 truncated sidecars
published as bookkeeping; status.log 343097c2; row-audit-winhalt 3e86a32b
(winhalt schema); batch-keys.json af19208f, 54 keys).  The batch is NOT a
complete enumeration book: batch-28 drive-1 probed aa001/aa002 (2-PAIR
WIN-HALT record, Part CB) and drive-2 probed aa003..aa007 (Part CD):
1 resolved LOSS row (aa003), 2 EXHAUSTED honest-UNKNOWN rows (aa004,
aa005: result 0 at budget 15M, same-condition re-probe not performed),
and 2 further WIN rows (aa006, aa007).  The remaining 47 keys (aa008..
aa054) are fileless UNPROBED and are not touched by this Part.

Emits the CANONICAL-ADOPTION increment cache over the published raw replay
rows of the resolved LOSS set only:

  * batch-28 (class 5343): the 1 resolved LOSS row aa003

The in-batch WIN rows aa001, aa002 (Part CC third-implementation
cross-verified) and aa006, aa007 (Part CG lane declared by a sibling
execution; cross-verification pending there) are HONEST LABELS ONLY and
are NOT adopted: they stay unconsumed (scrutiny owner C++ second-
implementation gate pin 9193f5b6...), like the batch-14residual q042 /
batch-26 l028 precedents (loss-only adoption with in-batch WINs left
unconsumed).  full != loss here (machine-stated): the adopted packet is
the 1-LOSS packet of a partially-probed batch.  The EXHAUSTED rows
aa004/aa005 carry NO verdict and are excluded (honest UNKNOWN).

The adoption base is the canonical exact-S5 verdict cache BASE = 6,293
rows sha256 9115be9e... (Part BZ adoption output), byte-pinned here; this
maker ABORTS against anything else.

Fail-closed gates: the adopted increment row must come from BOTH published
raw passes with identical (stones, legal, is_or, budget, result, nodes) and
a completed "# replay_done" line; legal and (lo,hi) must match the
published batch-keys.json for every key; the 4 WIN rows are likewise
two-pass re-verified (result 1) and their keys are asserted ABSENT from the
BASE cache and the quarantine registry and NOT emitted into the increment;
the 2 EXHAUSTED rows are two-pass re-verified (result 0, nodes==budget) and
asserted NOT emitted (honest UNKNOWN; absence from BASE is structural and
also asserted); every status.log PASS row must agree with the raws on
(budget, result, nodes); the status.log probed set must be exactly the
published probed set each-once (7 dated PASS rows), the WIN set must be
exactly the recorded unadopted WINs (aa001, aa002, aa006, aa007), the
exhaustion set must be exactly {aa004, aa005} with the published EXHAUSTED
records, the stop rows must be exactly the published WIN-HALT pairs (the
aa001, aa002, aa006, aa007 2-line pairs) and no other stop row may exist;
the truncated-retry bookkeeping lines must be exactly the published 4; no
EXECUTION-COMPLETE row anywhere; the published row-audit-winhalt summary
must agree (schema, class, batch, keys_total, probed, pass_rows, loss_rows,
win_rows, exhausted_rows, fragment/bookkeeping, mismatches 0, input_sha256);
all kit files must verify against the published MANIFEST (kit integrity
gate, 96 files); adopted-row pass node totals must agree on both passes
(4,070,373); the adopted key is distinct, ABSENT from the canonical BASE
cache (6,293 rows; ANY overlap ABORTS - the batch-28 rows post-date the
Part BZ merge), and absent from the quarantine registry.  Verdicts are
byte-taken from the raws.  The 1 LOSS row IS consumed into the canonical
cache by the Part CH fail-closed merger; no WIN verdict is consumed
anywhere.  11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.
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
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class16957-13342-loss6-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-plus-batch24loss2-plus-batch27loss4-20261123.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BATCH28_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5343-batch28-drive2-20261123"

B28_KEYS_SHA_EXPECTED = "af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5"
B28_ROW_AUDIT_SHA_EXPECTED = "3e86a32b847b5799594be5fbee6624878deadf02990940b2503f931d7af30e91"
B28_STATUS_SHA_EXPECTED = "343097c268425cc62263935f1063c26689515bc797c68bbdb82389c713952c98"
B28_MANIFEST_SHA_EXPECTED = "2811b577f01a29e0bbdafbf3a4d9bb6237851246753d02ad86f025a75d560713"
B28_KIT_FILES_EXPECTED = 96
BASE_CACHE_SHA_EXPECTED = "9115be9eca1e60828a90c50041f511b598ef79fc0be76d5e16821816e478e93e"
BASE_CACHE_ROWS_EXPECTED = 6293
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"

BUDGET = 15000000

B28 = {
    "id": 28, "dir": BATCH28_DIR, "class": 5343, "keysid": "aa", "keys_total": 54,
    "keys_sha": B28_KEYS_SHA_EXPECTED,
    "row_audit_sha": B28_ROW_AUDIT_SHA_EXPECTED,
    "status_sha": B28_STATUS_SHA_EXPECTED,
    "manifest_sha": B28_MANIFEST_SHA_EXPECTED,
    "kit_files": B28_KIT_FILES_EXPECTED,
    "input_schema": "n11-centralreply-closure-class5343-batch28-input-v1",
    "row_audit_schema": "n11-centralreply-closure-class5343-batch28-rowaudit-winhalt-v1",
    "probed": ["aa001", "aa002", "aa003", "aa004", "aa005", "aa006", "aa007"],
    "adopted_loss_ids": ["aa003"],
    "unadopted_win_ids": ["aa001", "aa002", "aa006", "aa007"],
    "exhausted_ids": ["aa004", "aa005"],
    "fragments": [],
    "status_lines_expected": 17,
    "final_row_expected": "2026-11-23T16:23:05Z aa006 WIN-HALT",
    "status_win_pairs": [
        ("2026-11-23T15:22:39Z aa002 PASS 15000000,1,6527041",
         "2026-11-23T15:22:39Z aa002 WIN-HALT"),
        ("2026-11-23T15:23:55Z aa001 PASS 15000000,1,13183855",
         "2026-11-23T15:23:55Z aa001 WIN-HALT"),
        ("2026-11-23T16:22:56Z aa007 PASS 15000000,1,13483540",
         "2026-11-23T16:22:56Z aa007 WIN-HALT"),
        ("2026-11-23T16:23:05Z aa006 PASS 15000000,1,14303810",
         "2026-11-23T16:23:05Z aa006 WIN-HALT"),
    ],
    "status_exhausted_pairs": [
        ("2026-11-23T16:10:42Z aa004 PASS 15000000,0,15000000",
         "2026-11-23T16:10:42Z aa004 EXHAUSTED 15000000,0,15000000"),
        ("2026-11-23T16:14:18Z aa005 PASS 15000000,0,15000000",
         "2026-11-23T16:14:18Z aa005 EXHAUSTED 15000000,0,15000000"),
    ],
    "truncated_retry_rows_expected": {
        ("aa004", "P2"), ("aa005", "P1"), ("aa006", "P2"), ("aa007", "P2"),
    },
    "adopted_nodes_pass_expected": 4070373,
    "truncated_sidecars": [
        "output/raw/aa004.p2.truncated.160858.out",
        "output/raw/aa005.p1.truncated.161058.out",
        "output/raw/aa006.p2.truncated.161949.out",
        "output/raw/aa007.p2.truncated.161949.out",
    ],
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_replay(path: Path):
    row = None
    for line in path.read_text().splitlines():
        if line.startswith("replay,"):
            parts = line.split(",")
            if row is not None:
                sys.exit(f"ABORT multiple replay rows in {path}")
            row = {
                "stones": int(parts[2]), "legal": int(parts[3]),
                "is_or": int(parts[4]),
                "budget": int(parts[5]), "result": int(parts[6]),
                "nodes": int(parts[7]), "wall_s": int(parts[8]),
                "lo": int(parts[9]), "hi": int(parts[10]),
            }
    if row is None:
        sys.exit(f"ABORT no replay row in {path}")
    return row


def parse_status(path: Path):
    got = {}
    for line in path.read_text().splitlines():
        m = re.match(r"^(\S+) (\S+) PASS (\d+),(\d+),(\d+)$", line)
        if m:
            kid, b, r, n = m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
            if kid in got:
                sys.exit(f"ABORT status key {kid} appears more than once (each-once gate)")
            got[kid] = (b, r, n)
    return got


def two_pass(batch: dict, kid: str):
    variants = {}
    for tag in ("p1", "p2"):
        p = batch["dir"] / f"output/raw/{kid}.{tag}.out"
        if not p.is_file():
            sys.exit(f"ABORT missing raw {p}")
        txt = p.read_text()
        if "# replay_done" not in txt:
            sys.exit(f"ABORT raw {p} lacks the '# replay_done' completeness guard")
        variants[tag] = parse_replay(p)
    ref = variants["p1"]
    fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
    for tag, r in variants.items():
        if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
            sys.exit(f"ABORT {kid}: pass mismatch {tag} {r} vs p1 {ref}")
    return ref


def verify_batch(batch: dict):
    d = batch["dir"]
    if sha(d / "input/batch-keys.json") != batch["keys_sha"]:
        sys.exit(f"ABORT batch-{batch['id']} batch-keys.json sha drift")
    if sha(d / "output/row-audit-winhalt.json") != batch["row_audit_sha"]:
        sys.exit(f"ABORT batch-{batch['id']} row-audit-winhalt.json sha drift")
    if sha(d / "output/status.log") != batch["status_sha"]:
        sys.exit(f"ABORT batch-{batch['id']} status.log sha drift")
    if sha(d / "MANIFEST-sha256.txt") != batch["manifest_sha"]:
        sys.exit(f"ABORT batch-{batch['id']} kit MANIFEST sha drift")

    # --- kit integrity gate: every published kit file must verify -----------
    kit_verified = 0
    for line in (d / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        want, rel = line.split(None, 1)
        p = d / rel
        if not p.is_file():
            sys.exit(f"ABORT batch-{batch['id']} kit file missing: {rel}")
        if sha(p) != want:
            sys.exit(f"ABORT batch-{batch['id']} kit file sha drift: {rel}")
        kit_verified += 1
    if kit_verified != batch["kit_files"]:
        sys.exit(f"ABORT batch-{batch['id']} kit files verified {kit_verified} != {batch['kit_files']}")
    batch["kit_verified"] = kit_verified

    keys = json.loads((d / "input/batch-keys.json").read_text())["keys"]
    bk_all = json.loads((d / "input/batch-keys.json").read_text())
    if bk_all["schema"] != batch["input_schema"]:
        sys.exit(f"ABORT batch-{batch['id']} batch-keys schema drift: {bk_all['schema']}")
    if bk_all["class_index"] != batch["class"] or bk_all["budget"] != BUDGET:
        sys.exit(f"ABORT batch-{batch['id']} batch-keys class/budget drift")
    by_id = {k["key_id"]: k for k in keys}
    if len(by_id) != batch["keys_total"]:
        sys.exit(f"ABORT batch-{batch['id']} batch-keys key count {len(by_id)} != {batch['keys_total']}")
    if bk_all["closure_class_rank_in_published_base"] != 27:
        sys.exit("ABORT batch-28 batch-keys closure rank drift")
    if int(bk_all["published_base_canonical_rows"]) != BASE_CACHE_ROWS_EXPECTED:
        sys.exit("ABORT batch-28 batch-keys published_base_canonical_rows drift")

    # --- status.log: the whole published picture -----------------------------
    status = parse_status(d / "output/status.log")
    probed = batch["probed"]
    if set(status) != set(probed):
        sys.exit(f"ABORT batch-{batch['id']} status probed set != published probed set: "
                 f"{sorted(set(status) ^ set(probed))}")
    if len(status) != len(probed):
        sys.exit(f"ABORT batch-{batch['id']} status each-once violation: {len(status)} vs {len(probed)}")
    status_wins = {k for k, v in status.items() if k in probed and v[1] == 1}
    if status_wins != set(batch["unadopted_win_ids"]):
        sys.exit(f"ABORT batch-{batch['id']} WIN set {sorted(status_wins)} != unadopted {sorted(batch['unadopted_win_ids'])}")
    status_exhausted = {k for k, v in status.items() if k in probed and v[1] == 0}
    if status_exhausted != set(batch["exhausted_ids"]):
        sys.exit(f"ABORT batch-{batch['id']} exhausted set {sorted(status_exhausted)} != {sorted(batch['exhausted_ids'])}")
    lines = (d / "output/status.log").read_text().strip().splitlines()
    if len(lines) != batch["status_lines_expected"]:
        sys.exit(f"ABORT batch-{batch['id']} status.log line count {len(lines)} != {batch['status_lines_expected']}")
    if lines[-1] != batch["final_row_expected"]:
        sys.exit(f"ABORT batch-{batch['id']} status.log final line drift: {lines[-1]}")
    if "EXECUTION-COMPLETE" in "\n".join(lines):
        sys.exit(f"ABORT batch-{batch['id']} unexpected EXECUTION-COMPLETE record")
    # stop rows: exactly the 4 published WIN-HALT rows (all halt-type rows are WIN-HALT)
    halt_rows = [ln for ln in lines if re.match(r"^\S+ \S+ (WIN-HALT|HARD-STOP|EXHAUSTED)( |$)", ln)]
    expected_halts = [h for pair in batch["status_win_pairs"] for h in [pair[1]]] + \
                      [pair[1] for pair in batch["status_exhausted_pairs"]]
    if sorted(halt_rows) != sorted(expected_halts):
        sys.exit(f"ABORT batch-{batch['id']} stop/EXHAUSTED rows must be exactly the published rows: {halt_rows}")
    for pass_row, halt_row in batch["status_win_pairs"]:
        if lines.count(pass_row) != 1:
            sys.exit(f"ABORT batch-{batch['id']} status.log lacks the published WIN pass row: {pass_row}")
        idx = lines.index(pass_row)
        if idx + 1 >= len(lines) or lines[idx + 1] != halt_row:
            sys.exit(f"ABORT batch-{batch['id']} WIN PASS row not directly followed by its dated WIN-HALT row: {pass_row}")
    for pass_row, ex_row in batch["status_exhausted_pairs"]:
        if lines.count(pass_row) != 1:
            sys.exit(f"ABORT batch-{batch['id']} status.log lacks the published EXHAUSTED pass row: {pass_row}")
        idx = lines.index(pass_row)
        if idx + 1 >= len(lines) or lines[idx + 1] != ex_row:
            sys.exit(f"ABORT batch-{batch['id']} EXHAUSTED PASS row not directly followed by its dated EXHAUSTED row: {pass_row}")
    # truncated-retry bookkeeping lines: exactly the published 4
    retry_rows = set()
    for ln in lines:
        m = re.match(r"^(\S+) (\S+) (P[12])-TRUNCATED-RETRY$", ln)
        if m:
            retry_rows.add((m.group(2), m.group(3)))
    if retry_rows != batch["truncated_retry_rows_expected"]:
        sys.exit(f"ABORT batch-{batch['id']} truncated-retry rows {sorted(retry_rows)} != published")
    # every truncated sidecar must exist and carry NO replay_done / replay row
    for rel in batch["truncated_sidecars"]:
        sp = d / rel
        if not sp.is_file():
            sys.exit(f"ABORT batch-{batch['id']} truncated sidecar missing: {rel}")
        stxt = sp.read_text()
        if "# replay_done" in stxt or re.search(r"^replay,", stxt, re.M):
            sys.exit(f"ABORT batch-{batch['id']} truncated sidecar carries evidence: {rel}")

    # --- row-audit-winhalt.json: derived-state agreement ---------------------
    ra = json.loads((d / "output/row-audit-winhalt.json").read_text())
    if ra["schema"] != batch["row_audit_schema"]:
        sys.exit(f"ABORT batch-{batch['id']} row-audit schema drift: {ra['schema']}")
    if ra["class_index"] != batch["class"] or ra["batch"] != batch["id"]:
        sys.exit(f"ABORT batch-{batch['id']} row-audit header drift")
    if ra["keys_total"] != batch["keys_total"] or ra["probed"] != len(probed):
        sys.exit(f"ABORT batch-{batch['id']} row-audit keys_total/probed drift")
    if ra["loss_rows"] != batch["adopted_loss_ids"]:
        sys.exit(f"ABORT batch-{batch['id']} row-audit loss_rows drift: {ra['loss_rows']}")
    if ra["win_rows"] != batch["unadopted_win_ids"]:
        sys.exit(f"ABORT batch-{batch['id']} row-audit win_rows drift: {ra['win_rows']}")
    if ra["exhausted_rows"] != batch["exhausted_ids"] or ra["mismatches"] != 0:
        sys.exit(f"ABORT batch-{batch['id']} row-audit exhaustion/mismatch drift")
    if ra["pass_rows"] != 1:
        sys.exit(f"ABORT batch-{batch['id']} row-audit pass_rows drift: {ra['pass_rows']}")
    if ra["fragment_keys"] != {}:
        sys.exit(f"ABORT batch-{batch['id']} row-audit fragment bookkeeping drift (must be empty)")
    if ra["input_sha256"] != batch["keys_sha"]:
        sys.exit(f"ABORT batch-{batch['id']} row-audit input_sha256 drift")
    fileless_expected = sorted(
        set(f"{batch['keysid']}{i:03d}" for i in range(1, batch["keys_total"] + 1))
        - set(probed) - set(batch["fragments"]))
    if ra["fileless_unprobed"] != fileless_expected or ra["unprobed_count"] != len(fileless_expected):
        sys.exit(f"ABORT batch-{batch['id']} row-audit fileless/unprobed bookkeeping drift")
    return status, by_id


def main() -> None:
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys.exit("ABORT base cache sha drift")
    merger = EXP / "scripts/s5_union_merge.py"
    if sha(merger) != MERGER_SHA_EXPECTED:
        sys.exit("ABORT fail-closed union merger (scripts/s5_union_merge.py) sha drift: "
                 "this Part must use the pinned merger byte-for-byte")

    base_keys = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    if len(base_keys) != BASE_CACHE_ROWS_EXPECTED:
        sys.exit(f"ABORT base cache rows {len(base_keys)} != {BASE_CACHE_ROWS_EXPECTED}")
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    batch = B28
    status, by_id = verify_batch(batch)
    emitted_keys = set()

    # --- the single adopted LOSS row: aa003 ---------------------------------
    ref = two_pass(batch, "aa003")
    if ref["budget"] != BUDGET or ref["stones"] != 5 or ref["is_or"] != 0:
        sys.exit(f"ABORT aa003: wrong budget/depth {ref}")
    if ref["result"] != 2:
        sys.exit(f"ABORT aa003: adopted row must be result 2, got {ref['result']}")
    if ref["nodes"] != batch["adopted_nodes_pass_expected"]:
        sys.exit(f"ABORT aa003: adopted-row nodes drift {ref['nodes']}")
    bk = by_id.get("aa003")
    if bk is None:
        sys.exit("ABORT batch-keys.json missing aa003")
    if ref["legal"] != int(bk["legal"]):
        sys.exit(f"ABORT aa003: legal mismatch raw={ref['legal']} keys={bk['legal']}")
    if (ref["lo"], ref["hi"]) != (int(bk["lo"]), int(bk["hi"])):
        sys.exit(f"ABORT aa003: key mismatch raw=({ref['lo']},{ref['hi']}) keys=({bk['lo']},{bk['hi']})")
    if status.get("aa003") != (ref["budget"], ref["result"], ref["nodes"]):
        sys.exit(f"ABORT aa003: status.log disagreement {status.get('aa003')}")
    key = (ref["lo"], ref["hi"])
    if key in quarantined:
        sys.exit(f"ABORT aa003: quarantined key {key}")
    if key in base_keys:
        sys.exit(f"ABORT aa003: key already in canonical BASE cache {key} "
                 f"(base={base_keys[key]}, raw={(ref['result'], ref['nodes'])})")
    emitted_keys.add(key)
    # second-pass node recomputation (independent of the parse)
    n_p2 = sum(int(line.split(",")[7])
               for line in (batch["dir"] / "output/raw/aa003.p2.out").read_text().splitlines()
               if line.startswith("replay,"))
    if n_p2 != ref["nodes"]:
        sys.exit(f"ABORT aa003: adopted-row pass node totals disagree: {n_p2} vs {ref['nodes']}")

    # --- unadopted WIN rows: two-pass re-verified honest labels --------------
    win_rows = []
    for kid in batch["unadopted_win_ids"]:
        winref = two_pass(batch, kid)
        winbk = by_id[kid]
        if winref["result"] != 1 or winref["budget"] != BUDGET or winref["stones"] != 5 or winref["is_or"] != 0:
            sys.exit(f"ABORT {kid}: WIN row not the published honest label: {winref}")
        if (winref["lo"], winref["hi"]) != (int(winbk["lo"]), int(winbk["hi"])):
            sys.exit(f"ABORT {kid}: key mismatch raw vs batch-keys")
        if winref["legal"] != int(winbk["legal"]):
            sys.exit(f"ABORT {kid}: legal mismatch raw={winref['legal']} keys={winbk['legal']}")
        if status.get(kid) != (winref["budget"], winref["result"], winref["nodes"]):
            sys.exit(f"ABORT {kid}: status.log disagreement")
        winkey = (winref["lo"], winref["hi"])
        if winkey in base_keys:
            sys.exit(f"ABORT {kid}: unadopted WIN key already in BASE cache {winkey}")
        if winkey in quarantined:
            sys.exit(f"ABORT {kid}: quarantined key {winkey}")
        if winkey in emitted_keys:
            sys.exit(f"ABORT {kid} WIN key leaked into the adopted rows")
        cross = ("Part CC third-implementation cross-verified"
                 if kid in ("aa001", "aa002")
                 else "Part CG cross-verification lane declared (pending output)")
        win_rows.append({
            "key_id": kid, "batch": batch["id"], "class_index": batch["class"],
            "s5_index": int(winbk["s5_index"]), "lo": winref["lo"], "hi": winref["hi"],
            "legal": winref["legal"], "result": winref["result"], "nodes": winref["nodes"],
            "two_pass_node_exact": True,
            "note": f"honest label only, never adopted in this Part ({cross}; "
                    "stays unconsumed)",
        })

    # --- EXHAUSTED rows: honest UNKNOWN, never emitted -----------------------
    exhausted_rows = []
    for kid in batch["exhausted_ids"]:
        exref = two_pass(batch, kid)
        exbk = by_id[kid]
        if exref["result"] != 0 or exref["nodes"] != BUDGET or exref["budget"] != BUDGET:
            sys.exit(f"ABORT {kid}: EXHAUSTED row not the published budget-exhaustion record: {exref}")
        if (exref["lo"], exref["hi"]) != (int(exbk["lo"]), int(exbk["hi"])):
            sys.exit(f"ABORT {kid}: key mismatch raw vs batch-keys")
        if exref["legal"] != int(exbk["legal"]):
            sys.exit(f"ABORT {kid}: legal mismatch raw={exref['legal']} keys={exbk['legal']}")
        if status.get(kid) != (exref["budget"], exref["result"], exref["nodes"]):
            sys.exit(f"ABORT {kid}: status.log disagreement (exhausted)")
        exkey = (exref["lo"], exref["hi"])
        if exkey in base_keys:
            sys.exit(f"ABORT {kid}: EXHAUSTED key already in BASE cache {exkey}")
        if exkey in quarantined:
            sys.exit(f"ABORT {kid}: quarantined key {exkey}")
        if exkey in emitted_keys:
            sys.exit(f"ABORT {kid} EXHAUSTED key leaked into the adopted rows")
        exhausted_rows.append({
            "key_id": kid, "batch": batch["id"], "class_index": batch["class"],
            "s5_index": int(exbk["s5_index"]), "lo": exref["lo"], "hi": exref["hi"],
            "legal": exref["legal"], "result": exref["result"], "nodes": exref["nodes"],
            "two_pass_node_exact": True,
            "note": "budget exhaustion at 15M (honest UNKNOWN; same-condition re-probe "
                    "not performed; NOT adopted, NOT emitted; nodes are bookkeeping",
        })

    # --- emit the increment + manifest --------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    hdr = [
        "# n11 central-reply closure batch-28 (class 5343) 1-LOSS",
        "#   canonical-adoption increment (Part CH, 2026-11-23)",
        "# published Part CH declaration (note amendment 2026-11-23; single-owner: loss-only",
        "#   adoption; the in-batch WIN rows aa001/aa002 (Part CC third-implementation",
        "#   cross-verified) and aa006/aa007 (Part CG lane declared; pending) are honest",
        "#   labels only and are NOT adopted; the EXHAUSTED rows aa004/aa005 are honest",
        "#   UNKNOWN bookkeeping, NOT adopted).",
        "# 2-pass node-exact exact-S5 verdict at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# batch-28 probed 7/54 keys across drive-1 (Part CB: aa001/aa002 WIN-HALT) and",
        "#   drive-2 (Part CD: aa003 LOSS row, aa004/aa005 EXHAUSTED, aa006/aa007",
        "#   WIN-HALT pairs published; 47 fileless UNPROBED).  The batch is NOT a complete",
        "#   enumeration book: only the resolved LOSS row below is adopted.",
        "#   the remaining keys stay UNKNOWN in canonical and untouched by this Part.",
        "# gates: kit MANIFEST sha verification (96 files), 2-way (p1/p2) node-exact +",
        "#   '# replay_done' completeness, status.log each-once agreement (b,r,n) per key,",
        "#   WIN set == unadopted, exhaustion set == {aa004, aa005} with published",
        "#   EXHAUSTED records, WIN-HALT 2-line pair pins, truncated-retry row pins +",
        "#   sidecar evidence-absence gate, row-audit-winhalt schema agreement,",
        "#   batch-keys legal/(lo,hi) agreement, adopted-row pass node sum (4,070,373),",
        "#   adopted key distinct, ZERO BASE-cache overlap (structural gate: batch-28 rows",
        "#   post-date the Part BZ merge; any overlap ABORTs), quarantine 0, WIN rows",
        "#   two-pass re-verified + presence bookkeeping (asserted NOT adopted),",
        "#   EXHAUSTED rows two-pass re-verified + asserted NOT emitted.",
        "# ADOPTED set = {aa003}.  full != loss here (machine-stated): the resolved",
        "#   packet additionally holds the aa001/aa002/aa006/aa007 WIN rows and the",
        "#   aa004/aa005 EXHAUSTED rows; the WIN verdicts stay UNCONSUMED (scrutiny",
        "#   owner C++ second-implementation gate pin 9193f5b6...; batch-14residual q042 /",
        "#   batch-26 l028 precedents); no WIN verdict is consumed anywhere by this Part;",
        "#   the unconsumed closure WIN candidates (aa001/aa002/aa006/aa007 among them)",
        "#   are untouched.",
        "# The 1 LOSS row IS consumed into the canonical cache by the Part CH merger;",
        "#   11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.",
        "# 1 row: the adopted LOSS verdict of class 5343's probed unknown S5 child",
        "#   aa003 (batch 28, s5 104943).",
    ]
    rowlines = [f"s5verdict,{ref['lo']},{ref['hi']},5,{ref['result']},{ref['nodes']}"]
    blob = ("\n".join(hdr + rowlines) + "\n").encode("utf-8")
    incr_path = OUT / "increment-b28loss1-20261123.cache"
    incr_path.write_bytes(blob)

    manifest = {
        "schema": "b28loss1-increments-manifest-v1",
        "batches": [{
            "batch": 28,
            "class_index": 5343,
            "keys_total": 54,
            "adopted_loss_ids": ["aa003"],
            "unadopted_win_ids": ["aa001", "aa002", "aa006", "aa007"],
            "exhausted_excluded_ids": ["aa004", "aa005"],
            "probed_ids": list(status.keys()),
            "fragment_ids": [],
            "fileless_unprobed_count": 47,
            "input_sha256": batch["keys_sha"],
            "row_audit_sha256": batch["row_audit_sha"],
            "status_log_sha256": batch["status_sha"],
            "status_log_stop_records": [
                {"pass_row": pair[0], "halt_row": pair[1]} for pair in batch["status_win_pairs"]
            ],
            "status_log_exhausted_records": [
                {"pass_row": pair[0], "exhausted_row": pair[1]} for pair in batch["status_exhausted_pairs"]
            ],
            "status_log_final_row": batch["final_row_expected"],
            "stop_rule": "pre-registered WIN-HALT (Part CB drive-1 aa001/aa002 2-line pairs + "
                         "Part CD drive-2 aa006/aa007 2-line pairs and aa003 LOSS row + "
                         "aa004/aa005 EXHAUSTED records; verdict not consumed)",
            "total_nodes_pass_one": ref["nodes"],
            "total_nodes_pass_two": n_p2,
            "kit_integrity": {
                "manifest_sha256": batch["manifest_sha"],
                "files_verified": batch["kit_verified"],
            },
            "fragment_state": {},
        }],
        "resolved_ids": list(status.keys()),
        "loss_ids": ["aa003"],
        "win_ids": batch["unadopted_win_ids"],
        "unadopted_win_ids": batch["unadopted_win_ids"],
        "exhausted_excluded_ids": batch["exhausted_ids"],
        "row_counts": {
            "probed_rows": 7, "adopted_loss_rows": 1, "wins": 4,
            "exhausted_excluded": 2, "fragments_unprobed": 0, "fileless_unprobed": 47,
        },
        "sha256": {"loss": hashlib.sha256(blob).hexdigest()},
        "full_packet_eq_loss_only": False,
        "full_packet_eq_loss_only_rationale":
            "batch-28 is a partial batch: the resolved packet holds 4 WIN rows "
            "(aa001/aa002/aa006/aa007, honest labels) and 2 EXHAUSTED rows "
            "(aa004/aa005, honest UNKNOWN) which are NOT adopted (unconsumed), so the "
            "adopted packet (1 LOSS row) != the resolved probed set",
        "win_scenario_exists": True,
        "win_scenario_note":
            "the in-batch WIN rows aa001 (s5 28037) and aa002 (s5 87306) "
            "(third-implementation cross-verified in Part CC) and aa006 (s5 129823) "
            "and aa007 (s5 135236) (Part CG cross-verification lane declared, pending "
            "output) are honest labels only, NOT adopted by this Part; they stay "
            "unconsumed (scrutiny owner C++ second-implementation gate pin 9193f5b6...; "
            "batch-14residual q042 / batch-26 l028 precedents); loss-only adoption "
            "NEVER frees class 5343 while its WIN children stay unconsumed",
        "unadopted_win_rows": win_rows,
        "exhausted_rows": exhausted_rows,
        "fragment_rows_note":
            "batch-28 has NO fragment keys in this drive: the 4 truncated sidecars "
            "(aa004.p2 / aa005.p1 / aa006.p2 / aa007.p2 at the wave-1 260s window) are "
            "bookkeeping only and were re-run fresh-cold by the published completeness "
            "guard; the fileless unprobed keys (aa008..aa054) are untouched by this Part",
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_absent_hits": 0,
        "base_cache_rows": BASE_CACHE_ROWS_EXPECTED,
        "quarantine_hits": 0,
        "interpretation_guard":
            "canonical single-row adoption increment: only the 1 LOSS row (aa003) is "
            "consumed into the canonical cache via the fail-closed union merger; the "
            "aa001/aa002/aa006/aa007 WIN verdicts are NOT consumed (unconsumed closure "
            "WIN candidates); 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(
        json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INCREMENT rows=1 loss_nodes={ref['nodes']} -> {incr_path}")


if __name__ == "__main__":
    main()
