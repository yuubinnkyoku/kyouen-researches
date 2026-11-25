# Part EN declaration: first-ever execution of the scrutiny-owner C++ second-implementation gate (pin `9193f5b6...`) on the 4 remaining unconsumed probe-level WIN rows of closure class 30484 (+ pre-registered anchors) (2026-11-25)

Single-owner declaration, publish-then-execute. Claim check at composition:
code search "Part EN" / "part-en" across research/log = total_count 0 (this is the first
Part EN publication). Parallel-lane head at composition time observed at
`680894b7` then re-checked immediately before push (see close-out log for the exact
pre-push HEAD; the Part EJ takeover at `90c75f9f` is a disjoint class-30118 lane).

## 1. What this Part is

The pre-registered adoption gate for every probe-level WIN row in the
central-reply closure program is the **C++ second implementation**
`cpp/solvers/kyouen_dfpn_root.cpp`, payload pin `9193f5b6...`, delegated to the
scrutiny owner and never executed because no executing lane had a working C++
toolchain. This session provides that toolchain for the first time and runs the
gate under fail-closed conditions. **This Part consumes no verdict**: adoption
of any WIN row stays a separate follow-up Part (pinned fail-closed union merger
`90711961...` route). If any row disagrees with its published raw, the runner
hard-stops, raws are published, and no interpretation is given (C5 rule).

Scope: closure class 30484's 4 remaining unknown children {aj030, ai048, aj049,
aj050} - each an unconsumed probe-level WIN label - plus the sixth-cost k04 row
whose delegated gate spec was pre-registered in
`research/log/2026-11-22-n11-sixthcost-k01-k03-thirdimpl-verdict-single-owner-note.md`
(expected result 1, nodes 9,433,024 at 15M), plus 3 published-baseline anchors.

## 2. Resolution of the gate pin (byte-exact)

`9193f5b6...` resolves to the bytes of `cpp/solvers/kyouen_dfpn_root.cpp`
at commit **`154f3b7a67b97e13acbaee8b04dc74ddca728d19`** (2026-10-10T03:10:00Z,
"n11: independently audit exact evidence and harden propagation trust"):

- full sha256 of the raw-CDN bytes fetched at that commit:
  `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e` (pin MATCH).
