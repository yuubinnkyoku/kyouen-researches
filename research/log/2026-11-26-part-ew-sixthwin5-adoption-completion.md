# Part EW completion log: sixthwin5 WIN-only canonical adoption (2026-11-26)

All waves landed.  Part EW closes complete; the canonical merged exact-S5
chain head of record formally advances to the sixthwin5 merged cache
`research/experiments/n11-centralreply-sixthwin5-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache`
(sha256 16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd,
6,797 rows, WIN 197 / LOSS 6,600), already published dossier-side and
byte-reproduced here by the fail-closed merger from BASE + the Part
increment; it is the new BASE for every later adoption / reaudit /
extractor.

## Wave chain (each push preceded by a fresh main refetch; each verified
by fetch-back byte comparison against the declared local bytes)

* A  declaration 7fcf9dde: all kit byte pins pre-registered before any
  kit byte was published (one commit, fetch-back byte-identical);
* B  kit scripts 3/3: 9bd8d586 (merger 90711961 byte-clone, maker
  9e6bf992, extractor cfefe839 in one commit);
* C  adoption outputs 5f05a14a: the six files - increment efee7b9e
  (5 WIN rows, row region byte-identical to the superseded dossier
  increment 44c16a28), manifest a7376780 (schema
  sixthwin5-adoption-increments-manifest-v1), merge-audit-run1/2/3
  all b404c248 (merged output byte-identical to the published dossier
  merged cache 16a12390, 6,797 rows WIN 197 / LOSS 6,600), decomp
  48913dc4 (schema sixthwin5-decomp-deltas-v1);
* D  close-out 7681848c: kit README + MANIFEST-sha256 (9 published kit
  members byte-pinned sha+size, README/MANIFEST self-excluded per
  convention);
* F  completion log = this commit.

Every wave fetch-back compared the raw published bytes with the local
declaration-pinned bytes byte-for-byte; no trailing-LF repair was
needed (unlike the Part EM wave-C incident), and no scratch or
temporary bytes were published.

NOT republished in this Part (deliberate, recorded in the kit MANIFEST
header): the merged scenario cache copy (byte-identical to the
published dossier file 16a12390; regenerable from BASE pin 6e49dd84
via the kit merger + increment), the probe-worklists (BASE regen pin
147b62d6, 3,715,963 B; SCEN regen pin 82f9e517, 3,715,904 B; size
policy), the dossier census json fd684d83 (published dossier-side).

## Execution record (this Part, all from published bytes; NO new solver
pass ran)

The kit extractor cfefe839 ran its full battery fail-closed over
published bytes only, twice, with byte-identical stdout and decomp
output: BOTH published refresh forks (the emloss21 dossier refresh
cc01b3d8 against BASE, the sixthwin5 dossier refresh fork 92a884c9
against SCEN, itself a byte-clone of cc01b3d8 differing in exactly
docstring / CACHE path / expected cache sha) re-executed byte-verbatim
in isolated scratch trees reproducing all 8 published / regen-pinned
outputs (7f379b71 / 68628134 / 9c5b2774 / 147b62d6 and 295027cf /
350e269a / 9c5b2774 / 82f9e517); the published dossier maker 424edee4
re-executed byte-verbatim (rc=0, byte-identical increment 44c16a28 +
manifest 25defefa), re-proving the entire adopt-eligibility chain live
from published bytes.  The merger reproduced the dossier merged head
16a12390 in 3/3 byte-identical conflict-free runs (audits b404c248 x3,
unique_rows 6,797, WIN 197 / LOSS 6,600).  A 3-mode tamper battery
(increment row / merge-audit / manifest mutations) all failed closed
rc=1 with byte-verified restore; recorded here, not published as kit
files.  The decomp 48913dc4 records the extractor's independent
recount agreeing EXACT with the published dossier census measurement
fd684d83 on both cache identities, census counts, the exact 8-flip
set, closure churn (rows 804 -> 804, the single unknown_now churn
{16734: 92 -> 91}, empty rank churn), per-root greedy deltas (none),
joint greedy (35,155 static), worklist totals, update8 numbers incl.
the single-key newly-resolved set {64872} and the 4 out-of-baseline
keys, win_hit identity (25 -> 25 IDENTICAL sets), serving-class
records, the owner histogram and the 5-row adopted table with owner
sets.

