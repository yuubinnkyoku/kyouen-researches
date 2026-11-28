# n11 thirteenth ladder-top k02 escalation (class 16757, stage-2 15M)

Execution kit of the escalation declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k02-escalation-declaration.md`
(publish-then-execute, declaration commit `b9c97423`, single owner).
Target: k02 `1152922672837951488:65792` (class 16757, legal 72,
s5_index 558553), the second and last remaining unknown S5 key of the
thirteenth ladder-top selected class 16757, under the head of record
`beecb024...` (6,894 rows WIN 212 / LOSS 6,682).  Prior state:
stage-1 2M UNKNOWN (escalation kit `12d8359c`, suppressed by the k01
WIN-stop rule).

## Result

| key | stage-1 2M (prior) | stage-2 15M (this kit) | pair byte-identical |
|---|---|---|---|
| k02 `1152922672837951488:65792` | UNKNOWN(0), nodes 2,000,000 | **WIN(1), nodes 3,485,963**, wall_s 17 | yes |

The declared procedure's stage-3 L50M was not required (k02 resolved
at stage-2).  With k01 (WIN(1) nodes 2,678,305 @15M, pillar-complete:
cppgate GATE-PASS + thirdimpl CORROBORATION-PASS, kits `f1f5c49d`),
both remaining unknown S5 keys of class 16757 are now measured WIN
rows at the single-implementation level.

## Claim status

Batch bookkeeping only: NO verdict consumed.  The k02 WIN row is
single-implementation (jsreplay replica) and requires the C++
scrutiny gate plus third-implementation corroboration under a
separate declaration before any adoption Part; class 16757 adoption
additionally requires the standing WIN-side flip-census review and
Board-verified free_now at adoption time.  11x11 remains UNKNOWN.

## Files

- `batch-summary.json` - machine summary (schema
  n11-thirteenth-ladder-top-k02-escalation-summary-v1).
- `k02.input.csv` - probe input (byte-identical to the selection and
  first escalation kits' k02 input).
- `raws/at15m-k02-p1.raw`, `raws/at15m-k02-p2.raw` - stage-2 15M cold
  pair, fully byte-identical including wall_s 17.
- `MANIFEST-sha256.txt` - sha256 of every file in this kit.

## Inputs (published elsewhere)

jsreplay runner sha256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`,
`--only=5 --memo=22`; head of record `beecb024...`; selection kit
dependency pins inherited unchanged from commit `fa4e6cb2`.
