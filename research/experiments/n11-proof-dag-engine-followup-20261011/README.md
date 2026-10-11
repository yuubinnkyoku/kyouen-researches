# 11×11 cross-root TT sharing and shared proof bundle (2026-10-11)

## Aim and scope

This follow-up extends the proof-DAG pilot in
[`../n11-proof-dag-engine-20261011/README.md`](../n11-proof-dag-engine-20261011/README.md).
It adds terminal-closed certificates for multiple solver roots, an independent
verifier for that bundle format, and exact-TT comparisons over two groups of
three **already resolved** direct-LOSS S5 positions. The first group are
siblings of S4 `(1188950301626859520,536870912)` and the second group are
known children of the latest candidate S4 `(1297036692683752448,0)` added to
main during this task. Inputs and provenance are recorded in
`input/resolved-s5-positions.json` and
`input/current-s4-resolved-s5-positions.json`.

No unresolved S5 position was searched: the shared worktree contained active
S5 artifacts from other work, and the task prohibited competing with those
probes. The current S4 still has 96 UNKNOWN children among 106. The target
two-stone position `{60,27}` remains UNKNOWN/unsolved by this experiment.
The current candidate's measured root order did not materially reduce
nodes, so no order change was integrated into general sweeps.

## Implementation

`cpp/solvers/kyouen_dfpn_root.cpp` now accepts
`--proof-dag-dir=DIR` together with exact replay and
`--exact-replay-share-tt`. It accumulates exact dependencies from all selected
roots and writes one shared trace after replay. The existing single-root
`--proof-dag=PATH` mode remains available. Proof capture refuses external
layer/residual shortcuts and never emits a root for UNKNOWN or a cutoff.

The new trace records each canonical position once, each concrete legal move
and canonical child dependency, the exact verdict, terminal marker, and legal
move count. The root rows refer to roots in the shared node table. The
independent `scripts/verify_shared_bundle.py` checks board safety and D4
canonicality with the existing integer-geometry `Board`, verifies every
transition and terminal, checks the fixed-original-first-player AND/OR rule,
rejects cycles, missing or unreachable nodes, and checks complete legal-child
coverage at universal nodes and one decisive witness at existential nodes.
It uses no solver or TT values; only the fixed-player outcome-combination
primitive is reused from the established certificate verifier. A LOSS at an
even S6 node is universal and therefore requires every legal S7 child to be
present and LOSS. Trusted leaves are forbidden.

The portable JSON certificate and CSV trace gzip are deterministic and
lossless. The raw 154,859,700-byte trace is not retained: its SHA-256 and the
gzip round-trip receipt are recorded in the run summary/archive manifest.

## Correctness checks

- `tests/test_shared_bundle.py` checks agreement with the established
  single-root verifier on a 4×4 fixture and rejects missing universal
  children, illegal transitions, wrong outcomes, trusted leaves, unreachable
  nodes, cycles/rank errors, and a bad terminal marker in a gzip trace.
- `scripts/check_multi_root_capture.py` exercises the native writer with two
  duplicate 4×4 empty roots: both are LOSS, the second is a 0-node TT return,
  and the shared bundle independently verifies with no trusted leaves. It
  also checks that a one-node cutoff remains UNKNOWN and writes no proof, and
  that legacy single-root capture remains compatible.
- The predecessor's seven proof-DAG tests cover terminal-only closure and the
  fixed-player convention. Those tests and the new bundle tests are rerun
  separately during integration.
- The first three-root 11×11 bundle was independently checked from solver
  output: 3/3 roots LOSS, 1,002,511 unique proof positions, 1,517,437 edges,
  128,528 terminal positions, and 0 trusted leaves. Receipt:
  `output/shared-s5-proof-bundle-reverse-v1/verification.json`.
- A second three-root bundle for known LOSS children of the latest candidate
  S4 was independently checked: 3/3 roots LOSS, 2,337,747 unique proof
  positions, 3,484,437 edges, 331,495 terminal positions, and 0 trusted
  leaves. Receipt: `output/current-s4-proof-bundle-reverse-v1/verification.json`.

## Measurements

### Transposition sharing and root order: previously resolved sibling set

All variants use the same three resolved roots, `--memo=22`,
`--exact-order=count`, a 15,000,000-node budget per root, and the same host.
Independent mode creates a fresh TT for each root; shared mode retains exact
TT entries across roots. Only the root order changes between shared runs.

