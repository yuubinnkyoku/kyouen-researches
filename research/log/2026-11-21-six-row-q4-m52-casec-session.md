# Session log: six-row q=4 m=52 case-c-complete escalation (fast lane, 2026-11-21, Part B)

Lane: standard-rule fixed-width q=4, six-row m=52 case-c-complete escalation
(Part B). Single-owner declaration:
`2026-11-21-five-row-q4-band-41plus-and-six-row-q4-m52-casec-single-owner-note.md`
(commit `bab006adc`, HEAD-at-declaration `0265c39b00`), same declaration as
the Part A session (five-row band 41+, commit chain a1dcf585/73cb82bd/124833bb/
d0d99e68/f092653c, K1212). Declared non-goals: (6,5)/(6,6)/(6,7) fronts,
(7,4) band, 11×11 heavy jobs. Acceptance conditions and their outcomes are
listed in K1213; all were met except that the escalation itself was negative
(which the declaration explicitly provided for: negatives are recorded as
finite scoped census records only).

## What was done

1. Engine completion (surgery_gen2 → surgery_gen2.1). The intermediate gen2
   engine (bounded-edit surgery, CUR(u) prefilter of seed-pair curves through
   each empty cell) reproduced control (a) at only 14/16 per base — the same
   2-orbit loss as K1211's published engine (56/64). Direct diagnosis on the
   two lost orbits (published idx 1, 15): both witnesses PASS the complete
   certification; their loss was an UNSOUND PREFILTER REJECT — for orbit 1,
   needed cell [39,1] is covered only by the circumcircle of [39,1],[32,1],
   [37,0] which happens to hold exactly ONE surviving seed stone (34,0) and no
   removed stone; such a curve is not a seed-pair curve and was invisible to
   CUR(u). Fix: an on-the-fly FINAL case-c branch in the kA=2 sweep (curve
   (u,a,b) survivor test), making the coverage classification exactly
   occupy/strong/k1/branch-4. kA=1 classes were already complete (a kA=1
   covering curve through u needs an add + ≥2 surviving seeds = strong).
   Integrity note: an early diagnostic harness had consumed the K1211 control
   config object's missing `m` key as undefined, silently emptying all
   board loops and vacuously "passing" verifyComplete; the diagnosis was redone
   with the explicit target width. No published or staged data was affected.
2. Control (a) K1209 m39→40: 64/64 exact (16 per D4 base, all 2R2A; union =
   the published 64-hit family exactly). Byte-identical replay verified.
3. Control (b) K1211 47→48: 4/4 reproduced exactly (m48-w1/w2/w1v/w2v);
   id_s5/v_s5 negative with the case-c branch active; plus a 3R extension
   (3R1A/3R2A) on all four seeds: 0 witnesses. The complete ≤3R≤2A census of
   the 47→48 surgery is exactly the 4 published witnesses.
4. m=52 escalation: seeds w51-{id,v,h,hv}-m51 (17 stones), board 6×52,
   classes 1R1A/2R1A/2R2A/3R1A/3R2A, E=295, 35,631,575 candidates per seed,
   142,526,300 total, case-c-complete, deterministic: **0 witnesses**.
   Byte-identical replay verified (m52esc id). Negative recorded as a finite
   scoped census (K1213 claim 4); M_{6,4} stays [52, 1113], m=52 UNDETERMINED;
   the declared roadmap step m51→m52 fails for every declared class from all
   four bank seeds.
5. Publication: experiment directory
   `research/experiments/six-row-q4-m52-casec-20261121/` (36 files: README,
   digests.txt, engine + diagnostic trace scripts, 16 run configs, 16 outputs)
   pushed as commit `38075cde` (HEAD-before-push `ea73c3e3`); fetch-back
   verification of all 36 files byte-identical at that commit. K1213 item and
   this session log in the following commit. Knowledge README bullet appended
   last (README re-fetched at its own HEAD immediately before that push).

## Superseded intermediate record (honesty trail)

- Pre-fix gen2 runs (14/16 per base on control (a), 4/4 on control (b), and a
  pre-fix m52 sweep) are superseded by the gen2.1 census; they were never
  published and are only referenced in the experiment README §5. The missing
  branch could only RESTORE candidates, so the gen2.1 negatives imply the
  pre-fix negatives a fortiori; the gen2.1 positives are complete.
- The git-push of the experiment happened after concurrent twin-lane commits
  (n11 S5 probe, seven-row batches) had advanced main from `c476182a` to
  `ea73c3e3`; no conflicts arose (new directory only).

## Next candidates recorded for the (6,4) front (no action taken)

- Fresh m51 seeds: the four bank w51-*-m51 configurations share one unblocked
  cell each; the negative census suggests that within ≤3R≤2A the unblocked-cell
  geometry cannot be re-covered at width 52. Candidate next steps: (i) 4A/3A
  classes at m=52 (beyond the declared |A|≤2 budget, needs a new declaration),
  (ii) new m51/m50 seeds from the K1211 translation+census bank outside the
  four chosen escalation lanes, (iii) an m52 seed-hunt from the m48 witnesses
  via 3R at 6×49/6×50/6×51 (staircase-style), each requiring a fresh
  single-owner declaration.
