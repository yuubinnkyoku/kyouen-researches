# Part EV second-environment verification (2026-11-26, long-term lane)

Independent verification of the Part EV WIN-4 C++ scrutiny gate
(b018/d002/e002/f017) published as waves 666fefd3 / b2f54948 / f6ab5c30 /
ee7a951b (completion log `2026-11-25-part-ev-win4-cppgate-completion.md`,
kit `research/experiments/n11-centralreply-closure-wins-b018d002e002f017-cppgate-20261125/`).
Every artifact consumed here was fetched from published bytes and
sha256-verified before use. This verification consumes NO verdict and
changes NO canonical state. The
parallel owner lane's Part EU waves advanced main during the verification
window (baa8a0c0 / f353dbe5 / efa482fd, all Part EU work, disjoint from
Part EV); HEAD re-checked immediately before this Part's push: 76835aa8
(Part EU wave F completion). No maker re-emission was part of this
verification: the kit inputs, SSOT registry and run artifacts are all
MANIFEST-pinned and byte-verified instead (V0).

## V0 - published-bytes fetch verification (all sha256 + size verified)

| source | pinned state | result |
|---|---|---|
| EV kit (36 MANIFEST entries: 8 input/SSOT + 14 raws + status + 5 audits + 3 kit scripts + t1/t2 JSON + tamper.log + 2 battery scripts) | main, kit MANIFEST-sha256.txt | **36/36 byte-identical, 0 mismatch** (sha256sum -c all OK on the fetched copy) |
| gate source kyouen_dfpn_root.cpp + kyouen_residual_micro.hpp + n11_s5_quarantine.hpp | 154f3b7a (EN/EO/EQ/ET/EV shared gate pins) | 3/3 = pins 9193f5b6... / 5976935d... / 2e36d694... |

## V1 - gate rebuild (independent binary from the pinned sources)

Pinned sources rebuilt at this host with zig 0.13.0
(`zig c++ -std=c++20 -O2` route; build-exe does not resolve the C++20
headers). Binary sha256 **b34f07e51e14cc5c8de121b2ee1933b0fb88efccc137b75074642cf2463a195a** - not pinned, per the EN/EO/EQ/ET/EV disclosure
policy (source pins authoritative; the published environment's binary
was 06be2036... - this is yet another independent binary from the same
pinned sources).

## V2 - full official re-run from published kit bytes (the core check)

All 7 rows re-executed with the published `scripts/gate_runner.sh`
(31dc23c3, byte-verified) two fresh-cold passes per row, one process per
pass, exact kit inputs, sequential single process at a time. This host,
2026-11-26 01:14:21Z-01:18:02Z (~3m41s wall). Honest note: rows were
dispatched anchors-first but with af039 last (the published run executed
it third); per-row execution is independent, so no verdict changes, but
this is disclosed for byte-honesty of the status-log comparison below.

**7/7 GATE-PASS** with (legal,budget,result,nodes) exactly the published
quadruples: anchor-at2m 98,2000000,0,2000000; anchor-aj001
84,30000000,2,5156075; anchor-af039 89,30000000,2,19234232; b018
60,15000000,1,3549602; d002 73,15000000,1,5359994; e002 79,15000000,1,
14112632; f017 82,15000000,1,3522635. Zero MISMATCH / GATE-FAIL /
GATE-CRASH / TRUNCATED.

- Raw comparison vs the published raws (14 files, byte-compared):
  **6/14 byte-identical outright** (at2m p1+p2, aj001 p2, b018 p1,
  d002 p1+p2); the other **8 differ ONLY in wall_s** (replay row field 9
  and the `# replay_done` tail): af039 p1 38s->41s / p2 41s->40s,
  aj001 p1 9s->10s, b018 p2 6s->7s, e002 p1 27s->30s / p2 29s->30s,
  f017 6s->7s (both passes). Every other column - legal, budget, result,
  nodes AND the internal key_lo/key_hi pair - is byte-exact, exactly the
  runner's declared pass-invariance discipline.
