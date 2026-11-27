# 2026-11-28 Eight-row q=10, 8x26: single-deficiency krow/minpos decomposition — single-owner declaration (publish-then-execute)

## Scope

- Board 8x26, q=10. Frontier M_{8,10} in [26,940]; widths 26..39 unresolved
  (m=26 all four published encodings INDET; m=27..31 probed INDET 60-270s;
  m=32..39 unswept). No active declaration on 8x26 q=10 was found on main at
  declaration time (only the completed m=26 two-edit-surgery negative kit of
  2026-11-27).
- This lane owns the **single-deficiency family decomposition of 8x26**:
  canonical deficiency classes {0},{1},{2},{3} mod V (V flips 0<->7, 1<->6,
  2<->5, 3<->4, so these four cover all 8 deficient-row positions),
  krow=y:8 (deficient row exactly 8 stones, all other rows exactly 9),
  minpos=P in 0..13 (leftmost stone of the deficient row, sound H-split),
  lex=H symmetry breaking.
- No m>=27 claim. No absence claim: INDET pieces are honest negatives.
- If any piece is SAT: immediate stop, decode + 3-system witness verification
  (sat.js verifyConfig + verify_frac.py + integer conic spot-check),
  report as an M_{8,10} >= 27 band extension.

## Machinery (pinned, identical to the six-row q=6 m=26 class-split kit)

- sat3.js md5 d03f908ea99ba819caee2a6fbb471c1b / sat2.js md5 282ae832efa0080127c6c153e65e1c3c / sat.js md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c
  (byte-clones of research/experiments/six-row-q6-m26-class-split-20261127/scripts).
- kissat 4.0.4 linux-amd64 sha256 21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1 (official release asset, verified).
- Pre-declaration calibration (disclosed): 6x25 q=6 class {2} krow=2:4 minpos=11
  SAT **3,574,244 conflicts — the published K1217 positive-control value
  reproduced bit-exact** on this host.

## Run discipline

- 280s kissat cap per piece, several pieces per bash call within budget.
- Determinism: at least one piece rerun byte-identical (conflicts).
- Declaration-time main HEAD: 400f7e862c81628f850f8ab599a7b4067dc1076f. All 8x26 pieces run after this commit.
- verdict NOT consumed. Standard 11x11 empty board, 19 central-reply roots,
  two-stone root {60,27}, third move {100,108}, S2, all closure classes:
  UNKNOWN at all times; conflict counts are bookkeeping.
