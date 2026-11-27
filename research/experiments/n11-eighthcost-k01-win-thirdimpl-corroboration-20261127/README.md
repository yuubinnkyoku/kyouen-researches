# n11-eighthcost-k01-win-thirdimpl-corroboration-20261127

Third-implementation corroboration pillar for the eighth-cost k01 WIN row
(key `1297036692750860288:64`, legal 84, stage-2 15M budget). Declared in
`research/log/2026-11-27-n11-eighthcost-k01-win-thirdimpl-corroboration-declaration.md`
(wave A commit 8914c50c).

## Result: CORROBORATION-PASS (verdict-level)

- third_impl.js (pinned standing implementation, sha256 08ea958f...,
  byte-clone from the Part SY kit) reported **result 1 (WIN)** for k01 in
  both fresh cold passes, expansion count 9,987,963 mutually identical
  (identical ttHits 5,498,898, quads=95670, memoPower=22, legal derived
  84 = legalIn 84, reason=clean).
- Replica (jsreplay 84585617) had reported WIN(1), nodes 8,514,427, cold
  pair node-identical (published eighth-cost kit raws).
- Verdict-level agreement: the third implementation agrees with the
  replica that k01 is WIN(1). Node and expansion counts are bookkeeping and
  are not expected to match across implementations.

## Honest disclosures

- The `rc=0` trailer line appended to each raw was emitted after an
  intervening echo, so it records the shell's rc of that echo, not directly
  of the node process; the node process rc was observed as 0 on the console
  line (`pN rc=0`) in the same command. Values are unaffected; provenance
  of the trailer is disclosed here.
- The wall_s field differs per pass (28.66 / 28.78); timing is not
  evidence.
- This is one of the two pillars required before any adoption of the k01
  WIN row. The C++ second-implementation scrutiny gate (Part SR/SW/SX
  pattern, expected k01 quadruple 84,15000000,1,8514427) remains pending.
- The verdict is NOT consumed: no cache increment, no class-status change,
  no coverage claim.

## Files

- `scripts/third_impl.js`: byte-clone of the pinned third implementation
  (sha256 08ea958f...).
- `output/raw/k01.p1.txt`, `output/raw/k01.p2.txt`: the two cold-pass raws
  (rc=0 trailer, disclosure above).
- `MANIFEST-sha256.txt`: kit manifest.

## Guards

The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. A third-implementation WIN(1) agreement is not a class closure
claim, not a root verdict, and transfers nothing.
