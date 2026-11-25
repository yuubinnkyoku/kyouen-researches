# F(33): exact-span exclusion at widths 595..616 (2026-10-10)

## Result

Let F(k) be the smallest span W=max(y_i)-min(y_i)+1 of k distinct integer horizontal rows, each containing two distinct integer points on a common real circle, with gcd of the k row differences >=2. **For every W=595,...,616, such a set of 33 rows is impossible.** The proof is a finite exhaustive modular exclusion, without any bound on the circle's coefficients or horizontal coordinates.

Combined with the *previously produced but not yet merged* full-width exclusions W<=560 and exact-span exclusions W=561..594, this improves the conditional cumulative bound to **617 <= F(33) <= 743**. The upper bound uses x²+y²=143650, checked independently by integer square roots. The new exclusions W=595..616 are self-contained; the combined lower bound depends on the previous proof files bundled as a separate ZIP.

## Mathematical reduction

Translate the lowest chosen row to y=0 and write the circle as x²+y²+Bx+Cy+D=0. Its two integer roots at y=0 imply B,D are integers. Let g>=2 be the gcd of differences of chosen row numbers. Write selected rows y=gi, including i=0 and i=h-1, h=(W-1)/g+1. Vieta's product relation at each selected row gives gCi integer; since the i's have gcd 1, a=gC is an integer. If d_i is the difference of the two integer x-roots and H=B²-4D, then

    g²*d_i² + (2*g²*i+a)² = g²*H + a².

For any modulus p coprime to g, there therefore exist residues c,n mod p such that n-(2gi+c)² is a quadratic residue (including 0) for *all* selected i. Each modulus is allowed its own c,n, a relaxation which can only create spurious solutions. Since both extreme selected rows occur, g divides W-1 and 2<=g<=floor((W-1)/32). Exhaust all these g, all p² residue pairs (c,n), and intersections of the permitted row masks, retaining only masks of at least 33 rows containing both endpoints. If every g is eliminated, the original circle is impossible regardless of its coefficients.

Moduli, in order: 9,11,7,49,19,31,23,43,47,37,41,53,59. Skip p with gcd(p,g)>1. All 22 widths ended with PASS, comprising 240 reported modulus stages. Widths 600,602,608,614 have no eligible g, so their exclusion is purely arithmetic. The entire per-modulus state count and maximum retained row count are in the output log.

## Reproduction and independent check

    g++ -std=c++20 -O3 research/experiments/fixed-width/scripts/verify_nonprimitive_33_exact_span_595_616.cpp -o /tmp/f33-a
    g++ -std=c++20 -O3 -DDIRECT_RESIDUES research/experiments/fixed-width/scripts/verify_nonprimitive_33_exact_span_595_616.cpp -o /tmp/f33-b
    for w in $(seq 595 616); do
      /tmp/f33-a "$w" 33 > /tmp/a.log
      /tmp/f33-b "$w" 33 > /tmp/b.log
      diff -u /tmp/a.log /tmp/b.log
    done

The two builds generate quadratic-residue masks in different ways; all 22 full outputs matched byte-for-byte. The state intersection and hash implementations are shared, so this is not a fully independent formal verification. All integer arithmetic is exact. This is a computer-assisted exhaustive proof for the stated finite set of spans, not a proof that any W>=617 is feasible or impossible. W=617 was attempted but did not finish within the bounded run; its partial state is **not** a result.

Repository status: GitHub main direct-write was attempted and rejected by a safety check. This package is an unmerged artifact, not an accepted knowledge item.
