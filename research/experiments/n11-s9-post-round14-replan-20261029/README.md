# N11 proof-only replan after round14

This deterministic coordinator consumes the **independently verified and frozen** round14 terminal certificate and WIN8 lift. It does not perform a giant root search, nor infer a verdict from potential coverage.

- Starting from the 338 eligible S9 classes in the frozen round13 replan, exclude the 32 selected round14 roots and all additionally certified LOSS9 parents induced by exact LOSS10 witnesses.
- Restrict the remaining options to the 55 unproved S8 edges of the fixed conditional 14-root S7 plan.
- Reconstruct round9–round14 certified WIN8 coverage, independently verify the round14 terminal certificate, reject forged witnesses and cross-batch WIN9/LOSS9 conflicts, and use the existing dominance-aware 32-root coordinator.
- Only freeze `next-plan.json` after the bounded run and independent checks pass. Candidate selection and potential coverage are not verdicts.

From the repository root:

```sh
node research/experiments/n11-s9-post-round14-replan-20261029/replan.js
```

The workflow uploads the generated JSON as an artifact for review before it is frozen on main. Any future frozen result is checked byte-for-byte at the object level.

**Standard 11×11 empty-board winner: UNKNOWN.**
