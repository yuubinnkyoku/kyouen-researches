# 36-root worker partition candidate

## Scope

This is an exploratory allocation study using the already-published 36-root, three-ply D4 overlap census. It does not run game search, depth-10 probes, certificate extraction, or receipt folding. The active 36-root depth-10 sweep remains owned by its declared lane and is not modified.

## Input

- Source: `research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json`
- SHA-256: `94fdb0c6e3503f1e9d19aaaf345f4478157c5a44374f10642c52325f346c2023`
- Git blob SHA-1: `730bc378f93c0de8a2ac1bf7941941e4d5a24798`
- 53,914 bytes; published source commit `c74dfd0c0b2c8795236e3064153531f5c7452d01`

## Method

The existing assignment is the driver’s `roots[W::4]` strided split. A deterministic simulated-annealing search tried 10 restarts × 120,000 swaps, with 500 randomization swaps after the first restart, seed `0xD41F11`, and a hard limit of 8% spread in summed per-root D4 memberships. The objective was to minimize the published pairwise overlap weight assigned across workers. A complete scan of feasible one-root swaps then checked the candidate’s local neighborhood.

## Result

- Baseline cross-worker pairwise overlap: 4,193 / 5,435 (77.1481%).
- Candidate cross-worker pairwise overlap: 2,000 / 5,435 (36.7985%), a 52.3015% reduction.
- Within-worker pairwise overlap changes from 1,242 to 3,435.
- The candidate keeps 9 roots per worker; D4-membership and raw 10-stone loads have 7.5067% and 7.5061% spread respectively (baseline: 6.6558% and 6.6547%).
- 222 feasible single-root swaps were checked under the 8% D4-load cap; none improves the 2,000 objective. This is a one-swap local optimum, not a global optimum.

The candidate groups and machine-readable metrics are in `output/worker-partition-candidate-20261121.json`. The checked-in script audits the fixed candidate and its one-swap neighborhood; it does not rerun the simulated-annealing search. Run `node scripts/audit_worker_partition_candidate_20261121.mjs` from the repository root to regenerate the audit output from the pinned census.

## Interpretation boundary

Pairwise geometric overlap is only a proxy for potential local-table reuse. A shared D4 class does not establish identical search depth, proof boundary, or an actual DFPN transposition-table hit. An exact per-root 10-stone class-membership regeneration attempt timed out; therefore no exact worker-local class-copy count is claimed.

Do not change the active sweep’s assignment based on this result alone. After the 36-root depth-10 sweep completes, measure actual TT hit/reuse and compare it with this candidate before considering a partition change. No new WIN/LOSS verdict, certificate, or closed receipt row is produced.