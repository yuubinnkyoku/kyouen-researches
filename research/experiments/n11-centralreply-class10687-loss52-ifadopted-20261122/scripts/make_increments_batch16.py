#!/usr/bin/env python3
"""Build the batch-16 (class 10687) 52-row LOSS IF-ADOPTED increment, fail-closed.

Executes the published single-owner Part AO declaration (note amendment,
pushed 2026-11-22 after the Part AM status update; declaring host = this
lane session).  All inputs are published main bytes, re-verified against
this host before use (raws/status.log/batch-keys byte-identical vs main at
publication commit `d349e8f8` + erratum `572dcbc3`, fetch-back 180/180 x2,
kit mirror source).

Emits the LOSS-only what-if increment cache over the published batch-16 raw
replay rows:

  * PLOSS52 - all 52 resolved LOSS rows (t001..t052)

Batch-16 facts being encoded (published, Part AM):
all 52 keys finished as 2-pass node-exact result 2 (LOSS) at budget 15M -
zero WIN rows, zero exhaustion rows (WIN 0 / exhaustion 0 / mismatch 0,
total 168,262,885 nodes per pass, row-audit `589c1141...`).  Since batch-16
has ZERO WIN rows and ZERO exhaustion rows, the "full packet" scenario is
IDENTICAL to this LOSS-only scenario: adopting every resolved row of
batch-16 == adopting the 52 LOSS rows {t001..t052}.  No PWIN scenario
exists for this batch; that absence is asserted here (win-resolved set
empty).

Fail-closed gates: every increment row must come from BOTH published raw
passes with identical (stones, legal, is_or, budget, result, nodes); legal
and (lo,hi) must match the published batch-keys.json (sha256 465cf447...)
for every key; every declaring-host status.log PASS row must agree with the
raws on (budget, result, nodes); the resolved set must be exactly 52 keys,
all result 2; the status.log probed set must be exactly {t001..t052}; all
keys distinct, ABSENT from the canonical BASE cache (6,027 rows, sha256
95e868d6...; ANY overlap ABORTs - batch-16 post-dates the Part Y merge),
and absent from the quarantine registry.  Verdicts are byte-taken from the
raws.  Read-only what-if analysis inputs; verdicts are NOT consumed.  11x11
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
BASE_CACHE = ROOT / "research/experiments/n11-central-reply-8784-closure-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-20261122.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class10687-batch16-20261122"
BATCH_KEYS_SHA_EXPECTED = "465cf44721a661ce94babe12212c26c697ebb346392548fcdafaa9d3e8c3dd4e"

LOSS_IDS = [f"t{i:03d}" for i in range(1, 53)]  # resolved LOSS rows (all 52)
WIN_IDS: list = []                               # batch-16 has zero WIN rows (asserted)
EXHAUSTED_IDS: list = []                         # batch-16 has zero exhaustion rows (asserted)
PROBED = list(LOSS_IDS)


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


def main() -> None:
    if sha(BASE_CACHE) != "95e868d6762925b9a27ad963a825a9ad4fd5131a864eb82fac0db77d7acdb326":
        sys.exit("ABORT base cache sha drift")
    if sha(BATCH_DIR / "input/batch-keys.json") != BATCH_KEYS_SHA_EXPECTED:
        sys.exit("ABORT batch-16 batch-keys.json sha drift")
    OUT.mkdir(parents=True, exist_ok=True)
    base_keys = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    q = json.loads(QUARANTINE.read_text())
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    keys = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())["keys"]
    by_id = {k["key_id"]: k for k in keys}
    if len(by_id) != 52:
        sys.exit(f"ABORT batch-keys key count {len(by_id)} != 52")
    status = parse_status(BATCH_DIR / "output/status.log")
    status_probed = {k for k in status if k in PROBED}
    if status_probed != set(PROBED):
        sys.exit(f"ABORT status probed set != {{t001..t052}}: {sorted(status_probed)}")
    status_resolved = {k for k, v in status.items() if k in PROBED and v[1] in (1, 2)}
    if status_resolved != set(PROBED):
        sys.exit(f"ABORT status resolved set != full probed set: {sorted(status_resolved)}")
    status_wins = {k for k, v in status.items() if k in PROBED and v[1] == 1}
    if status_wins:
        sys.exit(f"ABORT batch-16 must have zero WIN rows: {sorted(status_wins)}")
    status_exhausted = {k for k, v in status.items() if k in PROBED and v[1] == 0}
    if status_exhausted:
        sys.exit(f"ABORT batch-16 must have zero exhaustion rows: {sorted(status_exhausted)}")

    rows = []           # (kid, s5_index, lo, hi, result, nodes) - resolved verdict rows
    for kid in PROBED:
        variants = {}
        for tag in ("p1", "p2"):
            p = BATCH_DIR / f"output/raw/{kid}.{tag}.out"
            if not p.is_file():
                sys.exit(f"ABORT missing raw {p}")
            variants[tag] = parse_replay(p)
        ref = variants["p1"]
        fields = ("stones", "legal", "is_or", "budget", "result", "nodes", "lo", "hi")
        for tag, r in variants.items():
            if tuple(r[f] for f in fields) != tuple(ref[f] for f in fields):
                sys.exit(f"ABORT {kid}: pass mismatch {tag} {r} vs p1 {ref}")
        if ref["budget"] != 15000000 or ref["stones"] != 5 or ref["is_or"] != 0:
            sys.exit(f"ABORT {kid}: wrong budget/depth {ref}")
        if ref["result"] != 2:
            sys.exit(f"ABORT {kid}: batch-16 resolved rows must all be result 2, got {ref['result']}")
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
            # structural gate: batch-16 post-dates the Part Y merge; ANY overlap ABORTs.
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
        "# n11 central-reply closure batch-16 (class 10687) IF-ADOPTED increment (Part AO, 2026-11-22)",
        "# published Part AO declaration (note amendment 2026-11-22, after Part AM status update;",
        "#   observed HEAD-before-push recorded in the declaration commit message).",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# batch-16 was executed by the declaring host only (no takeover pass exists; Part AM)",
        "#   and completed 52/52 all LOSS (WIN 0, exhaustion 0, mismatch 0; row-audit 589c1141).",
        "# gates: 3-way (p1/p2/status) node-exact, status.log agreement, batch-keys (sha256 465cf447)",
        "#   legal/(lo,hi) agreement, resolved keys distinct, ZERO BASE-cache overlap (structural gate:",
        "#   batch-16 post-dates the Part Y merge; any overlap ABORTs), quarantine 0.",
        "# LOSS set = exactly {t001..t052}; zero WIN rows and zero exhaustion rows, so the 'full",
        "#   packet' scenario is IDENTICAL to this LOSS-only scenario (machine-asserted in the",
        "#   manifest). No PWIN scenario exists for this batch (asserted).",
        "# Read-only what-if analysis increment; verdicts are NOT consumed; 11x11 stays UNKNOWN;",
        "# nodes are bookkeeping, never verdicts.",
        "# 52 rows: the resolved LOSS verdicts of class 10687's unknown S5 children (16th batch).",
    ]

    lines = list(hdr)
    lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(rows, key=lambda r: (r[2], r[3]))]
    p = OUT / "increment-batch16-loss52-IFADOPTED-20261122.cache"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{p.name}: {len(rows)} rows, sha256 {sha(p)}")

    manifest = {
        "schema": "batch16-ifadopted-increments-manifest-v1",
        "batch": 16,
        "class_index": 10687,
        "loss_ids": LOSS_IDS,
        "resolved_ids": LOSS_IDS,
        "win_ids": WIN_IDS,
        "exhausted_excluded_ids": EXHAUSTED_IDS,
        "row_counts": {"resolved_rows": len(rows), "wins": len(wins), "losses": len(losses),
                       "exhausted_excluded": 0},
        "sha256": {"loss": sha(p)},
        "full_packet_eq_loss_only": True,
        "full_packet_eq_loss_only_rationale": ("batch-16 has zero WIN rows and zero exhaustion "
                                              "rows (all 52 probed keys resolved result 2), so "
                                              "adopting every resolved row equals adopting the "
                                              "52 LOSS rows"),
        "win_scenario_exists": False,
        "base_cache_absent_hits": 0,
        "quarantine_hits": 0,
        "interpretation_guard": "read-only what-if IF-ADOPTED analysis inputs; verdicts NOT consumed; 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print("OK 52 probed rows -> 52 resolved LOSS (t001..t052), zero WIN, zero exhaustion, "
          "zero BASE overlap, quarantine 0, full==loss, all gates PASS")


if __name__ == "__main__":
    main()