- provenance: `scripts/jsreplay.js` (published kit byte, sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`) states in its
  header that it replicates the STANDALONE EXACT REPLAY path of
  `cpp/solvers/kyouen_dfpn_root.cpp at commit 154f3b7a67 (file SHA-256
  9193f5b606...)` under the configuration `--n=11 --memo=22 --only=5
  --exact-order=count --exact-replay=<csv> --exact-replay-budget=<n>`.
- headers compiled alongside (both fetched at the same commit):
  `kyouen_residual_micro.hpp` sha256
  `5976935dcfccb9b5a26fa68f8de20868ce45363dd8c372dcd67d9b841167e7f5`,
  `n11_s5_quarantine.hpp` sha256
  `2e36d69481fafcde7aede8ae4fedf3d5477f91ee9846bcd4ae2975f32a4ba1a5`.
- note (pre-existing observation, recorded here because it matters for anyone
  rebuilding the gate): the current main copy of `kyouen_dfpn_root.cpp`
  (`a0786acb...`, last changed 2026-10-22) is a LATER revision of the file; the
  delegated gate pin has always meant the 154f3b7a67 bytes, which remain
  permanently fetchable (e.g. raw CDN at that commit) - this Part pins them.

## 3. Toolchain (honest environment record)

- Host: 2-core x86_64 sandbox, Python 3.12.14, Node available, **no system C/C++
  compiler**; `pip install` refused by the sandbox ("package installation is
  forbidden").
- Attempt 1 (failed, recorded): musl.cc `x86_64-linux-musl-cross.tgz` (115,063,639 B,
  sha256 `c5d410d9f82a4f24c549fe5d24f988f85b2679b452413a9f7e5f7b956f2fe7ea`)
  ships i386 binaries; this host's kernel refuses them ("Exec format error").
- Toolchain used: **zig 0.13.0** from
  `https://ziglang.org/download/0.13.0/zig-linux-x86_64-0.13.0.tar.xz`
  (47,082,308 B, sha256
  `d45312e61ebcc48032b77bc4cf7fd6915c11fa16e4aad116b66c9468211230ea`),
  compile command `zig c++ -std=c++20 -O2 -o kyouen_dfpn_root kyouen_dfpn_root.cpp`
  (46.6s); compile emits `warning: zig cannot build new glibc version 2.41.0;
  providing instead 2.39.0`; binary sha256
  `d27acf47de52e781d9aa48c6567fcdbfe52ddcf8a5ddf15798d2b47a112192f1`.
- The compiler is clang-based, not g++: the pinned SOURCE is the second
  implementation under test; the compiler is tooling and is disclosed here rather
  than hidden. Determinism of the compiled binary itself is checked by the
  two-pass protocol on every row.

## 4. Calibration (pre-declaration pilots, this same session, honest)

- C-a (EXHAUSTED node-exact): val-gate row `at2m` lo `1152921504606851072` hi
  `536870946` legal 98 @2,000,000 -> `replay,0,5,98,0,2000000,0,2000000,...`
  matches the published EK-kit baseline exactly (nodes == budget).
- C-b (decisive LOSS node-exact): `af039` lo `1152921504607895681` hi
  `68719476736` legal 89 @30,000,000 -> result 2, nodes **19,234,232**, equal to
  the published EK raw and the canonical cache row (43s wall).
- WIN-decisive calibration is `k04` in the official batch (pre-registered
  expectation (1, 9,433,024) @15M, per the k01/k03/k04 delegated-gate notes).

## 5. Official batch rows (budget/result/nodes pinned from published raws, SSOT)

| key | input (lo, hi, legal) | budget | expected (result, nodes) | raw provenance |
|---|---|---|---|---|
| aj030 | 1152922604135251976, 65536, 83 | 30,000,000 | (1, 15,284,699) | EK kit output/raw/aj030.p1.out |
| aj049 | 1152921574400065536, 1114112, 80 | 30,000,000 | (1, 4,998,452) | EK kit output/raw/aj049.p1.out (b39 @15M raw has the same decisive nodes) |
| aj050 | 1152921574400065536, 68157440, 80 | 15,000,000 | (1, 1,871,594) | b39 kit output/raw/aj050.p1.out |
| ai048 | 1152921573327372288, 68157440, 68 | 15,000,000 | (1, 2,232,854) | b38 kit output/raw/ai048.p1.out |
| k04 | 10376293541461626888, 65536, 83 | 15,000,000 | (1, 9,433,024) | sixthcost kit out/k04-replica-raws/at15m-run1-k04.out.csv |
| anchor-at2m | 1152921504606851072, 536870946, 98 | 2,000,000 | (0, 2,000,000) | EK kit val-gate published baseline |
| anchor-af039 | 1152921504607895681, 68719476736, 89 | 30,000,000 | (2, 19,234,232) | EK kit raw + canonical cache row |
| anchor-aj001 | 1152922604269469696, 65536, 84 | 30,000,000 | (2, 5,156,075) | EK kit output/raw/aj001.p1.out |

Every input csv in this kit is a byte-clone of the published kit input; sha256
pins recorded in `scripts/audit_gate.py` (G5) were cross-verified against the
source-kit MANIFEST-sha256.txt entries at main `680894b7` before this
declaration was composed.

## 6. Protocol (fail-closed)

Per row: 2 fresh-cold passes, one process per pass, sequential single worker
(modest-CPU lane rule), `scripts/gate_runner.sh` compares
(legal, budget, result, nodes) between passes and against the pinned expectation;
determinism mismatch or published-row disagreement -> HARD-STOP (C5: publish
raws, no interpretation, hand divergence to the research community; no adoption
anywhere). After the batch: `scripts/audit_gate.py` gates
G1 (structure/terminal lines), G2 (p1==p2 all fields except wall_s),
G3 (published-raw node-exactness), G4 (status accounting), G5 (input sha pins),
run 3x byte-identical; a tamper battery on scratch copies (corrupt an expected
pin; corrupt a raw byte; corrupt a status line -> audit must go rc=1 each time,
restored copy must PASS).

## 7. Assertions and guards

- **No verdict is consumed.** All four 30484 rows keep their unconsumed
  probe-level WIN labels even on GATE-PASS; adoption is a separate Part
  (merger `90711961...` route, Board re-verification, reaudit deltas). The
  class 30484 closure state ("unknown 4") changes only via that future adoption
  Part, not here.
- k04 (and the sixth-cost rows generally) remain unconsumed WIN labels; this
  Part only completes their delegated gate check.
- Nodes/expansions are never verdicts; wall times are runlimit artifacts and
  match nothing.
- **The standard 11x11 empty board, the 19 central-reply roots, the two-stone
  roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4, 30484, 34908, 20421,
  16371, 30118, 30345 all remain UNKNOWN throughout.** A GATE-PASS is a
  second-implementation reproduction of a published probe row, not a win/loss
  claim about the 11x11 empty board.
- Experiment dir: `research/experiments/n11-centralreply-closure-class30484-cppgate-20261125/`.
  Outputs and the close-out log are published after execution with fixed-commit
  fetch-back byte verification of every published file.
