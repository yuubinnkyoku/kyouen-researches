# Part EU declaration: euwin2 third WIN canonical adoption (2026-11-25)

Declaration for the Part EU lane before the publication waves (kit + outputs
will follow in waves B..E; a completion log closes the Part).  This Part
executes the THIRD WIN-row canonical adoption in the central-reply chain:
the 2 gate-verified WIN rows of closure class 30345 that the Part ES
exhausted-6 re-probe resolved at the 30M condition.

## HONEST process disclosure (pre-declaration exploration)

Unlike Parts EM/EP/ER, this declaration is issued AFTER a local
pre-declaration exploration already executed the full deterministic
adoption chain (maker -> merger -> refresh fork -> extractor) from the
published bytes only: these scripts are pure byte-transforms of published
inputs (no solver, no probe, no new verdict source); the exploration
result is used ONLY to pre-register the exact expected pins below, the
same way Part ER pre-registered its census expectations.  After this
declaration lands, the kit scripts are published (wave B) and every
output is REGENERATED in-session (wave C) and must match the declared
pins byte-for-byte; ANY mismatch aborts the Part.  No byte of this Part
is consumed anywhere until the waves are published to main; nothing was
probed, replayed, or re-run against any 15M condition.

## The adoption pool (2 WIN rows, both gate-verified at the ES 30M condition)

Class 30345 (mask 1152922604118478848/65536): ai007 (s5_index 441292,
nodes 16,090,493) and ai040 (s5_index 899584, nodes 20,711,023), the 2
of the 6 batch-38 honest-EXHAUSTED keys (ai007/ai024/ai030/ai038/
ai040/ai041) that the Part ES re-probe resolved as WIN at the DIFFERENT
30M condition.  Adopted node total 36,801,516.  The 4 ES-resolved LOSS
rows (ai024/ai030/ai038/ai041) are NOT adopted here (EM-pattern
loss-adoption territory at its own gate standard).

## Eligibility, all machine-verified before any row is emitted

1. Source-raw provenance: the published Part ES kit 30M two-pass
   fresh-cold node-exact raw pairs (nodes 16,090,493 / 20,711,023); the
   b38 15M raw pairs stay honest-EXHAUSTED (honest UNKNOWN at 15M) and
   are only the selection basis; NO row re-probed; the same-condition
   re-probe ban untouched (the 15M condition was never re-probed; the
   30M resolution condition was lawfully opened by Part ES).
2. Scrutiny-owner C++ second-implementation gate: the Part ET
   kyouen_dfpn_root.cpp gate at commit 154f3b7a (source byte pin
   9193f5b6...) re-executed all 9 rows (6 targets + 3 anchors),
   two-pass fresh-cold, 9/9 GATE-PASS, audit 2c6d7441... (schema
   n11-centralreply-cppgate-30345es6-audit-v1), four audit runs
   byte-identical, per-key budget/expected/observed equality; the ES kit
   (38 entries), the ET kit (38 entries) and the b38 kit (181 entries)
   verified file-by-file against their pinned MANIFESTs
   cc987739... / f0c1c27a... / 4dbf8856....
3. Key SSOT: every adopted (s5_index, lo, hi) triple matches the
   batch-38 batch-keys SSOT 29807104...; the ET registry
   gate-rows-et.json 6cf057ba... target pool must equal the b38
   raw-derivable honest-EXHAUSTED pool (exactly 6); the adopted set must
   equal the ES-30M raw-derived WIN disposition of that pool (exactly
   the 2); the manifest rows are SSOT/MANIFEST-extracted, never
   hand-typed (pin policy).
4. Freshness: every adopted (lo,hi) absent from the BASE merged chain
   cache 9c4dd94e... (Part ER canonical head, 6,765 rows WIN 186 /
   LOSS 6,579) and absent from the quarantine registry 81d23160...;
   ER regression tie: all 18 Part-ER adopted rows re-verified WIN in
   the BASE cache with identical nodes and NOT re-adopted here.
