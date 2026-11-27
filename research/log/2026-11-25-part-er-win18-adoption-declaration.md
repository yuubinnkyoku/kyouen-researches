# Part ER declaration: erwin18 second WIN canonical adoption (2026-11-25)

Declaration for the Part ER lane before the publication waves (kit + outputs
will follow in waves B..E; a completion log closes the Part).  This Part
executes the SECOND WIN-row canonical adoption in the central-reply chain,
the largest so far: all 18 still-unconsumed gate-verified batch-38 WIN rows
of closure class 30345.

## The adoption pool (18 WIN rows, all gate-verified)

Class 30345 (mask 1152922604118478848/65536) batch-38 rows: ai002, ai003,
ai005, ai006, ai010, ai013, ai014, ai017, ai023, ai028, ai034, ai035,
ai036, ai039, ai043, ai046, ai047, ai049 - the raw-derived b38 WIN
disposition (19 rows) minus ai048, which the Part EP first-ever WIN
adoption already consumed.  Adopted node total 136,604,338.  Honest record:
the Part EQ declaration prose summed the 21 gate targets as 136,539,338,
a mis-sum; the per-row registry/audit/raws agree on 136,604,338 and the
per-row data is SSOT (disclosed in the ER increments-manifest).

## Eligibility, all machine-verified before any row is emitted

1. Source-raw provenance: the published batch-38 kit original two-pass
   fresh-cold node-exact raw pairs at each row's own single condition
   (15M); no row re-probed; the same-condition re-probe ban untouched.
2. Scrutiny-owner C++ second-implementation gate: the Part EQ
   kyouen_dfpn_root.cpp scrutiny gate at commit 154f3b7a (source byte pin
   9193f5b6...) re-executed on all 21 batch-38 WIN targets (the 18 adopted
   here plus ai048 and b018-witness context), two-pass fresh-cold,
   21/21 GATE-PASS, audit c2ff2232... (schema
   n11-centralreply-cppgate-30345win18-audit-v1), four audit runs
   byte-identical, per-key budget/expected/observed equality; the EQ kit
   (74 entries) and the b38 kit (181 entries) verified file-by-file against
   their pinned MANIFESTs 786315f3... / 4dbf8856....
3. Key SSOT: every adopted (s5_index, lo, hi) triple matches the
   batch-38 batch-keys SSOT 29807104...; the manifest rows are
   SSOT-extracted, never hand-typed (pin policy).
4. Freshness: every adopted (lo,hi) absent from the BASE merged chain
   cache fd29a337... (Part EP canonical head, 6,747 rows WIN 168 /
   LOSS 6,579) and absent from the quarantine registry 81d23160...;
   ai048 already sits WIN in the BASE cache (EP regression tie, re-checked
   at adoption time).
5. Out of scope, consumed NOWHERE: the 6 batch-38 honest-EXHAUSTED keys
   (ai007/ai024/ai030/ai038/ai040/ai041, honest UNKNOWN at the 15M
   condition), the 24 b38 LOSS rows (Part EM loss-only adoption territory),
   ai044 (EM territory), b018 (batch-1 dual-class probe WIN, scrutiny-owner
   pending, same-condition re-probe prohibited), the k04 sixth-cost WIN
   (owned by the sixth-cost lane), and every other unconsumed probe-level
   WIN.  WIN canonical adoption remains the scrutiny C++ gate's exclusive
   right; this Part consumes only EQ-gate-verified WINs.

## Chain mechanics (fail-closed)

increment-erwin18-20261125.cache (18 s5verdict WIN rows, schema
erwin18-increments-manifest-v1) merged into BASE by the pinned fail-closed
union merger 90711961... (byte-clone of the Part EM merger) producing
merged-exact-s5-chain-plus-erwin18-20261125.cache (expected 6,765 rows,
WIN 186 / LOSS 6,579); 3 runs must be byte-identical incl. audits.  All
per-row published pins are SSOT/MANIFEST-extracted, never hand-typed.

## Post-conditions this Part will verify (reaudit + extractor)

* reaudit refresh: closure class 30345 (already excluded_now since the
  Part EP ai048 flip) drops cost-unknown 25 -> 7 (18 members consumed
  here; the 6 EXHAUSTED rows and b018 remain unknown insiders):
  scheduling bookkeeping, NOT a root verdict;
* the independent census must reproduce the published class-status counts
  exactly (unknown 34,477 -> 34,436, excluded_now 43 -> 84, free_now 39
  static, excluded 390 static) with EXACTLY 41 status flips, all UNKNOWN
  -> excluded_now, exactly the owner classes of the adopted keys that
  were still unknown; the further owner classes 29979/30345/30542 were
  already excluded_now at Part EP and must NOT double-flip;
* class 30354 must be untouched (no adopted member; unknown stays 96);
* the owner-union relation is class-30345-specific this time: none of the
  three EP-era dual classes re-flips;
* update8 frozen baseline static (union 31,859; resolved 260, remaining
  31,505, free groups 131), win_hit groups recorded as recomputed (the 10
  class-30354 groups lose nothing to this adoption);
* free_now may not shrink (39 static; Board verification 39/39 both sides);
* honest tradeoff to record: consuming 18 previously-unknown s5 WIN
  verdicts resolves them out of the joint-requirement accounting, so the
  removal of the 41 newly-excluded classes from the free-coverage option
  space nets a SHRINKING remaining greedy union (36,643 -> 36,619) and a
  smaller probe worklist: scheduling bookkeeping only, no coverage claim.

## Guarantees

Consuming a WIN label asserts NO root verdict and NO 11x11 outcome.  The
standard 11x11 empty board stays UNKNOWN.  All central-reply roots stay
UNKNOWN.  nodes are bookkeeping, never verdicts.  No claim of free
coverage, secured coverage, or root resolution is made anywhere in this
Part.