## State after the Part (all machine-verified by the extractor battery)

* canonical BASE of record: 16a12390... (6,797 rows WIN 197 /
  LOSS 6,600); the Part EM head 6e49dd84... remains published history
  and is the merge BASE of this Part;
* census: class_status_counts 34,417/103/39/390 -> 34,409/111/39/390
  with EXACTLY 8 flips, ALL unknown -> excluded_now, win-hit only,
  and exactly the owner classes of the 5 adopted keys that were
  unknown at BASE {774, 1387, 2169, 2339, 3077, 16734, 25845, 30329};
  the remaining owner class 30354 (k02) keeps its excluded_now status;
  NO class is freed (none moves to free_now); 34,409 S4 classes remain
  status-unknown;
* serving class 3077 (cost size 100, raw Board boundary 108):
  cost-unknown 100 -> 95 (the 5 adopted keys, all owned there); its
  status flips unknown -> excluded_now (the win-hit mechanism,
  measured dossier-side);
* closure-classes.csv 804 -> 804: ZERO rows enter or leave; unknown_now
  churn exactly {16734: 92 -> 91}; rank churn EMPTY (0 re-ranked rows);
  groups_served churn 0;
* update8 frozen baseline: resolved_count 280 -> 281 (newly_resolved
  exactly k02's s5 index 64872; the other four adopted keys - s5
  39127 / 91506 / 96472 / 112201 - sit outside the frozen baseline
  requirement, measured, disclosed), remaining_now 31,445 -> 31,445,
  groups_free_now 131 static, union baseline 31,859 stale-equal;
  win_hit_groups 25 -> 25 IDENTICAL sets;
* per-root free_now/uncovered identical at all 20 roots (per-root
  coverage byte-identical on both sides); individual greedy union
  UNCHANGED at all 20 roots; joint greedy 35,155 -> 35,155 UNCHANGED;
  unique_groups 2,115 static; group_best_options_nonfree 2,101
  static; worklist 64,277 -> 64,276 (-1, exactly the one newly
  resolved in-requirement key).  All scheduling bookkeeping; no
  coverage claim anywhere.

## Verdict scope and guarantees (unchanged)

Consumed in this Part: exactly the 5 unconsumed sixth-cost
exclusive-probe exact-WIN rows k02 (7,717,432 nodes, ea73c3e3 4-run
witness corroborated) / k03 (9,255,414) / k04 (9,433,024) / k05
(13,397,611) / k08 (6,195,897) (TI third-implementation verdict-level
WIN agreement), each two-pass fresh-cold node-exact at 15M plus a
voluntary third cold verify run, C++-gated GATE-PASS by the Part SK
kit; adopted node total 45,999,378; no WIN regression ties (all 5 keys
fresh to BASE 6e49dd84; win_ties = []).  Consuming a WIN label asserts
NO root verdict; owner classes leave live status by the win-hit
mechanism only; NO class is freed and NO coverage claim is made
anywhere.  NOT consumed and NOT emitted: the 3 standing honest LOSS
labels of the same ladder (k01 15M 10,369,650; k06 15M 8,182,231;
k07 2M 1,419,823) and every later third-impl batch WIN row (k13/k19
etc., parked4 L50M ladder); all stay in NO cache.  No batch key was
re-searched at any condition.  The standard 11x11 empty board and
every central-reply root stay UNKNOWN; nodes are bookkeeping, never
verdicts; no free/secured-coverage or root-resolution claim is made
anywhere in this Part.  Next: any later adoption Part takes 16a12390
as its BASE; the sixth-cost serving class 3077 is now excluded_now
with its 100-child cost set 95 exact (5 WIN children consumed,
5 unknown cost children remain).

## Session honesty note

The Part maker and extractor were prepared inside this session as
staged structural forks of the published Part EM kit scripts; a
context compaction hit mid-fork (a draft-stage loss).  Every final
kit byte was re-staged from the published EM kit files and
re-verified against all published pins before the recorded runs, and
each publication wave was fetch-back byte-verified; nothing in the
kit depends on the lost draft.
