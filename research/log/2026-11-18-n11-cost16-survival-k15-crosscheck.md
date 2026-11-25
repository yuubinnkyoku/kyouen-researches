# n11 cost-16 survival curve k=15 extension - independent arithmetic cross-check

Date: 2026-11-18
Lane: verification (n11 long-term lane)
Commits verified: `be21591ef` (k=15, second non-hub root (15,24); I-E verified to still terminate at quads)

## Scope

The parallel lane extended the exact cost-16 ban-survival curve to k=15 while this
lane's k=13/k=14 cross-check was being published. This entry records the
verification-lane cross-check of the k=15 publication and the extension of the
cross-check script (`cost16_survival_k13_k14_crosscheck_20261118.py`, now 21 checks)
to cover k=15. As before, no recomputation: exact BigInt arithmetic over the
published values plus git-blob-sha1 pinning of the three inputs.

## Inputs (git blob sha1 pinned)

- k13: `bcf680f7529a119223f362099ed89685b9e37db6`
- k14: `1f0b64b1d0587333be30b412e87178dd28afec6a`
- k15: `fdf99a93571c8c76d5e97325dd2e92ef4b57ce31` (45,280 bytes; the blob sha1 was computed from the GitHub API text with a method validated against the known k14 pin)

## Checks (11 k=15-specific, all PASS; 21 total in the updated script)

1. Grand-total identity extended: `A_survive(k) + B_survive(k) + kill(k) == 2,966,450,341,680,481,356` for every k=1..15 (constant).
2. `kill(15) - kill(14) == 69,803,318,697,895,551` matches the published marginal and is <= `m15 == 125,028,546,135,310,176` (55.8% of m15).
3. `kill_A(15) + kill_B(15) == kill(15)`; both components monotone through k=15.
4. `A_survive`, `B_survive` strictly decreasing through k=15; `B_survive(15) = 291,965,616,884,613,987` (9.842255%) consistent with the published share.
5. `kill(15) = 1,605,462,614,470,419,817` (54.120664%).
6. rank-15 root membership split: `a_part + b_part == 125,028,546,135,310,176 == m15`.
7. The k15 JSON's own `reproduce_k1_14` check (pass) re-derives all k=1..14 points from the k15 machinery (105 pairs / 455 triples / 1,365 quads), matching the published k14 values this lane verified in the previous entry.
8. The I-E termination claim ("all 3,003 5-subsets structurally zero") is recorded by the k15 JSON's own `quints.all_zero_3003` check; the cross-check script asserts that check is present and passing. The structural argument (every 5-subset contains at least 3 hub roots, forcing hub double/triple coverage; the two non-hub roots (0,15)/(15,24) both cover row 15) is consistent with the published structure section.

## Note

The k15 JSON pins its k14 input at `1f0b64b1...` (the same blob this lane
verified), so the chain of custody is: direct per-d-slice recomputation
(`33abfdb8`) <-> k13/k14 I-E publications <-> k15 publication, with each link
machine-checked. Blob-sha1 pinning from GitHub API text was validated by
recomputing the known k14 pin exactly before pinning the k15 blob.

## Status

Cover-plan combinatorics only. Survival points count minimum cover plans
containing at least one banned root; they are not search costs and imply
nothing about the outcome of the game. Standard 11x11 empty board remains
UNKNOWN; two-stone roots {49,60}/{59,60}, S2 {59,60}, and class 1/2/4 all
remain UNKNOWN.
