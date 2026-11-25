# Kit: belowband-row2-20261125 (K1314 audit machine)

Publish-then-execute audit kit for **T-BB2**: the universal law of the
below-band SECOND ROW k = z+n-4 of every n-mountain face (all n >= 3, all
z >= 0, all descending heap multisets X), together with its n=2 second
rows (L-2 plane law, PB2 wall law), the base lemmas L-BR2 (published
K0832 single-token closed-form slice) and L-0, and the K0832 3-token
transient-band corollaries A/B/C (k=0 slice), all as one closed packet:

```
T-BB2 (n >= 3):   E <= z+n-4 -> H = [E odd]   /  E == z+n-3 -> 2
                  /  E >= z+n-2 -> H = 1-[E odd]
                  exceptions: (1,1,1)@z=0 -> 0, (1,1,1)@z=1 -> 2 only;
                  (E,w) merge (w := E+z+n-5) across all n >= 3 with the only
                  multivalue cells (-1,-3)->{0,1}, (-1,-2)->{1,2}.
L-2  (n=2, plane Z>=1, k=Z-2): beds 2 iff (a,Z)=(1,1) else 0;
     pairs Z<=g-2 -> [g even] / Z=g-1 -> 2 / Z>=g -> [g odd].
PB2  (n=2, plane 0, k=-2):     g<=2 -> [g odd] / g=3 -> 2 / g>=4 -> [g even].
L-BR2 (n=1, k=Z-3):            R=0 -> 0; 2 iff (Z==x>=2) or (1,3) or (3,1);
                               Z>=x+1 -> [x odd]; Z<=x-1 -> [x even].
```

Full claims, hand proofs (typed children, existence lemmas (E1)-(E4),
5-region D-coordinate mex table, interface families F1-F5, single strong
induction on R), the frozen pre-declaration exploration waves WA..WG,
the machine declaration (battery counts, 15-mode tamper table, predry
sha) and the honest history live in the single-owner declaration note
published FIRST:

    research/log/2026-11-25-belowband-row2-single-owner-note.md

## Files

- `verify_k1314.py` — audit machine, 14 batteries, 40,513 declared
  comparisons, expected overall_bad 0. Startup sha gate on the embedded
  engine block (pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92,
  same published K1138 bytes as the K1282..K1313 chain).
- `engine_block.py` — standalone copy of the same published engine block
  (sha256 582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0).
- `explore_k1314.py`, `explore_k1314.out` — frozen pre-declaration
  exploration (waves WA..WG, all bad 0; see declaration note §3;
  explore_k1314.out sha256 197ca679c79a3b211072fc37118ef5a499baa4243ecfceb4839ee92661cad7f0).
- `predry/` — predry runs (cwd PYTHONHASHSEED random / 1; isolated tree
  env -i PYTHONHASHSEED 99 / 7), all rc=0, stdout byte-identical:
  sha256 4c2102c689e3b7848fcb1708a4a8c0f865e81d31c1a2118e4d8cbd598bee1240.
  `.info` files are volatile stderr (battery progress + elapsed); the
  .out stdout JSON is the deterministic artifact.
- `output/` — official runs + tamper records + detcheck.json + MANIFEST
  (pushed after fetch-back byte verification; protocol as
  K1309/K1311/K1312/K1313).

## Running

    python3 verify_k1314.py                       # clean run, expect rc 0
    python3 verify_k1314.py --tamper-engine      # expect rc 2 (sha gate)
    python3 verify_k1314.py --tamper=MODE        # 14 modes, expect rc 1

Stdout is deterministic JSON (byte-identical across hash seeds and
isolated trees); stderr carries volatile progress only. Censuses are
consistency checks; the universality of T-BB2/L-2/PB2 is carried by the
hand proofs in the declaration note. The unified conjecture U (k >= 1
slices, rows k <= z+n-5) remains OPEN (O-BBL3). Standard disclaimer: the
11x11 empty board, two-stone roots, S2 and classes 1/2/4 remain UNKNOWN
at all times; no verdicts consumed.
