fold20 (K1129) external second verification: published bytes re-confirmed by an
independent third-implementation verifier (2026-11-20)

## Position

The fold20 receipt fold (root `00000000000000003800000008d10000`, residual 41 -> 38
rows, twenty-seventh receipt and tenth WIN8-D10 receipt fold) was published by the
publisher lane as experiment dir
`n11-residual38-win8-receipt-fold-root08d10000-20261120/`
(receipt `76fd255b...`, machine `9e141d4a...`, builder `4ba91cd0...`, README `637841d2...`),
at which point multiple runs, the pristine rerun gate of the published fold19
machine and the full-chain frontier recomputation were already machine-checked.
The fold20 experiment dir (like fold21, unlike fold24 onwards) carries no
publisher-bundled independent audit machine. The fold21 (K1168) and fold22 (K1167)
external verifiers machine-checked the fold20 record only as a chain record and
re-ran the fold20 machine as a rerun gate; a value-level external second
verification of the fold20 receipt's own claims
(open 8-row closure, claim 3 + extra 5 rows, closed edge cost 599, residual 41 -> 38,
five-parent target 71 -> 74, frontier 6,152/487,418 -> 6,144/486,819,
solved 1,696 -> 1,704, incidence 11,711 -> 11,701, needed 4,460/353,866 -> 4,452/353,267,
28 canonical-row classification 8/20/0, win16 candidates 7 -> 6 roots) is performed
for the first time by this verification, under the single-owner declaration
([declaration note](../../log/2026-11-20-n11-fold20-external-second-verification-single-owner-note.md),
commit `5f6c1b7a910e695349ad497cde309d3042d4636a`, declared 2026-11-20T23:09:08Z,
6 acceptance conditions).
The verifier `scripts/verify_fold20_external_20261120.py` is a third implementation:
per the declaration note it follows the design of the fold21 external verifier
(`scripts/verify_fold21_external_20261120.py`, experiment dir
`n11-fold21-external-second-verification-root80880200-20261120`), with the target
replaced by fold20 through machine-checked region surgery, while the geometry and
aggregation primitives (8 D4 coordinate maps, 4x4 concyclic determinant,
survival-move legal-move reimplementation, census parent bookkeeping) remain the
verifier family's own implementations: no code is shared with the fold20/fold19
publication machines, and the fold21/fold22 verification results are never used as
inputs. Output is a single deterministic audit JSON with sorted keys and no clock
fields (on any gate failure no audit is written and exit status is 1).

## Fixed pins

Published bytes were re-fetched from GitHub at both the declaration-time pinned HEAD
`ec24b235f806822086680fee4075820679c78acf` and the verification-time main
`299264789acbf5dc3bdd7e379ab8becaf750024f`; all fetched bytes matched byte-identically
between the two refs (W tree and publication dir full `diff -r`, see reproduction.log).
SHA-256 pins asserted by the verifier (P section):

- published receipt `win8-root08d10000-receipt-fold-20261120.json`
  `76fd255bf16ef0e434d15579cf148015bd564929e85910172f0a0ef87015842a2` (24,684 bytes)
- published machine `fold_win8_root08d10000.py`
  `9e141d4a721025fd55a5bda68266a5f1b43cbcb65112f438839b0db351a06f72` (70,951 bytes)
- published builder `build_fold20.py`
  `4ba91cd09170d482426514bee89f3f0e0fcbe7fc70af6041dd9ae24decf921db` (36,412 bytes)
- published README `637841d2e26f416cc5e4944e3ace1ec0e06878d63dfcabee470a46225230881a` (9,056 bytes)
- previous fold19 receipt
  `c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae` (22,898 bytes)
- fold19 machine `51442d96341fcffc17d9cb72e36946cb68cd97100abaa6939b27e0d6a20949e8` (68,386 bytes)
- K1121 certificate body `8513e36613c2676fb82816f47a1ecdda674264eedb9c583dae2616346f4000d2`
  (1,026,202 bytes, 28,328 rows)
- K1121 audit canon `0088ebab040a29e608c987fb8ae866abf59253d60455b0d2ca6b6ef963170940` (19 gates)
- K1091 sweep master pin (K1121 audit g01) `edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`