| Variant | Root order | Total nodes | Wall seconds | Peak RSS | Node reduction |
| --- | --- | ---: | ---: | ---: | ---: |
| Independent TT | first, second, third | 8,774,720 | 38.125 | 174,481,408 B | baseline |
| Shared TT | first, second, third | 6,304,672 | 28.406 | 173,793,280 B | 28.15% |
| Shared TT | third, second, first | 4,807,724 | 21.484 | 173,772,800 B | 45.21% |

In both shared orders, the last root was returned from exact TT in one node.
The reverse order leads with the previously hardest resolved root, so this is
evidence that order matters for this three-root set, not a general optimal
ordering rule. `output/shared-tt-benchmark-v1/summary.json` contains each row,
raw CSV hash, input hash, executable hash, time, and memory sample.

### Latest candidate S4 resolved children

After fetching current main, we found a new candidate S4 with three committed
direct-LOSS child results. Those exact positions were replayed with the same
solver, `--memo=22`, count order, and 15M budget per root:

| Variant | Root order | Total nodes | Wall seconds | Peak RSS | Node reduction |
| --- | --- | ---: | ---: | ---: | ---: |
| Independent TT | legal84, legal92, legal94 | 13,897,366 | 60.547 | 174,456,832 B | baseline |
| Shared TT | legal84, legal92, legal94 | 13,958,217 | 62.484 | 173,813,760 B | −0.44% |
| Shared TT | legal94, legal92, legal84 | 13,837,831 | 62.391 | 174,317,568 B | 0.43% |

The two shared runs are within half a percent of the independent baseline and
are slower on this sample. Cross-root TT reuse is therefore **not an observed
speedup** for this three-root set; its completed LOSS results are still useful
proof inputs. The per-root runs, inputs, and checksums are in
`output/shared-tt-current-s4-v1/summary.json`.

### Latest candidate S4 proof capture and verification cost

The shared-reverse no-capture run above and the proof-capture run below use
the same executable, root order, input positions, and node budget. Capture
does not change the 13,837,831 search node count, but the solver takes longer
and holds a much larger proof dependency store.

| Variant | Nodes | Wall seconds | Peak RSS | Trace / certificate |
| --- | ---: | ---: | ---: | ---: |
| Shared TT, capture off | 13,837,831 | 62.391 | 174,317,568 B | — |
| Shared TT, proof capture on | 13,837,831 | 116.609 | 2,560,937,984 B | 52,122,189 B trace.gz; 72,771,052 B certificate.gz |

For this set, capture and serialization added 54.218 s (86.9%) and
2,386,620,416 B peak RSS. Independent verification took 1,805.750 s and
4,398,759,936 B peak RSS. The archived trace's uncompressed size was
358,856,750 B. The large memory/time increase reinforces that proof collection
should remain opt-in. Full counts, commands, executable and trace hashes are
in `output/current-s4-proof-bundle-reverse-v1/summary.json`.

### Shared proof capture cost and capacity

Capture was measured on the same reverse-order replay, node budget, host, and
exact same executable (`solver_sha256` is in the measurement receipt).
Capture-off follows the unchanged exact-search path. This is one end-to-end
sample, not a paired multi-run median.

| Variant | Total nodes | Wall seconds | Peak RSS | Stored trace / certificate |
| --- | ---: | ---: | ---: | ---: |
| Shared TT, capture off | 4,807,724 | 21.406 | 174,342,144 B | — |
| Shared TT, proof capture on | 4,807,724 | 37.156 | 1,023,954,944 B | 21,403,584 B trace.gz; 29,607,918 B certificate.gz |

Capture plus serialization took 15.750 s more in this sample (73.6%) and
raised peak RSS by 849,612,800 B (about 810 MiB). The certificate has 1,002,511 nodes and
1,517,437 dependency edges. Independent verification took 753.765 s and
1,906,094,080 B peak RSS. The raw trace was 154,859,700 B before deterministic
gzip; its SHA-256 is
`f998a8e199a784436d3fd49c57861c4566575ce9281339b1d19f107ddffab84b`. The
compressed trace SHA-256 is
`d764499dffb364664aa5985529990aa46c0430072dce83994d508c7ce1741a6f`; the
portable certificate SHA-256 is
`9f55e6997f62ee2bae31d286b98ad2b89b6306e18df5091eac081b05d5d10af6`.

