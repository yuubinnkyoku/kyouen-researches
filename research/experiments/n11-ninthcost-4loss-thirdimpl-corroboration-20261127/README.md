# n11-ninthcost-4loss-thirdimpl-corroboration-20261127

Third-implementation corroboration pillar for the four ninth-cost
15M-stage LOSS rows of the exclusive S5 probe class
`1297036692683751424:134217728` (wave C6, commit 95883e09) - the same
four rows gated by n11-ninthcost-4loss-cppgate-20261127 (652e19f7).
Declared in research/log/2026-11-27-n11-ninthcost-4loss-thirdimpl-
declaration.md (913373d8, publish-then-execute; single-owner claim,
disjoint from the k12 WIN-row corroboration kit).

## Result: CORROBORATION-PASS (verdict-level)

Standing third implementation `third_impl.js` (sha256 08ea958f...,
byte-clone of the published k12 kit copy, byte-verified), protocol
cap=400000000, wallcap=260, memo-power=22, two fresh cold passes per
key (one node process per pass, node_rc captured by the shell in the
same command):

- k01 `1297036692683751424:134283264` (legal 89): result 2 (LOSS),
  expansions 2,439,912, both passes identical (ttHits 1,467,669).
- k03 `1297036761403228160:134217728` (legal 86): result 2 (LOSS),
  expansions 8,958,740, both passes identical (ttHits 4,896,481).
- k05 `1152921504624672768:536903680` (legal 91): result 2 (LOSS),
  expansions 10,108,236, both passes identical (ttHits 5,384,615).
- k06 `1152923703764321280:68719476736` (legal 99): result 2 (LOSS),
  expansions 9,429,199, both passes identical (ttHits 4,910,358).

All 8 passes: reason clean, node_rc=0, legal derived == published
legal, per-key pairs identical on every field except wall_s. Verdict-
level agreement: the third implementation agrees with the replica
(wave C6 cold pairs) and the C++ second-implementation gate (GATE-PASS
652e19f7) that all four rows are LOSS(2). Nodes and expansions are
different counters across implementations and are bookkeeping.

## Honest disclosures

- No exploratory or discarded passes: every executed pass is published
  (8/8); all resolved clean on the pre-registered cap 400,000,000.
- Execution happened after the wave A declaration push (913373d8) and
  before this publication; the wall_s fields differ per pass and timing
  is not evidence.
- The 4 input key/lo/hi/legal tuples are machine-extracted from the
  published ninth-cost kit (inputs byte-identical to the kit MANIFEST
  pins 5768229a / 3b33982d / ed29fa0f / ed853a05...).
- Pillar status after this Part: the four C6-published ninth-cost LOSS
  rows now have all three implementation pillars (replica cold pair +
  C++ gate + third-impl corroboration). NOT covered here: the k12 WIN
  row (corroboration published separately by the concurrent lane; its
  C++ gate is pending), any further ninth-cost escalation rows, and
  adoption of any row (separately declared Part under the parent
  batch's WIN/LOSS conflict policy).

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
expansions are bookkeeping, never verdicts.
