# 2026-11-17 n11 class2-lane cost76c: bit61 legal-defense audit and driver guard v2

## Background

The current cost76c claim selects raw bit61 as the primary WIN7-D10 certificate target and bit99 as fallback. Bit113 is REFUTED-D10 and excluded. The corrected marginal audit says bit61 and bit99 each touch the same one open manifest row; bit61 has fewer raw sweep nodes, but raw search nodes are not certificate-extraction cost.

This work starts from main commit 353cda65aa4550ff159ba760130371fccb9c474a. The raw six-stone child is 00000000010000809002000001000000.

## Exact bit61 root geometry

Adding bit61 without canonicalizing gives raw seven-stone root:

0000000001000080b002000001000000

Occupied cells are [24,49,60,61,63,71,88]. All 35 four-stone subsets have nonzero exact determinant, so the root itself is safe.

The raw-root defense list was independently re-derived in three ways:

- New pivoted Bareiss 4x4 determinant implementation.
- Translated 3x3 determinant on differences of (x,y,x²+y²), with the expected sign relation to the 4x4 determinant.
- Existing legal_candidates.py, pinned by Git blob SHA 8e97082c42838c7a4a4b6d2dd235276c8d43ab9a.

Direct candidate testing and union-of-triple forbidden-mask enumeration agree. The result is 55 legal defenses and 59 illegal empty cells. Every legal extension remains safe; every illegal cell has a concrete zero-determinant triple witness. The reproducible JSON stores the complete legal list and a hash of the witness map.

Artifacts:
- scripts/audit_cost76c_bit61_root_legal_moves_20261117.py
- output/class2-lane-cost76c-bit61-root-legal-moves-20261117.json

The JSON SHA-256 is f28d8f4ddf57978fc67787f12f1a956b53f43600d58caf2e051ca62bb8a2fbd1.

## Driver defect found and fixed

The previous cert_driver76c.ts accepted any nonempty, unique, in-range move list. It did not require that the list equal every legal defense of the raw seven-stone root. Therefore an omitted legal defense or an included illegal cell could still reach extractBatch and, if the listed subtrees completed, be written with the full-certificate header. The independent verifier should reject such a file, but the extraction driver itself did not fail closed at the root-coverage boundary.

The driver now independently derives the complete legal-defense list from the raw child|bit root using exact Bareiss 4x4 determinants. It rejects before calling the extractor unless the supplied list is exactly the ascending legal list. It also checks that perMove keys exactly match that list, certificate rows have the expected board/move syntax and move range, and board keys are unique (not merely full row strings). Existing fatal, cap, fbt_drops, row-count and atomic no-overwrite checks remain.

The same driver path handles bit99 as a fallback. The mock test pins its 65-defense list as well as bit61's 55-defense list.

## Regression result

Node 22.16.0, --experimental-strip-types:

- 14/14 mock cases passed.
- Two valid full lists (bit61 and bit99) reach the mocked extractor and produce the expected raw root header.
- Twelve invalid or incomplete cases are rejected: missing defense, illegal defense, duplicate defense, unsorted defense, missing bit99 defense, fatal result, fbt_drops, missing rows, incomplete per-move result, malformed row, duplicate board key, and occupied selected bit.
- The extractor mock is used; the actual certificate extractor was not invoked.

The test file is scripts/test_cert_driver76c_guard.mjs. This is a driver-safety regression, not a certificate verification.

## Boundary and next action

No WIN7 certificate was extracted in this run, no receipt was folded, and no new game-theoretic verdict was established. Run the guarded driver for bit61 with all 55 raw-root defenses, then independently verify the resulting certificate, repeat extraction in a fresh process for byte identity, recompute its marginal against canonical head1472, and scan for WIN/LOSS conflicts before folding. Bit99 remains fallback only.

The standard 11x11 empty root, both two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.
