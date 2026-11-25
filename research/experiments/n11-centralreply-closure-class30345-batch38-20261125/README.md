# Part EF batch-38: closure class 30345 (rank 12) fresh 49-key probe - COMPLETE

Single-owner Part EF declared as `research/log/` declaration commit `16d7336e`
(2026-11-25T16:07:09+09:00); the original owner's drive stalled after inc5
(ai001..ai043, 43/49 keys); the takeover lane completed the remaining 6 keys
(ai044..ai049) under `research/log/2026-11-25-part-ef-batch38-takeover-declaration.md`
(commit bb97def1). All verdicts are UNCONSUMED honest labels; the standard
11x11 empty board and every root stay UNKNOWN.

## Selection basis (frozen at the EF declaration)

- Post-af034loss1 reaudit closure table: rank 12 class 30345
  (mask [1152922604118478848, 65536]) unknown_now 50;
  ranks 1..11 machine-verified fresh-0 (freshness-ranks1to12.csv e5f51717).
- The 50th unknown child is the batch-1 dual-class key b018
  (probe_order 140, probe-level unconsumed WIN from 2026-11-22, scrutiny-owner
  pending, same-condition re-probe prohibited) - excluded from targets.
- Targets: 49 fresh never-probed keys ai001..ai049 (probe_order 132..139, 141..181).

## Kit bytes (all sha-pinned in `input/batch-keys-b38.json` pins and MANIFEST-sha256.txt)

- scripts: jsreplay.js 84585617, runbatch.sh f591f8c2 (BUDGET 15,000,000, order 0),
  drive38_local_step.sh 2bd91341 (WIN-CONTINUE: one drive completes all 49 keys),
  make_batch38_keys.py 9b117808 (G1-G7 fail-closed), audit_b38.py (takeover-lane
  machine audit, b39 pattern, A1-A9).
- input: batch-keys-b38.json 29807104 + 49 single-row target CSVs
  (`target,0,5,lo,hi,legal,0,0,0,0,0` schema).
- sources: canonical cache fc3e4ac9 (6,666 s5verdict rows, read-only reference
  base of the EI-era chain head), closure-classes 27e00b0d, prior-probe universe
  6deee846 (2,104 pairs), worklist-class30345-extract 7fe55513,
  freshness e5f51717, quarantine 81d23160, refresh-summary 6af660a1,
  batch-1 packet byte-clones (batch keys 2aaccc94 / status 559a0884).
- val-gate: 4 molecules (2x 2M exhaustion, 15m LOSS pair 3,651,923 / 5,040,200)
  vs published batch-31 kit baselines (6e902ab1/eeafe3ac/8035fe54/91dffdec).

## Drive record (two-pass fresh-cold exact replay @15M, order 0)

Original owner waves: inc1 ai001-ai008, inc2 ai009-ai016,
inc3 ai018-ai021 (fresh re-probe after an owner-side sandbox reset: the
pre-reset local runs of these keys were NEVER published and are not evidence),
inc4 ai022-ai032, inc5 ai033-ai043 (commit d4a1792c, last 08:43Z).
Takeover lane wave: inc6 ai044-ai049 (commit c5a42798, 15:19-15:21Z) - val-gate
fresh 4/4 node-exact before the first drive step; 3 drive-step invocations
(2 keys x 2 workers each), 0 MISMATCH, 0 TRUNCATED in inc6.
Final status.log: 81 lines = 49 PASS + 6 EXHAUSTED + 19 WIN-HALT
+ 7 P2-TRUNCATED-RETRY (historical, each with a published truncated artifact
that carries no replay_done marker and is NOT evidence; the runner's
replay_done guard re-ran each affected pass fresh-cold).

## Results (49/49 keys resolved, honest labels, verdicts UNCONSUMED)

