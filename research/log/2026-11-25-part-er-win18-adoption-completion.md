# Part ER completion log: erwin18 second WIN canonical adoption (2026-11-25)

Close-out of Part ER.  Every computational phase of this Part completed
before publication and is recorded in the kit README; this log records
the publication waves and the same-session fetch-back verification.

## What Part ER did

Second WIN-row canonical adoption in the central-reply chain, the largest
so far: all 18 still-unconsumed scrutinized batch-38 WIN rows of closure
class 30345 (ai002/ai003/ai005/ai006/ai010/ai013/ai014/ai017/ai023/ai028/
ai034/ai035/ai036/ai039/ai043/ai046/ai047/ai049; adopted node total
136,604,338 - the Part EQ declaration prose mis-sum 136,539,338 is
disclosed in the manifest, per-row data is SSOT) consumed into the
canonical exact-S5 chain, on top of the Part EP head fd29a337... (6,747
rows WIN 168 / LOSS 6,579) producing 9c4dd94e... (6,765 rows, WIN 186 /
LOSS 6,579).  Exactly 41 classes flipped UNKNOWN -> excluded_now (exactly
the adopted-key owner classes that were still unknown; the three further
owners 29979/30345/30542 were already excluded_now at Part EP and did not
double-flip).  Class 30345 cost-unknown dropped 25 -> 7 (stays
excluded_now since the EP ai048 flip); class 30118 flipped (unknown 51 ->
50, member ai034); class 30354 untouched (96 -> 96, no adopted member).
Census unknown 34,477 -> 34,436, excluded_now 43 -> 84, free_now 39
static, excluded 390 static.  Honest tradeoff recorded: the joint greedy
remaining union shrinks 36,643 -> 36,619 (-24) and the probe worklist
64,328 -> 64,309 (-19): scheduling bookkeeping only.

## Run record (2026-11-25, before publication)

maker PASS (rows=18, nodes=136,604,338; every pin extracted from the
byte-verified published EQ/b38 kit MANIFESTs and the b38 SSOT batch-keys,
none hand-typed); merger selftest PASS + 3/3 byte-identical merge runs
(audits sha d55f578f... x3); ER refresh executed in-session with outputs
byte-pinned; extractor 125 s PASS incl. the byte-verbatim scratch
re-execution of BOTH refresh forks (published EP 99d583c3... and ER
6c91e0ce...) with all eight outputs byte-identical, then a second full
extractor run whose decomp output was byte-identical (cd11b1a5... both
times); tamper T-ER1 fail-closed confirmed (increments-manifest.json +1
byte -> immediate ABORT manifest sha drift, file restored byte-exactly).
One honest environment note: the extractor's first internal ordering was
killed by the OOM watcher while a subprocess refresh re-execution
co-resident the frozen dependency graph with the parent copy; the
restructure runs both refresh re-executions BEFORE the single parent graph
load - no verification guarantee changed.

## Publication waves (all landed on main)

* A a4a6cd46  declaration log (this Part's log file, a258783a...)
* B e13588f6  kit scripts 3: maker 39f6c86a..., merger 90711961...,
  extractor c3e82ea...
* C 06119a79  outputs 6: increment 4f6b7797..., increments-manifest
  48b71d6a..., merged cache 9c4dd94e..., merge-audit-run1/2/3.json
  (d55f578f... x3)
* D a0a9063d  reaudit + deltas 5: refresh fork 6c91e0ce...,
  refresh-summary a6b8d082..., closure-classes 4c03f965...,
  per-root-coverage 1bf6c25a..., decomp-deltas cd11b1a5...
  (probe-worklist.csv 3,717,828 B NOT published: size policy, regen pin
  78e499dd... recorded in the kit MANIFEST)
* E 28b66333  kit close-out: README.md 8223f791...,
  MANIFEST-sha256.txt 46eef302... (14 published files byte-pinned;
  README/MANIFEST self-excluded per convention)
* F this commit  completion log

Each wave was preceded by a fresh main head fetch; push conflicts and
parallel-lane history were checked each time (a parallel-lane commit
857976ec landed between waves D and E and did not touch any Part ER path).

## Fetch-back verification (same session)

Every published file was re-fetched by commit sha from
raw.githubusercontent.com and byte-compared (sha256) against the local
push payload: A 1/1, B 3/3, C 6/6, D 5/5, E 2/2 - 17/17 byte-identical
PASS at their wave heads.  The wave commits above pin the exact bytes
forever.

## Guarantees

No verdict consumed beyond the 18 adopted WIN rows.  Consuming a WIN
label transfers NO verdict to any central-reply root: the adoption is
chain bookkeeping, class-status bookkeeping, and scheduling bookkeeping
only.  The standard 11x11 empty board stays UNKNOWN.  nodes are
bookkeeping, never verdicts.  No free/secured coverage or root
resolution is claimed anywhere in this Part.
