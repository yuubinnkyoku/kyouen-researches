# Part EO close-out: second C++ second-implementation scrutiny gate executed - class 34908's 6 remaining unconsumed WIN rows independently re-derived, 9/9 GATE-PASS (2026-11-25)

Close-out of `research/experiments/n11-centralreply-closure-class34908-cppgate-20261125/`
(declaration: `research/log/2026-11-25-part-eo-cppgate-34908win6-declaration.md`).
Single-owner session. Pre-push HEAD at declaration time observed at `25aafd1a`
(K1330 official runs, disjoint z-slice lane); immediately before the kit push it
was `8a1062335e94c36c3055775a50ebc5eae66e7498` (no path overlap with this Part;
re-fetched and re-checked before this outputs push as well).

## 1. Outcome in one line

The scrutiny-owner C++ second implementation (`cpp/solvers/kyouen_dfpn_root.cpp`,
payload pin `9193f5b6...` = full sha256
`9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`,
resolved byte-exact to commit `154f3b7a67b97e13acbaee8b04dc74ddca728d19`)
was compiled in a fresh session environment (no fix chain: runner
machine-identical to Part EN rev2, audit adapted from EN rev4 with the
10-capture-group regex assert built in from the start) and executed for the
second time in this program, on closure class 34908's 6 remaining unconsumed
probe-level WIN rows plus the same 3 published-baseline anchors as Part EN.
All 9 rows reproduced their pinned published values node-exactly, 2-pass
deterministic, fail-closed.

**No verdict was consumed.** The 6 class-34908 WIN rows
{af029, af047, af050, af053, af023, af048} are now independently re-derivable
from the pinned source (on top of the Part EG third-implementation JS
agreement already on record), but their labels stay UNCONSUMED; adoption
remains a separate Part (pinned fail-closed union merger `90711961...` route,
Board re-verification, reaudit deltas). The standard 11x11 empty board
remains UNKNOWN; class 34908's "6 unconsumed WIN children" state is unchanged.

## 2. Execution summary (all 9 rows GATE-PASS)

Config per pass: `--n=11 --memo=22 --only=5 --exact-order=count
--exact-replay=input/<row>.input.csv --exact-replay-budget=<budget>`.
One process per pass, fresh-cold, single sequential worker; batch window
19:27:04Z-19:35:07Z, zero MISMATCH/GATE-FAIL/GATE-CRASH lines.

| row | key_lo | key_hi span | legal | budget | result | nodes (p1, p2 identical) | published source of the pin |
|---|---|---|---|---|---|---|---|
| af029 | 1152921504607895553 | 68720525312 | 86 | 15M | 1 | 4,862,485 | EG kit sources/b33-raw (15M); ea-raw 30M anchor row has identical nodes |
| af047 | 1152921504607895809 | 68719476736 | 84 | 15M | 1 | 9,841,975 | EG kit sources/b33-raw (15M) |
| af050 | 1152921504607899649 | 68719476736 | 94 | 15M | 1 | 7,311,834 | EG kit sources/b33-raw (15M) |
| af053 | 1152921504606852096 | 17660905521152 | 90 | 15M | 1 | 5,182,129 | EG kit sources/b33-raw (15M) |
| af023 | 1152921504607895553 | 68719478784 | 94 | 30M | 1 | 28,933,179 | EG kit sources/ea-raw (30M re-probe; b33 15M row was budget-ceiling EXHAUSTED, not pinned) |
| af048 | 1152921508902862849 | 68719476736 | 87 | 30M | 1 | 17,816,616 | EG kit sources/ea-raw (30M re-probe; b33 15M row was budget-ceiling EXHAUSTED, not pinned) |
| anchor-at2m | 1152921504606851072 | 536870946 | 98 | 2M | 0 | 2,000,000 | EN official-run baseline (EK at2m val-gate) |
| anchor-af039 | 1152921504607895681 | 68719476736 | 89 | 30M | 2 | 19,234,232 | EN official-run baseline (canonical cache row) |
| anchor-aj001 | 1152922604269469696 | 65536 | 84 | 30M | 2 | 5,156,075 | EN official-run baseline |

Result semantics as in Part EN: result 0/2 = budget ceiling; result 1 =
replay-path WIN outcome as pinned from the published raws; nodes are node
counts and never verdicts. Gate rows total nodes: 73,948,218 per pass
(147,896,436 both passes); anchors 26,390,307 per pass; batch total
200,677,050 expansions. Longest row: af023 (61s/62s per pass).

Raw files: `output/raw/<row>.{p1,p2}.out`; status: `output/gate-status.log`
(9 PASS lines). Extra reproduction observation: the anchor-at2m raws are
byte-identical to the EN published raws (sha256
`cfa72d667428bfc7b3cc60306be5828b859f2e50631bb89b37a8601d6bf02ee3`, all
passes, wall_s included) - the two sessions' binaries produce the same bytes
on that row; af029's own p1 and p2 are byte-identical to each other for the
same reason (wall_s 9s both passes). Anchor-af039/aj001 raws differ from EN's
only in the wall_s field.

## 3. Toolchain and reproducibility

- This session rebuilt from scratch (the EN session environment was gone):
  zig 0.13.0 re-downloaded from ziglang.org (47,082,308 B, sha256
  `d45312e61ebcc48032b77bc4cf7fd6915c11fa16e4aad116b66c9468211230ea`).
  First download attempt timed out at 15 MB; completed via a resume loop
  (11 attempts logged), then sha-verified.
