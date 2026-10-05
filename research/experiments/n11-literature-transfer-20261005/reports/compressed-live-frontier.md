# Compressed Game Solving transfer on the live n=11 reply=27 frontier

Date: 2026-10-06

**The 11x11 empty-board outcome remains UNKNOWN.**

The earlier small-board audit showed that the language of safe five-stone
positions has a very small exact acyclic DFA compared with explicit
enumeration.  This follow-up tests the same finite-language representation on
the **actual n=11 proof frontier**, rather than on complete small-board layers.

The transfer target is Jeffrey Considine's *Compressed Game Solving*: keep
sets of positions in a compressed automaton and try to perform set operations
and move generation on the representation instead of treating every position
as an independent object.

## Input frontier

Source: GitHub Actions run `37334644565`,
artifact `reply27-current-cache-optimization`,
digest `sha256:a9334f00a8547357d92ff063ca03347e3f27daee092bb261debfa4b188008543`.

At that point the fixed two-stone root `{60,27}` had

- 17 exact LOSS s4 classes,
- secured third-move coverage 66/119,
- exact minimum 14 additional classes,
- current 14-class repair frontier with **1,346 distinct UNKNOWN canonical s5 roots**.

Each canonical position is represented as the sorted sequence of occupied point
numbers.  A prefix trie is built and then minimized exactly by merging states
with identical labeled continuation languages.  There is no approximate hash.

For the one-ply image, every legal sixth move is generated from each canonical
s5 root, the resulting s6 position is D4-canonicalized, and the exact language
of distinct canonical s6 roots is minimized in the same way.

## Result

| set | explicit objects | trie states | minimal DFA states | objects / DFA state |
|---|---:|---:|---:|---:|
| current s5 repair frontier | **1,346** | 3,815 | **293** | **4.59** |
| canonical one-ply s6 image | **66,630** | 125,089 | **5,515** | **12.08** |

The 1,346 s5 roots generate **126,979 raw legal transitions**.  D4
canonicalization reduces these to **66,630** distinct s6 roots, a **47.53%**
transition deduplication.

More importantly for bulk solving, **59,621 of the 66,630 s6 roots are reached
from at least two distinct s5 parents**.  The maximum number of distinct s5
parents is 5.  If symmetric duplicate moves from the same parent are counted as
separate transitions, the corresponding figures are 59,627 roots and maximum
raw transition multiplicity 6; those are transition multiplicities, not parent
multiplicities.

The immediately preceding frontier, before the latest class rejection, gave a
very similar result:

- 1,346 s5 -> DFA 310 states;
- 127,278 raw transitions -> 66,848 canonical s6;
- s6 DFA 5,318 states;
- 59,713 s6 roots shared by multiple distinct parents (59,719 if repeated
  transitions from the same parent are counted).

So the compression is not tied to one particular 14-class matching.

## Interpretation

This is stronger evidence than the earlier 5x5--7x7 whole-layer experiment:
the **real 11x11 proof boundary** is itself highly compressible as a finite
language.

What is *not* yet shown is that a compressed solver is faster.  The current
measurement still explicitly enumerates the 126k transitions before building
the minimized automaton.  The important next experiment is therefore not
another compression-ratio measurement; it is implementing at least one useful
operation directly on the automaton, for example:

1. compressed one-point extension from the s5 language to an s6 language;
2. set subtraction against an exact s6 verdict set;
3. reverse incidence from solved s6 subsets back to all s5 parents;
4. batch detection of s5 parents that already have a LOSS s6 witness.

The last two are especially relevant because selective s6 boundary expansion
has already closed hard s5 roots in the live proof.

If these operations can avoid materializing most of the 126,979 transitions,
Compressed Game Solving becomes a plausible second implementation lane beside
the current shard-based exact replay.  If they cannot, the DFA remains useful
mainly as a compact certificate/index.

## Reproduction

The generic exact audit is:

```bash
python research/experiments/n11-literature-transfer-20261005/scripts/frontier_dfa_audit.py \
  --targets current-repair-targets.csv
```

where `current-repair-targets.csv` is the target file from the cited Actions
artifact.

The script regenerates legal moves using the repository's audited n=11 geometry
code and canonicalizes every s6 child under D4 before minimization.
