# 11×11 proof-cover minimum and disk-backed proof bundles (2026-10-11)

## Scope

This experiment reconstructs the current `117/119` third-move cover from the
frozen K0372 frontier, derives each LOSS-class incidence again from integer
geometry, and adds a disk-backed verifier plus a compact binary encoding for
the existing shared proof-bundle schema. It launches no game search and does
not modify the source JSON certificate, K0372, or solver verdicts. The
alternative witness is emitted as a separate, locally stored proof variant.

The measured proof input is the current-main three-root S5 LOSS bundle from
[`../n11-proof-dag-engine-followup-20261011/README.md`](../n11-proof-dag-engine-followup-20261011/README.md):
2,337,747 unique positions, 3,484,437 move-labelled edges, 331,495 terminal
positions, and zero trusted leaves. This is not an S4 proof, the `{60,27}`
root proof, or completion of the current S4 boundary.

## Frozen class-cover result

`scripts/analyze_class_cover.py` checks all 3,384 S4 classes and the 119 legal
third moves against K0372's saved frontier and third-move certificate. For each
of the 31 current LOSS classes, it enumerates D4 orientations, checks the fixed
two-stone root and third move, and tests whether the fourth move is legal. The
geometry-derived incidence agrees with every stored class incidence and every
saved witness.

All 31 known LOSS classes are required to reproduce the present 117/119 cover:
112 of the 117 covered moves have exactly one covering class, and these unique
witnesses include all 31 classes. The remaining five covered moves have
incidence counts `2, 2, 2, 2, 13`; moves 100 and 108 have no known LOSS-class
witness. Therefore the exact minimum is 31 classes for this frozen set and
this 117-move target. It does not imply that these classes have independent
minimax proofs. K0372 supports only one of the 31 class verdicts from raw-rooted
evidence; the root `{60,27}` remains UNKNOWN.

The minimum class count is separate from proof-DAG size and verifier cost. A
bounded audit found two closed S6 LOSS witnesses for S5 root
`10412322338480590849`: the stored move 11 child has a 666,475-node closure;
move 46 has a 792,830-node closure and is already selected by another root.
Replacing root 2's witness with that already verified move 46 and pruning
nodes that become unreachable leaves all three roots intact and reduces this
three-root DAG from 2,337,747 nodes / 3,484,437 edges to 1,718,259 nodes /
2,547,576 edges. The smaller standalone closure was not the better global
choice because move 46's larger closure was already shared. The new variant
was independently verified in full. This is an exact improvement for the
frozen three-root graph, not a global minimum or a result for the containing
S4 or `{60,27}` root. No S6 search was launched.

## Disk-backed verifier and compact format

`scripts/bundle_store.py` has five operations:

- `verify-json` incrementally parses one JSON node at a time into a temporary
  SQLite index, then checks geometry, canonicality, all legal moves, witness
  polarity, complete universal children, terminal labels, strict rank increase,
  root verdicts, no trusted leaves, and reachability.
- `convert` validates a JSON source, emits the compact format, decodes it
  independently, and compares the graph tables and roots field by field.
- `verify-compact` decodes and independently verifies the compact proof.
- `optimize-witness-switch` requires a successful receipt bound to the exact
  compact input, replaces one existential root witness with a legal move to a
  previously verified closed child, prunes unreachable nodes, and writes a
  separate compact certificate.
- `export-json` verifies a compact proof and exports the original JSON schema.

During conversion, the frozen three-root graph is also checked for alternate
S6 LOSS children that are legal moves of an S5 root and already present as
closed nodes in the shared DAG. If alternatives exist, it measures the
terminal-closed descendant node count to support a witness comparison. This
audit is bounded to proof material already in the certificate; it does not
scan solver caches or start an S6 replay.

The `KYPRFDG v1` payload fixes the board proposition and schema in its versioned
header. It stores each canonical mask once as a delta-coded integer, derives the
stone count from the mask, stores verdict/terminal/legal-count/out-degree, and
represents each concrete edge by its move byte and node-table reference. It
preserves every legal-move label and every canonical child dependency. An
internal SHA-256 checksum detects accidental corruption; the source/output
SHA-256 receipt binds the exact artifact for publication. The checksum is an
integrity check and does not replace semantic verification.

Temporary indexes are created outside Git. Large converted certificates belong
in an artifact store or release asset accompanied by the compact-format version,
source JSON SHA-256, compact artifact SHA-256, node/edge counts, and verifier
receipt. They should not be added to ordinary repository history.

## Tests and reproduction

Small independent fixtures compare both formats with the established shared
bundle verifier and reject modified bytes, omitted universal children, illegal
moves, incorrect polarity, trusted leaves, and unreachable nodes. The frozen
cover test rebuilds the 117/119 incidence and the 31-class lower bound. A
journal-disabled SQLite regression confirms that witness-switch measurements
restore the original source edge.

```powershell
uv run --locked python research/experiments/n11-proof-compact-20261011/scripts/analyze_class_cover.py
uv run --locked python -m unittest discover -s research/experiments/n11-proof-compact-20261011/tests -v
uv run --locked python research/experiments/n11-proof-compact-20261011/scripts/benchmark_verifier.py `
  --format json `
  --certificate research/experiments/n11-proof-dag-engine-followup-20261011/output/current-s4-proof-bundle-reverse-v1/proof-dag-bundle.json.gz `
  --out-dir .local/n11-proof-compact-20261011/bench-json-replay
