# n11 central-reply: unconsumed-packet WIN-vs-LOSS decomposition IF-ADOPTED (2026-11-22)

Decomposition companions of the joint 25-row unconsumed-packet analysis
(Part H, `research/experiments/n11-central-reply-joint-4win-adoption-ifadopted-20261122/`)
and the packet-minus-f017 scenario
(`research/experiments/n11-central-reply-packet-minus-f017-ifadopted-20261122/`).

## What this is

The joint packet increment (4 WINs b018/d002/e002/f017 + 21 LOSS rows) is
split into disjoint what-if increments, each merged onto the canonical
5,924-row cache (sha256 `8a721a18...`) and run through the same published
refresh pipeline (published `s5_union_merge.py` selftest PASS; refresh
byte-copy with only the cache pins + the script-depth line changed; every
scenario run twice, byte-identical; root {60,27} control 119/119):

- **P4** = the 4 WIN rows only (`p4/`),
- **P17** = the 17 batch12264 LOSS rows only (f001-f016, f018; keys
  re-derived fail-closed from the pinned kit raws) (`p17/`),
- **P21** = all 21 LOSS rows only (`p21/`),

together with the already-published scenarios P24 (packet minus f017 WIN)
and P25 (full packet). `scripts/compare_decomp_deltas.py` gates the whole
decomposition and writes `output/decomp-deltas.json`.

**Read-only planning computation. No verdict is consumed. No class, root,
coverage or closure claim is made. 11x11 stays UNKNOWN.**

## Machine-verified decomposition (all deltas vs the published baseline)

| metric | base | P4 (4 WINs) | P17 (17 f-LOSS) | P21 (21 LOSS) | P24 | P25 (full) |
|---|---|---|---|---|---|---|
| excluded_now | 23 | **37** (+14) | 23 (0) | 23 (0) | 34 (+11) | 37 (+14) |
| free_now | 33 | 33 | 33 | 33 | 33 | 33 |
| unknown classes | 34,503 | 34,489 (−14) | 34,503 (0) | 34,503 (0) | 34,492 | 34,489 |
| update8 remaining | 31,838 | **31,709** (−129) | 31,821 (−17) | 31,818 (−20) | 31,743 | 31,709 |
| update8 resolved | 21 | 24 (+3) | 38 (+17) | 41 (+20) | 43 | 44 (+23) |
| win-hit groups | 0 | **15** | 0 | 0 | 9 | 15 |
| joint greedy size | 35,617 | **35,616 (−1)** | **36,989 (+1,372)** | 36,985 (+1,368) | 36,984 | 36,984 (+1,367) |
| probe worklist total | 65,213 | 65,208 (−5) | 65,192 (−21) | 65,188 (−25) | 65,184 | 65,183 (−30) |
| per-root free coverage | as published | identical | identical | identical | identical | identical |

Merged scenario caches (analysis-only, NOT canonical; own commits):
P4 5,928 rows sha256 `60c70fdf...`; P17 5,941 rows sha256 `a6201b42...`;
P21 5,945 rows sha256 `f17916ca...`.

## Findings (each machine-gated in `output/decomp-deltas.json`)

1. **The +1,367 joint plan-cost increase is entirely LOSS-row-driven and
   WIN-neutral**: adopting all four WINs moves the joint greedy size by
   **−1** (P4); the 17 batch12264 f-LOSS rows alone drive **+1,372** (P17);
   the remaining 4 non-f LOSS rows net −4 (P21 vs P17). This RETRACTS the
   Part H attribution of the cost increase to f017's adoption: f017's
   single-adoption scenario (+1,372) carries the same 17 f-LOSS rows in its
   increment, and its cost increase is those rows' effect, not the WIN's.
2. **Adopting the four WINs alone yields the full WIN-side benefit at no
   plan cost**: excluded_now +14, unknown −14, update8 remaining −129
   (b018 −29, d002 −49, e002 0, f017 −51, all additive), win-hit 15 groups
   ({16757: 5, 20421: 4, 12264: 6}), greedy −1, worklist −5, per-root free
   coverage unchanged.
3. **Class-status counts are WIN-driven only**: every LOSS-only scenario
   (P17, P21) leaves excluded/free/unknown exactly at baseline; the LOSS
   rows act purely through the scheduling option pool (update8 resolved
   +17/+20, worklist −21/−25, greedy +1,372/+1,368).
4. **Additivity**: joint = P4 + P21 exactly on 8 of 9 metrics. The single
   measured exception is update8-remaining: delta(P4)+delta(P21) = −149 vs
   joint −129; the WIN-side resolutions subsume the LOSS-side remaining
   reduction (overlap exactly 20, machine-checked).
5. **The WIN-adoption question and the plan-cost question are separable**:
   the cost increase attaches to the packet's f-LOSS completions regardless
   of whether any WIN (including f017) is adopted (P24 == P25 == 36,984).
   Any scrutiny-owner decision on the 4 WINs can be taken on the WIN-side
   numbers alone; the +1,367 is a property of adopting the batch12264
   LOSS-side knowledge, not of consuming a refutation.
6. Ranking constraint (unchanged in kind): in every packet scenario the
   closure ranking top-5 is the refuted quartet + 30345 and the first clean
   closure candidate is rank 6, class 5473 (`1158058422931816448:0`,
   unknown 51).

## Status

Verdicts NOT consumed; canonical cache unchanged at 5,924 rows; free_now 33
unchanged; scrutiny owner / C++ second-implementation gate precedent
unchanged; no closure, coverage or root claim. **The standard 11x11 empty
board, the 19 central-reply roots and all classes remain UNKNOWN; nodes and
expansions are not verdicts.**
