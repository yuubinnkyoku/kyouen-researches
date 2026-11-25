# n11 sixth-cost k04 third-implementation verdict re-verification: single-owner addendum note (2026-11-22)

Declared: 2026-11-22T01:05Z (lane: the n11 long-term lane; this note extends TODAY's
k01/k03 third-implementation re-verification program
research/log/2026-11-22-n11-sixthcost-k01-k03-thirdimpl-verdict-single-owner-note.md
to the k04 row published minutes ago, following the WIN-row precedent that the
third-implementation program extends only with a fresh declaration). HEAD at
composition, re-fetched immediately before this push: `cb7ffe05` (this lane's own
k04 checkpoint commit; the ladder is halted per its pre-registered WIN rule, so the
host is otherwise idle for this lane's claimed keys).

## Scope

- PRIMARY: k04 `10376293541461626888:65536` (stones 5, legal 83; TODAY's fresh replica
  raw WIN(1) nodes 9,433,024 at 15M, three cold runs identical, published at
  commit `cb7ffe05`): the fourth unconsumed WIN raw of the n11 exclusive-probe
  program. Row spec `target,0,5,10376293541461626888,65536,83,0,0,0,0,0`.
- Implementation and pins identical to the k01/k03 note (third_impl.js sha256
  `08ea958f...`, verify_tbl.js `c8c52528...`, replica jsreplay.js `84585617...`
  for verify_tbl only; k04 raws consumed at HEAD `cb7ffe05` byte-verified against
  the just-published blobs).
- Acceptance: C1 calibration already executed THIS session on THIS host
  (verify_tbl 95,670/95,670 + 195,044 triples 0 mismatches; anchor w2 expansions
  7,583,990 == published value) - recorded in the k01/k03 experiment dir; it is NOT
  re-run, the published raws from this same session are the calibration evidence on
  this host (honest reuse, timestamps in the raws).
- C2 k04 verdict-level expectation WIN(1); at least two full cold runs of
  third_impl with identical (result, expansions, ttHits) plus one `--verify-legal=1`
  run with identical (result, expansions).
- C4 fail-closed input gates on k04: declared legal 84 (vs derived 83) -> GATE_FAIL
  rc=1; declared stones 6 -> GATE_FAIL rc=1.
- C5 any disagreement is a hard stop: publish raws, no interpretation, hand to the
  scrutiny owner.
- C6 no verdict consumed; the delegated pinned C++ gate for k04
  (`cpp/solvers/kyouen_dfpn_root.cpp` sha256 `9193f5b6...`,
  `target,0,5,10376293541461626888,65536,83,0,0,0,0,0` @15,000,000, expected
  result 1, nodes 9,433,024) is recorded and UNCHANGED; adoption stays with the
  scrutiny owner. **The standard 11x11 empty board, the two-stone root {60,27}, and
  third moves {100,108} remain UNKNOWN. Node/expansion counts are never verdicts.**
- Publication: new files + README appendix inside this lane's own experiment dir
  `research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/`
  (owned by this lane since today's declaration); a separate auditor
  `audit_k04.py` so the published `audit.py` stays byte-frozen; MANIFEST appended.
  No K item, no knowledge README edit (same convention as the parent note).
- Disjointness: the sibling thirdimpl stretch-37 run and the n11-s4bd lane touch
  none of these paths; the probe dir is untouched by this note (only the k04
  thirdimpl experiment dir is written).
