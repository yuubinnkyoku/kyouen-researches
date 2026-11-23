#!/usr/bin/env python3
"""Build the batch-24 + batch-27 joint 6-LOSS canonical-adoption increment, fail-closed.

Prepared (read-only dry-run, BEFORE the Part BZ declaration push) for the
Part BZ adoption: the published batch-24 packet (class 16957, Part BL/BN
era kit MANIFEST 8a8e30a8, 83 files all sha256-verified here; raws 8 =
y001/y002/y004/y006 p1/p2 complete; status.log dcba6b0e; row-audit-winhalt
9d073038; batch-keys.json 486858d6, 53 keys) and the published batch-27
packet (class 13342, Part BR drive-1 + takeover; kit MANIFEST eb4da2f7, 92
files all sha256-verified here; raws 12 = o001/o002/o003/o005/o007 p1/p2
complete + the o009 fragment pair p1-complete/p2-truncated; status.log
50a4f407; row-audit-winhalt 530fe947 (winhalt schema); batch-keys.json
67814ed6, 54 keys).  NEITHER packet is a complete enumeration book:
batch-24 probed 4/53 keys under the pre-registered WIN-HALT stop rule
(first WIN at y001; worker continued y006 then halted: the published
2-pair WIN-HALT record), batch-27 probed 5/54 keys (second key o002 WIN).
The fragment o009 (p1 a complete single pass = bookkeeping only, p2
truncated) carries NO evidence and is UNPROBED.  The remaining keys are
fileless UNPROBED (49/49) and are not touched by this Part.

Emits the CANONICAL-ADOPTION increment cache over the published raw replay
rows of the resolved LOSS sets only:

  * batch-24 (class 16957): the 2 resolved LOSS rows y002, y004
  * batch-27 (class 13342): the 4 resolved LOSS rows o001, o003, o005, o007

The in-batch WIN rows y001, y006 (batch-24; third-implementation
cross-verified in Part BW) and o002 (batch-27; third-implementation
cross-verified in Part BY) are HONEST LABELS ONLY and are NOT adopted:
they stay unconsumed (scrutiny owner C++ second-implementation gate pin
9193f5b6...), like the batch-14residual q042 / batch-26 l028 precedents
(loss-only adoption with in-batch WINs left unconsumed).  full != loss
here (machine-stated): the adopted packet is the 6-LOSS packet of a
partially-probed pair of batches.

The adoption base is the canonical exact-S5 verdict cache BASE = 6,287 rows
sha256 e32a2e44... (Part BU adoption output), byte-pinned here; this maker
ABORTS against anything else.

Fail-closed gates (per batch, plus joint): every adopted increment row must
come from BOTH published raw passes with identical (stones, legal, is_or,
budget, result, nodes) and a completed "# replay_done" line; legal and
(lo,hi) must match the published batch-keys.json for every key; the N
WIN rows are likewise two-pass re-verified (result 1) and their keys are
asserted ABSENT from the BASE cache and the quarantine registry and NOT
emitted into the increment; every status.log PASS row must agree with the
raws on (budget, result, nodes); the status.log probed set must be exactly
the published probed set each-once (4 dated PASS rows for batch-24, 5 for
batch-27), the WIN set must be exactly the recorded unadopted WINs (y001,
y006 / o002), the exhaustion set EMPTY (absence gate), the stop rows must
be exactly the published WIN-HALT pairs (batch-24: the y001 and y006
2-line pairs; batch-27: the o002 2-line pair) and no other stop row may
exist; no EXECUTION-COMPLETE row anywhere; the published row-audit-winhalt
summary must agree per batch (schema, class, batch, keys_total, probed,
pass_rows, loss_rows, win_rows, exhausted_rows, fragment/fileless
bookkeeping, mismatches 0, input_sha256); the fragment o009 must have its
p1 complete single pass flagged bookkeeping-only (evidence false, probed
false, absent from status PASS rows) and its p2 truncated (no replay row,
no "# replay_done"), and the o009 key must NOT be emitted; all kit files
must verify against the published MANIFESTs (kit integrity gate, 83 + 92
files); adopted-row pass node totals must agree on both passes per batch
(batch-24: 850,035; batch-27: 13,967,778); all adopted keys distinct,
ABSENT from the canonical BASE cache (6,287 rows; ANY overlap ABORTs -
batch-24/27 rows post-date the Part BU merge), and absent from the
quarantine registry.  Verdicts are byte-taken from the raws.  The 6 LOSS
rows ARE consumed into the canonical cache by the Part BZ fail-closed
merger; no WIN verdict is consumed anywhere.  11x11 stays UNKNOWN; nodes
are bookkeeping, never verdicts.
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
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class1849-loss52-adoption-reaudit-20261123/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-20261123.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BATCH24_DIR = ROOT / "research/experiments/n11-centralreply-closure-class16957-batch24-20261123"
BATCH27_DIR = ROOT / "research/experiments/n11-centralreply-closure-class13342-batch27-20261123"

B24_KEYS_SHA_EXPECTED = "486858d6e2de0662ef38a6ff1fd61c1c0dcf6e9b09012c2c32fdd99153d096cc"
B24_ROW_AUDIT_SHA_EXPECTED = "9d073038f99af68f5832e6b49de2f760356dbfddcbd468623b762cce1083c0d5"
B24_STATUS_SHA_EXPECTED = "dcba6b0e25b9643651eafaac6f4da85624e1335a6936762b10a2a00dcb04d7d5"
B24_MANIFEST_SHA_EXPECTED = "8a8e30a8b8692f1a728410d806e22a9511ef9a3b6da5248f4d7b505ae104d2c2"
B24_KIT_FILES_EXPECTED = 83
B27_KEYS_SHA_EXPECTED = "67814ed6287d68d6e97212c931dce2b7ee585219e20b4d43edb621632220a014"
B27_ROW_AUDIT_SHA_EXPECTED = "530fe94712c79bc73f0df4933e2778bc90eb372675fcb7f5d9ca2d4236ac03ed"
B27_STATUS_SHA_EXPECTED = "50a4f407b369e06f9569238d1b0c35deb02dfad7d839cf57b2fc97a389512ca9"
B27_MANIFEST_SHA_EXPECTED = "eb4da2f7917c0b5b32fc92065ef3928e2a324fdf30726e0c030bc69e002fc1d1"
B27_KIT_FILES_EXPECTED = 92
BASE_CACHE_SHA_EXPECTED = "e32a2e442e77799ea36194f675baeb2424f3410a1d3e681b4c4fbb389f66fe93"
BASE_CACHE_ROWS_EXPECTED = 6287

B24 = {
    "id": 24, "dir": BATCH24_DIR, "class": 16957, "keysid": "y", "keys_total": 53,
    "keys_sha": B24_KEYS_SHA_EXPECTED, "row_audit_sha": B24_ROW_AUDIT_SHA_EXPECTED,
    "status_sha": B24_STATUS_SHA_EXPECTED, "manifest_sha": B24_MANIFEST_SHA_EXPECTED,
    "kit_files": B24_KIT_FILES_EXPECTED,
    "row_audit_schema": "n11-centralreply-closure-class16957-batch24-rowaudit-winhalt-v1",
    "input_schema": "n11-centralreply-closure-class16957-batch24-input-v1",
    "adopted_loss_ids": ["y002", "y004"],
    "unadopted_win_ids": ["y001", "y006"],
    "probed": ["y001", "y002", "y004", "y006"],
    "fragments": [],
    "pass_pairs_expected": 8,       # complete p1/p2 pairs present in raw/ (4 keys)
    "partial_frags_expected": [],
    "status_lines_expected": 6,
    "final_row_expected": "2026-11-23T06:52:09Z y006 WIN-HALT",
    "status_win_pairs": [
        ("2026-11-23T06:52:02Z y001 PASS 15000000,1,5291064", "2026-11-23T06:52:02Z y001 WIN-HALT"),
        ("2026-11-23T06:52:09Z y006 PASS 15000000,1,5321639", "2026-11-23T06:52:09Z y006 WIN-HALT"),
    ],
    "total_nodes_pass_expected": 217944 + 632091,
    "stop_rule": "pre-registered WIN-HALT (Part BN drive published stop record: PASS row directly "
                 "followed by the dated WIN-HALT row for each of y001 and y006; verdict not consumed)",
}
B27 = {
    "id": 27, "dir": BATCH27_DIR, "class": 13342, "keysid": "o", "keys_total": 54,
    "keys_sha": B27_KEYS_SHA_EXPECTED, "row_audit_sha": B27_ROW_AUDIT_SHA_EXPECTED,
    "status_sha": B27_STATUS_SHA_EXPECTED, "manifest_sha": B27_MANIFEST_SHA_EXPECTED,
    "kit_files": B27_KIT_FILES_EXPECTED,
    "row_audit_schema": "n11-centralreply-closure-class13342-batch27-rowaudit-winhalt-v1",
    "input_schema": "n11-centralreply-closure-class13342-batch27-input-v1",
    "adopted_loss_ids": ["o001", "o003", "o005", "o007"],
    "unadopted_win_ids": ["o002"],
    "probed": ["o001", "o002", "o003", "o005", "o007"],
    "fragments": ["o009"],
    "pass_pairs_expected": 10,      # complete p1/p2 pairs (5 keys)
    "partial_frags_expected": [("o009", "p1")],   # p1 complete single pass (bookkeeping), p2 truncated
    "status_lines_expected": 6,
    "final_row_expected": "2026-11-23T12:36:05Z o007 PASS 15000000,2,6644942",
    "status_win_pairs": [
        ("2026-11-23T12:34:28Z o002 PASS 15000000,1,4589084", "2026-11-23T12:34:28Z o002 WIN-HALT"),
    ],
    "total_nodes_pass_expected": 2829495 + 2400082 + 2093259 + 6644942,
    "stop_rule": "pre-registered WIN-HALT (Part BR drive-1 takeover stop record: the o002 2-line "
                 "pair, worker1 then continued its bounded window to o001/o003/o005/o007; verdict "
                 "not consumed)",
}
BATCHES = [B24, B27]
BUDGET = 15_000_000
MERGER = EXP / "scripts/s5_union_merge.py"
MERGER_SHA_EXPECTED = "907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a"


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

    # --- status.log: the whole published picture -----------------------------
    status = parse_status(d / "output/status.log")
    probed = batch["probed"]
    if set(status) != set(probed):
        sys.exit(f"ABORT batch-{batch['id']} status probed set != published probed set: "
                 f"{sorted(set(status) ^ set(probed))}")
    status_resolved = {k for k, v in status.items() if k in probed and v[1] in (1, 2)}
    if status_resolved != set(probed):
        sys.exit(f"ABORT batch-{batch['id']} status resolved set != probed set (exhaustion gate)")
    status_wins = {k for k, v in status.items() if k in probed and v[1] == 1}
    if status_wins != set(batch["unadopted_win_ids"]):
        sys.exit(f"ABORT batch-{batch['id']} WIN set {sorted(status_wins)} != unadopted {sorted(batch['unadopted_win_ids'])}")
    lines = (d / "output/status.log").read_text().strip().splitlines()
    if len(lines) != batch["status_lines_expected"]:
        sys.exit(f"ABORT batch-{batch['id']} status.log line count {len(lines)} != {batch['status_lines_expected']}")
    if lines[-1] != batch["final_row_expected"]:
        sys.exit(f"ABORT batch-{batch['id']} status.log final line drift: {lines[-1]}")
    if "EXECUTION-COMPLETE" in "\n".join(lines):
        sys.exit(f"ABORT batch-{batch['id']} unexpected EXECUTION-COMPLETE record")
    halt_rows = [ln for ln in lines if re.match(r"^\S+ \S+ (WIN-HALT|HARD-STOP)( |$)", ln)]
    expected_halts = [p[1] for p in batch["status_win_pairs"]]
    if halt_rows != expected_halts:
        sys.exit(f"ABORT batch-{batch['id']} stop rows must be exactly the published WIN-HALT rows: {halt_rows}")
    for pass_row, halt_row in batch["status_win_pairs"]:
        if pass_row not in lines or lines.count(pass_row) != 1:
            sys.exit(f"ABORT batch-{batch['id']} status.log lacks the published WIN pass row: {pass_row}")
        idx = lines.index(pass_row)
        if idx + 1 >= len(lines) or lines[idx + 1] != halt_row:
            sys.exit(f"ABORT batch-{batch['id']} WIN PASS row not directly followed by its dated WIN-HALT row: {pass_row}")

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
    if ra["exhausted_rows"] != [] or ra["mismatches"] != 0:
        sys.exit(f"ABORT batch-{batch['id']} row-audit exhaustion/mismatch drift")
    if ra["input_sha256"] != batch["keys_sha"]:
        sys.exit(f"ABORT batch-{batch['id']} row-audit input_sha256 drift")
    fileless_expected = sorted(set(f"{batch['keysid']}{i:03d}" for i in range(1, batch["keys_total"] + 1))
                               - set(probed) - set(batch["fragments"]))
    if ra["fileless_unprobed"] != fileless_expected or ra["unprobed_count"] != len(fileless_expected) + len(batch["fragments"]):
        sys.exit(f"ABORT batch-{batch['id']} row-audit fileless/unprobed bookkeeping drift")
    return status, by_id


def main() -> None:
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys.exit("ABORT base cache sha drift")
    if sha(MERGER) != MERGER_SHA_EXPECTED:
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

    rows = []           # (kid, batch_id, class_index, s5_index, lo, hi, result, nodes)
    win_rows = []        # re-verified honest labels (never adopted)
    per_batch = {}
    emitted_keys = set()
    total_nodes = {"p1": 0, "p2": 0}

    for batch in BATCHES:
        status, by_id = verify_batch(batch)
        b_rows = []
        b_total = {"p1": 0, "p2": 0}
        for kid in batch["adopted_loss_ids"]:
            ref = two_pass(batch, kid)
            if ref["budget"] != BUDGET or ref["stones"] != 5 or ref["is_or"] != 0:
                sys.exit(f"ABORT {kid}: wrong budget/depth {ref}")
            if ref["result"] != 2:
                sys.exit(f"ABORT {kid}: adopted rows must be result 2, got {ref['result']}")
            b_total["p1"] += ref["nodes"]
            bk = by_id.get(kid)
            if bk is None:
                sys.exit(f"ABORT batch-{batch['id']} batch-keys.json missing {kid}")
            if ref["legal"] != int(bk["legal"]):
                sys.exit(f"ABORT {kid}: legal mismatch raw={ref['legal']} keys={bk['legal']}")
            if (ref["lo"], ref["hi"]) != (int(bk["lo"]), int(bk["hi"])):
                sys.exit(f"ABORT {kid}: key mismatch raw=({ref['lo']},{ref['hi']}) keys=({bk['lo']},{bk['hi']})")
            if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
                sys.exit(f"ABORT {kid}: status.log disagreement {status.get(kid)}")
            key = (ref["lo"], ref["hi"])
            if key in quarantined:
                sys.exit(f"ABORT {kid}: quarantined key {key}")
            if key in base_keys:
                sys.exit(f"ABORT {kid}: key already in canonical BASE cache {key} "
                         f"(base={base_keys[key]}, raw={(ref['result'], ref['nodes'])})")
            if key in emitted_keys:
                sys.exit(f"ABORT duplicate key across the joint increment {key}")
            emitted_keys.add(key)
            b_rows.append((kid, batch["id"], batch["class"], int(bk["s5_index"]),
                           ref["lo"], ref["hi"], ref["result"], ref["nodes"]))
        if b_total["p1"] != batch["total_nodes_pass_expected"]:
            sys.exit(f"ABORT batch-{batch['id']} adopted-row pass node sum drift: {b_total['p1']}")
        # second-pass node recomputation (independent of the parse)
        b_total["p2"] = sum(
            int(line.split(",")[7])
            for kid in batch["adopted_loss_ids"]
            for line in (batch["dir"] / f"output/raw/{kid}.p2.out").read_text().splitlines()
            if line.startswith("replay,"))
        if b_total["p2"] != b_total["p1"]:
            sys.exit(f"ABORT batch-{batch['id']} adopted-row pass node totals disagree: {b_total}")
        rows += b_rows
        total_nodes["p1"] += b_total["p1"]
        total_nodes["p2"] += b_total["p2"]

        # --- unadopted WIN rows: two-pass re-verified honest labels ----------
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
            win_rows.append({
                "key_id": kid, "batch": batch["id"], "class_index": batch["class"],
                "s5_index": int(winbk["s5_index"]), "lo": winref["lo"], "hi": winref["hi"],
                "legal": winref["legal"], "result": winref["result"], "nodes": winref["nodes"],
                "two_pass_node_exact": True,
                "note": f"honest label only, never adopted in this Part (Part "
                        f"{'BW' if batch['id'] == 24 else 'BY'} third-implementation cross-verified; "
                        "stays unconsumed)",
            })

        # --- fragment bookkeeping (must carry NO evidence) -------------------
        batch["fragment_state"] = {}
        for kid in batch["fragments"]:
            ra = json.loads((batch["dir"] / "output/row-audit-winhalt.json").read_text())
            frag = ra["fragment_keys"].get(kid)
            if frag is None or frag["evidence"] is not False or frag["probed"] is not False:
                sys.exit(f"ABORT batch-{batch['id']} row-audit fragment {kid} bookkeeping drift: {frag}")
            if frag["pass_pair_complete"] is not False:
                sys.exit(f"ABORT batch-{batch['id']} fragment {kid} must not be a complete pass pair")
            p1 = batch["dir"] / f"output/raw/{kid}.p1.out"
            p2 = batch["dir"] / f"output/raw/{kid}.p2.out"
            if not p1.is_file() or not p2.is_file():
                sys.exit(f"ABORT batch-{batch['id']} fragment {kid} raw pair missing")
            p1_txt, p2_txt = p1.read_text(), p2.read_text()
            if "# replay_done" not in p1_txt:
                sys.exit(f"ABORT batch-{batch['id']} fragment {kid}.p1 must be the complete single pass")
            if "# replay_done" in p2_txt or re.search(r"^replay,", p2_txt, re.M):
                sys.exit(f"ABORT batch-{batch['id']} fragment {kid}.p2 must be the truncated pass")
            f1 = parse_replay(p1)
            fk = by_id[kid]
            if (f1["lo"], f1["hi"]) != (int(fk["lo"]), int(fk["hi"])):
                sys.exit(f"ABORT batch-{batch['id']} fragment {kid} key mismatch vs batch-keys")
            if f1["result"] != frag["p1_result_bookkeeping"]:
                sys.exit(f"ABORT batch-{batch['id']} fragment {kid} p1 bookkeeping result drift")
            fkey = (f1["lo"], f1["hi"])
            if fkey in emitted_keys:
                sys.exit(f"ABORT fragment {kid} key leaked into the adopted rows")
            if fkey in base_keys:
                sys.exit(f"ABORT fragment {kid} key in BASE cache")
            if kid in status:
                sys.exit(f"ABORT fragment {kid} must not have a status.log PASS row (UNPROBED gate)")
            batch["fragment_state"][kid] = {
                "p1_complete_single_pass": True, "p1_result_bookkeeping": f1["result"],
                "p1_nodes_bookkeeping": f1["nodes"], "p2_complete_single_pass": False,
                "pass_pair_complete": False, "evidence": False, "probed": False,
            }

        per_batch[batch["id"]] = {
            "b_rows": b_rows, "b_total": dict(b_total),
            "status": status, "by_id": by_id,
        }

    if total_nodes["p1"] != total_nodes["p2"]:
        sys.exit(f"ABORT joint pass totals disagree: {total_nodes}")
    if len(rows) != 6:
        sys.exit(f"ABORT adopted row count {len(rows)} != 6")
    wins = [r for r in rows if r[6] == 1]
    losses = [r for r in rows if r[6] == 2]
    if wins or len(losses) != 6:
        sys.exit(f"ABORT adopted row verdict counts {len(wins)}/{len(losses)} != 0/6")

    hdr = [
        "# n11 central-reply closure batch-24 (class 16957) + batch-27 (class 13342) joint",
        "#   6-LOSS canonical-adoption increment (Part BZ, 2026-11-23)",
        "# published Part BZ declaration (note amendment 2026-11-23; single-owner: loss-only",
        "#   joint adoption; the in-batch WIN rows y001/y006 (batch-24, Part BW cross-verified)",
        "#   and o002 (batch-27, Part BY cross-verified) are honest labels only and are NOT",
        "#   adopted; fragment o009 is bookkeeping only, UNPROBED).",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# batch-24 probed 4/53 keys under the pre-registered WIN-HALT rule (y001, y006 WIN",
        "#   pairs published; 49 fileless UNPROBED); batch-27 probed 5/54 keys (o002 WIN pair",
        "#   published; fragment o009 UNPROBED; 48 fileless UNPROBED).  NEITHER batch is a",
        "#   complete enumeration book: only the resolved LOSS rows below are adopted.",
        "#   the remaining keys stay UNKNOWN in canonical and untouched by this Part.",
        "# gates (per batch + joint): kit MANIFEST sha verification (83 + 92 files), 2-way",
        "#   (p1/p2) node-exact + '# replay_done' completeness, status.log each-once",
        "#   agreement (b,r,n) per key, WIN sets == unadopted, exhaustion absence gate,",
        "#   WIN-HALT 2-line pair pins, row-audit-winhalt schema agreement, batch-keys",
        "#   legal/(lo,hi) agreement, adopted-row pass node sums (batch-24 850,035;",
        "#   batch-27 13,967,778), adopted keys distinct, ZERO BASE-cache overlap",
        "#   (structural gate: batch-24/27 rows post-date the Part BU merge; any overlap",
        "#   ABORTs), quarantine 0, WIN rows two-pass re-verified + presence bookkeeping",
        "#   (asserted NOT adopted), fragment o009 completeness-guard asymmetry asserted",
        "#   + NOT emitted + absent from status PASS rows.",
        "# ADOPTED set = {y002, y004} + {o001, o003, o005, o007}.  full != loss here",
        "#   (machine-stated): the resolved packets additionally hold the y001/y006/o002",
        "#   WIN rows, which stay UNCONSUMED (scrutiny owner C++ second-implementation",
        "#   gate pin 9193f5b6...; batch-14residual q042 / batch-26 l028 precedents); no",
        "#   WIN verdict is consumed anywhere by this Part; the unconsumed closure WIN",
        "#   candidates (y001/y006/o002 among them) are untouched.",
        "# The 6 LOSS rows ARE consumed into the canonical cache by the Part BZ merger;",
        "#   11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.",
        "# 6 rows: the adopted LOSS verdicts of class 16957's and class 13342's",
        "#   probed unknown S5 children (batches 24 and 27).",
    ]

    lines = list(hdr)
    lines += [f"s5verdict,{r[4]},{r[5]},5,{r[6]},{r[7]}" for r in sorted(rows, key=lambda r: (r[4], r[5]))]
    p = OUT / "increment-b24b27-loss6-20261123.cache"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{p.name}: {len(rows)} rows, sha256 {sha(p)}")

    manifest = {
        "schema": "b24b27-loss6-increments-manifest-v1",
        "batches": [
            {
                "batch": b["id"], "class_index": b["class"], "keys_total": b["keys_total"],
                "adopted_loss_ids": b["adopted_loss_ids"],
                "unadopted_win_ids": b["unadopted_win_ids"],
                "probed_ids": b["probed"],
                "fragment_ids": b["fragments"],
                "fileless_unprobed_count": per_batch[b["id"]]["b_rows"] and
                    (b["keys_total"] - len(b["probed"]) - len(b["fragments"])),
                "input_sha256": b["keys_sha"], "row_audit_sha256": b["row_audit_sha"],
                "status_log_sha256": b["status_sha"],
                "status_log_stop_records": [{"pass_row": pr, "halt_row": hr}
                                             for pr, hr in b["status_win_pairs"]],
                "status_log_final_row": b["final_row_expected"],
                "stop_rule": b["stop_rule"],
                "total_nodes_pass_one": per_batch[b["id"]]["b_total"]["p1"],
                "total_nodes_pass_two": per_batch[b["id"]]["b_total"]["p2"],
                "kit_integrity": {"manifest_sha256": b["manifest_sha"],
                                  "files_verified": b["kit_verified"]},
                "fragment_state": b["fragment_state"],
            } for b in BATCHES
        ],
        "resolved_ids": [kid for b in BATCHES for kid in b["probed"]],
        "loss_ids": [kid for b in BATCHES for kid in b["adopted_loss_ids"]],
        "win_ids": [kid for b in BATCHES for kid in b["unadopted_win_ids"]],
        "unadopted_win_ids": [kid for b in BATCHES for kid in b["unadopted_win_ids"]],
        "exhausted_excluded_ids": [],
        "row_counts": {
            "probed_rows": 9, "adopted_loss_rows": 6, "wins": 3,
            "exhausted_excluded": 0, "fragments_unprobed": 1,
            "fileless_unprobed": 97,
        },
        "sha256": {"loss": sha(p)},
        "full_packet_eq_loss_only": False,
        "full_packet_eq_loss_only_rationale": (
            "batch-24 and batch-27 are partial batches: the resolved packets hold 3 WIN rows "
            "(y001/y006/o002, honest labels) which are NOT adopted (unconsumed), so the "
            "adopted packet (6 LOSS rows) != the resolved probed set"),
        "win_scenario_exists": True,
        "win_scenario_note": (
            "the in-batch WIN rows y001 (s5 91296) and y006 (batch-24, third-implementation "
            "cross-verified in Part BW) and o002 (s5 209134, batch-27, third-implementation "
            "cross-verified in Part BY) are honest labels only, NOT adopted by this Part; they "
            "stay unconsumed (scrutiny owner C++ second-implementation gate pin 9193f5b6...; "
            "batch-14residual q042 / batch-26 l028 precedents); loss-only adoption NEVER frees "
            "class 16957 / class 13342 while their WIN children stay unconsumed"),
        "unadopted_win_rows": win_rows,
        "fragment_rows_note": (
            "fragment o009 (batch-27) carries NO evidence: its p1 complete single pass is "
            "bookkeeping only, its p2 is truncated; o009 is UNPROBED and NOT emitted; the "
            "fileless unprobed keys of both batches are untouched by this Part"),
        "merger_sha256": MERGER_SHA_EXPECTED,
        "base_cache_absent_hits": 0,
        "base_cache_rows": len(base_keys),
        "quarantine_hits": 0,
        "interpretation_guard": (
            "canonical joint adoption increment: only the 6 LOSS rows are consumed into the "
            "canonical cache via the fail-closed union merger; the y001/y006/o002 WIN "
            "verdicts are NOT consumed (unconsumed closure WIN candidates); 11x11 stays "
            "UNKNOWN; nodes are bookkeeping, never verdicts"),
    }
    (OUT / "increments-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print("OK 9 probed rows (3 WIN unadopted, 1 fragment UNPROBED) -> 6 adopted LOSS, "
          "zero exhaustion, zero BASE overlap, quarantine 0, kits 83+92 verified, "
          "full != loss packet, row-audit winhalt schema agreement both batches, "
          "all gates PASS")


if __name__ == "__main__":
    main()
