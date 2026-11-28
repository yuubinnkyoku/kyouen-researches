# six-row q8 band4 (m=109..123) all UNSAT — fast-lane takeover first increment

Direct continuation of the takeover declared in
2026-11-28-six-row-q8-band-closure-m109-370-takeover-single-owner.md
(prior declaration 7bc633a6 stalled 8 days; fresh-env calibration m=108
conflicts 675,709 bit-exact disclosed there). This increment sweeps the
(6,m,8) def-mode widths m=109..123 with genfast3.js + kissat 4.0.4 (230s cap):

**all 15 widths UNSAT**, no INDET, no SAT. Per-width conflicts range
555,697..703,128 (vs band3 m=60..108 range 0.45M..1.05M — flat, no difficulty
wall in sight). m=109 was additionally run twice from cold: conflicts 640,938
bit-exact both runs (cold-pair determinism check, same convention as the 5x27
kit part 3).

With band3 (K1134) this extends the witness-free band to **{19..123}**, i.e.
M_{6,8} = 19 or >= 124. Upper bound U_{6,8}=371 unchanged (K0318/K0806).
Remaining: m=124..370 under the same single-owner declaration; records.jsonl
in output/band4/ is append-only and the sweep skips widths already recorded,
so any resumed session is idempotent.

Scope: finite machine verification per width (row-deficient-maximal
non-existence at each width 109..123), same census-completeness caveat as the
kit README (q>=w+2 chord-pair argument, CNF byte-identity and instance-identity
calibrations, kissat correctness). NOT a universal claim beyond these widths.
11x11 empty board, its 19 central-reply roots, two-stone roots {60,27},
third-move {100,108}, S2, and all closure classes remain UNKNOWN at all times.
conflicts/sec are bookkeeping, not verdicts.

- artifacts: output/band4/records.jsonl (15 records) + per-width meta/kissat logs
- date: 2026-11-28 (UTC)
