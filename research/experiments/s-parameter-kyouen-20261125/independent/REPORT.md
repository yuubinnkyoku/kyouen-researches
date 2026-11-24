# Independent verification — s-parameter kyouen game on AG(2,q)

**Verdict: PASS.** All three requested cases reproduce the claimed values exactly.
Board validation passes for q = 2, 3, 4, 5. The parity-graded lemma statement holds
on every safe set of AG(2,4), s = 2 (p = 0, 0 violations). No discrepancy was found,
including no mismatch in misère values or Grundy distributions.

- Date: 2026-11-25
- Verifier: independent implementation written from scratch in this `independent/` directory
- Runtime: Python 3.12.13, standard library only
- Constraints honored:
  - nothing was imported from the experiment's `scripts/`;
  - `output/grundy_general.json` was **not** read until after the independent recomputation finished;
  - the only path created/modified by this verification is `research/experiments/s-parameter-kyouen-20261125/independent/`;
  - no commit was made. (The surrounding working tree already had unrelated uncommitted changes before this task; they were not touched.)

## 1. Commands

Run from the repository root:

```powershell
python research/experiments/s-parameter-kyouen-20261125/independent/verify.py
python research/experiments/s-parameter-kyouen-20261125/independent/crosscheck.py
python research/experiments/s-parameter-kyouen-20261125/independent/check_claims.py
python research/experiments/s-parameter-kyouen-20261125/independent/compare_experiment_output.py
```

`verify.py` (≈3.3 s total) writes `board_validation.json`, `grundy_results.json`,
`parity_lemma_ag24_s2.json`. `crosscheck.py` (≈2.0 s) writes `crosscheck.json`.
`check_claims.py` writes `claims_check.json`. `compare_experiment_output.py`
writes `experiment_output_comparison.json` and is the only script that reads
`output/grundy_general.json`. The exact console output is preserved in `run_log.txt`.

## 2. Board validation (all four AG(2,q) boards)

Parsed `output/board_ag2q{2,3,4,5}.txt` (format `<n> <b>` then `b` lines `<k> p1 ... pk`, 0-based).
Required checks: `n = q^2`, `b = q(q+1)`, every line has `q` distinct points, every point is in range,
every pair of points lies on exactly one line, every point lies on exactly `q+1` lines.
Extra structural checks: no duplicate lines, the disjointness relation partitions the lines into
`q+1` parallel classes of `q` lines each, and for every point `p` and line `L` not through `p`
there is exactly one line through `p` disjoint from `L` (affine parallel axiom).

| board | n | b | line size | pairs covered | lines per point | parallel classes | required checks | extra checks | verdict |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| AG(2,2) | 4 | 6 | 2 | 6/6 (each ×1) | 3 | 3 × 2 | PASS | PASS | PASS |
| AG(2,3) | 9 | 12 | 3 | 36/36 (each ×1) | 4 | 4 × 3 | PASS | PASS | PASS |
| AG(2,4) | 16 | 20 | 4 | 120/120 (each ×1) | 5 | 5 × 4 | PASS | PASS | PASS |
| AG(2,5) | 25 | 30 | 5 | 300/300 (each ×1) | 6 | 6 × 5 | PASS | PASS | PASS |

These four axioms make each board a 2-(q², q, 1) design with affine parallel structure.
Board file SHA-256s are recorded in `board_validation.json`.

## 3. Method and independence

Two algorithmically different implementations were used.

* **Implementation A — `verify.py`.**
  Canonical DFS enumeration of safe sets in increasing point order with incremental per-line counts,
  plus a second enumeration in decreasing point order. Every enumerated set is re-checked directly
  against the line masks (`(S & L).bit_count() <= s` for all lines). Maximality is tested by scanning
  all points for a legal addition. Grundy values and misère outcomes are computed by DP in
  decreasing set-size order.
  - Normal play: a player with no move **loses**; `G(S) = mex{G(S+x)}`.
  - Misère: a player with no move **wins**; `misere_win(S) = terminal OR ∃ move to a misère loss`.
