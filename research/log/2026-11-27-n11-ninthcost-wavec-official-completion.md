# 2026-11-27 n11 ninth-cost wave C official completion (stage-1 2M sweep + 15M escalation + k12 WIN row third-implementation corroboration)

Owner lane: ninth-cost class `1297036692683751424:134217728` exclusive S5
probe (single-owner declaration wave A ac4d7432, selection kit wave B
4e8d2c7a). This Part executes the official wave C that the previous session
lost to an execution-environment reset (honest record 76181b40), on a fresh
host, per the resume instructions recorded there.

## Execution and environment disclosures

- Two hosts were used across ONE execution-environment reset (disclosed):
  the reset happened while a bash chunk was running and discarded the first
  attempt's 44 completed at2m raws; all raws were re-executed from scratch on
  the fresh host and all subsequent state was kept on the persistent
  knowledge mount `_ninth-wavec/` and published incrementally (waves
  C1..C7) so no further state was host-local.
- Val-gate was reproduced node-exact on BOTH hosts (at2m 0,2000000 x2
  targets; at15m 2,3651923 and 2,5040200). jsreplay byte-clone 84585617
  verified against the published MANIFEST (kit inputs 50/50 byte-identical
  on fetch-back).
- One bash chunk timed out at the 290s wall (k04+k05 pair); k04's completed
  pair survived on the knowledge mount, k05's partial file was deleted and
  re-executed. All values are from complete runs only.

## Stage-1 2M cold-pair sweep (waves C1-C5)

All 45 keys k01..k45: result 0 / nodes 2,000,000 on both passes (90 rows).
All 45 pairs node-identical. Published: `output/raw/at2m-run{1,2}/`,
summary `output/stage1-2m-sweep-summary.json`. Matches the disclosed lost
scratch round node-exactly.

## Stage-2 15M escalation, ascending (waves C6-C7)

- k01 LOSS(2) 2,163,556; k03 LOSS 7,753,840; k05 LOSS 8,687,533;
  k06 LOSS 8,130,387; k08 LOSS 3,306,768; k09 LOSS 4,711,230;
  k10 LOSS 5,542,083 (all node-exact reproductions of the disclosed scratch
  observations, cold pairs node-identical).
- k11 LOSS 5,931,960; **k12 WIN(1) nodes 14,521,862** (new results; k11/k12
  were never reached in the lost scratch round). k12 is the first WIN of
  the ninth-cost batch; the pre-registered WIN stopping rule FIRED and
  escalation was suppressed for k14..k45.
- k02 / k04 / k07 UNKNOWN@15M (nodes 15,000,000 x2, pairs identical) = L50M
  escalation candidates (parked).
- **Overreach disclosure**: k13's 15M cold pair (LOSS(2), nodes 4,217,733)
  executed within the same bash command after the k12 WIN determination,
  before the operator observed it. Disclosed as an observation only, NOT
  consumed; official k13 status = 2M UNKNOWN pair, escalation suppressed
  (same treatment as the eighth-cost k02 precedent). The batch summary
  JSON records this.

Batch summary: `output/batch-summary-15m.json`
(schema n11-ninthcost-batch-checkpoint-summary-v1).

## k12 WIN row third-implementation corroboration (kit d9ce050a)

CORROBORATION-PASS verdict-level: pinned third_impl.js (08ea958f, standing
implementation, not fresh) reported result 1 (WIN) in both cold passes,
expansions 17,247,041 identical (a first cap-15M pair ended runlimit:cap
INDET, disclosed; cap raised to 400M per the seventh-cost precedent). Kit
`research/experiments/n11-ninthcost-k12-win-thirdimpl-corroboration-20261127/`.
The C++ second-implementation scrutiny gate (Part SR/SW/SX pattern,
expected quadruple for k12 = 92,15000000,1,14521862) remains pending and is
required before any adoption of the WIN row, together with a WIN/LOSS
conflict review and a fresh single-owner adoption declaration.

## Verification

- All 116 published raws fetch-back verified byte-identical against the
  knowledge-mount copies at HEAD 913373d8 (raw CDN sha256 compare).
- `MANIFEST-raw-sha256.txt` (116 rows, sha size path) published for the
  kit raws.
- The 8 LOSS rows of this batch are single-implementation (Node.js
replica) apart from the k12 corroboration; per the k20/k33/k05/k01
precedent they need the C++ gate before adoption.

## Resume (next session)

1. Re-fetch latest main first (hourly parallel lanes).
2. Next Part: k12 WIN row C++ second-implementation scrutiny gate (zig
   0.13.0, runner/gate source pin 154f3b7a, expected quadruple
   92,15000000,1,14521862, single-row WIN form as the eighth-cost k01
   gate kit n11-eighthcost-k01-win-cppgate-20261127). Also eligible: the
   8 LOSS rows C++ gate (41-loss Part SW pattern). After both pillars:
   adoption Part (BASE 0935c94c, fresh declaration, WIN/LOSS conflict
   review, k05/eighth-k01 win-hit flip census review) with the merger and
   reaudit/flip-census machinery of the eighth-cost SZ/EM precedents.
3. Parked k02/k04/k07 are L50M escalation candidates (declaration first).
4. The ladder pre-audit instrument needs a ninth ledger pin extension
   before it can audit this batch (the eighth pre-audit precedent).

## Guards

Scratch observations only unless published above; no verdict is consumed or
claimed. All rows are single-implementation except the disclosed k12
third-implementation corroboration. The standard 11x11 empty board:
UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root {60,27}:
UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure class: UNKNOWN
unless a published Part says otherwise. WIN(1)/LOSS(2) rows are cache
bookkeeping rows only; nodes and expansions are never evidence of WIN or
LOSS beyond the fail-closed replay semantics.
