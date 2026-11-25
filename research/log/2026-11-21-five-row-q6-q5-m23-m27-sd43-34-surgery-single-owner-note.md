# 2026-11-21 five-row q6/q5 m=23/m=27 sd<=(4,3)/(3,4) partial sweep — single-owner declaration

Declaration time: 2026-11-21T22:40Z (declaration-time main HEAD
`5c4cfca9f267bb849475ae25d9f03e3f7a182ec0`, the in-flight m21/m25-species
follow-up declaration; this lane is disjoint from it).

## Scope (single owner, this lane only)

Extends the completed sd<=(3,3) frontier-surgery campaign (commit `c2010307`,
`five-row-q6-q5-m23-m27-sd6-surgery-20261121`) to the adjacent bounded-edit
classes:

1. `(5,6)` target `5x23`, seed = the published 24-stone m=22 witness
   (K0852, `seed_5x22_q6.json`), budgets (maxP,maxRm) = **(4,3)** and **(3,4)**,
   targetMax = 24.
2. `(5,5)` target `5x27`, seed = the published 19-stone m=26 witness
   (`seed_5x26_q5.json`), budgets **(4,3)** and **(3,4)**, targetMax = 19.

Machinery: `surgery4.js` md5 `7dc40fc0f08150692d64241d0c6c4029` + `sat.js`
`0cc6021a4e523a0d7f4d5e0f5f5d40c` + `census4_check.js`
`dadbeae1b02ad2a9650c6ce86021fb9c`, same enumeration-class statement as the
parent campaign (removals only on deficit curves with full deficit coverage;
free removals out of scope; no global absence claim).

Placement grid: **class representatives only**, per the machine-verified
rectangle-symmetry class reduction lemma of the parent campaign (id@t reps:
3 classes t=0..2 for 5x23 span-21, 8 classes t=0..7 for 5x27 span-20), plus
one full-class cross-check member per campaign per budget (q6: V@2 in class
t=0; q5: HV@7 in class t=0). The lemma is budget-independent, so no other
members are run.

## Acceptance conditions

1. Script integrity: the three scripts re-verified by md5 against the
   published pins before any run; census gates (5,12,6)=212 / (5,15,5)=629 /
   (5,23,6)=996 / (5,27,5)=2355 re-run PASS.
2. Seed sanity: `sat_verify.js` + `safety_only.js` + `verify_general.py` PASS
   on both seeds on their home boards; tamper controls still FAIL.
3. Positive self-completion control (minus-2 seed, (2,2) budget, home board)
   re-finds the published witnesses before the sweeps.
4. Determinism: one representative re-run per campaign per budget; all
   logical invariants (nP/nPpruned/nRmLeaves/nSafe/nMaximal/nWitness/
   nEmpty/nTprime) must agree (elapsedMs excepted).
5. Any witness found: halt the campaign, three independent verifications
   before any bound statement; csv bounds change only then. All-negative:
   bounds unchanged, csv note/source update only, no new K item (parent
   precedent).
6. Fail-closed: a crash, unexpected pruning, or a cross-check disagreement
   halts the campaign and records IN FLIGHT; no partial absent-claims. A run
   that exceeds the single-process wall budget (~280s, shared 2-core host)
   is recorded **budget-limited INDETERMINATE** and is not counted as a
   negative.

## Non-goals

- No m=21/m=25 species campaigns (in-flight lane `5c4cfca9`), no (4,4)
  m=35/36, no (5,4) m>=41, no six-row m52 (all other lanes'), no SAT/kissat,
  no 11x11, no budgets beyond (4,3)/(3,4), no free-removal classes, no
  global absence claims.
