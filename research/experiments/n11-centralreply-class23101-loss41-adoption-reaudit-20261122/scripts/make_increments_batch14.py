#!/usr/bin/env python3
"""Build the batch-14 (class 23101) 41-LOSS canonical-adoption increment, fail-closed.

Executes the published single-owner Part AS declaration (note amendment,
pushed 2026-11-22 as commit 5b6af2ed after the Part AR status update;
declaring host = this lane session).  All inputs are published main bytes,
re-verified against this host before use (batch-14 dir at publication commit
7b211d38: raws 84 (q001-q042 p1/p2) + status.log + batch-keys.json,
MANIFEST-sha256 per-file verified on this host; current canonical exact-S5
verdict cache 6,079 rows sha256 342e8683... fetched at HEAD and byte-pinned).

Emits the CANONICAL-ADOPTION increment cache over the published batch-14 raw
replay rows:

  * the 41 resolved LOSS rows {q001..q041}

The 42nd probed key q042 is a two-pass node-exact WIN (result 1,
9,149,084 nodes, published WIN-HALT row).  Its verdict is NOT consumed by
this Part: the WIN row is detected here from BOTH published raw passes plus
the status.log `q042 WIN-HALT` stop row, verified absent from the BASE
cache, and then EXCLUDED from the increment by machine (the adoption packet
contains zero WIN rows).  The full resolved packet (42 rows) is therefore NOT
identical to this LOSS-only increment: full != loss for batch-14, and WIN
adoption stays gated on the scrutiny owner's C++ second implementation.

Fail-closed gates: every increment row must come from BOTH published raw
passes with identical (stones, legal, is_or, budget, result, nodes); legal
and (lo,hi) must match the published batch-keys.json (sha256 dfde0e90...)
for every key; every status.log PASS row must agree with the raws on
(budget, result, nodes); the status.log probed set must be exactly
{q001..q042} with the WIN-HALT and WAVE-END stop=1 rows present; the LOSS
set must be exactly {q001..q041} all result 2; the WIN set must be exactly
{q042} (2-pass verified, then machine-excluded); zero exhaustion rows; all
keys distinct, ABSENT from the canonical BASE cache (6,079 rows, sha256
342e8683...; ANY overlap ABORTs - batch-14 post-dates the Part AP merge),
and absent from the quarantine registry.  Verdicts are byte-taken from the
raws.  The 41 LOSS rows ARE consumed into the canonical cache by the Part
AS fail-closed merger; the q042 WIN row is NOT consumed anywhere.  11x11
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
BASE_CACHE = ROOT / "research/experiments/n11-centralreply-class10687-loss52-adoption-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-20261122.cache"
QUARANTINE = ROOT / "results/n11-s5-evidence-quarantine.json"
BATCH_DIR = ROOT / "research/experiments/n11-centralreply-closure-class23101-batch14-20261122"
BATCH_KEYS_SHA_EXPECTED = "dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f"
BASE_CACHE_SHA_EXPECTED = "342e86838e0c2bef915798059cb397f7c91e59c65426bf74db19530ecdd7979e"

LOSS_IDS = [f"q{i:03d}" for i in range(1, 42)]  # resolved LOSS rows (41)
UNADOPTED_WIN_IDS = ["q042"]                     # 2-pass WIN, NOT adopted here
PROBED = LOSS_IDS + UNADOPTED_WIN_IDS            # the published probed set (42)
EXHAUSTED_IDS: list = []                         # batch-14 has zero exhaustion rows (asserted)


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
        sys.exit("ABORT batch-14 batch-keys.json sha drift")
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
        sys.exit(f"ABORT status probed set != {{q001..q042}}: {sorted(status_probed)}")
    status_resolved = {k for k, v in status.items() if k in PROBED and v[1] in (1, 2)}
    if status_resolved != set(PROBED):
        sys.exit(f"ABORT status resolved set != full probed set: {sorted(status_resolved)}")
    status_wins = {k for k, v in status.items() if k in PROBED and v[1] == 1}
    if status_wins != set(UNADOPTED_WIN_IDS):
        sys.exit(f"ABORT batch-14 WIN set {sorted(status_wins)} != {{'q042'}}")
    status_exhausted = {k for k, v in status.items() if k in PROBED and v[1] == 0}
    if status_exhausted:
        sys.exit(f"ABORT batch-14 must have zero exhaustion rows: {sorted(status_exhausted)}")
    status_text = (BATCH_DIR / "output/status.log").read_text()
    if "q042 WIN-HALT" not in status_text:
        sys.exit("ABORT status.log lacks the published 'q042 WIN-HALT' stop row")
    if not re.search(r"^.*WAVE-END q039 q040 q041 q042 stop=1$", status_text, re.M):
        sys.exit("ABORT status.log lacks the published WAVE-END stop=1 row")

    # --- the single unadopted WIN row: detect, verify, exclude ---------------
    for kid in UNADOPTED_WIN_IDS:
        ref = two_pass(kid)
        if ref["budget"] != 15000000 or ref["stones"] != 5 or ref["is_or"] != 0:
            sys.exit(f"ABORT {kid}: wrong budget/depth {ref}")
        if ref["result"] != 1:
            sys.exit(f"ABORT {kid}: published WIN row must be result 1, got {ref['result']}")
        bk = by_id.get(kid)
        if ref["legal"] != int(bk["legal"]) or (ref["lo"], ref["hi"]) != (int(bk["lo"]), int(bk["hi"])):
            sys.exit(f"ABORT {kid}: batch-keys disagreement win raw={ref} keys={bk}")
        if status.get(kid) != (ref["budget"], ref["result"], ref["nodes"]):
            sys.exit(f"ABORT {kid}: status.log disagreement {status.get(kid)} vs raw")
        wkey = (ref["lo"], ref["hi"])
        if wkey in quarantined:
            sys.exit(f"ABORT {kid}: quarantined key {wkey}")
        if wkey in base_keys:
            sys.exit(f"ABORT {kid}: WIN key already in canonical BASE cache {wkey}")
    win_key = (int(by_id["q042"]["lo"]), int(by_id["q042"]["hi"]))
    win_s5_index = int(by_id["q042"]["s5_index"])

    rows = []           # (kid, s5_index, lo, hi, result, nodes) - adopted LOSS rows
    for kid in LOSS_IDS:
        ref = two_pass(kid)
        if ref["budget"] != 15000000 or ref["stones"] != 5 or ref["is_or"] != 0:
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
        key = (ref["lo"], ref["hi"])
        if key in quarantined:
            sys.exit(f"ABORT {kid}: quarantined key {key}")
        if key in base_keys:
            sys.exit(f"ABORT {kid}: key already in canonical BASE cache {key} "
                     f"(base={base_keys[key]}, raw={(ref['result'], ref['nodes'])})")
        if key == win_key:
            sys.exit("ABORT WIN key reachable from the LOSS id list")
        if any(r[3] == key[0] and r[4] == key[1] for r in rows):
            sys.exit(f"ABORT duplicate key within batch {key}")
        rows.append((kid, int(bk["s5_index"]), ref["lo"], ref["hi"], ref["result"], ref["nodes"]))

    wins = [r for r in rows if r[4] == 1]
    losses = [r for r in rows if r[4] == 2]
    got_losses = sorted(r[0] for r in losses)
    if got_losses != sorted(LOSS_IDS):
        sys.exit(f"ABORT LOSS set mismatch: {got_losses}")
    if len(rows) != 41 or wins or len(losses) != 41:
        sys.exit(f"ABORT resolved row counts {len(rows)}/{len(wins)}/{len(losses)} != 41/0/41")

    hdr = [
        "# n11 central-reply closure batch-14 (class 23101) 41-LOSS canonical-adoption increment (Part AS, 2026-11-22)",
        "# published Part AS declaration (note amendment 2026-11-22, commit 5b6af2ed;",
        "#   observed HEAD-before-push b394c3ca recorded in the declaration commit message).",
        "# 2-pass node-exact exact-S5 verdicts at budget 15M, fresh cold, pinned jsreplay.js",
        "#   sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df",
        "# batch-14 was executed by the Part AQ takeover host (42/52 probed = 41 LOSS +",
        "#   1 WIN-HALT at q042, exhaustion 0, mismatch 0; row-audit cc22a1c8, status.log",
        "#   'q042 WIN-HALT' + WAVE-END stop=1 stop rows published).",
        "# gates: 3-way (p1/p2/status) node-exact, status.log agreement incl. the published",
        "#   WIN-HALT stop rows, batch-keys (sha256 dfde0e90) legal/(lo,hi) agreement,",
        "#   resolved keys distinct, ZERO BASE-cache overlap (structural gate: batch-14",
        "#   post-dates the Part AP merge; any overlap ABORTs), quarantine 0.",
        "# ADOPTED set = exactly the 41 LOSS rows {q001..q041}. The WIN row q042",
        "#   (s5_index 745184, result 1, 9,149,084 nodes) is verified 2-pass here and then",
        "#   MACHINE-EXCLUDED from this increment: its verdict is NOT consumed (the 15th",
        "#   unconsumed closure WIN; scrutiny owner gate 9193f5b6... unchanged). Adopting",
        "#   every resolved batch-14 row would include that WIN row, so full != loss here;",
        "#   this partial-packet adoption consumes the 41 LOSS rows only.",
        "# The 41 LOSS rows ARE consumed into the canonical cache by the Part AS merger;",
        "#   11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts.",
        "# 41 rows: the adopted LOSS verdicts of class 23101's unknown S5 children (14th batch).",
    ]

    lines = list(hdr)
    lines += [f"s5verdict,{r[2]},{r[3]},5,{r[4]},{r[5]}" for r in sorted(rows, key=lambda r: (r[2], r[3]))]
    p = OUT / "increment-batch14-loss41-20261122.cache"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{p.name}: {len(rows)} rows, sha256 {sha(p)}")

    manifest = {
        "schema": "batch14-loss41-increments-manifest-v1",
        "batch": 14,
        "class_index": 23101,
        "loss_ids": LOSS_IDS,
        "resolved_ids": LOSS_IDS,
        "win_ids": [],
        "unadopted_win_ids": UNADOPTED_WIN_IDS,
        "unadopted_win_key": list(win_key),
        "unadopted_win_s5_index": win_s5_index,
        "exhausted_excluded_ids": EXHAUSTED_IDS,
        "row_counts": {"resolved_rows": len(rows), "wins": len(wins), "losses": len(losses),
                       "exhausted_excluded": 0, "probed_total": 52, "probed_resolved": 42},
        "sha256": {"loss": sha(p)},
        "full_packet_eq_loss_only": False,
        "full_packet_eq_loss_only_rationale": ("batch-14 resolved 42 of 52 probed keys; "
                                                "the single WIN row q042 is NOT adopted "
                                                "(verdict not consumed; scrutiny-owner "
                                                "gate), so the adopted packet is the "
                                                "41 LOSS rows only"),
        "win_scenario_exists": True,
        "win_scenario_note": ("a single-WIN (q042) if-adopted decomposition is a "
                              "separate future Part (Part V/R/AB/AH/AI/AN flow); "
                              "it is out of scope for this adoption"),
        "base_cache_absent_hits": 0,
        "base_cache_rows": len(base_keys),
        "quarantine_hits": 0,
        "interpretation_guard": ("canonical adoption increment: the 41 LOSS rows are "
                                 "consumed into the canonical cache via the fail-closed "
                                 "union merger; the q042 WIN verdict is NOT consumed; "
                                 "11x11 stays UNKNOWN; nodes are bookkeeping, never verdicts"),
    }
    (OUT / "increments-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print("OK 42 probed rows -> 41 adopted LOSS (q001..q041) + 1 verified machine-excluded "
          "WIN (q042, not consumed), zero exhaustion, zero BASE overlap, quarantine 0, "
          "partial packet full!=loss, all gates PASS")


if __name__ == "__main__":
    main()
