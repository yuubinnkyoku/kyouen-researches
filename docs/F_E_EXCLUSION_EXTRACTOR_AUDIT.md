# F-E historical exclusion extractor audit

Freeze base: `224f0dae89f95bfafa20290e872d96b9567dc6d7`.

Before generating the holdout manifest, the current extractor at `f1ab74e` needs two coverage fixes.

1. `.tsv` is classified as text, but `parse_csv()` uses the default comma delimiter. Therefore TSV label records can be silently missed.
2. The accepted text extensions omit source files such as `.py`, `.cpp`, `.inc`, `.rs`. Historical scripts can contain hard-coded states paired with WIN/LOSS labels, so restricting the history audit to result/document extensions does not establish the preregistered claim that previously labelled four-stone orbits were excluded.

Required correction before manifest freeze:

- Parse `.tsv` with a tab delimiter.
- Include source-code text blobs in the historical scan, or prove separately that no reachable source blob contains an explicit four-stone state paired with WIN/LOSS.
- Record a `review_candidate_blobs` class for decoded text blobs containing both a four-integer state-shaped token and WIN/LOSS but yielding no unambiguous parsed record. These must be reviewed before the clean universe is frozen.
- Do not generate or inspect the 36-state holdout manifest until this audit reaches zero unresolved candidates.

This is a pre-outcome amendment: it changes only leakage detection and does not use candidate holdout labels or outcomes.
