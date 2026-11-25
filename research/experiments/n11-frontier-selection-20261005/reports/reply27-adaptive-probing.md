# Reply=27 adaptive repair probing

Date: 2026-10-05

**11×11 empty-board outcome remains UNKNOWN.**

This note records the first exact adaptive-probing experiment on the reply=27
repair frontier and the resulting scheduling change.

## Starting repair frontier

After the original 31 selected s4 classes were classified as

- LOSS 16
- WIN 15
- UNKNOWN 0

the 16 proved LOSS classes secured 62/119 legal third-move vertices.  Repairing
the remaining 57 vertices required at least 15 additional classes.  The
additive-work optimum used 17 UNKNOWN repair classes and had 1,375 distinct
uncached canonical s5 targets.

## First adaptive sample

Workflow run `37276125535` selected the two lowest-legal uncached s5 roots from
each of the 17 repair classes, deduplicated them, and cold-replayed the resulting
34 roots at a 15M-node cap.

Exact result:

- sampled s5: **34**
- WIN: **7**
- LOSS: **27**
- UNKNOWN: **0**
- exact nodes: **144,484,374**
- process wall: **375.27 s**

The seven WIN s5 roots are decisive counterexamples to any repair class that
contains them: such a class is WIN and cannot be used in a LOSS cover.

After loading the 34 exact verdicts and reoptimizing the repair:

- globally forbidden WIN classes: **17 -> 36**
- proved LOSS classes: **16 -> 16**
- secured vertices: **62 -> 62**
- additive optimum: **17 classes / 1,393 additive / 1,375 unique**
  -> **16 classes / 1,460 additive / 1,458 unique**

The target union therefore grew by 83.  This is not a regression in proof
knowledge.  The earlier 1,375-target frontier was optimistic: several of its
cheap classes were actually WIN.  The probes exposed those false candidates
before paying to solve all their children.

## Retrospective value of one probe per class

The 34-root batch can be split exactly according to the deterministic sampling
rule.

The first probe from each of the 17 repair classes used:

- roots: **17**
- WIN: **3**
- LOSS: **14**
- nodes: **64,947,715**

Because one of those WIN roots is shared by another repair class, these three
WIN roots already invalidate **4 of the 17** starting repair classes.

The second probe from each class used:

- roots: **17**
- WIN: **4**
- LOSS: **13**
- nodes: **79,536,659**

After both rounds, seven of the starting repair classes are invalidated.

In the original 1,375-root union, those seven invalidated classes touched 502
targets; **491** of those targets belonged to no surviving starting repair
class.  Reoptimization must introduce replacement classes, so those 491 are not
a direct wall-time saving, but the experiment shows that class falsification
has very high information value.

This motivates a stricter adaptive loop:

1. probe **one** promising s5 per current repair class;
2. ingest exact WIN/LOSS verdicts;
3. immediately reclassify all 3,384 s4 classes and reoptimize the repair;
4. only then choose the next probe.

The workflow was changed from two probes per class to one probe per class in
commit `30b45854`.

## Relation to Expected Work Search

The experiment reinforces the separation between solve cost and witness
probability.

Low legal count is a useful local proxy for exact solve cost, but it is not a
general outcome predictor.  On the hard9 s6 boundary, low-legal witness probes
missed every LOSS witness, while ordering by larger legal count brought the
first LOSS much earlier.  Conversely, forcing descending legal order inside
ordinary s5 exact DFS worsened a three-root benchmark by about 26% in nodes.

A cost-aware `s5-target92` A/B reduced nodes only slightly on the same three
LOSS roots:

- baseline: **20,501,549 nodes**, 37.38 s
- target92: **20,106,600 nodes**, 38.71 s
- node ratio: **0.980736**

The wall time did not improve.  It remains an experiment, not a default solver
policy.

The useful Expected-Work-style transfer is therefore at the **frontier
scheduler**: spend small exact work to falsify whole candidate classes, then
reoptimize.  A single fixed child ordering inside every exact DFS is too coarse.
