# N11 Unreflected Consolidated Bundle Import (2026-10-12)

## Source and provenance

- Source archive: `n11-unreflected-consolidated-20261012.zip`, 148,287,116 bytes, SHA-256 `1ccbf01ae834fc8544d9acbc3aeece628440d38c369926559d546891c50efd3e`.
- The source is preserved byte-for-byte as four numbered parts under `research/archive/source-snapshot-2026-10-12/`. `n11-unreflected-consolidated-20261012.zip.parts.json` records each part hash and the original archive hash for reassembly verification.
- Verified all 73 nested ZIPs against `ARCHIVE_MANIFEST.csv` for both byte length and SHA-256. The nested historical archives remain inside the preserved source bundle; they were not unpacked into active experiment directories.
- The bundle records an earlier checked main commit (`386d8de7...`). Integration was performed on `b39f2d7f...`; each selected source-file blob precondition still matched, including the unchanged S5 quarantine policy.
- The bundle's README and helper scripts were reviewed as source material. User request and repository instructions determined the integration scope.

## Integrated changes

- Updated `dfpn_s5_merge.sh` to serialize cooperative merges with a stable sidecar lock, retain rows already committed to the output, reject conflicting evidence and unsafe aliases, and preserve existing permission bits. Duplicate exact rows retain the lower node count.
- Updated `dfpn_s5_recover.py` to parse replay CSV rows with floating-point wall time, keep UNKNOWN out of exact cache output, and refuse contradictory observations or cache entries.
- Updated the S5 evidence router to validate the complete S6 child-key boundary before deriving an outcome and to detect disagreements among independent proof, direct S5, and saved S6 evidence. Updated its caller and regression fixtures.
- Added recovery regression tests. No 11x11 game outcome was inferred or changed by this import.

## Validation

- Merge safety tests: 26 passed under WSL/Linux Bash.
- Recovery tests: 8 passed.
- Hierarchical strategy tests: 15 passed.
- `uv sync --locked`: passed.
- `uv run --locked python tools/knowledge/check.py`: 408 items, 0 errors, 0 warnings.
- `uv run --locked python -m unittest discover -s tools/knowledge/tests`: 33 passed.
- `uv run --locked python tools/knowledge/build.py`: generated six views from 408 current items in the integrated worktree. `git diff --exit-code -- README.md research/knowledge/generated` passed, so the generated views and README already matched.
- A HEAD-only archive lacks 29 existing untracked experiment artifacts referenced by already tracked K0396, K0403, K0405, and K0407-K0410. These paths were absent from both supplied bundles and were preserved unstaged. The successful temporary build snapshot overlaid the current workspace items and their artifacts; it did not resolve this pre-existing clean-checkout gap.
