# 2026-11-17 n11 class2-lane: cost72d sweep and certificates complete — 11 WIN7-D10 roots extracted, independently verified and published

## Summary

The cost72d lane (census v5 runner-up row, the cheapest remaining unswept/
unclaimed row of the primary class-2 target family after the completed cost71e
sweep and certificate publication) ran its fresh 72-bit v17 depth-10 sweep and
then the blind certificate extraction of every WIN7-D10 root:

* sweep: 11 WIN7-D10 bits [1, 6, 24, 25, 43, 49, 75, 80, 83, 98, 114] +
  61 REFUTED-D10, 0 capped; 133,761,580 candidate nodes plus 9 pilot
  controls at exactly 3,402 nodes each (9/9 exact)
* controls: the 5 census-v5 confirmation bits [5, 20, 103, 108, 115] were
  re-run fresh and all came out REFUTED-D10 as predicted (bit 5 = cost69j
  bit 14, bit 20 = cost64h bit 14, bit 103 = cost66i bit 34, bit 108 =
  cost66j bit 86, bit 115 = pre-64h harvest); determinism reruns of batches 1
  (WIN bits 1, 6) and 3 (heaviest bit 41, 4,501,083 nodes) were
  field-identical on every non-ms field; the independent v15 runner re-checked
  all 11 WIN bits with 11/11 agreement (pilot 5,949 exact, 0 capped); the
  stdlib raw audit recomputed legal_candidates and all cross-source checks
  and passed everything
* extraction: blind extraction with `class4_child1_cert_extractor_exact.ts`
  (repo-verbatim, engine v15 inlined, FBS=1<<20) via `cert_driver72d.ts`
  (71e driver duplicated, empty kill table), fbt_drops=0 on all eleven, no
  fatal, no capped per-move
* total certificate rows 522,517; total extraction nodes 120,204,754;
  published bytes 18,850,168 (bit 75 whole file; the other ten split
  part1of2/part2of2 at line boundaries with a README-split per bit)
* independent verification with `verify_bit7_win7_cert.ts` (engine-free,
  Bareiss 4x4), orchestrated per root by `verify_cost72d_one.sh`:
  root-check stones=7 on every root, loser mobility equals the independent
  legal_candidates.py enumeration on the RAW root (bit1:55, bit6:54,
  bit24:57, bit25:54, bit43:58, bit49:59, bit75:50, bit80:53, bit83:57,
  bit98:55, bit114:61), all sub-roots PASS (subroots_pass == loser mobility
  on every root), terminal stone range [13,17] everywhere,
  consumed-winner-state union vs the certificate row set 0 missing / 0 extra
  in both directions on every root (re-checked locally at publication time
  from the archived certkeys/consumed files)
* determinism: fresh-process re-extraction byte-identical (md5
  `bdd29dc364f975050280f45a5c1428bc`) on bit 1
* all 21 certificate files (1 whole + 20 parts) landed byte-exact on the
  raw CDN at commit pins `a03dfac2`..`3e6709fc`; every split recombination
  was re-checked with cat + md5sum against the manifest md5s at the final
  pin

Coordinate convention carried over from the 66i/71e lessons: loser defenses
and the certificate root use the RAW child|bit position. For bits
1/6/24/25/43/49 raw==canon; for bits 75/80/83/98/114 the raw root is a
non-canonical D4 image (d4_canon_root recorded per manifest entry) and the
defense list is enumerated on the raw root; the verifier's root-header check
guards this.

## Interpretation guard

WIN7-D10 certificates prove a first-player win within depth 10 from the
individual 7-stone roots of this child only. REFUTED-D10 is not a LOSS
proof. No manifest row of the head-1472 family is closed by this
publication. The receipt fold of this row waits behind the pending cost-76c,
cost-66i, cost-66j, cost-69j and cost-71e folds (managed by their own lanes).

**The 11x11 empty board remains UNKNOWN. The two-stone roots {49,60}
and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.**

## Files pushed

* raw sweep: `output/class2-lane-cost72d-raw-batch{1..8}-20261117.jsonl`,
  `output/class2-lane-cost72d-raw-batch9-confirmation-20261117.jsonl`
  (commits `a8ff1d81`, `18057d7b`), controls
  `output/class2-lane-cost72d-det-batch{1,3}-20261117.jsonl`,
  `output/class2-lane-cost72d-v15-crosscheck-{a,b}-20261117.jsonl`, the
  stdlib audit `output/class2-lane-cost72d-raw-sweep-audit-20261117.json`
  and `scripts/audit_cost72d_raw_batches_20261117.py` (commit `99f93ea8`)
* certificates (commits `a03dfac2`..`3e6709fc`, 21 files):
  `output/class2-lane-cost72d-certificates/n11_s7_*.cert.part1of2/
  part2of2` for bits 1/6/24/25/43/49/80/83/98/114 and
  `n11_s7_00000000000008403800000008004000.cert` whole for bit 75
* this commit: `output/class2-lane-cost72d-certificates/README-split-bit{b}.md`
  (ten split recombination notes),
  `bit{b}-rootcheck.json` and `bit{b}-subroots.jsonl` (per-bit verification
  records, 11 bits), the certificate manifest
  `output/class2-lane-cost72d-certificates/class2-lane-cost72d-win7-certificates-20261117.json`,
  the claim v2 `output/class2-lane-cost72d-inflight-20261117.json`
  (updater asserts the v1 git blob
  `b4454257b73a471417bcad0dd3172fd035e493b8`), archived lane tooling
  `scripts/update_claim72d_v2_20261117.py`, `scripts/cert_driver72d.ts`,
  `scripts/verify_cost72d_one.sh`, `scripts/ev72d.sh`, and this log

## Next

The receipt fold of this row stays pending behind the 76c/66i/66j/69j/71e
folds. Next fresh targets for this lane: the census v5 top-10 cost-73 rows
`00000000000000403800400008000000` (open 68) and
`00000000000000403800000408000000` (open 69).
