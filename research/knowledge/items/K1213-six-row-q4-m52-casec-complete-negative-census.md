# K1213: the (6,4) m=52 bounded-edit escalation census is completely negative — case-c-complete surgery engine (K1211 gap closed and independently re-root-caused), 47→48 census completed at ≤3R≤2A, M_{6,4} unchanged in [52, 1113]

Date: 2026-11-21
Lane: standard-rule fixed-width q=4, six-row m=52 case-c-complete escalation
("Part B" of the fast lane). Single-owner declaration:
`research/log/2026-11-21-five-row-q4-band-41plus-and-six-row-q4-m52-casec-single-owner-note.md`
(commit `bab006adc`, 2026-11-21, HEAD-at-declaration `0265c39b00`), same
declaration as K1212 (Part A). Declared non-goals: (6,5)/(6,6)/(6,7) fronts
(twin declarations `5bf4c7a51`/`cdd3b80ec`), (7,4) band, 11×11 heavy jobs.
Acceptance conditions of the declaration: reproduction of the K1209 64-hit
control, reproduction of the K1211 47→48 witnesses, case-c-completeness of the
add enumeration, ≥2 independent integer verification families for positives,
byte-identical determinism runs, and negatives recorded only as finite scoped
records. All conditions met (see below); the escalation outcome is NEGATIVE
and no global value changes.

Experiment directory (self-contained, all sha256 in its digests.txt):
`research/experiments/six-row-q4-m52-casec-20261121/` (commit `38075cde`).

## Claims (each machine-verified and exactly scoped)

1. **Case-c-complete bounded-edit surgery engine (exact integer arithmetic).**
   `scripts/surgery_gen2_1.js` enumerates removals R ⊂ S (|R| ≤ 3) and added
   cells A (|A| ≤ 2) class by class (1R1A/2R1A/2R2A/3R1A/3R2A; 3R3A excluded by
   declaration) and certifies every candidate with a COMPLETE on-board check
   (row caps, complete safety over S2, complete maximality over every empty
   cell), with the curve engine byte-verbatim from the published K1209
   surgery.js (sha256 `0410d787…`). Completeness of the coverage prefilter for
   q=4, kA=2 is the four-fold classification: occupy / strong (≥2 surviving
   seeds + an add) / k1 (≥2 base seeds incl. ≥1 removed + both adds) / FINAL
   case-c (circumcircle-or-line of (u,a,b) with exactly one surviving seed and
   no removed stone — a curve that carries only ONE base stone and hence is
   invisible to any seed-pair precomputation). Branch 4 was missing from the
   intermediate gen2 build (superseded; recorded in the experiment README §5)
   and is the SAME mechanism as K1211's diagnosed gap, independently
   re-derived from the construction side. The two K1209 orbits lost by both
   K1211's published engine and pre-fix gen2 (published idx 1 and 15) are
   certified by branch-4 circles: orbit 1 cell [39,1] only by circle
   (-71,-11,1258,1) through adds (32,1),(37,0) + surviving seed (34,0);
   orbit 15 cell [14,1] only by circle (-156,8,1585,3) through adds
   (37,4),(38,1) + surviving seed (15,4) (`scripts/diag-casec-trace.js`).
2. **Control (a): K1209 m39→40 reproduced 64/64.** On the four D4 image
   bases of the published m39 witness (5×40 board, remBudget 2): 16 certified
   witnesses per base, all 2R2A; the 4-base union (64 raw stone sets) EQUALS
   the published 64-hit family {16 published distinct sets × 4 D4 images},
   0 missing, 0 extra. K1211's published engine reproduced 56/64 on the same
   control; the missing 8 hits = orbits 1, 15 × 4 images are all branch-4-only.
3. **Control (b): K1211 47→48 reproduced 4/4 and the census COMPLETED.**
   On the four published m47 surgery seeds (6×48 board, remBudget 2):
   h_s6/hv_s6 each yield exactly the published 2 witnesses (m48-w1/w2 and
   m48-w1v/w2v, stone-set identical); id_s5/v_s5 yield 0, now with the
   case-c branch active (passFrontier strictly increased: 18→26 on h/hv;
   every additional frontier passer failed complete certification).
   Extension beyond the published remBudget (3R1A/3R2A): 0 witnesses on all
   four seeds. So the complete ≤3R≤2A bounded-edit census of the K1211 47→48
   surgery contains EXACTLY the 4 published witnesses — a census-level
   strengthening of K1211's record.
4. **Complete negative m=52 escalation census (finite record, scoped).**
   Seeds: the four published R=51 witness configurations (K1211 witness bank
   tags w51-id-m51 / w51-v-m51 / w51-h-m51 / w51-hv-m51, 17 stones each =
   the roadmap surgery52esc seeds), target board 6×52, classes
   1R1A/2R1A/2R2A/3R1A/3R2A, E = 295 empty cells. Total enumerated candidates
   35,631,575 per seed (1R1A 5,015 = 17·295; 2R1A 40,120 = C(17,2)·295;
   2R2A 5,897,640 = C(17,2)·C(295,2); 3R1A 200,600 = C(17,3)·295;
   3R2A 29,488,200 = C(17,3)·C(295,2)), 142,526,300 over the four seeds.
   **Witnesses: 0.** Every candidate either failed the sound prefilter or the
   complete certification. Statement (finite, scoped): no (6,4) witness at
   width 52 exists within edit distance ≤3 removals and ≤2 additions of ANY
   of the four published R=51 witness configurations. This does NOT decide
   m=52 existence in general and does NOT claim M_{6,4} > 52.
5. **Value conservation.** M_{6,4} ∈ **[52, 1113]** (K1211) UNCHANGED.
   m = 52: UNDETERMINED. T_6 = 1113 unchanged. The declared roadmap step
   "m51→m52 by bounded surgery" fails for every declared class from every
   bank seed; a next constructive step for the (6,4) front must come from a
   different neighborhood (fresh seeds at m51 with other unblocked-cell
   geometry, larger edit budgets, or non-surgery constructions).
6. **Determinism and verification chain.** Byte-identical full replays
   (control-a id base; m52esc id seed), cmp-clean. Validation of the negative:
   the identical code path certified the 68 positive witnesses of controls
   (a)+(b) (64 + 4), reproducing both published censuses exactly (K1209 =
   system 1 / gen2.1 = system 2 for control (a); K1211 = system 1 / gen2.1 =
   system 2 for control (b)). Publish-back fetch verification: all 36
   experiment files byte-identical to the staged originals at commit
   `38075cde`.

## Status of previously open threads

- K1211's "case-c gap" (56/64 on the K1209 control, 8 hits): CLOSED — root
  cause identified twice over (K1211's diagnosis on the enumeration side; this
  lane's diagnosis on the precomputation side: seed-pair curve tables admit
  only ≥2-base-stone curves while a branch-4 case-c curve carries exactly one
  surviving stone), implemented, and controlled against both published
  positive censuses (64/64, 4/4).
- The (6,4) m=52 escalation (Part B declared): DONE, negative, published as a
  complete census. 11×11 / two-stone root / S2 / class 1-2-4 fronts: not
  touched (as declared).
