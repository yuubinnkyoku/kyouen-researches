# six-row q=4 (6,4) witness m=47..51 chain: translation census, bounded-edit surgery, band update M_{6,4} in [52, 1113]

Date of experiment: 2026-11-21 (engine cleaned-room and re-derived twice after
execution-environment resets; every published number below comes from the
final deterministic engine and was byte-reproduced a second time).

Lane: standard-rule fixed-width q=4 family, six-row band ("(6,4) m=47
witness constructive surgery" fast lane).
Single-owner declaration:
`research/log/2026-11-21-six-row-q4-m47-witness-surgery-single-owner-note.md`
(commit `ad2c411`, declared 2026-11-21T20:24Z at HEAD `b19d79a6`).
Acceptance conditions: clean-room engine (no repo code), positive control =
reproduction of the K1209 (5,4) m=39->40 surgery at stone-set level,
>= 2 independent integer verification families, byte-identical determinism
run on the main outputs, negatives scoped as finite bounded-neighborhood
records only, no universal claim, `mwq_stabilization.csv` unchanged
(K1201 precedent).

## Status of the acceptance condition on the positive control (read first)

The positive control was **substantially, not completely, reproduced**:
engine v2 rediscovers **56 of the 64 published K1209 hits** (14 per D4
image, 4 images; all 56 are members of the published set, verified at
stone-set level). The 8 missing hits are not engine "wins" lost nor
published errors: a publication-time diagnostic
(`output/casec-recheck.json`) shows each of the 8 missing sets has exactly
one empty cell whose **every** blocking curve contains exactly one
surviving seed stone together with **both** added stones. engine v2's
pair-addition enumeration (classes 2R2A/3R2A) only enumerates blocking
coverage through >= 2 surviving stones, so this coverage class (case c)
is unreachable for it. Consequences, stated honestly:

- every **positive** result below is unaffected: each witness was checked
  from scratch by the engine's full-board verifier and by two further
  independent families (see Section 5), not by the restricted search;
- every **negative** result below is stronger scoped: the single-add
  classes 1R1A/2R1A/3R1A are complete (a blocking curve of an added-only
  cell needs >= 2 stones besides the cell, and with one addition these
  are 3 survivors or 2 survivors + the addition, both enumerated), but
  the pair classes 2R2A/3R2A refer only to coverage through >= 2
  surviving stones; case-c-only witnesses may exist outside that scope;
- the complete published K1209 bank itself (64 raw hits + 16 distinct
  sets + 3 seeds = 83 items) **passes all three verification families**
  (83/83), so the gap is a search-restriction gap, not a disagreement
  about what a witness is.

## Results (machine-verified finite claims; no universal claim beyond them)

### 1. R(S) translation census of the published (6,4) band-top witnesses

`census` mode (exact integer triple-curve bitmask registry, D4 images
x shifts, scan 120, exact integer arithmetic; the expected calibration
values are asserted as a fail-closed gate).

Seeds: the published (6,4) band witnesses m=41/42/43/44
(`four-row-q4-q5-frontier-20261115` batches, records in
`configs/cfg-census.json`) and the published m=46 witness
(constructive free-column append of the m=45 witness, same experiment
family). 1708 placements.
Calibration: the m=46 witness at its published position
(id image, shift 4) has R=46, first unblocked cell (46,0) — matching the
published record, so m=47 was a **true frontier**.

- The m=41..44 seeds' families reach at most R=41/42/43/44 respectively:
  none extends a single width past its published board.
- The m=46 witness family reaches **R=47 in exactly 4 placements**
  (id/shift 5, V/shift 5, H/shift 6, HV/shift 6; all translation-only,
  no stone edit): **four width-47 witnesses**
  (`output/witness-bank-20.json`, tags m47-id-s5 / m47-h-s6 /
  m47-v-s5 / m47-hv-s6), each 17 stones, rows [2,3,3,3,3,3]
  (single-deficient, deficient row 0 or its vertical mirror row 5).

### 2. 47->48: bounded-edit surgery (remove<=2 / add<=2)

Classes 1R1A (remove-1/add-1), 2R1A, 2R2A on the 6x48 board, seeded from
the four width-47 placements. Deterministic, seedless.

- 1R1A / 2R1A: 0 witnesses on all four seeds (complete classes).
- 2R2A: 2 witnesses from the m47-h-s6 seed (W1, W2) and 2 from the
  m47-hv-s6 seed (their V-images W1v, W2v); 0 from the id/v seeds
  (case-c scope applies to this negative).
- **Four width-48 witnesses**, 17 stones, single-deficient (rows
  [2,3,3,3,3,3] or its vertical mirror)
  (`output/witness-bank-20.json`, tags m48-w1/w1v/w2/w2v).
  Note: the width-47 translation family itself does not cover width 48
  (its placements stop at R=47), so the edit was genuinely needed here.

### 3. W1/W2 translation census: one pattern reaches R=51

Same census on the four width-48 witnesses (W1/W2 and their V-images,
680 placements over D4 x shifts):

- W1 family: four placements reach **R=51** (id/shift 6, V/shift 6,
  H/shift 9, HV/shift 9) — consecutive placements of the same pattern
  reach R=49, R=50, R=51.
- W2 family: stops at R=48.
- **Therefore widths 49, 50, 51 are witnessed** by the four W1-family
  placements (12 bank entries w51-{id,h,v,hv}-m{49,50,51}; the id/V
  forms have maxx=41, i.e. a single stone set witnesses **ten
  consecutive widths 42..51** — the widest single-set staircase recorded
  for (6,4); the H/HV forms witness widths 45..51).

### 4. 51->52: bounded escalation, negative (scoped)

remove<=3 / add<=2, classes 1R1A/2R1A/2R2A/3R1A/3R2A, seeded from the
four R=51 placements on the 6x52 board:

- **0 witnesses** in all classes on all four seeds
  (`output/surgery-52esc-*.json`).
- Scope: 1R1A/2R1A/3R1A complete as in Section "Status"; 2R2A/3R2A cover
  only blocking through >= 2 surviving stones (case c not enumerated);
  remove-3/add-3 *not implemented* (the declaration's escalation budget
  was remove<=3/add<=3; the 3R2A class was run, 3R3A was not). No
  absence claim at m=52: **UNDETERMINED**.

### 5. Independent verification (three families) and determinism

Witness bank (20 items: 4 x m47, 4 x m48, 4 images x m49/m50/m51) and
control bank (83 items: the complete published K1209 m=40 material):

1. engine_v2 `verify_config` (integer 4x4-determinant degenerate
   concyclicity + exact line/circle registry on the full m-column board),
2. `verify_frac.py` (Fraction center-radius circle / cross-product line
   family: safety by perp-bisector-solved circles, blocking with early
   exit, tamper control by add-one-stone-at-a-blocked-cell),
3. `verify_node.mjs` (BigInt 4x4 Bareiss determinant + BigInt blocking,
   pure ECMAScript).

- witness bank: **20/20 PASS on all three families**
  (`output/verify-bank-{engine,frac,node}.json`).
- control bank: **83/83 PASS on all three families**
  (`output/verify-control-{engine,frac,node}.json`).
- tamper controls: add-stone tamper fails loudly on every family;
  moved-stone tamper caught by the engine selftest
  (`output/selftest.json`: tamper_m40_fails, unsafe_flagged).
- determinism: every main output was computed twice from scratch
  (including one run after a full execution-environment reset during the
  session); the pairs are **byte-identical** (census-5seeds.json ==
  its re-run, census-w48.json == its re-run, surgery-47to48 ==
  re-run, surgery-52esc == re-run, surgery-control-m40 == re-run);
  md5 pairs and sha256 pins of every published file are recorded in
  `output/digests.txt`.

### 6. Band update (the only value change)

With widths 6..46 published (K1207 re-verified bank m=6..31;
`four-row-q4-q5-frontier-20261115` / band-extension witnesses m=32..46;
m=47 sat behind the SAT CNF RAM wall of
`six-row-q4-m47-rowY0-oom-20261115`), this lane adds widths **47, 48,
49, 50, 51 constructively**:

**M_{6,4} in [52, 1113]** (lower bound = width 51 witnessed; upper bound
T_6 = 1113 = B_max(6)+1 from the K1207 demand-supply inequality,
unchanged). `mwq_stabilization.csv` remains untouched; the value change lives
here, in the session log, and in knowledge item K1211.

## What this is not

- No completeness claim for the width-47..51 witness populations: only
  the declared translation families and bounded-edit neighborhoods were
  searched (and 2R2A/3R2A only in the >= 2-survivor coverage scope).
- No existence or absence claim at m=52 or beyond: UNDETERMINED.
- The positive control reproduction is 56/64, not 64/64; the gap is
  fully diagnosed (case c) and recorded above.
- checked/candidate counts are machine effort, never wins or losses.
- The standard 11x11 empty board, two-stone roots {49,60}/{59,60},
  S2 {59,60}, classes 1/2/4 are untouched by this lane and remain
  UNKNOWN.
- The K1207 inequality, the published (6,4) band witnesses m<=46 and
  the K1209 control material are used as verified inputs; not re-derived
  here. The K1209 publication itself is not modified by this experiment.

## Honesty record

- Two execution-environment resets occurred during the session; the
  first destroyed the pre-reset engine v1 and its raw outputs. Rather
  than publish unregenerated numbers, the engine was rebuilt clean-room
  (engine v2) and every number in this README was re-derived, then
  byte-reproduced a second time. No pre-reset raw file is claimed.
- The reach convention and the census shift convention were pinned by
  asserting the published m=46 calibration values inside the engine
  (fail-closed: a wrong convention fails the census run). The K1209
  control battery caught search-scope discrepancies (56/64, the case-c
  class) before any negative claim was staked; all negatives above are
  scoped accordingly.
- The single-deficiency structure (rows [2,3,3,3,3,3], 17 stones) is
  preserved by every published witness; saturation (18 stones, all rows
  3) loses deficiency, which is why pure-add surgery is impossible
  here too.

## Reproduction

```
python3 scripts/engine_v2.py selftest > output/selftest.json
python3 scripts/engine_v2.py census   configs/cfg-census.json        > output/census-5seeds.json
python3 scripts/engine_v2.py census   configs/cfg-census-w48.json    > output/census-w48.json
python3 scripts/engine_v2.py run      configs/cfg-surgery47to48-h_s6.json > output/surgery-47to48-h_s6.json   # etc.
python3 scripts/engine_v2.py run      configs/cfg-surgery52esc-id_s6.json  > output/surgery-52esc-id_s6.json  # etc.
python3 scripts/engine_v2.py run      configs/cfg-control-m40-id.json     > output/surgery-control-m40-id.json
python3 scripts/engine_v2.py verifymany output/witness-bank-20.json  > output/verify-bank-engine.json
python3 scripts/verify_frac.py        output/witness-bank-20.json    > output/verify-bank-frac.json
node    scripts/verify_node.mjs       output/witness-bank-20.json    > output/verify-bank-node.json
# same triple for output/control-bank-83.json -> verify-control-*.json
# the census/surgery re-runs must be byte-identical (md5 pairs in digests.txt)
sha256sum -c output/digests.txt
```

## Structure

```
README.md
scripts/engine_v2.py          clean-room engine (verify/census/surgery/selftest, deterministic)
scripts/verify_frac.py         verifier family 2 (Fraction center-radius)
scripts/verify_node.mjs        verifier family 3 (BigInt Bareiss determinant)
configs/cfg-census.json        seeds m41/42/43/44/m46 + asserted calibration
configs/cfg-census-w48.json    seeds W1/W2 (+V images)
configs/cfg-surgery47to48-*.json   4 seeds, classes 1R1A/2R1A/2R2A
configs/cfg-surgery52esc-*.json    4 seeds, classes up to 3R2A
configs/cfg-control-m40-*.json     K1209 positive-control seeds
output/selftest.json           battery incl. tamper + calibration
output/census-5seeds.json      1708 placements, R<=47; 4 placements at R=47
output/census-w48.json         680 placements, R<=51; 4 placements at R=51
output/surgery-47to48-*.json   W1/W2 (+V images) from h/hv seeds; id/v negative
output/surgery-52esc-*.json    all negative (scoped)
output/surgery-control-m40-*.json  56/64 rediscovery (see Status section)
output/casec-recheck.json      diagnostic: the 8 missing hits are case-c-only
output/witness-bank-20.json    the 20 published witness stone sets
output/control-bank-83.json    the 83 K1209 control items
output/verify-bank-*.json      20/20 x 3 families
output/verify-control-*.json   83/83 x 3 families
output/digests.txt             sha256 pins of every file above
```
