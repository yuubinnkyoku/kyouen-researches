"""Is "every triple on a block" NECESSARY for the bound K <= lambda_2 + 2?

The bound was derived assuming every triple of S lies on a block.  But maybe
the bound holds even without that assumption, via a different argument.

Let me test directly: for each q, is there a safe set of size lambda_2 + 3 = q+4?
If not, the bound might hold for a different reason.

For q=3: lambda_2+3 = 7.  K=5, so no.
For q=5: 9.  K=6, so no.
For q=7: 11.  K=6, so no.
For q=9: 13.  K=9, so no.
For q=11: 15.  K=9, so no.

All far below.  So the bound is not tight and the question of necessity is
moot for these q -- the bound holds with room to spare.

The real question: is the bound VALID (not just true for small q)?  The proof
requires the property.  If the property fails for some q, the proof breaks.

Let me look for a safe set that does NOT have the property, and check whether
its size can exceed lambda_2 + 2.

Approach: for q=7, enumerate ALL safe sets of size 6 and check whether all of
them have the property.  If some size-6 safe set lacks the property, then the
property is not automatic even for maximum sets.

Actually more useful: check whether there is a safe set of size 7 for q=7
(we know K=6, so no).  And check whether all size-6 safe sets have the property.

Let me count size-6 safe sets for q=7 and check the property for each.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=7)
    ap.add_argument("--size", type=int, default=6)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    pts, blocks, through, nc, nl = build_ag(args.q)
    n = len(pts)
    n_blocks = len(blocks)
    print(f"AG(2,{args.q}): {n} points, {n_blocks} blocks", flush=True)

    # enumerate all safe sets of the given size
    safe_sets = []
    target = args.size

    def rec(start: int, chosen: list, pmask: int, cnt: list):
        if len(chosen) == target:
            safe_sets.append(list(chosen))
            return
        for p in range(start, n):
            if pmask >> p & 1:
                continue
            ok = True
            for bi in through[p]:
                if cnt[bi] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for bi in through[p]:
                cnt[bi] += 1
            chosen.append(p)
            rec(p + 1, chosen, pmask | (1 << p), cnt)
            chosen.pop()
            for bi in through[p]:
                cnt[bi] -= 1

    cnt = [0] * n_blocks
    rec(0, [], 0, cnt)
    print(f"  safe sets of size {target}: {len(safe_sets)}", flush=True)

    # check the property for each
    with_prop = 0
    without = []
    for S in safe_sets:
        Sset = set(S)
        bsets = [frozenset(b) & Sset for b in blocks]
        bsets = [b for b in bsets if len(b) >= 3]
        ok = True
        for tri in itertools.combinations(S, 3):
            t = frozenset(tri)
            if not any(t <= b for b in bsets):
                ok = False
                break
        if ok:
            with_prop += 1
        else:
            if len(without) < 3:
                without.append(S)

    print(f"  with all-triples-on-block: {with_prop}/{len(safe_sets)}", flush=True)
    if without:
        print(f"  examples WITHOUT the property: {without}", flush=True)

    out = {"q": args.q, "size": target, "total": len(safe_sets),
           "with_property": with_prop,
           "without_examples": without}
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
