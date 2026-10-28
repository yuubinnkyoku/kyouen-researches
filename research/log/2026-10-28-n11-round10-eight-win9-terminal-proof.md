# 2026-10-28: N11 round10, eight terminal WIN9 and 24 LOSS9

Reviewed latest main, `AGENTS.md`, `research/knowledge/README.md`,
K0023/K0105, round9 terminal and replan logs, and the frozen 32-class
post-round9 selection. No branch or PR was used.

The [bounded round10 terminal discovery](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40654746616)
**PASS** solved the 32 selected S9 positions to the actual terminal game with
two independent integer geometries (3×3 difference determinant and 4×4
Bareiss). The frozen certificate contains **8 WIN9 / 24 LOSS9**. All 207
S10 children of the eight WIN9 are WIN10. Each LOSS9 has an explicit
terminal LOSS10 witness. There were 393 unique terminal S10 leaves and
68,906 recursive states per geometry in discovery; the 24 LOSS10 witnesses
induce 240 canonical LOSS9 parents (not claimed globally new).

[Independent fixed-certificate verification CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40654867335)
**PASS** rechecked all required terminal and parent-incidence obligations
with both geometries and rejected forged WIN/LOSS and out-of-range witnesses.
The compact replay needed **231** distinct S10 leaves and **42,709** terminal
states per geometry: 41.2% fewer leaves and 38.0% fewer terminal states than
discovery. These are replay-work counts, not measured wall-clock speedups.

The independently audited next-batch preflight
([CI 40654502979](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40654502979),
PASS) found 830 ordered S9→S10 children but only 829 distinct leaves,
so within-batch terminal cache sharing can save just one full-boundary leaf
in this batch. This does not preclude early LOSS9 witnesses or cross-batch
reuse.

A separate `lift.js` and [bounded workflow](https://github.com/yuubinnkyoku/kyouen-researches/actions/workflows/n11-s9-post-round9-round10-lift.yml)
were added to rebuild the conditional 14-root WIN8 frontier from previously
certified evidence. Its result was **not yet available** at the time of this
record. Accordingly, do not infer a new WIN8 count or reduced unproved-edge
count from the eight WIN9 alone.

Last confirmed proof-only WIN8 **5,449**, conditional 14-root unproved S8
edges **93**, new two-stone closures **0**. Standard 11×11 empty-board
winner **UNKNOWN**.
