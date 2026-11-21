# K1212: the (5,4) witness band extends to m=44 — translation/D4 census over the published K1209 width-40 witnesses reaches R=44 (staircase 25..44 from one stone set), an erratum against the K1209 README closure sentence, and M_{5,4} in [45, 567]

Date: 2026-11-21
Lane: standard-rule fixed-width q=4, five-row band ("(5,4) band 41+ constructive
extension" fast lane). Single-owner declaration:
`research/log/2026-11-21-five-row-q4-band-41plus-and-six-row-q4-m52-casec-single-owner-note.md`
(commit `bab006adc`, 2026-11-21, HEAD-at-declaration `0265c39b00`), with a
converge policy recorded for the twin declarations `5bf4c7a51` / `cdd3b80ec`
(their (5,4) m=41 experiment directories were not on main at census time; this
lane's census was run first and is published with the converge note). Acceptance
conditions of the declaration: published-script lineage only (the census engine
is the published K1211 engine byte-identical, configs set to w=5), fail-closed
calibration gates, >= 2 independent integer verification families, byte-identical
determinism runs, lower-bound-only value update, T_5 unchanged. All conditions met.

## Claims (each machine-verified and exactly scoped)

1. **R(S) exhaustive re-placement census of the published K1209 width-40
   witnesses (exact integer arithmetic).** Seeds: the 16 published K1209
   distinct width-40 witness stone sets. Census: D4 images (id/H/V/HV) x all
   horizontal shifts in the scan window (scan 64), 2476 placements, with two
   fail-closed calibration gates asserted in-engine (m40_1 id s15 -> R=42,
   first unblocked [42,1]; m40_3 id s15 -> R=40, [40,1] — both equal the K1209
   published values). R distribution above 40: **R=41: 18, R=42: 6, R=43: 6,
   R=44: 4 placements** (34 placements with R >= 41). The four R=44 placements
   all come from the m40_3 family: H/HV at shift 0 (maxx=24) and V/id at
   shift 19 (maxx=43); the H/HV shift-0 placement witnesses twenty consecutive
   widths **[25, 44]** — the widest single-set staircase recorded for (5,4),
   replacing K1209's nine-width record (32..40, the maxx=31 set). A cascade
   census over the four R=44 placements as seeds (scan 80, 896 placements)
   reproduces the staircase as shift-generated (R = 25 + k at left-offset
   k in 0..19, saturation 16 placements at R=44, collapse to R in {0,1}
   beyond) and finds **no R >= 45 anywhere in the scanned windows** — a
   bounded-family negative observation only.
2. **Band update (the only value change).** Every width m in {41, 42, 43, 44}
   has a placement with maxx+1 <= m <= R (counts among the 34: 28/12/8/4 for
   widths 41/42/43/44): the (5,4) def-mode witness band now includes m=41..44,
   and with the published widths 5..40 (K1207 bank + K1209) the lower bound
   moves by four: **M_{5,4} in [45, 567]** (lower bound = width 44 witnessed;
   upper bound T_5 = 567 = B_max(5)+1 from the K1207 demand-supply inequality,
   unchanged). `mwq_stabilization.csv` is unchanged (K1201 precedent); the
   frontier moves to m=45.
3. **Erratum recorded against K1209 (README claim vs K1209's own raw output;
   no primary file modified).** The K1209 experiment README states "R(S)=40
   for all 16 sets, so none of them extends to width 41 (each leaves exactly
   the free cell (40,1) unblocked)". K1209's own published raw file
   `output/criterion-m40-witnesses.txt` records for its second record
   ("witness 2", 0-based W[1], the maxx=37 set): free_append_reach=42,
   first_unblocked=[42,1], witness_widths=[38,42] — i.e. width-41 and
   width-42 witnesses were already present in the published K1209 raw data.
   The K1209 value claim M_{5,4} in [41, 567] itself remains valid (width 40
   was witnessed regardless; no material conflict); the sentence quoted above
   is a documentation-side inconsistency inside K1209, recorded here as the
   erratum note. Per AGENTS.md, K1209 primary files are not edited.
4. **Verification (three independent integer families).** For the 34 R>=41
   placements and the widths they witness: (i) the census engine (published
   K1211 engine v2, det4, byte-identical, sha256 pinned); (ii) the published
   K1209 `append_criterion.py` (exact Fraction circle equations,
   byte-identical): first_unblocked agrees on 34/34; (iii) the published
   `verify_node.mjs` (BigInt Bareiss, byte-identical). Verification bank
   (52 items = placement x every width m with max(41, maxx+1) <= m <= R,
   per-width counts 28/12/8/4): 52/52 ok on both executable families, tags in
   identical order. An earlier draft of the bank used the range 41..R without
   the maxx+1 floor; the engine's fail-closed assert caught the out-of-board
   stones and the bank was corrected before any verification was accepted
   (honesty record). Stone-move tamper control: both families fail loudly
   (ok=false, uncovered=2). Determinism: both census outputs regenerated
   twice, byte-identical; verification outputs regenerated twice, byte-identical.

## What this is not

- No completeness claim for the width-41..44 witness populations: only the
  D4 x translation re-placements of the published K1209 seeds (and of the four
  R=44 placements, for the cascade) were enumerated. Other stone sets may
  exist at every width.
- No existence or absence claim at m=45: UNDETERMINED. The max R=44 over all
  3372 placements is a bounded-family observation, not an absence proof.
- No new engine code was introduced for this result: all three scripts are
  byte-identical copies of published versions (pins in the experiment's
  digests.txt).
- mwq_stabilization.csv is unchanged; T_5 = 567 unchanged.
- The standard 11x11 empty board, two-stone roots {49,60}/{59,60},
  S2 {59,60}, class 1/2/4 are unrelated to this lane and remain UNKNOWN.
- The six-row (6,4) m=52 case-c escalation declared in the same single-owner
  note is a separate work item and is not claimed here.

## Evidence

- Experiment: `research/experiments/five-row-q4-band-41plus-20261121/`
  (README, 3 published scripts, 2 census configs with fail-closed calib gates,
  2 census outputs, criterion agreement record, 52-item verification bank,
  tamper bank, 3 verification outputs, sha256 digests; fetch-back byte-verified
  against the local pre-push artifacts on all 15 files).
- Session log: `research/log/2026-11-21-five-row-q4-band-41plus-session.md`.

## Relations

- Uses K1209 (the 16 published width-40 witness stone sets are the census
  seeds; the K1209 raw criterion file is the erratum's subject; the K1209
  m39->40 surgery is untouched).
- Uses K1211's published census/verification engine (byte-identical, configs
  set to w=5) and verification scripts; the (5,4) m=40 calib values are the
  K1209-published ones.
- Uses K1207 (T_5 = 567 upper bound; demand-supply inequality source).
- The six-row counterparts (K1211) found the same translation-census mechanism
  fertile (m=47 by pure translation); here the mechanism alone moves the
  (5,4) frontier by four widths without any stone edit.
- Non-goals (twin-lane territory, untouched): (6,5)/(6,6)/(6,7) frontiers, the
  (7,4) band lane, and the 11x11 root lanes.