- gate-status.log: the 7 status lines carry identical verdict columns;
  only the UTC timestamp prefixes and the af039 dispatch position differ.
- Per-pass node total recomputed from the 7 re-run raws: single-pass
  **52,935,170** / two-pass bill **105,870,340** - both equal the
  published completion-log bookkeeping.

## V3 - audit regeneration on this host's own re-run directory

The published `scripts/audit_gate.py` (cfbba264) executed 4x against
this host's re-run directory: **4/4 rc=0, output byte-identical** sha256
**ded81846c7c3e1a957d580eb691ed31d8e0e1432460e37946e0aea554b0d0f1e**,
overall **PASS, 36/36 gates PASS** (G1 x14 raw-shape, G2 x7 two-pass
determinism, G3 x7 published pins, G4 status accounting, G5 x7 input
pins). Not published; this log is the record.

- Honest diff vs the published canonical audit
  0327dad83f7c33d475656d8d1f9ccd2e67c3b78f8f394b9a5daf74c2b96c91c4:
  exactly **5 entries differ, all G2 detail strings**, and each of the 5
  embeds the per-pass wall_s values quoted verbatim from the raws (e.g.
  af039 p1=...,38,... vs p1=...,41,...). All 36 gate STATUSES, the
  parsed rows block and the schema block are byte-identical; overall PASS
  on both sides. Cross-environment audit byte-identity is impossible BY
  DESIGN (the audit quotes wall_s verbatim, so the recorded published
  audit pins those impossible details); the second-environment invariant
  is statuses + rows + schema. Concretely, the Part EV "raw diff =
  wall_s column only" convention extends to the audit JSON as "audit
  diff = G2-detail wall_s fields only" - a stricter statement than
  Part ET's blanket "wall_s detail fields naturally differ".

## V4 - tamper battery (re-executed from published bytes, on a scratch clone)

Protocol: the byte-verified fetched kit copy was kept pristine; the
battery ran only on a scratch clone of it (fetched-copy integrity
re-verified 36/36 after the battery). Fail-safe ordering pin-assert ->
backup -> tamper -> pre-assert -> audit -> restore -> restore-assert held
on all three tamperings; every restore byte-verified.

- **T1** audit ROWS pin break (b018 expected nodes 3549602 -> 3549603):
  tampered-state script sha256 037750103105ae2bda791447c7d2bbc96d00f73e534b2ca438089b0f2a738b62 - **byte-match with the published tamper.log
  T1 value**; audit rc=1, FAIL **G3:b018** exactly as published; restore
  to pin cfbba264 byte-OK.
- **T2** raw nodes alter (d002.p1 5359994 -> 5359995): tampered-state raw
  sha256 4ff6100e306b8fd8a96541af50cd8dc177cae5e10f8397df256c9cac4ba376ce
  - **byte-match with the published T2 value**; audit rc=1, FAIL
  **G2:d002 + G3:d002** exactly as published; restore to pin 32d2378d
  byte-OK.
- **T3** phantom GATE-PASS appended to gate-status.log: tampered-state
  sha256 43d7f501278be6ec2b083b8dc3c08ad8f1c0b95c137b00520c08f1382773dfc1
  - **byte-match with the published T3 value** (unlike the Part ET
  battery, whose phantom-line bytes were not published; the EV battery
  script hard-codes the same line, so the tampered state reproduces
  byte-exactly); audit rc=1, FAIL **G4 passes=8/7** exactly as published;
  restore to pin 927339e0 byte-OK.
- The published lane's wrong-JSON-key capture bug (KeyError 'G3'/'G2' in
  the battery's result-probe, no effect on run artifacts) reproduced
  identically here on the first battery pass, as expected from the
  pinned battery bytes; the pinned recheck script then captured the fail
  sets **T1-RECHECK ['G3:b018']**, **T2-RECHECK ['G2:d002','G3:d002']**
  with the published detail texts, and the regenerated t1_result.json /
  t2_result.json **byte-match the kit pins a3732ce8 / 7891c46e**.
