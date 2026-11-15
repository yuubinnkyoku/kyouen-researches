# 2026-11-15 n11 published-fold chain audit — second independent verification of the v3 extension (class2 lane)

Class2 lane (11x11 two-stone-root proof-support lane). The parallel lane landed the v3
extension of the published-fold-chain whole-chain audit (`b9d6b7c6`, endpoint 75d, 95 pins,
569 roots). This session had — concurrently and before seeing that landing — extended the
same v1 audit script to the same 75d endpoint as an independent derivation: the extension
constants (77b/77c/75d head pins, own-branch fold counts 557/565/569, own-baseline links,
canonical-line entries, endpoint numbers) were all re-derived from the published head JSONs,
fold scripts and completed claims. This log records the resulting **second independent
verification**: the landed v3 audit reproduces byte-exact in a fresh mirror, and the two
independently extended implementations agree on every substantive control.

## 1. Landed v3 audit reproduced byte-exact (fresh mirror, no shared state)

The v3 script (`audit_published_chain_roots_independent_20261115.py`, blob `17431197…`,
54,548 B) and v3 audit JSON (blob `9ae57954…`, 86,060 B) were fetched from main and the
script re-executed in a mirror rebuilt from the codeload tarball plus this session's local
75d fold artifacts (the same corpus the fold scripts themselves assert against):
`AUDIT PASSED`, and the regenerated JSON is **byte-identical to the pushed blob, two
consecutive runs**.

## 2. Two independently extended implementations, identical substantive results

The independently extended implementation was kept as
`audit_published_chain_roots_second_independent_20261115.py` (blob `794c027c…`, 55,423 B);
its v2 output is published as
`class2-lane-published-chain-roots-independent-audit-v2-20261115.json` (blob `db0916c0…`,
85,324 B, md5 `d067ab29…`; 6 consecutive runs byte-identical). Control-by-control
comparison of the v2 and v3 audit JSONs:

- cumulative published-root inventory per post-70e head (17 entries, 497@1233 → 569@75d,
  every own-branch lineage matching the published own claim): **identical**
- D4 orbit structure (569 roots / 558 orbits / 11 twin pairs, full twin_analysis with
  provenance): **identical**
- head arithmetic (69 heads, per-head entries, classifications, quote-status counts,
  0 anomalies; the 70f quote erratum and the 74g pointer-differs case unchanged):
  **identical**
- canonical-line hex-level exactly-once (63 manifest hexes over 1233 → 1296, total mim 63
  == distinct 63 == 1296 − 1233, zero multi-claims, per-head breakdown): **identical**
- child-orbit closure (24 heads, each child closed by exactly one receipt record,
  consistent with the declared `child_closed_by_bit`): **identical**
- convention-external receipts (single benign `cost72_fold` record, D4 twin of an
  inventoried orbit): **identical**
- per-record geometry (434 receipt records + 40 group records, 0 anomalies, the single
  cost63cd published-hex erratum): **identical**
- 75d endpoint record (1296/6551/517468/4821/381191, receipts 4, child closed at bit 12):
  **identical**
- interpretation guard (bookkeeping only; 11x11 / two-stone root / S2 / classes 1, 2, 4
  UNKNOWN): **identical**

Differences are presentation-only and both favor the v3 canonical audit: v3 pins 95 (the
v2 pin proposals 71c/70f/73g/70g now pinned) while the second implementation pins 91 and
carries the same four shas as *computed* pin proposals — independently recomputed here
with **identical values** (`61af2eb3…`/`4d0f130e…`/`e4fb98dc…`/`73890fe3…`), confirming the
pins; v3 crosschecks all four endpoint claims (77a/77b/77c/75d) while the second
implementation re-crosschecks the 75d claim only. The second implementation additionally
asserts the 75d claim's `parents_lost_rows` record — the target parent losing both the
cost-75 child row `00000000000040801202000000200000` and the cost-77 child row
`00000000100000801202000000200000` (the bit-92 cross-cover of the parallel cost-77d
sweep's in-flight child row) plus `parents_after` = 11 rows / 866 — independently
reconfirming the warm-hygiene fact recorded in the 75d fold log.

## Collision handling

Both extensions were authored concurrently against the same v1 baseline; the parallel
landing (v3, same script path, same output filename) won the race. Per the lane's
collision rules the in-flight duplicate extension was NOT pushed over the landed files:
the v1 script path and the v1/v3 audit JSON filename are untouched, and the second
implementation is published under its own filenames instead.

## Interpretation guard

Bookkeeping audit over published receipts and head records only. Solved counts measure
manifest coverage, not the game-theoretic value of any position. WIN7 certificates prove
a win within depth 10 from the individual 7-stone roots only. **11x11 empty board /
two-stone root {49,60} / S2 {59,60} / class 1 / class 2 / class 4 all remain UNKNOWN.**

## Machine-readable record

- Second implementation: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_published_chain_roots_second_independent_20261115.py`
  — git blob sha `794c027c1af03a23fcb98aaa3b5f935167fe89e4`, 55423 bytes.
- v2 audit JSON (second implementation output): `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-chain-roots-independent-audit-v2-20261115.json`
  — git blob sha `db0916c0ecb64a475537bc0ac9028c73dd3f5294`, 85324 bytes,
  md5 `d067ab299c4b8c4a423f7b4b230b87cf`, schema
  `n11-class2-lane-published-chain-roots-independent-audit-20261115-v2`.
- Canonical audit (v3): unchanged as landed in `b9d6b7c6` — script blob `17431197…`,
  JSON blob `9ae57954…`.

## Resume notes

- When the cost-77d fold lands (warm-hygiene required: its child row is already closed at
  head 1296 by the 75d bit-92 cross-cover), extending either audit script to the 77d
  endpoint is now a mechanical v4 step (POST70E_PINS/ORDER + own_claim + own_baseline +
  one CANONICAL_LINE entry + endpoint entry); the second implementation should be
  extended in lockstep so the double-verification property is preserved.
- The second-verification comparison here is a one-time record; the v3 audit remains the
  single canonical audit file for future checkpoints.
