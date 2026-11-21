# Session log: five-row q=4 band 41..44 constructive extension (fast lane, 2026-11-21)

Lane: standard-rule fixed-width q=4, five-row band. Single-owner declaration:
`2026-11-21-five-row-q4-band-41plus-and-six-row-q4-m52-casec-single-owner-note.md`
(commit `bab006adc`, HEAD-at-declaration `0265c39b00`), converge policy vs twin
declarations `5bf4c7a51` / `cdd3b80ec` recorded in the declaration (their (5,4)
m=41 experiment dirs were not on main at census time; the lane ran its own
census first and publishes it here).

## What was done

1. Re-placed the 16 published K1209 width-40 witness stone sets under the full
   D4 image group x all translations (scan 64) with the published K1211 engine
   v2 (byte-identical, configs set to w=5, two fail-closed calib gates matching
   the K1209 published values). 2476 placements. Result: 34 placements with
   R >= 41 (R=41: 18, 42: 6, 43: 6, 44: 4), all seeds from the m40_1/m40_3/
   m40_7/m40_9/m40_15 families. The m40_3-family H/HV shift-0 placement
   (maxx=24) witnesses twenty consecutive widths [25,44], the widest single-set
   staircase recorded for (5,4).
2. Cascade census over the four R=44 placements as seeds (scan 80, 896
   placements): the staircase is shift-generated (R = 25+k at left-offset
   k in 0..19, saturation at R=44, collapse beyond); no R >= 45 in any scanned
   window (bounded-family negative observation only).
3. Width coverage 41/42/43/44 confirmed (28/12/8/4 placements per width with
   maxx+1 <= m <= R). Band update: **M_{5,4} in [45, 567]** (lower bound = 44
   witnessed; T_5 = 567 unchanged). m = 45: UNDETERMINED.
4. Erratum against the K1209 README closure sentence ("R(S)=40 for all 16
   sets ... none extends to width 41") recorded: K1209's own published raw
   `output/criterion-m40-witnesses.txt` already contains reach 42 /
   witness_widths [38,42] for its second record (W[1], maxx=37). No K1209
   primary file was modified (AGENTS.md). The K1209 value claim [41,567]
   remains valid; this lane supersedes the value.
5. Verification: (i) census engine det4; (ii) published K1209
   `append_criterion.py` (Fraction), 34/34 first_unblocked agreement;
   (iii) published `verify_node.mjs` (BigInt Bareiss). 52-item verification
   bank (placement x each width max(41,maxx+1)..R) 52/52 ok on both executable
   families; stone-move tamper fails loudly on both (uncovered=2). All
   outputs regenerated twice, byte-identical. All scripts byte-identical to
   published versions (sha256 in digests.txt).
6. Honesty record: the first bank draft used the width range 41..R without the
   maxx+1 floor; the fail-closed engine assert caught stones outside the
   claimed board and the bank was rebuilt (52 items) before any verification
   was accepted. An earlier FNV implementation bug (float overflow instead of
   32-bit modular multiply; caught by the length-verified-mismatch pattern when
   transport-checking prior to push; fixed with Math.imul) is recorded here;
   no published artifact was affected.
7. Publication: experiment dir published in three commits (small files,
   census1, census2); fetch-back byte-identical on all 15 files
   (commits `a1dcf585`, `73cb82bd`, `124833bb`).

## What is NOT claimed

- No witness-population completeness at widths 41..44 (only the published
  seeds' D4 x translation re-placements were enumerated).
- m = 45: UNDETERMINED (existence or absence not claimed; max R=44 over the
  family is a bounded observation).
- No new engine code; mwq_stabilization.csv unchanged; T_5 unchanged;
  11x11 / two-stone roots / S2 / class 1/2/4 untouched, UNKNOWN.
- The six-row (6,4) m=52 case-c-complete escalation declared in the same
  note is NOT covered by this session's publication (separate work item).

## Artifacts

- Experiment: `research/experiments/five-row-q4-band-41plus-20261121/`
- Knowledge item: K1212.
- Declaration: `research/log/2026-11-21-five-row-q4-band-41plus-and-six-row-q4-m52-casec-single-owner-note.md`
