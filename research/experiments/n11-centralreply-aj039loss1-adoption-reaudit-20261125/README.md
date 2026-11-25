# n11-centralreply-aj039loss1-adoption-reaudit-20261125 (Part EL)

Loss-only canonical adoption of the single fresh exact-LOSS row **aj039**
(key (1152922606282735616, 65536), legal 88, s5_index 897668), probed by the
published Part EK 30M re-probe kit (two-pass fresh-cold node-exact, budget
30,000,000 order 0, nodes 16,549,916 per pass, MISMATCH 0, resolved in
(15M, 30M] beyond the honest EXHAUSTED 15M history of batch-39 - not a
same-condition re-probe).  Declaration:
`research/log/2026-11-25-part-el-aj039loss1-adoption-declaration.md`.

- BASE: the published Part EI canonical merged cache
  `merged-exact-s5-chain-plus-b39loss46-20261125.cache` (6,712 rows, WIN 158
  / LOSS 6,554, sha256 73482be0...).
- Pool source: the published Part EK kit
  `research/experiments/n11-centralreply-closure-class30484-aj030aj039-reprobe30m-20261125/`
  (MANIFEST-sha256 rev2 97574401..., 42 files, audit_ek.json d9aa8aab...,
  79/79 gates PASS).
- NOT consumed: aj030 (probe-level WIN 15,284,699 at 30M, WIN-HALT,
  scrutiny-owner C++ second-implementation gate 9193f5b6... exclusive, sits in
  NO cache); ai044/ai048 (Part EF claim-reserved, untouched); aj049/aj050
  (batch-39 probe-level WINs, sit in NO cache).
- Scripts: `scripts/make_increments_el_adoption.py` (sha
  910ede30d49251d88ee83b778aa65486609fc0b8937a0b237fdaaf6ed38d1d17,
  EI-maker fork adapted to the Part EK artifacts, fail-closed), and the
  byte-clone of the pinned fail-closed union merger
  `scripts/s5_union_merge.py` (sha 90711961..., identical to the published
  Part EE/EI merger bytes).
- Protocol: publish-then-execute.  Maker 3x byte-identical + tamper battery
  (T-EL1 raw sha drift / T-EL2 status.log kit sha drift / T-EL3 BASE cache
  sha drift, each rc=1 fail-closed) + restored clean control, then merger 3x
  byte-identical (cache + merge-audit).  Outputs: increment
  `output/increment-aj039loss1-20261125.cache` (1,254 B, sha 7838b081...),
  `output/increments-manifest.json` (schema
  `ek-aj039loss1-increments-manifest-v1`, sha 34439f4d...), merged chain head
  `output/merged-exact-s5-chain-plus-aj039loss1-20261125.cache` (6,713 rows,
  WIN 158 / LOSS 6,555, sha cf08e181...), merge-audits x3 (sha 0ab05a15...
  each).  Reaudit refresh fork + delta extractor follow as waves D/E.
- **This unit consumes NO WIN verdict, asserts NO root verdict, frees NO
  class and excludes NO class.  The standard 11x11 empty board stays
  UNKNOWN; nodes are bookkeeping, never verdicts.**
## Run record (waves A-F; every published byte fetch-back verified)

| wave | content | commit |
|---|---|---|
| A | single-owner adoption declaration (counter-declaration scan clean) | `11ac123f` |
| B | kit: maker `scripts/make_increments_el_adoption.py` (sha `910ede30...`, EI-maker fork pinned to the Part EK artifacts) + pinned union merger byte-clone `scripts/s5_union_merge.py` (sha `90711961...`) | `405dcc17` |
| C | outputs 6: increment (1,254 B, `7838b081...`) / increments-manifest (`34439f4d...`) / merged chain head (`cf08e181...`, 6,713 rows WIN 158 / LOSS 6,555) / merge-audit x3 (`0ab05a15...` each) | `56bcc871` |
| D | reaudit refresh fork `reaudit/scripts/refresh_adoption_el.py` (sha `c0debd18...`) | `648ef1b0` |
| D | reaudit outputs 3: refresh-summary (`4579a021...`) / closure-classes (`880e1c37...`) / per-root-coverage (`bafc7b66...`); probe-worklist.csv NOT published (3,721,201 B, size policy; regen pin `ed289920...`, extractor reruns regenerate it byte-identical x3) | `9df5a474` |
| E | delta extractor `scripts/compare_deltas_el_adoption.py` (sha `220348fa...`) + machine decomp-deltas json (`02103ac1...`) | `3f613fc0` |
| F | this README run record + MANIFEST-sha256.txt (14 entries) + completion log `research/log/2026-11-25-part-el-aj039loss1-adoption-completion.md` | (this commit) |

