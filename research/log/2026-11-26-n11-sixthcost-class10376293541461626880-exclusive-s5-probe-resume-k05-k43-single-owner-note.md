# n11 sixth-cost exclusive S5 probe third resumption batch k05..k43: single-owner note (2026-11-26, third resumption)

Declared: 2026-11-26T04:40Z (lane: the recurring n11 long-term lane that published
the sixth-cost exclusive probe batch 30e694a6/1b262355/e0a30fab/f348343e, the first
resumption k03 checkpoint 92ddb69b/28a038a5/3d1e5639, the second resumption k04
checkpoint cb7ffe05/1ccbe303 (note 65f7a3f8), and the k01/k03 and k04
third-implementation verdict re-verification single-owner notes (53d8fe28 /
d5371854 of 2026-11-22 and the k04 addendum note of 2026-11-22 with its
k01-k03-dir publication bcc39add).
HEAD re-fetched immediately before this push: `ec7acda6bb3a91e5eb566b09e928e6a9aff67f89`
(Part EM wave F completion, 2026-11-26T04:22:47Z; no other lane has pushed since).
No other session has started k05 (repo code search for k05 raws: the newest
sixth-cost artifacts are still the k04 witness publication 1ccbe303 of 2026-11-22;
no third-resumption note exists before this one).

## Scope: resume the halted batch at k05..k43 (40 remaining keys, no new keys claimed)

The second resumption session halted at k04 on the pre-registered WIN stopping
rule; that stop is session-scoped ("no further claimed-key starts THIS session"),
so this session resumes the remaining 40 exclusive keys k05..k43 of the SAME
published machine list (`n11-sixthcost-exclusive-selection-v1`,
output/sixth-cost-exclusive-keys.json, authoritative `exclusive_probe_order`).
No new key is claimed; the k01 LOSS and k02/k03/k04 WIN raw rows and all their
unconsumed verdicts are unchanged.

Since the k04 halt, the verification position kept improving WITHOUT any
disagreement being published: k02, k03 and k04 each gained a published pinned
third-implementation WIN reproduction (two full cold runs + one verify-legal run
each, k04 addendum bcc39add/audit_k04.py 31/31 fail-closed gates), k01 gained a
published LOSS x2 third-implementation reproduction (90f38c95), and the
third-implementation bank full-band recalibration landed 198/198 verdict-level
agree (c3c62fd4). The delegated pinned C++ gates remain recorded and UNCHANGED
(k01 `1297036692683751424:1114112` expected 2/10,369,650; k02
`1297036692683751424:68157440` 1/7,717,432; k03 `10376293541461626880:65792`
1/9,255,414; k04 `10376293541461626888:65536` 1/9,433,024; all @15,000,000,
gate source cpp/solvers/kyouen_dfpn_root.cpp sha256 9193f5b6...). The canonical
merged exact-S5 chain head of record moved well past this program's frozen
increment base (bb4495e0 via 9c4dd94e / 63f33c4f to the current Part EM head
6e49dd84, 6,792 rows WIN192/LOSS6600) purely through central-reply adoption
Parts; those adoptions never touched this class's exclusive keys (the selector's
disjointness gates below re-verify against the pinned bases; the central-reply
chain consumes only its own closure-batch/probe territory). This session's
expectation is honest either way: more band-1 WINs add redundancy against any
single-row rejection, more LOSSes refine the mixed bin prior
(bin_prior_all_loss_index 0.34616); the batch never consumes verdicts.

## Declarations re-run on this host BEFORE any ladder start

- D1 Selector re-execution (scripts/select_sixth_exclusive.py, byte-identical to
  the published copy, all 13 sha256 input pins verified inside the selector,
  inputs fetched at HEAD ec7acda6): ALL 229 fail-closed gates PASS
  (stdout `{"all_gates_pass": true, "gates": 229, "exclusive_keys": 43,
  "proxy_exclusive_sum": 229056664}`). The regenerated selection JSON is
  byte-identical to the published one (sha256
  d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87) and all 43
  regenerated k01..k43 input CSVs are byte-identical to the published batch inputs
  (43/43 cmp).
