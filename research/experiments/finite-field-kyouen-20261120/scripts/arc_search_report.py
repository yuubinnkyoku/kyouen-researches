"""Drive arc_maxsearch.exe and verify every witness independently.

The C search only reports a candidate arc; this script re-checks it from
scratch against the circle list (so a bug in the incremental blocking logic
cannot produce a false claim), and records the result as JSON.

Verification of a witness arc A (a list of point indices):
    for every circle c:  |A & c| <= 3
Because two distinct circles of an inversive plane meet in at most two points,
"no circle carries four points of A" is exactly "A is safe".

Run
---
    python arc_search_report.py --q 5 7 8 9 11 13 17 19 23 25 27 29 31 32 \
        --trials 200 --ils 500 --seeds 3 --out ../output/arc_maxsearch.json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"
EXE = HERE / "arc_maxsearch.exe"

BEST_RE = re.compile(r"^BEST\s+(\d+)((?:\s+\d+)*)\s*$")


def read_circles(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        n, b = (int(x) for x in fh.readline().split())
        circles = []
        for _ in range(b):
            parts = fh.readline().split()
            k = int(parts[0])
            circles.append(tuple(int(x) for x in parts[1:1 + k]))
    assert len(circles) == b
    return n, circles


def verify_arc(n: int, circles, arc) -> tuple[bool, str]:
    if len(set(arc)) != len(arc):
        return False, "repeated point"
    if any(not (0 <= p < n) for p in arc):
        return False, "point index out of range"
    aset = set(arc)
    for c in circles:
        if len(aset.intersection(c)) >= 4:
            return False, f"circle carries {len(aset.intersection(c))} arc points: {sorted(aset.intersection(c))}"
    return True, "ok"


def run_one(q: int, trials: int, ils: int, seed: int) -> dict:
    path = OUT / f"circles_q{q}.txt"
    if not path.exists():
        return {"q": q, "error": f"missing {path.name}"}
    proc = subprocess.run(
        [str(EXE), str(path), "--trials", str(trials), "--ils", str(ils),
         "--seed", str(seed)],
        capture_output=True, text=True, timeout=3600)
    if proc.returncode != 0:
        return {"q": q, "error": f"exit {proc.returncode}: {proc.stderr[:200]}"}
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    header = lines[0]
    m = BEST_RE.match(lines[1])
    if not m:
        return {"q": q, "error": f"unparsable output: {lines[1][:120]}"}
    size = int(m.group(1))
    arc = [int(x) for x in m.group(2).split()] if m.group(2).strip() else []
    n, circles = read_circles(path)
    ok, why = verify_arc(n, circles, arc)
    return {"q": q, "size": size, "verified": ok, "why": why,
            "arc": arc, "header": header, "seed": seed}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--trials", type=int, default=100)
    ap.add_argument("--ils", type=int, default=400)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        best = None
        for s in range(1, args.seeds + 1):
            r = run_one(q, args.trials, args.ils, s * 7919)
            if "error" in r:
                print(f"q={q} seed={s}: ERROR {r['error']}", flush=True)
                rows.append(r)
                break
            if not r["verified"]:
                print(f"q={q} seed={s}: WITNESS REJECTED ({r['why']})", flush=True)
                rows.append({**r, "error": "witness failed verification"})
                break
            if best is None or r["size"] > best["size"]:
                best = r
            print(f"q={q} seed={s}: size={r['size']} verified", flush=True)
        if best is not None:
            rows.append(best)
            print(f"  -> q={q} best={best['size']} witness={best['arc']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
