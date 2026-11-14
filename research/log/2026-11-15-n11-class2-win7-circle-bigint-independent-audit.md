# 2026-11-15: independent class2 WIN7 certificate replay and parallel-frontier reconciliation

Audited main snapshot: `0b9e53d492605dcb2b6f5b224351dc0050c4eb60`.

## 1. Independent replay of 18 WIN7 certificates

The audit covers 18 seven-stone strategy certificates:

- cost-63e original: bits 28, 90, 97;
- cost-63e warm rebuild: bits 42, 73, 100, 116, 120;
- cost-65h: bits 7, 109, 24;
- cost-65i: bits 7, 43, 99;
- cost-67b: bits 17, 117, 109;
- cost-65g warm rebuild: bit 44.

The geometry implementation is independent of the solver and repository verifier. For a non-collinear triple it solves the circle equation with 3x3 Cramer determinants; for a collinear triple it uses an exact integer cross-product line test. All arithmetic is BigInt, with no floating point, solver, verdict cache, or verifier imports.

For each certificate the replay checked:
- the exact header, root, sorted unique strategy rows, and seven-stone root;
- root safety and every legal opponent reply;
- every winner-to-move state has a legal strategy move;
- every opponent-to-move state expands all legal replies;
- every terminal is opponent-stuck at the correct parity;
- the consumed winner-state set equals the certificate row set exactly.

All **18/18 certificates PASS**. Across them:
- 630,410 strategy rows;
- 896 root replies/sub-roots;
- 1,405,024 summed sub-root visited states;
- 207,232 terminal visits;
- 1,302,337 opponent-reply edges;
- every terminal has 13–17 stones;
- all 18 roots are distinct under D4.

The visited-state and terminal figures are sums over certificate sub-roots, not a globally deduplicated state count. The standalone Node script checks the Git blob SHA for all 18 files and the published SHA-256 for the 17 files that have a SHA-256 manifest. The cost-65g bit-44 warm file had no published SHA-256 manifest at this snapshot.

## 2. Exact union of the cost-63e-warm and cost-67b frontier branches

Both published recomputations start from the same after-cost-65h+65i baseline:

- 991 solved S6 manifest positions;
- 6,856 unique S6 positions remaining;
- remaining edge cost 540,177;
- open-class demand 5,126 S6 / 403,900 edge cost.

The cost-63e warm branch contributes six distinct marginal manifest keys and reduces cost by 432. The cost-67b branch contributes two distinct marginal manifest keys and reduces cost by 142. The two key sets are disjoint.

The exact union is therefore:

- **999 solved S6**;
- **6,848 remaining S6**;
- **539,603 remaining edge cost**;
- open-class demand **5,118 S6 / 403,326 edge cost**.

The second class-2 S5 `00000000000000803202000000000000` has the same 15-child / cost-1,072 baseline in both branches. The cost-63e-warm branch removes one cost-71 child; the cost-67b branch removes a different cost-67 child. Their union leaves **13 children / cost 934**.

The three cost-67b certificates (bits 17, 117, 109) share the S6 parent `00000000000000803202000020000000` and give three distinct legal winning seventh moves. The bit-109 certificate also lifts a second D4-canonical S6 manifest parent `00000000080000809002000000000800`. Thus cost-67b closes two distinct S6 manifest orbits, not three. The cost-65g bit-44 certificate is independently verified, but its S6 parent `00000000000000803202000000000004` is already absent from the remaining second-class-2 child list and is not counted as a new frontier closure.

## 3. cost-68c raw sweep: all 68 candidates present, metadata not finalized

The nine raw batches contain 68 unique candidate rows, exactly matching the 68-bit claim set, with no duplicates or omissions. All nine pilot controls reproduce the 3,402-node, `loss=false`, uncapped control.

- WIN7-D10 candidates (`loss=true`): bits 11, 21, 24, 53, 118 — 5;
- REFUTED-D10 candidates (`loss=false`): 63;
- capped: 0;
- total search nodes: 104,482,623.

This is a completed raw sweep, but the checked-in inflight JSON still has `status: in_flight`, and the finalized `class2-lane-cost68c-sweep-20261114.json` summary is absent. No WIN7 certificate has yet been published for these five candidates, so no S6 frontier change is credited from cost-68c. REFUTED-D10 is not a LOSS proof.

## Reproduction and limits

- Verifier and reconciliation script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_class2_win7_circle_bigint.mjs`
- Machine-readable output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-win7-certificates-circle-bigint-audit-20261115.json`

The in-run checks were executed in the tool V8 runtime against GitHub blob/file contents. The standalone Node script is committed for local reproduction but was not run from a repository checkout in this run because the checkout attempt failed at DNS resolution. Knowledge checks and generated-view rebuilds were therefore not run.

K0783 remains on its earlier cost-56a/cost-58b narrative. This log does not replace that knowledge item; no knowledge item or generated view was edited.

## Interpretation guard

These are individual seven-stone WIN certificates, two S6 parent lifts from cost-67b, and frontier bookkeeping. They do not solve the S5 blocker classes, S2 `{59,60}`, the two-stone root `{49,60}`, or the standard 11x11 empty root. All remain **UNKNOWN**.
