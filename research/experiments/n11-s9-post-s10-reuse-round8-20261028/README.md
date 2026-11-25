# 11×11: post-S10-reuse round 8, 32 terminal LOSS9 certificates

Standard q=4, normal play, original-first-player viewpoint. Empty-board outcome **UNKNOWN**.

Source: the exact 32 selected keys in ../n11-s10-cross-batch-reuse-20261028/plan.json (selection SHA-256 fixed in certificate.json). No unselected roots were explored.

Run: node research/experiments/n11-s9-post-s10-reuse-round8-20261028/verify.js --full --negative

Independent 3x3 difference determinant and 4x4 integer Bareiss checks of legal S9->S10 boundaries and terminal minimax: 32 S9 LOSS, zero S9 WIN. First-loss ordered scan checked 243 distinct S10 terminal leaves (211 WIN, 32 LOSS), 49,224 minimax memo states per geometry. The 32 fixed LOSS10 witnesses alone suffice to recheck all 32 LOSS9 roots: node research/experiments/n11-s9-post-s10-reuse-round8-20261028/verify.js --negative (32 terminal leaves, 10,233 states per geometry before negative tests). False LOSS witness and out-of-range witness are rejected.

Removing each of the ten stones from the 32 LOSS10 witnesses yields 320 distinct canonical LOSS9 parents, independently checked as legal moves under both geometries; 32 are the selected roots. The other 288 parent keys are not claimed as new global proof classes: possible overlap with existing certified LOSS9 has not been subtracted. The 211 WIN10 terminal results are replayable from the ordered first-loss scan but are not sufficient to label any S9 parent WIN without its full child boundary.

The existing 14-root conditional frontier remains at 100 unproved S8 edges, proof-only WIN8 5,407, with no new S7/S5 or two-stone closure. This is a bounded terminal-only local proof, not a solution to the empty board. No branch/PR was used.
