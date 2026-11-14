# n11 class2-lane: cost-65e — third child of the 809102 target swept, most receipt-rich sweep so far (21 WIN7-D10); bit-107 certificate fully verified; both lanes merged, frontier solved 959 → 965

Session 11 second-run continuation, after cost-63a (bit-119 receipt, solved
951 → 953 on the after-cost-61d fork). Claim pushed before any sweep compute
(commit `b35d07d7`); target S6 child `00000000000000809102000000800000`
(edge cost 65, demand c1=0,c2=2,c4=0), the cheapest remaining unswept child
of the first class-2 target S5 `00000000000000809102000000000000` after the
cost-63a receipt. The parallel session-12 lane worked the second class-2
target in the same window (cost-61e, then cost-61f: 11 WIN7-D10, 3
certificates bits 23/26/99, published after-cost-61f frontier solved 959) —
no collision.

## Sweep

- **65 candidates: 21 WIN7-D10 (bits 1, 2, 7, 26, 29, 31, 32, 33, 36, 42,
  46, 90, 94, 105, 106, 107, 111, 114, 116, 118, 120) + 44 REFUTED,
  0 capped, 308,092,253 nodes** — the most WIN7-rich child swept so far in
  the class-2 lane (21/65). 9 batches, raw JSONL pushed per batch, remote
  md5 verified per commit (records complete: commit `8e559aa6`; a md5
  transcription typo in the sweep record's certificate block was fixed and
  re-pushed transparently, commit `bdf0a20b`).
- Pilot d6 control: loss=false at exactly 5,949 nodes in all 9 batch
  invocations. Terminal stone ranges [13,17] only.
- Determinism: bits 102, 88, 120 and 107 re-solved fresh in separate
  processes: node-exact identical.
- Cross-engine: `runner_fbs20.ts` (FBS=1<<20 instrumented v15) on bits
  102/88/120: verdicts and node counts bit-exact, fbtDrops=0,
  fbtMaxProbe<=5.

## WIN7 bit-107 certificate — all verification PASS

- Root `00000800000000809102000000800000` (7 stones = child | bit 107), the
  cheapest WIN7 of the sweep (1,331,774 solve nodes).
- Extraction: blind (empty kill table), FBS=1<<20, single batch over all 44
  loser first-moves: 18,930 rows, 2,523,928 extraction nodes, fbt_drops=0,
  all 44 per-move extractions ok and uncapped; the 44 loser moves equal the
  independent legal_candidates.py enumeration (44). Rows sorted (no
  duplicates) before verification.
- Independent verifier `verify_bit7_win7_cert.ts`: root-check PASS
  (stones=7, loserMobility=44 = independent enumeration); 44/44 sub-roots
  PASS; union of consumed winner states equals the 18,930-row set exactly
  (0 missing / 0 extra); terminal ranges within [13,17].
- Pushed as a line-boundary 2-part split (9,466/9,466 lines); join md5
  `89fe2214aa925b12100d9e924752924c`, sha256
  `ac656690280ef9f2162936fcc48504902840ac1f24315aa3a9323c84a778c2e9`;
  part md5s `ce977d981e640766bd7d7b741531b7d9` /
  `016661db22bc261f8243b05a7ad57a96` (commits `9e36e267` / `9c98953a`);
  all verified by commit-SHA raw md5 after landing, join verified remotely.
- Root hex grepped against all 36 published win7-certificates manifests on
  main: 0 hits (no cross-child reuse).
- The other 20 WIN7s remain unverified search verdicts; warm
  certificate-rebuild candidates for this orbit.

## Merged frontier recompute — both lanes unified (solved 959 → 965)

The class-2 lane had forked at after-cost-61d: session 12 continued
cost-61e/61f on the second class-2 target (published after-cost-61f frontier
959 / 6,888 / 542,417 / 5,158-406,140), while this lane completed cost-63a
and cost-65e on the first target. `recompute_frontier_merged_after61f_63a65e_
20261114.py` reconciles the branches: it reproduces the published
after-cost-61f frontier via runpy of the published
`recompute_frontier_cost61f_20261114.py` with every staged control asserted,
then asserts the completed 63a/65e sweep records, claims and receipts and
adds both receipts. Cross-branch coverage is recomputed, not assumed:

- cost-63a bit-119 on the after-61f base: covers 7 / marginal 6 /
  in-manifest 2 (unchanged from the after-61d fork — no 61f overlap).
- cost-65e bit-107 on the merged base: covers 7 / marginal 7 /
  in-manifest 4 (child orbit + 3 cross-target).
- 63a/65e children remaining-membership in the fork baseline: True/True
  (recorded as controls); 65e child demand c1=0,c2=2,c4=0 re-derived.
- **Merged: solved 965 / unique remaining 6,882 / sum 542,020 /
  open 5,152-405,743** — fully additive (959 + 2 + 4), no double coverage
  between the branches.
- First class-2 target: 38 → 35 orbits (2,721 → 2,525); three receipts so
  far (62a bit-11, 63a bit-119, 65e bit-107). Its next cheapest unswept
  child is cost-65 `00000000000000809102000080000000` (c1=0,c2=2,c4=0).
- Byte-identical determinism rerun (script + JSON + both CSVs); pushed in
  commit `09e26e62`, commit-SHA raw md5 verified for all four files.
- Concurrent lane note: cost-63e (second target, 63 candidates) raw batches
  were complete on main at merge time but its records/receipts were not yet
  published; it is excluded here and folds into the next recompute.

11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2 and class 4
remain UNKNOWN; WIN7 certificates prove only individual 7-stone roots within
depth 10; REFUTED-D10 sweeps prove only the absence of such receipts.
