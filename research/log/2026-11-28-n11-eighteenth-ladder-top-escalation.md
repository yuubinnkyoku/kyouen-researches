# Completion log: n11 eighteenth ladder-top escalation

Completion of the Part declared in
`research/log/2026-11-28-n11-eighteenth-ladder-top-escalation-declaration.md`
(declaration commit `53749821`, single owner, publish-then-execute).
Kit: `research/experiments/n11-eighteenth-ladder-top-escalation-20261128/`
(commit `88e825d5`, 11 files; fetch-back byte-identical against the
kit MANIFEST-sha256 via commit-pinned raw CDN + sha256).

## Result

- Declared order k03 -> k04 -> k05 at 15M, WIN-stop at the first
  WIN(1), cold pair each.
- **k03 `1155173441859489792:131072` (s5 605961, legal 73)
  resolves WIN(1), nodes 5,266,012 (35.1% of the 15M budget),
  cold pair node-identical (raws byte-identical `a80c2dcb`,
  wall_s 26/26).** WIN-stop fired; k04/k05 stay at their
  published stage-1 2M UNKNOWN(0) (sixteenth escalation kit
  `85edd462`).
- Calibration u01 `1153485622925590528:0` at 2M (run after the
  declaration, before the 15M runs) reproduces the published
  calibration VALUES exactly: result 0, nodes 2,000,000,
  forbidden quadruples 95,670, wall_s 9; input csv byte-identical
  `52d79efc`.
- Head basis: `e56ca5ca...` (6,902 rows WIN 220 / LOSS 6,682,
  seventeenth k02 adoption head). Freshness measured on this
  host by direct row scan: 0 rows for each of k03/k04/k05; the
  adopted k02 row present exactly once (the only delta from the
  sixteenth k01 head `dbc1d950...`).
- Runner: jsreplay.js `84585617...` (published pinned replica of
  the C++ standalone exact-replay path at commit `154f3b7a`),
  re-fetched from the published twelfth-cost kit and sha-verified
  this session; Node.js v22.20.0; fresh cold solver per row.

## Claim status / next

Escalation bookkeeping only: NO verdict is consumed. The k03
WIN(1) row is single-implementation (jsreplay replica) and
requires the C++ second-implementation scrutiny gate plus a
third-implementation corroboration before any adoption Part; a
k03 adoption would additionally require the standing WIN-side
flip-census review (owner union k03 [18136, 18143, 20128, 20421]
with the shared-owner pre-exclusion caveat). Class 20421 is NOT
complete (k04-k05 remain stage-1 2M UNKNOWN). The standard 11x11
empty board, all 19 central-reply roots, the two-stone root
{60,27} and third moves 100/108 remain UNKNOWN. Nodes and wall_s
are bookkeeping, never verdicts.
