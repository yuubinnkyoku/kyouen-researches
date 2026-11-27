# Part EO declaration: second execution of the scrutiny-owner C++ second-implementation gate (pin `9193f5b6...`) on the 6 remaining unconsumed probe-level WIN rows of closure class 34908 (+ the same 3 published-baseline anchors as Part EN) (2026-11-25)

Single-owner declaration, publish-then-execute. Claim check at composition:
code search "Part EO" across the repo = total_count 0 (this is the first Part EO
publication; also 0 hits for a 34908 cppgate experiment dir or declaration).
Parallel-lane head at composition observed at `25aafd1a` (K1330 official runs,
a disjoint high-speed z-slice lane); re-checked immediately before push.
This Part follows the Part EN close-out's own next-step list (option (b):
"gate the 6 WIN rows of class 34908 (af029/af047/af050/af053/af023/af048 per
the EG per-row provenance) - the natural next scrutiny batch").

## 1. What this Part is

The pre-registered adoption gate for every probe-level WIN row in the
central-reply closure program is the **C++ second implementation**
`cpp/solvers/kyouen_dfpn_root.cpp`, payload pin `9193f5b6...`. Part EN
executed it for the first time ever (class 30484, 2026-11-25, 8/8 GATE-PASS).
This Part executes the same pinned gate on closure class 34908's 6 remaining
unknown children {af029, af047, af050, af053, af023, af048} - each an
honest unconsumed probe-level WIN label per the Part EG kit `rows.json` and
per-row provenance - plus the 3 published-baseline anchors reused byte-exactly
from Part EN's kit (anchor-at2m, anchor-af039, anchor-aj001), whose published
budget-ceiling baselines were already independently reproduced by the EN run
of this same binary source. **This Part consumes no verdict**: adoption of any
WIN row stays a separate follow-up Part (pinned fail-closed union merger
`90711961...` route, Board re-verification, reaudit deltas). If any row
disagrees with its published raw, the runner hard-stops, raws are published,
and no interpretation is given (C5 rule).

## 2. Resolution of the gate pin (byte-exact, re-verified this session)

`9193f5b6...` resolves to the bytes of `cpp/solvers/kyouen_dfpn_root.cpp`
at commit **`154f3b7a67b97e13acbaee8b04dc74ddca728d19`** (2026-10-10T03:10:00Z).
This session fetched those bytes fixed-commit (raw CDN) and verified:

- `kyouen_dfpn_root.cpp`: 189,384 B, sha256
  `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e` (pin MATCH).
- `kyouen_residual_micro.hpp` (same commit): 13,089 B, sha256
  `5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5` (pin MATCH).
- `n11_s5_quarantine.hpp` (same commit): 478 B, sha256
  `2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5` (pin MATCH).
- jsreplay provenance pin (EG kit `scripts/jsreplay.js` fetched at `bb661fbb`):
  sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (pin MATCH); its header states the replicated configuration
  `--n=11 --memo=22 --only=5 --exact-order=count --exact-replay=<csv>
  --exact-replay-budget=<n>` against the 154f3b7a67 bytes.
- The current main copy of `kyouen_dfpn_root.cpp` (`a0786acb...`, 2026-10-22
  revision) remains a LATER revision; the delegated gate pin means the
  154f3b7a67 bytes (recorded identically in Part EN; policy unchanged).

## 3. Toolchain (honest environment record)

- This lane's execution environment was reset since Part EN: no C/C++
  compiler, no previous zig install. zig 0.13.0 re-downloaded from
  `https://ziglang.org/download/0.13.0/zig-linux-x86_64-0.13.0.tar.xz`
  (47,082,308 B, sha256
  `d45312e61ebcc48032b77bc4cf7fd6915c11fa16e4aad116b66c9468211230ea`, OK).
  First single-shot download attempt timed out at 15 MB (slow host network);
  completed via a resume loop (11 attempts logged), then sha-verified.
- Compile: `zig c++ -std=c++20 -O2 -o kyouen_dfpn_root kyouen_dfpn_root.cpp`
  (125s wall); emits `warning: zig cannot build new glibc version 2.41.0;
  providing instead 2.39.0` (same warning as Part EN's build).
- Binary sha256
  `330ce0120904a080caabb2f445ffe57a26fffcf7ffee4f6dda266be0e8307745`
  (14.5 MB). This DIFFERS from Part EN's session binary
  `d27acf47de52e781d9aa48c6567fcdbfe52ddcf8a5ddf15798d2b47a112192f1`:
  both were built from the same pinned source with zig 0.13.0 on different
  hosts/ABI shims. The binary is deliberately NOT pinned - the pinned source
  is the second implementation under test, and per-row binary determinism is
  enforced by the 2-pass fresh-cold protocol, not by a binary hash.
- The compiler is clang-based, not g++: disclosed for the same reason as EN.

## 4. Calibration (pre-declaration pilots, this session, honest)

- C-a (EXHAUSTED node-exact): val-gate row `anchor-at2m` @2,000,000 ->
  `replay,0,5,98,0,2000000,0,2000000,...` matches the published baseline
  exactly (nodes == budget).
- C-b (decisive LOSS node-exact): `anchor-af039` @30,000,000 -> result 2,
  nodes **19,234,232**, equal to the published EK raw and the canonical cache
  row (40.6s wall).
- C-c (decisive WIN node-exact, pre-declaration this time): EN kit
  `input/k04.input.csv` (byte-clone, sha256 pin re-verified
  `110776a29b4a9ce4fa0b61c47fc2a586e3475bdd94328db77b506ae8456a80a4`) @15M ->
  result 1, nodes **9,433,024**, equal to the pre-registered sixth-cost
  expectation and the EN official-run reproduction (19.9s wall).

All three calibration outputs are retained in this session's scratch (not
published: they are pilots; the official batch re-runs the pinned anchors
fresh-cold under the runner).

