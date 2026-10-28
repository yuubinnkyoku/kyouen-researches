# N11 round12: exact terminal certificates for 32 selected S9 roots

The frozen round11 replan against the **79** outstanding edges of the fixed conditional 14-root S7 plan selected exactly **32** nine-stone classes. The selection SHA-256 is `05f4f971ffeeadb9688a64ab5c67cb6eb193ab891bc3c34c7a0a09515190b53a`. Only those classes were explored. The earlier boundary preflight had independently verified **807** legal S9→S10 edges and **805** distinct D4-canonical S10 children.

## Terminal proof

- **12 WIN9** roots: all **311** legal S10 children were independently proven WIN.
- **20 LOSS9** roots: each has a frozen S10 LOSS witness.
- Discovery tested **443** distinct S10 terminal positions (**444** first-LOSS obligations), with **80,850** recursive states *per geometry*.
- The 20 fixed LOSS10 witnesses yield **200** canonical LOSS9 parents. This is the closure size, not 200 globally new verdicts.
- No WIN9/LOSS9 contradiction was detected within the fixed batch; **no two-stone root was closed**.

The terminal solver uses two independent exact integer formulations: 3×3 difference determinants and 4×4 Bareiss determinants. It compares verdict, legal-move count, and recursive state count on every evaluated S10 leaf. The frozen certificate stores 32 witness bytes (`255` for universal WIN9, otherwise the lexicographic index of a LOSS10 child), selection and witness SHA-256, WIN9 keys, and the LOSS9-parent closure hash.

## Independent replay

[Discovery workflow 40702770011](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40702770011) **PASS**. [Independent verification workflow 40702942607](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40702942607) **PASS**, including full discovery replay and forged-witness rejection.

The compact verifier checks **330** distinct S10 terminal leaves (**331** obligations), with **59,233** recursive states per geometry: **25.5%** fewer leaves and **26.7%** fewer recursive states than discovery. These are *terminal recomputation* counts, not wall-clock speedups.

From the repository root:

```sh
node research/experiments/n11-s9-post-round11-round12-20261028/prove.js
node research/experiments/n11-s9-post-round11-round12-20261028/verify_compact.js --negative
```

## Verified upward proof-only lift

[Proof-only lift run 40703068702](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40703068702) **PASS**. The script reconstructs the original round7 certified 5,407-class WIN8 frontier, adds the independently terminal-proven round9, round10 and round11 witnesses to obtain 5,545, then adds only the round12 terminal WIN9 parents. The 12 new WIN9 roots yield **107** distinct canonical WIN8 parents; **98** were not already in the 5,545-class proof-only frontier, so the new certified WIN8 count is **5,643**. None conflicts with the frozen LOSS8 set.

For the *fixed* conditional 14-root S7 plan, **484 of 548** move edges are now certified, up from 469; outstanding edges fall from **79 to 64**. This is not an optimized new 14-root minimum, nor a new S7 verdict. The exact result is frozen in `lift.json` and `lift.js` checks its identity on replay.

Potential incidence is not a WIN verdict. No S7, S5, two-stone or empty-board root was closed. **Standard 11×11 empty-board winner: UNKNOWN.**
