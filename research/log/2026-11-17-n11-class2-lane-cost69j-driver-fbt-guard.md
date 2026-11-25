# 2026-11-17: cost69j certificate driver fails closed on extractor drops

## Finding

The published `cert_driver69j.ts` wrote `res.rows` whenever rows existed and `res.fatal` was falsy. It did not reject `res.fbt_drops > 0`. A bounded forbidden-bit table can therefore produce a non-fatal partial row set that the driver would write as if it were a complete certificate.

This is a concrete guard gap, not evidence that any of the six already published cost69j certificates is invalid: their recorded extraction summaries all have `fbt_drops=0` and `fatal=null`, and their independent verification records remain unchanged. The earlier cost76c saturation incident makes a fail-closed driver condition worthwhile.

## Change

`scripts/cert_driver69j.ts` now writes no certificate unless all three conditions hold:

- `res.rows` is an array;
- `res.fatal` is falsy;
- `res.fbt_drops === 0`.

On any failed condition it prints a refusal message, sets a nonzero process exit code, and returns before `writeFileSync`.

The change affects only future extraction output gating. It does not rewrite the six published certificate files, their hashes, the manifest, or any verdict map.

## Validation boundary

- Source-level inspection confirms the write is after the three fail-closed checks.
- The GitHub contents update succeeded on `main` (commit `24ab6ef86afdf0fb4a6d9f1c0c2fbfe35566d8e9`).
- Runtime extraction, a mocked saturation test, the independent certificate verifier, and repository CI were not run in this session; do not mark them passed.

## Research status

No new WIN7/REFUTED-D10 verdict or receipt was created. The six cost69j WIN7-D10 certificates remain individual seven-stone-root certificates; their receipt fold remains gated behind the pending cost76c/cost66i/cost66j folds. REFUTED-D10 is not a LOSS proof. Standard 11×11 remains UNKNOWN.
