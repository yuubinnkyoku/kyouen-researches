# 2026-11-26 kit-17x: independent blind second census cross-check of the published kit-17 (m49/m50 frontier)

## S1 Context

- Same hourly lane as the kit-17 builder; the builder session was mid-build
  (determinism battery) when this session started. This session therefore did
  NOT build a duplicate kit-17 and did not take over the publication while the
  builder was alive. Instead it built an independent blind second census
  (kit-9b pattern) of the same registered rows and cross-checked the builder's
  frozen output.
- Latest main at start: `1f1577b0` (Part ST complete). Registration source:
  published kit-16 frozen `.out` sha256 `85c04e43...` (commit `f997daca`),
  `future_slice_registration_constants` (34 items) + window proposals + even-m
  z=3m+14 continuation.
- AGENTS.md / research/knowledge/README.md re-read; placement follows the
  current SSOT structure (independent experiment dir + independent log; no
  branch/PR; no changes to knowledge items).

## S2 What was done

1. **Semantics reconstruction + validation**: fresh harness (nested-loop
   enumeration; row = R=z+m+1, S in m..max(m+38,z+2), shapes = 1..3 tokens
   >= m summing to S containing m; separation iff H_canonical(R,X,z) !=
   single_token(S,z,R)). Validated against ALL 49 published kit-16 rows:
   49/49 exact reproduction (shape counts + separation content,
   order-independent).
2. **Blind census of the 49 kit-17 registered rows** (frozen BEFORE reading
   any kit-17 output): 211 separations total.
   - frontier 36th/37st: m=49@z=97 {49,50}@S=99 UP 2v0 EXACT / m=50@z=98
     (50,50)@S=100 UP 2v1 EXACT (scaffold observation 38/38 m=13..50)
   - windows m=47 z{85..92} / m=48 z{86..93}: 16/16 CLEAN
   - 28 ladder next-depth rows: all registered predictions FULL HIT
   - evenlife z=3m+14 (m=14/16/18 @ z=56/62/68): 3/3 EXACT, trio conform 3/3
3. **Cross-check**: builder lane's frozen `.out` (sha `420d1c83...`,
   496,038 B, 4 byte-identical determinism runs) vs this census:
   **49/49 rows identical** (shapes, R, every separation value/collapse/
   direction). Builder lane then published kit-17 itself
   (`d14a89bb`/`2e949ac1`/`f90d5d5e`), record of record unchanged.
4. **Independent fresh audit** (`audit_kit17x.py`, 9 gates, no transform of the
   published audit_kit17.py): battery 2,162 literals recomputed (bad 0),
   anchors 1,210 recomputed (bad 0), census cross-check 49/49, windows 16
   clean, registration provenance (binding texts byte-verbatim in kit-16
   future constants, kit-16 sha verified), binding hits 44/44, census totals
   49/211. AUDIT-PASS. Tamper 3/3 fail-closed: T1 battery literal flip ->
   G0+G2; T2 frontier value flip -> G0+G4 (48/49); T3 anchor flip -> G0+G3.
5. **Determinism of the published census script**: `census_kit17x.py census`
   re-run reproduced the frozen census identically (49/49 rows, 211 seps).

## S3 Published artifacts

`research/experiments/strip-newband-m49m50-blind-second-census-20261126/`:
README.md, engine_block.py (byte-clone `582c93c1...`), census_kit17x.py
(`3abfc53c...`), census_kit17x.out (frozen, `813e7e8b...`), audit_kit17x.py
(`e3da60b8...`). This log. Fetch-back verification: see S5.

## S4 Honest disclosure

1. **Two hand-typed pin constants were wrong in this lane's own scripts**
   (a 65-char kit-16 sha in the audit script; a mistyped pin in the census
   script). Both were caught by this lane's own fail-closed gates before any
   publication byte was written, and fixed by machine extraction
   (sha256sum -> regex). Standing rule re-confirmed: pins are never typed by
   hand.
2. The builder lane's artifacts live in the shared knowledge mount
   (`_kit15-rebuild/build/`); this session read their frozen `.out` for the
   cross-check but never their kit-17 explorer/generator source. The census
   was frozen before the comparison.
3. Row semantics were reconstructed with reference to the published kit-16
   explorer source (SSOT); the enumeration implementation is fresh and was
   validated on all 49 kit-16 rows before any kit-17 measurement.
4. Builder-lane timing: this session observed their determinism battery
   (run1..run4 sha `420d1c83`), derive (3,205 DERIVE-PASS), audits
   (20/20 x2 AUDIT-PASS), then their waves A/B/C publication. No
   interference: this session's work is disjoint (different kit dir, log only
   from this lane).

## S5 Resume notes

- kit-18 registration source (when the next lane picks it up): published
  kit-17 frozen `.out` `420d1c83...` `future_slice_registration_constants`
  (34 items; frontier 38th/39th m=51@z99 / m=52@z100 candidates, windows
  z arithmetic per the frozen prediction text, ladder next-depth, even-m
  z=3m+16 contingent on the kit-17 even-m z=3m+14 outcomes which measured
  3/3 EXACT in BOTH the builder kit and this second census).
- The published kit-17 record of record remains
  `strip-newband-m49m50-frontier-windows-evenlife-20261126/`; this second
  census kit is corroboration, not a replacement.
- 11x11 empty board, all roots, S2, closure classes: UNKNOWN throughout.
  Verdict NOT consumed. K slot not claimed. All results above are finite
  observations; no universal claim.
