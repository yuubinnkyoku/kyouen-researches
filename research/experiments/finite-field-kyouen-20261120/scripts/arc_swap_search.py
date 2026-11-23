"""Drive arc_swapsearch.exe: try to beat each known arc size, and verify hits.

arc_maxsearch.c grows a set greedily and is stuck at the values recorded in
K1251.  arc_swapsearch.c works at a *fixed* size and minimises the number of
circles carrying four or more of the set, so it explores a different basin.
For each q we ask it for a set of size (current best) and of size (best + 1):

  * finding the current best again validates the tool,
  * failing at best+1 is evidence that the recorded value is not a search
    artefact.

Every reported set is re-verified against the circle list from scratch.

Run:  python arc_swap_search.py --q 13 17 19 23 29 31 --iters 300000 --sample 24
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"
EXE = HERE / "arc_swapsearch.exe"

KNOWN = {5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 10, 16: 12, 17: 13, 19: 14,
         23: 16, 25: 18, 27: 19, 29: 20, 31: 21, 32: 22, 37: 25, 41: 27,
         43: 28, 47: 30, 49: 32}

WITNESS_FILES = ["arc_maxsearch.json", "arc_maxsearch_long.json",
                 "arc_maxsearch_big.json", "arc_maxsearch_q49.json",
                 "arc_maxsearch_q49b.json", "arc_maxsearch_push.json"]


def load_witness(q: int):
    """Largest arc recorded for q by the greedy search (K1251's tables)."""
    best = None
    for name in WITNESS_FILES:
        p = OUT / name
        if not p.exists():
            continue
        for rec in json.loads(p.read_text(encoding="utf-8")):
            if rec.get("q") == q and "arc" in rec and rec.get("verified", True):
                if best is None or len(rec["arc"]) > len(best):
                    best = rec["arc"]
    return best


def read_circles(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        n, b = (int(x) for x in fh.readline().split())
        circles = []
        for _ in range(b):
            parts = fh.readline().split()
            k = int(parts[0])
            circles.append(tuple(int(x) for x in parts[1:1 + k]))
    return n, circles


def verify(circles, arc) -> tuple[bool, str]:
    if len(set(arc)) != len(arc):
        return False, "repeated point"
    aset = set(arc)
    for c in circles:
        hit = len(aset.intersection(c))
        if hit >= 4:
            return False, f"{hit} points on one circle"
    return True, "ok"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--iters", type=int, default=300000)
    ap.add_argument("--sample", type=int, default=24)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        path = OUT / f"circles_q{q}.txt"
        if not path.exists():
            print(f"skip q={q}: missing {path.name}", flush=True)
            continue
        n, circles = read_circles(path)
        base = KNOWN.get(q)
        targets = [base, base + 1] if base else [8, 9, 10]
        rec = {"q": q, "n": n, "results": []}
        witness = load_witness(q)
        for k in targets:
            if k is None or k > n:
                continue
            cmd = [str(EXE), str(path), "--k", str(k),
                   "--iters", str(args.iters), "--sample", str(args.sample)]
            if witness and k == base + 1 and len(witness) == base:
                # start the growth attempt from the known best arc
                cmd += ["--init", ",".join(str(x) for x in witness)]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
            out = proc.stdout.strip().splitlines()
            last = out[-1] if out else ""
            found = proc.returncode == 0
            item = {"k": k, "found": found, "raw": last}
            if found:
                for line in out:
                    if line.startswith("FOUND"):
                        arc = [int(x) for x in line.split()[2:]]
                        ok, why = verify(circles, arc)
                        item.update({"verified": ok, "why": why, "arc": arc})
                        break
                else:
                    item.update({"verified": False, "why": "no witness line"})
            rec["results"].append(item)
            print(f"q={q:>2} k={k:>2}: {'FOUND' if found else 'not found'} "
                  f"{'' if not found else 'verified=' + str(item.get('verified'))}", flush=True)
        rows.append(rec)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        print(f"wrote {args.out}")
    if any(r.get("verified") is False for rec in rows for r in rec["results"]):
        raise SystemExit("a reported arc FAILED verification")


if __name__ == "__main__":
    main()
