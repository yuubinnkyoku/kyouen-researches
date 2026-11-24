"""Merge per-task result files into spectrum_results.json and verify witnesses.

* deduplicates by (q, s), preferring the entry that carries a witness;
* writes output/spectrum_results.json sorted by (q, s);
* verifies every referenced witness directly against the board (no SAT);
* records the dual blocking quantity tau_d = q^2+1-K_s with d = q+1-s.

Usage:
    python merge_results.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def verify(q: int, s: int, points: list[int]) -> bool:
    board = json.loads((OUT / f"board_q{q}.json").read_text(encoding="utf-8"))
    S = set(points)
    return all(len(S.intersection(C)) <= s for C in board["blocks"])


def main() -> None:
    entries: dict[tuple[int, int], dict] = {}
    for path in OUT.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        for r in data.get("results", []):
            key = (r["q"], r["s"])
            old = entries.get(key)
            if old is None or ("witness" in r and "witness" not in old):
                entries[key] = r

    merged = []
    for key in sorted(entries):
        r = entries[key]
        if "witness" in r:
            w = json.loads((EXP.parents[2] / r["witness"]).read_text(encoding="utf-8"))
            ok = verify(r["q"], r["s"], w["points"]) and len(w["points"]) == r["exact"]
            r["witness_verified"] = ok
            assert ok, r
        q, s = r["q"], r["s"]
        if 1 <= s <= q:
            d = q + 1 - s
            r["dual_d"] = d
            r["tau_d"] = q * q + 1 - r["exact"]
            r["tau_linear_bound"] = d * (q + 1)
            assert r["tau_d"] >= r["tau_linear_bound"], r
        merged.append(r)
    out = {"experiment": "inversive-spectrum-20261124",
           "definition": "K_s(q) = max |S| with |S ∩ C| <= s for every circle C",
           "theorem": "K_s(q) <= (s-2)(q+1)+2 for 2 <= s <= q+1",
           "results": merged}
    (OUT / "spectrum_results.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(merged, indent=1))
    for path in OUT.glob("task_*.json"):
        path.unlink()
    for path in OUT.glob("ad_hoc.json"):
        path.unlink()


if __name__ == "__main__":
    main()
