# 2026-11-16 n11 class2-lane cost-66c WIN7 certificates blind re-extraction verification (7/7 byte-identical)

## Start state

- Start main: `fcbd795d` (post-fold, canonical head 1450/174/6398/506297/4671/370211).
- Inputs: the 7 published cost-66c WIN7-D10 certificates (bits 73/75/79/87/96/97/112
  of child `00000000000000003800000008002008`, commits `9590bb1c`..`00b73223`, manifest
  blob `463ed0f0`), the published dual verification records, and the landed fold
  receipt's per-bit certificate entries (`96e2dbac`).

## Method (fully blind)

- Moves: re-enumerated per root with the published `legal_candidates.py`
  (44/53/47/50/51/45/58 moves) - all 7 agree with the published driver move lists,
  no hand transcription (root hexes regenerated with `%032x` from child|1<<bit; a
  hand-transcribed bit-97 root hex was caught and discarded during setup, the same
  failure mode as the publisher's bit-97 incident).
- Extraction: published generic driver `cert_driver65j.ts` + repo-verbatim
  `class4_child1_cert_extractor_exact_v16.ts`, empty kill table (blind), fresh
  environment, one part1of1 chunk per root.
- Assembly: `sorted(set(rows))` + `n11-terminal-strategy-v1` header + root line.
- Comparison: byte-for-byte against the published certificates (whole for bits 79/97,
  joined parts for 73/75/87/96, the first 3-part split joined for bit 112).
- Verifiers: both published verifiers re-run on the independently assembled certs:
  `verify_win7_certificate_bigint_independent.mjs` and
  `verify_bit7_win7_cert.ts --cert --root --root-check --subroots`.
- Cross-check: the independently assembled certs' md5s compared against the landed
  fold receipt's per-bit certificate entries.

## Results

- **7/7 assembled certificates byte-identical to the published ones** (total
  310,129 rows / 42,779,918 extraction nodes / 348 sub-roots / 11,218,652 bytes;
  bit 112 = the first 3-part split, 2,774,034 bytes joined).
- Per-move node counts agree for every move of every root (engine fingerprint at
  the deepest available granularity); fbt_drops 0, no fatal.
- BigInt verifier: 7/7 union_missing 0 / union_extra 0, all record fields equal to
  the published bigint-verify records.
- Bareiss verifier: 7/7 all sub-roots PASS (348/348 across the 7 roots), terminal
  range [13,17], all aggregate fields equal to the published bareiss-verify records.
- Fold receipt cross-check: 7/7 md5 / extraction-nodes / sub-root counts agree with
  the receipt's certificate entries.
- Output: `output/class2-lane-cost66c-win7-certificates-independent-verification-20261116.json`
  + the 7 independent extraction summaries
  `class2-lane-cost66c-independent-extraction-bit{73,75,79,87,96,97,112}-summary-20261116.json`.

## Position

- The certificate layer of cost-66c is now third-party verified end-to-end: sweep
  verdicts (independent re-run, `42788a0d`), certificates (this verification),
  fold receipt vs pre-registration (companion commit). All 7 WIN7-D10 certificates
  are rebuildable from published artifacts alone by a third party.
- Head 1450 unchanged by this verification.

## Interpretation guard

- Bookkeeping verification only. WIN7 certificates prove a first-player win within
  depth 10 from the individual 7-stone roots only. REFUTED-D10 is not a LOSS proof.
  NOT-STERILE is not a game resolution. The 11x11 empty board, the two-stone roots
  {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 all remain **UNKNOWN**.