Fail-closed verification battery: maker pre-dry 3x byte-identical + tamper T-EL1/EL2/EL3 (raw-sha / status.log / BASE-cache drift, each rc=1) + restoration byte-identical; merger 3x byte-identical with identical merge-audits; refresh fork 3x byte-identical (~62 s/run); extractor pre-dry 3x byte-identical (decomp sha `02103ac1...` x3) + tamper T-EL4/EL5/EL6 (scenario-cache / manifest / closure-classes single-byte flips, each rc=1 fail-closed) + restoration byte-identical. The extractor additionally re-executes BOTH published refresh forks (Part EI `1bcf1972...` and Part EL `c0debd18...`) from published bytes on every run and gates all 8 outputs byte-identical, so every reaudit output in this dir is provably regenerable from published bytes alone.

Independent second-environment verification of waves B-D (parallel lane): maker 3x / merger 3x / refresh 3x byte-identical from a fresh clone of published bytes, tamper T-EL1..4 fail-closed including a coordinated two-pass RAW_SHAS rewire caught at the kit-manifest pin layer, clean control PASS: `research/log/2026-11-25-part-el-aj039loss1-waves-bcd-second-environment-verification.md`.

Machine-derived deltas (BASE = published Part EI reaudit, SCENARIO = Part EL; recomputed by the extractor, never hand-transcribed): class 30484 unknown 6 -> 5, rank 9 -> 7, groups_served 4 static, NOT freed, NOT excluded (54-child Board boundary regenerated; the adopted aj039 is the only adopted member; the 5 remaining unknowns are aj030 892576 unconsumed probe-level WIN + ai044 900354 / ai048 900718 EF claim-reserved + aj049 902511 / aj050 902512 unconsumed batch-39 probe-level WINs); classes 30118 / 16371 byte-static (adopted key outside both Board boundaries); 20421 / 34908 rank-churn-only (8 -> 9 / 7 -> 8, unknown static); closure table 807 rows on both sides, zero left/entered, zero groups_served churn, 804 fully stable rows + exactly 2 rank-churn-only rows + class 30484 itself; update8 byte-static (resolved 259 / remaining 31,600 / groups_free_now 131 / newly-resolved empty; the adopted s5 index 897668 sits outside the frozen baseline requirement); class_status EXACTLY static {excluded 390, excluded_now 23, free_now 39, unknown 34,497} (Board verification 39/39, zero rejections both sides); bookkeeping only: joint greedy 36,505 static, worklist 64,366 -> 64,365, known universe 891 -> 892, cache in universe 868 -> 869, free/uncovered thirds identical at every root (nothing freed), root 24 individual greedy 2,782 -> 2,781 pure re-selection, root 27 stays 119/119.

Interpretation guard (unchanged in force): this Part consumes exactly 1 fresh exact-LOSS verdict row (aj039, Part EK 30M two-pass fresh-cold node-exact, resolved in (15M, 30M] beyond the honest EXHAUSTED 15M history - not a same-condition re-probe). NO WIN verdict and NO EXHAUSTED verdict enters the canonical cache; the probe-level WIN rows aj030 / aj049 / aj050 sit in NO cache (scrutiny-owner C++ second-implementation gate pin `9193f5b6...` exclusive); the EF claim-reserved dual-class batch-38 keys ai044 / ai048 are untouched. Nothing is freed, nothing is excluded, no root verdict and no coverage claim is made. The standard 11x11 empty board and all 19 central-reply roots stay UNKNOWN.