| key_id | probe_order | s5_index | honest label | nodes (2-pass node-exact) | legal |
|---|---|---|---|---|---|
| ai001 | 132 | 39148 | LOSS | 10528977 | 83 |
| ai002 | 133 | 151694 | WIN (unconsumed) | 3552766 | 74 |
| ai003 | 134 | 195012 | WIN (unconsumed) | 5682652 | 79 |
| ai004 | 135 | 298570 | LOSS | 4352970 | 87 |
| ai005 | 136 | 355799 | WIN (unconsumed) | 11770537 | 87 |
| ai006 | 137 | 391735 | WIN (unconsumed) | 8819998 | 88 |
| ai007 | 138 | 441292 | EXHAUSTED (honest UNKNOWN) | 15000000 | 84 |
| ai008 | 139 | 473959 | LOSS | 3221447 | 87 |
| ai009 | 141 | 604944 | LOSS | 7514829 | 78 |
| ai010 | 142 | 624629 | WIN (unconsumed) | 13066796 | 78 |
| ai011 | 143 | 657234 | LOSS | 6715814 | 82 |
| ai012 | 144 | 716150 | LOSS | 4767152 | 87 |
| ai013 | 145 | 731678 | WIN (unconsumed) | 10255279 | 78 |
| ai014 | 146 | 753317 | WIN (unconsumed) | 14969659 | 79 |
| ai015 | 147 | 754556 | LOSS | 3086764 | 91 |
| ai016 | 148 | 800006 | LOSS | 3496190 | 83 |
| ai017 | 149 | 826581 | WIN (unconsumed) | 8468415 | 81 |
| ai018 | 150 | 827502 | LOSS | 6236845 | 91 |
| ai019 | 151 | 866157 | LOSS | 4269857 | 91 |
| ai020 | 152 | 878758 | LOSS | 9007508 | 87 |
| ai021 | 153 | 879412 | LOSS | 6190420 | 78 |
| ai022 | 154 | 888325 | LOSS | 7405631 | 90 |
| ai023 | 155 | 888357 | WIN (unconsumed) | 13676098 | 85 |
| ai024 | 156 | 889534 | EXHAUSTED (honest UNKNOWN) | 15000000 | 86 |
| ai025 | 157 | 889976 | LOSS | 9392986 | 90 |
| ai026 | 158 | 891015 | LOSS | 9199731 | 87 |
| ai027 | 159 | 891592 | LOSS | 10234914 | 85 |
| ai028 | 160 | 892997 | WIN (unconsumed) | 4892185 | 76 |
| ai029 | 161 | 893644 | LOSS | 12001061 | 89 |
| ai030 | 162 | 894456 | EXHAUSTED (honest UNKNOWN) | 15000000 | 91 |
| ai031 | 163 | 894824 | LOSS | 4148336 | 84 |
| ai032 | 164 | 895608 | LOSS | 11928171 | 89 |
| ai033 | 165 | 895907 | LOSS | 4181137 | 80 |
| ai034 | 166 | 896605 | WIN (unconsumed) | 3087464 | 74 |
| ai035 | 167 | 897030 | WIN (unconsumed) | 4227036 | 84 |
| ai036 | 168 | 897221 | WIN (unconsumed) | 8137160 | 82 |
| ai037 | 169 | 897427 | LOSS | 7709821 | 89 |
| ai038 | 170 | 898436 | EXHAUSTED (honest UNKNOWN) | 15000000 | 89 |
| ai039 | 171 | 899303 | WIN (unconsumed) | 13065437 | 87 |
| ai040 | 172 | 899584 | EXHAUSTED (honest UNKNOWN) | 15000000 | 85 |
| ai041 | 173 | 900170 | EXHAUSTED (honest UNKNOWN) | 15000000 | 91 |
| ai042 | 174 | 900292 | LOSS | 9086966 | 86 |
| ai043 | 175 | 900322 | WIN (unconsumed) | 3897909 | 74 |
| ai044 | 176 | 900354 | LOSS | 5677449 | 72 |
| ai045 | 177 | 900436 | LOSS | 7700102 | 86 |
| ai046 | 178 | 900561 | WIN (unconsumed) | 5256793 | 80 |
| ai047 | 179 | 900716 | WIN (unconsumed) | 2946085 | 82 |
| ai048 | 180 | 900718 | WIN (unconsumed) | 2232854 | 68 |
| ai049 | 181 | 900719 | WIN (unconsumed) | 832069 | 72 |

Class-30484 dual-class claim-reserved children (first-ever probe, inc6):
- ai044 (s5 900354): **LOSS 5,677,449** - unconsumed honest label; a future
  loss-only adoption Part may adopt it (EI/EL pattern) to shrink class 30484's
  unknown children; the adoption is a separate declared Part, not done here.
- ai048 (s5 900718): **WIN 2,232,854** - unconsumed; scrutiny-owner C++ gate
  9193f5b6 exclusive for any adoption.

Totals per the machine audit (batch-audit.json 73652099...): 24 LOSS
+ 19 WIN (unconsumed) + 6 EXHAUSTED (ai007/ai024/ai030/ai038/ai040/ai041,
honest UNKNOWN, no same-condition re-probe), MISMATCH 0,
total nodes single pass 396,892,270. Nodes are bookkeeping, not win-distance.

## Machine verification

- audit_b38.py (A1-A9 fail-closed; see docstring for the batch-38-specific
  adaptations): 3x clean runs byte-identical batch-audit.json 73652099...;
  tamper battery 9/9 fail-closed incl. 2 deep coordination attacks
  (output/audit-battery.log 385bae6a).
- Independent second-environment verification lane (separate experiment dir
  `n11-centralreply-closure-class30345-batch38-secondenv-verification-20261125`):
  kit byte-reconstruction + maker re-run G1-G7 ALL PASS 49/49 inputs
  byte-identical + val-gate 4/4 node-exact + inc1-3 21 keys (42 passes) fresh
  re-run node-exact + 86-raw published-evidence crosscheck (wave V1 614f58ff);
  the inc4-5 22-key independent re-verification was interrupted (README final
  4e002320) and remains an open verification item for a future wave.
- inc6 (takeover lane) is the FIRST re-run evidence itself for ai044..ai049;
  a future independent verification wave can reproduce the 6 keys.

## Verdict discipline

No closure, no coverage, no secured-coverage, no root outcome is claimed
anywhere in this Part. Batch-38 verdicts are NOT consumed (the canonical chain
head is untouched; the 50 batch-38 child pairs remain absent from the canonical
cache by machine check A9). WIN adoption (including ai048) is exclusive to the
scrutiny-owner C++ gate 9193f5b6. The standard 11x11 empty board, all 19
central-reply roots, the two-stone roots, S2, and classes 30345/30484/30118
stay UNKNOWN.
