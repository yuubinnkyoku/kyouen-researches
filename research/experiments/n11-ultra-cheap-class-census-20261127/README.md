# n11 ultra-cheap class-completion candidate census (2026-11-27)

Independent machine census of the closure-ladder classes that sit at
exactly ONE remaining unknown S5 child under the canonical head of
record `1e2eeda2...` (eleventh-cost k01 adoption, 6,890 rows WIN 208 /
LOSS 6,682), published as scheduling input for the adaptive
coordinator: a single adopted verdict on such a key completes its
class (a free_now candidate, Board-verified at adoption time), which
is strictly cheaper than another multi-key serving-class batch.

## Result (PASS, rc=0, 3 runs byte-identical, 18 gates)

All 804 published closure-ladder rows
(`n11-eleventhcost-k01-adoption-reaudit-20261127/reaudit/output/closure-classes.csv`,
sha256 `d7ae77dd...`) have their `unknown_now` count independently
recomputed from the frozen dependency graph `54f9c364...` + head
`1e2eeda2...` + update8 receipts `b658290a...` (fresh re-implementation
of the refresh's trust boundary; the refresh machinery itself is NOT
read or executed): **804/804 exact match**, and the one-unknown set is
exactly the four classes the SZ-wave-E note predicted:

| class_index | class key | remaining unknown S5 key | s5_index |
|---|---|---|---|
| 16371 | 1153202979851993088:16 | 1153202979851993088:272 | 550879 |
| 23101 | 1152921504892059648:16 | 1152921505747697664:1032 | 745184 |
| 1849 | 1152922672972169216:0 | 1153485622925590528:0 | 81011 |
| 2251 | 1155314042043105280:0 | 1297036830121656320:131074 | 93815 |

(class 16371's key `1153202979851993088:272` matches the SZ-wave-E
published measurement verbatim, an independent cross-check.)

**Claim status: all four keys are UNCLAIMED** — checked against
focus_35, cert_38, third_39, fourth_41, fifth_44, sixth_43,
seventh_42, eighth_43, ninth_45, tenth_44, eleventh_46, twelfth_51,
sbd_101, parked_6 and the 2-entry quarantine registry: no overlap.
All four are fresh vs the head. None is in the probe-13 supply, so
legal/proxy are null here (legal re-derivation belongs to a future
selection Part).

## Files

- `scripts/ultra_cheap_census.py` — fresh census instrument
  (sha256 `c5e7b88e76d1a4652c67bfdd05b870b0c1076681a55c64691eaa87e6f9af634d`).
- `output/ultra-cheap-census-run{1,2,3}.json` + `output/stdout-run{1,2,3}.txt`
  — three cold passes, byte-identical (run json sha256
  `a60716ac84e22833eaf570819d8744a2c66b2ad1d563b3791ade829eaed87906`).
- `MANIFEST-sha256.txt` — sha256 of every file in this kit.

## Inputs (published elsewhere, sha-pinned in-script)

dependency graph `n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz`
(`54f9c364...`), update8 receipts
`n11-night-plan-update8-20261016/output/repaired-joint-plan-update8.json`
(`b658290a...`), head of record `1e2eeda2...`, closure ladder
`d7ae77dd...`, probe-13 supply `31f0d29b...` + candidate ledger
`2a4c2382...` (shape gates), quarantine `81d23160...`, ccp.json
(focus/cert lists), the nine cost-selection key lists, the sbd-101
keymap, and the parked-2/parked-4 batch CSVs.

## Tamper battery (5/5 fail-closed; clean control re-PASS byte-identical)

- T1 closure-ladder `unknown_now` flip on the rank-1 row ->
  P2 recomputation gate, rc=1
- T2 head verdict-row deletion -> P0 head-sha gate, rc=1
- T3 duplicate key appended to the fifth claim list -> P3 claim-size
  gate, rc=1
- T4 dependency-graph `s4_cost` edit -> P0 graph-sha gate, rc=1
- T5 update8 receipt deletion (a receipt that is a member of ladder
  class costs) -> caught by BOTH the update8-sha pin and the P2
  804-row recomputation gate (the semantic detector), rc=1

## Honest disclosures

- The first draft keyed classes by geometry.json.gz class keys and
  failed its own gate (the ladder's class_index universe is the frozen
  dependency graph, not the geometry keying); it was rewritten against
  the dependency graph before any result was recorded.
- The CAND_SHA pin constant was initially mistyped (62 of 64 hex
  chars); the fail-closed pin gate caught it before any run passed.
- The update8 `resolved_s5_verdicts` map holds 23 receipt keys (282 is
  a different counter in the refresh bookkeeping); the gate is set to
  the machine-observed 23 with the union_size 31,859 requirement gate.
- The first T5 attempt (flipping a receipt whose key overlaps the head
  cache) was a structural no-op: no receipt key is present in the head
  cache (receipts resolve exactly the keys outside it). Replaced with
  the receipt-deletion tamper above.
- The 23 receipt keys were cross-checked against the head: 0
  receipt/cache conflicts (same trust boundary invariant the published
  refresh enforces).

## Meaning and non-meaning

Scheduling bookkeeping only: NO verdict is claimed or consumed.
Resolving any listed key would still require the standing cold-pair +
C++ second-implementation gate + third-implementation corroboration
pillars before any adoption, and the class completion would be
Board-verified at adoption time. Nodes and proxy values are never
evidence of WIN or LOSS. The standard 11x11 empty board: UNKNOWN. All
19 central-reply roots: UNKNOWN. The two-stone root {60,27} and its
remaining third moves 100/108: UNKNOWN.

This lane runs without access to the user's computer (scheduled task);
publication is via the GitHub API only. No probe of any key was
executed here.
