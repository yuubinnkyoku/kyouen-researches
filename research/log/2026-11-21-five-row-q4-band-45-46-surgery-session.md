# 2026-11-21 five-row q=4 band 45/46 SurgeryJoint session log (高速レーン)

- **Instance**: Vibe 高速レーン (single-owner declaration
  `research/log/2026-11-21-five-row-q4-m45-surgery-single-owner-note.md`,
  commit `59b1251aa7360d48ed0a553212fda9ddd38da9b6`, HEAD-at-declaration `451e0fe8e45d3c699a9b191c0c00f2909a5d9d6f`, work started 2026-11-21 ~22:36Z).
- **Inputs / lineage**: K1209 m39→40 surgery positive control, K1212 published-seed
  census (`research/experiments/five-row-q4-band-41plus-20261121/`, pin `59b1251aa`),
  engine v2 + append_criterion.py + verify_node.mjs + verify_frac.py byte-identical
  re-use (pins in the experiment's digests.txt).

## What happened (chronological, compressed)

1. **Control reproduction diagnosed an engine coverage gap.** Re-running the K1209
   m39→40 control with the published engine reproduced only 14/16 witness stone sets
   (2 per D4 base). Root cause: the engine's 2-addition classes propose an addition z
   only when z lies on a curve through the target cell and a pair of *surviving*
   stones; cells blocked by the joint triple {one survivor, y, z} (both additions plus
   one survivor on one curve) are enumerated by no class. This is the same shape as
   the "case-c" gap K1213 diagnosed on the six-row 56/64 control — here it is closed
   for the five-row lane with an exact method: the mode-(d) candidate pool
   jpool(u, y) = OR over survivors s of curve(u, s, y) makes the pair prefilter
   exact (no junk pairs, no lost candidates).
2. **Surgery45 joint implementation** (new `scripts/surgery45.py`, engine_v2.py
   unmodified, subclass): integer Cramer circle coefficients + isqrt root solving
   (5,000-curve cross-check vs engine cell logic, assert 0 mismatch; a disc=0
   duplicate-curve bug and a degenerate-curve infinite loop (removed-stone coordinate
   ∈ U) were both caught by the cross-check / OOM symptom and fixed by design-safe
   skips). Control: **16/16 set-equality across all 4 D4 images, 2 runs byte-identical**.
3. **m=45 hunt** (budget 2, seeds = published m40-seeds census, all 34 R≥41
   placements): 34 witness records from 10 placements → **17 D4-canonical species**
   (14 stones, rows [3,2,3,3,3]). Speed ~5 s/placement.
4. **w45 census** (scan 60 over the 17 species, 1792 placements, calib gates on
   w45-05 id0 R=46 and w45-00 id0 R=45): R=46 reached by 4 families (w45-05, w45-11,
   w45-13, w45-16; 16 placements), no R=47 in scan. Two calib anchors passed.
5. **m=46 witnesses fixed and verified**: 3-system battery (engine det4 / append
   criterion Fractions / node BigInt Bareiss). All 16 R=46 census placements re-verified
   as 5×46 witnesses by engine (verifymany) and node; criterion witness_widths agree.
6. **m=47 negative searches** (scoped, not absence claims): budget 2 and budget 3
   over all 16 R=46 placements, all negative (~5 s and ~33 s per placement).
   The first run covered 12 placements; after the w45-13 family reading of the census
   it was re-run over all 16 (originals byte-identical, kept in kit archives).
7. **Staircase records**: w45-00/w45-01 witness at widths 26..45 (20 consecutive —
   new (5,4) record, previous 9), w45-16 at widths 30..46 (17 consecutive). Re-verified
   per width in a dedicated re-run (`output/staircase-45.txt`).
8. **Band update**: M_{5,4} ∈ [47, 567] (lower bound 45 → 47, upper bound T_5=567
   unchanged, csv untouched). m=45 and m=46 both witnessed; m=47 UNDETERMINED.

## Session-specific records

- Environment resets killed `/home/user/work/` twice; the working tree was kept under
  the knowledge kit from the start, so nothing was lost. Heavy steps were split so no
  single bash call ran long (2 resets were caused by 300 s-timeout kills).
- Verified numbers before writing the README from the actual JSON/jsonl payloads
  (34 sweep / 10 hit placements / 34 records / 17 species; census 1792 placements,
  16×R=46, 0×R=47; m47 b2/b3 all negative). The README was then corrected against
  the files, not the other way round.
- Two bugs found and fixed during implementation were kept as documentation in the
  script docstring (disc=0 duplicate curves; s==u/s==y degenerate joint curves).
- K1213 (six-row casec) was published mid-session by the parallel lane; verified
  path-disjointness (their files: six-row-q4-m52-casec-20261121; mine: five-row q4
  m45/46) before this push. Latest main at push-time re-fetched per protocol.

## Publications

1. Experiment: `research/experiments/five-row-q4-band-45-46-surgery-20261121/`
   (README, scripts incl. new surgery45.py, configs, outputs incl. census extract,
   verification batteries, digests; fetch-back byte-verified).
2. K item: `research/knowledge/items/K1214-five-row-q4-band-m45-m46-surgery-joint.md`.
3. This log. Knowledge README bullet appended.

## Next (handoff)

- m=47: escalate along other routes (64-scan census for R=46 placements outside the
  current families; budget 3+ joint pool is in place, ~33 s/placement at b3).
- The joint mode-(d) pool closes the 2-addition coverage gap for the five-row engine;
  six-row counterpart of the same fix could be contributed to the case-c lane as a
  follow-up (K1213's engine is a separate implementation; do not touch their files).
- Staircase: the 20-width record set (maxx=25) suggests looking for low-maxx
  width-generic rows [3,2,3,3,3] families; a structural question, not a sweep.