* **Implementation B — `crosscheck.py`.**
  - For the two 16-point boards, all `2^16 = 65,536` subsets are tested directly against the line
    definitions, and the DP uses only safe-set membership.
  - For AG(2,5), s = 2, subsets are enumerated by increasing size with `itertools.combinations`;
    level 7 contains 0 safe sets, so no safe set of size ≥ 7 exists (every subset of a safe set is safe),
    which proves completeness. 726,206 subsets were scanned.
  - Full Grundy **and** full misère tables are compared with Implementation A through SHA-256 hashes.

Both enumeration orders in Implementation A returned identical sets in all three cases
(1,793 / 16,426 / 26,073).

## 4. Results versus the claims

All claimed fields match. "Per-size" counts are over all safe sets; "maximal" means no point can be
added while remaining safe. Misère(∅) = 1 means the player to move from the empty position wins
under the stated misère convention.

| case | safe sets | per-size counts (computed) | maximal (size:count) | G(∅) | misère(∅) | Grundy distribution | max G |
|---|---:|---|---|---:|---:|---|---:|
| AG(2,4), s=2 | 1,793 | {0:1, 1:16, 2:120, 3:480, 4:840, 5:288, 6:48} | {4:120, 6:48} | 0 | 1 | {0:1009, 1:784} | 1 |
| AG(2,5), s=2 | 16,426 | {0:1, 1:25, 2:300, 3:2000, 4:6500, 5:6600, 6:1000} | {5:600, 6:1000} | 0 | 1 | {0:5401, 1:8025, 2:3000} | 2 |
| AG(2,4), s=3 | 26,073 | {0:1, 1:16, 2:120, 3:560, 4:1800, 5:4128, 6:6688, 7:7200, 8:4440, 9:1120} | {8:120, 9:1120} | 1 | 0 | {0:12184, 1:12929, 2:960} | 2 |

Field-by-field claim check (`claims_check.json`, `all_pass: true`):

| case | safe count | per-size | maximal | G(∅) | misère(∅) | Grundy distribution |
|---|---|---|---|---|---|---|
| AG(2,4), s=2 (all fields claimed) | PASS | PASS | PASS | PASS | PASS | PASS |
| AG(2,5), s=2 (sizes not claimed) | PASS | — | PASS | PASS | PASS | PASS |
| AG(2,4), s=3 (sizes not claimed) | PASS | — | PASS | PASS | PASS | PASS |

Additional computed misère win/loss distributions over all safe sets
(0 = losing for the player to move, 1 = winning):

| case | misère distribution |
|---|---|
| AG(2,4), s=2 | {0:784, 1:1009} |
| AG(2,5), s=2 | {0:8025, 1:8401} |
| AG(2,4), s=3 | {0:12929, 1:13144} |

## 5. Parity-graded lemma on AG(2,4), s = 2

Statement checked: *if all maximal safe sets have the same parity p, then
Grundy(S) = (p − |S|) mod 2 for every safe S.*

- Maximal sizes are 4 and 6, both even, so the parity is uniform and `p = 0`.
- All **1,793** safe sets were checked against `G(S) = (0 − |S|) mod 2`; **violations: 0**
  (see `parity_lemma_ag24_s2.json`).
- Since negation is the identity mod 2, the formula is `G(S) = |S| mod 2` here. The Grundy
  distribution `{0:1009, 1:784}` equals the even/odd size counts `{even:1009, odd:784}`,
  so the distribution check also agrees.
- Context requested in the task: AG(2,5), s=2 has maximal sizes 5 and 6 (mixed parity) and
  Grundy 2 appears (3,000 sets); AG(2,4), s=3 has maximal sizes 8 and 9 (mixed parity),
  G(∅)=1 and Grundy 2 appears (960 sets). These are consistent with parity uniformity being a
  sufficient hypothesis (the data check does not address its converse).

