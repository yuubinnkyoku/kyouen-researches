# 2026-11-14 class4-lane cost-80 sweep: 7th sterile child (80/80 REFUTED-D10)

## Context

Resume of the class-4 lane after cost-79b (6th sterile child, pushed by the parallel
lane). Latest main HEAD at session start: d9436902. The after-cost78b ranking
(`class-frontier-top-candidates-s6-after-cost78b.csv`, best class-4 blocker-candidate
S5 `00000000020000003800000080000000`, remaining 19 orbit / cost 1540) lists the three
cheapest unswept S6 children in the cost-80 band:

1. `00000000020000003800000180000000` (cost 80, c1=0,c2=0,c4=2)  <- this session
2. `00000000020000003800040080000000` (cost 80, c1=0,c2=0,c4=3)
3. `00000000020000003800200080000000` (cost 80, c1=0,c2=0,c4=1)

## Sweep (child 1: `00000000020000003800000180000000`)

Protocol identical to cost-74a/b/75/78/78b/79/79b: `scripts/class4_child1_runner.ts`
(v15 engine verbatim) via native Node v22, per-candidate freshEngine, close-first AND
at depth>=8, cap 1e9 (effectively uncapped), depth 10 single-run, foreground batches
20+20+20+20 with per-batch JSONL durability pushes.

- Candidate enumeration: `legal_candidates.py` (post-bugfix version) independently
  derives 80 legal non-degenerate 7th-stone candidates; matches the published edge
  cost 80 exactly.
- **Result: all 80 candidates REFUTED-D10. 0 WIN7, 0 capped, 290,092,122 nodes
  total, terminal stone range [13,17] global.**
- Controls:
  - pilot d6: 5/5 batch invocations loss=false at exactly 5,949 nodes.
  - determinism: heaviest candidates bits 93/11/66 (12,288,748 / 11,374,987 /
    10,447,800 nodes) re-run fresh in a separate process: node-exact identical.
  - extra determinism evidence: batch 1 (bits 0..26) was unintentionally executed
    twice (a stray parallel invocation that was believed to have failed); all 20
    per-bit node counts were identical across both runs, and the deduplicated
    record uses each bit once.

Record: `output/class4-lane-cost80-sweep-20261114.json` (md5 410574f96eca33f7cd98a52099f1bc80),
raw batches `output/class4-lane-cost80-raw-batch{1..5}-20261114.jsonl` (16 bits each).

## Interpretation

This is the **7th sterile child** of the class-4 lane: no depth<=10 WIN7 exists from
any 7-stone root in this child, so its c4 demand cannot be closed by batch3-style
certificates from within the child; it must be covered through other S6 parents of the
same orbit. Frontier bookkeeping is unchanged (sterile children contribute no receipts).

Cost-80 band: child 1 done (sterile); children 2 and 3 remain.

## Guard

REFUTED-D10 is only the negation of a winner win within depth 10 from the 7-stone
root (loser to move). It is NOT a statement about deeper play, the S5/S6 orbits, the
two-stone root {49,60}, S2 {59,60}, or the 11x11 empty board.
**11x11 remains UNKNOWN.**