- Build: `zig c++ -std=c++20 -O2` (125s); binary sha256
  `330ce0120904a080caabb2f445ffe57a26fffcf7ffee4f6dda266be0e8307745`
  (14.5 MB, not published). This differs from the EN session binary
  `d27acf47de52e781d9aa48c6567fcdbfe52ddcf8a5ddf15798d2b47a112192f1`
  (different host / glibc shim 2.39 fallback, same zig 0.13.0 and same
  pinned source). Disclosed in the declaration before execution: the binary
  is not the pin, the pinned source is; per-row determinism is enforced by
  the 2-pass fresh-cold protocol, not by a binary hash.
- Gate source header pins (unchanged from EN): `5976935dcfccb9b5a26fa68f8de
  20868ce45363dd8c372dcd67d9b841167e7f5` and `2e36d69481fafcde7aede8ae4fed
  3d5477f91ee9846bcd4ae2975f32a4ba1a5`; jsreplay provenance pin
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`.
- Current main's `cpp/solvers/kyouen_dfpn_root.cpp` (`a0786acb...`, 2026-10-22
  revision) remains a LATER revision than the gate pin, per jsreplay's
  header statement; recorded deliberately, as in EN.

## 4. Commit chain of this Part (all direct to main, no branch/PR)

1. `74ec7b17` - declaration + kit (README, declaration, runner, audit, 9
   input CSVs, all pins pre-verified; pre-push head `8a106233` re-fetched,
   no competition for "Part EO" or the experiment dir)
2. this commit - outputs (raws 18, status 9 PASS, audit 4x, tamper.log),
   README run record + honesty notes, `MANIFEST-sha256.txt`, this close-out

No fix-chain commits were needed: the EN lessons (runner CSV field indices,
wall_s exclusion index, G1 telemetry over-requirement, 10-group regex) were
all inherited structurally in the EO kit from the start.

## 5. Honesty notes (this Part)

- Zero GATE-FAIL/MISMATCH/CRASH lines and zero runner/audit revisions in the
  official run: unlike EN, no in-session fix chain occurred. The tamper
  battery was run immediately after the canonical audit and failed closed on
  all three injections (below), which is the evidence the audit is not
  vacuous - EN's critical lesson (a regex group-count bug made G2/G3 vacuous
  and the battery caught it) is structurally prevented here by the
  `assert REPLAY.groups == 10` line in the audit source.
- Every tampered file's sha256 was asserted changed BEFORE its audit run
  (EJ/EL lesson enforced from the start).
- Calibration (pre-declaration, scratch, not published): at2m
  EXHAUSTED-exact, af039 LOSS-exact, k04 WIN node-exact (1,9,433,024) - the
  anchors were then re-run fresh-cold under the runner in the official
  batch.
- The tamper battery ran on scratch copies at `/home/user/kr-lt/tamper`
  (ephemeral); its verbatim transcript is `output/tamper.log`, whose bytes
  are published and pinned in `MANIFEST-sha256.txt`.

## 6. Machine audit and tamper battery

- 46 gates (G5 input pins x9, G1 structure x18, G2 determinism x9, G3
  published pins x9, G4 accounting x1): rc=0, overall PASS. Run three extra
  times: all four `audit_gate*.json` byte-identical, sha256
  `b46f2130e9855204b5d3a12c07833083af1e96fc4dd9013893f6be7ed0bfa057`.
- Tamper battery (`output/tamper.log`):
  - T1 corrupt audit-source expected pin (af029 nodes 4862485 -> 4862486):
    FAIL `G3:af029`, rc=1
  - T2 tamper raw byte (af029.p1 nodes 4862485 -> 4862486): FAIL
    `G2:af029,G3:af029`, rc=1
  - T3 inject phantom GATE-FAIL into gate-status.log: FAIL `G4`, rc=1
  - CONTROL untouched copy: rc=0, audit byte-identical to canonical
  - verdict: 3/3 fail-closed, control clean.

## 7. UNKNOWN guard / next steps

- The standard 11x11 empty board: UNKNOWN. The 19 two-stone roots and every
  closure class: UNKNOWN. Class 34908 keeps its 6 unconsumed probe-level WIN
  children (now second-implementation-verified on top of the JS
  third-implementation agreement, but UNCONSUMED). Class 30484 also keeps its
  4 EN-verified WIN rows unconsumed. Nodes are not verdicts; probe-level WIN
  labels under a budget ceiling are not class verdicts.
- Next lane options, in value order:
  (a) adoption Part: consume the verified WIN rows via the pinned fail-closed
      union merger `90711961...` route (Board re-verification, reaudit
      deltas). Two candidates are now fully gate-verified: class 30484
      (4 rows, EN) and class 34908 (6 rows, EG + EO);
  (b) batch-41 on class 30345 (26 unknown rows remaining) - the next natural
      scrutiny batch;
  (c) parallel-lane record: the K1330 high-speed z-slice lane was in progress
      at declaration time (head `25aafd1a`); the af034 60M re-probe dir for
      class 34908 exists (`...-af034-reprobe60m-20261125`) and was not
      touched by this Part.
- Toolchain note: the zig build environment in this session is ephemeral;
  the kit is reproducible from source pins with any C++20 toolchain.
