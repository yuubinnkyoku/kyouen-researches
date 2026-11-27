# Part ES declaration: class 30345 exhausted-6 re-probe at the 30M condition (2026-11-25)

Publish-then-execute declaration for the Part ES lane, published before any
target machine run.  Single-owner lane: the Part ER second-environment
verification lane of 2026-11-25 continues here (as this same run session).
Kit, outputs and close-out will follow in the waves named below; a
completion log closes the Part.

## What this Part is

The canonical chain head is the Part ER head `9c4dd94e...` (6,765 rows, WIN
186 / LOSS 6,579, third-host-reproducible, verified this session at commit
`bc70b536`).  Closure class 30345 (mask [1152922604118478848, 65536]) now
holds exactly 7 unknown members: the 6 batch-38 honest-EXHAUSTED keys at
the 15M condition (ai007/ai024/ai030/ai038/ai040/ai041) plus the batch-1
dual-class key b018.  This Part re-probes exactly the 6 EXHAUSTED keys at
a DIFFERENT condition - budget 30,000,000 - the route pre-declared in the
Part ER close-out ("30M+ different-condition probe or a third
implementation"), so the same-condition re-probe ban is untouched: no 15M
re-probe of any completed exhaustion row happens anywhere in this Part.

## Targets (machine-extracted from the batch-38 SSOT, never hand-typed)

All six are serving_class 30345, fresh to the canonical head `9c4dd94e`
(absent, verified machine-side), absent from the quarantine registry
`81d23160`.  b018 stays excluded (dual-class, scrutiny-owner pending,
same-condition re-probe prohibited - untouched by this Part).

| key_id | probe_order | s5_index | lo | hi | legal | 15M label |
|---|---|---|---|---|---|---|
| ai007 | 138 | 441292 | 1152922604118478880 | 65536 | 84 | EXHAUSTED |
| ai024 | 156 | 889534 | 1152922604118479104 | 65536 | 86 | EXHAUSTED |
| ai030 | 162 | 894456 | 1152921573327372288 | 17825792 | 91 | EXHAUSTED |
| ai038 | 170 | 898436 | 1152927002164989952 | 65536 | 89 | EXHAUSTED |
| ai040 | 172 | 899584 | 1152922604118487040 | 65536 | 85 | EXHAUSTED |
| ai041 | 173 | 900170 | 1152921573327372288 | 34603008 | 91 | EXHAUSTED |

`input/targets-30m.json` (sha256 `1c27a238...`) is the machine-extracted
target table from the published batch-38 SSOT
`input/batch-keys-b38.json` (`29807104...` of the Part EF kit).

## Condition and stop rules (pre-registered)

* Envelope (identical to the published batch-38 drive): jsreplay.js
  (byte-clone `84585617...`, the Node replica of the C++
  kyouen_dfpn_root.cpp exact-replay path, source pin `9193f5b6...` at
  commit 154f3b7a), `--exact-replay=<single-row csv>
  --exact-replay-budget=30000000` fresh-cold per pass, order=count-asc,
  n=11 memo=22 only=5, fresh solver per row, empty 2^22 PnTT, PROBE=32.
* Runner: `runbatch30m.sh`, disclosed fork of the pinned batch-38
  `runbatch.sh` (`f591f8c2...`): BUDGET 15M -> 30M (diff 1), WIN-HALT
  removed -> WIN-CONTINUE (diff 2; all 6 keys are probed regardless, WIN
  rows logged).  Everything else byte-equivalent: two-pass fresh-cold,
  truncated-pass replay_done guard, MISMATCH determinism hard-stop rc=42,
  P1/P2 fail rc=43/44, honest EXHAUSTED label.
* An EXHAUSTED@30M outcome is again an honest UNKNOWN at this new
  condition (no 30M re-probe thereafter; next steps would be a 60M+
  different condition or a third implementation).  A WIN outcome is an
  UNCONSUMED probe-level WIN: canonical adoption is the scrutiny-owner
  C++ second-implementation gate's exclusive right and is out of this
  Part's scope.  A LOSS outcome is Part-EM loss-only adoption territory,
  equally unconsumed here.
* Val-gate before any target drive: the four published batch-38 val-gate
  molecules byte-cloned into `val-gate/` (two at-2M exhaustion molecules,
  two 15M molecules resolving LOSS at 3,651,923 / 5,040,200 nodes) run
  fresh in this environment; each replay row must equal its published
  baseline byte-for-byte except the wall_s field.  A val-gate failure
  aborts the Part before any target key runs.
* Environment honesty: this environment measured ~213K nodes/s on the
  at-2M molecule (2,000,000 nodes in 9.4 s), so a 30M-budget pass worst
  case is ~140 s; passes are run in foreground split calls, at most 2
  keys in parallel (modest-CPU rule); truncated partial passes are never
  evidence and are re-run fresh-cold by the pinned guard.

## Publication waves (planned)

* A this declaration log
* B kit: scripts (jsreplay.js byte-clone, runbatch30m.sh), input
  (6 byte-cloned target CSVs + targets-30m.json), val-gate (8 byte-clones)
* C outputs: val-gate run raws + 12 target pass raws + status.log
* D close-out: README + MANIFEST-sha256
* E completion log

## Guarantees

Nothing in this Part consumes any verdict: the standard 11x11 empty
board stays UNKNOWN, all 19 central-reply roots stay UNKNOWN, class
scheduling and the canonical chain head `9c4dd94e...` are untouched
(no adoption, no refresh, no merger run in this Part).  Probe-level
honest labels (WIN/LOSS/EXHAUSTED) are recorded as raws only.  nodes are
bookkeeping, never verdicts.  No coverage or secured-coverage claim is
made anywhere in this Part.
