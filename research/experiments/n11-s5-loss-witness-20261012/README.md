# 11×11 S5 LOSS witness search benchmark (2026-10-12)

## Scope

This experiment compares ways to rediscover an exact S6 LOSS witness for six
S5 positions already independently proved LOSS. The fixed sample is the six
roots used by K0375/K0378: three children of the then-current candidate S4
`(1297036692683752448,0)` and three children of the preceding S4. Both
three-root source bundles and their independent receipts are recorded in
`input/targets.json`; K0378 records the combined six-root certificate hash,
LOSS for all roots, and zero trusted leaves.

The sample is deliberately a resolved-root benchmark. It does not estimate
how often an unknown S5 is LOSS or how often a particular S6 is a LOSS
witness. Candidate ordering is only a deterministic cost heuristic, not a
probability claim. The S6 children chosen for each comparison were fixed by
the geometry-only schedule before any solver run.

At each S5, every arm has a total ceiling of 250,000 exact-search nodes. The
direct arm spends that cap on the S5. The S6 arms screen at most five
preselected S6 children, with at most 50,000 nodes per child. Each arm runs
each S5 in a fresh process and starts with empty solver caches. A child is a
LOSS witness only when exact DFPN returns LOSS; WIN and UNKNOWN both continue
the schedule. A found S6 LOSS is a solver result in this benchmark, not a new
independent certificate. Existing terminal-only certificates remain the
independent evidence for the six S5 roots.

## Arms

| Arm | Search | S6 candidate order | Cache behavior |
| --- | --- | --- | --- |
| A | Direct S5 DFPN | not applicable | fresh per root |
| B | Individual S6 DFPN, stop at first exact LOSS | canonical key ascending | fresh per child |
| C | Individual S6 DFPN, stop at first exact LOSS | S6 legal-move count ascending, then key | fresh per child |
| D | Same S6 schedule as C | S6 legal-move count ascending, then key | one shared exact TT per S5 |
| E | Same S6 schedule as C | S6 legal-move count ascending, then key | exact verdict sharing at the 7-stone layer only |

The solver binary and compile flags are identical across arms. Each process
starts with a fresh TT; E's exact-layer map is also process-local and empty at
startup. D shares only among S6 children of the same S5, not between the six
different S5 roots. The experiment records all invocations, node counts,
timeouts/cutoffs, wall time, peak RSS, and cache hits. No result is inferred
for budget-exhausted UNKNOWN rows.

## Logic and trust boundary

The fixed-first-player convention is unchanged. At five stones, one exact S6
LOSS suffices to establish S5 LOSS. At six stones, LOSS requires every legal
S7 child to be LOSS; a partial child set or an UNKNOWN row is not a witness.
The optional `--exact-replay-stop-on-loss` flag only stops after an exact
LOSS row and is disabled by default. It does not change DFPN propagation or
the K0371/K0372 quarantine rules.

No solver-trusted result is imported into the independent proof DAG. The
existing six-root independent certificate is used only as sample provenance.
No unresolved S5 from the current S4 was searched, so this experiment does
not overlap the active boundary work.

## Reproduction

From the repository root in PowerShell:

```powershell
uv sync --locked
New-Item -ItemType Directory -Force .local/n11-s5-loss-witness-20261012 | Out-Null
g++ -O3 -std=c++20 -DNDEBUG cpp/solvers/kyouen_dfpn_root.cpp -o .local/n11-s5-loss-witness-20261012/dfpn.exe
python research/experiments/n11-s5-loss-witness-20261012/scripts/prepare_candidates.py
python -m unittest discover -s research/experiments/n11-s5-loss-witness-20261012/tests
python research/experiments/n11-s5-loss-witness-20261012/scripts/check_stop_on_loss.py --solver .local/n11-s5-loss-witness-20261012/dfpn.exe --out research/experiments/n11-s5-loss-witness-20261012/output/stop-on-loss-reproduction-v1
python research/experiments/n11-s5-loss-witness-20261012/scripts/benchmark_witness_methods.py --solver .local/n11-s5-loss-witness-20261012/dfpn.exe --schedule research/experiments/n11-s5-loss-witness-20261012/input/s6-candidate-schedule.json --out research/experiments/n11-s5-loss-witness-20261012/output/reproduction-v1
python research/experiments/n11-s5-loss-witness-20261012/scripts/hash_artifacts.py
```

The benchmark refuses to overwrite output. The generated solver binary and
large transient files live under ignored `.local/`; committed artifacts are
the fixed input/schedule, small CSV/JSON measurements, test code, and SHA-256
receipts. `input/build.json` records the compiler, flags, source hash, and
binary hash. The result manifest includes input, source, binary, raw-row, and
summary hashes.

## Result

### Same-binary, equal node ceiling

The six roots were run serially on Windows with one binary built from the
committed solver source. Every arm received exactly 250,000 nodes per S5
(1,500,000 total). A tested the S5 directly. B–E screened the first five
geometry-ranked canonical S6 children per S5 at 50,000 nodes each; all 30
screened S6 rows in each arm reached their cap and returned UNKNOWN.

| Arm | Exact S5 / S6 LOSS witness | UNKNOWN rows | Nodes | Wall seconds | Max RSS bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| A direct S5 | 0 / 0 | 6 | 1,500,000 | 4.927 | 173,260,800 |
| B key-order S6 | 0 / 0 | 30 | 1,500,000 | 7.570 | 173,342,720 |
| C legal-count-order S6 | 0 / 0 | 30 | 1,500,000 | 7.508 | 173,330,432 |
| D shared TT among S6 | 0 / 0 | 30 | 1,500,000 | 4.813 | 173,215,744 |
| E shared exact 7-stone layer | 0 / 0 | 30 | 1,500,000 | 7.549 | 173,367,296 |

No arm resolved any target under this ceiling, so there is no demonstrated
S5 LOSS witness cost reduction. D was about 36% faster in wall time than C,
but it used the same node count and was only about 2% faster than direct A.
Because C creates a fresh 2^22-entry TT for each child while D allocates one
table per S5, this timing difference is consistent with avoiding repeated TT
initialization; it does not show fewer proof-search nodes. The one-run timing
is not a verified speedup. E recorded zero 7-stone exact-layer hits and zero
stores: these cutoffs did not complete exact subproofs that could be reused.

The main obstruction is the all-children closure required for an exact S6
LOSS. At 50,000 nodes per candidate, none of the tested S6 roots completed
an exact verdict, so proof sharing had no exact 7-stone facts to transfer.
The legal-count ranking did not change resolution or node use versus key
order. The S6 arms screened only 5 of 84–94 canonical children at each root;
their remaining children are unobserved, and no cost or result is inferred
for them. The selected S5 roots were already resolved and are a biased sample
for future UNKNOWN roots. The experiment therefore does not justify a larger
run or dispatching work on the current S4's UNKNOWN children.

K0375's original direct runs for these roots used 2,335,333–5,416,337 nodes,
but those source runs do not have the same binary/host receipt and are used
only to describe sample selection, not as a controlled baseline. No current
S4 UNKNOWN S5 was searched and no solver result was imported into an
independent certificate. The test-fixture development attempts are separately
audited in `output/regression-fixture-development.json`; they total 149 small
4×4 test nodes and are excluded from the 11×11 comparison.

The optional `--exact-replay-stop-on-loss` mode is disabled by default. Its
4×4 regression receipt checks LOSS-then-WIN behavior, UNKNOWN followed by a
LOSS, and ordinary replay with the flag absent.
