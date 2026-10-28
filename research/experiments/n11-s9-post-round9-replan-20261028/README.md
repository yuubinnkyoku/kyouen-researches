# N11 round9: proof-only next-plan audit

The round9 terminal certificate establishes five WIN9 and 27 LOSS9. Its five WIN9 witnesses establish 42 additional distinct WIN8 classes, reducing the conditional 14-root frontier from 100 to 93 unproved S8 edges. This does not close the empty board or any new two-stone root.

The reproducible replan checks all 32 S9 terminal claims with independent 3x3 and 4x4 integer geometry. It validates the LOSS10-to-LOSS9 parent closure, its SHA-256, all WIN8 parents and WIN/LOSS conflicts. Previously proved LOSS9 classes and all round9 selections are excluded. Candidates are then filtered against the new 93-edge proof-only frontier and dominance-pruned before bounded greedy/exchange selection.

Run from repository root:

    node research/experiments/n11-s9-post-round9-replan-20261028/replan.js

The bounded CI produces a proposed JSON plan as an artifact. It is not a terminal certificate; freeze and independently verify its output before running the next terminal batch. Standard 11x11 empty-board outcome: UNKNOWN.

## Frozen independently checked result

CI run 40648005327 passed. Eligible S9 classes: 1011 to 890 (50 proof exclusions, 71 no longer relevant to the 93-edge frontier). Dominance-pruned: 125. The next 32 proposed candidates potentially cover 43 S8 classes with 830 legal S10 children. The frozen next-plan.json is checked byte-for-byte against fresh replan output in CI.

## Independent bounded preflight for the next 32 candidates

Run `node research/experiments/n11-s9-post-round9-replan-20261028/audit_next_batch.js`.
This does **not** run terminal minimax or replan the 14-root frontier. It checks the
frozen 32 canonical safe S9 roots, their complete S10 child sets under two
independent integer geometries, and S8 reverse incidences. It also rejects
modified keys, duplicate selections and forged empty-board verdicts.

[Independent preflight CI 40654502979](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40654502979)
**PASS**: 830 ordered S10 child obligations but **829 distinct** S10
classes (one shared child); 288 S8 reverse incidences but 286 distinct
S8 parents (two repeated). Within-batch deduplication therefore saves
only one terminal leaf if all children are visited. Cross-batch cache
reuse and early LOSS9 witnesses are separate, not measured here.
No new S9/S8 verdict or two-stone closure; 11×11 empty-board **UNKNOWN**.