An initial approach independently traced all three roots and converted them
one by one. It produced 235,995,147 raw trace bytes; one conversion was still
using about 1.03 GB RSS after roughly 631 CPU seconds and had not produced a
verified certificate when stopped. Those compressed diagnostic traces and
their raw/gzip SHA-256 receipts are retained under
`output/shared-s5-proof-reverse-v1/`. The capture-cost measurement reproduced
the verified raw trace byte-for-byte; see
`output/capture-cost-same-binary-v1/summary.json`. The abandoned traces are not
counted as proof receipts.
Sharing the proof dependency store reduced the archived trace to 21.4 MB and
the portable shared certificate to 29.6 MB.

The capture memory and serialization cost is material. This experiment does
not enable capture for routine S5 sweeps. The shared TT's node reduction is
promising for batches of already known roots, but this benchmark covers only
three related roots and one machine.

## Reproduction

From the repository root in PowerShell, after the source S5 result files
listed in the input manifest are available:

```powershell
uv sync --locked
g++ -O3 -std=c++20 -DNDEBUG cpp/solvers/kyouen_dfpn_root.cpp -o .local/n11-proof-dag-engine-followup-20261011/dfpn.exe
python research/experiments/n11-proof-dag-engine-followup-20261011/scripts/benchmark_shared_roots.py `
  --solver .local/n11-proof-dag-engine-followup-20261011/dfpn.exe `
  --positions research/experiments/n11-proof-dag-engine-followup-20261011/input/resolved-s5-positions.json `
  --out research/experiments/n11-proof-dag-engine-followup-20261011/output/reproduction-tt
python research/experiments/n11-proof-dag-engine-followup-20261011/scripts/certify_shared_roots.py `
  --solver .local/n11-proof-dag-engine-followup-20261011/dfpn.exe `
  --positions research/experiments/n11-proof-dag-engine-followup-20261011/input/resolved-s5-positions.json `
  --order reverse --solver-order count `
  --out research/experiments/n11-proof-dag-engine-followup-20261011/output/reproduction-bundle
python research/experiments/n11-proof-dag-engine-followup-20261011/scripts/verify_shared_bundle.py `
  --certificate research/experiments/n11-proof-dag-engine-followup-20261011/output/reproduction-bundle/proof-dag-bundle.json.gz
python research/experiments/n11-proof-dag-engine-followup-20261011/scripts/certify_shared_roots.py `
  --solver .local/n11-proof-dag-engine-followup-20261011/dfpn.exe `
  --positions research/experiments/n11-proof-dag-engine-followup-20261011/input/current-s4-resolved-s5-positions.json `
  --order reverse --solver-order count `
  --out research/experiments/n11-proof-dag-engine-followup-20261011/output/reproduction-current-s4-bundle
python research/experiments/n11-proof-dag-engine-followup-20261011/scripts/benchmark_capture_cost.py `
  --solver .local/n11-proof-dag-engine-followup-20261011/dfpn.exe `
  --replay research/experiments/n11-proof-dag-engine-followup-20261011/output/shared-s5-proof-bundle-reverse-v1/replay-input.csv `
  --out research/experiments/n11-proof-dag-engine-followup-20261011/output/reproduction-capture-cost `
  --expected-raw-trace-sha256 f998a8e199a784436d3fd49c57861c4566575ce9281339b1d19f107ddffab84b
```

The first portable-bundle verification takes about 12.5 minutes and 1.9 GB
peak RSS on the recorded machine. Reproducing and verifying the current-S4
bundle takes about 30 minutes and 4.4 GB peak RSS. Each output path must be
new; the scripts refuse to overwrite an existing run. The source S5 CSV inputs
come from the committed 2026-10-10 and 2026-10-11 resolved-root experiments;
they are not regenerated here.

## Limits and next step

The solver improvements measured here are exact TT reuse and root ordering,
not a change to DFPN's internal child ordering. Multiple ordering variants
were compared; no S6/S7 frontier search or unresolved S5 experiment was run.
Proof records do not turn UNKNOWN, cutoff, or cache-only leaves into proofs.
The generated certificates cover only the three listed S5 LOSS roots, not all
children of S4 and not `{60,27}`. The next useful integration is a coordinated
replay of remaining S4 child roots, after confirming that it will not compete
with current S5 work, followed by an independently verified parent proof.

Experiment artifacts, scripts, test fixtures, and outputs are listed with
SHA-256 in `output/final-sha256.json`. Rebuild/check that inventory with:

```powershell
python research/experiments/n11-proof-dag-engine-followup-20261011/scripts/hash_artifacts.py
python research/experiments/n11-proof-dag-engine-followup-20261011/scripts/hash_artifacts.py --check
```
