# Session log 2026-11-21: six-row q=4 (6,4) m47-witness surgery lane — translation/census/surgery chain to m=51, band M_{6,4} in [52,1113]

Lane: `(6,4) m=47 witness constructive surgery` fast lane, declared in
`2026-11-21-six-row-q4-m47-witness-surgery-single-owner-note.md`
(commit `ad2c411`, 2026-11-21T20:24Z, HEAD-at-declaration `b19d79a6`).
Outcome: **published as K1211 + experiment
`six-row-q4-m47-m51-witness-chain-20261121`** (this session's pushes).
Value change: M_{6,4} lower bound 47 -> 52 (band m=6..51 witnessed;
upper T_6=1113 unchanged; `mwq_stabilization.csv` untouched, K1201
precedent).

## Order of events (times UTC, approximate)

1. **20:2x Declaration + kit fetch.** Latest main, AGENTS.md, knowledge
   README, prior K1209 lane format fetched; published (6,4) band
   witnesses m=41..46 (rowY0 SAT witnesses + m=46 free-column-append
   record, `four-row-q4-q5-frontier-20261115` batches) and the K1209
   control material fetched byte-exact into a local kit.
2. **20:3x-20:4x clean-room engine v1.** Verification (det-4 +
   line/circle registry), census, bounded surgery; m47 seeds from the
   m46 translation family first found by census. **Execution
   environment reset destroyed the work directory (engine v1 and all
   raw outputs lost).** Nothing from that phase was published.
3. **20:4x-21:0x engine v2 clean-room rebuild + full re-derivation.**
   All numbers below are v2-only. Sequence of discovery within the
   re-derivation:
   - selftest battery (published m=46 seed witness + calibration
     R=46@(46,0) at the published position, published K1209 m40 16-witness
     battery PASS, tamper flags) — PASS;
   - 5-seed census (m41/42/43/44/m46, 1708 placements): m41..44 families
     do not extend past their own width; **m46 family reaches R=47 in 4
     placements (id/V shift5, H/HV shift6) -> four width-47 witnesses,
     translation-only (no stone edit needed: the frontier pattern
     survives a 1-column right translation / mirror+translation)**;
   - 47->48 surgery (1R1A/2R1A/2R2A): id/V seeds 0; H/HV seeds 2 each
     -> **W1, W2 + V-images, four width-48 witnesses** (all from the
     2R2A class, same as K1209's fertile class);
   - W1/W2 census (680 placements): **W1 reaches R=51 in 4 placements**
     (id/V shift6, H/HV shift9; consecutive staircase R=49/50/51),
     W2 stops at 48 -> **widths 49, 50, 51 witnessed**; the id/V W1
     stone set witnesses ten consecutive widths 42..51 (widest
     single-set staircase recorded for (6,4));
   - intermediate bounded surgery chain attempts at R=48..50 seeds
     (16 config runs, remove<=2/add<=2 + remove<=3/remove<=2 variants):
     0 witnesses — the 48->49..51 advance came from **translation, not
     surgery**; those raws were kept out of the publication set and are
     noted here (they add nothing beyond surgery-52esc's negative scope);
   - 51->52 escalation (4 R=51 seeds, classes 1R1A/2R1A/2R2A/3R1A/3R2A,
     incl. 3R2A pairCandidates ~2.27M/seed): **0 witnesses** — m=52
     UNDETERMINED;
   - K1209 positive control (5x39->40, 4 D4 images of the m=39 seed):
     **56/64 rediscovered, all 56 members of the published set**; the 8
     missing hits diagnosed (then re-derived independently at
     publication time, see below) as **case-c-only**: exactly one empty
     cell each whose every blocking curve contains exactly one
     surviving stone + both added stones.
4. **21:0x three-family verification.** witness bank (20 items) and
   control bank (83 items = 64 raw + 16 distinct + 3 seeds) PASS 20/20
   and 83/83 on engine det4 family, Fraction center-radius family
   (`verify_frac.py`), and BigInt Bareiss family (`verify_node.mjs`).
   Tamper controls fail loudly as designed.
5. **21:0x-21:1x determinism.** census, w48-census, surgery-47to48,
   surgery-52esc, surgery-control re-run pairs byte-identical (md5
   pairs recorded in the experiment digests).
6. **21:1x-21:2x pre-publication audit** (session-continuation pass):
   re-fetched latest main; confirmed K1209 format; confirmed **K1210 is
   name-reserved in prose by another in-flight lane
   (`four-row-q6-m46-reconcile-20261121` README)** — its item does not
   exist yet, but to avoid needless renumbering friction at integration
   time this lane publishes as **K1211** (AGENTS.md allows provisional
   numbers; integration renumbers on real collision). Re-derived the
   case-c diagnostic independently (`output/casec-recheck.json`:
   8/8 missing hits have exactly 1 case-c-only cell, survivor counts
   exactly {1}). Re-confirmed all R=47/R=51 placements, staircases,
   and the 56-in-64 subset relation at stone-set level.
7. **21:2x push.** Before pushing: latest main re-fetched (collision
   protocol). Pushed experiment dir + session log + K1211 + knowledge
   README bullet; fetch-back byte verification performed.

## Acceptance conditions vs outcome (honest table)

| Condition (owner note) | Outcome |
|---|---|
| clean-room engine, no repo code | met (engine v2, stdlib only) |
| positive control = K1209 m40 surgery fully reproduced at stone-set level | **NOT met in full**: 56/64, all 56 subset of published; gap fully diagnosed as the case-c coverage class (1 cell per missing hit); complete 83-item published bank re-verified 20/20+83/83 by three families |
| >= 2 independent integer verification families | met (3 families, zero disagreement) |
| determinism: 2 runs byte-identical | met (all five main output pairs + control pair byte-identical) |
| negatives = finite bounded-neighborhood records only | met; 2R2A/3R2A negatives additionally scoped by the case-c coverage restriction |
| no universal claim, csv unchanged | met |

Publication proceeded despite the partial control because every
positive claim is verified by complete from-scratch checks (not by the
restricted search), the published bank of the control target passes all
three families, and the gap is understood at the single-cell level.

## Failure / limitation record

- Execution-environment reset destroyed engine v1 and its raw outputs;
  everything was re-derived from scratch with engine v2 and re-verified.
  No pre-reset raw is claimed anywhere.
- engine v2 does not implement case-c pair coverage and does not
  implement remove-3/add-3; the 51->52 negative is scoped accordingly.
- The intermediate R=48..50 surgery chain found nothing; publishing
  only the census translation path keeps the negative raws minimal
  (noted here; they are reproducible from the published configs'
  methodology by changing m_target).
- m=41..44 seeds in the census are side observations only; their
  published sources (rowY0 SAT witnesses) were inputs, not claims.

## Next work (handoff)

- The case-c pair-coverage class can be added to a future engine for a
  stronger 51->52 sweep (the current negative covers only the
  >=2-survivor coverage scope; 3R3A not implemented).
- The W1 staircase suggests scanning the m46-family/W1-family census
  for other mirror/parities as a cheap source of further widths, but
  R=51 placements stop at 51 within scan=120; new widths need new
  structure.
- Alternative: SAT class-split sweep at m=47 remains the OOM lane's
  domain (`six-row-q4-m47-rowY0-oom-20261115`); this lane does not
  touch it.
