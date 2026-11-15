# 5x25 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

Date: 2026-11-15. Fast lane, successor of K0836 (5x24). Extends the (5,7) witness-free
sweep one width on the same class-split SAT machinery (K0816/K0821/K0834/K0835/K0836
protocol). This sweep completed across an execution-environment outage: the prior
session finished 17 direct classes + 2 lex=H cross-checks + 10 krow instances (29 raw
logs, byte-exact on main); the resuming session regenerated all 56 CNFs with the
byte-identical encoders, re-ran c2 (259,243) and 0k4 (755,207) as cross-run
calibration (both bit-exact with the main logs), and completed the 26 k=5 x minpos
instances plus the positive control.

## Claim

1. On the 5x25 integer grid (q=7), for every one of the 19 row-mirror-canonical deficiency
   classes D ⊆ {0..4} (canonical representatives of the 31 non-empty subsets under
   y -> 4-y), the class-split SAT instance — rows in D hold at most 5 stones (unit ¬rowGe[y]),
   rows outside D hold exactly 6 (unit rowGe[y]; safety caps every row at 6 since a row is
   a line of length 25 ≥ q), safety ≤ 6 stones per census curve, maximality (every empty
   cell covered by a ≥6-stone curve) — has **no solution**:
   - 17/19 classes directly **UNSAT** (kissat 4.0.4, exit 20; hardest {0,1}: 535,454
     conflicts / 17.5 s; {2}: 259,243; direct total 3,534,969 conflicts — the
     m=22→m=25 direct difficulty trend is monotonically decreasing: 5,256,816 →
     4,673,619 → 4,160,006 → 3,534,969).
   - {0} and {1}: decided by the **complete k × minpos decomposition** (the
     K0816/K0821/K0834/K0835/K0836 protocol): k = 0..4 (exact deficient-row stone count, 5
     instances each; hardest {1} k=4: 786,695 / {0} k=4: 755,207) and k = 5 ×
     minpos = 0..12 (13 instances each — the sound bound grows to floor((m−1)/2) = 12
     at m = 25: x1 ≥ 13 forces the mirror's leftmost column 24−x5 ≤ 24−13 = 11 ≤ 12).
     All 36 sub-instances **UNSAT** (hardest {1} k=5 mp=0: 2,021,531 conflicts / 83.04 s;
     {0} k=5 mp=0: 1,620,423 / 64.6 s — both below their m=24 counterparts 2,282,668 /
     1,745,942).
   - Total conflicts across the 53 deciding instances: **15,521,919** (17 direct:
     3,534,969; 36 decomposition: 11,986,950); the two lex=H cross-checks add 681,980
     (records.jsonl total 16,203,899). No SAT, no INDET among the deciding instances.
2. Coverage: the exact deficiency set D = {rows with ≤ q-2 stones} is non-empty for every
   deficient maximal safe configuration and the exact-D instances partition them
   (K0818/K0816 class logic, brute-force-validated on small boards in K0818); the
   k×minpos decomposition is exhaustive: k = 0..5 partitions the deficient row's stone
   count, and for k = 5 the minpos split pins the **leftmost stone of the first deficient
   row at column exactly P**; every configuration or its column mirror has leftmost stone
   column ≤ 12 at m = 25 (if x1 ≥ 13 then the mirror has leftmost column 24−x5 ≤
   24−13 = 11); the column mirror preserves row occupancy, hence the class. Therefore
   **no row-deficient maximal safe configuration exists on 5x25**; every maximal safe
   configuration on 5x25 has 30 stones (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19), K0816 (5x20), K0821 (5x21), K0834 (5x22), K0835
   (5x23), K0836 (5x24) — all witness-free — and K0332 (29-stone witness at 5x18, least
   witness width 18): the witness-free width set of (5,7) is **{19, 20, 21, 22, 23, 24,
   25}**, so in the set form **M_{5,7} ∈ {19,...,25} or M_{5,7} ≥ 26**, sharpened (the
   K0821-audit convention, applied to the extended free set) to **M_{5,7} = 19 or
   M_{5,7} ≥ 27**: widths 20–25 are verified witness-free and cannot be the threshold,
   and M = 26 would require a witness at the verified witness-free width 25, so the next
   possible witness sits at w ≥ 26, forcing M = w + 1 ≥ 27. The upper bound 158
   (K0332/K0024 substitution) is unchanged. The witness-search frontier moves to 5x26.

## Method

`sat3.js` class-split encoder on the K0810 census (circleABC integer triples) and
sequential-counter core, decided by the official kissat 4.0.4 linux-amd64 release binary
(arminbiere/kissat rel-4.0.4 asset). 2-worker queue runs with per-instance `timeout`
60–260 s; CNF regeneration + solve + records by mkcnf.sh / qrun.sh / mkrecords5725.js
(scripts/ dir, deterministic; byte-identical encoders to the K0834/K0835/K0836 lanes —
the sat.js/sat2.js/sat3.js copies are byte-identical to the K0836 m=24 lane scripts).

## Verification

- **Positive control**: 5x18 q=7 class {0} **SAT** — 343,134 conflicts / 10.6 s,
  **bit-exact with the K0821, K0834, K0835 and K0836 lane control runs** (fourth
  cross-lane reproduction); decoded model 29 stones rows (5,6,6,6,6), census-free
  `verifyConfig` PASS (K0332 witness board rediscovered end-to-end).
- **Cross-encoding**: {0,1} and {2} re-encoded with --lex=H (lex-leader over column
  reflection — class-preserving, hence sound) are UNSAT again (391,407 / 290,573
  conflicts).
- **Cross-run determinism (environment-outage resume)**: the 29 raw logs produced by
  the interrupted prior session are byte-exact on main (git blob sha verified); the
  resuming session regenerated all 56 CNFs from the byte-identical encoders and
  re-ran c2 (259,243 conflicts) and 0k4 (755,207 conflicts), matching the prior
  session's logs bit-exactly — the second time this protocol demonstrates cross-reset
  bit-exactness (the first was the K0835 mid-sweep reset), plus the fourth cross-lane
  bit-exact reproduction of the 343,134 control.

## Scope and limits

Finite machine verification up to the correctness of the K0810 census, the class-split
encoding and k×minpos decomposition (protocol brute-force-validated in K0816/K0818), and
kissat 4.0.4; not a number-theoretic proof. Persistence at m ≥ 26 remains open: exact
M_{5,7} needs witness-free verification for all widths up to the K0332/K0024 bound
U=158 or a universal tail argument. The witness frontier moves to 5x26: a witness there
gives M ≥ 27; witness-free there extends the free set to {19,...,26}. The difficulty
trend suggests m=26 stays in the class-split lane's practical range (deciding totals
20,916,467 → 17,349,736 → 15,521,919 for m=23→24→25; the minpos sound bound grows to
floor((25)/2)=12 at m=26). The 11x11 empty board, two-stone root {49,60}, S2 {59,60},
class 2 and class 4 are unaffected and remain UNKNOWN.
