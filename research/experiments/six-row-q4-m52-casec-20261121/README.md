# Six-row q=4: case-c-complete bounded-edit surgery, 47→48 census completion, and the negative m=52 escalation census

Date: 2026-11-21
Status: EXPERIMENT (complete finite enumerations, published-positive controls, deterministic replays).
Claim update: **none.** M_{6,4} ∈ [52, 1113] is UNCHANGED (K1211). m = 52 witness existence: **UNDETERMINED**
(this experiment records a complete finite negative edit-neighborhood census around the four
R=51 witness configurations; it makes no claim that M_{6,4} > 52 and no claim about witnesses
unrelated to those seeds).
Standard 11×11 status: unchanged, UNKNOWN. mwq_stabilization.csv: not modified.
Lane: fast lane, single-owner declaration bab006adc (Part B scope: (6,4) m=52 case-c-complete
escalation + the two published positive controls), commit
research/log/2026-11-21-five-row-q4-band-41plus-and-six-row-q4-m52-casec-single-owner-note.md.
Non-goals (declared): (6,5)/(6,6)/(6,7) fronts, (7,4) band, 11×11 heavy jobs.

## 1. The engine: surgery_gen2_1.js (closes K1211's case-c gap)

Class-by-class bounded-edit surgery, general in (w, m, q): given a safe+maximal seed witness
S on the board w×m (seed has exactly one uncovered cell, so S witnesses widths maxx+1..m-1),
enumerate all removals R ⊂ S with |R| ≤ 3 and all added cells A with |A| ≤ 2 on the target
board w×m_target, and certify each S2 = (S\R) ∪ A by a COMPLETE on-board check
(rows cap, complete safety over S2, complete maximality over every empty cell: base blocking
curves that survive R, plus every line/circle through the cell and an added stone).
Curve engine (canonLine / circleIR / parseKey / fastOnLine / fastOnCircle / Board) reused
VERBATIM from the published K1209 surgery.js
(sha256 0410d787a53ffadda3bc44b9c31b423ce4a38ab4798b28e279230cfb73ab7e25).

Completeness classification (q=4, |A|≤2; the prefilter is a sound-rejection stage only,
every passer re-certified by the complete check above). For a needed cell u (a cell whose
every base blocking curve lost a stone to R), a covering curve of S2 through u holds ≥3
stones of S2 and must contain an added cell, so with |A| ≤ 2 exactly one of:

1. occupy: an added cell IS u;
2. strong: a curve with ≥2 SURVIVING seeds containing an added cell
   (precomputed per u from all seed-pair lines/circles through u with ≥2 seed stones);
3. k1: a curve through u holding both added cells, ≥2 base seed stones of which ≥1 was
   removed (k = 1 surviving): stones = a + b + 1 = 3 (K1211 called the surviving-witness
   instances of this family "case c");
4. FINAL case-c (gen2.1): the covering curve is determined by (u, a, b) ALONE and holds
   exactly ONE surviving seed stone and NO removed stone: the circumcircle of u,a,b
   (or the line u,a,b) is then not a ≥2-seed-stone base curve, so it never enters the
   precomputed per-cell curve table; the kA=2 sweep tests it on the fly
   (stones = a + b + ≥1 surviving = ≥3 iff ≥1 surviving seed lies on curve(u,a,b)).

Classes 1R1A / 2R1A / 3R1A (kA=1) were already complete without branch 4: a kA=1 covering
curve through u needs a + ≥2 surviving seeds, which is exactly branch 2.
This branch-4 omission was the ONLY incompleteness of the pre-fix gen2 engine (superseded
runs recorded below) and it reproduced, from the construction side, the same 2-of-16 orbit
loss K1211's published engine showed on the K1209 control (56/64): the gen2 pre-computed
curve table CUR(u) admitted only curves through ≥2 seed stones, so a case-c circle
through (u, a, b, exactly one surviving seed) was invisible to it.
`scripts/diag-casec-trace.js` prints the two certificate curves closing the lost orbits:

- K1209 published orbit 1 (id base): needed cell [39,1] is ONLY covered by circle
  (-71,-11,1258,1) through adds (32,1),(37,0) and surviving seed (34,0);
- K1209 published orbit 15 (id base): needed cell [14,1] is ONLY covered by circle
  (-156,8,1585,3) through adds (37,4),(38,1) and surviving seed (15,4).

Determinism: fixed iteration order, pure integer arithmetic, no randomness; re-runs are
byte-identical (verified, see §5).

## 2. Control (a): K1209 five-row m39→40 — 64/64 exact reproduction

Seed: the published K1209 m39 witness (s5x39q4, 14 stones, identical to K1211's
cfg-control-m40-id.json seed; the H/V/HV control seeds are its D4 images, byte-checked),
target board 5×40, remBudget 2 (classes 1R1A/2R1A/2R2A). Configs: configs/run-ctla-{id,H,V,HV}.json.
Outputs: output/ctlA21-{id,H,V,HV}.json. tried per base:
1R1A 2604, 2R1A 16926, 2R2A 1,565,655 (= C(14,2)·C(186,2)), passFrontier 131, witnesses 16 per base, all 2R2A.

- Per base: the 16 certified stone sets equal the 16 published distinct width-40 witnesses
  (research/experiments/five-row-q4-witness-band-40plus-20261121/, distinct-m40-witnesses.json),
  EXACTLY, as unordered sets: 0 missing, 0 extra (base id).
