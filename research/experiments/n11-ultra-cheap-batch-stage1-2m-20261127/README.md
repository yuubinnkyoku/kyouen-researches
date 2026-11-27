# n11 ultra-cheap batch stage-1 sweep (2M cold pairs + 15M WIN-stopped escalation)

Execution kit of the ultra-cheap batch declared in
`research/log/2026-11-27-n11-ultra-cheap-batch-declaration.md`, covering
the four one-unknown class-completion S5 keys published by the
ultra-cheap census (`a60716ac...`) with dual-implementation legal
pre-check (`89fd85ac...`), under canonical head of record `1e2eeda2...`
(6,890 rows WIN 208 / LOSS 6,682).

Probe order u01 (1849, legal 88), u02 (2251, legal 80), u03 (16371,
legal 78), u04 (23101, legal 85).  Status at publication of this README:
**DECLARED, execution in progress** (stage-1 2M cold pairs, then 15M
WIN-stopped escalation in declared order).  Results, raws, batch summary
and MANIFEST will be published in follow-up commits to this kit.

## Files (wave A: declaration scaffold)

- scripts/jsreplay.js - byte-clone of the published pin `84585617...`,
  unchanged (sha256 verified locally at assembly; published in wave B).
- input/u01..u04.input.csv - the four probe input rows
  (target,0,5,lo,hi,legal,0,0,0,0,0), legal from the dual-implementation
  pre-check kit, fail-closed against the runner's Board-derived legal
  count.

## Meaning and non-meaning

Scheduling/batch bookkeeping only: NO verdict is claimed or implied.
Nodes are bookkeeping, never evidence of WIN or LOSS.  The standard
11x11 empty board, the two-stone root {60,27} and its remaining third
moves 100/108 stay UNKNOWN.
