#!/usr/bin/env python3
"""Build the batch-15 (class 5830) r001/r002 IF-ADOPTED increment, fail-closed.

Executes the published single-owner Part AN declaration (note amendment,
pushed 2026-11-22 after the Part AI status update; declaring host = this
lane session).  All inputs are published main bytes, re-verified against
this host before use (raws/status.log/batch-keys byte-identical vs main at
observed HEAD `e17a708d`, 10/10, kit mirror source).

Emits the WIN-only what-if increment cache over the published batch-15 raw
replay rows:

  * PWIN2 - the 2 unconsumed closure WIN rows only (r001/r002)

Batch-15 facts being encoded (published, Part AK + third-impl Part AL):
wave-1 fired the pre-registered WIN-HALT rule twice (r001: 2-pass node-exact
result 1, 2,521,302 nodes; r002: result 1, 5,973,924 nodes), and r003/r004
are 15M budget EXHAUSTION rows (result 0, nodes == budget) - honest UNKNOWN,
NOT verdicts.  The exhaustion rows are therefore EXCLUDED from the increment
by a type gate (result 0 is not a verdict), and since batch-15 has ZERO
resolved LOSS rows, the "full packet" scenario is IDENTICAL to the WIN-only
scenario: adopting every resolved row of batch-15 == adopting {r001, r002}.
No PLOSS2/PFULL4 scenario exists for this batch; that absence is asserted
here (loss-resolved set empty).

Fail-closed gates: every increment row must come from BOTH published raw
passes with identical (stones, legal, is_or, budget, result, nodes); legal
and (lo,hi) must match the published batch-keys.json (sha256 af3e4c46...)
for every key; every declaring-host status.log PASS row must agree with the
raws on (budget, result, nodes); the exhaustion rows r003/r004 must be
2-pass node-exact result 0 with nodes == budget and are excluded (type
gate); the WIN set must be exactly {r001, r002}; all keys distinct, ABSENT
from the canonical BASE cache (6,027 rows, sha256 95e868d6...; ANY overlap
ABORTs - batch-15 post-dates the Part Y merge), and absent from the
quarantine registry.  Verdicts are byte-taken from the raws.  Read-only
what-if analysis inputs; verdicts are NOT consumed.  11x11 stays UNKNOWN;
nodes are bookkeeping, never verdicts.
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
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class5830-batch15-20261122"
BATCH_KEYS_SHA_EXPECTED = "af3e4c46af0d84bcb248c350283b07e26b901f6e0d196038e24bd1292b133727"

WIN_IDS = ["r001", "r002"]       # resolved WIN rows
EXHAUSTED_IDS = ["r003", "r004"]  # budget exhaustion, result 0, NOT verdicts
PROBED = ["r001", "r002", "r003", "r004"]


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
        sys.exit("ABORT batch-15 batch-keys.json sha drift")
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
        sys.exit(f"ABORT status probed set != {{r001..r004}}: {sorted(status_probed)}")
    status_resolved = {k for k, v in status.items() if k in PROBED and v[1] in (1, 2)}
    if status_resolved != set(WIN_IDS):
        sys.exit(f"ABORT status resolved set != WIN set: {sorted(status_resolved)}")
    status_exhausted = {k for k, v in status.items() if k in PROBED and v[1] == 0}
    if status_exhausted != set(EXHAUSTED_IDS):
        sys.exit(f"ABORT status exhaustion set mismatch: {sorted(status_exhausted)}")

    rows = []           # (kid, s5_index, lo, hi, result, nodes) - resolved verdict rows
    exhausted_info = []  # bookkeeping only, NOT verdicts
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
        if kid in EXHAUSTED_IDS:
            # type gate: exhaustion is honest UNKNOWN, never a verdict, excluded
            if ref["result"] != 0 or ref["nodes"] != ref["budget"]:
                sys.exit(f"ABORT {kid}: exhaustion row must be result 0 / nodes==budget: {ref}")
            exhausted_info.append({
                "key_id": kid, "s5_index": int(bk["s5_index"]),
                "lo": ref["lo"], "hi": ref["hi"],
                "nodes": ref["nodes"], "budget": ref["budget"],
                "verdict": None,
                "treatment": "excluded: result 0 budget exhaustion = honest UNKNOWN, not a verdict",
            })
            continue
        if ref["result"] not in (1, 2):
            sys.exit(f"ABORT {kid}: non-resolved result {ref['result']} in resolved set")
        if key in base_keys:
            # structural gate: batch-15 post-dates the Part Y merge; ANY overlap ABORTs.
            sys.exit(f"ABORT {kid}: key already in canonical BASE cache {key} "
                     f"(base={base_keys[key]}, raw={(ref['result'], ref['nodes'])})")
        if any(r[3] == key[0] and r[4] == key[1] for r in rows):
            sys.exit(f"ABORT duplicate key within batch {key}")
        rows.append((kid, int(bk["s5_index"]), ref["lo"], ref["hi"], ref["result"], ref["nodes"]))

    wins = [r for r in rows if r[4] == 1]
    losses = [r for r in rows if r[4] == 2]
    got_wins = sorted(r[0] for r in wins)
    if got_wins != sorted(WIN_IDS):
        sys.exit(f"ABORT WIN set mismatch: {got_wins}")
    if len(rows) != 2 or len(wins) != 2 or losses:
        sys.exit(f"ABORT resolved row counts {len(rows)}/{len(wins)}/{len(losses)} != 2/2/0")
    if len(exhausted_info) != 2:
        sys.exit(f"ABORT exhaustion rows {len(exhausted_info)} != 2")

    hdr = [
        "# n11 central-reply closure batch-15 (class 5830) IF-ADOPTED increment (Part AN, 2026-11-22)",
        "# published Part AN declaration (note amendment 2026-11-22, after Part AI status update;",
        "#   observed HEAD-before-push recorded in the declaration commit message).",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# batch-15 was executed by the declaring host only (no takeover pass exists; Part AK).",
        "# Third-implementation verdict-level cross-verification of both WIN rows is published",
        "#   (Part AL, audit 51/51 gates). r003/r004 are budget EXHAUSTION rows (result 0,",
        "#   nodes==budget): honest UNKNOWN, excluded from the increment by the type gate.",
        "# gates: 3-way (p1/p2/status) node-exact, status.log agreement, batch-keys (sha256 af3e4c46)",
        "#   legal/(lo,hi) agreement, resolved keys distinct, ZERO BASE-cache overlap (structural gate:",
        "#   batch-15 post-dates the Part Y merge; any overlap ABORTs), quarantine 0.",
        "# WIN set = exactly {r001, r002}; zero resolved LOSS rows, so the 'full packet' scenario",
        "#   is IDENTICAL to this WIN-only scenario (machine-asserted in the manifest).",
        "# Read-only what-if analysis increment; verdicts are NOT consumed; 11x11 stays UNKNOWN;",
        "# nodes are bookkeeping, never verdicts.",
        "# 2 rows: the unconsumed closure WINs r001/r002 (15th-batch WIN pair).",
    ]

    lines = list(hdr)
    lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(rows, key=lambda r: (r[2], r[3]))]
    p = OUT / "increment-batch15-wins2-IFADOPTED-20261122.cache"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{p.name}: {len(rows)} rows, sha256 {sha(p)}")

    manifest = {
        "schema": "batch15-ifadopted-increments-manifest-v1",
        "batch": 15,
        "class_index": 5830,
        "win_ids": WIN_IDS,
        "resolved_ids": WIN_IDS,
        "exhausted_excluded_ids": EXHAUSTED_IDS,
        "exhausted_rows": exhausted_info,
        "row_counts": {"resolved_rows": len(rows), "wins": len(wins), "losses": len(losses),
                       "exhausted_excluded": len(exhausted_info)},
        "sha256": {"win": sha(p)},
        "full_packet_eq_win_only": True,
        "full_packet_eq_win_only_rationale": ("batch-15 has zero resolved LOSS rows; the exhaustion rows "
                                              "r003/r004 (result 0, nodes==budget) are not verdicts and are "
                                              "excluded by the type gate, so adopting every resolved row "
                                              "equals adopting {r001, r002}"),
        "loss_scenario_exists": False,
        "base_cache_absent_hits": 0,
        "quarantine_hits": 0,
        "interpretation_guard": "read-only what-if IF-ADOPTED analysis inputs; verdicts NOT consumed; 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print("OK 4 probed rows -> 2 resolved WIN (r001/r002) + 2 exhaustion excluded (type gate), "
          "zero BASE overlap, quarantine 0, full==win, all gates PASS")


if __name__ == "__main__":
    main()
