# n11-ninthcost-parked3-l50m-thirdimpl-corroboration-20261127

Third-implementation corroboration pillar for the three ninth-cost
stage-3 L50M resolved rows of the exclusive S5 probe class
`1297036692683751424:134217728` (wave B commit 41b331d1,
`output/batch-summary-l50m.json` of the ninth-cost exclusive-probe kit):
k02, k04, k07. With this Part every resolved row of the ninth-cost
ladder (9 LOSS + 3 WIN) has the third-implementation pillar.

## Result: CORROBORATION-PASS (verdict-level)

Standing third implementation `third_impl.js` (sha256 08ea958f...,
byte-clone of the published k12-win thirdimpl kit copy, byte-verified),
protocol cap=400000000, wallcap=260, memo-power=22, two fresh cold
passes per key (one node process per pass, node_rc captured directly by
the shell in the same command), declaration commit 9b4cdaac
(publish-then-execute):

- k02 `1297036692683751424:201326592` (legal 87): **result 1 (WIN)**,
  expansions 21,380,266, ttHits 11,785,622, both passes identical.
- k04 `1152921504607903744:536903680` (legal 98): **result 2 (LOSS)**,
  expansions 28,939,982, ttHits 14,857,679, both passes identical.
- k07 `1152923703765368832:68719476736` (legal 96): **result 1 (WIN)**,
  expansions 33,128,202, ttHits 16,617,418, both passes identical.

All 6 passes: reason clean, node_rc=0, quads=95670, legal derived ==
published legal, per-key pairs identical on every field except wall_s.
Verdict-level agreement with the replica (published L50M cold pairs:
k02 WIN nodes 18,123,017 / k04 LOSS 24,309,957 / k07 WIN 27,621,128).
Node and expansion counts are bookkeeping and are not expected to
match across implementations.

Pre-registered acceptance of the declaration was met on all three keys
(k02 WIN / k04 LOSS / k07 WIN). No pass was discarded; no INDET pass
occurred (all passes resolved clean well under the cap).

## Honest disclosures

- Execution happened after the wave-A declaration push (9b4cdaac) and
  before this publication; wall_s differs per pass and timing is not
  evidence.
- The three rows remain single-implementation replica rows plus this
  third-impl pillar; the C++ second-implementation scrutiny gate (Part
  SR/SW/SX pattern) for k02/k04/k07 remains OPEN. The three rows are NOT
  adoption-eligible until that gate is published; the batch adoption
  Part additionally needs a fresh single-owner declaration and the
  WIN/LOSS conflict review.
- No verdict consumed; no cache increment; no class-status change; no
  coverage claim; no adoption.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Files

- `scripts/third_impl.js`: byte-clone of the pinned third implementation
  (sha256 08ea958f...).
- `output/raw/<key>.p1.txt` / `.p2.txt`: the 6 cold-pass raws.
- `MANIFEST-sha256.txt`: kit manifest (sha256sum-compatible, 2-column).

## Guards

The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. A third-implementation WIN(1)/LOSS(2) agreement is not a
class closure claim, not a root verdict, and transfers nothing.
