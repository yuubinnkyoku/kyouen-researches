# Part EP declaration: epwin10 FIRST-EVER WIN canonical adoption (2026-11-25)

Declaration for the Part EP lane before the publication waves (kit + outputs
will follow in waves B..E; a completion log closes the Part).  This Part
executes the first WIN-row canonical adoption in the central-reply chain.

## The adoption pool (10 WIN rows, all gate-verified)

Class 34908 (mask 1152921504607895553/68719476736): af029, af047, af050,
af053 (b33 15M raws), af023, af048 (Part EA 30M reprobe raws; the b33 15M
EXHAUSTED labels are honest UNKNOWN remnants of a superseded condition and
are NOT adopted).  Class 30484 (mask 1152922604135251968/65536): aj030,
aj049 (Part EK 30M reprobes; aj049 additionally anchored by the b39 15M
same-nodes witness), aj050 (b39 15M), ai048 (b38 15M).  Adopted node total
98,335,817.

## Eligibility, all machine-verified before any row is emitted

1. Source-raw provenance: published original two-pass fresh-cold
   node-exact raw pairs in their own kits at each row's own single
   condition; no row re-probed; the same-condition re-probe ban untouched.
2. Scrutiny-owner C++ second-implementation gate: kyouen_dfpn_root.cpp at
   commit 154f3b7a (source byte pin 9193f5b6...), executed two-pass
   fresh-cold in the published Part EN (class 30484 rows; audit f35cddd2,
   8/8 GATE-PASS) and Part EO (class 34908 rows; audit b46f2130, 9/9
   GATE-PASS), zero MISMATCH/GATE-FAIL/GATE-CRASH, per-key
   budget/expected/observed equality.
3. Third-implementation corroboration for the class-34908 rows: the Part
   EG JS replication (third_impl 08ea958f, audit-summary 73af060a, all
   gates PASS).
4. Key SSOTs: (lo,hi,legal,s5_index) quadruples match b33 batch-keys
   8a863381, EA reprobe-keys 3744b522, b39 keys 5e25b550, b38 keys
   29807104.
5. Freshness: every adopted (lo,hi) absent from the BASE merged chain
   cache b5be64e6... (Part EM canonical head, 6,737 rows WIN 158 /
   LOSS 6,579) and absent from the quarantine registry 81d23160.
6. Out of scope, consumed NOWHERE: the k04 sixth-cost WIN (verified by the
   Part EN gate, owned by the sixth-cost lane), the remaining batch-38
   probe-level WIN rows, the 6 honest-EXHAUSTED keys, b018, and every
   other probe-level WIN.  WIN canonical adoption remains the scrutiny
   C++ gate's exclusive right; this Part consumes only gate-verified WINs.

## Chain mechanics (fail-closed)

increment-epwin10-20261125.cache (10 s5verdict WIN rows, schema
epwin10-increments-manifest-v1) merged into BASE by the pinned fail-closed
union merger 90711961... (byte-clone of the Part EM merger) producing
merged-exact-s5-chain-plus-epwin10-20261125.cache (expected 6,747 rows,
WIN 168 / LOSS 6,579); 3 runs must be byte-identical incl. audits.  All
per-row published pins are MANIFEST-extracted, never hand-typed (pin
policy adopted this Part).

## Post-conditions this Part will verify (reaudit + extractor)

* reaudit refresh: closure classes 30484 (cost-unknown 4) and 34908
  (cost-unknown 6) become FULLY KNOWN (0 unknown); both classes flip to
  excluded (a known WIN child ends free all-LOSS coverage) - scheduling
  bookkeeping, NOT a root verdict;
* the independent census must reproduce the published class-status counts
  exactly (unknown 34,497 -> 34,477, excluded_now 23 -> 43, free_now 39
  static, excluded 390 static) with EXACTLY 20 status flips, all UNKNOWN
  -> excluded_now, exactly the 20 classes whose s4_cost contains an
  adopted key;
* free_now may not shrink (39 static; Board verification 39/39 both sides);
* update8 frozen baseline static (union 31,859), resolved/remaining and
  the win_hit groups recorded as recomputed;
* honest tradeoff to record: the removal of the two closure classes from
  the free-coverage option space grows the joint greedy remaining
  requirement.

## Guarantees

Consuming a WIN label asserts NO root verdict and NO 11x11 outcome.  The
standard 11x11 empty board stays UNKNOWN.  All 19 central-reply roots stay
UNKNOWN.  nodes are bookkeeping, never verdicts.  No claim of free
coverage, secured coverage, or root resolution is made anywhere in this
Part.
