# 2026-11-14 n11 class4-batch3 child#3 sweep (session 19, long lane)

Session-18 resume item 1: sweep the cheapest remaining S6 child of the class-4 lane
target S5 `00000000020000003800000080000000` after the batch2 frontier recompute.

## Target

- S6 child `00000000020000003802000080000000` (s6_s7_edge_cost 68, demand c1=0,c2=0,c4=3)
- 68 non-degenerate 7th-stone candidates (of 115 empty cells; no 4-cocircular with the
  6 stones), ordered by root mobility ascending (mob 46..65).

## Sweep result (v15 engine verbatim, native Node, ~550k nodes/s)

- **67 candidates REFUTED-D10, 1 candidate WIN7-D10 (bit 37), 0 capped.**
- bit 37: root `00000000020000003802002080000000`, lossAt(root,10)=true at
  9,625,156 nodes (3 independent runs, node counts identical).
- Total 218,994,665 nodes over 68 candidates in 3 foreground executions
  (cap 50M/candidate never reached; largest single candidate bit7 11,196,395).
- Pilot control PASS: lossAt(6)=false at exactly 5,949 nodes (published v15 reference).
- Determinism controls: fresh re-solves of bits {36,7,40,114,112,16} node-exact vs the
  sweep run; terminal stone range [13,17] on every uncapped candidate.

## bit 37 WIN7 certificate (11th verified WIN7 certificate overall, 1st of batch3)

- Extraction: kill-first, single process, all 49 root first-moves,
  17,310,200 nodes, 36,092 rows, terminals [13,17].
- Certificate: `output/class4-batch3-certificates/n11_s7_00000000020000003802002080000000.cert`
  (plain text, 1,300,688 bytes, md5 5228c195af4a4b8a7d4b252e7eea3a5e).
- Independent verification (verify_five_terminal_loss7.py TS port, exact Bareiss,
  no engine import): **49/49 sub-roots PASS**, consumed winner-state union = 36,092 =
  the full row set exactly (missing 0 / extra 0), root checks PASS
  (7 stones, no 4-cocircular subset, loser mobility 49).
- Record: `output/class4-batch3-bit37-certificate.json`;
  sweep record: `output/class4-batch3-child3-sweep.json`.

## Frontier effect (local, exact)

covers(root37) = 7 canonical S6 orbits; two of them are remaining children of the
class-4 lane target:
- the swept child itself `00000000020000003802000080000000` (cost 68), and
- `00000000020000003800002080000000` (cost 77).

**Class-4 lane target: remaining 32 → 30 S6 orbits, cost 2530 → 2385.**
Next cheapest remaining S6 child: `00000000020000003800000084000000` (cost 69).
The manifest-level frontier recompute (solved&manifest, demand histogram,
class-2/4 global ranking with this certificate in WIN7_VERIFIED) still needs the
repo `audit_class_frontier.py` run with the gz inputs (gz files are not retrievable
through the file connector; run it where the repo checkout lives) — next session.

## Lane-switch reconsideration (session-18 resume item 2)

After this session's delta the comparison stands: class-4 lane target now
30 orbits / 2385 cost; class-2 best blocker `00000000000000003802000008000000`
32 orbits / 2206 cost. Orbit count now favors the class-4 lane (30 < 32); cost
still favors class-2. The class-2 blocker is another lane's published target
(class2-batch certificates) and its children have demand c2=2, while the class-4
target's children mostly have c4=3 (each WIN7 certificate closes up to three
class-4 S5 candidates). Decision: stay on the class-4 lane; re-evaluate after the
full frontier recompute.

## Operational notes

- Background (`nohup`) processes do not survive between bash calls in this
  execution environment; the sweep was run as 3 foreground executions instead.
- Certificate transfer used paged `read_file` reassembly in the sandbox push
  (session-18 method); post-push verification via git blob SHA comparison.

## Status

WIN7 certificates prove only a win within depth 10 from their 7-stone root;
REFUTED-D10 entries negate only WIN7-within-depth-10. class 4, S2 {59,60},
two-stone root {49,60}, and the 11x11 empty root remain **UNKNOWN**. The bit7
400-node aggregation discrepancy reserve remains open and unrelated.
