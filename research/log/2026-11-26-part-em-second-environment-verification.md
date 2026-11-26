# Part EM full second-environment verification (2026-11-26)

Cross-environment verification of the Part EM chain step, the same
discipline the Part EU verification log (2026-11-26, "Part EU full
second-environment verification") applied to the EU chain step.  Part EM
(wave chain c5793256 -> 3fc406da/8e570d0e -> ff942502/66badee4 ->
5c8ed34f -> completion log at ec7acda6) is the step that advanced the
canonical merged exact-S5 chain head of record to the published dossier
file `research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-emloss21-20261126.cache`
(sha256 6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d,
6,792 rows, WIN 192 / LOSS 6,600): the emloss21 loss-only canonical
adoption.  This log records the first full second-environment
re-execution of the published fail-closed extractor battery over the
published bytes, on a fresh host/container that played no role in any
wave of the Part.  After this verification the canonical head of record
cross-environment record is: declaring-session bytes -> this second
execution environment, battery output byte-identical in both.

Nothing was consumed and no repo byte was modified by the verification
itself (the scratch trees are local-only; no push of kit bytes; the
probe-worklist regen outputs enter only as sha-verified scratch, never
published).  The verdict scope of Part EM is unchanged exactly as its
completion log records: the 21 adopted exact-LOSS rows (17 batch-5
class-12264 rows f001-f016/f018 at 15M, 4 Part ES class-30345 reprobe30m
rows ai024/ai030/ai038/ai041 at 30M, adopted node total 129,518,414
bookkeeping) stay the only EM consumption; f017/ai007/ai040 stay
regression ties NOT re-adopted; the sixth-cost probe batch rows (k01
LOSS; k02/k03/k04/k05 WIN, all published unconsumed by the sixth-cost
lane) and every other unconsumed probe-level WIN stay in NO cache; the
standard 11x11 empty board and every root stay UNKNOWN.

## Fetch record (published bytes only)

All bytes fetched from main commit-pinned at
f51243317081550c7d3a81f7d5e3a478dc1b1e47 (HEAD at verification time,
raw.githubusercontent commit-pinned fetches), every one sha256-verified
against its published pin BEFORE the battery ran (zero drift anywhere):

* EM kit `n11-centralreply-emloss21-adoption-reaudit-20261126/`:
  all 9 MANIFEST-sha256 entries verified sha+size (merger 90711961,
  maker cd603627, extractor b9a74915, increment 3e6e9bf0, manifest
  bd4b9e76, merge-audits x3 17a390e7, decomp c1bf5881);
* the extractor's own pinned input table re-verified byte-exact, 27/27
  entries (BASE cache 63f33c4f 6,771 rows WIN 192 / LOSS 6,579; scenario
  cache 6e49dd84 6,792 rows WIN 192 / LOSS 6,600; dossier increment
  47443dc1 / dossier manifest 94815c34 / dossier maker 74fbbfd9 /
  dossier census measurement d67b6e9b; EV Part increment 7f125610;
  BASE reaudit outputs 1fafd081 / 6ba51faa / d9eee976; SCEN reaudit
  outputs 7f379b71 / 68628134 / 9c5b2774; refresh forks f2edac3e (Part
  EV dossier) and cc01b3d8 (emloss21 dossier); union merger 90711961;
  the three published merge audits 17a390e7; frozen pins
  dependency-graph 54f9c364, update8 b658290a, Board source 954d3a10,
  policy 78655e94, quarantine 81d23160);
* the dossier maker's consumed-source pins re-verified byte-exact:
  batch-5 kit direct pins (README 1f69bfb1, batch-keys 57da4702,
  status.log c473e32c and all 36 raw two-pass files), Part ES kit
  verified file-by-file against its published MANIFEST cc987739
  (38/38 entries, including the jsreplay replica pin 84585617 that
  also anchors the batch-5 replica) plus the MANIFEST-self-excluded
  README verified against the maker's direct pin 67ab379d, and the
  batch-38 SSOT batch-keys-b38.json 29807104.

Honest environment note: the FIRST battery attempt aborted rc=1 inside
the dossier-maker re-execution because the local fetch set initially
omitted the Part ES kit README (a MANIFEST-self-excluded file the
dossier maker consumes by its own direct sha pin) - a fetch-packaging
gap of this verification tree only, not any published-byte drift: the
file verified against 67ab379d immediately on fetch, and both recorded
clean runs below ran from the completed tree.  One aborted attempt, two
clean runs.

## Battery execution (this environment, container-fresh)

* run1: rc=0, wall 1m59.0s (real 1m59.002s; user 1m57.5s);
* run2: rc=0, wall 2m0.1s (real 2m0.061s; user 1m58.6s);
* stdout run1 vs run2: byte-identical (cmp), exactly:

  `EM decomp OK: flips=0 census=34417/103/39/390 IDENTICAL caches=6771->6792 win=192->192 loss=6579->6600 closure_rows=805->804 exit=30345 resolved=263->280 greedy=36618->35155 worklist=64302->64277`

* the regenerated decomposition was byte-identical to the pristine
  published `output/decomp-deltas-emloss21-adoption.json` pin c1bf5881
  after run1 AND after run2 (cmp against a preserved pristine copy,
  sha256 c1bf5881... re-verified both times) - the same decomp sha the
  wave-C declaring session observed, now reproduced in a SECOND
  independent execution environment;
* inside EACH run the battery fail-closed re-executed BOTH published
  refresh forks byte-verbatim in isolated scratch trees (BASE: the
  Part EV dossier refresh f2edac3e against cache 63f33c4f; SCEN: the
  emloss21 dossier refresh cc01b3d8 against cache 6e49dd84) and
  verified all EIGHT regenerated outputs against their
  publication/regen pins (1fafd081 / 6ba51faa / d9eee976 / ca50cb68
  and 7f379b71 / 68628134 / 9c5b2774 / 147b62d6) - zero drift, zero
  conflicts; both runs equally deterministic;
* inside EACH run the published dossier maker 74fbbfd9 was re-executed
  byte-verbatim in an isolated scratch tree (rc=0 twice,
  byte-identical reproduction of its pinned outputs increment 47443dc1
  and manifest 94815c34), re-proving live on this host, from published
  bytes only, the entire Part EM adopt-eligibility evidence chain the
  dossier maker encodes (batch-5 direct byte pins, Part ES kit
  MANIFEST verification, the b38 SSOT cross-gates with the prior 15M
  EXHAUSTED honest-label pins, all 24 probed rows' two-pass payload
  gates, the f017/ai007/ai040 WIN regression ties against BASE, the
  fresh-to-BASE / quarantine / canonical-safety gates, the
  adopted-table digest 4fd8723e);
* the battery re-derived machine-verified, inside each run: the
  manifest decomposition (schema emloss21-adoption-increments-manifest-v1)
  with all supersession / provenance / pools fields; SCEN == BASE rows
  + exactly the 21 Part increment rows (6,792 rows WIN 192 /
  LOSS 6,600, verdict agreement everywhere), no adopted key intersecting
  the Part EV increment; the independent full-class census as IDENTICAL
  class_status_counts on both sides (34,417 / 103 / 39 / 390) with
  EXACTLY ZERO status flips; the serving-class Board arithmetic
  (class 12264 cost-unknown 50 -> 33, class 30345 cost-unknown 4 -> 0,
  class 30345 EXITS the closure ranking 805 -> 804 with status
  excluded_now unchanged), the closure churn incl. the 763-row rank
  table and the unknown_now churn {6518: 61->60, 6547: 58->57,
  9478: 61->60, 12235: 61->60, 12264: 50->33}; the frozen update8
  refresh (resolved 263 -> 280 with the newly_resolved set exactly the
  17 batch-5 s5 indices, remaining 31,445 static, win_hit 25 -> 25
  IDENTICAL sets); per-root free_now/uncovered identical at all 20
  rows with greedy-union changes only at roots {5, 12, 16, 36, 38,
  49}; joint greedy 36,618 -> 35,155; worklist 64,302 -> 64,277; and
  the dossier census measurement d67b6e9b cross-compared
  field-by-field against the battery's own independent recount (EXACT
  agreement; the dossier-time verdict-scope fields stay superseded by
  the Part EM declaration).

## Cross-environment invariants (measurement discipline)

The battery's stdout and decomposition carry NO wall-clock fields, so
unlike the Part ET/EV audit JSONs (per-pass wall_s verbatim quoting
makes those cross-environment byte-identity impossible by design), the
full Part EM battery output IS byte-identical across environments:
stdout pair byte-identical here, decomp byte-identical to the published
pin, deterministic content across two execution environments
(wave-C declaring session; this verification).  Wall-time differences
are disclosed above and carry no verification weight.

## Honest scope

* this log records ONLY the verification; it adopts nothing, consumes
  nothing, changes no kit byte;
* the canonical BASE of record 6e49dd84... (6,792 rows WIN 192 /
  LOSS 6,600) is unchanged by this verification; every later adoption
  / reaudit / extractor Part still takes it as BASE;
* NOT-consumed set unchanged: the sixth-cost probe batch rows (k01
  LOSS; k02/k03/k04/k05 WIN) and all other unconsumed probe-level
  WINs stay in NO cache;
* standard 11x11 empty board, the two-stone roots, all 19
  central-reply roots, S2 and every closure class: UNKNOWN; no
  coverage claim anywhere; nodes are bookkeeping, never verdicts.
