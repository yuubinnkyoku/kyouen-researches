# Part EU completion log: euwin2 third WIN canonical adoption (2026-11-26)

All waves landed.  Part EU closes complete; the canonical merged exact-S5
chain head formally advances to the EU merged cache
`merged-exact-s5-chain-plus-euwin2-20261125.cache`
(sha256 3ba486086703b9f44a0c685d7d5b45fab80f86760f2cd032a8dc18a2690233d6,
6,767 rows, WIN 188 / LOSS 6,579), the new BASE for every later adoption /
reaudit / extractor.

## Wave chain (each push preceded by a fresh main refetch; each verified by
commit-pinned fetch-back against the regenerated local bytes)

* A  declaration  7136d22c  (research/log/2026-11-25-part-eu-win2-adoption-declaration.md)
* B  kit scripts 3/3: 9675e519 (merger 90711961 byte-clone) / f8d6550b (maker f2ae97a1) / feae2f6d (extractor aaf13bdc)
* C  adoption outputs f7e607b1 (regenerated post-declaration at a third environment
  after the owner-typo outage retraction, resume log baa8a0c0):
  increment d9365d80, increments-manifest 793f68c5, merged 3ba48608,
  merge-audits 9f807c95 x3 - all byte-matched the declared pins
* D0 repair decision + repaired kit efa482fd
  (research/log/2026-11-26-part-eu-scen-refresh-pin-repair.md):
  SCEN_REFRESH_SHA supersession a377eea0 -> published fork 6dc24c15
  (3-region-diff byte-clone of the ER refresh 6c91e0ce; 4/4 declared
  refresh output pins reproduced byte-identically: 2b70bb55 / 59a4c85f /
  cfc2bfe1 / 397a4379); kit extractor repaired aaf13bdc -> 9bc5f06a in
  exactly two disclosed hunks; fetch-back 3/3
* D  reaudit + deltas ee191e73: reaudit outputs 2b70bb55 (refresh-summary
  34,192 B) / 59a4c85f (closure-classes 805 rows) / cfc2bfe1 (per-root-
  coverage 588 B) + decomp-deltas-euwin2-adoption.json 8d4a5743 (8,806 B);
  fetch-back 4/4; probe-worklist NOT published (3,717,712 B, regen pin
  397a4379, size policy)
* E  close-out d50ccda1: kit README run record + MANIFEST-sha256 (14
  published kit files byte-pinned sha+size, README/MANIFEST self-excluded
  per convention, repair disclosed in the header); fetch-back 2/2;
  MANIFEST re-check 14/14
* F  completion log = this commit

## State after the Part (all machine-verified by the repaired extractor's
full battery, rc=0 twice, stdout byte-identical; and container-invariant
vs the throwaway diagnostic f353dbe5)

* canonical BASE: 3ba48608... (6,767 rows WIN 188 / LOSS 6,579); the
  Part ER head 9c4dd94e... remains published history;
* census: class_status_counts 34,436/84/39/390 -> 34,430/90/39/390 with
  EXACTLY 6 UNKNOWN->excluded_now flips {12846, 12875, 13801, 30308,
  30326, 30282} - the adopted keys' still-unknown owner classes; class
  30345 NOT double-flipping (EP-flipped; cost-unknown 7 -> 5 on the
  51-raw/50-cost Board boundary); class 30354 untouched (97/97, 96
  static, its 10 win_hit groups unchanged with 97 unknown children on
  both sides);
* closure-classes.csv 805 -> 805, zero rows left/entered, zero
  groups_served churn; unknown_now churn only 30345 (7->5); rank churn
  only the two-row swap {30345: 8->7, 20421: 7->8};
* update8 frozen baseline static (union 31,859 / resolved 260 /
  remaining 31,505 / free groups 131); Board verification 39/39 both
  sides; per-root free_now/uncovered thirds identical at every root;
  individual greedy deltas only at roots 12 (2850->2848) and 36
  (3007->3005); joint greedy 36,619 static; group_best_options_nonfree
  2,105 static; worklist 64,309 -> 64,307.  All re-selection bookkeeping;
  no coverage claim anywhere.

## The repair provenance (honest, permanent record)

The declaration's SCEN_REFRESH_SHA a377eea0 pointed at bytes that were
never published and are unrecoverable; the diagnostic pin 353f15d3
(f353dbe5) was likewise throwaway-local.  The Part closed via the
disclosed option-2 repair (efa482fd): the published fork 6dc24c15 is a
machine-verified 3-region byte-clone of the published ER refresh
6c91e0ce (all computation bytes identical), and the repaired extractor
9bc5f06a differs from wave-B aaf13bdc in exactly two disclosed hunks.
The guarantee is carried by (a) the fork's byte-verified relation to the
pinned ER refresh and (b) its outputs byte-matching the declaration's
pre-registered, docstring-insensitive pins - not by any preimage claim on
a377eea0.

## Verdict scope and guarantees (unchanged)

Consumed in this Part: exactly the 2 ET-gate-verified WIN rows ai007
(class 30345, s5_index 441292, nodes 16,090,493) and ai040 (class 30345,
s5_index 899584, nodes 20,711,023) - b38 15M basis honest-EXHAUSTED,
ES-30M-resolved, Part ET C++ scrutiny gate 9/9 GATE-PASS, audit
2c6d7441.  Consuming a WIN label asserts NO root verdict.  NOT consumed:
the 4 ES-30M-resolved LOSS rows (ai024/ai030/ai038/ai041; EM-pattern
territory), the b38 15M honest-EXHAUSTED labels (honest UNKNOWN at 15M;
same-condition re-probe ban untouched), b018 (dual-class, scrutiny-owner
pending), the k04 sixth-cost WIN, and every other unconsumed probe-level
WIN.  The standard 11x11 empty board and every central-reply root stay
UNKNOWN; nodes are bookkeeping; no free/secured-coverage claim is made
anywhere.  Next natural step recorded by the lanes: the EV adoption Part
(b018/d002/e002/f017, gate-verified UNCONSUMED at Part EV ee7a951b) may
now take 3ba48608 as its BASE.
