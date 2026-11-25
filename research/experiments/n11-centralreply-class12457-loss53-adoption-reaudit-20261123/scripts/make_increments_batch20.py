#!/usr/bin/env python3
"""Build the batch-20 (class 12457) 53-LOSS canonical-adoption increment, fail-closed.

Executes the published Part BI declaration (note amendment, commit 879e898c,
observed HEAD-before-push 1d46f883; single-owner: batch-20 53-LOSS adoption).
All inputs are published main bytes, re-verified against this host before use:
batch-20 dir (publication commits 358cac13 / 564cc66a / 928546df; kit MANIFEST
d0ef293b 191 files all sha256-verified here; raws 106 (x001-x053 p1/p2) + 14
host-event truncated fragments that never produced a verdict row; status.log
627d306b; row-audit.json (summary schema) 1dcb7fb8; batch-keys.json
efb40b1b); current canonical exact-S5 verdict cache BASE = 6,182 rows
sha256 0b594f7e... (Part BC adoption output), byte-pinned here.

Emits the CANONICAL-ADOPTION increment cache over the published batch-20 raw
replay rows:

  * the 53 resolved LOSS rows {x001..x053}

batch-20 was executed by the Part BG host (53/53 probed = 53 LOSS, 0 WIN,
0 exhaustion, 0 mismatch; pinned jsreplay.js 84585617..., 2-pass fresh-cold
node-exact, total 175,842,846 nodes each pass; fourteen host-event truncated
fragments never produced a verdict row and were re-run fresh cold).  There is
NO WIN row in batch-20 and NO exhaustion row, so the adopted packet IS the full
resolved packet: full == loss for batch-20 (machine-stated).

Fail-closed gates: every increment row must come from BOTH published raw
passes with identical (stones, legal, is_or, budget, result, nodes) and a
completed "# replay_done" line; legal and (lo,hi) must match the published
batch-keys.json (sha256 efb40b1b...) for every key; every status.log PASS row
must agree with the raws on (budget, result, nodes); the status.log probed set
must be exactly {x001..x053} each-once (53 dated PASS rows), with the published
final row x053 PASS 15000000,2,6402333; batch-20's status.log carries NO stop
record (honest record - the probed-set, each-once, WIN-absence, exhaustion-
absence and final-row gates replace it); the WIN set must be EMPTY (absence
gate) and the exhaustion set EMPTY (absence gate); the published row-audit
summary must agree (schema n11-centralreply-closure-class12457-batch20-
rowaudit-v1, class 12457, batch 20, keys_total/probed/pass_rows 53, win_rows
[], exhausted_rows [], mismatches 0, input_sha256 efb40b1b); all 191 kit
files must verify against the published MANIFEST d0ef293b (kit integrity
gate); the 14 truncated fragments must exist and carry NO replay row; pass
totals must agree on both passes (175,842,846); all keys distinct, ABSENT
from the canonical BASE cache (6,182 rows; ANY overlap ABORTS - batch-20
post-dates the Part BC merge), and absent from the quarantine registry.
Verdicts are byte-taken from the raws.  The 53 LOSS rows ARE consumed into
the canonical cache by the Part BI fail-closed merger; no WIN verdict is
consumed anywhere (none exists).  11x11 stays UNKNOWN; nodes are bookkeeping,
never verdicts.
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
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class23101-residualloss10-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-20261122.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class12457-batch20-20261123"
BATCH_KEYS_SHA_EXPECTED = "efb40b1bb7a43595bb8d014a31af2b878c404be86b8f9d5abc717eb176d1ed51"
ROW_AUDIT_SHA_EXPECTED = "1dcb7fb8847221cc069680ef24d3e9a9960734cdbd04bead81769aac0900136f"
STATUS_LOG_SHA_EXPECTED = "627d306b1c28421a35833e6e08bbd7474b9f94627aaf93a22b206fd08c6ddede"
KIT_MANIFEST_SHA_EXPECTED = "d0ef293bdf81b68acd9feeb31338c1dfc5b4ce3237016b74630f398cff824507"
KIT_FILES_EXPECTED = 191
BASE_CACHE_SHA_EXPECTED = "0b594f7e14d7eb67263d38a3daa2816e1fd0b73b23403f9b58ca2917225f877a"
BASE_CACHE_ROWS_EXPECTED = 6182

LOSS_IDS = [f"x{i:03d}" for i in range(1, 54)]  # resolved LOSS rows (53)
UNADOPTED_WIN_IDS = []                           # batch-20 has zero WIN rows (asserted)
PROBED = LOSS_IDS + UNADOPTED_WIN_IDS            # the published probed set (53)
EXHAUSTED_IDS: list = []                         # batch-20 has zero exhaustion rows (asserted)
BUDGET = 15_000_000
TOTAL_NODES_PER_PASS_EXPECTED = 175_842_846
FINAL_ROW_EXPECTED = "2026-11-23T02:44:04Z x053 PASS 15000000,2,6402333"
TRUNCATED_FRAGMENTS_EXPECTED = [
    "x008.p1.truncated.021533.out", "x009.p1.truncated.021533.out",
    "x015.p1.truncated.021954.out", "x016.p2.truncated.021954.out",
    "x019.p2.truncated.022417.out", "x022.p2.truncated.022500.out",
    "x028.p2.truncated.022838.out", "x031.p1.truncated.022917.out",
    "x035.p2.truncated.023301.out", "x038.p2.truncated.023426.out",
    "x043.p2.truncated.023723.out", "x044.p1.truncated.023723.out",
    "x048.p2.truncated.024146.out", "x053.p1.truncated.024248.out",
]


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
        m = re.match(r"^\S+ (\S+) PASS (\d+),(\d+),(\d+)$", line)
        if m:
            kid, b, r, n = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            kid = kid.split(".")[0]
            if kid in got and got[kid] != (b, r, n):
                sys.exit(f"ABORT status disagreement for {kid}")
            if kid in got:
                sys.exit(f"ABORT status key {kid} appears more than once (each-once gate)")
            got[kid] = (b, r, n)
    return got


def two_pass(kid: str):
    variants = {}
    for tag in ("p1", "p2"):
        p = BATCH_DIR / f"output/raw/{kid}.{tag}.out"
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


def main() -> None:
    if sha(BASE_CACHE) != BASE_CACHE_SHA_EXPECTED:
        sys.exit("ABORT base cache sha drift")
    if sha(BATCH_DIR / "input/batch-keys.json") != BATCH_KEYS_SHA_EXPECTED:
        sys.exit("ABORT batch-20 batch-keys.json sha drift")
    if sha(BATCH_DIR / "output/row-audit.json") != ROW_AUDIT_SHA_EXPECTED:
        sys.exit("ABORT batch-20 row-audit.json sha drift")
    if sha(BATCH_DIR / "output/status.log") != STATUS_LOG_SHA_EXPECTED:
        sys.exit("ABORT batch-20 status.log sha drift")
    if sha(BATCH_DIR / "MANIFEST-sha256.txt") != KIT_MANIFEST_SHA_EXPECTED:
        sys.exit("ABORT batch-20 kit MANIFEST sha drift")
    OUT.mkdir(parents=True, exist_ok=True)

    # --- kit integrity gate: all 191 published files must verify ------------
    kit_verified = 0
    for line in (BATCH_DIR / "MANIFEST-sha256.txt").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        want, rel = line.split(None, 1)
        p = BATCH_DIR / rel
        if not p.is_file():
            sys.exit(f"ABORT kit file missing: {rel}")
        if sha(p) != want:
            sys.exit(f"ABORT kit file sha drift: {rel}")
        kit_verified += 1
    if kit_verified != KIT_FILES_EXPECTED:
        sys.exit(f"ABORT kit files verified {kit_verified} != {KIT_FILES_EXPECTED}")

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

    keys = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())["keys"]
    bk_all = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())
    if bk_all["class_index"] != 12457 or bk_all["budget"] != BUDGET:
        sys.exit("ABORT batch-keys class/budget drift")
    if bk_all["published_base_canonical_rows"] != BASE_CACHE_ROWS_EXPECTED:
        sys.exit("ABORT batch-keys published_base_canonical_rows drift")
    by_id = {k["key_id"]: k for k in keys}
    if len(by_id) != 53:
        sys.exit(f"ABORT batch-keys key count {len(by_id)} != 53")

    # --- status.log: whole picture -----------------------------------------
    status = parse_status(BATCH_DIR / "output/status.log")
    status_probed = {k for k in status if k in PROBED}
    if status_probed != set(PROBED):
        sys.exit(f"ABORT status probed set != {{x001..x053}}: {sorted(status_probed)}")
    extra_status = set(status) - set(PROBED)
    if extra_status:
        sys.exit(f"ABORT status.log PASS rows outside the probed set: {sorted(extra_status)}")
    status_resolved = {k for k, v in status.items() if k in PROBED and v[1] in (1, 2)}
    if status_resolved != set(PROBED):
        sys.exit(f"ABORT status resolved set != full probed set: {sorted(status_resolved)}")
    status_wins = {k for k, v in status.items() if k in PROBED and v[1] == 1}
    if status_wins != set(UNADOPTED_WIN_IDS):
        sys.exit(f"ABORT batch-20 WIN set {sorted(status_wins)} != empty (absence gate)")
    status_exhausted = {k for k, v in status.items() if k in PROBED and v[1] == 0}
    if status_exhausted != set(EXHAUSTED_IDS):
        sys.exit(f"ABORT batch-20 must have zero exhaustion rows: {sorted(status_exhausted)}")
    status_text = (BATCH_DIR / "output/status.log").read_text()
    if FINAL_ROW_EXPECTED not in status_text:
        sys.exit("ABORT status.log lacks the published final row 'x053 PASS 15000000,2,6402333'")
    if status_text.strip().splitlines()[-1] != FINAL_ROW_EXPECTED:
        sys.exit("ABORT status.log final line is not the published x053 PASS row")
    if re.search(r"^\S+ \S+ (WIN-HALT|HARD-STOP)( |$)", status_text, re.M):
        sys.exit("ABORT status.log contains a dated WIN-HALT/HARD-STOP stop row")
    if "EXECUTION-COMPLETE" in status_text:
        sys.exit("ABORT unexpected stop record in batch-20 status.log (published batch-20 has none)")

    # --- row-audit.json: summary agreement -----------------------------------
    ra = json.loads((BATCH_DIR / "output/row-audit.json").read_text())
    if ra["schema"] != "n11-centralreply-closure-class12457-batch20-rowaudit-v1":
        sys.exit(f"ABORT row-audit schema drift: {ra['schema']}")
    if ra["class_index"] != 12457 or ra["batch"] != 20:
        sys.exit("ABORT row-audit whole-picture header drift")
    if ra["keys_total"] != 53 or ra["probed"] != 53 or ra["pass_rows"] != 53:
        sys.exit("ABORT row-audit keys_total/probed/pass_rows drift")
    if ra["win_rows"] != [] or ra["exhausted_rows"] != [] or ra["mismatches"] != 0:
        sys.exit(f"ABORT row-audit results not the clean all-LOSS picture: "
                 f"{ra['win_rows']}/{ra['exhausted_rows']}/{ra['mismatches']}")
    if ra["input_sha256"] != BATCH_KEYS_SHA_EXPECTED:
        sys.exit("ABORT row-audit input_sha256 drift")

    # --- host-event truncated fragments -------------------------------------
    present_frags = sorted(p.name for p in (BATCH_DIR / "output/raw").glob("*.truncated.*.out"))
    if present_frags != sorted(TRUNCATED_FRAGMENTS_EXPECTED):
        sys.exit(f"ABORT truncated fragment set drift: {present_frags}")
    for name in present_frags:
        p = BATCH_DIR / "output/raw" / name
        txt = p.read_text()
        if re.search(r"^replay,", txt, re.M):
            sys.exit(f"ABORT hostevent fragment carries a verdict row: {p}")
        if "# replay_done" in txt:
            sys.exit(f"ABORT hostevent fragment carries a completion guard: {p}")

    rows = []           # (kid, s5_index, lo, hi, result, nodes) - adopted LOSS rows
    total_nodes = {"p1": 0, "p2": 0}
    for kid in LOSS_IDS:
        ref = two_pass(kid)
        if ref["budget"] != BUDGET or ref["stones"] != 5 or ref["is_or"] != 0:
            sys.exit(f"ABORT {kid}: wrong budget/depth {ref}")
        if ref["result"] != 2:
            sys.exit(f"ABORT {kid}: adopted rows must be result 2, got {ref['result']}")
        total_nodes["p1"] += ref["nodes"]
        bk = by_id.get(kid)
        if bk is None:
            sys.exit(f"ABORT batch-keys.json missing {kid}")
        if ref["legal"] != int(bk["legal"]):
            sys.exit(f"ABORT {kid}: legal mismatch raw={ref['legal']} keys={bk['legal']}")
        if (ref["lo"], ref["hi"]) != (int(bk["lo"]), int(bk["hi"])):
            sys.exit(f"ABORT {kid}: key mismatch raw=({ref['lo']},{ref['hi']}) keys=({bk['lo']},{bk['hi']})")
        if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
            sys.exit(f"ABORT {kid}: status.log disagreement {status.get(kid)} vs {(ref['budget'], ref['result'], ref['nodes'])}")
        key = (ref["lo"], ref["hi"])
        if key in quarantined:
            sys.exit(f"ABORT {kid}: quarantined key {key}")
        if key in base_keys:
            sys.exit(f"ABORT {kid}: key already in canonical BASE cache {key} "
                     f"(base={base_keys[key]}, raw={(ref['result'], ref['nodes'])})")
        if any(r[3] == key[0] and r[4] == key[1] for r in rows):
            sys.exit(f"ABORT duplicate key within batch {key}")
        rows.append((kid, int(bk["s5_index"]), ref["lo"], ref["hi"], ref["result"], ref["nodes"]))

    # second-pass node totals cross-check (independent of parse)
    for tag in ("p1", "p2"):
        s = 0
        for kid in LOSS_IDS:
            for line in (BATCH_DIR / f"output/raw/{kid}.{tag}.out").read_text().splitlines():
                if line.startswith("replay,"):
                    s += int(line.split(",")[7])
        total_nodes[tag] = s
    if total_nodes["p1"] != total_nodes["p2"] or total_nodes["p1"] != TOTAL_NODES_PER_PASS_EXPECTED:
        sys.exit(f"ABORT pass node totals drift: {total_nodes} != {TOTAL_NODES_PER_PASS_EXPECTED}")

    wins = [r for r in rows if r[4] == 1]
    losses = [r for r in rows if r[4] == 2]
    got_losses = sorted(r[0] for r in losses)
    if got_losses != sorted(LOSS_IDS):
        sys.exit(f"ABORT LOSS set mismatch: {got_losses}")
    if len(rows) != 53 or wins or len(losses) != 53:
        sys.exit(f"ABORT resolved row counts {len(rows)}/{len(wins)}/{len(losses)} != 53/0/53")

    hdr = [
        "# n11 central-reply closure batch-20 (class 12457) 53-LOSS canonical-adoption increment (Part BI, 2026-11-23)",
        "# published Part BI declaration (note amendment 2026-11-23, commit 879e898c, observed",
        "#   HEAD-before-push 1d46f883a1fea022128a1bb28d28713b75dcbcf6; note blob lock 4e09fd83).",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# batch-20 was executed by the Part BG host (53/53 probed = 53 LOSS, 0 WIN, 0",
        "#   exhaustion, 0 mismatch; fourteen host-event truncated fragments never produced",
        "#   a verdict line and were re-run fresh cold; row-audit 1dcb7fb8 summary agrees,",
        "#   status.log 627d306b: 53 dated each-once PASS rows, final row 'x053 PASS",
        "#   15000000,2,6402333', NO stop record (batch-20 status.log has none; the",
        "#   probed-set/each-once/final-row gates replace it - honest record)).",
        "# gates: kit MANIFEST d0ef293b 191/191 file sha verification, 2-way (p1/p2) node-exact",
        "#   + '# replay_done' completeness, status.log each-once agreement (b,r,n) per key,",
        "#   row-audit.json summary agreement (schema/class/batch/probed/pass/win/exhausted/",
        "#   mismatches/input_sha), batch-keys efb40b1b legal/(lo,hi) agreement, pass node",
        "#   totals 175,842,846 x2, resolved keys distinct, ZERO WIN rows (absence gate),",
        "#   ZERO exhaustion rows (absence gate), ZERO BASE-cache overlap (structural gate:",
        "#   batch-20 post-dates the Part BC merge; any overlap ABORTS), quarantine 0.",
        "# ADOPTED set = the full resolved packet {x001..x053} = exactly all 53 LOSS rows.",
        "#   No WIN row exists in batch-20, so full == loss here (machine-stated); no WIN",
        "#   verdict is consumed anywhere by this Part; the 19 unconsumed closure WINs are",
        "#   untouched (scrutiny owner gate 9193f5b6... unchanged).",
        "# The 53 LOSS rows ARE consumed into the canonical cache by the Part BI merger;",
        "#   11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.",
        "# 53 rows: the adopted LOSS verdicts of class 12457's unknown S5 children (20th batch).",
    ]

    lines = list(hdr)
    lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(rows, key=lambda r: (r[2], r[3]))]
    p = OUT / "increment-batch20-loss53-20261123.cache"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{p.name}: {len(rows)} rows, sha256 {sha(p)}")

    manifest = {
        "schema": "batch20-loss53-increments-manifest-v1",
        "batch": 20,
        "class_index": 12457,
        "loss_ids": LOSS_IDS,
        "resolved_ids": LOSS_IDS,
        "win_ids": [],
        "unadopted_win_ids": UNADOPTED_WIN_IDS,
        "exhausted_excluded_ids": EXHAUSTED_IDS,
        "row_counts": {"resolved_rows": len(rows), "wins": len(wins), "losses": len(losses),
                       "exhausted_excluded": 0, "probed_total": 53, "probed_resolved": 53},
        "sha256": {"loss": sha(p)},
        "full_packet_eq_loss_only": True,
        "full_packet_eq_loss_only_rationale": ("batch-20 resolved all 53 probed keys as "
                                                "LOSS; zero WIN rows exist (absence gate) "
                                                "and zero exhaustion rows, so the adopted "
                                                "packet IS the full resolved packet"),
        "win_scenario_exists": False,
        "win_scenario_note": ("batch-20 contains no WIN row; no WIN adoption scenario "
                              "arises from this batch; the 19 unconsumed closure WINs "
                              "are untouched by this Part"),
        "row_audit_agreement_rows": 53,
        "row_audit_sha256": ROW_AUDIT_SHA_EXPECTED,
        "status_log_stop_record": None,
        "status_log_stop_record_note": ("batch-20 status.log carries NO stop record "
                                        "(honest record); the probed-set/each-once/"
                                        "WIN-absence/exhaustion-absence/final-row gates "
                                        "replace it"),
        "status_log_final_row": FINAL_ROW_EXPECTED,
        "status_log_sha256": STATUS_LOG_SHA_EXPECTED,
        "total_nodes_pass_one": total_nodes["p1"],
        "total_nodes_pass_two": total_nodes["p2"],
        "truncated_fragments": TRUNCATED_FRAGMENTS_EXPECTED,
        "truncated_fragments_carries_verdict": False,
        "kit_integrity": {"manifest_sha256": KIT_MANIFEST_SHA_EXPECTED,
                          "files_verified": kit_verified},
        "base_cache_absent_hits": 0,
        "base_cache_rows": len(base_keys),
        "quarantine_hits": 0,
        "interpretation_guard": ("canonical adoption increment: the 53 LOSS rows are "
                                 "consumed into the canonical cache via the fail-closed "
                                 "union merger; no WIN verdict is consumed (none exists "
                                 "in batch-20); 11x11 stays UNKNOWN; nodes are "
                                 "bookkeeping, never verdicts"),
    }
    (OUT / "increments-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print("OK 53 probed rows -> 53 adopted LOSS (x001..x053), zero WIN (absence gate), "
          "zero exhaustion, zero BASE overlap, quarantine 0, kit 191/191 verified, "
          "full==loss packet, row-audit summary agreement, all gates PASS")


if __name__ == "__main__":
    main()
