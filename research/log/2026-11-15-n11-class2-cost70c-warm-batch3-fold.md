# n11 class2-lane: cost-70c warm batch-3 (bits 3/42/86/103) certificates + gain-0 fold; cost-70c band 13/13 complete; chain head unchanged 1163

Long-term lane session (2026-11-15 JST). The cost-69f receipts recompute
(commit 30c638d5, chain head 1163/6684/527280/4954/391003) explicitly
deferred the four cost-70c warm batch-3 receipts to "the next recompute".
This session published those four WIN7 certificates (completing the
cost-70c band 13/13 certified) and executed the deferred gain-0 fold. No
sweep claims are made here beyond the published records — receipts only.

## Warm batch-3 certificates (blind extraction + BigInt independent verification)

`warm_rebuild_pipeline2_20261115.py` (raw-batch row extraction, no repo
verifier/solver/cache import) rebuilt the four last uncertified WIN7 bits of
the cost-70c sweep at child `00000000000000803242000000000000`, followed by
independent BigInt verification of every record (root == child | 1<<bit,
rows sorted-unique, sub-roots == loser mobility, union 0/0, terminal range
13..17, md5/sha256/bytes against the pushed certificate files) and a
separate-process determinism rerun for bit 103 (extraction nodes and md5
exact):

- bit 3, root `00000000000000803242000000000008`: 50,955 rows /
  11,537,642 extraction nodes / md5 `ae02f4b95be3e50518ce7830d2083434`
- bit 42, root `00000000000000803242040000000000`: 50,015 rows /
  11,335,391 nodes / md5 `b7ae6d13da02e880ca10b4ba7c8231d9`
- bit 86, root `00000000004000803242000000000000`: 68,358 rows /
  27,716,890 nodes / md5 `483618fc5b04db401d91dd6a82b25dfd`
- bit 103, root `00000080000000803242000000000000`: 45,205 rows /
  11,012,568 nodes / md5 `aac78501eb7b16edfc4cb45c04d2a897`

Totals: 214,533 rows / 61,602,491 extraction nodes. Certificates published
under `output/class2-lane-cost70c-certificates/` (bits 3/42/86 as two parts
each, bit 103 as a single 1.63 MB file under the ~1.75 MB per-push limit);
every file verified byte-exact by git blob sha after landing. Commits:
inflight claim b9822fb0; certificate parts de5c28dc / f555a61a (bit 3),
eae84c55 / bc9ea030 (bit 42), ab456709 / 088321b2 (bit 86), d0c20dbf
(bit 103); records JSON + claim closure 267762ab.

## The deferred fold (recompute_frontier_after70cwarm3_20261115.py, commit 6d4ced10)

Environment fact first: an earlier variant of this script reproduced the
unified-merge head a second time in the same process (a second full runpy
chain) and was killed by the execution environment's ~1 GB memory cap
(SIGKILL mid-chain at the cost-61d controls; exit 137). One full runpy
chain per process is the working limit. The published variant instead
reuses the unified-merge namespace from inside the cost-69f chain: that
chain already reproduces the unified head with a blob-identical head-JSON
control (blob a0789eed… asserted), so no second chain is needed.

Controls of the published script, all asserted:

1. runpy reproduction of the cost-69f chain head byte-identically
   (1163/6684/527280/4954/391003), including its chain-internal
   unified-merge reproduction (1154/6693/527949/4963/391672) and the
   assertion that the 1163 solved set extends the 1154 solved set;
2. the four warm batch-3 records asserted against the published records
   JSON (root identity, rows, sub-roots, union 0/0, terminal range,
   md5/sha256/bytes, bit-103 determinism rerun exact);
3. root disjointness: the four new roots vs the 49 distinct unified
   receipt roots (12 + 31 + 6) and the 9 cost-69f receipt roots,
   intersections empty;
4. fold in record order (bits 3, 42, 86, 103) with every per-record
   marginal re-derived from the growing union, and the set-equality
   control s_after == s_1163 UNION covers(4 batch-3 roots);
5. gain-0 in manifest asserted: total marginal 8 (bits 42/86: 4 each,
   non-manifest orbits only), marginal-in-manifest 0 for all four bits,
   head numbers unchanged;
6. cross-check against the parallel lane's published prediction
   (`class2-lane-next-fold-marginal-prediction-20261115.json`): per-bit
   marginals 0/4/4/0 match exactly, marginal-in-manifest 0/0/0/0.

Two local runs byte-identical; all four pushed files (script + recompute
JSON + ranking CSV + top-candidates CSV) verified byte-exact by git blob
sha after landing.

## Result and the three independent derivations

Fold result at the 1163 head: covers 7 per root; marginal 0/4/4/0
(bits 3/103 fully pre-covered by receipts already in the chain, bits 42/86
covering only non-manifest orbits); marginal-in-manifest 0. The head is
unchanged: **1163 / 6,684 / 527,280 / 4,954 / 391,003** (175 remaining S5
orbits). The cost-70c band is now 13/13 WIN7-certified (9 previously + 4
here). This is a band-completion bookkeeping fold — no frontier numbers
changed and no verdict is claimed by it.

Three independent derivations of the batch-3 gain-0 structure now agree:

- the parallel lane's prediction (baseline 1154): per-bit marginal
  0/4/4/0, marginal-in-manifest 0 for all four;
- the parallel lane's third-method independent audit
  (`class2-lane-next-fold-prediction-independent-audit-20261115.json`,
  commit c10e6e9f: independent D4 canonicalization, one-stone-deletion
  lift re-derivation, determinant-based concyclicity, no repo imports):
  bits 42/86 regenerated non-manifest lift count exactly 4,
  marginal-in-manifest consistent with 0, 13/13 root identity+safety;
- this fold recompute at the 1163 head (chain-internal, receipts-only).

## Interpretation guard

solved counts measure manifest coverage, not the game-theoretic value of
any position; REFUTED-D10 sweeps prove only the absence of WIN7-D10; WIN7
certificates prove a win within depth 10 from the individual 7-stone roots
only. The standard 11x11 empty board, the two-stone roots {49,60}/{59,60},
S2 {59,60}, class 2 and class 4 remain UNKNOWN.
