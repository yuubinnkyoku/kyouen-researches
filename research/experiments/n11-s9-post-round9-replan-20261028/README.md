# N11 round9: proof-only next-plan audit

The round9 terminal certificate establishes five WIN9 and 27 LOSS9. Its five WIN9 witnesses establish 42 additional distinct WIN8 classes, reducing the conditional 14-root frontier from 100 to 93 unproved S8 edges. This does not close the empty board or any new two-stone root.

The reproducible replan checks all 32 S9 terminal claims with independent 3x3 and 4x4 integer geometry. It validates the LOSS10-to-LOSS9 parent closure, its SHA-256, all WIN8 parents and WIN/LOSS conflicts. Previously proved LOSS9 classes and all round9 selections are excluded. Candidates are then filtered against the new 93-edge proof-only frontier and dominance-pruned before bounded greedy/exchange selection.

Run from repository root:

    node research/experiments/n11-s9-post-round9-replan-20261028/replan.js

The bounded CI produces a proposed JSON plan as an artifact. It is not a terminal certificate; freeze and independently verify its output before running the next terminal batch. Standard 11x11 empty-board outcome: UNKNOWN.
