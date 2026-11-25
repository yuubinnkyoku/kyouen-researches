# 2026-11-14 n11 class2 cost-58b WIN7 certificate: independent BigInt audit

Source commit: 9983c53349b6df6639622cfeaee96f0a84cc6d15.

The commit adds a strategy certificate for root
00000000000000803202000000042000 (the cost-58 S6 child
00000000000000803202000000002000 plus bit 18). The certificate was independently
replayed before treating it as reusable evidence.

## Independent verification

Source certificate:

- Path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost58b-certificates/bit18-root-00000000000000803202000000042000.cert
- Git blob SHA-1: da591d87cdef5c43426847811a37be99c6fcf8cb
- 1,208,076 bytes; 33,461 nonempty lines; 33,459 strategy rows.
- Header: n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS.

The verification core was run in a separate V8 execution context, without
importing the search engine or repository verifier. It used a BigInt 3x3-minor
Laplace expansion of det([x^2+y^2,x,y,1]), not the repository verifier's
Number/Bareiss implementation. No floating point or verdict cache was used.
All legal moves were recomputed from triples; every opponent reply was expanded;
every winner strategy move was checked; and the consumed winner-state union was
compared with the complete strategy-row set.

Results:

- Root: 7 stones; all 35 four-point subsets pass the exact determinant safety check.
- Root loser mobility: 48; all **48/48** eight-stone sub-roots PASS.
- Sum of visited states across sub-roots: 71,903 (sum across traversals, not a
  globally deduplicated count).
- Winner-state visits: 46,839; unique consumed winner states: **33,459**.
- Terminal leaves: 9,855; opponent edges: 68,210.
- Terminal stone range: **13–17**.
- Strategy-row union: missing **0**, extra **0**.
- Exact geometry work: 16,439 distinct triples cached; 1,939,802 BigInt
  determinant evaluations.

The reusable standalone verifier is
research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost56a_bigint_certificate.mjs.
Pass this certificate path and root with --cert and --root; the default arguments
still point to cost-56a. As with cost-56a, the verification core was executed in
this run's V8 context; the checked-in Node CLI itself has not yet been run under
Node 22 here.

## Six-stone parent lifts

The seven one-stone deletions of the root produce four entries in the published
S6 worklist:

| Winning move from parent | Canonical S6 parent | Worklist cost | Classes |
|---:|---|---:|---:|
| 13 | 00000000000000803202000000040000 | 73 | 2 |
| 18 | 00000000000000803202000000002000 | 58 | 6 |
| 57 | 00000000000000801802000000084000 | 65 | 4 |
| 61 | 00000000000000801202000000042000 | 77 | 6 |

For each matched parent, the removed stone is a legal move to the certified
seven-stone WIN7 root, so that S6 parent is a first-player win. The cost-58
parent is explicitly present as the cheapest remaining child of S5
00000000000000803202000000000000 in the after-cost-56a top-candidate file:
that S5 currently has 39 remaining S6 orbits and edge cost 2,657. This receipt
therefore removes at least that child locally, giving 38 / 2,599.

The other three parent incidences are not counted as marginal until the full
receipt union is recomputed. The global after-cost-56a frontier remains the
last published baseline; no after-cost-58b global totals are asserted here.

## Interpretation guard

This is a verified WIN7 root and local first-player wins for its matched S6
parents. It does not settle the five-stone S5 target, S2 {59,60}, two-stone root
{49,60}, or the empty 11x11 board. All remain UNKNOWN.

## Artifacts

- Certificate: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost58b-certificates/bit18-root-00000000000000803202000000042000.cert
- Independent verifier: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost56a_bigint_certificate.mjs
- Machine-readable result: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost58b-independent-audit-20261114.json
- Last global frontier: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost56a-recompute-20261114.json
