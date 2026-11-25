# n11-centralreply-b38loss24-adoption-reaudit-20261125 (Part EM)

Loss-only canonical adoption of the **24 fresh exact-LOSS rows** of the
published, complete Part EF batch-38 kit (`ai001, 004, 008, 009, 011, 012,
015, 016, 018, 019, 020, 021, 022, 025, 026, 027, 029, 031, 032, 033, 037,
042, 044, 045`, adopted node total per pass 168,055,078), every one a
first-ever probe (two-pass fresh-cold node-exact at the single 15M
budget/order-0 condition, solved within budget, MISMATCH 0).  Declaration:
`research/log/2026-11-25-part-em-b38loss24-adoption-declaration.md`.

- BASE: the published Part EL canonical merged cache
  `merged-exact-s5-chain-plus-aj039loss1-20261125.cache` (6,713 rows,
  WIN 158 / LOSS 6,555, sha256 cf08e181...).
- Pool source: the published Part EF batch-38 kit
  `research/experiments/n11-centralreply-closure-class30345-batch38-20261125/`
  (MANIFEST-sha256 4dbf8856..., 181 files, batch-audit.json 73652099...
  all gates PASS, verdicts_consumed false; 24 LOSS / 19 WIN / 6 EXHAUSTED).
- NOT consumed: the 19 batch-38 probe-level WIN rows (incl. **ai048**, the
  class-30484 dual-class sibling of the adopted ai044 - WIN canonical
  adoption is scrutiny-owner C++ second-implementation gate
  `9193f5b6...` exclusive, sits in NO cache); the 6 honest-EXHAUSTED keys
  (ai007/ai024/ai030/ai038/ai040/ai041, honest UNKNOWN at 15M,
  same-condition re-probe prohibition in force); b018 (prior batch-1
  dual-class WIN, excluded); aj030 / aj049 / aj050 (Part EK/batch-39
  probe-level WINs, sit in NO cache).
- Scripts: `scripts/make_increments_em_adoption.py` (sha
  c787472af13275ec31c73b58c9daeeeb181c4576f9d003c85ebce4456e6d2b34,
  EL-maker fork adapted to the Part EF artifacts, fail-closed), the
  byte-clone of the pinned fail-closed union merger
  `scripts/s5_union_merge.py` (sha 90711961..., identical to the published
  Part EE/EI/EL merger bytes), the reaudit refresh fork
  `reaudit/scripts/refresh_adoption_em.py` (sha baf9cbde..., EL-refresh
  fork with the EM merged-cache pin) and the delta extractor
  `scripts/compare_deltas_em_adoption.py` (sha 2d6ae570...,
  EL-extractor fork with BASE = the published Part EL reaudit outputs).
- Protocol: publish-then-execute.  Maker 3x byte-identical + tamper battery
  (T-EM1 kit-raw / T-EM2 status / T-EM3 BASE-cache drift, each rc=1
  fail-closed) + restored clean control, merger 3x byte-identical (cache +
  merge-audit), refresh fork 3x byte-identical (~62 s/run, all 4 outputs
  incl. the probe-worklist regen), extractor 2x byte-identical + tamper
  T-EM4/5/6 (scenario-cache / manifest / closure-classes single-byte
  flips, each rc=1 fail-closed) + restored clean control.
- Outputs: increment `output/increment-b38loss24-20261125.cache` (2,638 B,
  25 comment lines + 24 s5verdict exact-LOSS rows, sha 3c632661...),
  `output/increments-manifest.json` (schema
  `em-b38loss24-increments-manifest-v1`, sha ac5649f8...), merged chain
  head `output/merged-exact-s5-chain-plus-b38loss24-20261125.cache`
  (6,737 rows, WIN 158 / LOSS 6,579, sha b5be64e6..., 281,016 B),
  merge-audits x3 (sha 4a877e17... each), reaudit outputs
  (refresh-summary bacf6a68... / closure-classes 93a68897... /
  per-root-coverage bce9f8f1...; probe-worklist.csv NOT published,
  3,719,664 B, size policy, regen pin b4d16b7f...), machine decomp
  `output/decomp-deltas-b38loss24-adoption.json` (sha cd8bbf89...).
- **This unit consumes NO WIN verdict, asserts NO root verdict, frees NO
  class and excludes NO class.  The standard 11x11 empty board stays
  UNKNOWN; nodes are bookkeeping, never verdicts.**

## Run record (waves A-F; every published byte fetch-back verified)

