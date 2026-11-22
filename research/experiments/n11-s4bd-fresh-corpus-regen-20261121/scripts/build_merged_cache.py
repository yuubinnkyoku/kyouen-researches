#!/usr/bin/env python3
"""Build the merged S5 exact cache for the fresh corpus regeneration lane.

Base: the reply27 JS-replica probe-13 merged cache (byte-preserved pinned
SHA-256). Increment: fresh 15M-budget two-pass exact replays of the 101
declared keys (99 canonical S5 children of S4 (1297036692683752448,0) absent
from the probe-13 chain, plus the 2 unclaimed backward-only LOSS rows),
executed by the pinned Node.js replica jsreplay.js (identical bytes to the
reply27 chain publications).

Fail-closed gates (see merge-manifest.json):
  - determinism: pass1 and pass2 rows must be identical in result and nodes;
  - history: every settled fresh verdict must equal the audited union-backlog
    historical verdict (any disagreement is published and blocks the lane);
  - budget exhaustion is only allowed for TARGET_S5
    (1152921504607899649,536870912), whose row is then the S6-witness-derived
    row (verdict 2, nodes 0), exactly as in the Oct 12 precedent;
  - geometry: every key canonical, quadruple-safe, 5-stone, quarantined-free,
    Board-derived legal count, corpus keys inside the frozen 106-child S4
    boundary;
  - cache: merged file strictly sorted, no duplicates, no base conflicts.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4bd-fresh-corpus-regen-20261121"
INP = EXP / "input"
BASE = ROOT / "research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache"
BASE_SHA = "60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
JSREPLAY_SHA = "845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df"
RAWS = EXP / "output" / "raw"
RAWS2 = EXP / "output" / "raw"
OUT_CACHE = EXP / "output" / "merged-exact-s5-after-js-probe-13-plus-freshregen-20261121.cache"
OUT_MANIFEST = EXP / "output" / "merge-manifest.json"
BUDGET = 15_000_000
S6_KEY = (1152921504675009536, 536870912)
TARGET_S5 = (1152921504607899649, 536870912)
KEY_IDS = [f"k{i:03d}" for i in range(1, 102)] + ["s6w"]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_replay_file(path: Path) -> dict:
    rows, done = [], False
    for line in path.read_text(encoding="utf-8").split("\n"):
        if line.startswith("replay,"):
            f = line.split(",")
            rows.append({
                "stones": int(f[2]), "legal": int(f[3]), "is_or": int(f[4]),
                "budget": int(f[5]), "result": int(f[6]), "nodes": int(f[7]),
                "key_lo": int(f[9]), "key_hi": int(f[10]),
            })
        elif line.startswith("replay_error"):
            raise ValueError(f"replay_error row in {path}: {line}")
        elif line.startswith("# replay_done"):
            done = True
    if not done or len(rows) != 1:
        raise ValueError(f"expected exactly one completed replay row in {path}")
    return rows[0]


def read_input_file(path: Path) -> dict:
    lines = [l for l in path.read_text(encoding="utf-8").split("\n") if l and not l.startswith("#")]
    if len(lines) != 1:
        raise ValueError(f"expected one input row in {path}")
    f = lines[0].split(",")
    return {"stones": int(f[2]), "key": (int(f[3]), int(f[4])), "legal": int(f[5])}


def main() -> None:
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board
    sys.path.insert(0, str(ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"))
    from s5_evidence_policy import is_canonical_safe_s5_key, quarantined_cache_keys
    board = Board(11)

    if sha(BASE) != BASE_SHA:
        raise ValueError("base probe-13 cache SHA-256 pin mismatch")
    if sha(EXP / "scripts" / "jsreplay.js") != JSREPLAY_SHA:
        raise ValueError("jsreplay.js SHA-256 pin mismatch")

    corpus = json.loads((INP / "corpus-def.json").read_text(encoding="utf-8"))
    if corpus["schema"] != "n11-s4bd-fresh-corpus-regen-def-v1":
        raise ValueError("corpus-def schema mismatch")
    legals = {tuple(map(int, k.split(","))): v for k, v in corpus["legals"].items()}
    historical = {tuple(map(int, k.split(","))): v for k, v in corpus["bo_verdicts"].items()}
    corpus99 = {tuple(k) for k in corpus["corpus99"]}
    unclaimed2 = {tuple(k) for k in corpus["unclaimed2"]}
    s5_keys = corpus99 | unclaimed2
    if len(s5_keys) != 101 or TARGET_S5 not in s5_keys:
        raise ValueError("declared S5 key set is not the expected 101")

    with gzip.open(GEOMETRY, "rt", encoding="utf-8") as f:
        geometry = json.load(f)
    if len(geometry) != 3384:
        raise ValueError("geometry class count mismatch")
    s4 = next((row for row in geometry if tuple(row["key"]) == (1297036692683752448, 0)), None)
    if s4 is None or len(s4["children"]) != 106:
        raise ValueError("target S4 geometry row missing or boundary changed")
    s4_children = {tuple(c) for c in s4["children"]}
    if corpus99 - s4_children or len(corpus99) != 99:
        raise ValueError("corpus99 not exactly the frozen S4 children minus chain keys")

    quarantine = quarantined_cache_keys()
    for key in s5_keys:
        if not is_canonical_safe_s5_key(key):
            raise ValueError(f"noncanonical/unsafe declared key {key}")
        if key in quarantine:
            raise ValueError(f"quarantined key declared {key}")
        mask = key[0] | (key[1] << 64)
        if mask.bit_count() != 5 or board.legal(mask).bit_count() != legals[key]:
            raise ValueError(f"legal count mismatch for {key}")

    # per-key raw verification (both passes)
    fresh = {}
    per_key = []
    for kid in KEY_IDS:
        row_in = read_input_file(INP / f"{kid}.input.csv")
        key = row_in["key"]
        r1 = read_replay_file(RAWS / f"{kid}.p1.out")
        r2 = read_replay_file(RAWS2 / f"{kid}.p2.out")
        for r in (r1, r2):
            if (r["key_lo"], r["key_hi"]) != key:
                raise ValueError(f"{kid}: replay row key mismatch")
            if r["stones"] != row_in["stones"] or r["legal"] != row_in["legal"]:
                raise ValueError(f"{kid}: stones/legal mismatch")
            if r["budget"] != BUDGET or r["is_or"] != (1 - r["stones"] % 2):
                raise ValueError(f"{kid}: budget/polarity mismatch")
        if r1["result"] != r2["result"] or r1["nodes"] != r2["nodes"]:
            raise ValueError(
                f"DETERMINISM GATE FAILURE for {kid} {key}: "
                f"pass1=({r1['result']},{r1['nodes']}) pass2=({r2['result']},{r2['nodes']})")
        if key in fresh:
            raise ValueError(f"duplicate key {key}")
        fresh[key] = (r1["result"], r1["nodes"], kid)
        per_key.append({"id": kid, "key": list(key), "stones": row_in["stones"],
                        "legal": row_in["legal"], "result": r1["result"],
                        "nodes": r1["nodes"]})

    if set(fresh) != s5_keys | {S6_KEY}:
        raise ValueError("raw keys do not equal the 101 declared keys plus the S6 witness")
    s6 = fresh.pop(S6_KEY)
    if s6[0] != 2 or s6[1] != 5_859_060:
        raise ValueError(f"S6 witness must settle LOSS with the published 5,859,060 nodes: {s6}")

    for key, (result, nodes, _) in fresh.items():
        if result == 0 and key != TARGET_S5:
            raise ValueError(f"undeclared budget exhaustion for {key}")
        if result == 1:
            raise ValueError(f"fresh WIN forbidden on this lane (history conflict): {key}")
        if key in historical and result in (1, 2) and result != historical[key]:
            raise ValueError(
                f"FRESH/HISTORY VERDICT DISAGREEMENT for {key}: "
                f"fresh={result} historical={historical[key]}")

    settled = {k: v for k, v in fresh.items() if v[0] in (1, 2)}

    # base cache
    base_rows = []
    for line_no, line in enumerate(BASE.read_text(encoding="utf-8").split("\n"), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        f = s.split(",")
        if len(f) != 6 or f[0] != "s5verdict":
            raise ValueError(f"invalid base cache row {line_no}")
        lo, hi, stones, verdict, nodes = map(int, f[1:])
        key = (lo, hi)
        if stones != 5 or verdict not in (1, 2) or nodes < 0 or key in quarantine:
            raise ValueError(f"invalid/quarantined base cache row {line_no}: {key}")
        base_rows.append((key, verdict, nodes))
    base_keys = [k for k, _, _ in base_rows]
    if base_keys != sorted(base_keys) or len(set(base_keys)) != len(base_keys):
        raise ValueError("base cache is not strictly sorted / has duplicates")
    if len(base_rows) != 5756:
        raise ValueError(f"base cache row count changed: {len(base_rows)}")
    if s5_keys & set(base_keys):
        raise ValueError("a declared backward-only key already exists in the base cache")

    merged = list(base_rows)
    added = []
    for key in sorted(settled):
        verdict, nodes, kid = settled[key]
        merged.append((key, verdict, nodes))
        added.append({"id": kid, "key": list(key), "verdict": verdict, "nodes": nodes,
                      "derived": False})
    derived_target = TARGET_S5 not in settled
    if derived_target:
        merged.append((TARGET_S5, 2, 0))
        added.append({"id": fresh[TARGET_S5][2] if TARGET_S5 in fresh else "k012",
                      "key": list(TARGET_S5), "verdict": 2, "nodes": 0, "derived": True})
    merged.sort(key=lambda r: r[0])
    merged_keys = [k for k, _, _ in merged]
    if merged_keys != sorted(merged_keys) or len(set(merged_keys)) != len(merged_keys):
        raise ValueError("merged cache is not strictly sorted / has duplicates")
    if any(k in quarantine for k, _, _ in merged):
        raise ValueError("quarantined key entered the merged cache")
    if len(added) != 101 or len(merged) != len(base_rows) + 101:
        raise ValueError(f"unexpected increment/merged size: {len(added)}/{len(merged)}")

    header = ("# S5 solver-trusted exact; base=merged-exact-s5-after-js-probe-13.cache "
              f"(sha256 {BASE_SHA[:16]}...); increment=101 fresh rows "
              "(99 canonical S5 children of S4 1297036692683752448:0 absent from the chain, "
              "2 unclaimed backward-only rows, 1 S6-witness-derived TARGET_S5 row nodes=0); "
              "see merge-manifest.json\n")
    OUT_CACHE.write_text(
        header + "".join(f"s5verdict,{k[0]},{k[1]},5,{v},{n}\n" for k, v, n in merged),
        encoding="utf-8")

    manifest = {
        "schema": "n11-s4bd-freshregen-merge-manifest-v1",
        "base_cache": {"path": str(BASE.relative_to(ROOT)), "sha256": BASE_SHA, "rows": len(base_rows)},
        "fresh_increment": {
            "declared_s5_keys": 101,
            "s5_rows_added": len(added),
            "direct_settled": sum(1 for a in added if not a["derived"]),
            "derived_rows": [a for a in added if a["derived"]],
            "s6_witness": {"key": list(S6_KEY), "result": 2, "nodes": s6[1],
                           "pass_determinism": "identical result+nodes in both passes",
                           "published_oct12_nodes": 5_859_060},
            "target_s5_fresh_result": fresh[TARGET_S5][0] if TARGET_S5 in fresh else None,
            "target_s5_row_is_derived": derived_target,
        },
        "rows": added,
        "per_key_rows": per_key,
        "merged_cache": {"path": str(OUT_CACHE.relative_to(ROOT)), "sha256": sha(OUT_CACHE),
                         "rows": len(merged)},
        "raws": {"pass1_dir": str(RAWS.relative_to(ROOT)),
                 "pass2_dir": str(RAWS2.relative_to(ROOT))},
        "fail_closed_gates": [
            "determinism: identical result+nodes across the two passes (per key)",
            "history: every settled verdict equals the audited union-backlog historical verdict",
            "budget exhaustion only allowed for TARGET_S5 (row then S6-witness-derived, nodes 0)",
            "no fresh WIN rows (would contradict history and block the lane)",
            "geometry: canonical, safe, quarantined-free, 5-stone, Board-derived legal counts",
            "boundary: corpus99 = frozen 106-child S4 boundary minus the 7 chain keys",
            "S6 witness: canonical 6-stone child of TARGET_S5, settled LOSS with published nodes",
            "cache: strictly sorted, no duplicates, no base conflicts, no quarantined keys",
        ],
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in
                      ("schema", "base_cache", "fresh_increment", "merged_cache")}, indent=1))
    print("OK")


if __name__ == "__main__":
    main()