- D2 Validation gate on THIS execution host (input/val-gate/ 4 rows, pinned
  Node.js replica jsreplay.js sha256
  845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df): 4/4
  node-exact PASS (at2m x2 result 0 / nodes 2,000,000 / legal 98, 99; 15M rows
  result 2 / nodes 3,651,923 and 5,040,200 / legal 98, 99); only wall_s differs
  (this host 10/9/18/26 s vs the resume2 host 9/9/17/24 s). This host's rows are
  published as a new val summary file (distinct name, no overwrite):
  output/val-gate-summary-resume3-20261126.json (pushed together with this note).

## Pre-registered ladder and stopping rules (fail-closed, identical to the first and second resumptions)

- Per key, in ascending truncated-cost-proxy machine order k05..k43: stage 2M
  (one run); if result nonzero, a second independent 2M run must reproduce
  identical (result, nodes); if result 0 (UNKNOWN), escalate to 15M: two
  independent cold runs. Both 15M runs nonzero-and-identical => resolved; both
  15M runs exhausted (result 0, nodes 15,000,000) => parked (no cache row). A
  disagreement across a determinism pair is a hard stop of the batch: record the
  anomaly, publish the raw outputs plainly, hand the divergence to the next run;
  no interpretation and no consumption in this session.
- Any WIN (result 1) at any stage stops further claimed-key starts in THIS session
  (rule (1) of the parent batch): publish the WIN checkpoint raws with honest
  labels (plus a voluntary third cold verification run for any WIN, honestly
  labeled, per the k02/k03/k04 precedent); verdicts of the entire batch remain
  unconsumed.
- Raw rows are pushed incrementally to the published output/raw/ as per-key
  checkpoints (at2m-kNN, at15m-run1-kNN, at15m-run2-kNN, at15m-run3-verify-kNN)
  with status.log appended in the published format; the batch never claims a
  verdict before its full audit, merged cache increment and SHA-256 manifest are
  published.
- Consumption gate (unchanged): rows resolved here (LOSS with identical
  determinism pairs) may enter a merged cache increment that byte-preserves the
  chain tip plus the new rows, under the WIN/LOSS conflict gate, with a
  fail-closed audit JSON and a sha256 manifest; k01/k02/k03/k04 rows never enter
  any increment (delegated C++ gate). Before such an increment, main is re-fetched;
  if any third-implementation disagreement about this lane's rows has been
  published meanwhile, this batch also stays unconsumed and the increment is not
  published. No increment is planned THIS session.
- A session wall-time budget is pre-registered (see Environment facts): if the
  ladder is still running when the session budget ends, the batch stops at the last
  completed key (honest "budget-stop" status in status.log); remaining keys stay
  claimable by the next run.

## Concurrency and disjointness

- Latest main was re-fetched immediately before this push (HEAD ec7acda6, Part EM
  wave F completion 2026-11-26T04:22:47Z): the Part EM adoption (central-reply
  emloss21 territory) is fully orthogonal to this lane's S5 exclusive keys;
  the strip/Z-census lanes (z25f20 kit 155c6ad2) touch no probe path; no other
  sixth-cost artifact has landed since the k04 witness publication (1ccbe303,
  2026-11-22).
- Each ladder checkpoint push in this session re-fetches HEAD first; if any
  concurrent lane pushes between two checkpoints, the new HEAD is recorded in
  status.log at the next checkpoint and disjointness is re-asserted (probe keys are
  machine-disjoint from all claim sets, re-verified by the selector's gates above).
- This session pushes only: this note, this host's new val summary file, new
  output/raw/* checkpoint files with status.log appends, a README checkpoint
  appendix at the end, and a session log. No cache file is modified; no K item; no
  knowledge README edit (verdict-unconsumed-class batch per precedent).

## Environment facts

- Node v22.20.0, Python 3.12.14, 2 cores; serial single-process foreground ladder
  runs (one jsreplay process per run, no parallelism).
- No C++ toolchain (re-verified this session: no gcc/g++/clang/zig on PATH;
  package installation is forbidden in this sandbox); delegated C++ gate unchanged
  (k01/k02/k03/k04 expectations recorded above).
- Unauthenticated raw.githubusercontent.com working; every input fetched at pinned
  commit ec7acda6 and sha-verified by the selector's own fail-closed gates.

## Status guard

Scheduling and raw evidence only. The standard 11x11 empty board, the two-stone
root {60,27}, and its remaining third moves 100/108 remain UNKNOWN throughout.
Nodes, budgets, proxy values and solved counts are never verdicts. This batch
cannot close the class (58 shared children remain outside this lane); any
class-level statement will only be made machine-checked against the full
108-child set.