uv run --locked python research/experiments/n11-proof-compact-20261011/scripts/bundle_store.py `
  --scratch-dir .local/n11-proof-compact-20261011/convert-replay/scratch convert `
  --source research/experiments/n11-proof-dag-engine-followup-20261011/output/current-s4-proof-bundle-reverse-v1/proof-dag-bundle.json.gz `
  --output .local/n11-proof-compact-20261011/current-s4-three-s5-roots.kpd.gz `
  --prior-verification .local/n11-proof-compact-20261011/bench-json-replay/benchmark.json `
  --receipt .local/n11-proof-compact-20261011/conversion.json
uv run --locked python research/experiments/n11-proof-compact-20261011/scripts/benchmark_verifier.py `
  --format compact `
  --certificate .local/n11-proof-compact-20261011/current-s4-three-s5-roots.kpd.gz `
  --out-dir .local/n11-proof-compact-20261011/bench-compact-replay
uv run --locked python research/experiments/n11-proof-compact-20261011/scripts/bundle_store.py `
  --scratch-dir .local/n11-proof-compact-20261011/optimize-replay/scratch optimize-witness-switch `
  --certificate .local/n11-proof-compact-20261011/current-s4-three-s5-roots.kpd.gz `
  --prior-verification .local/n11-proof-compact-20261011/bench-compact-replay/benchmark.json `
  --root-id 2 --move 46 `
  --output .local/n11-proof-compact-20261011/current-s4-three-s5-roots-witness-46.kpd.gz `
  --receipt .local/n11-proof-compact-20261011/witness-switch-variant.json
uv run --locked python research/experiments/n11-proof-compact-20261011/scripts/benchmark_verifier.py `
  --format compact `
  --certificate .local/n11-proof-compact-20261011/current-s4-three-s5-roots-witness-46.kpd.gz `
  --out-dir .local/n11-proof-compact-20261011/bench-optimized-replay
uv run --locked python research/experiments/n11-proof-compact-20261011/scripts/bundle_store.py export-json `
  --certificate .local/n11-proof-compact-20261011/current-s4-three-s5-roots-witness-46.kpd.gz `
  --output .local/n11-proof-compact-20261011/current-s4-three-s5-roots-witness-46-round-trip.json.gz
```

## Measurements

The verifier runs used one Windows host and a 250 ms process-tree RSS / scratch
sampler. The old baseline is the same three-root certificate and same host,
using the prior JSON-materializing verifier. The streamed JSON measurement's
wall time and scratch peak are valid, but its first RSS sampler observed only
the Python launcher; its RSS is therefore omitted. The corrected process-tree
sampler was used for both compact runs.

| Proof / verifier | Nodes | Edges | Certificate bytes | Wall seconds | Peak RSS | Peak scratch |
|---|---:|---:|---:|---:|---:|---:|
| Prior JSON verifier | 2,337,747 | 3,484,437 | 72,771,052 | 1,805.750 | 4,398,759,936 B | not recorded |
| Disk-backed JSON | 2,337,747 | 3,484,437 | 72,771,052 | 1,905.109 | not measured | 627,754,176 B |
| Compact, same graph | 2,337,747 | 3,484,437 | 22,089,195 | 1,853.203 | 197,369,856 B | 626,414,784 B |
| Compact, witness switched | 1,718,259 | 2,547,576 | 16,080,927 | 1,366.687 | 193,683,456 B | 454,351,644 B |

The base compact file is 69.65% smaller than JSON. The verified witness-switch
variant is 77.90% smaller than JSON and 27.20% smaller than the base compact
file. Against the original shared graph it removes 26.50% of nodes and 26.89%
of edges. The switch variant verifies 26.25% faster than the base compact graph
and 24.31% faster than the prior materialized verifier. Its peak scratch is
27.47% below the base compact run. The base compact run reduces peak RSS by
95.51% versus the old verifier, at a 2.63% wall-time increase; binary encoding
alone did not make that full graph faster to verify.

The original JSON and compact receipts have zero trusted leaves and the same
three LOSS roots. The switched variant retains the same roots and has zero
trusted leaves. Full details, including source and output hashes, are in
[`output/proof-compact-audit.json`](output/proof-compact-audit.json). The large
`.kpd.gz` artifacts are local under `.local/` and deliberately excluded from
Git history.

## Limits

The proof still covers only three already resolved S5 roots below one S4, not
all S4 children and not `{60,27}`. While this work was running, latest `main`
advanced with two separately recorded experiments on the leading S4
`(1297036692683752448,0)`. Its 106-child boundary is now LOSS 40 / WIN 0 /
UNKNOWN 66, up from LOSS 10 / WIN 0 / UNKNOWN 96. Those additions are direct
solver exact findings, not terminal-closed independent proofs for those S5
roots ([10-root update](../n11-reply27-ten-loss-20261011/README.md),
[20-root update](../n11-reply27-20more-20261011/README.md)). This compact-proof
work launched no overlapping S4 search or probe.
K0372's trust boundary is unchanged: only one of the 31 known LOSS classes has
raw-rooted support for all of its children, and the other 30 are not promoted
to independent minimax proofs. The exact 31-class minimum is not a node-count
minimum. The witness switch is optimal only for this fixed three-root graph
and this already closed candidate set; it does not minimize the full S4 or
`{60,27}` certificate.

The schema keeps an explicit root list and allows shared descendants, so the
same index can later hold a complete S4 node with all 106 S5 LOSS child edges,
or the two-stone `{60,27}` node with all 119 third-move dependencies. Those
edges and their terminal-closed descendants still have to be present and
verified; current three-root S5 data does not close either parent.
