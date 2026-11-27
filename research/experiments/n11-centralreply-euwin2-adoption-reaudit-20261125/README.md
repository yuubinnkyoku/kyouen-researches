# n11-centralreply-euwin2-adoption-reaudit-20261125 (Part EU, 2026-11-25/26)

Part EU: the THIRD WIN canonical adoption in the central-reply chain.  The
2 Part-ES-30M-resolved, Part-ET-C++-gate-verified WIN rows of closure class
30345 (ai007: s5_index 441292, nodes 16,090,493; ai040: s5_index 899584,
nodes 20,711,023; adopted node total 36,801,516) are consumed into the
canonical merged exact-S5 chain cache as WIN verdicts.

Nothing here asserts any root verdict and no 11x11 outcome: a WIN
canonical adoption transfers NO verdict to any central-reply root.  Class
30345 stays excluded_now (flipped at Part EP) with cost-unknown dropping
7 -> 5, and exactly 6 further classes flip UNKNOWN -> excluded_now -
derived scheduling bookkeeping, re-audited fail-closed below.  The standard
11x11 empty board stays UNKNOWN.  nodes are bookkeeping, never verdicts.

## chain position

* BASE = the Part ER canonical merged chain head 9c4dd94e...
  (6,765 rows, WIN 186 / LOSS 6,579).
* increment = `output/increment-euwin2-20261125.cache` (2 WIN rows,
  sha256 d9365d80...), SSOT-extracted per-row pins in
  `output/increments-manifest.json` (schema euwin2-increments-manifest-v1,
  sha256 793f68c5...).
* merged head = `output/merged-exact-s5-chain-plus-euwin2-20261125.cache`
  (6,767 rows, WIN 188 / LOSS 6,579, sha256 3ba48608...), fail-closed
  union merger byte-clone (90711961...), 3 deterministic runs
  byte-identical incl. their audits (merge-audit-run1/2/3.json all
  sha256 9f807c95...).  Published at wave C (f7e607b1) and re-verified
  byte-identically from published bytes by the resumption session
  (baa8a0c0) and by this close-out session.

## WIN label eligibility (fail-closed, machine-verified)

The maker `scripts/make_increments_eu_win2_adoption.py` re-verifies every
gate before emitting a single row (fail-closed; rc=1 on ANY drift):

1. every referenced published kit is verified file-by-file against its
   pinned MANIFEST-sha256 (Part ES kit 38 entries, Part ET kit 38
   entries, batch-38 kit 181 entries); per-row pins are SSOT/MANIFEST
   extracted, never hand-typed;
2. the adopted pool equals the ES-30M WIN disposition of the re-derived
   6-key b38 honest-EXHAUSTED pool (ai007/ai024/ai030/ai038/ai040/ai041):
   exactly {ai007, ai040}; the b38 15M raw pairs stay honest-EXHAUSTED
   and are only the selection basis - the same-condition re-probe ban is
   untouched (the 30M resolution condition was lawfully opened by
   Part ES);
3. the C++ scrutiny-owner second-implementation gate
   kyouen_dfpn_root.cpp (source pin 9193f5b6... at 154f3b7a) re-executed
   all 9 rows two-pass fresh-cold, 9/9 GATE-PASS, audit 2c6d7441...
   (schema n11-centralreply-cppgate-30345es6-audit-v1), ES/ET gate raws
   node-exact vs the ES source raws;
4. (s5_index, lo, hi) triples match the b38 batch-keys SSOT
   29807104...; freshness: both keys absent from BASE and from the
   quarantine registry 81d23160...; the ER regression tie re-verifies
   all 18 Part-ER adopted rows sit WIN in BASE and are NOT re-adopted.

NOT consumed (each stays in NO cache): the 4 ES-30M-resolved LOSS rows
(ai024/ai030/ai038/ai041 - EM-pattern loss-adoption territory), the b38
15M honest-EXHAUSTED labels (honest UNKNOWN at 15M), b018 (dual-class,
scrutiny-owner pending), the k04 sixth-cost WIN, and every other
unconsumed probe-level WIN.

## reaudit (Board fail-closed child verification) + the disclosed repair

`reaudit/scripts/refresh_adoption_eu.py` (sha256 6dc24c15...) is the
PUBLISHED disclosed-repair scenario refresh fork of the Part ER refresh
6c91e0ce...: machine-verified 3-region diff (CACHE path, expected cache
sha, docstring), all computation bytes identical.  Repair provenance: the
declaration's original fork pin a377eea0... pointed at never-published
bytes (wave B carried only the 3 kit scripts; declaring environment
gone) and the diagnostic fork 353f15d3 (f353dbe5) was likewise
throwaway-local - decision record:
`research/log/2026-11-26-part-eu-scen-refresh-pin-repair.md`.

The kit extractor `scripts/compare_deltas_eu_adoption.py` (sha256
9bc5f06a...; was wave-B aaf13bdc...) was repaired in exactly two
disclosed hunks (the SCEN_REFRESH_SHA pin supersession + the docstring
mention); no other byte changed.

Run records (this close-out session, all from published bytes):

* fork executed rc=0 (wall 64.7 s) -> refresh-summary 2b70bb55... (34,192
  B), closure-classes 59a4c85f... (805 rows), per-root-coverage
  cfc2bfe1... (588 B), probe-worklist regen pin 397a4379...
  (3,717,712 B, unpublished per the size policy) - all four
  byte-identical to the declaration pins;
* repaired extractor full battery rc=0 TWICE (wall 2m15.8s / 2m12.8s),
  stdout byte-identical; both refresh forks re-executed byte-verbatim in
  isolated scratch trees reproducing all EIGHT outputs (incl. the
  publication-exempt worklist regen pins 78e499dd / 397a4379);
* decomp-deltas-euwin2-adoption.json sha256 8d4a5743... byte-identical
  across both runs AND container-invariant vs the f353dbe5 diagnostic
  (same 8d4a5743... under the throwaway 353f15d3 pin).

The battery re-derived from published bytes: exactly 6 UNKNOWN ->
excluded_now flips {12846, 12875, 13801, 30282, 30308, 30326} (the
adopted keys' still-unknown owner classes) with 30345 NOT double-flipping
(EP-flipped, cost-unknown 7 -> 5 on the 51-raw/50-cost Board boundary);
30354 untouched (97/97 boundary, unknown 96 static; its 10 win_hit groups
hold 97 unknown children on both sides); census 34,436/84/39/390 ->
34,430/90/39/390; closure 805 -> 805 with zero rows left/entered, the only
unknown_now churn 30345: 7 -> 5 and the only rank churn the two-row swap
{30345: 8->7, 20421: 7->8}; update8 static (union 31,859, resolved 260,
remaining 31,505, free groups 131); Board verification 39/39 both sides;
per-root free_now/uncovered thirds identical everywhere, individual
greedy changes only at roots 12 (2850 -> 2848) and 36 (3007 -> 3005);
joint greedy 36,619 static; group_best_options_nonfree 2,105 static;
worklist 64,309 -> 64,307.  Pure re-selection bookkeeping; no coverage
claim.

## Interpretation guard

Consuming the 2 WIN labels asserts NO root verdict.  The 34,430 status-
unknown S4 classes remain; the standard 11x11 empty board and every
central-reply root stay UNKNOWN.  No free-coverage, secured-coverage or
root-resolution claim is made anywhere in this Part.
