# 2026-11-27 n11 ninth-cost remaining-4-LOSS-row third-implementation corroboration (k08/k09/k10/k11)

Companion to the wave C official completion log. Scope: the four
ninth-cost 15M-stage LOSS rows NOT covered by the concurrent lane's
kits: k08, k09, k10, k11 (wave C7 commit 838ee2f2). Kit:
`research/experiments/n11-ninthcost-4loss-rest-thirdimpl-corroboration-20261127/`.

Result: **CORROBORATION-PASS verdict-level** - standing third_impl.js
(08ea958f) resolves all four rows LOSS(2), cold pairs identical
(k08 3,805,281 / k09 5,462,764 / k10 6,533,529 / k11 6,925,942
expansions; cap 400M, wallcap 260, memo-power 22, all clean, node_rc=0).

Pillar status after this Part: every resolved row of the ninth-cost
batch (8 LOSS + k12 WIN) has the third-implementation pillar
(k12 via the k12 kit; k01/k03/k05/k06 via the concurrent lane's 4loss
kit; k08/k09/k10/k11 via this kit). Still OPEN: the k12 WIN row C++
gate; the C++ gate for k08/k09/k10/k11; the parked k02/k04/k07 L50M
escalation (declaration required first); and the adoption Part (fresh
single-owner declaration, WIN/LOSS conflict review, merger + flip
census per the eighth-cost SZ/EM precedent).

Honest disclosure: this lane had also executed third_impl pairs for
k01/k03/k05/k06 before noticing the concurrent lane's published kit;
those local runs matched its expansion counts exactly and are not
republished here (recorded only as a cross-host determinism
observation in the kit README).

Guards: no verdict consumed. All rows stay single-implementation
replica + third-implementation corroboration labels (C++ gate pending
where noted). The standard 11x11 empty board: UNKNOWN. All 19
central-reply roots: UNKNOWN. Two-stone root {60,27}: UNKNOWN.
Third-move pair {100,108}: UNKNOWN. Every closure class: UNKNOWN
unless a published Part says otherwise.