- Across the 4 D4 bases: 64 certified hits; the union of raw stone sets has 64 members and
  equals exactly {D4 images of the 16 published sets} (K1209's published 64-hit family).
- The gen2.1 engine therefore fully reproduces K1209's published census
  (K1211's published engine reproduced 56/64; the 8 missing hits were exactly orbits 1 and
  15, the two FINAL case-c orbits above).

## 3. Control (b): K1211 six-row 47→48 — 4/4 reproduction and census completion

Seeds: the four published K1211 m47 surgery seeds (cfg-surgery47to48-{id_s5,v_s5,h_s6,hv_s6}),
target board 6×48, remBudget 2. Configs: configs/run-ctlb-*.json. Outputs: output/ctlB21-*.json.
tried per seed: 1R1A 4607, 2R1A 36856, 2R2A 4,975,560.

- h_s6 / hv_s6: 2 witnesses each; the four stone-sets equal the published m48-w1, m48-w2,
  m48-w1v, m48-w2v exactly (0 extra).
- id_s5 / v_s5: 0 witnesses — and this is now PROVEN at census level: with the case-c branch,
  passFrontier increased (5→5+ vs pre-fix; h_s6/hv_s6 18→26) but no additional pair passed
  the complete certification, so the published 4-witness census holds with case-c closed.

3R extension (beyond the published remBudget; classes 3R1A/3R2A on the same seeds):
configs/run-ctlb3R-*.json, outputs output/ctl48x3R-*.json. tried per seed:
3R1A 184,280 (= C(17,3)·271), 3R2A 24,877,800 (= C(17,3)·C(271,2)). Witnesses: 0 on all four seeds.
Consequence: the complete ≤3-remove/≤2-add bounded-edit census of the K1211 47→48 surgery
contains EXACTLY the 4 published witnesses (all 2R2A), and no 3R-road witness exists from
these seeds.

## 4. The negative m=52 escalation census (Part B main experiment)

Seeds: the four R=51 witness configurations of the published K1211 witness bank
(witness-bank-20.json tags w51-id-m51, w51-v-m51, w51-h-m51, w51-hv-m51; 17 stones each =
K1211's roadmap surgery52esc seeds), target board 6×52, classes 1R1A/2R1A/2R2A/3R1A/3R2A
(remBudget 3 as declared). Configs: configs/run-m52esc-{id,v,h,hv}.json.
Outputs: output/m52esc-{id,v,hv,h}.json. On the 6×52 board E = 52·6−17 = 295 empty cells.

Complete enumeration per seed (all tried classes are full class enumerations):

| class  | tried per seed  | product form            | witnesses |
|--------|-----------------|-------------------------|-----------|
| 1R1A   | 5,015           | 17·295                  | 0 |
| 2R1A   | 40,120          | C(17,2)·295             | 0 |
| 2R2A   | 5,897,640       | C(17,2)·C(295,2)        | 0 |
| 3R1A   | 200,600         | C(17,3)·295             | 0 |
| 3R2A   | 29,488,200      | C(17,3)·C(295,2)        | 0 |

35,631,575 candidates per seed, 142,526,300 over the four seeds.
passFrontier: 2R2A id/v: 3, h/hv: 1; 3R1A: 0; 3R2A: 0; every frontier passer failed the
complete certification (0 witnesses). Each seed: n=17, rows=(3,3,3,3,3,2) or (2,3,3,3,3,3),
safe (ml=3, mc=3), exactly 1 unblocked cell.

RESULT (finite negative record, scoped): **no (6,4) witness at width 52 exists within
edit distance ≤3 removals and ≤2 additions of ANY of the four published R=51 witness
configurations w51-{id,v,h,hv}-m51.** In particular the K1211 roadmap escalation step
m51→m52 fails for every declared bounded-edit class. This does NOT decide m=52 witness
existence in general (other seeds, larger edit budgets, or non-surgery constructions remain
open); M_{6,4} stays [52, 1113] with m=52 UNDETERMINED.

## 5. Determinism, validation, and superseded history

- Determinism: full re-runs of control (a) id base and the m52esc id seed produced
  byte-identical output files (cmp clean; the engine embeds no timestamps and no randomness).
- Validation chain of the negative census: (i) the curve engine functions are byte-verbatim
  from the published K1209 surgery.js (sha256 above); (ii) positive control (a) reproduces
  K1209's published 16-orbit census exactly (§2); (iii) positive control (b) reproduces
  K1211's published 4-witness census exactly (§3); (iv) the complete per-candidate
  certification (rows/safety/maximality over the whole target board) is exercised by those
  68 positive certificates under the identical code path as the 142.5M negatives.
- Superseded pre-fix gen2 runs (kept out of this directory; recorded here as the honesty
  trail): the pre-fix engine found 14/base (56/64) on control (a) — the same 8 missing hits
  as K1211's published engine — and 4/4 on control (b); its m52 sweep is superseded by the
  gen2.1 census above (the pre-filter missing branch could only RESTORE candidates, so
  the pre-fix m52 negative is implied a fortiori by this census, and is not used).

## 6. Files

- scripts/surgery_gen2_1.js — the engine (Node >= 18, single file, stdin-free):
  `node surgery_gen2_1.js <config.json> <out.json>`.
- scripts/diag-casec-trace.js — prints the two FINAL case-c certificate curves (§1).
- configs/run-*.json — 16 run configs (4 control-a bases, 4 control-b seeds, 4 control-b
  3R-extension seeds, 4 m52 escalation seeds). Each states w, m, q, seed, class list, label.
  Seed provenance: control (a) = K1209 s5x39q4 witness + D4 images (= K1211 cfg-control-m40-*),
  control (b) = K1211 cfg-surgery47to48-*, escalation = K1211 witness-bank-20 w51-*-m51.
- output/*.json — the 16 run outputs (counts, seeds, witnesses with rem/add/stones/rows).
- digests.txt — sha256 of every file in this directory.

Reproduction: `node scripts/surgery_gen2_1.js configs/run-m52esc-id.json /tmp/out.json`
(deterministic; expect witnesses=0 and tried counts as in §4).
