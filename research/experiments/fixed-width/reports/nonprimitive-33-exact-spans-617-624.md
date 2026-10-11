# F(33): exact-span modular exclusions W=617..624 (2026-10-10)

## Result and scope

Let F(k) denote the smallest span W=max(y_i)-min(y_i)+1 of k distinct integer horizontal rows, each containing two distinct integer lattice points on a single real circle, where the gcd of the selected row differences is >=2. **For each W=617,618,...,624, no such configuration with k=33 exists.** This is a computer-assisted exhaustive modular proof, without a bound on the circle's coefficients or x-coordinates.

Combined with the *previously produced but not merged into main* exclusions W<=616, the cumulative result is **625 <= F(33) <= 743**. The upper-bound witness is x^2+y^2=143650. The present package includes the preceding proof package as `PRIOR-F33-bounds-617-743.zip`. The eight new exact-span exclusions are independently meaningful and do not depend on the earlier exclusions.

## Mathematical reduction

Translate the minimum selected row to y=0. Write the real circle as x^2+y^2+Bx+Cy+D=0. Its two integer x-roots at y=0 imply B,D are integers. Let g>=2 be the gcd of all selected row differences. The rows are y=gi, where 0<=i<h=(W-1)/g+1, both endpoints are selected, and the selected i's have gcd 1. By Vieta's product of the two integer x-roots, C*g*i is an integer for every selected i, so a=g*C is an integer. Let H=B^2-4D and d_i be the difference of the two integer roots at y=gi. Then

    g^2*d_i^2 + (2*g^2*i+a)^2 = g^2*H+a^2.

For every modulus p coprime to g, dividing by g^2 yields residues c,n (mod p) with

    n-(2*g*i+c)^2 in QR(p)

for every selected i. Here QR includes zero. Allowing different c,n for different moduli only relaxes the original problem. The exact gcd and endpoint condition imply g | (W-1) and 2<=g<=floor((W-1)/32). Exhaust all such g. For each p enumerate all p^2 choices of (c,n), construct permitted row masks, intersect the masks across moduli, discard masks with fewer than 33 rows or missing endpoints, and deduplicate. If no masks survive for any g, the real-circle configuration is impossible.

## Exhaustive verification

The verifier uses the moduli 9,11,7,49,31,23,19,43,47,37,41,53,59 (skip any p not coprime to g). Bitsets contain 384 bits; for these widths, h<=312. Two C++ builds construct the quadratic-residue masks differently: a direct (c,n,i) loop and a transposed (c,i,n) loop. They share the mask intersection, hashing, and deduplication logic, so this is not a fully independent end-to-end formal verification.

| W | Number of modulus stages | Result | Notes |
|---:|---:|---|---|
| 617 | 21 | PASS | g=2,4,7,8,11,14 all eliminated |
| 618 | 0 | PASS | W-1=617 prime; no eligible g |
| 619 | 17 | PASS | g=2,3,6 eliminated |
| 620 | 0 | PASS | W-1=619 prime; no eligible g |
| 621 | 19 | PASS | g=2,4,5,10 eliminated |
| 622 | 9 | PASS | g=3,9 eliminated |
| 623 | 7 | PASS | g=2 eliminated |
| 624 | 3 | PASS | g=7 eliminated |

All eight widths were completed in the standard implementation and in the `DIRECT_RESIDUES` implementation. The normal/direct logs are identical for W=617,618,620,621,622,623,624; W=619 was verified with different modulus orders, so only their final PASS conclusions match. Every log is included in `output/f33-exact-spans-617-624/`.

Reproduce from repository root:

```sh
g++ -std=c++20 -O3 research/experiments/fixed-width/scripts/verify_nonprimitive_33_exact_span_617_624.cpp -o /tmp/f33-a
g++ -std=c++20 -O3 -DDIRECT_RESIDUES research/experiments/fixed-width/scripts/verify_nonprimitive_33_exact_span_617_624.cpp -o /tmp/f33-b
for w in $(seq 617 624); do
  /tmp/f33-a "$w" 33 > "/tmp/f33-a-$w.log"
  /tmp/f33-b "$w" 33 > "/tmp/f33-b-$w.log"
  diff -u "/tmp/f33-a-$w.log" "/tmp/f33-b-$w.log"
done
```

The last diff command should produce no differences with the new verifier's common modulus order. The original W=619 log in this package is from the prior order; its intermediate lines are therefore not byte-identical to the DIRECT log, but the fresh reproduction will be. The proof's trust boundary is the mathematical necessary-condition reduction and the finite C++ exhaustive mask intersection, not a Lean proof. **W=625 is not excluded by this result.**

Repository integration: direct main write was attempted via the GitHub connector but rejected by safety checks. The artifacts here are not yet merged into main or promoted into a knowledge item.
