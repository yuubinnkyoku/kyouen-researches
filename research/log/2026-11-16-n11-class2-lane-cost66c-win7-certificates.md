# 2026-11-16 n11 class2-lane cost-66c WIN7-D10 certificates (7 published, dual-verified; fold deferred to the post-cost65n head)

## Start state

- Start main: `b17e978e` (cost-66c sweep completed NOT-STERILE, claim v2).
- The 7 WIN7-D10 receipts (bits 73, 75, 79, 87, 96, 97, 112 of the sweep) were pending
  certificate extraction; the cost-65n fold and the cost-65o sweep were both still
  in flight (no landing between the sweep commit and this publication).

## Extraction

- Blind extraction with the published generic single-root driver `scripts/cert_driver65j.ts`
  (repo-verbatim `class4_child1_cert_extractor_exact_v16.ts`, empty kill table), one
  `part1of1` chunk per root; all hex values regenerated with `format(..., '032x')`,
  no hand transcription.

| bit | root hex | D4 canon | rows | extraction nodes | sub-roots | published form |
|----:|----------|----------|----:|------------------:|----------:|----------------|
| 73 | `00000000000002003800000008002008` | `00000000000000203800000008080080` | 34,822 | 2,379,811 | 44 | part1of2 + part2of2 |
| 75 | `00000000000008003800000008002008` | `00000000000000083800000008080080` | 40,267 | 3,619,378 | 53 | part1of2 + part2of2 |
| 79 | `00000000000080003800000008002008` | `00000000000000801202000220800000` | 30,590 | 2,372,373 | 47 | whole (1,107,891 B) |
| 87 | `00000000008000003800000008002008` | `00000000000020003800000008080080` | 41,870 | 3,421,353 | 50 | part1of2 + part2of2 |
| 96 | `00000001000000003800000008002008` | `00000000020020801202000040000000` | 54,558 | 6,009,719 | 51 | part1of2 + part2of2 |
| 97 | `00000002000000003800000008002008` | `00000000020000003800000008080080` | 31,205 | 1,364,577 | 45 | whole (1,130,350 B) |
| 112 | `00010000000000003800000008002008` | `00000000000000801202000300800000` | 76,817 | 23,612,707 | 58 | part1of3 + part2of3 + part3of3 |

- All 7 D4 canons match the census v4 bit table (`class2-lane-next-target-presweep-1441-20261116.json`)
  and the sweep log's receipt-root table.
- Totals: **310,129 rows / 42,779,918 extraction nodes / 348 sub-roots / 11,218,652 cert
  bytes**; winner_states 443,651 / loser_states 135,109 / terminal_count 107,270.

## The bit-97 extraction incident (recorded as an experiment fact)

- The first bit-97 extraction invocation passed a moves list derived from a
  **mis-transcribed root hex**: the file name and the moves list corresponded to the
  bit-85 root (50-move mobility) while the repo-verbatim extractor derived the correct
  bit-97 root internally from `(child, bit)`. The assembler's mobility assertion
  (`driver moves == legal_candidates(root)`) caught the mismatch before any publication.
  The wrong-scope chunk and its summary were discarded; bit 97 was re-extracted with
  the correct 45-move mobility (published figures 31,205 rows / 1,364,577 nodes; the
  discarded wrong-scope figures were 41,636 rows / 3,295,492 nodes on a 50-move list
  that is not the bit-97 mobility). This re-confirms the lane rule: every hex value is
  regenerated with `%032x` and cross-checked, never hand-copied. The manifest carries
  this record in `process_notes`.

## Assembly and verification

- `scripts/assemble_cost66c_certificates_20261116.py` (65n protocol, with the publication
  split generalized from 2 parts to N parts: bit 112's whole cert is 2,774,034 bytes,
  more than 2x the 1,200,000-byte publication split threshold, so it is the **first
  3-part cert split**; parts 924,688 / 924,695 / 924,651 bytes, join receipt published).
- Per bit: rows `sorted(set(...))` (exact byte order), `n11-terminal-strategy-v1` header
  + root line, then **both published independent verifiers**:
  - `verify_bit7_win7_cert.ts --cert --root --root-check --subroots` (exact integer
    Bareiss 4x4 determinants): **348/348 sub-roots PASS**, terminal range [13,17].
  - `verify_win7_certificate_bigint_independent.mjs` (BigInt 3x3 cofactor expansion):
    **union_missing 0 / union_extra 0** for all 7 roots, rows_sorted_unique true,
    root_mobility == `legal_candidates(root)` == the driver move list.
- Root-mobility cross-check against `legal_candidates.py` for all 7 roots; `fbt_drops` 0
  and no fatal on every extraction; the assembler was re-run end-to-end after the bit-97
  correction and reproduced every cert, receipt and verify wrapper byte-identically
  (second full dual-verification pass, deterministic).
- Independent join check (this session, stdlib only): the published parts concatenated
  equal the rebuilt whole byte-exactly for all 5 split certs; receipt md5/blob fields
  match the parts for every split.

## Publication

- Bookkeeping commit `39665854`: manifest
  `class2-lane-cost66c-win7-certificates-20261116.json` (blob `463ed0f0aafb`,
  schema `n11-class2-lane-cost66c-win7-certificates-20261116-v1`) + assembler
  (blob `99e6991445a2`) + 7x {bigint-verify, bareiss-verify, extraction summary} +
  5 split receipts (bit 112 3-part, bits 73/75/87/96 2-part).
- Cert commits: bit73 `9590bb1c`+`abc596e6`, bit75 `d03c1d91`+`75c93412`,
  bit79 `41fae118`, bit87 `c5317d94`+`a297ae2b`, bit96 `f20e9a0c`+`4e023fe5`,
  bit97 `a9246119`, bit112 `89418d8b`+`b2bed04c`+`00b73223`.
- **All 40 published files verified byte-identical against main via the raw CDN
  (cmp) after the final push.**

## Status and next steps

- The cost-66c row (66 candidates) is now fully determined at head 1441: 7 WIN7-D10
  with published dual-verified certificates + 52 swept REFUTED-D10 + 7 transferred
  REFUTED-D10, 0 capped. The row is **NOT-STERILE**.
- The **fold of the 7 WIN receipts is deferred** until the in-flight cost-65n fold
  (preregistration `class2-lane-cost65n-fold-preregistration-20261116.json`, blob
  `da2b2292`, projected head 1444/174/6404/506746/4677/370660) lands; the 66c fold must
  then run on the post-65n head basis with a conflict census against the folded-root
  corpus (and the cost-65o sweep corpus once it lands) before the next ranking.
- Cross-row watch item (unchanged): 66c bit 83 REFUTED-D10 root canon
  `00000000000000a09002080080000000` is D4-identical to the in-flight cost-65o claim's
  open bit 43 candidate; the cost-65o completion must record it as a transfer or a
  WIN/LOSS conflict investigation.

## Interpretation guard

- WIN7 certificates prove a first-player win within depth 10 from the **individual
  7-stone roots only**. REFUTED-D10 is not a LOSS proof. NOT-STERILE does not decide
  the row's own value. The standard 11x11 empty board, the two-stone roots {49,60} and
  {59,60}, S2 {59,60}, and classes 1/2/4 all remain **UNKNOWN**.
