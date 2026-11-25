# n11 class2-lane: cost-63a — second child of the 809102 target swept; 10 WIN7-D10, bit-119 certificate fully verified; frontier solved 951 → 953

Session 11 second-run continuation. Claim pushed before any compute (commit
`230dabfb`); target S6 child `00000000000000809102000800000000` (edge cost 63,
demand c1=0,c2=2,c4=0), the cheapest remaining unswept child of the class-2
target S5 `00000000000000809102000000000000` after the cost-62a receipt
(38 orbits / 2,721). Sweeping a second child of the same S5 advances the
receipt framework on that target while the parallel session-12 lane works the
second class-2 target S5 `803202...` (cost-56a/58b/60b/61d) — no collision.
The parallel audit lane independently audited raw batch 1 in flight
(`class2-lane-cost63a-batch1-independent-audit-20261114.json`: exact 63-bit
candidate set via BigInt Laplace expansion, exact_set_match=true; bit2 WIN7
root independently confirmed).

## Sweep

- **63 candidates: 10 WIN7-D10 (bits 2, 11, 15, 28, 96, 97, 100, 109, 118,
  119) + 53 REFUTED, 0 capped, 288,069,056 nodes.** 8 batches (8x7 then 7),
  raw JSONL pushed per batch (`class2-lane-cost63a-raw-batch1..8`).
- Pilot d6 control: loss=false at exactly 5,949 nodes in all 8 batch
  invocations. Terminal stone ranges [13,17] only.
- Determinism: heaviest bit 32 (13,242,071) and WIN7s 2 (12,280,257),
  119 (3,074,897), 11 (5,671,351) re-solved fresh in separate processes:
  node-exact identical.
- Cross-engine: `runner_fbs20.ts` (FBS=1<<20 instrumented engine) on bits
  32/2/119: verdicts and node counts bit-exact, fbtDrops=0,
  fbtMaxProbe<=3.
- **Env-reset cross-restart control**: the execution environment reset
  mid-sweep and the local raw JSONL for batches 1-5 was lost; every affected
  batch was re-run deterministically from scratch and reproduced its
  pre-reset node counts exactly (batches 1-3 re-pushed byte-identical,
  commit `4c0b2c8d`; batches 4-8 pushed from the post-reset reruns, commit
  `31a4c24b`). Recorded as a cross-restart reproduction control.

## WIN7 bit-119 certificate — all verification PASS

- Root `00800000000000809102000800000000` (7 stones = child | bit 119), the
  cheapest WIN7 of the sweep (3,074,897 solve nodes).
- Extraction: `cert_driver68.ts` over the repo-verbatim
  `class4_child1_cert_extractor_exact.ts`, blind (empty kill table),
  FBS=1<<20, single batch over all 49 loser first-moves: 28,509 rows,
  5,731,248 extraction nodes, fbt_drops=0, fatal=null, all 49 per-move
  extractions ok and uncapped. Rows sorted (no duplicates) before
  verification.
- Independent verifier `verify_bit7_win7_cert.ts`: root-check PASS
  (stones=7, loserMobility=49 = independent legal_candidates.py
  enumeration); 49/49 sub-roots PASS; union of consumed winner states equals
  the 28,509-row set exactly (0 missing / 0 extra); terminal ranges within
  [13,17].
- Pushed as a line-boundary 2-part split (14,256/14,255 lines); join md5
  `c042fbf46be29ecc0ac74ceb25324b16`, sha256
  `3c7e7133d0176e073bfafaebb7b037b06236e76158d92f85f9c0408ba3997d6b`;
  part md5s `c920f058977d3773d2b7ec098a77b622` /
  `580ac8e73099b0828353571062114d96`; all verified by commit-SHA raw md5
  after landing.
- Root hex grepped against all 33 published win7-certificates manifests on
  main: 0 hits (no cross-child reuse).
- The other 9 WIN7s (bits 2,11,15,28,96,97,100,109,118) remain unverified
  search verdicts; any one can be certified later if a second receipt for
  this orbit is ever wanted.

## Frontier after cost-63a (solved 951 → 953)

`recompute_frontier_cost63a_20261114.py` (runpy extension of the published
`recompute_frontier_cost61d_20261114.py`) reproduces every staged control
through after-cost-61d (951/6,896/542,952/5,166/406,675 asserted; local
rerun reproduces the published 60b/61d JSONs and CSVs byte-identically),
asserts the completed 63a sweep + completed claim + child demand + the
bit-119 receipt (rows/sub-roots/union), and adds the receipt:
covers 7, marginal 6, marginal-in-manifest 2 (the child orbit itself plus
cross-target `00000000000080809002000000000200`).

**After cost-63a: solved 953 / unique remaining 6,894 / sum 542,827 /
open 5,164-406,550.** The 809102 class-2 target drops 38 → 37 orbits
(2,721 → 2,658); its next cheapest unswept children are two cost-65
children. The 63a receipt is the second for this S5 (62a bit-11, 63a
bit-119). Byte-identical determinism rerun.

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4
remain UNKNOWN; WIN7 certificates prove only individual 7-stone roots.
