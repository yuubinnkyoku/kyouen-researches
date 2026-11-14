# 2026-11-14 class2-lane cost-69b sweep (long-term lane)

## Target

S6 child `00000000000000809082000000400000` (edge cost 69, demand c1=2, c2=2) of the best
class-2 target S5 `00000000000000809082000000000000` — the cheapest unswept child in the
after-cost69a ranking (cost-69 band, second child swept in this band).

## Result

**All 69 candidates REFUTED-D10 — 0 WIN7-D10, 0 capped, 305,754,861 search nodes.
13th sterile child in the lane** (no WIN7 certificate candidates produced; the swept
child contributes no new orbit covers).

- Independent enumeration (legal_candidates.py): 69 legal candidates, matching the
  published edge cost 69.
- Pilot d6 control: loss=false at exactly 5,949 nodes in all 5 batch invocations.
- Terminal stone ranges across all candidates: [13, 17].
- Heaviest candidates: bit 68 (15,565,883 nodes), bit 119 (11,048,413), bit 41 (10,780,096);
  fresh rerun of all three node-exact (determinism).
- Bit 75 terminal range is [15, 17], all others [13, 17].

## Notes

- batchB was accidentally executed twice (a background invocation survived a failed
  wrapper command and appended after the rerun); both passes were node-exact identical —
  another cross-restart determinism confirmation. The pushed raw-batchB is the deduped copy.
- No frontier effect: sterile child (all REFUTED). Next cheapest unswept children of the
  same target per after-cost69a ranking: `00000000000000809082040000000000` (cost 69,
  c1=2,c2=1), then `000000000000008090c2000000000000` (cost 69), then cost-70 band.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}: UNKNOWN.
class 2 / class 4 blockers: UNKNOWN. (A sterile child proves nothing about the
game-theoretic value of any position; it only removes this child from the orbit-cover frontier.)
