"""Cross-check of the C s=7 Grundy/misere tables by independent Python recursion.

The C engine dumped out/grundy_s7.bin and out/misere_s7.bin: one byte per
24-bit mask, value + 1 (0 = unsafe position).  This script

  * recomputes the full distribution directly from the table,
  * samples safe positions of every size 8..13 and recomputes their Grundy
    value and misere outcome from scratch (direct octad-intersection safety
    tests, recursive mex, no use of the C table except for the comparison),
  * checks the structurally forced values at sizes 12 and 13.
"""

from __future__ import annotations

import json
import random
import sys
from collections import Counter

from common import N, OUT_DIR, load_board, octad_masks, thru_lists

FULL = (1 << N) - 1


def main() -> int:
    _, octads = load_board()
    oct_masks = octad_masks(octads)
    thru, _pts = thru_lists(octads)
    gtab = (OUT_DIR / "grundy_s7.bin").read_bytes()
    mtab = (OUT_DIR / "misere_s7.bin").read_bytes()
    assert len(gtab) == 1 << N and len(mtab) == 1 << N
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)

    # ---- global distributions from the dumped tables ----------------------
    gcount = Counter(gtab)
    mcount = Counter(mtab)
    check(gcount.get(0, 0) == (1 << N) - 7932035,
          f"unsafe count {gcount.get(0)} != {1 << N} - 7932035")
    check(sum(v for k, v in gcount.items() if k) == 7932035, "safe count mismatch")
    check(sum(v for k, v in mcount.items() if k) == 7932035, "misere safe count mismatch")

    # per-size grundy-0 and value distribution
    size_vals = [Counter() for _ in range(N + 1)]
    nonzero_by_size = [0] * (N + 1)
    for m in range(1 << N):
        v = gtab[m]
        if v:
            k = m.bit_count()
            size_vals[k][v - 1] += 1
            nonzero_by_size[k] += 1
    gdist = Counter()
    for k in range(N + 1):
        for g, c in size_vals[k].items():
            gdist[g] += c
    check(dict(sorted(gdist.items())) == {0: 3662291, 1: 1662832, 2: 2606912},
          f"grundy distribution {dict(gdist)}")

    # structurally forced sizes
    check(nonzero_by_size[13] == 30912, f"size 13 safe {nonzero_by_size[13]}")
    check(size_vals[13].get(0, 0) == 30912, "size 13 is not all Grundy 0")
    check(size_vals[12].get(0, 0) == 1020096,
          f"size 12 Grundy-0 count {size_vals[12].get(0)} != 1020096")
    check(size_vals[12].get(1, 0) == 1393616 - 1020096,
          "size 12 non-maximal count mismatch")
    check(set(size_vals[12]) <= {0, 1}, "size 12 has Grundy > 1")

    # ---- independent recursive recomputation on samples -------------------
    rng = random.Random(20261125)
    print("collecting samples ...", flush=True)
    samples: dict[int, list[int]] = {k: [] for k in range(8, 14)}
    want = {8: 0, 9: 4, 10: 12, 11: 16, 12: 20, 13: 20}
    trials = {8: 0, 9: 20, 10: 40, 11: 60, 12: 80, 13: 4000}
    for k in range(8, 14):
        got = 0
        t = 0
        while got < want[k] and t < trials[k] * 60:
            t += 1
            pts = rng.sample(range(N), k)
            m = 0
            for p in pts:
                m |= 1 << p
            if all(((m & b).bit_count() <= 7) for b in oct_masks):
                samples[k].append(m)
                got += 1
    for k in samples:
        check(len(samples[k]) == want[k], f"only {len(samples[k])} samples of size {k}")
    print({k: len(v) for k, v in samples.items()}, flush=True)

    def safe(m):
        return all(((m & b).bit_count() <= 7) for b in oct_masks)

    def safe_add(m, p):
        # octads not through p are unchanged and m is already known safe;
        # for octads through p the intersection grows by one.
        return all(((m & oct_masks[b]).bit_count() <= 6) for b in thru[p])

    def children(m):
        out = []
        for p in range(N):
            if m & (1 << p):
                continue
            if safe_add(m, p):
                out.append(m | (1 << p))
        return out

    def grundy(m, memo):
        if m in memo:
            return memo[m]
        seen = set()
        for c in children(m):
            seen.add(grundy(c, memo))
        g = 0
        while g in seen:
            g += 1
        memo[m] = g
        return g

    def misere(m, memo):
        if m in memo:
            return memo[m]
        ch = children(m)
        if not ch:
            v = 1
        else:
            v = 1 if any(misere(c, memo) == 0 for c in ch) else 0
        memo[m] = v
        return v

    checked = 0
    for k, lst in samples.items():
        for m in lst:
            memo: dict[int, int] = {}
            g = grundy(m, memo)
            if gtab[m] != g + 1:
                failures.append(f"grundy mismatch size {k} mask {m}: py {g} c {gtab[m] - 1}")
            memo2: dict[int, int] = {}
            mv = misere(m, memo2)
            if mtab[m] != mv + 1:
                failures.append(f"misere mismatch size {k} mask {m}: py {mv} c {mtab[m] - 1}")
            checked += 1
    print(f"independently recomputed {checked} sampled positions", flush=True)

    result = {
        "safe_total": sum(v for k, v in gcount.items() if k),
        "grundy_distribution": dict(sorted(gdist.items())),
        "grundy0_by_size": {k: size_vals[k].get(0, 0) for k in range(14)},
        "samples": {k: len(v) for k, v in samples.items()},
        "samples_checked": checked,
        "checks_failed": failures,
        "PASS": not failures,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "task5_crosscheck.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps(result, indent=1))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
