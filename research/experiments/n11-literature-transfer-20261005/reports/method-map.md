# 11×11 weak-solve literature transfer: method map

Date: 2026-10-05

**11×11 empty board remains UNKNOWN.**

This note records which ideas from solved/weakly-solved games transferred to
the current n=11 pipeline, which were rejected, and what was actually measured.
It is a method map, not a new game-outcome claim.

## Current n=11 proof shape

The active line is no longer a monolithic empty-root df-pn run.  For a fixed
two-stone root `{first=60,r2}`, the proof is organized as

1. choose a small family of canonical four-stone classes covering every legal
   third move;
2. classify each chosen s4 class from exact canonical s5 children;
3. when an s5 root is hard, descend one layer and classify it from the complete
   or selected exact s6 boundary;
4. reuse exact s5 verdicts and late residual subgame results across the
   remaining frontier.

The empty-board result is still UNKNOWN; all claims below concern search
organization and finite subproofs.

## Othello / endgame-boundary lesson: solve only the boundary needed by the root

The useful transferable idea is not Othello's game-specific evaluation but the
separation between a forward proof skeleton and a set of exact boundary
positions that are actually needed to close that skeleton.

For n=11 this became the s4-cover / s5-oracle architecture.

For root `{60,0}`, replacing the old 31-class theorem witness by an explicit
direct-union witness preserves the minimum class count 31 and full 119/119
third-move coverage while reducing the not-yet-known canonical s5 union from
3,229 to **2,319** roots.

For root `{60,27}`, the first structural 31-class witness contains **2,262**
distinct s5 roots.  A 15M-node replay classified 2,229 of them
(42 WIN / 2,187 LOSS); nine of the remaining hard roots were later classified
through their s6 boundary.  The combined exact cache expected by the independent
replay pipeline is **2,238** roots (43 WIN / 2,195 LOSS).

The next repair is therefore cache-aware: proved LOSS classes secure vertices
for free, proved WIN classes are forbidden, and only the remaining uncovered
vertices receive new UNKNOWN class targets.  The exact-union MILP in
`cache_aware_reply27_union_cover.py` minimizes the number of distinct uncached
s5 roots rather than the additive child count.

This is the closest current analogue of solving only the exact boundary that
the top-level proof really needs.

## Sprouts / impartial-game lesson: share solved small subgames, not the whole search

Čížek, Balko and Schmid's massively parallel proof-number-search work on
impartial games motivates sharing exact Grundy values for repeated small
components instead of trying to synchronize whole proof/disproof tables.

The n=11 residual game already decomposes into independent hypergraph
components.  On the saved 826-snapshot corpus:

- residual components: 1,011;
- exact component types recurring across different trials: 26;
- cross-trial occurrences: 603;
- after discarding isolated one-vertex components: 238 nontrivial occurrences.

A direct mex-state accounting over the recurring nontrivial types gave

- naive repeated solves: 946 memo states;
- solve each exact type once: 172 memo states;
- reduction: **81.8%**.

The C++ residual micro-solver now has an exact arbitrary-relabeling component
cache.  Exhaustive tests over all clutters with at most four vertices compare
three implementations: plain recursion, the existing compressed solver, and the
shared canonical cache.

An initial n=11 sample showed the important caveat: sharing reduced internal
memo work but a naive n! canonicalizer could lose wall time.  Stable incidence
color refinement was therefore added before within-color permutation.  On the
same sample, residual memo states fell from 1,268,205 at gate 0 to

- gate 4: 684,409;
- gate 5: 507,638;
- gate 6: 366,131.

Verdicts matched.  Wall time, not hit rate, remains the acceptance criterion.

## Pentago / retrograde lesson: descend one layer when the parent root is hard

A full-board retrograde solution like Pentago is not realistic for n=11: the
middle layers are too large.  The transferable part is narrower: explicitly
materialize a finite boundary layer, solve that layer in parallel, and propagate
the exact values one step upward.

This was decisive on nine hard reply-27 s5 roots.

Their complete canonical s6 boundary contains **816** distinct roots.  A
four-shard cold exact replay at 10M nodes per s6 root produced:

- s6 WIN: 729;
- s6 LOSS: 81;
- s6 UNKNOWN: 6;
- total exact nodes: 901,901,494.

Despite six unresolved s6 roots, every parent s5 became exact:

- s5 LOSS: **8**;
- s5 WIN: **1**;
- s5 UNKNOWN: **0**.

A LOSS s6 witness is enough for a five-stone AND node to be LOSS; the unique WIN
parent had all 88 canonical s6 children exact WIN.

This is strong evidence that selective one-layer boundary expansion is a useful
escape hatch when direct s5 replay stalls.

## Expected Work Search lesson: separate solve cost from chance of finding a witness

Expected Work Search combines estimated proof size with a probability that a
branch gives the desired proof.  The current coordinator already uses a cost
proxy: lower legal-move count is tried first.

The available n=11 data show why this should not be interpreted as a WIN
probability model.

On the 103-child fixed LOSS class:

- corr(legal, log exact nodes) = **0.529**;
- a one-unit increase in legal count corresponds to about 1.032× predicted
  node cost in a simple log-linear fit;
- typical multiplicative error of that one-feature fit is about 1.20×.

But on the independent 23-root mixed WIN/LOSS benchmark:

- corr(legal, log exact nodes) = **0.222**;
- AUC of legal count for discriminating WIN from LOSS = **0.519**.

Thus legal count is a usable local cost proxy but almost no outcome predictor.
A faithful EWS-style scheduler would need a second model for WIN-witness
probability, probably from residual-hypergraph features rather than legal count
alone.

Until that model is validated, using measured/online cost estimates without a
fabricated win-probability term is the safer choice.

## Relevance-zone and QBF routes

A naive relevance-zone transfer is unsafe for Kyouen because a move far outside
a local pattern can create a new forbidden quadruple with three inside points or
otherwise alter future legality.  Local proof reuse therefore needs a
game-specific closure condition; ordinary geometric locality is not sufficient.

Direct QBF encoding is logically natural for a positional avoidance game, but
the current n=11 bottleneck is not a lack of a Boolean formulation.  The finite
frontier and late residual games already expose much smaller exact subproblems,
so QBF is currently a secondary validation route rather than the main solver.

## Practical priority after this comparison

The strongest transferred methods, in current order, are:

1. **cache-aware exact-boundary selection** over s4/s5;
2. **selective s6 boundary expansion** for hard s5 roots;
3. **shared exact residual-component Grundy values** once wall-time-positive;
4. **measured expected-work scheduling**, with cost and outcome probability
   modeled separately.

The literature comparison therefore changes the n=11 strategy: the main target
is no longer “make one global df-pn search a little better”.  It is to keep
shrinking and reusing the exact proof boundary until a fixed second reply is
closed, then lift that result through the remaining reply/frontier structure.
