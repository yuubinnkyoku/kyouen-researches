# 2026-11-21 n11 residual72 36-root worker partition candidate

Latest main was refreshed during the run: `a45a626d1b5517f66ad3a3b0b792b1d395dde6ed`. `AGENTS.md`, `research/knowledge/README.md`, K1193/K1192, the 36-root three-ply census, and the single-owner notes for the depth-10 sweep were read.

The 36-root depth-10 sweep remains a single-owner task; its experiment directory still contains preparation files only, with no published output directory. I did not start probes or touch its driver, runner, roots, or assignment.

Using the pinned published three-ply pairwise-overlap table, I ran a deterministic balanced-partition heuristic. The strided split’s cross-worker pairwise overlap is 4,193; a 9-root-per-worker candidate reduces it to 2,000 (52.3015%) while keeping D4 and raw 10-stone loads within 7.51% spread. An exhaustive single-swap neighborhood scan under the 8% D4-load cap found 222 feasible swaps and no improvement. This is a local heuristic result, not a global optimum.

An attempted full regeneration of the exact 10-stone class-to-root memberships timed out. The candidate is therefore audited against the published pairwise table only; no exact worker-local class-copy count, TT hit rate, speedup, or search-cost reduction is claimed.

Follow-up: leave the active sweep untouched. Once it completes, instrument or recover actual TT-hit/reuse counts and evaluate whether the candidate improves measured worker sharing without harming balance. No new verdict/certificate/receipt closure occurred; standard 11×11 remains UNKNOWN.