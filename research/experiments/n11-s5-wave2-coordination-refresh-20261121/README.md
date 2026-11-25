# n11 S5 wave-2 coordination refresh (measurement + fail-closed merger toolkit)

Declared in `research/log/2026-11-21-n11-s5-wave2-refresh-union-merge-fourthcost-probe-single-owner.md` (commit `1f94f501`). Part A is read-only measurement over pinned published artifacts; Part B is tooling only. No searches are performed or claimed here.

## Part A: wave2_refresh.py

`scripts/wave2_refresh.py` re-executes the published class-closure-priority measurement byte-exactly (pinned script + inputs, published-output sha comparison), re-derives the live-class census, registers the concurrent lanes' fixed claimed key sets from machine sources (focus-lane 35 via live incidence with the ccp in-script gate as cross-check, certificate-class exclusive 38, third-cost exclusive 39, sbd fresh corpus 99 + 2 extra rows from the published `corpus-def.json`), verifies the two coordination facts (the 38-key ccp/sbd double-claim; the sbd two extra rows are two-live-parent shared children), computes the two static IF-scenarios (all-claimed-LOSS / all-claimed-parked-UNKNOWN) over the 62 live classes, ranks wave-2 unclaimed targets, and emits the fourth-cost class exclusive unclaimed probe order, cross-checked band-by-band against the declaration note enumeration.

Headline (scheduling facts, no verdicts):
- under all-claimed-LOSS only `1297036692683752448:0` becomes closable;
- the cheapest class with unclaimed exclusive keys is `1297107061427929088:0`: 100 unknown children, 98 unclaimed, 41 exclusive unclaimed, unclaimed proxy 541,959,403; bands 5,041,585 x9 / 5,234,938 x27 / 5,932,112 x5.

Outputs: `output/wave2-priority.json`, `output/wave2-priority.csv`. Inputs are pinned by sha256 inside the script and re-fetched by `scripts/bootstrap.sh`.

## Part B: s5_union_merge.py

Fail-closed S5 verdict-cache union merger (stdlib only). Row gate `s5verdict,<lo>,<hi>,5,<verdict>,<nodes>` with verdict in {1,2}; strict 6-field schema; WIN/LOSS conflicts (within one file or across files) abort with rc=1 and no output; same-value duplicates elided with first-occurrence provenance; nodes-field mismatches recorded in the audit only (nodes are bookkeeping, never verdicts); deterministic sorted output; SHA-256 audit JSON.

Validation battery (`output/merger-validation.json`): built-in selftest (positive dedupe/sort over a shuffled pseudo-corpus, cross-file conflict reject, within-file conflict reject, malformed-verdict reject, double-run determinism); single-file idempotency (the pinned probe-13 cache re-renders byte-identically); chain positive control: the union of the 14 published chain caches (two-target-design base + reply27 JS probes 1..13) reproduces `merged-exact-s5-after-js-probe-13.cache` byte-identically with 74,737 duplicate rows elided, zero conflicts, zero nodes mismatches.

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and third moves 100/108 remain UNKNOWN throughout. Nodes, solver counts, proxies, scenario flags and rankings are scheduling quantities, never verdicts.

## Cross-lane validation

The merger additionally reproduces the third-cost lane's published merged cache increment byte-identically: the union of the pinned probe-13 base cache and the 37 new LOSS rows extracted from `merged-exact-s5-after-class-excl-1.cache` (sha256 `bb4495e0...`) re-renders that exact file (see `output/merger-validation.json`, `output/xval-thirdcost.audit.json`). Zero conflicts, zero nodes mismatches.
