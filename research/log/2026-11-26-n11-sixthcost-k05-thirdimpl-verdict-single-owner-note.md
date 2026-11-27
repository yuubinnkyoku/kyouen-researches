# n11 sixth-cost k05 third-implementation verdict re-verification: single-owner addendum note (2026-11-26)

Declared: 2026-11-26T04:55Z (lane: the n11 long-term lane; this note extends the
third-implementation re-verification program of
research/log/2026-11-22-n11-sixthcost-k01-k03-thirdimpl-verdict-single-owner-note.md
and its k04 addendum
research/log/2026-11-22-n11-sixthcost-k04-thirdimpl-verdict-single-owner-note.md
to the k05 row published earlier today, following the WIN-row precedent that the
third-implementation program extends only with a fresh declaration). HEAD
re-fetched immediately before this push: `68bc863d` (a parallel lane's z=26
floor-20 census commit whose paths - the `strip-z26-floor20-20261126` experiment
dir and its log - are disjoint from every path written here; this lane's own
latest commit remains `9f6434f5`, the k05 witness-publication commit; the ladder
is halted per its pre-registered WIN rule with k06..k43 NOT started, so the keys
claimed here are otherwise idle).

Host honesty: this addendum runs on a NEW host (Vibe sandbox with Node.js and
Python3, no C++ toolchain), NOT the 2026-11-22 third-impl host. The C1
calibration was therefore re-executed fresh on this host this session instead
of reusing the published calibration raws (honest non-reuse).

## Scope

- PRIMARY: k05 `10376293541461757952:65536` (stones 5, legal 88; today's fresh
  replica raw WIN(1) nodes 13,397,611 at 15M, three cold runs identical, plus a
  2M UNKNOWN stage raw nodes 2,000,000 result 0, published at commit
  `704cb3ef`): the fifth unconsumed WIN raw of the n11 exclusive-probe program
  (third resumption, machine order 5, declared in
  research/log/2026-11-26-n11-sixthcost-class10376293541461626880-exclusive-s5-probe-resume-k05-k43-single-owner-note.md).
  Row spec `target,0,5,10376293541461757952,65536,88,0,0,0,0,0`.
- Implementation and pins identical to the k01/k03 and k04 notes (third_impl.js
  sha256 `08ea958f...`, verify_tbl.js `c8c52528...`, replica jsreplay.js
  `84585617...` consumed by verify_tbl.js only; the four k05 raws consumed at
  HEAD `9f6434f5` under
  `n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/output/raw/`
  were fetched and byte-hashed here, then re-published inside this experiment
  dir at `out/k05-replica-raws/` with per-file sha pins in `audit_k05.py`).
- C1 calibration executed THIS session on THIS host (fresh host, see above):
  verify_tbl equality replica quads 95,670 == mine 95,670 over 195,044 random
  triples, 0 mismatches, rc=0 (`out/k05-calib-verify-tbl.txt`); anchor w2
  `10376293541461626880:131328` reproducing WIN(1) expansions 7,583,990 == the
  published ea73c3e3 witness value on both executions (22.51s rc-annotated kept
  in `out/k05-calib-anchor-w2.txt`, 22.17s in
  `out/k05-calib-anchor-w2-run2.txt`), identical counts.
- C2 k05 verdict-level expectation WIN(1); three full cold runs of third_impl
  with identical (result, expansions, ttHits, ttOverwrites) plus the
  `--verify-legal=1` run with identical (result, expansions): observed
  result 1, expansions 15,949,585, ttHits 8,391,212, ttOverwrites 11,755,281
  on all three (walls 44.44 / 45.13 / 80.42s), against replica WIN(1) nodes
  13,397,611. Expansion counts are never compared to replica node counts
  (different implementations count different quantities).
- C4 fail-closed input gates on k05: declared legal 89 (vs derived 88) ->
  GATE_FAIL rc=1; declared stones 6 (vs bits 5) -> GATE_FAIL rc=1.
- C5 any disagreement is a hard stop: publish raws, no interpretation, hand to
  the scrutiny owner. No disagreement occurred.
- Auditor: separate `audit_k05.py` (31 gates; the published `audit.py` and
  `audit_k04.py` stay byte-frozen), deterministic byte-identical output across
  runs, exit 0 only on all-pass; negative tamper controls on full kit copies:
  T1 k05 cold verdict flip 1 -> 2 fails closed via
  `C2_k05_determinism_3runs_identical` + `C2_k05_win_verdict_level_vs_replica`;
  T2 replica-raw nodes edit fails closed via `repl_sha_*` + `repl_row_*` +
  `repl_k05_win_3runs_unanimous`; both restores byte-verified; final clean
  control rc=0 byte-identical to baseline (`out/audit-tamper-controls-k05.txt`).
  Honest note: the published tamper log was reassembled from the executed
  control transcript after an inline gate-listing helper printed a SyntaxError
  into the transcript; rc values and failed-gate lists come directly from the
  control JSON outputs, and every kit restore was byte-verified. No raw
  predates or postdates any audit edit.
- C6 no verdict consumed; the delegated pinned C++ gate for k05
  (`cpp/solvers/kyouen_dfpn_root.cpp` sha256 `9193f5b6...`,
  `target,0,5,10376293541461757952,65536,88,0,0,0,0,0` @15,000,000, expected
  result 1, nodes 13,397,611) is recorded and UNCHANGED; it could NOT be run
  on this host (no C++ toolchain in this sandbox) and remains delegated to the
  scrutiny owner / external C++ resource; adoption stays with the scrutiny
  owner. **The standard 11x11 empty board, the two-stone root {60,27}, and
  its remaining third moves {100,108} remain UNKNOWN. Node/expansion counts
  are never verdicts.**
- Publication: new files + README k05 addendum + MANIFEST append inside this
  lane's experiment dir
  `research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/`
  (owned by this lane since the k04 addendum); no probe-dir writes, no K item,
  no knowledge README edit (same convention as the parent and k04 notes).
- Disjointness: the probe dir, the selector, and the k06..k43 resumption keys
  are untouched; the scratch full-kit copies used by the tamper controls live
  outside the published tree and are disposable.