- Clean control rc=0 twice (battery end + recheck end); post-battery
  audit_gate.json regenerated **byte-identical to the canonical
  0327dad8**; post-battery full MANIFEST verify on the clone: **35/36
  PASS, tamper.log the sole expected diff** (the battery appends its own
  timestamped lines to tamper.log by design; the published pin covers
  only the original run's entries). The untouched fetched kit copy:
  **36/36 PASS** after everything.

## Honest / environment lessons (this lane's own incidents, disclosed)

1. Never hand-type pins - recurring: the 36-line MANIFEST was first
   transcribed by hand from the connector view and one sha line was
   mis-copied (f017, 65 characters, an inserted hex pair). sha256sum's
   "improperly formatted" warning caught it before any wrong
   verification claim was made; the line was corrected against the
   sha256sum of the already-fetched published bytes, after which
   sha256sum -c = 36/36 PASS. This is the Part ET lesson #1 recurring;
   transcription of pin manifests must always go through byte fetches
   and checksum-format assertions, not copy-typing.
2. No git CLI exists in this execution environment; all repo reads,
   the commit push and the fetch-back verification went through the
   authenticated GitHub app connector, every byte artifact pinned by
   sha256 at its pinned commit.
3. The audit-gate wall_s lesson (V3) generalized for future
   second-environment verifications of this gate family: compare
   statuses + rows + schema for byte-identity, disclose G2-detail
   wall_s differences explicitly, and do not attempt (or imply) a
   cross-environment audit-json byte pin.

## Status guarantees

Nothing is consumed: the four gate-verified WIN rows (b018 dual-class
batch-1, d002 batch-3, e002 batch-4, f017 batch-5) remain UNCONSUMED
labels eligible for the future adoption Part in the EP/ER/EU pattern.
The standard 11x11 empty board, all 19 central-reply roots, S2, class
1/2/4 and all closure classes remain UNKNOWN at all times. nodes are
bookkeeping, never verdicts. No win/loss, coverage or secured-coverage
claim is made or implied anywhere. This verification adds no new claim -
it raises the evidence level of the published Part EV gate run to
second-host reproduced (7/7 re-run node-exact, tamper fail-closed
byte-reproduced 3/3, audit determinism re-established).

## Resume notes (for the next run; re-fetch latest main first)

- Part EU has since CLOSED at its wave F (76835aa8): the canonical
  merged exact-S5 chain head formally advanced 9c4dd94e -> 3ba48608
  (6,767 rows WIN 188 / LOSS 6,579), verdict scope exactly the 2
  ET-gate-verified WIN rows ai007+ai040, with the disclosed
  SCEN_REFRESH_SHA repair (fork 6dc24c15, extractor 9bc5f06a) in the
  chain. Adoption of b018/d002/e002/f017 is therefore no longer blocked
  on EU; a future adoption Part (EP/ER/EU pattern: declare; re-derive
  from SSOT at the new head 3ba48608; merge with WIN/LOSS conflict
  check; census already taken: 16757->3 / 20421->6 / 16371->2 /
  12264->51) can be declared next.
- The b018 dual-class flip cross-check must be re-derived from SSOT in
  that adopting Part, not assumed from logs (b018 is the dual-class
  batch-1 row; same-condition re-probe ban applies).
- Second-environment verification candidates remaining in the chain: the
  Part EU close-out artifacts now fully published (wave-D refresh outputs
  2b70bb55/59a4c85f/cfc2bfe1 + decomp 8d4a5743, repaired extractor
  9bc5f06a, refresh fork 6dc24c15, merged head 3ba48608).
- 11x11 itself: UNKNOWN. No result of this Part speaks to the empty
  board's value; move-count and node-count statements are bookkeeping.
