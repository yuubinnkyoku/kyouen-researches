# 2026-11-21 five-row q6 m=21-species / q5 m=25-species m=23/m=27 sd<=6 surgery — single-owner declaration

Declaration time: 2026-11-21T22:25Z (declaration-time main HEAD `c20103072e002b46e7aac062590dccf5738e3054`, my own completed frontier-surgery push).

## Scope (single owner, this follow-up lane only)

Two witness-species-extension bounded-surgery campaigns, complementing the
completed m=22-witness/m=26-witness campaigns (commit `c2010307`,
`five-row-q6-q5-m23-m27-sd6-surgery-20261121`):

1. `(5,6)` target `5x23`, seeds = the full published m=21 witness species:
   the K0815 24-stone 5x21 witness (`five-row-q6-m22-surgery-20261115`
   ctrl/seed_w56_21.json) plus its two published sd<=2 variants
   ((10,2)->(11,2) and (10,2)->(12,2), `verify_variants_5x21.json`).
2. `(5,5)` target `5x27`, seed = the published m=25 19-stone witness
   (`five-row-q5-m26-extend-20261115` output/w25.json).

Machinery: `surgery4.js` md5 `7dc40fc0f08150692d64241d0c6c4029` + `sat.js`
`0cc6021a4e523a0d7f4d5e0f5f5d40c`, budgets maxP=3 maxRm=3, targetMax
= full-capacity minus 1 (24 q6 / 19 q5), same class statement as the
parent experiment (R on deficit curves only; free removals out of scope,
no global absence claim).

Placement grid: per species, per the machine-verified rectangle-symmetry
class lemma of the parent experiment (class reps id@t; 3 classes for
5x23 span-21 seeds, 8 classes for 5x27 span-20 seeds), each class run at
its id representative plus one full-class H/V/HV cross-check per campaign.

## Acceptance conditions

1. Every seed verified on its home board by sat.js verifyConfig + the
   corrected independent Python Fraction verifier + safety_only.js.
2. Census gates already published at (5,23,6)/(5,27,5) = 996/2355
   (parent experiment output/census4_gates.txt); re-run once here.
3. Positive self-completion control per species (minus-2 seed, home
   board, (2,2) budget) re-finds the published witness set.
4. Any witness found: three independent verifications before any bound
   statement; csv bounds unchanged otherwise (note/source only).
5. Fail-closed: if a run crashes, prunes unexpectedly, or any cross-check
   class member disagrees with its representative, the campaign halts and
   records IN FLIGHT; no partial absent-claims.

## Non-goals

- No (4,4) m=35/36, no (5,4) m>=41, no six-row m52 (all other lanes'),
  no SAT/kissat, no 11x11, no sd>6 budgets, no new K item for negatives.
