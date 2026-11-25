#!/usr/bin/env python3
"""Build the batch-17 (class 10661) 52-LOSS canonical-adoption increment, fail-closed.

Executes the published Part AV declaration (note amendment, commit `340abef3`)
as taken over by this host under the published Part AV takeover amendment
(note, commit `d3ef2dc6`, observed HEAD-before-push `432664f7`; scope unchanged
from `340abef3` - ownership transfer only).  All inputs are published main
bytes, re-verified against this host before use: batch-17 dir (publication
commit `ffc09de1` + hygiene `4741a92f`; raws 104 (u001-u052 p1/p2) + merged
status.log + batch-keys.json (sha256 db762175...) + row-audit.json
(sha256 c19e768f...) + hostevent fragments 5 (verdict row absent), kit mirror
sha-verified 177/177; current canonical exact-S5 verdict cache 6,120 rows
sha256 be9cb24e... = Part AS canonical adoption, byte-pinned here).

Emits the CANONICAL-ADOPTION increment cache over the published batch-17 raw
replay rows:

  * the 52 resolved LOSS rows {u001..u052}

batch-17 was executed by the Part AU host (52/52 probed = 52 LOSS, 0 WIN,
0 exhaustion, 0 mismatch; pinned jsreplay.js 84585617..., 2-pass fresh-cold
node-exact, total 196,536,452 nodes per pass; five host-event truncated
fragments never produced a verdict line and were re-run fresh cold).  There
is NO WIN row in batch-17 and NO exhaustion row, so the adopted packet IS
the full resolved packet: full == loss for batch-17 (machine-stated).

Fail-closed gates: every increment row must come from BOTH published raw
passes with identical (stones, legal, is_or, budget, result, nodes) and a
completed "# replay_done" line; legal and (lo,hi) must match the published
batch-keys.json (sha256 db762175...) for every key; every status.log PASS row
must agree with the raws on (budget, result, nodes); the status.log probed
set must be exactly {u001..u052} with the published "EXECUTION-COMPLETE:
52/52 probed = 52 LOSS" stop record; the WIN set must be EMPTY (absence gate)
and the exhaustion set EMPTY (absence gate); the published row-audit.json
must agree row-for-row (52 rows: result 2, budget 15,000,000, node_exact,
nodes == pass2_nodes == raw nodes, legal/(lo,hi)/s5_index/probe_order ==
batch-keys) with machine-verified whole-picture fields (class 10661, batch
17, probed 52, results loss 52 / win 0 / exhausted 0 / mismatch 0,
two_pass_node_exact 52, totals 196,536,452 both passes,
batch_keys_sha256 db762175..., 5 host fragments with no verdict line and
incomplete rows re-searched fresh-cold); all keys distinct, ABSENT from the
canonical BASE cache (6,120 rows, sha256 be9cb24e...; ANY overlap ABORTS -
batch-17 post-dates the Part AS merge), and absent from the quarantine
registry.  Verdicts are byte-taken from the raws.  The 52 LOSS rows ARE
consumed into the canonical cache by the Part AV fail-closed merger; no WIN
verdict is consumed anywhere (none exists).  11x11 stays UNKNOWN; nodes are
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
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class23101-loss41-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-20261122.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class10661-batch17-20261122"
BATCH_KEYS_SHA_EXPECTED = "db762175272206aa53622f30addc1267d534e8a3e576f70c6a084f21392645d2"
ROW_AUDIT_SHA_EXPECTED = "c19e768f1ce4223de6736713a679028990ef5a884c9886affd62c951e307d5f9"
BASE_CACHE_SHA_EXPECTED = "be9cb24e899fbe93db51e415320c50fa733e378748bb7a41fe13fd7b22f06685"
BASE_CACHE_ROWS_EXPECTED = 6120

LOSS_IDS = [f"u{i:03d}" for i in range(1, 53)]  # resolved LOSS rows (52)
UNADOPTED_WIN_IDS = []                          # batch-17 has zero WIN rows (asserted)
PROBED = LOSS_IDS + UNADOPTED_WIN_IDS           # the published probed set (52)
EXHAUSTED_IDS: list = []                       # batch-17 has zero exhaustion rows (asserted)
BUDGET = 15_000_000


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
        sys.exit("ABORT batch-17 batch-keys.json sha drift")
    if sha(BATCH_DIR / "output/row-audit.json") != ROW_AUDIT_SHA_EXPECTED:
        sys.exit("ABORT batch-17 row-audit.json sha drift")
    OUT.mkdir(parents=True, exist_ok=True)
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
    by_id = {k["key_id"]: k for k in keys}
    if len(by_id) != 52:
        sys.exit(f"ABORT batch-keys key count {len(by_id)} != 52")

    # --- status.log: whole picture -----------------------------------------
    status = parse_status(BATCH_DIR / "output/status.log")
    status_probed = {k for k in status if k in PROBED}
    if status_probed != set(PROBED):
        sys.exit(f"ABORT status probed set != {{u001..u052}}: {sorted(status_probed)}")
    status_resolved = {k for k, v in status.items() if k in PROBED and v[1] in (1, 2)}
    if status_resolved != set(PROBED):
        sys.exit(f"ABORT status resolved set != full probed set: {sorted(status_resolved)}")
    status_wins = {k for k, v in status.items() if k in PROBED and v[1] == 1}
    if status_wins != set(UNADOPTED_WIN_IDS):
        sys.exit(f"ABORT batch-17 WIN set {sorted(status_wins)} != empty (absence gate)")
    status_exhausted = {k for k, v in status.items() if k in PROBED and v[1] == 0}
    if status_exhausted != set(EXHAUSTED_IDS):
        sys.exit(f"ABORT batch-17 must have zero exhaustion rows: {sorted(status_exhausted)}")
    status_text = (BATCH_DIR / "output/status.log").read_text()
    if "EXECUTION-COMPLETE: 52/52 probed = 52 LOSS" not in status_text:
        sys.exit("ABORT status.log lacks the published 'EXECUTION-COMPLETE: 52/52 probed = 52 LOSS' record")
    if re.search(r"^\S+ \S+ (WIN-HALT|HARD-STOP)( |$)", status_text, re.M):
        sys.exit("ABORT status.log contains a dated WIN-HALT/HARD-STOP stop row")
    if not re.search(r"^\S+ u052 PASS 15000000,2,2472941$", status_text, re.M):
        sys.exit("ABORT status.log lacks the final u052 PASS row")

    # --- row-audit.json: whole picture + row-for-row agreement -------------
    ra = json.loads((BATCH_DIR / "output/row-audit.json").read_text())
    if ra["schema"] != "n11-centralreply-closure-class10661-batch17-rowaudit-v1":
        sys.exit(f"ABORT row-audit schema drift: {ra['schema']}")
    if ra["class_index"] != 10661 or ra["batch"] != 17 or ra["key_prefix"] != "u":
        sys.exit("ABORT row-audit whole-picture header drift")
    if ra["budget"] != BUDGET or ra["probed"] != 52:
        sys.exit("ABORT row-audit budget/probed drift")
    if ra["results"] != {"loss": 52, "win": 0, "exhausted": 0, "mismatch": 0}:
        sys.exit(f"ABORT row-audit results drift: {ra['results']}")
    if ra["two_pass_node_exact"] != 52:
        sys.exit("ABORT row-audit two_pass_node_exact != 52")
    if ra["total_nodes_pass_one"] != ra["total_nodes_pass_two"] or ra["total_nodes_pass_one"] != 196_536_452:
        sys.exit("ABORT row-audit total node drift")
    if ra["batch_keys_sha256"] != BATCH_KEYS_SHA_EXPECTED:
        sys.exit("ABORT row-audit batch_keys_sha256 drift")
    if not ra["host_event_incomplete_never_produced_verdict"]:
        sys.exit("ABORT row-audit host_event_incomplete_never_produced_verdict is false")
    if not ra["incomplete_rows_researched_fresh_cold_after_reset"]:
        sys.exit("ABORT row-audit incomplete_rows_researched_fresh_cold_after_reset is false")
    frags = ra["host_event_truncated_fragments"]
    if len(frags) != 5 or any(f["carries_verdict"] for f in frags):
        sys.exit(f"ABORT row-audit host fragments {frags}")
    for f in frags:
        p = BATCH_DIR / f["file"]
        if not p.is_file():
            sys.exit(f"ABORT missing hostevent fragment {p}")
        if sha(p) is None or p.stat().st_size != f["bytes"]:
            sys.exit(f"ABORT hostevent fragment size drift {p}")
        if re.search(r"^replay,", p.read_text(), re.M):
            sys.exit(f"ABORT hostevent fragment carries a verdict row: {p}")
    ra_rows = {r["key_id"]: r for r in ra["rows"]}
    if len(ra_rows) != 52:
        sys.exit(f"ABORT row-audit rows {len(ra_rows)} != 52")

    rows = []           # (kid, s5_index, lo, hi, result, nodes) - adopted LOSS rows
    for kid in LOSS_IDS:
        ref = two_pass(kid)
        if ref["budget"] != BUDGET or ref["stones"] != 5 or ref["is_or"] != 0:
            sys.exit(f"ABORT {kid}: wrong budget/depth {ref}")
        if ref["result"] != 2:
            sys.exit(f"ABORT {kid}: adopted rows must be result 2, got {ref['result']}")
        bk = by_id.get(kid)
        if bk is None:
            sys.exit(f"ABORT batch-keys.json missing {kid}")
        if ref["legal"] != int(bk["legal"]):
            sys.exit(f"ABORT {kid}: legal mismatch raw={ref['legal']} keys={bk['legal']}")
        if (ref["lo"], ref["hi"]) != (int(bk["lo"]), int(bk["hi"])):
            sys.exit(f"ABORT {kid}: key mismatch raw=({ref['lo']},{ref['hi']}) keys=({bk['lo']},{bk['hi']})")
        if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
            sys.exit(f"ABORT {kid}: status.log disagreement {status.get(kid)} vs {(ref['budget'], ref['result'], ref['nodes'])}")
        rr = ra_rows.get(kid)
        if rr is None:
            sys.exit(f"ABORT row-audit missing row {kid}")
        if (not rr["node_exact"]) or rr["result"] != 2 or rr["budget"] != BUDGET:
            sys.exit(f"ABORT {kid}: row-audit row drift {rr}")
        if rr["nodes"] != ref["nodes"] or rr["pass2_nodes"] != ref["nodes"]:
            sys.exit(f"ABORT {kid}: row-audit nodes drift {rr['nodes']}/{rr['pass2_nodes']} vs {ref['nodes']}")
        if rr["legal"] != int(bk["legal"]) or (int(rr["lo"]), int(rr["hi"])) != (int(bk["lo"]), int(bk["hi"])):
            sys.exit(f"ABORT {kid}: row-audit key/legal drift {rr}")
        if int(rr["s5_index"]) != int(bk["s5_index"]) or int(rr["probe_order"]) != int(bk["probe_order"]):
            sys.exit(f"ABORT {kid}: row-audit s5_index/probe_order drift {rr} vs {bk}")
        key = (ref["lo"], ref["hi"])
        if key in quarantined:
            sys.exit(f"ABORT {kid}: quarantined key {key}")
        if key in base_keys:
            sys.exit(f"ABORT {kid}: key already in canonical BASE cache {key} "
                     f"(base={base_keys[key]}, raw={(ref['result'], ref['nodes'])})")
        if any(r[3] == key[0] and r[4] == key[1] for r in rows):
            sys.exit(f"ABORT duplicate key within batch {key}")
        rows.append((kid, int(bk["s5_index"]), ref["lo"], ref["hi"], ref["result"], ref["nodes"]))

    wins = [r for r in rows if r[4] == 1]
    losses = [r for r in rows if r[4] == 2]
    got_losses = sorted(r[0] for r in losses)
    if got_losses != sorted(LOSS_IDS):
        sys.exit(f"ABORT LOSS set mismatch: {got_losses}")
    if len(rows) != 52 or wins or len(losses) != 52:
        sys.exit(f"ABORT resolved row counts {len(rows)}/{len(wins)}/{len(losses)} != 52/0/52")

    hdr = [
        "# n11 central-reply closure batch-17 (class 10661) 52-LOSS canonical-adoption increment (Part AV, 2026-11-22)",
        "# published Part AV declaration (note amendment 2026-11-22, commit 340abef3) + Part AV",
        "#   takeover amendment (note, commit d3ef2dc6, observed HEAD-before-push 432664f7;",
        "#   scope unchanged - ownership transfer only).",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# batch-17 was executed by the Part AU host (52/52 probed = 52 LOSS, 0 WIN, 0",
        "#   exhaustion, 0 mismatch; five host-event truncated fragments never produced a",
        "#   verdict line and were re-run fresh cold; row-audit c19e768f, status.log",
        "#   'EXECUTION-COMPLETE: 52/52 probed = 52 LOSS' record published).",
        "# gates: 3-way (p1/p2/status) node-exact + '# replay_done' completeness, status.log",
        "#   agreement incl. the published EXECUTION-COMPLETE record, row-audit.json 52-row",
        "#   agreement (result/verdict/nodes/legal/(lo,hi)/s5_index/probe_order/whole picture),",
        "#   batch-keys (sha256 db762175) legal/(lo,hi) agreement, resolved keys distinct,",
        "#   ZERO WIN rows (absence gate), ZERO exhaustion rows (absence gate), ZERO",
        "#   BASE-cache overlap (structural gate: batch-17 post-dates the Part AS merge;",
        "#   any overlap ABORTs), quarantine 0.",
        "# ADOPTED set = the full resolved packet {u001..u052} = exactly all 52 LOSS rows.",
        "#   No WIN row exists in batch-17, so full == loss here (machine-stated); no WIN",
        "#   verdict is consumed anywhere by this Part; the 17 unconsumed closure WINs are",
        "#   untouched (scrutiny owner gate 9193f5b6... unchanged).",
        "# The 52 LOSS rows ARE consumed into the canonical cache by the Part AV merger;",
        "#   11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.",
        "# 52 rows: the adopted LOSS verdicts of class 10661's unknown S5 children (17th batch).",
    ]

    lines = list(hdr)
    lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(rows, key=lambda r: (r[2], r[3]))]
    p = OUT / "increment-batch17-loss52-20261122.cache"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{p.name}: {len(rows)} rows, sha256 {sha(p)}")

    manifest = {
        "schema": "batch17-loss52-increments-manifest-v1",
        "batch": 17,
        "class_index": 10661,
        "loss_ids": LOSS_IDS,
        "resolved_ids": LOSS_IDS,
        "win_ids": [],
        "unadopted_win_ids": UNADOPTED_WIN_IDS,
        "exhausted_excluded_ids": EXHAUSTED_IDS,
        "row_counts": {"resolved_rows": len(rows), "wins": len(wins), "losses": len(losses),
                       "exhausted_excluded": 0, "probed_total": 52, "probed_resolved": 52},
        "sha256": {"loss": sha(p)},
        "full_packet_eq_loss_only": True,
        "full_packet_eq_loss_only_rationale": ("batch-17 resolved all 52 probed keys as "
                                                "LOSS; zero WIN rows exist (absence gate) "
                                                "and zero exhaustion rows, so the adopted "
                                                "packet IS the full resolved packet"),
        "win_scenario_exists": False,
        "win_scenario_note": ("batch-17 contains no WIN row; no WIN adoption scenario "
                              "arises from this batch; the 17 unconsumed closure WINs "
                              "are untouched by this Part"),
        "row_audit_agreement_rows": 52,
        "row_audit_sha256": ROW_AUDIT_SHA_EXPECTED,
        "status_log_stop_record": "EXECUTION-COMPLETE: 52/52 probed = 52 LOSS",
        "base_cache_absent_hits": 0,
        "base_cache_rows": len(base_keys),
        "quarantine_hits": 0,
        "interpretation_guard": ("canonical adoption increment: the 52 LOSS rows are "
                                 "consumed into the canonical cache via the fail-closed "
                                 "union merger; no WIN verdict is consumed (none exists "
                                 "in batch-17); 11x11 stays UNKNOWN; nodes are "
                                 "bookkeeping, never verdicts"),
    }
    (OUT / "increments-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print("OK 52 probed rows -> 52 adopted LOSS (u001..u052), zero WIN (absence gate), "
          "zero exhaustion, zero BASE overlap, quarantine 0, full==loss packet, "
          "row-audit 52-row agreement, all gates PASS")


if __name__ == "__main__":
    main()