The input tree W is rebuilt by `scripts/reconstruct_fold20_inputs.py`
(SHA-256 `bf21d0428300168a8c8bf90637334c35250b91786fc784b53bfdfef1104a92b8`,
10,168 bytes, default Git ref `ec24b235...`): the fold20 machine's 49 input pins
(12 Git blob SHA-1 + 37 SHA-256) are re-checked fail-closed, and the published chain
machines needed by the rerun gate are placed SHA-checked (fold19 machine `51442d96...`,
fold18 machine `dcdfbf92...`, fold18 preverified copy `d342f1f8...`). That the fold19
machine's own input pin table (12 blob + 34 SHA-256) is a subset of the fold20
machine's 49 pins with equal values is machine-confirmed by both the reconstruction
script and the verifier (I section).

## What was done and results

The audit canon is `output/external-audit.json`
(128,175 bytes, SHA-256 `5a9bb98feb907ebefe5eeddf1c15acd241eae7911ae0cc258ff27f4dc3e3e5ad`,
gate 1,317) with `all_gates_pass` true. Gate breakdown: P 13 (publication pins),
I 60 (W 49 pins + pin-chain consistency), C 1,215 (independent rederivation),
X 15 (pristine reruns), T 14 (tamper fail-closed). Main contents:

- **Publication pin match / W reconstruction (P/I)**: SHA-256 match of the 9 canons
  above, re-check of all 49 W pins, and machine confirmation of the
  fold19-pin-table subset relation against the fold20 machine's 49 pins.
- **Pristine re-execution x4 (X)**: the published fold20 machine re-run with
  `FOLD_PREVERIFIED_CHAIN` unset. Four runs (same cwd twice on W in place; fresh
  copytree W with isolated cwd/HOME; fresh copytree W with isolated cwd/HOME plus
  `PYTHONHASHSEED=random`) all returned 0 with the receipt output SHA-256
  byte-identical to the published canon `76fd255b...`. Every run nests the
  published fold19 machine pristine rerun gate (fold19 canon `c02d9a54...` match),
  which in turn nests the fold18 preverified rerun and the K1120 gate group
  (transitive re-verification). A standalone fold20 machine run measures ~4.7-4.8 s
  wall.
- **Independent rederivation (C 1,215)**: the full frontier chain
  ledger/globalFold -> previousCostFold -> firstFold tarball -> secondThird ->
  fold4 -> fold56 -> fold7/8 -> ninth-twelfth -> windfall4 -> fold10..fold19
  (16 chained folds recomputed from the base worklist of 6,438 rows) yields
  post-fold19 open frontier 6,152 rows / 487,418 cost, solved 1,696, incidence 11,711,
  residual five-parent target rows 41 (71/112 closed), matching every published
  stage value. The K1121 root `00000000000000003800000008d10000` is independently
  confirmed as 8 stones [16,20,22,23,27,59,60,61], quadruple-free, D4-canonical, with
  50 legal moves re-derived by the survival-move reimplementation (K1121 gate
  g05/g11/g12 == 50). The C(8,6)=28 body geometry canonical rows are re-derived two
  ways ((A) 8 D4 images x C(8,2) two-stone removals = 224 operations vs (B) D4
  canonicalization of the 28 six-stone subsets) and agree as sets; the 28 canonical
  rows classify 8 open-frontier / 20 not-in-worklist / 0 closed-before. The receipt's
  closed 8 rows split into 3 claimed five-parent target rows (cost 74/75/76) and
  5 extra rows (cost 80/83/70/72/69), closed edge cost 599, parent deltas on 4
  parents (class 4: 79 -> 77 with 2 rows, 80 -> 78 with 2 rows; class 2: 12 -> 9 with
  3 rows, 40 -> 37 with 3 rows; 10 row-closings, 0 fully closed parents),
  frontier_after 6,144/486,819, solved 1,704, incidence 11,701, needed 4,452/353,267,
  five-parent target 71 -> 74, residual 41 -> 38, win16 candidates 7 -> 6 roots
  (1 retired; 15 claimed rows remaining = 49 - 4-3-3-4-3-4-3-3-4-3) all re-computed
  and matched value-level against every corresponding field of the published
  receipt canon (including controls, independent-verification block and the
  5-statement interpretation guard). The K1121 audit 19-gate main values
  (g01 K1091 master pin, g02==g03 runner blob `c132cc64...`, g05 mobility 50,
  g06 uncapped probes 564,695/673,870 (andclose1/andclose0), terminal stone counts
  [14,18], g07 claim 3 rows, g08 pilot_d6 4 + reproduced 2/2, g13 extraction nodes
  A 2,428,240 / B 1,748,509, g14 certificate 1,026,202 bytes / 28,328 rows
  sorted-unique, g15 28,328, g17 bareiss 50/15,513, third-method aggregation
  terminals 15,513 / visited 83,544 / winner 53,570 / loser 14,461 / move edges
  72,930, g19 K1097 record sha `2896deb0...`), the K1097 refsolve 27 gates, the
  footprint 16 roots with `intrinsic == claimed`, the exactly-once 49-row partition,
  residual-23 disjointness and the retired-root predecessor
  `00000000000000801212000001009000` are re-checked independently.
