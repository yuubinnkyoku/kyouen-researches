# n11 sixth-cost class 10376293541461626880:65536 exclusive S5 probe resumption batch k03..k43: single-owner note (2026-11-21)

Declared: 2026-11-21T21:37Z (lane: the n11 long-term lane that published the sixth-cost
exclusive probe batch `30e694a6`/`1b262355`/`e0a30fab`/`f348343e`, the third-cost probe and
the parked-2 L50M ladder). HEAD at the moment of composition, re-fetched immediately before
push: `73cb82bd6538ef2f4e35c25ba1530f5733d51f01`.

## Scope: resume the halted batch at k03..k43 (41 keys, no new keys claimed)

The parent session's batch halted at k02 on the pre-registered WIN stopping rule; that stop
is session-scoped ("no further claimed-key starts THIS session"), so this session resumes the
remaining 41 exclusive keys k03..k43 of the SAME published machine list
(`n11-sixthcost-exclusive-selection-v1`, `output/sixth-cost-exclusive-keys.json`). No new
key is claimed; k01/k02 raw rows and their unconsumed verdicts are unchanged.

Declarations re-run on this host BEFORE any ladder start, all recorded in this session:

- D1 Selector re-execution (`scripts/select_sixth_exclusive.py`, unmodified, at HEAD
  `73cb82bd`): ALL 229 fail-closed gates PASS under the sha-pinned inputs (probe-13 chain
  base `60e0dc34...` 5,756 rows; latest published chain increment still
  `bb4495e0...` 5,793 rows — no newer increment exists at composition time; frozen geometry
  3,384 classes; all concurrent claim sets focus35/cert38/third39/fourth41/fifth44/sbd101/
  parked-2 machine-read and disjoint). The regenerated selection JSON is byte-identical to
  the published one (sha256 `d5e9b059...`), and all regenerated k03..k43 input CSVs are
  byte-identical to the published batch inputs.
- D2 Validation gate on THIS execution host (`input/val-gate/` 4 rows, pinned Node.js
  replica `jsreplay.js` sha256 `84585617...`): 4/4 node-exact PASS against the published
  rows (at2m x2 result 0 / nodes 2,000,000 / legal 98, 99; 15M rows result 2 / nodes
  3,651,923 and 5,040,200 / legal 98, 99); only wall_s differs. New
  `output/val-gate-summary-resume.json` will record this host's rows.

## Pre-registered ladder and stopping rules (fail-closed)

- Per key, in ascending truncated-cost-proxy machine order k03..k43: stage 2M (one run);
  if result nonzero, a second independent 2M run must reproduce identical (result, nodes);
  if result 0 (UNKNOWN), escalate to 15M: two independent cold runs. Both 15M runs
  nonzero-and-identical => resolved; both 15M runs exhausted (result 0, nodes 15,000,000)
  => parked (no cache row). A disagreement across a determinism pair is a hard stop of the
  batch: record the anomaly, publish the raw outputs plainly, hand the divergence to the
  next run; no interpretation and no consumption in this session.
- Any WIN (result 1) at any stage stops further claimed-key starts in THIS session
  (same rule (1) as the parent batch): publish the WIN checkpoint raws with honest labels;
  verdicts of the entire batch remain unconsumed (k02 precedent).
- Raw rows are pushed incrementally to `output/raw/` as per-key checkpoints
  (`at2m-kNN`, `at2m-run2-kNN`, `at15m-run1-kNN`, `at15m-run2-kNN`) with `status.log`
  appended in the published format; the batch never claims a verdict before its full
  audit, merged cache increment and SHA-256 manifest are published.
- Consumption gate for THIS batch (only if it completes with zero WIN): rows resolved
  here (LOSS with identical determinism pairs) may enter a merged cache increment that
  byte-preserves the chain tip `bb4495e0...` (5,793 rows) plus the new rows, under the
  WIN/LOSS conflict gate, with a fail-closed audit JSON and a sha256 manifest. The k01/k02
  rows do NOT enter any increment: their adoption stays gated on the delegated pinned C++
  second-implementation verification (`cpp/solvers/kyouen_dfpn_root.cpp`, sha256
  `9193f5b6...`; k02 expected result 1 / nodes 7,717,432, k01 expected result 2 / nodes
  10,369,650), and the concurrent third-implementation re-verification
  (`ceb4eed71`, declared 20:45Z) is additional evidence only in this lane's reading.
- Before that increment is published, main is re-fetched; if the third-implementation
  re-verification lane has meanwhile published any DISAGREEMENT about this lane's
  published rows, this batch's verdicts also remain unconsumed and the increment is not
  published in this session (handed to the next run).

## Concurrency and disjointness

- The 43-key machine list is claimed by this lane's parent declaration; this note changes
  no claim set. The n11 third-implementation re-verification (`ceb4eed71`) claims no new
  keys and writes no cache file; its targets (k01/k02 raws, validation pair, parked pair,
  possibly the 37 third-cost rows) are disjoint from the k03..k43 ladder keys. The
  fourth-cost pass-1 (`a808d05a1`) published raws only for its own fourth-cost class
  keys (machine-verified disjoint in D1); no cache increment from it exists at composition
  time (verified: chain tip still `bb4495e0`). All other concurrent lanes since the parent
  declaration (seven-row, six-row, five-row, four-row, s12/s13) are non-n11-S5 topics.
- Pushes to this experiment dir are limited to new `output/raw/*` checkpoint files,
  `status.log` appends, this-lane audit/merge/manifest artifacts and README checkpoint
  sections; the shared knowledge README and K items are not touched by this batch
  (verdict-unconsumed-class batch per precedent).

## Environment facts (recorded for the next runs)

- 2 cores; Node.js v22.20.0; Python 3.12.14; serial single-process foreground ladder runs.
- No C++ toolchain and package installation forbidden (re-verified this session): the
  delegated pinned C++ second-implementation gate for k01/k02 stays delegated.
- Unauthenticated raw.githubusercontent.com worked throughout this session so far; the
  20:33-20:36Z unauthenticated outage observed by the parallel run is noted; fetch-backs
  prefer authenticated app-tool blob-sha comparison (git blob sha1 of both sides).

## Status guard

Scheduling and raw evidence only. The standard 11x11 empty board, the two-stone root
{60,27}, and its remaining third moves 100/108 remain UNKNOWN throughout. Nodes, budgets,
proxy values and solved counts are never verdicts. This batch cannot close the class
(58 shared children remain outside this lane); any class-level statement will only be
made machine-checked against the full 108-child set.
