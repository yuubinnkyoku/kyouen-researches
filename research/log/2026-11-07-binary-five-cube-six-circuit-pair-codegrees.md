# Binary 5-cube six-point affine circuit pair codegrees (2026-11-07)

## Finite exhaustive result

For any distinct vertices x,y of {0,1}^5 at Hamming distance h, the number of six-element **minimal affinely dependent** sets containing both is:

| h | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| circuits containing a fixed pair | 1150 | 1294 | 1284 | 1294 | 1150 |
| circuits containing 0 and any vertex at distance h | 5750 | 12940 | 12840 | 6470 | 1150 |

A separate six-subset loop containing vertex 0 counted **7830** circuits. The independent double-count identity is `sum_h binom(5,h) lambda(h)=5*7830=39150`. Vertex transitivity implies total circuit count `32*7830/6=41760`, agreeing with the prior full enumeration, but the distance-resolved data are new.

## Exact procedure

Enumerate all `binom(31,5)=169911` sets consisting of 0 and five other vertices. Form the 6-by-6 augmented binary-coordinate matrix, compute rank over F_101, and require rank < 6. For each of the six five-element deletions, require augmented rank exactly 5. For every accepted set, increment the distance bucket of each of its five nonzero vertices. Divide each bucket by `binom(5,h)`: coordinate permutations fixing 0 act transitively on the vertices of a given Hamming weight, so the quotient is the codegree of any pair at that distance (translation by XOR maps any first vertex to 0 and preserves affine dependencies via coordinate reflections).

The modular test is **exact over Q**: all nonzero maximal minors after subtracting a row are determinants of 0,±1 matrices of order <=5, and Hadamard bounds their absolute values by `5^(5/2)<56<101`. Thus no nonzero minor vanishes accidentally modulo 101.

## Boundary

This is a finite complete enumeration for d=5, not a dimension-uniform formula or the missing d=6 full-support-six count. It provides an additional independent audit invariant for the d=5 circuit generator, and a lower-dimensional regression target for the K6 pipeline.
