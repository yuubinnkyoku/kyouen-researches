#!/usr/bin/env python3
"""Build the batch-13 (class 16930) p002/p003 IF-ADOPTED increments, fail-closed.

Executes the published single-owner Part AI declaration (note amendment,
commit a0cdb0da, 2026-11-22T13:08Z): the declaring host stayed silent with no
status update and no experiment directory for 2h+ (observed HEAD 858a4158 at
2026-11-22T15:18Z), so this run takes over under the Part U / Part Z
takeover convention.  All inputs are published main bytes, re-verified against
this host before use (raws/status.log/batch-keys byte-identical, fetch-back
documented in the README).

Emits three what-if increment caches over the published batch-13 raw replay
rows (4 probed rows, 3-way p1/p2/status node-exact; batch-13 was executed by
the declaring host only, so there is no takeover pass - Part AE verbatim):
  * PWIN2   - the 2 unconsumed closure WIN rows only (p002/p003)
  * PLOSS2  - the 2 probed exact-LOSS rows (p001/p004)
  * PFULL4  - all 4 resolved probed rows (2 WIN + 2 LOSS)

Fail-closed gates: every row must come from BOTH published raw passes with
identical (stones, legal, is_or, budget, result, nodes); legal and (lo,hi)
must match the published batch-keys.json (sha256 c6c56a1a...) for every key;
every declaring-host status.log PASS row must agree with the raws on
(budget, result, nodes); the WIN set must be exactly {p002, p003}; all keys
must be distinct, ABSENT from the canonical BASE cache (6,027 rows, sha256
95e868d6...; ANY overlap ABORTs - batch-13 post-dates the Part Y merge and
no pre-consumed duplicates are anticipated, but the gate is kept structural),
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
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class16930-batch13-20261122"
BATCH_KEYS_SHA_EXPECTED = "c6c56a1a0552b8a87d1e1f5f9e0d6c3955cf1f58a85ef6726317d17846a0a2c7"

RESOLVED = ["p001", "p002", "p003", "p004"]
WIN_IDS = ["p002", "p003"]


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
        sys.exit("ABORT batch-13 batch-keys.json sha drift")
    OUT.mkdir(parents=True, exist_ok=True)
    base_keys = {}
    with BASE_CACHE.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            base_keys[(int(row[1]), int(row[2]))] = (int(row[4]), int(row[5]))
    q = json.loads(json.dumps(json.loads(QUARANTINE.read_text())))
    quarantined = {tuple(e["key"]) for e in q["entries"] if e.get("active")}

    keys = json.loads((BATCH_DIR / "input/batch-keys.json").read_text())["keys"]
    by_id = {k["key_id"]: k for k in keys}
    status = parse_status(BATCH_DIR / "output/status.log")
    status_resolved = {k for k, v in status.items() if v[1] in (1, 2)}
    if status_resolved != set(RESOLVED):
        sys.exit(f"ABORT status resolved set != expected probed set: "
                 f"extra={sorted(status_resolved - set(RESOLVED))} missing={sorted(set(RESOLVED) - status_resolved)}")

    rows = []  # (kid, s5_index, lo, hi, result, nodes)
    for kid in RESOLVED:
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
        if ref["result"] not in (1, 2):
            sys.exit(f"ABORT {kid}: non-resolved result {ref['result']} in resolved set")
        key = (ref["lo"], ref["hi"])
        if key in base_keys:
            # structural gate: batch-13 post-dates the Part Y merge; ANY overlap ABORTs.
            sys.exit(f"ABORT {kid}: key already in canonical BASE cache {key} "
                     f"(base={base_keys[key]}, raw={(ref['result'], ref['nodes'])})")
        if key in quarantined:
            sys.exit(f"ABORT {kid}: quarantined key {key}")
        if any(r[3] == key[0] and r[4] == key[1] for r in rows):
            sys.exit(f"ABORT duplicate key within batch {key}")
        rows.append((kid, int(bk["s5_index"]), ref["lo"], ref["hi"], ref["result"], ref["nodes"]))

    wins = [r for r in rows if r[4] == 1]
    losses = [r for r in rows if r[4] == 2]
    got_wins = sorted(r[0] for r in wins)
    if got_wins != sorted(WIN_IDS):
        sys.exit(f"ABORT WIN set mismatch: {got_wins}")
    if len(rows) != 4 or len(wins) != 2 or len(losses) != 2:
        sys.exit(f"ABORT row counts {len(rows)}/{len(wins)}/{len(losses)} != 4/2/2")

    hdr = [
        "# n11 central-reply closure batch-13 (class 16930) IF-ADOPTED increment (Part AI takeover, 2026-11-22)",
        "# published Part AI declaration a0cdb0da (2026-11-22T13:08Z); declaring host silent 2h+ (no status",
        "#   update, no experiment dir at observed HEAD 858a4158); takeover per the Part U / Part Z convention.",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# batch-13 was executed by the declaring host only (no takeover pass exists; Part AE verbatim).",
        "# gates: 3-way (p1/p2/status) node-exact, status.log agreement, batch-keys (sha256 c6c56a1a)",
        "#   legal/(lo,hi) agreement, 4 distinct keys, ZERO BASE-cache overlap (structural gate: batch-13",
        "#   post-dates the Part Y merge; any overlap ABORTs), quarantine 0. WIN set = exactly {p002, p003}.",
        "# Methodology per Part H / H-bis / J / R / V / AB / AH: WIN-only vs LOSS-only vs full packet.",
        "# Read-only what-if analysis increments; verdicts are NOT consumed; 11x11 stays UNKNOWN;",
        "# nodes are bookkeeping, never verdicts.",
    ]
    tags = {
        "win": "# 2 rows: the unconsumed closure WINs p002/p003 (13th-batch WIN pair; third-impl verified by Part AG).",
        "loss": "# 2 rows: the probed exact-LOSS rows p001/p004.",
        "all": "# 4 rows: all resolved probed batch-13 rows (2 WIN + 2 LOSS).",
    }
    names = {
        "win": "increment-batch13-wins2-IFADOPTED-20261122.cache",
        "loss": "increment-batch13-loss2-IFADOPTED-20261122.cache",
        "all": "increment-batch13-full4-IFADOPTED-20261122.cache",
    }

    def write(tag, sel):
        lines = hdr + [tags[tag]]
        lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(sel, key=lambda r: (r[2], r[3]))]
        p = OUT / names[tag]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{names[tag]}: {len(sel)} rows, sha256 {sha(p)}")

    write("win", wins)
    write("loss", losses)
    write("all", rows)

    manifest = {
        "schema": "batch13-ifadopted-increments-manifest-v1",
        "batch": 13,
        "class_index": 16930,
        "win_ids": WIN_IDS,
        "resolved_ids": RESOLVED,
        "row_counts": {"rows": len(rows), "wins": len(wins), "losses": len(losses)},
        "sha256": {tag: sha(OUT / names[tag]) for tag in names},
        "base_cache_absent_hits": 0,
        "quarantine_hits": 0,
        "interpretation_guard": "read-only what-if IF-ADOPTED analysis inputs; verdicts NOT consumed; 11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts",
    }
    (OUT / "increments-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print("OK 4 probed rows -> 4 unique-new (2 WIN + 2 LOSS), zero BASE overlap, quarantine 0, all gates PASS")


if __name__ == "__main__":
    main()
