# 2026-11-13 n11 milestone-5: published reproducer source audit

Baseline main: b81f69001202f7a966872d91c883c648a5eaa43d (2026-11-13 07:07 JST observation). Inspected AGENTS.md, research/knowledge/README.md, K0023, K0783, the milestone-5 S7 reuse experiment README and its purported reproducer source.

## Finding (repository artifact, not a game verdict)

The file `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/ms5_s7_reuse_analysis.ts` on main contains **only a comment header and a pointer to git history/log**; it has no executable program body. Consequently, the README/K0783 description of this path as a deterministic reproducer/verifier cannot currently be followed from a clean checkout of main. This does not refute the earlier reported independent derivation or its recorded MD5; it identifies a *reproducibility gap* in the published artifact.

A future repair should restore the exact executed source (or a clean-room implementation), include input paths and invocation, and run a regression that reproduces the manifest MD5 `0e95a438dbcb486368393de9c73fc21e` and the 8,763/396/8,367 counts. Until then, treat the reported full independent regeneration as a recorded computational result, not as independently rerunnable from the currently linked source.

No game positions were solved in this audit. 11x11 empty board, S2 {49,60} and S2 {59,60}: **UNKNOWN**.
