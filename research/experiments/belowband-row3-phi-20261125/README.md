# Kit: belowband-row3-phi-20261125 (K1318 direct-measurement machine)

Publish-then-execute kit for the **OBS-BBL3-PHI observation packet**:
the frozen (m,W)-Phi ladder-geometry measurement battery for the
below-band THIRD ROW k = z+n-5 family anchors (K1315 next-task 2,
provisional slot K1318).  This is an OBSERVATION packet; it contains
no theorems.  Summary of what the frozen data shows:

```
OBS-BBL3-PHI (frozen measurement battery, waves WA..WZ):
 D1  synthesis, family level: A(n,j,W) = eta(n) + 2j - 2*Phi(m,W)
     with eta(n) = -5(n-4), m = n-j.  WJ: 415 rows, 291 measurements,
     agree 237, violations 0, conform_bad 0, parity anomalies 0,
     law_open 140, suppressed 38.
 D2  tier rules: m=6 Phi=0 (112 sweep rows + witnesses), m=7
     Phi = [c2=0] (168 sweep rows), rule_bad 0.  Visibility boundary
     A_pred == E (z2=0) measured as visible (revision (a)).
 D3  2-recursion Phi([2^a V],m) = Phi(V,m-a): 17 fresh pairs, bad 0
     (handoff typo pair [223]@11 -> [3]@9 corrected before freeze).
 D4/D5 base-family closed forms (pure [3^b], pure [4^c], mixed
     [3^b 4^c] wall rule): 51 fresh rows, mismatch 0.
 D6  pre-registered predictions: 12/12 HIT.
 D7  below-wall suppression arithmetic (A < E => no-2):
     7 rows suppressed_consistent, plateau violations 0.
 DEEP linear tier kappa <= -2 directly measured: Phi = m-6
     ([3^6]@10=4 reached, F=10 construction; []@11=15 via j-shift
     foot j=1 F=8 A=-68; [3^8]@12=6, [3^7]@10=4, [3^6]@9=3).
 FLOOR  m'<=5 open domain: family formula diverges negative but
     measured Phi = 0 flat floor across all word families (WZ:
     30/30 linear fits, floor probe 54/54 zeros).  Formula domain
     closed to m'>=6 (revision (e)).
CONJ-BBL3-A (CONJECTURE, unproven): the synthesis + tier/wall/floor
     rules hold for ALL instances, ALL n >= 3 (K item, conjecture
     grade only).
```

Claims, scopes, the frozen wave/row tables, the machine declaration,
predry records and the honest history (two handoff-log typo fixes,
the workspace loss and byte-exact reconstruction, revision notes
(a)-(f), the [33]@12 j=1 foot choice, the WB F=9 OOM foot swap) live
in the single-owner declaration note published FIRST:

    research/log/2026-11-25-belowband-row3-phi-single-owner-note.md

## Files

- `explore_k1318.py` - exploration machine, waves WA..WZ, embedded
  engine-pin gate (pin
  bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92,
  same published K1138 bytes as the K1282..K1319 chain), deterministic
  single-line JSON output, ~4 min/run (ulimit -v 900000); sha256
  58b9c71e7b88070cb919bd900aaf6541329055aa29397b26c1f916168274c47f.
- `explore_k1318.out` - frozen pre-declaration output of the above
  (140,634 bytes; sha256
  cac6024207c91881960410def67930d29b890dea20431b9e719d0dd469902459).
  Predry: 2 runs byte-identical (cwd run + env -i run with
  PYTHONHASHSEED=12345).
- `engine_block.py` - standalone copy of the same published engine
  block (sha256
  582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0,
  identical bytes to the K1282..K1319 kits).
- `output/` - official run records (published separately after the
  4-run + tamper battery; see detcheck.json).

Standard 11x11 empty board, two-stone roots, S2, classes 1/2/4 stay
UNKNOWN at all times; no verdicts consumed; the frozen measurements
are observations, not proofs.
