# six-row q8 band4 m=144..158 all UNSAT — takeover third increment

Continuation of the single-owner takeover (declaration
2026-11-28-six-row-q8-band-closure-m109-370-takeover-single-owner.md; increments
m=109..123 and m=124..143 published earlier today). This increment sweeps
(6,m,8) def-mode widths **m=144..158: all 15 UNSAT**, no INDET, no SAT.
Conflicts 511,094..705,219, sec 78.0..98.2 — upward drift continues, cap
headroom now ~2.3x at the worst width (m=144, 98.2s vs 230s cap).

Environment note: the execution sandbox was reset mid-increment after m=149;
the kit was rebuilt from repo main (all md5 pins re-verified: genfast3
12c2bd9c..., kissat 3a5eba83..., sat.js 0cc6021a..., sat2.js 282ae832...,
verify_witness.py 0530d166...) and m=144..149 were re-run from cold. The re-runs
reproduced the pre-reset conflicts bit-exact (m=145: 585,152; m=146: 584,216;
m=147: 705,219; m=148: 636,885; m=149: 651,618), an unplanned cross-restart
cold-pair determinism check.

Witness-free band now **{19..158}**; M_{6,8} = 19 or >= 159. Upper bound
U_{6,8}=371 unchanged. Remaining m=159..370 under the same declaration.

Scope: finite machine verification per width (row-deficient-maximal
non-existence at m=144..158), kit README census caveats apply. NOT a universal
claim beyond these widths. 11x11 empty board, 19 central-reply roots,
two-stone roots {60,27}, third-move {100,108}, S2, and all closure classes
remain UNKNOWN at all times; conflicts/sec are bookkeeping, not verdicts.

- artifacts: output/band4/records.jsonl (50 records, m=109..158) + per-width
  meta/kissat logs
- date: 2026-11-28 (UTC), HEAD at push 03f52eba8