- **Tamper x2 (T)**: 1-byte XOR 0x01 mutations at this lane's own unannounced offsets
  on isolated copytree W copies: `inputs/worklist.csv` byte offset 5077 is caught by
  the legacy blob pin ('input blob mismatch') and the K1121 certificate body byte
  offset 28081 by the SHA-256 pin ('input sha256 mismatch'); both return nonzero with
  no output written. The production W is untouched (pins re-verified afterwards).

The audit canon was produced byte-identical by 3 executions (same cwd twice; isolated
cwd/HOME with `PYTHONHASHSEED=random`), and the reconstruction was byte-identical from
the two pinned refs (declaration-time HEAD and verification-time main). One verifier
execution measures ~21 s wall (six fold20-machine launches per run including tamper
probes). The run record is `output/reproduction.log`.

### Experimental facts

- During region surgery of the verifier, the C1 tail block (post-fold19 residual-41
  verification: fold19 record SHA match in W, frontier recomputation, receipt
  `previous_fold` cross-check) was accidentally lost; it surfaced at first run as a
  `NameError` (`fa19`) and was restored by an anchored splice into its correct
  position. Lesson recorded: after any splice, grep-verify that the inserted text is
  actually present.
- The restored gate first failed as written (`receipt previous_fold record ref ends
  with fold19 sha`): the receipt's `previous_fold.record` string ends with
  "(sha256 c02d9a54...)" so the check was corrected to a containment check of the
  fold19 record SHA (`c02d9a54...` still asserted verbatim, fail-closed). The
  acceptance condition itself is unchanged.
- The declaration note was pushed with the real body (no placeholder), fetch-back
  byte-identical (10,140 bytes, SHA-256
  `03e07ceaa158b87124e01b1fe46d1a6dc9b6e1f0c645d6d19fe291b820c3a5f3`, 0 placeholders).

## Reproduction

```
python3 scripts/reconstruct_fold20_inputs.py <W_dir> <pub_dir> [<git_ref>]
python3 scripts/verify_fold20_external_20261120.py <W_dir> <pub_dir> <out_json>
```

`<pub_dir>` is the fold20 publication experiment dir (4 published files). The
reconstruction script's default Git ref is `ec24b235f806822086680fee4075820679c78acf`
(byte-identical at main `29926478...` as well). The verifier runs single-process,
serially, in about 21 s; reproduction succeeds iff `<out_json>` is byte-identical to
this README's SHA-256 `5a9bb98f...` (128,175 bytes, gate 1,317).

## Limits

This verification re-examines receipt bookkeeping, machine determinism, input pins
and fail-closed defenses; it closes no S6 row and no five-parent target row. That the
fold20 receipt itself closed 8 rows is the publisher lane's bookkeeping, externally
confirmed here. WIN8-D10 certificates are confined to the eight-stone root's game
tree; REFUTED-D10 is not a LOSS proof. Node counts, solved counts and coverage counts
are not win/loss readings.
**The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and
classes 1/2/4 all remain UNKNOWN.**
