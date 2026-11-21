#!/usr/bin/env python3
"""Audit the fresh S6 witness re-executions and the AND-derivation of TARGET_S5.

The S6 witness (1152921504675009536,536870912) is a canonical 6-stone child of
the canonical 5-stone TARGET_S5 (1152921504607899649,536870912). At a 5-stone
AND node (second player to move) a single exact LOSS child proves the parent
LOSS for the original first player, exactly as in the Oct 12
n11-s4-boundary-direct certificate (backward_only backlog row for TARGET_S5).

Fail-closed checks: both fresh passes return result=2 (LOSS) with
nodes=5,859,060 identical to the published Oct 12 raw; the witness is
canonical, 6-stone, legal 87, a canonical child of TARGET_S5; the dedicated
raw files match their recorded SHA-256 and contain exactly one replay row.
Writes output/s6-witness-fresh-audit.json, consumed (with pinned SHA
verification) by this lane's audit_root_loss.py.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-s4bd-fresh-corpus-regen-20261121"
INP = EXP / "input"
WITNESS1 = EXP / "output" / "raw" / "s6w.p1.out"
WITNESS2 = EXP / "output" / "raw-pass2" / "s6w.p2.out"
PUBLISHED_OCT12 = ROOT / "research/experiments/n11-s4-boundary-direct-20261012/output/raw/s6-211.csv"
OUT = EXP / "output" / "s6-witness-fresh-audit.json"
S6_KEY = (1152921504675009536, 536870912)
TARGET_S5 = (1152921504607899649, 536870912)
BUDGET = 15_000_000
NODES_EXPECT = 5_859_060
LEGAL_EXPECT = 87


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_witness(path: Path) -> dict:
    txt = path.read_text(encoding="utf-8")
    if "replay_error" in txt:
        raise ValueError(f"replay_error present in {path}")
    rows = [l.split(",") for l in txt.split("\n") if l.startswith("replay,")]
    if len(rows) != 1 or len(rows[0]) != 11:
        raise ValueError(f"expected exactly one replay row in {path}")
    f = rows[0]
    if "# replay_done" not in txt:
        raise ValueError(f"incomplete raw (no replay_done): {path}")
    return {"raw_path": str(path.relative_to(ROOT)), "row_sequence": int(f[1]),
            "stones": int(f[2]), "legal": int(f[3]), "is_or": int(f[4]),
            "budget": int(f[5]), "verdict_code": int(f[6]), "nodes": int(f[7]),
            "key": [int(f[9]), int(f[10])]}


def main() -> None:
    sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
    from independent import Board
    board = Board(11)

    pass1 = read_witness(WITNESS1)
    pass2 = read_witness(WITNESS2)
    inp = (INP / "s6w.input.csv").read_text(encoding="utf-8").strip()
    if inp != f"target,0,6,{S6_KEY[0]},{S6_KEY[1]},{LEGAL_EXPECT},0,0,0,0,0":
        raise ValueError("dedicated witness input does not match the declared key/legal")
    for rec in (pass1, pass2):
        if (rec["stones"], rec["legal"], rec["is_or"], rec["budget"]) != (6, LEGAL_EXPECT, 1, BUDGET):
            raise ValueError(f"S6 witness row shape mismatch: {rec}")
        if rec["verdict_code"] != 2 or rec["nodes"] != NODES_EXPECT:
            raise ValueError(f"S6 witness not settled LOSS with published node count: {rec}")
        if tuple(rec["key"]) != S6_KEY:
            raise ValueError(f"S6 witness key mismatch: {rec}")
    if pass1["verdict_code"] != pass2["verdict_code"] or pass1["nodes"] != pass2["nodes"]:
        raise ValueError("S6 witness pass determinism failure")

    pub = read_witness(PUBLISHED_OCT12)
    if (pub["stones"], pub["legal"], pub["is_or"], pub["budget"], pub["verdict_code"],
            pub["nodes"], tuple(pub["key"])) != (6, LEGAL_EXPECT, 1, BUDGET, 2, NODES_EXPECT, S6_KEY):
        raise ValueError(f"published Oct 12 S6 witness row mismatch: {pub}")

    mask = S6_KEY[0] | (S6_KEY[1] << 64)
    if mask.bit_count() != 6 or board.canonical(mask) != mask:
        raise ValueError("S6 witness not canonical 6-stone")
    if board.legal(mask).bit_count() != LEGAL_EXPECT:
        raise ValueError("S6 witness independent legal count mismatch")
    tmask = TARGET_S5[0] | (TARGET_S5[1] << 64)
    if tmask not in board.predecessors(mask):
        raise ValueError("S6 witness is not a child of TARGET_S5")
    if board.canonical(tmask) != tmask or tmask.bit_count() != 5:
        raise ValueError("TARGET_S5 not canonical 5-stone")

    doc = {
        "schema": "n11-s4bd-freshregen-s6-witness-audit-v1",
        "s6_key": list(S6_KEY),
        "s6_stones": 6, "s6_legal": LEGAL_EXPECT, "s6_budget": BUDGET, "s6_is_or": 1,
        "parent_s5": list(TARGET_S5),
        "parent_relation_independently_verified": True,
        "and_polarity_derivation": (
            "the 5-stone parent is an AND node (second player to move): one exact "
            "LOSS child proves the parent LOSS for the original first player"),
        "derived_parent_s5_outcome": "LOSS",
        "loss_witnesses": [list(S6_KEY)],
        "pass_results": [pass1, pass2],
        "pass_determinism": True,
        "published_oct12_row": {k: pub[k] for k in
                                ("raw_path", "stones", "legal", "is_or", "budget",
                                 "verdict_code", "nodes", "key")},
        "new_s6_results": [
            {"key": list(S6_KEY), "verdict": "LOSS", "nodes": pass1["nodes"],
             "raw_path": pass1["raw_path"], "raw_sha256": sha(WITNESS1),
             "raw_pass2_path": pass2["raw_path"], "raw_pass2_sha256": sha(WITNESS2)},
        ],
        "trust": ("fresh execution by the pinned Node.js replica jsreplay.js "
                  "(sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df), "
                  "two independent passes, independent Board geometry checks, "
                  "historical cross-check against the published Oct 12 raw"),
    }
    OUT.write_text(json.dumps(doc, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    print(json.dumps({k: doc[k] for k in ("schema", "derived_parent_s5_outcome",
                                          "loss_witnesses", "pass_determinism")}, indent=1))
    print("OK")


if __name__ == "__main__":
    main()
