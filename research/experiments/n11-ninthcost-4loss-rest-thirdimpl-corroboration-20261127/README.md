# n11-ninthcost-4loss-rest-thirdimpl-corroboration-20261127

Third-implementation corroboration pillar for the four REMAINING
ninth-cost 15M-stage LOSS rows of the exclusive S5 probe class
`1297036692683751424:134217728` (wave C7 commit 838ee2f2): k08, k09,
k10, k11. Complements n11-ninthcost-4loss-thirdimpl-corroboration-20261127
(k01/k03/k05/k06, published by the concurrent lane) and
n11-ninthcost-k12-win-thirdimpl-corroboration-20261127 (k12 WIN row).
After this Part every resolved row of the ninth-cost batch has the
third-implementation pillar.

## Result: CORROBORATION-PASS (verdict-level)

Standing third implementation `third_impl.js` (sha256 08ea958f...,
byte-clone of the published eighth-cost k01 kit copy, byte-verified),
protocol cap=400000000, wallcap=260, memo-power=22, two fresh cold
passes per key (one node process per pass, node_rc captured directly by
the shell in the same command):

- k08 `1152956688979984384:536903680` (legal 98): result 2 (LOSS),
  expansions 3,805,281, both passes identical.
- k09 `1224979098645823488:536903680` (legal 92): result 2 (LOSS),
  expansions 5,462,764, both passes identical.
- k10 `1297036692683751424:134217730` (legal 96): result 2 (LOSS),
  expansions 6,533,529, both passes identical.
- k11 `1297036692683751424:134217744` (legal 97): result 2 (LOSS),
  expansions 6,925,942, both passes identical.

All 8 passes: reason clean, node_rc=0, legal derived == published legal,
per-key pairs identical on every field except wall_s. Verdict-level
agreement with the replica (wave C7 cold pairs). The four rows do NOT
yet have the C++ second-implementation gate (unlike k01/k03/k05/k06,
gated in n11-ninthcost-4loss-cppgate-20261127); that pillar stays OPEN.

## Honest disclosures

- The four input key/lo/hi/legal tuples are machine-read from the
  published ninth-cost kit input CSVs (inputs byte-identical to the kit
  MANIFEST pins 2d69fef0 / 2d11337d / c1dc5728 / 327e8186...).
- During the same session this lane also executed third_impl cold pairs
  for k01/k03/k05/k06 BEFORE observing that the concurrent lane had
  declared and published the same four rows (kit commit at 10:41:40Z).
  Those local runs are NOT published here and are disclosed only as an
  observation: they resolved LOSS(2) with expansions exactly equal to
  the published values of the concurrent lane's kit (k01 2,439,912 /
  k03 8,958,740 / k05 10,108,236 / k06 9,429,199), an accidental
  cross-host determinism confirmation of the standing implementation.
- Execution happened before this publication; wall_s differs per pass
  and timing is not evidence.
- No verdict consumed; no adoption claimed. The k12 WIN row's C++ gate
  and the batch adoption Part remain OPEN (adoption needs a fresh
  single-owner declaration and the WIN/LOSS conflict review).

## Files

- `scripts/third_impl.js`: byte-clone of the pinned third implementation.
- `output/raw/<key>.p1.txt` / `.p2.txt`: the 8 cold-pass raws.
- `MANIFEST-sha256.txt`: kit manifest.

## Guards

The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. A third-implementation LOSS(2) agreement is not a class
closure claim, not a root verdict, and transfers nothing. Nodes and
expansions are bookkeeping.
