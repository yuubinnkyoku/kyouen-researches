# 2026-11-14 n11 class4-batch3 child#5 sweep (session 19, continued)

Next cheapest remaining S6 child of the class-4 lane target
S5 `00000000020000003800000080000000` after child#4 (cost 69).

## Target

- S6 child `00000000020000003800000080001000` (cost 72, demand c1=0,c2=0,c4=3)
- 72 non-degenerate 7th-stone candidates, ordered by root mobility ascending
  (mob 42..69).

## Sweep result (v15 engine verbatim, native Node)

- **68 candidates REFUTED-D10, 4 candidates WIN7-D10 (bits 108/95/99/17), 0 capped.**
- WIN7 roots (lossAt(root,10)=true, node-exact over 3 independent runs each):
  - bit 108: `00001000020000003800000080001000` (1,759,232 nodes, root mobility 42)
  - bit 95: `00000000820000003800000080001000` (2,515,780 nodes, root mobility 49)
  - bit 99: `00000008020000003800000080001000` (10,291,560 nodes, root mobility 56)
  - bit 17: `00000000020000003800000080021000` (8,703,066 nodes, root mobility 59)
- Total 256,648,013 nodes over 72 candidates in 4 foreground executions
  (cap 50M/candidate never reached).
- Pilot control PASS: lossAt(6)=false at exactly 5,949 nodes (published v15 reference).
- Determinism controls: WIN bits {108,95,99,17} node-exact over 3 independent runs;
  fresh re-solves of REFUTED bits {42,76} node-exact; terminal stone range [13,17]
  on every uncapped candidate.

## WIN7 certificates (15th-18th verified overall)

| bit | rows | bytes | md5 | sub-roots PASS | union |
|-----|------|-------|-----|----------------|-------|
| 108 | 16,700 | 602,670 | a47ba09a33ad4b7daa864b3e651cbdd2 | 42/42 | exact (0/0) |
| 95  | 24,611 | 887,995 | 0ea8d9fb7ec0f08df207a2331f21595b | 49/49 | exact (0/0) |
| 99  | 50,090 | 1,807,564 | ce42f1e4325daad9cae850a73e831d0c | 56/56 | exact (0/0) |
| 17  | 46,051 | 1,663,689 | 15d65d744c13a023ecfe60e773900bb1 | 59/59 | exact (0/0) |

Extraction (kill-first, single process, all root first-moves): 3,698,502 /
4,890,657 / 18,891,995 / 15,526,528 nodes, terminals [13,17] each.
Independent verification (verify_five_terminal_loss7.py TS port, exact Bareiss,
no engine import): all sub-roots PASS, consumed winner-state union = full row
set exactly (missing 0 / extra 0), root checks PASS (7 stones, no 4-cocircular
subset, loser mobility 42/49/56/59).

- Certificates: `output/class4-batch3-certificates/n11_s7_<roothex>.cert` (4 files).
- Records: `output/class4-batch3-child5-sweep.json`,
  `output/class4-batch3-win7-certificates-child5-20261114.json`.

## Frontier effect (conservative)

Each root's drop-one S6 parents include the swept child itself (cost 72), so at
minimum one remaining orbit of the class-4 lane target is closed:
**remaining 28 -> at most 27 S6 orbits, cost 2241 -> at most 2169.**
The exact additional coverage of the other drop-one S6 parents (canonical-orbit
comparison against the remaining-children manifest) is deferred to the
manifest-level frontier recompute — recorded conservatively to avoid the
child#4 double-coverage arithmetic error (see the corrected child#4 section of
`2026-11-14-n11-class4-child3-sweep.md`).

## Operational notes

- `tools.file_system.read_file` caps a single call at ~64KB: the first bit108
  certificate push landed truncated and was immediately re-pushed complete
  (paged reassembly, byte-exact 602,670; post-push additions/deletions verified
  via get_commit). Large-file pushes must always page reads inside the sandbox.
- Two pushes (bit99, bit17) hit the 16 MiB sandbox memory limit *after* the
  push call executed; both landed complete (get_commit additions 50,092 /
  46,053 lines). Landing must be confirmed after such errors.

## Status

WIN7 certificates prove only a win within depth 10 from their 7-stone root;
REFUTED-D10 entries negate only WIN7-within-depth-10. class 4, S2 {59,60},
two-stone root {49,60}, and the 11x11 empty root remain **UNKNOWN**. The bit7
400-node aggregation discrepancy reserve remains open and unrelated.
