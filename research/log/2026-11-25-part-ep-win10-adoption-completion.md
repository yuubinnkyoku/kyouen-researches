# Part EP completion log: epwin10 FIRST-EVER WIN canonical adoption (2026-11-25)

Close-out of Part EP.  Every computational phase of this Part completed
before publication and is recorded in the kit README; this log records the
publication waves and the same-session fetch-back verification.

## What Part EP did

First WIN-row canonical adoption in the central-reply chain: 10
scrutinized probe-level WIN rows (class 34908: af029/af047/af050/af053/
af023/af048; class 30484: aj030/aj049/aj050/ai048; adopted node total
98,335,817) consumed into the canonical exact-S5 chain, on top of the Part
EM head b5be64e6... (6,737 rows) producing fd29a337... (6,747 rows, WIN 168
/ LOSS 6,579).  Closure classes 30484/34908 became fully known
(cost-unknown 4 -> 0 and 6 -> 0) and flipped to excluded_now - scheduling
bookkeeping only.  Exactly 20 classes flipped UNKNOWN -> excluded_now
(exactly those whose s4_cost contains an adopted key); census unknown
34,497 -> 34,477, excluded_now 23 -> 43, free_now 39 static, excluded 390
static.  Honest tradeoff recorded: joint greedy remaining union
36,460 -> 36,643 (+183) while the probe worklist shrinks by 11.

## Run record (2026-11-25, before publication)

maker 0.5 s PASS (G0-G6, 9 dependency kits verified file-by-file against
their MANIFESTs at commit pin 28822eb0..., every per-row sha
MANIFEST-extracted, none hand-typed); merger selftest PASS + 3/3
byte-identical merge runs (audits sha efbe25bc... x3); reaudit refresh
61 s PASS; extractor 122 s PASS incl. the byte-verbatim scratch
re-execution of BOTH refresh forks (EM and EP) with all eight outputs
byte-identical.  This session recovered the entire workspace by
commit-pinned re-fetch after an environment reset (no non-reproducible
local state was load-bearing; the published kit now reproduces everything
by construction).

## Publication waves (all landed on main)

* A 2d8d24a7  declaration log (this Part's log file, 70b7d65d...)
* B de22fcc8  kit scripts 3: maker efc40a0b..., merger 90711961...,
  extractor e28a6893...
* C 2af4d26c  outputs 6: increment c245bc4c..., increments-manifest
  25d3abdf..., merged cache fd29a337..., merge-audit-run1/2/3.json
  (efbe25bc... x3)
* D c83c32e2  reaudit + deltas 5: refresh fork 99d583c3...,
  refresh-summary 5a1ff0c5..., closure-classes fdd4e4b2...,
  per-root-coverage 487a95c4..., decomp-deltas ce7974c4...
  (probe-worklist.csv 3,718,981 B NOT published: size policy, regen pin
  7cd566bf... recorded in the kit MANIFEST)
* E 7d6cb5bd  kit close-out: README.md c8c64ddb...,
  MANIFEST-sha256.txt 5a429ae0... (14 published files byte-pinned;
  README/MANIFEST self-excluded per convention)
* F this commit  completion log

Each wave was preceded by a fresh main head fetch; push conflicts and
parallel-lane history were checked each time (none affected these paths).

## Fetch-back verification (same session)

Every published file was re-fetched by commit sha from
raw.githubusercontent.com and byte-compared (sha256) against the local
push payload: A 1/1, B 3/3, C 6/6, D 5/5, E 2/2 - 17/17 byte-identical
PASS at their wave heads.  The wave commits above pin the exact bytes
forever.

## Guarantees

No verdict consumed beyond the 10 adopted WIN rows.  Consuming a WIN
label transfers NO verdict to any of the 19 central-reply roots: the
adoption is chain bookkeeping, class-status bookkeeping, and scheduling
bookkeeping only.  The standard 11x11 empty board stays UNKNOWN.  nodes
are bookkeeping, never verdicts.  No free/secured coverage or root
resolution is claimed anywhere in this Part.
