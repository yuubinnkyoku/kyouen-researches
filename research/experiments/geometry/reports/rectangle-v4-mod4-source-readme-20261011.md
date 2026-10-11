# Rectangle V4 mod-4 theorem (2026-10-11)

This archive includes the independent exact-integer audit program and its complete output.

Run: `python rectangle_v4_mod4_audit.py`.

The general proof and formulas are committed to GitHub at
`research/experiments/geometry/reports/rectangle-v4-mod4-20261011.md`.

The GitHub connector accepted the proof report but blocked uploading the Python
verifier. This archive is therefore the source of record for the executable audit.

Proof scope: all positive integer rectangle dimensions.
Computational audit scope: 48 rectangles with 1<=w,h<=7 and w*h<=42,
554288 four-point subsets in total. All four involution/fixed-set counts and
both mod-4 formulas agree with direct integer determinant enumeration.
