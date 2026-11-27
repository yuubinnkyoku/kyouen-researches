# n11 sixth-cost k06/k07/k08 third-impl re-verification session log (2026-11-26)

Session lane: the recurring n11 long-term lane. Scope executed under the
single-owner declaration
`research/log/2026-11-26-n11-sixthcost-k06-k07-k08-thirdimpl-verdict-single-owner-note.md`
(push `b9dc2bb3`, declared 2026-11-26T07:58Z at HEAD `dc7f36e1`): the
third-implementation verdict re-verification program was extended to the
three fourth-resumption rows with no third-impl verdict yet (k06/k07/k08),
per the program's fresh-declaration rule.

## Chain

1. Declaration pushed (`b9dc2bb3`) BEFORE any target-row execution, after a
   repo probe finding no competing claim (`audit_k06` 0 hits; kit dir holds
   exactly the k01/k03 parent program plus k04/k05 addenda).
2. All eleven replica raws consumed at HEAD `dc7f36e1` over
   raw.githubusercontent.com, byte-hashed here, then re-published at
   `out/k06-replica-raws/`, `out/k07-replica-raws/`, `out/k08-replica-raws/`
   (k07's run1/run2 raws and k08's run1/run2 raws are byte-identical pairs
   at the blob level; that is expected and is what the probe lane
   published).
3. C1 calibration on THIS host: verify_tbl quads equality 95,670 == 95,670
   over 195,044 triples, 0 mismatches, rc=0; anchor w2 WIN(1) expansions
   7,583,990 == the published ea73c3e3 witness value, two executions
   (21.57 / 21.65 s) identical counts.
4. C2 runs (all cold, independent solvers, serial, one node process at a
   time, --cap=400000000 --wallcap=270 --memo-power=22):
   k06-a/k06-b both LOSS(2) expansions 9,474,431 ttHits 5,163,124
   ttOverwrites 5,280,127 (walls 27.38 / 28.03 s);
   k07-a/k07-b both LOSS(2) expansions 1,608,994 ttHits 935,234 ttOverwrites
   169 (walls 4.83 / 4.84 s);
   k08-a/k08-b/k08-v all WIN(1) expansions 7,243,596 ttHits 3,873,045
   ttOverwrites 3,050,565 (walls 19.88 / 19.77 / 35.67 s; --verify-legal=1
   derived masks == from-scratch legality at every visited node).
   Verdict-level agreement with the published replica raws on all three
   rows (2v2, 2v2, 1v1). Determinism identical within each row.
5. C4 negative gates: all six GATE_FAIL rc=1 with the pinned mismatch
   strings (`out/neg-gate-*`).
6. `audit_k06k07k08.py` written as a SEPARATE auditor (audit.py /
   audit_k04.py / audit_k05.py byte-frozen): 82/82 gates ALL PASS rc=0,
   deterministic byte-identical output across runs in a fixed layout;
   tamper battery 2/2 fail-closed (T1 k08 cold verdict flip 1->2 ->
   C2_k08_determinism_3runs_identical + C2_k08_win_verdict_level_vs_replica;
   T2 k06 replica-raw nodes edit -> repl_sha_* + repl_row_* +
   repl_k06_loss_2runs_unanimous), kit restores byte-verified, final clean
   control rc=0 (`out/audit-tamper-controls-k06k07k08.txt`).
7. Publication: addendum files + README k06/k07/k08 addendum + MANIFEST
   append pushed; raw fetch-back byte-verified for every pushed file.

## Honest session notes

- The auditor's replica-path resolution section was edited twice BEFORE the
  first audit run (local-kit vs published-layout candidates); the Published
  auditor is the clean final version; no raw predates or postdates any
  audit edit; no gate was weakened at any point.
- The auditor's first execution on this host failed ONLY at
  `pin_jsreplay_js_sha256` ("not found in any candidate location"): the new
  host's local kit copy of `inv/jsreplay.js` had not been laid down yet.
  Fixed by copying the pinned file from the 2026-11-22 lane kit (sha256
  re-verified 84585617...), a resolution fix, not an audit-content edit;
  re-run then 82/82 rc=0.
- The audit summary JSON is byte-identical across runs in a fixed layout;
  across layouts the only differing bytes are resolved-path detail strings
  (the precedent published JSONs carry their hosts' absolute paths in those
  fields; same normalized output byte-identical).
- The published tamper log is the transcript of one full battery re-run
  (baseline / T1 / T2 / final control); an earlier inline exploratory
  battery had produced the same rc values and failed-gate lists.
- A garbled gate-count sentence in the README addendum was fixed BEFORE the
  push (no measurement affected).

## Result summary (verdict-level; nothing consumed)

| row | third impl | replica | agreement |
|---|---|---|---|
| k06 `10376293541462675456:65536` | LOSS(2) | LOSS(2) 8,182,231 @15M (x2) | yes |
| k07 `10376293542535368704:65536` | LOSS(2) | LOSS(2) 1,419,823 (x4) | yes |
| k08 `10376293610182148096:68719476736` | WIN(1) | WIN(1) 6,195,897 @15M (x3) | yes |

With this addendum every resolved row of the k01..k08 chain now has an
independent third-implementation verdict re-verification (k02 via the
original ea73c3e3 program, k01/k03/k04/k05 via this dir's addenda, k06/k07/k08
via this addendum). All verdicts remain UNCONSUMED; the delegated pinned C++
gates for all eight rows (`9193f5b6...`) remain recorded, UNCHANGED and not
executable on this sandbox (no C++ toolchain); adoption stays with the
scrutiny owner. The k09..k43 fifth-resumption rows (30 LOSS + 5 parked) have
no third-impl reproduction yet.

## Resume pointers (next natural steps, after re-fetching latest main)

- Third-impl batch extension to the 30 resolved k09..k43 LOSS rows (fresh
  single-owner declaration required; the smallest replica-node rows first if
  a session budget is short).
- The parked-4-keys (k13/k19/k20/k33) L50M ladder is single-owner declared by
  the parallel lane (`9e042a5f`); k38's L50M followup remained unclaimed at
  this session's close.
- The C++ delegated gates for k01..k08 stay open for any host with a C++
  toolchain.

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining
third moves {100,108} remain UNKNOWN throughout. Node/expansion counts,
budgets and wall times are never verdicts. This session consumed no verdict,
touched no cache file, no probe-dir path, no K item and no knowledge README.
