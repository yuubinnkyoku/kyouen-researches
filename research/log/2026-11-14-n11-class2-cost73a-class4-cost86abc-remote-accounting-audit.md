# 2026-11-14 — n11: remote accounting audit of cost-73a and cost-86a/86b/86c (session 11)

## Context

Four sweeps were published on 2026-11-14 for the S5 targets of the class-2 and
class-4 lanes: class2-lane cost-73a (session-11 takeover, 1 WIN7-D10 bit81 with
certificate) and class4-lane cost-86a/86b/86c (19th/20th/21st observed sterile
children). This session re-fetched every remote artifact and recomputed the
accounting from the raw lines only, under the same protocol as the cost-73e /
cost-74 remote accounting audit.

## What was done

- Re-fetched all 64 remote files at commit 203e96fc: raw batches 11+11+14+15,
  determinism reruns (4), the 73a FBS=1<<20 crosscheck, inflight records (4) and
  sweep records (4). Strict JSON parse of every line: 0 parse failures.
- Verified via path-filtered commit listing that no commit after 203e96fc
  touches any audited file.
- Compared candidate bit sets bit-exact against inflight/record candidate lists;
  compared every raw row's nodes/verdict/capped/terminal-range against the
  sweep records; recomputed node totals from raw lines only; checked all pilot
  d6 control lines (loss=false at exactly 5,949 nodes).

## Results (all PASS)

- cost-73a: 73/73 rows; total exactly 383,290,602; WIN7 bits [81]; 72 REFUTED;
  0 capped; terminal range [13,17] on every row; determinism rerun (bits
  92/23/48/81) node-and-verdict-exact; runner_fbs20 crosscheck (parallel lane)
  4/4 rows fbtDrops=0 with node counts bit-exact identical (fbtMaxProbe<=6);
  session-9 cross-restart control: the 64 previously-counted candidates sum
  exactly 324,426,606 and the completing 9 sum exactly 58,863,996; heaviest-bit
  table exact.
- cost-86a: 86/86 rows, total exactly 373,903,515; determinism (bits 118/105/34)
  node-exact; sterile (19th).
- cost-86b: 86/86 rows, total exactly 344,931,733; determinism (bits 8/86/67)
  node-exact; sterile (20th).
- cost-86c: 86/86 rows, total exactly 301,085,672; determinism (bits 112/82/113)
  node-exact; sterile (21st).
- Combined: 331 candidates, 1,403,211,522 nodes, 1 WIN7, 330 REFUTED, 0 capped.
- Wording note: the 73a record says "all 12 batch invocations" but the 11 pushed
  batch files hold 11 pilot control lines (batch2 carries a single line); same
  wording-vs-file class as the cost-74 audit, substance unaffected.
- fbt link: the 73a FBS=1<<20 crosscheck closes the fbt-audit follow-up-2
  pending items (bits 92/23 are saturated-but-confirmed-surviving, drop-free node
  counts identical to the canonical counts). The fbt audit README, log, K0783
  and runs-manifest-followup2.json are updated pending->confirmed in the same
  commit.

## Consequences

No verdict, frontier number, or certificate changes. The accounting of all four
sweeps is independently recomputable from the pushed raw batches. 11x11 remains
UNKNOWN.

## Artifacts

- research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73a-class4-lane-cost86a-86b-86c-remote-audit-20261114.json
- updated: n11-fbt-saturation-audit-20261114 README.md, output/runs-manifest-followup2.json
- updated: research/log/2026-11-14-n11-fbt-saturation-audit.md
- updated: research/knowledge/items/K0783-n11-ms5-worklist-derivation-verified-and-s7-reuse-partition.md

## Interpretation guard

REFUTED-D10 is the absence of a winner-win-within-depth-10 in a 7-stone subtree;
WIN7-D10 proves only an individual 7-stone root; sterile children are not child
refutations. **11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2,
class 4: UNKNOWN.**
