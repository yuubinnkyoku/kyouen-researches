# Kit: belowband-row3-20261125 (K1315 observation machine)

Publish-then-execute kit for the **O-BBL3 entry packet**: the frozen
class-layered collapse census of the below-band THIRD ROW
k = z+n-5 of the n-mountain faces (all swept heap grids), together with
the L-BR3 single-token transcription slice and the CONJ-BBL3 unifying
conjecture (stated, NOT proven).  This is an OBSERVATION packet; it
contains no theorems.  Summary of what the frozen data shows:

```
L-BR3  (n=1, k=z-4, GRID-VERIFIED x,z<=30): 924/924 cells equal the
       published K0832 closed form single_token(x,z,x+z-4).
OBS-BBL3 (census on frozen grids, w := E+z, classes (n,j)):
 (a) raw (E,z) layer: NO collapse (multivalue cells
     n=3:17, 4:21, 5:48, 6:61, 7:90) -> layer by (n,j) instead;
 (b) class layer: (6,0),(6,1),(7,1)..(7,7) exactly-collapsed in sweep;
     (7,0) has 33 multivalue cells = the tail-family conflict band
     w in [-17,-15];
 (c) per tail-family 3-piece law V = 2[w=A] / [E even][w<A] /
     [E odd][w>A]: ZERO genuine violations n=4..8 (5,779 rows incl.
     n=8 464); declared off-level outliers: 8 rows (n=4), 2 rows (n=5);
     n=3 wall clans (t+3,t,1),(t+2,t,2): 36 rows, z=0 cell absorbed
     into the right plateau;
 (d) anchors: eta(n) = 1,0,-5,-10,-15/-17 (n=7 splits: m2=2 -> -15,
     m2>=3 -> -17); A_{n,j} shape eta+2j-2*[j>=n-3]; n=8 j=0 ladder
     c2>=2 -> -20 / c2=1 -> -22 / m2=3 -> -24 / m2>=4 -> -26;
     n=8 j=1: -18|-20; j=2: -16;
 (e) suppression: line at z* = A-E <= 0 -> whole window [E odd];
     zero unexplained missing-line rows at n>=4 in sweep; all-2s-top
     clans ((2^4,1,1), (2,2,1^4), (3,3,1^4)) lose the mountain in
     window while (3,3,2,2,1,1)/(4,4,1,1,1,1) show the line at z*=0.
CONJ-BBL3 (CONJECTURE, unproven): the 3-piece law with per-family
anchor holds for ALL instances, ALL n >= 3.
```

Claims, scopes, the frozen wave tables, the machine declaration
(5 batteries, 1,307 declared comparisons, 6 tamper modes), predry
records and the honest history live in the single-owner declaration
note published FIRST:

    research/log/2026-11-25-belowband-row3-single-owner-note.md

## Files

- `verify_k1315.py` - audit machine, 5 batteries, 1,307 declared
  comparisons, expected overall_bad 0.  Startup sha gate on the
  embedded engine block (pin
  bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92,
  same published K1138 bytes as the K1282..K1314 chain).  Tamper
  modes: --tamper-engine (rc 2), --tamper=law|cells|xen|anchors|census
  (rc 1, single-battery contamination as declared).
- `engine_block.py` - standalone copy of the same published engine
  block (sha256
  582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0,
  identical bytes to the K1282..K1314 kits).
- `explore_k1315.py`, `explore_k1315.out` - frozen pre-declaration
  exploration (waves WA..WG, deterministic JSON, ~146 s/run; sha256
  29f7080ae59ff9852b62a8c2f6d4300b3db2c713dae90589c7d9e09eda37e195 /
  558ed202ebdd0d80b6159856a836842dd10e73807d37c6eb392437f1175032eb).
- `output/` - official run records (see detcheck.json).

Standard 11x11 empty board, two-stone roots, S2, classes 1/2/4 stay
UNKNOWN at all times; no verdicts consumed; the frozen censuses are
observations, not proofs.
