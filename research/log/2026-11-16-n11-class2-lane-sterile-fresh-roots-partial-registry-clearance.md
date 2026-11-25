# class2-lane: sterile-row fresh roots partial registry clearance (2026-11-16)

## What was done

- All 135 fresh root orbits from the orbit-aware fresh-target tables (65k: 49, 70j: 45, 74h: 41) were checked against the swept-root sets of the four candidates whose child hexes are published in this session's fetched fold records: cost-60c child 00000000000000003800000008008020, cost-75e child 00000000040000809002000000000002, cost-65f/65j child 00000000000000809102000080000000, cost-70g child 00000000000000801202000040000001.

## Results

- Registry sizes: 60/75/65/70 swept roots - exactly matching the recorded candidate counts of the four sweeps (60c: 60 candidates, 75e: 75, 65f/65j: 65, 70g: 70). Independent confirmation of both the child hexes and the legal-bit implementation.
- Control: the certified WIN7 cost-60c bit-92 root (00000000000000801292200000000000) is found in the cost-60c child registry at bit 92.
- Clearance: **135/135 fresh root orbits cleared (0 hits)** against the 270 swept roots of these four candidates. None of the published fresh targets is a root of any of these four candidates.
- Tables JSON updated to v2 with the clearance record.

## Remaining caveat

- Older candidate sweeps (2026-11-15 lanes 75c/75d/76a/76b/77a-d/78a/79a/80d/82c/83a/83b, plus 63a/63h/72b/69i and earlier) are not remotely enumerable here. A fresh root swept REFUTED in any of them would be a false-fresh target (it cannot be WIN7 or the row would already be closed). The engine lane must check the fresh roots against the full swept-root registry before sweeping their generator children.
- The second coverable class-2 parent 00000000000000801202000040000000 holds two further open STERILE rows (edges 64 and 71 among its 5 remaining rows 76/76/77/64/71); their hexes cannot be uniquely identified remotely (the parent's ~116 superset orbits are mostly long-closed, the cost fingerprint is insufficient). The engine lane should extract them from the manifest and apply the same fresh-target methodology.

## Status

- 11x11 empty board, S2 {59,60}, class1/class2/class4 roots: **UNKNOWN** (unchanged; geometry and bookkeeping only).

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-sterile-rows-orbit-aware-fresh-target-tables-20261116.json` (v2)