Remark: the statement itself is an elementary induction on the remaining game length, but the
task asked for a data check on every safe set; that is what is reported here.

## 6. Cross-checks

| case | second method | subsets scanned | safe count | full-table match (Grundy) | full-table match (misère) |
|---|---|---:|---:|---|---|
| AG(2,4), s=2 | full powerset | 65,536 | 1,793 | yes | yes |
| AG(2,4), s=3 | full powerset | 65,536 | 26,073 | yes | yes |
| AG(2,5), s=2 | combinations by size | 726,206 | 16,426 | yes | yes |

Full-table SHA-256 (format: sorted `mask:value;` entries; identical in both implementations):

| case | Grundy table SHA-256 | misère table SHA-256 |
|---|---|---|
| AG(2,4), s=2 | `16e01adf3d0a1cffbec9cffee4ffc38b3b9bcfd8e5c201e04eef8cd6e585d691` | `95173ccb7c46e6d36d2e295283f5ad025236b9b5ddecce8968c3c2bcd3df481a` |
| AG(2,5), s=2 | `010ab293c13bfb9a30c38a9848c16a22c60b2cd350436b1299df42e595ce25ca` | `2b09d661a3373bac46ae3cceee16217fa626664e6537e7686cde7c16d8e48388` |
| AG(2,4), s=3 | `bbbe753f940db81762cc46b0e45ada8b13e2cfa10e7c532472889abf729bb269` | `531ed6cb88dae9fe6b4ccaa45cb57562e98314c13050a1c6f04d1c0744061fc7` |

`crosscheck.json` records `all_match_verify: true`.

## 7. Comparison with the experiment's stored output

Only after the independent recomputation completed, `output/grundy_general.json` was read and its
aggregates for the three cases were compared (`experiment_output_comparison.json`). All fields
matched: `safe`, `size_counts`, `maximal_by_size`, `root_grundy`, `root_misere_win`, `grundy_dist`.
So claims, independent computation, and the experiment's own stored output agree on all three cases.

## 8. Discrepancies

**None.**

- No mismatch in misère values (AG(2,4) s=2: 1; AG(2,5) s=2: 1; AG(2,4) s=3: 0).
- No mismatch in Grundy distributions (`{0:1009,1:784}`, `{0:5401,1:8025,2:3000}`,
  `{0:12184,1:12929,2:960}`).
- No mismatch in safe-set counts, per-size counts, maximal-set sizes/counts, or G(∅).
- Board checks all pass, and the parity-lemma data check has zero violations.

## 9. Artifacts in this directory

| file | contents |
|---|---|
| `verify.py` | primary independent implementation (DFS + DP) |
| `crosscheck.py` | second independent implementation (powerset / combinations + membership DP) |
| `check_claims.py` | field-by-field comparison against the claimed values |
| `compare_experiment_output.py` | post-recomputation comparison with `output/grundy_general.json` |
| `board_validation.json` | per-board checks, counts, file SHA-256 |
| `grundy_results.json` | computed aggregates, full-table hashes, timings |
| `parity_lemma_ag24_s2.json` | per-safe-set formula check, p, violations, size-parity counts |
| `crosscheck.json` | second-method results, completeness argument, hash comparison |
| `claims_check.json` | machine-readable PASS/FAIL per claimed field (`all_pass: true`) |
| `experiment_output_comparison.json` | agreement with the experiment's stored aggregates |
| `run_log.txt` | captured console output of all four commands |

## 10. Notes and limitations

- This is a finite verification of the three requested computations and of the board files; it does
  not attempt to prove the general parity-graded lemma or any q-general statement.
- The misère recursion uses the task's convention (no move = win); terminal maximal sets are therefore
  misère wins, which is reflected in the distributions above.
- Full Grundy/misère tables are not dumped to disk; they are pinned by the SHA-256 hashes and can be
  regenerated deterministically by the two scripts in a few seconds.
