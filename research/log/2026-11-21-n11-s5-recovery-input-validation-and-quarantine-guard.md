# 2026-11-21 — S5 recovery input validation and quarantine guard

- Base main: `b953c7ef2ea2a9b64615e118e4e59f83b09ffbaa`.
- Read `AGENTS.md`, `research/knowledge/README.md`, current K1187/K1181, K0329, the S5 recovery report, and current recovery/merge scripts and tests.
- Baseline isolated run on CT204 tmpfs: existing recovery unit tests **8/8 PASS**.
- A concrete noncanonical-key probe used a vertical D4 reflection of a known safe key. Before the fix, `dfpn_s5_recover.py` returned exit 0 and wrote the alias into the worker cache (`MERGE_OK`). This directly demonstrates the gap, not just static suspicion.
- Updated recovery to use the shared `s5_evidence_policy.is_canonical_safe_s5_key` predicate for every log verdict and every cache row. Existing-cache parsing now requires exactly six CSV fields, S5, a decided WIN/LOSS, nonnegative node count, correct bit ranges/popcount, and canonical quadruple-free geometry; malformed rows no longer silently disappear.
- Recovery now loads the mandatory quarantine registry and filters quarantined keys from both recovered and existing cache before overlap/conflict analysis, preventing withdrawn keys from being reintroduced in worker output.
- Added seven regressions: reflected noncanonical log key, unsafe collinear key, malformed cache row, UNKNOWN cache row, quarantine exclusion before conflict checking, missing registry refusal, and noncanonical existing-cache key refusal. Connected this recovery test file to the existing CI S5 guard step.
- The patch was validated in an isolated `/dev/shm` tree assembled from exact raw main-pinned files; **15 recovery tests and 28 merge tests passed**. A post-fix noncanonical probe returned exit 1 and wrote no output. No dirty repository checkout was modified during validation.
- No solver verdict, certificate, receipt, S6 closure, or 11×11 outcome changed. This is an evidence-ingestion guard only.
