# Kit: belowband-toprow-20261125 (K1313 audit machine)

Publish-then-execute audit kit for **T-BB**: the single-coordinate collapse of the
below-band TOP ROW k = z+n-3 of every n-mountain face (all n >= 2, all z >= 0, all
descending heap multisets X):

```
u := E + z + n - 4          (E := 2*max(X) - sum(X), K1311 convention)
u >= 1  ->  H = [E odd]     (python parity, E negative included)
u == 0  ->  H = 2
u <= -1 ->  H = 1 - [E odd]
```

Full claims, hand proofs (L-BR1 base lemma, typed children, existence lemma,
6-region mex algebra U1/U2/H/I1/I2, single strong induction on R), the frozen
pre-declaration exploration waves X1..X10, the machine declaration (battery
counts, 13-mode mutation table, predry sha) and the honest history live in the
single-owner declaration note published FIRST:

    research/log/2026-11-25-belowband-toprow-single-owner-note.md

## Files

- `verify_k1313.py` — audit machine, 12 batteries, 28,024 declared comparisons,
  expected overall_bad 0. Startup sha gate on the embedded engine block
  (pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92,
  same published K1138 bytes as the K1282..K1312 chain).
- `engine_block.py` — standalone copy of the same published engine block
  (sha256 582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0).
- `explore_k1313.py`, `explore_k1313.out` — frozen pre-declaration exploration
  (waves X1..X10, all bad 0; see declaration note §3;
  explore_k1313.out sha256 5ce1ec3a65ecb3b708bc0d0b2303807ee9dc0846d0e0089f9e4df33ab62d74fa).
- `predry/` — predry runs (cwd PYTHONHASHSEED random / 1; isolated tree
  env -i PYTHONHASHSEED 99 / 7), all rc=0, stdout byte-identical:
  sha256 a634658cd7baa418b2474e4793700aca2b8d7b8e2b652d7be312a31b89c4b78e.
  `.info` files are volatile stderr (battery progress + elapsed); the .out
  stdout JSON is the deterministic artifact.
- `output/` — official runs + tamper records + detcheck.json + MANIFEST
  (pushed after fetch-back byte verification; protocol as K1309/K1311/K1312).

## Running

    python3 verify_k1313.py                       # clean run, expect rc 0
    python3 verify_k1313.py --tamper-engine      # expect rc 2 (sha gate)
    python3 verify_k1313.py --tamper=MODE        # 12 modes, expect rc 1

Stdout is deterministic JSON (byte-identical across hash seeds and isolated
trees); stderr carries volatile progress only. Censuses are consistency
checks; the universality of T-BB/L-BR1 is carried by the hand proofs in the
declaration note. Standard disclaimer: the 11x11 empty board, two-stone roots,
S2 and classes 1/2/4 remain UNKNOWN at all times; no verdicts consumed.
