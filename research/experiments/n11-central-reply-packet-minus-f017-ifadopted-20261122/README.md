# n11 central-reply: packet-minus-f017 P24 IF-ADOPTED scenario (2026-11-22)

Companion scenario of the joint 4-WIN packet analysis (Part H,
`research/experiments/n11-central-reply-joint-4win-adoption-ifadopted-20261122/`).

## What this is

The 25-row unconsumed-packet increment (4 WINs + 21 LOSS rows) **minus the
single f017 WIN row**: a 24-row increment (3 WINs b018/d002/e002 + 21 LOSS
rows), i.e. the what-if "adopt the whole packet except f017". f017's key is
re-derived fail-closed from the pinned kit raw (`scripts/make_p24_increment.py`).
Read-only planning computation. **No verdict is consumed; the canonical merged
chain cache stays at 5,924 rows (sha256 `8a721a18...`); the standard 11x11
empty board, the 19 central-reply roots and all classes remain UNKNOWN.**

- merge: published `s5_union_merge.py` (selftest PASS) -> 5,948 rows,
  WIN 161 / LOSS 5,787, 0 conflicts, sha256
  `ee4618dec59dfe88e01f01246d28339fd400b4c8aa17a97d342f963f2440a256`
  (published as its own single-file commit; analysis-only, NOT canonical)
- refresh: byte-copy of the published refresh script with only the 2 cache
  pins changed; run twice, byte-identical; root {60,27} control 119/119.

## Results (machine-verified, deltas vs the published baseline re-audit)

| metric | base | P24 | P25 (full packet) |
|---|---|---|---|
| excluded_now | 23 | **34** (+11) | 37 (+14) |
| free_now | 33 | 33 | 33 |
| unknown classes | 34,503 | 34,492 (−11) | 34,489 (−14) |
| update8 remaining | 31,838 | 31,743 (−95) | 31,709 (−129) |
| update8 resolved | 21 | 43 (+22) | 44 (+23) |
| win-hit groups | 0 | 9 (16757: 5, 20421: 4; no 12264) | 15 |
| joint greedy size | 35,617 | **36,984 (+1,367)** | 36,984 (+1,367) |
| probe worklist total | 65,213 | 65,184 (−29) | 65,183 (−30) |
| per-root free coverage | as published | identical to baseline | identical to baseline |

Headline findings:

1. **Dropping f017 does NOT avoid the plan-cost increase**: P24's joint
   greedy is 36,984, identical to the full-packet P25. This was the
   motivating question of the scenario, and the answer falsifies the
   Part H mechanism attribution (see the erratum in the joint experiment's
   README: the +1,367 is driven by the packet's LOSS-side rows, not by
   f017, and is fully decomposed in
   `research/experiments/n11-central-reply-packet-win-vs-loss-decomposition-ifadopted-20261122/`).
2. Under P24 the win-hit set loses exactly class 12264's 6 groups
   (f017's WIN not adopted), keeping b018/d002's 9 groups.
3. Under P24 the closure ranking top is 16757/12264/20421/16371/30345
   (12264 at rank 2 with unknown 34, its f-rows probed but its WIN not
   adopted), so as in P25 **the first clean closure candidate is rank 6,
   class 5473** (`1158058422931816448:0`, unknown 51).

Not republished (transport): `output/probe-worklist.csv` (~3.7MB) regenerates
deterministically from the pinned inputs; its total is in
`output/refresh-summary.json`.

## Status

Verdicts NOT consumed; scrutiny owner / C++ second-implementation gate
precedent unchanged; free_now 33 unchanged; no closure, coverage or root
claim is made. 11x11, the 19 central-reply roots and all classes remain
UNKNOWN.
