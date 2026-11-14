# n11 class2-lane: cost-62a — first sweep of the next class-2 target after the uncoverability audit; 11 WIN7-D10, bit-11 certificate fully verified; frontier solved 921 → 924

Session 11 continuation. Starting point: the after-cost-73a frontier (solved 921 /
remaining 6,926 / sum 544,995 / open 5,196/408,718) and the uncoverability audit
pushed earlier this session (best class-2 S5 `00000000000000809082000000000000`
receipt-unclosable — all 10 remaining children sterile-swept). The cheapest
unswept child of the next class-2 target S5 `00000000000000809102000000000000`
(40 orbits / 2,850, 0 sterile) is its cost-62 child
`00000000000000809102000001000000`. Claim pushed before any compute
(commit `caddef1d`); the parallel audit lane independently reconciled the early
batches while the sweep was in flight
(`2026-11-14-n11-class2-cost62a-partial-raw-audit.md`: batches 1-4 = 108,012,447
nodes, 32 distinct bits, 4 pilots at 5,949 nodes, and D4-canonical distinctness +
non-degeneracy of all 62 candidate roots).

## Sweep

- **62 candidates: 11 WIN7-D10 (bits 1, 11, 32, 66, 86, 89, 95, 105, 109, 112,
  118) + 51 REFUTED, 0 capped, 245,781,099 nodes.** 8 batches (8x8 candidates),
  raw JSONL pushed per batch as completed (`class2-lane-cost62a-raw-batch1..8`).
- Pilot d6 control: loss=false at exactly 5,949 nodes in all 8 batch invocations.
- Candidate enumeration: legal_candidates.py independent Bareiss 4x4, 62 legal =
  published edge cost 62, bit-exact.
- Terminal stone ranges [13,15] and [13,17] only.
- Determinism: heaviest bit 114 (14,917,704) and WIN7s 86 (13,028,038),
  1 (11,849,776), 11 (2,557,437) re-solved fresh in separate processes:
  node-exact identical.
- Cross-engine: `runner_fbs20.ts` (FBS=1<<20 instrumented engine) on bits
  114/86/11: verdicts and node counts bit-exact, fbtDrops=0, fbtMaxProbe<=3.

This child is unusually receipt-rich (11/62 WIN7 vs 1/73 for cost-73a); the
extra WIN7s lower the risk that this S6 orbit ever becomes uncoverable.

## WIN7 bit-11 certificate — all verification PASS

- Root `00000000000000809102000001000800` (7 stones = child | bit 11), the
  cheapest WIN7 of the sweep (2,557,437 solve nodes).
- Extraction: `cert_driver68.ts` over the repo-verbatim
  `class4_child1_cert_extractor_exact.ts`, blind (empty kill table), FBS=1<<20,
  single batch over all 47 loser first-moves: 24,728 rows, 5,152,966 extraction
  nodes, fbt_drops=0, fatal=null, all 47 per-move extractions ok and uncapped.
  Rows sorted (no duplicates) before verification per the established note.
- Independent verifier `verify_bit7_win7_cert.ts`: root-check PASS (stones=7,
  loserMobility=47 = independent legal_candidates.py enumeration); 47/47
  sub-roots PASS; union of consumed winner states equals the 24,728-row set
  exactly (0 missing / 0 extra); terminal ranges within [13,17].
- Pushed as a line-boundary 2-part split (12,365/12,365 lines) + README; join md5
  `173c3987a63035f2a1722887314af11a`, sha256
  `45ec61197dd6f449f186f74c21f73a05adb9e4273f91af559a52135ca85f87e5`; part md5s
  `2a20b64fe74e5c1220dc3eb24875614a` / `eb4f17da6011a2e18fd468a810ddcaea`.
- All 11 WIN7 root hexes grepped against the published win7-certificates
  records (locally mirrored main): 0 hits.
- The other 10 WIN7s (bits 1,32,66,86,89,95,105,109,112,118) remain unverified
  search verdicts; any one can be certified later if a second receipt for this
  orbit is ever wanted.

## Frontier after cost-62a (solved 921 → 924)

`recompute_frontier_cost62a_20261114.py` reproduces every staged control through
after-cost-73a (921/6,926/544,995/5,196/408,718 asserted), asserts the completed
62a sweep record, asserts the newly completed sterile class4-lane cost-86a/86b/86c
sweeps receipt-free, adds the bit-11 receipt, and re-asserts the uncoverability
audit conclusion (best class-2 S5 still 10 remaining, all sterile-swept).

- Receipt: covers 7 S6 orbits, all 7 marginal; **3 in the manifest** — the child
  itself, a second child of the same S5 (`00000000000000809102000000000800`,
  the parent | bit 11), and `00000000000000801202000040200000`.
- **solved 924 / unique remaining 6,923 / sum 544,799 / open 5,193/408,522.**
- Next class-2 target `00000000000000809102000000000000`: 40 → **38 orbits**
  (2,850 → 2,721) — the receipt covered two of its children at once.
- Best class-4 unchanged (18/1,460: 12 sterile-swept + 6 unswept; the class4-lane
  parallel is mid-flight on cost-86d).
- Determinism: two consecutive runs byte-identical
  (`class-frontier-cost62a-recompute-20261114.json`).

## Operational finding: 64KB read paging truncates large pushes

The first certificate-part push landed truncated (1,768/1,769 lines instead of
12,365 each): `file_system.read_file` pages at ~64KB per call and a naive single
read silently returns only the first page. The parts were re-pushed with paged
full reads (loop over `next_offset` until `was_truncated` is false) and the
remote md5s now equal the local files exactly. Any future push of a file larger
than ~64KB must page the reads and verify by commit-SHA raw md5. This matches the
six-row lane's earlier "truncated by 64KB paging cap" observation and generalizes
it to the read side of the class2-lane tooling.

## Status

- 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  **UNKNOWN.** All WIN7 certificates prove only individual 7-stone roots;
  REFUTED-D10 sweeps prove only absence of a depth-10 winner win in that subtree.

## Artifacts

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost62a_20261114.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost62a-sweep-20261114.json`
- `.../class2-lane-cost62a-win7-certificates-20261114.json`
- `.../class2-lane-cost62a-certificates/` (bit11 root parts + README)
- `.../class-frontier-cost62a-recompute-20261114.json` (+ ranking/top-candidates CSVs)
- `.../class2-lane-cost62a-raw-batch1..8-20261114.jsonl`, determinism rerun, fbs20 crosscheck