5. Out of scope, consumed NOWHERE: the 4 ES-30M-resolved LOSS rows
   (ai024/ai030/ai038/ai041, EM-pattern loss-adoption territory), the
   15M honest-EXHAUSTED labels of every pool key (honest UNKNOWN at
   15M, untouched), b018 (batch-1 dual-class probe WIN, scrutiny-owner
   pending, same-condition re-probe prohibited), the k04 sixth-cost
   WIN (owned by the sixth-cost lane), and every other unconsumed
   probe-level WIN.  WIN canonical adoption remains the scrutiny C++
   gate's exclusive right; this Part consumes only ET-gate-verified
   WINs.

## Chain mechanics (fail-closed) with pre-registered expected pins

increment-euwin2-20261125.cache (2 s5verdict WIN rows, schema
euwin2-increments-manifest-v1, expected sha256 d9365d80a90aff30
cb451f8f2519ab2cc004c6d10ba4fb149a7ee340e0aa0b4f...) merged into BASE by
the pinned fail-closed union merger 90711961... (byte-clone of the Part
EM/ER merger) producing merged-exact-s5-chain-plus-euwin2-20261125.cache
(expected 6,767 rows, WIN 188 / LOSS 6,579, sha256 3ba486086703b9f44a
0c685d7d5b45fab80f86760f2cd032a8dc18a2690233d6); 3 runs must be
byte-identical incl. audits (expected audit sha256 9f807c95e71a3da1f4d3
d958cdf87f5f31f2bd1c961a1b105b63368fa0b159ce x3).  All per-row
published pins are SSOT/MANIFEST-extracted, never hand-typed.

## Post-conditions this Part will verify (reaudit + extractor)

* reaudit refresh fork (only the CACHE path / expected sha / docstring
  differ from the published Part ER refresh 6c91e0ce...): expected
  refresh-summary 2b70bb55..., closure-classes 59a4c85f...,
  per-root-coverage cfc2bfe1..., worklist regen pin 397a4379...
  (unpublished per the size policy);
* class 30345 (already excluded_now since the Part EP ai048 flip) drops
  cost-unknown 7 -> 5 (the 2 members consumed here; the 4 unconsumed
  ES-resolved LOSS rows and the non-b38 child s5_index 528497 remain
  unknown insiders): scheduling bookkeeping, NOT a root verdict;
* the independent census must reproduce the class-status counts exactly
  (unknown 34,436 -> 34,430, excluded_now 84 -> 90, free_now 39 static,
  excluded 390 static) with EXACTLY 6 status flips, all UNKNOWN ->
  excluded_now, exactly the still-unknown owner classes of the adopted
  keys (ai007: {12846, 12875, 13801, 30345}; ai040: {30282, 30308,
  30326, 30345}); class 30345 itself was already excluded_now at Part
  EP/ER and must NOT double-flip;
* class 30354 must be untouched (no adopted member; unknown stays 96;
  the win_hit groups stay exactly the 10 class-30354 groups with 97
  unknown children each, identical on both sides);
* update8 frozen baseline static (union 31,859; resolved 260, remaining
  31,505, free groups 131);
* free_now may not shrink (39 static; Board verification 39/39 both
  sides);
* closure-classes.csv: 805 -> 805 rows, NO row leaves, NO row enters,
  NO groups_served churn; the only unknown_now churn is 30345: 7 -> 5;
  the only rank churn is the two-row swap 30345: 8->7 and 20421: 7->8;
* per-root coverage: free_now/uncovered thirds identical at every
  root; the individual greedy union changes only at 2 roots
  (12: 2850 -> 2848, 36: 3007 -> 3005); joint greedy union stays
  36,619 (the 6 flipped owner classes serve no closure group);
  group_best_options_nonfree stays 2,105; worklist 64,309 -> 64,307;
  all pure re-selection bookkeeping, no coverage claim.

## Guarantees

Consuming a WIN label asserts NO root verdict and NO 11x11 outcome.
The standard 11x11 empty board stays UNKNOWN.  All central-reply roots
stay UNKNOWN.  nodes are bookkeeping, never verdicts.  No claim of free
coverage, secured coverage, or root resolution is made anywhere in this
Part.
