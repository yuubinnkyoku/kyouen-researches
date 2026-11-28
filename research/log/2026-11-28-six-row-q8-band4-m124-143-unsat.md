# six-row q8 band4 m=124..143 all UNSAT — takeover second increment

Continuation of the single-owner takeover (declaration
2026-11-28-six-row-q8-band-closure-m109-370-takeover-single-owner.md; first
increment m=109..123 published earlier today). This increment sweeps
(6,m,8) def-mode widths **m=124..143: all 20 UNSAT**, no INDET, no SAT.
Conflicts 450,706..762,314, sec 53.2..89.2 — the slow upward drift from m~132
continues the band3 trend but stays far under the 230s cap (max 89.2s at
m=138; headroom factor ~2.6).

Witness-free band now **{19..143}**; M_{6,8} = 19 or >= 144. Upper bound
U_{6,8}=371 unchanged. Remaining m=144..370 under the same declaration;
records.jsonl (now 35 records, m=109..143) is append-only and idempotent on
resume.

Scope: finite machine verification per width (row-deficient-maximal
non-existence at m=124..143), kit README census caveats apply. NOT a universal
claim beyond these widths. 11x11 empty board, 19 central-reply roots,
two-stone roots {60,27}, third-move {100,108}, S2, and all closure classes
remain UNKNOWN at all times; conflicts/sec are bookkeeping, not verdicts.

- artifacts: output/band4/records.jsonl + per-width meta/kissat logs
- date: 2026-11-28 (UTC), HEAD at push bff9f44dc