| wave | content | commit |
|---|---|---|
| A | single-owner adoption declaration (counter-declaration scan clean at main `86644142`; registered as resume note (b) of the Part EF completion log) | `4e3185b7` |
| B | kit: maker `scripts/make_increments_em_adoption.py` (sha `c787472a...`, EL-maker fork adapted to the 24-row EF pool, all 181 kit files byte-verified, 49-key pins machine-regenerated from the kit SSOTs) + pinned union merger byte-clone `scripts/s5_union_merge.py` (sha `90711961...`).  Maker 3x byte-identical + tamper T-EM1/2/3 rc=1 + restoration identical | `98b4bfb7` |
| C1 | merged chain head `output/merged-exact-s5-chain-plus-b38loss24-20261125.cache` (`b5be64e6...`, 6,737 rows WIN 158 / LOSS 6,579, exactly as declared) | `ff2a3836` |
| C2 | increment (`3c632661...`, 2,638 B) + increments-manifest (`ac5649f8...`, schema em-b38loss24-increments-manifest-v1) + merge-audit x3 (`4a877e17...` each).  Merger 3x byte-identical | `3c174ef2` |
| D | reaudit refresh fork `reaudit/scripts/refresh_adoption_em.py` (sha `baf9cbde...`, 3 changes vs the EL fork: docstring / CACHE path / cache sha pin) | `c56cb936` |
| D | reaudit outputs 3: refresh-summary (`bacf6a68...`) / closure-classes (`93a68897...`) / per-root-coverage (`bce9f8f1...`); probe-worklist.csv NOT published (3,719,664 B, size policy; regen pin `b4d16b7f...`, refresh 3x byte-identical).  Refresh fork published-then-executed, 3x byte-identical (~62 s/run) | `c7b24ce4` |
| E | delta extractor `scripts/compare_deltas_em_adoption.py` (sha `2d6ae570...`) + machine decomp-deltas json (`cd8bbf89...`).  Extractor 2x byte-identical + tamper T-EM4/5/6 (scenario-cache / manifest / closure-classes single-byte flips, each rc=1 fail-closed) + restoration byte-identical | `2c03af4e` |
| F | this README run record + MANIFEST-sha256.txt (14 entries) + completion log `research/log/2026-11-25-part-em-b38loss24-adoption-completion.md` | (this commit) |

The extractor verifies ALL 181 EF kit files (sha + size), re-verifies ALL
49 batch-38 keys' two-pass raw replays against the batch-keys SSOT and the
manifest decomposition (the 7 reported p2-truncation retry artifacts are
the only non-complete raw files and are audit-accounted), re-executes BOTH
published refresh forks (Part EL `c0debd18...` and Part EM `baf9cbde...`)
from published bytes in isolated scratch trees on every run and gates all 8
outputs byte-identical, so every reaudit output in this dir is provably
regenerable from published bytes alone.

Machine-derived deltas (BASE = published Part EL reaudit, SCENARIO = Part
EM; recomputed by the extractor, never hand-transcribed):

- **class 30345** (the batch-38 target): unknown **50 -> 26**, rank
  **13 -> 11**, groups_served 4 static, NOT freed, NOT excluded; all 24
  adopted rows sit inside its 51-child Board boundary (1 non-s5 child;
  50 in-universe children at BASE, zero known at BASE).
- **class 30484** (dual-class owner of ai044/ai048): unknown **5 -> 4**,
  rank 7 -> 7, groups_served 4 static, NOT freed, NOT excluded; the
  adopted ai044 (s5 900354) is the only adopted member inside the
  54-child boundary; the 4 remaining unknowns are ALL unconsumed
  probe-level WINs: aj030 892576 / ai048 900718 / aj049 902511 /
  aj050 902512.
- **class 30118** (the in-flight Part EJ batch-40 target): unknown
  **52 -> 51**, rank **21 -> 17**, groups_served 4 static, NOT freed,
  NOT excluded; exactly one adopted row (ai033) sits inside its 56-child
  boundary; the EJ owner lane is untouched - its worklist baseline moved
  and the EJ owner must re-baseline from this published cache.
- witnesses 16371 / 20421 / 34908: **byte-static** (closure rows
  byte-identical; zero adopted members inside their Board boundaries).
- closure table: 807 rows both sides, zero left/entered, zero
  groups_served churn; 6 rank-churn-only rows (1518 / 2634 / 5343 / 8106 /
  8785 / 13342, each +1) + 798 fully stable rows; ZERO additional
  unknown_now changes beside the three classes above (Board-verified
  own-membership deltas).
- update8: byte-static (resolved 259 / remaining 31,600 /
  groups_free_now 131 / newly-resolved empty / win_hit_groups []); ALL 24
  adopted s5 indices sit OUTSIDE the frozen update8 baseline requirement.
- class_status EXACTLY static {excluded 390, excluded_now 23, free_now
  39, unknown 34,497} (Board verification 39/39, zero rejections both
  sides); root 27 stays 119/119.
- bookkeeping only: joint greedy 36,505 -> 36,460 (unique_groups 2,115
  static), worklist 64,365 -> 64,339, known universe 892 -> 916,
  cache in universe 869 -> 893, free/uncovered thirds IDENTICAL at every
  root (nothing freed), individual greedy re-selection only at 6 roots
  (0: 3001->3000, 1: 6352->6351, 2: 6129->6134, 12: 2890->2866,
  24: 2781->2780, 36: 2997->2975).

Interpretation guard (unchanged in force): this Part consumes exactly the
24 fresh batch-38 exact-LOSS verdict rows (two-pass fresh-cold node-exact
at the single 15M condition, each a first-ever probe).  NO WIN verdict and
NO EXHAUSTED verdict enters the canonical cache; the 19 batch-38 WIN rows
(incl. ai048), the 6 honest-EXHAUSTED keys, b018 and aj030/aj049/aj050 sit
in NO cache (scrutiny-owner C++ second-implementation gate pin
`9193f5b6...` exclusive).  Nothing is freed, nothing is excluded, no root
verdict and no coverage claim is made.  The standard 11x11 empty board and
all 19 central-reply roots stay UNKNOWN.
