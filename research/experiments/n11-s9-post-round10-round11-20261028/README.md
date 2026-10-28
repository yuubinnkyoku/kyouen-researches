# N11 round11: 32 selected S9 roots, exact terminal certificates

The 32 roots were selected by the frozen post-round10 proof-only replan against the **83** outstanding edges of the conditional 14-root S7 plan. The selection SHA-256 is `9392e37f5a8381c49094b2fff32a2c8c9ac26122e90dbc9066951f4ae7806227`. Only this selection was explored.

## Reproducible result

- **4 WIN9**, each with every legal S10 child independently terminal-WIN; **28 LOSS9**, each with a fixed terminal-LOSS S10 witness.
- **822** legal S10 edges across the selected 32 S9 roots; **96** universal S10 WIN obligations for the four WIN9 roots.
- Discovery stopped on the first LOSS10 child of each LOSS9 root. It tested **320** distinct S10 terminal positions, with **57,384** recursive terminal states **per geometry**.
- **280** canonical S9 parents are derivable from the 28 fixed LOSS10 witnesses. This is a closure size, not a claim of 280 globally new verdicts; other certificates may overlap.
- **0** WIN9/LOSS9 conflicts within this fixed batch. No two-stone root was closed.

The terminal computation uses two independently implemented exact integer geometries: a 3×3 difference determinant and a 4×4 Bareiss determinant. The complete S9→S10 boundary is checked in both. For each S10 terminal position, the two minimax solvers must agree on outcome, legal move count, and recursion state count. The frozen witness bytes encode `255` for a WIN9 universal proof and otherwise the lexicographic index of one LOSS10 child. The certificate also fixes the SHA-256 of the selected roots, witness bytes, and 280 canonical LOSS9 parents.

From repository root:

```sh
node research/experiments/n11-s9-post-round10-round11-20261028/prove.js
node research/experiments/n11-s9-post-round10-round11-20261028/verify_compact.js --negative
```

`prove.js` recomputes the discovery trace and checks exact equality with `certificate.json`. `verify_compact.js` checks only the necessary terminal obligations and rejects forged WIN9/LOSS9 claims and invalid witness indices. Both require the frozen upstream plan; neither uses an incomplete df-pn result as a terminal verdict.

**Scope:** These are local S9 certificates. The proof-only S8 coverage and the conditional 14-root frontier must be recalculated separately before claiming any reduction of the 83 outstanding edges. Standard 11×11 empty-board winner: **UNKNOWN**.

## Independent verification receipt

[CI run 40677563379](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40677563379) **PASS**: the frozen certificate was independently replayed and all forged-claim negative controls were rejected. The minimal certificate verifier checked **124** distinct S10 terminal leaves and **23,710** recursive states per geometry, versus **320** leaves and **57,384** states in the full discovery replay. This saves **61.25%** of terminal leaves and about **58.68%** of terminal recursion states for repeated checking; it is not a wall-clock benchmark. The complete discovery replay also matched the frozen certificate byte-for-byte.
