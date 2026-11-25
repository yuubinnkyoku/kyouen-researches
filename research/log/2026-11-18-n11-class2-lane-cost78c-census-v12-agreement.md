# 2026-11-18 n11 class2-lane: cost78c census v12 cross-lane agreement check (PASS 7/7)

## Scope

The presweep census v12 (commit
`56d81b077362e71a2cb0ec232470b25c4fd06ca9`, git blob
`8e64d55250242a557c954ad5bad8c993bacd354b`) marks the cost-78c row swept as
its 15th verdict map and selects the census v11 runner-up (cost 79) as the
next sweep target. The census was published before the cost78c BigInt
third-implementation re-verification batch (commit
`2d447098547c74d89b7d8147eeefe7c77fd4e4e7`), so it cannot reference it; this
check closes that direction: every 78c fact the census relies on is
cross-agreed here against the BigInt-reverified bytes population. Follows
the check_cost73j/check_cost73k cross-lane agreement pattern. All four
compared files are blob-pinned: census v12, claim v5
(`1850832186ba9c8715624094f05d67aa4eb10f0b`), the BigInt batch output
(`7d97599186e6c76b8566d5f5703d71915224a129`) and the in-band manifest
(`b7fe519e923c6170e836f71e3f084f73219319d5`).

No verdict is created, no row is closed, no frontier number changes. The
11x11 empty board, the two-stone roots {49,60} and {59,60}, S2 {59,60},
class 1, class 2 and class 4 all remain UNKNOWN.

## Checks (7/7 PASS, deterministic)

1. chain_head: census v12 `1473/174/6375/504596/4648/368510` == the claim
   v5 basis_head.
2. Verdict map position: cost78c is the 15th (last) of the 15
   new_verdict_maps.
3. Win bits: census 78c win7_d10_bits == claim v5 win7_d10_bits == the
   BigInt batch entry bits == [1,4,9,30,49,69,75,79,100,114,116].
4. Refuted bits: census 78c refuted_d10_bits == claim v5 refuted_d10_bits
   (67 bits), capped 0, win/refuted disjoint, union == the 78
   legal_candidates.
5. Totals: census cross_checks 78c_manifest_totals == manifest totals ==
   claim v5 certificates.totals == BigInt batch summary (rows 614,003 /
   extraction_nodes 77,967,826 / published_bytes 22,223,603 / fbt_drops 0 /
   capped 0).
6. BigInt roots: all 11 BigInt-re-verified roots are child | (1 << win_bit),
   each verifier_status PASS and manifest_record_agreement True.
7. Next target: selected_target cost 79 (census v11 runner-up), parent ==
   the cost-78c s5 parent, sweep_bits + confirmation_bits ==
   legal_candidates == 79.

The census 78c cross_checks statements (78c_certificates 11/11 published,
78c_receipt_fold pending behind the 66i/66j/69j/71e/72d/73i/73j/73k/73l
folds, 78c_manifest_roots_are_child_or_bit, the 11/11
win_bits_claim_audit_manifest_agreement) were also re-read and asserted.

Determinism: two consecutive runs produced byte-identical output
(md5 `0bb84795a0ae7ea50612e7b86ca917d9`).

## Interpretation guard

- The census 78c verdict map carries REFUTED-D10 for 67 bits; REFUTED-D10
  is NOT a LOSS proof of those roots.
- 73i certificates remain unpublished on main as of this session; the 73i
  BigInt reverification stays prohibited until that publication.
- The next sweep target per the census v12 selection policy is the cost-79
  row (s6 `00000000000000c09002000200000000`); its sweep is a sweep lane's
  work, not this check's.
