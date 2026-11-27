# n11 ninth-cost 4 LOSS row third-impl corroboration completion (2026-11-27)

Wave A declaration 913373d8 (publish-then-execute) -> results + kit
(this commit). Kit dir:
research/experiments/n11-ninthcost-4loss-thirdimpl-corroboration-20261127/.

## Result: CORROBORATION-PASS (verdict-level)

8/8 clean cold passes (4 keys x 2, third_impl.js 08ea958f, cap
400,000,000, wallcap 260, memo-power 22, node_rc=0 each):

- k01 1297036692683751424:134283264 (legal 89): LOSS(2), expansions 2,439,912 x2 identical
- k03 1297036761403228160:134217728 (legal 86): LOSS(2), expansions 8,958,740 x2 identical
- k05 1152921504624672768:536903680 (legal 91): LOSS(2), expansions 10,108,236 x2 identical
- k06 1152923703764321280:68719476736 (legal 99): LOSS(2), expansions 9,429,199 x2 identical

No exploratory or discarded passes (8/8 published). Legal derived ==
published legal for all keys. Verdict-level agreement with the replica
(wave C6 cold pairs) and the C++ second-implementation gate
(652e19f7): the four C6-published ninth-cost LOSS rows now have all
three implementation pillars.

## Pillar status and remaining work

- The four C6 LOSS rows: replica cold pair + C++ gate + third-impl
corroboration (3/3 pillars, adoption-eligible as a set only under a
separately declared adoption Part with the parent batch's WIN/LOSS
conflict review).
- The ninth-cost k12 WIN(1) row: third-impl corroboration published by
the concurrent lane (d9ce050a); its C++ gate remains pending.
- The rest of the ninth-cost ladder (k08-k13 raws in C7, further keys,
parked L50M candidates k02/k04/k07): single-implementation.
- The ninth-cost pre-audit ledger needs the ninth batch-summary pin
once the ladder closes.

No verdict consumed. No cache increment, no class-status change, no
coverage claim, no adoption. The standard 11x11 empty board: UNKNOWN.
All 19 central-reply roots: UNKNOWN. Two-stone root {60,27}: UNKNOWN.
Third-move pair {100,108}: UNKNOWN. S2, class 1/2/4 and all closure
classes: UNKNOWN. Nodes and expansions are bookkeeping, never
verdicts.