## 5. Official batch rows (budget/result/nodes pinned from published source raws, SSOT)

| key | input (lo, hi, legal) | budget | expected (result, nodes) | raw provenance |
|---|---|---|---|---|
| af029 | 1152921504607895553, 68720525312, 86 | 15,000,000 | (1, 4,862,485) | EG kit sources/b33-raw/af029.p1.out |
| af047 | 1152921504607895809, 68719476736, 84 | 15,000,000 | (1, 9,841,975) | EG kit sources/b33-raw/af047.p1.out |
| af050 | 1152921504607899649, 68719476736, 94 | 15,000,000 | (1, 7,311,834) | EG kit sources/b33-raw/af050.p1.out |
| af053 | 1152921504606852096, 17660905521152, 90 | 15,000,000 | (1, 5,182,129) | EG kit sources/b33-raw/af053.p1.out |
| af023 | 1152921504607895553, 68719478784, 94 | 30,000,000 | (1, 28,933,179) | EG kit sources/ea-raw/af023.p1.out |
| af048 | 1152921508902862849, 68719476736, 87 | 30,000,000 | (1, 17,816,616) | EG kit sources/ea-raw/af048.p1.out |
| anchor-at2m | 1152921504606851072, 536870946, 98 | 2,000,000 | (0, 2,000,000) | EN kit budget-ceiling baseline |
| anchor-af039 | 1152921504607895681, 68719476736, 89 | 30,000,000 | (2, 19,234,232) | EN kit budget-ceiling baseline |
| anchor-aj001 | 1152922604269469696, 65536, 84 | 30,000,000 | (2, 5,156,075) | EN kit budget-ceiling baseline |

Every source raw above was fetched fixed-commit this session (EG kit at
`bb661fbb`, EN kit at `949e68a7`) and its `replay,` row compared field-wise
against the pin before this declaration was composed: all 9 match (and the
published ea-raw af029 30M anchor row additionally shows nodes 4,862,485 at
the higher budget - a budget-independence observation recorded as such, not
re-run here). The b33 15M raws for af023/af048 are EXHAUSTED (budget-ceiling)
rows and are deliberately NOT pinned: their published WIN labels come from the
30M re-probes.

Every input csv in this kit is a byte-clone of the published kit input
(six WIN rows: EG kit `input/` at `bb661fbb`, git-blob-verified; three
anchors: EN kit `input/` at `949e68a7`, sha256-verified against the EN audit
G5 pins). sha256 pins for all nine are recorded in `scripts/audit_gate.py` (G5).

## 6. Protocol (fail-closed)

Per row: 2 fresh-cold passes, one process per pass, sequential single worker
(modest-CPU lane rule), `scripts/gate_runner.sh` compares
(legal, budget, result, nodes) between passes and against the pinned
expectation; determinism mismatch or published-row disagreement -> HARD-STOP
(C5: publish raws, no interpretation, hand divergence to the research
community; no adoption anywhere). After the batch: `scripts/audit_gate.py`
gates G1 (structure/terminal lines), G2 (p1==p2 all fields except wall_s),
G3 (published-raw node-exactness), G4 (status accounting), G5 (input sha pins),
run canonically plus 3 times, all `audit_gate*.json` byte-identical; a tamper
battery on scratch copies (T1 corrupt an expected pin in the audit source,
T2 corrupt a raw byte, T3 inject a phantom GATE-FAIL into the status log ->
each must produce rc=1 with the named FAIL gate, with the tampered file's
sha256 pre-asserted to have changed (EJ/EL lesson), and a clean control copy
must reproduce the canonical audit byte-identically).

## 7. Assertions and guards

- **No verdict is consumed.** All six 34908 rows keep their unconsumed
  probe-level WIN labels even on GATE-PASS; adoption is a separate Part
  (merger `90711961...` route, Board re-verification, reaudit deltas). The
  class 34908 closure state ("6 unconsumed WIN children") changes only via
  that future adoption Part, not here.
- The 19 central-reply roots, the two-stone roots {49,60}/{59,60}, S2
  {59,60}, and closure classes 1/2/4, 30484 (still unknown 4, EN rows
  unconsumed), 30118, 30345, 20421, 16371 all remain untouched.
- Nodes/expansions are never verdicts; wall times are runlimit artifacts and
  match nothing; the Part EG third-implementation (JS) agreement already on
  record is a separate cross-check, not replaced by this Part.
- **The standard 11x11 empty board remains UNKNOWN throughout.** A GATE-PASS
  is a second-implementation reproduction of a published probe row, not a
  win/loss claim about the 11x11 empty board.
- Experiment dir:
  `research/experiments/n11-centralreply-closure-class34908-cppgate-20261125/`.
  Outputs and the close-out log are published after execution with
  fixed-commit fetch-back byte verification of every published file.
