# n11 central-reply canonical S5 chain integrity: independent TS re-audit (Part DD, 2026-11-24, read-only)

Single-owner read-only audit lane; no compute-lane interference. This experiment publishes an
independent, non-owner verification of the published canonical S5 chain waypoints that every
adoption / reaudit / batch-selection Part builds on:

- CH: n11-centralreply-class5343-loss1-adoption-reaudit-20261123 (6,294 rows, sha256 3124461b...)
- CO: n11-centralreply-class5343-loss7-adoption-reaudit-20261123 (6,301 rows, 854800f3...)
- CU: n11-centralreply-class2251-loss16-adoption-reaudit-20261123 (6,317 rows, 30ddad9d..., BASE at publication time)

Method: a from-scratch sandboxed TypeScript implementation (pure-TS sha256/sha1, FIPS vectors +
256-bit agreement with three independent published pin sources) reads the published chain files
through the GitHub contents API and re-derives every checkable invariant. No Python, no native
host, no solver rerun, no verdict consumption. Full machine-generated report: output/audit-report.json.

## Results: ALL GATES PASS

- Row-level parse of all three waypoints: 6,294 / 6,301 / 6,317 rows, schema-strict (stones=5, verdict in {1,2}), 0 bad rows, 0 duplicate-key verdict conflicts.
- Verdict counts reproduce the published figures exactly (CO: WIN 158 / LOSS 6,143; CU: WIN 158 / LOSS 6,159).
- CH is a strict subset of CO and CO a strict subset of CU (verdict AND nodes identical on every shared key; no key lost).
- The CO-CH delta is exactly the 7-key increment-b28loss7-20261123; the CU-CO delta is exactly the 16-key increment-b29loss16-20261123 (key sets, verdicts, per-key nodes; no increment key already in base).
- b28loss1 increment (aa003) sits inside CH with verdict/nodes agreement.
- Increment nodes sums equal the manifest totals (b28loss7: 38,784,669; b29loss16: 57,463,971).
- Both active quarantine keys (results/n11-s5-evidence-quarantine.json) are absent from all three waypoints.
- Published pins all match when recomputed from the fetched files (CH manifest, CO manifest, CU manifest, internal manifest JSON fields, refresh-script CACHE_SHA_EXPECTED via CU reaudit, completion-log pins).
- Channel integrity: recomputed git blob sha1 == connector-reported sha for every fetched file; all fetched files ASCII-only.

## NOT claimed

No game-search rerun, no canonical-geometry (Board) check, no class-status or coverage claim, no
verdict consumption. The standard 11x11 empty board, the 19 central-reply roots, the two-stone
roots and S2 stay UNKNOWN. Nodes are bookkeeping, never verdicts.

## Files

- scripts/audit_chain_integrity.ts: the executed audit program (sandboxed TS; header comment added for publication, executable code unchanged).
- output/audit-report.json: full machine-generated report of this run.
- output/audit-summary.txt: human-readable summary.
- MANIFEST-sha256.txt: sha256 pins of all published files above.

## Reproduce / extend

Rerun scripts/audit_chain_integrity.ts in a tool sandbox with read-only GitHub access to this repo
(it re-lists and re-resolves all input file names; no hand transcription). To extend to the next
waypoint (e.g. the Part DB 37-LOSS adoption merged cache once published), add the corresponding
experiment dir and pin, and re-check the CO->DB->... subset/delta chain the same way.

Interpretation guard: this audit strengthens chain-trust (independent cross-language, cross-channel
verification of the BASE artifacts); it does not advance or consume any verdict. 11x11 UNKNOWN.
