# s_12 / s_13 constructive upper bounds, session 1: census reproduction, transplant diagnostics, complete local nets, 2-swap optimality walls, SLS witness hunts, and lattice-isometry classification (no improvement found; one new 12x12 witness configuration for s_12 <= 11; one SLS find is a rediscovery of the K0320 witness)

Lane: standard-board minimal-maximal size s_n, constructive upper-bound side for n = 12, 13
(K0026 / K0320 / K0312 / K0147 / K0148 / K0149 family).
Single-owner declaration: research/log/2026-11-21-s12-s13-minimal-maximal-upper-witness-single-owner-note.md
(commit 593a567a, 13:59Z).

## Scope of session 1 (what is claimed here and what is NOT)

Claimed (all finite-machine, all explicit):

1. **Census (third independent implementation)** of the forbidden-quartet structure
   for n = 5..13: primitive-direction maximal lines + canonical-reduced circle-key
   grouping of every non-collinear triple (circle equation x^2+y^2+Dx+Ey+F = 0 with
   the rational (D,E,F) reduced over Z to a unique key), C(m,4) decomposition per
   curve. Reproduces every published anchor exactly:
   F_5..F_13 (826 ... 252,362), D/C splits n = 9..13 (3,156/25,996 ... 27,340/225,022),
   line catalog sizes (n = 10: 154, 11: 232, 12: 326), circle catalog sizes
   (n = 10: 12,170, 11: 20,847, 12: 34,031), and the publish-grade internal
   consistency gate (every circle group of m points carries exactly C(m,3) triples).
   (records/census_check_n5_13.json: 9/9 rows, anchor issues 0.)
2. **All 7 published witnesses reproduce** under the new incremental machinery
   (K0031, K0038, K0320 n=11..15): safe and maximal on their own boards
   (records/witness_reproduce.txt). This validates the State engine (incremental
   quartet counters, coverage counters, violation counters) end to end.
3. **Cross-board transplant diagnostics (complete placement scans)**: for every
   published witness with n <= m, ALL D4-image x translation placements on the host
   board m (deduplicated by cell-set), with uncovered-cell counts, histograms, and
   the best (minimum-uncovered) placements (records/transplant_host1[2-5].json):
   - No placement of any published witness is maximal on a larger board than its
     origin (12 x 12, 13 x 13, 14 x 14, 15 x 15 hosts; the K0320 n=11..14
     witnesses at min-uncovered 4/13, 10/13 offer, resp., and the n=13..14-to-15
     minima 9 and 8). Zero-uncovered placements occur only for the witness on its
     own board (8 D4 self-images, sanity anchor).
   - The deep-witness K0320 family shows min uncovered 4 (11->12), 10 (12->13),
     9 (13->14), 8 (14->15): each n+1-board construction needs at least one added
     attack, consistent with the K0320 n-1 construction pattern (they added exactly
     one stone per board step).
   These are exact scans of the canonically-placed families (task sizes recorded),
   NOT nonexistence statements about other boards or other configurations.
4. **Complete local nets around the published 12/13-stone witnesses** (a hunt lane
   for a k-1-stone witness inside the witness neighborhood):
   - 12 x 12 around the K0320 11-stone witness: remove-1/add-0 (11), remove-2/add-0
     (55), complete remove-2/add-1 (55 pairs x 1,735 candidate configs): no 10-stone
     maximal safe set (records/nets_n12.json).
   - 13 x 13 around the K0320 12-stone witness: remove-1/add-0 (12), remove-2/add-0
     (66), complete remove-2/add-1 (66 x 2,457): no 11-stone maximal safe set
     (records/nets_n13.json).
   Exact scans, negative outcomes labeled as failed neighborhood searches.
5. **Complete 2-out/2-in neighborhood (2-swap) scans of the plateau states**
   (doubleSwapComplete in scripts/hunt.mjs): for a config S and every stone pair
   {s1,s2}, the candidate add cells are exactly those that can complete some uncovered
   cell of S\{s1,s2} (cnt==2 quartet completions and both cells of cnt==1 quartets);
   every 1-add and every unordered 2-add combination is checked.
   - 12 x 12, S = K0320-witness-minus-one-stone (the natural wall config, score 4 =
     4 uncovered cells, 130/134 empty cells blocked): 45 pairs, 6,099 1-add checks,
     413,100 2-add checks (15.4 s): no witness, no 9-stone subset, best score in the
     whole net = 4. S is a strict 2-swap local optimum of the exhaustion of the net.
     (records/probe2_wall_n12.json; restricted first-order probe: probe_wall_n12.json.)
   - 13 x 13, S = the SLS plateau config (score 6): 55 pairs, 8,781 + 699,600 checks
     (35.4 s): same strictness at score 6 (records/probe2_pl_n13.json).
6. **SLS positive controls on 12 x 12 at the feasible size k = 11: one genuinely new
   witness configuration, one rediscovery of the published witness**
   (the harness must be able to find known-feasible sizes):
   - W_b = [[6,0],[5,1],[6,2],[2,6],[7,6],[10,6],[2,7],[4,7],[9,7],[2,11],[5,11]]
     (found at ~45 s by the seeded run, seed 2024; the pre-reset record file was
     lost to an environment reset, config recovered from the session record and
     re-verified after rebuild)
   - W_c = [[5,1],[4,2],[5,4],[9,5],[0,6],[10,6],[4,7],[0,9],[4,9],[5,9],[11,11]]
     (found at 45.8 s post-reset, seed 5150; records/ctrl_k11_seeded.json)
   Both are verified by three independent systems (python integer-permutation
   4x4 determinants with full per-empty-cell certificates incl. canonical curve
   coefficients; Node BigInt Bareiss with a different column order; the quartet
   catalogue State): all report SAFE+MAXIMAL, 133/133 empty points blocked
   (records/verify_{py,mjs,state}_s12_11{b,c}.json + witness_s12_11{b,c}.json).
   **Lattice-isometry classification (records/classify_s12_11stone.json,
   scripts/classify.mjs + the independent anchor-enumeration check
   scripts/check_congruent.mjs): W_b IS the published K0320 n=12 witness
   (same board, 180-degree rotation (x,y) -> (11-x, 11-y), zero translation);
   W_c is NOT congruent to it (canonical-form keys differ, embedding search
   finds no map).** Therefore the session's net new configuration is W_c: the
   second known witness for s_12 <= 11 up to plane-D4 plus translation. W_b
   stands as an unseeded-scratch-independent SLS rediscovery of the known
   optimum, not as a new witness. The earlier in-session wording of this README
   and of K1206 ("second/third explicit witnesses") counted W_b as new and is
   corrected here and in the K1206/K1206-bullet revision of this session.
   Negative controls: removing one stone from W_b makes both verifiers reject
   (rc=1, 10 uncovered) in the predicted pattern (records/verify_{py,mjs}_negctrl.json).
7. **SLS bounded-negative records for the k = target hunt (witness finding only)**:
   - 12 x 12, k = 10: seeded runs (4 x 60 s + 1 x 100 s, ~413 s total incl. earlier
     probes) all plateau at score 4 and converge to the same D4/translation family
     (the K0320-witness-minus-one-stone basin); scratch runs (2 x 120 s, no useful
     seeds) plateau at score 8 with a different config type. No 10-stone witness
     found (records/sls_k10_v1_a.json, sls_k10_a.json, sls_k10_scratch_b.json).
   - 13 x 13, k = 11: 2 x 60 s runs plateau at score 6 (records/sls_k11_n13_a.json).
   NO nonexistence claim is made. The searches are bounded; the failure to find
   k = 10 on 12 x 12 also cannot be read as evidence for absence because the same
   engine needed seeds to re-find the feasible k = 11 (see the honest control
   records: ctrl2_k11_scratch.json = 3 x 35 s scratch k = 11 attempts all stuck at
   score 2; ctrl_k12_n13.json = scratch k = 12 on 13 x 13 stuck at score 2 - the
   engine is simply weaker without structural seeds at these depths).

NOT claimed: any s_11 value (a45a626d lane), any s_12/s_13 lower bound or exact
value, any s_n for n >= 14, any monotonicity statement, any asymptotic statement,
any reading of moves/evaluations/restarts as verdicts.

## Method notes

- Quartet semantics: forbidden quartet = 4 cells on one circle or one line
  (board-independent incidence); safe = no forbidden quartet inside S; maximal =
  every empty cell p is attacked, i.e. some triple T of stones with T + {p} on a
  common circle or line. Every cocircular quartet lies on a >= 4-point circle, so
  the curve catalogue (maximal lines, >= 4-point circles) generates the quartet
  multiset exactly once (quartetList asserts |Q| = F_n against the census totals).
- State engine: per-quartet stone counters, per-cell coverage counters (#quartets
  through the cell with >= 3 stones), violation and uncovered totals maintained
  incrementally per add/remove; every published witness and the two new witnesses
  pass it (and the geometry verifiers pass with it).
- Census crash-log (for reproducibility): two implementation bugs were found and
  fixed by the anchor gate during development: (a) horizontal direction family
  (a, 0) with a > 1 duplicated every row (D_7 counted 1,885 vs 660), (b) gcd(0,0)
  reduced to 1 instead of 0, making origin-centered circle keys non-canonical
  (2 extra "circles" of 4 quartets at n = 9, +2 to F_9). The published anchors
  catch both. The session also experienced one execution-environment reset
  (mid-session, after the first seeded k = 11 control); all scripts were rebuilt
  from the session record and all records in this directory were regenerated
  deterministically after the reset (the lost run is documented above in item 6).

## Files

- scripts/census.mjs — census + anchor verification + quartetList (CLI: number list)
- scripts/witnesses.mjs — the 7 published witnesses + D4-image enumeration
- scripts/hunt.mjs — Board/State engine, localNets (complete remove-2/add-1 etc.),
  transplant placements, SLS (sls), plateau probes (probe = completion-ordered
  restricted, probe2 = complete 2-out/2-in), witnesscheck mode
- scripts/verify_witness.py — integer-permutation determinant verifier with full
  per-empty-point certificates (attacking triple + canonical curve coefficients)
- scripts/verify_witness.mjs — BigInt Bareiss second verifier (different column
  order, different expansion)
- scripts/witness_reproduce.mjs — loads all 7 published witnesses (sanity gate)
- scripts/classify.mjs — lattice-isometry canonical form (plane D4 + translation) of a
  stone configuration; CLI prints canonical keys for K0320 n=11..15, W_b, W_c
- scripts/check_congruent.mjs — independent congruence check by explicit
  8-transform x anchor-translation embedding search
- witness_s12_11b.json / witness_s12_11c.json — the two 11-stone SLS finds
  (W_b: rediscovery of the K0320 witness; W_c: new configuration)
- records/ — all machine-readable outputs listed above

## Reproduction

node scripts/hunt.mjs board '{"n":12}'
node scripts/hunt.mjs nets '{"n":12}'
node scripts/hunt.mjs transplant '{"host":12}'
node scripts/hunt.mjs probe2 '{"n":12,"cells":[[6,0],[9,0],[2,4],[7,4],[9,4],[1,5],[4,5],[9,5],[5,9],[6,10]]}'
node scripts/hunt.mjs sls '{"n":12,"targetK":11,"budgetMs":75000,"runs":1,"seedMaxN":11,"seed":5150}'
python3 scripts/verify_witness.py witness_s12_11b.json
node scripts/verify_witness.mjs witness_s12_11c.json
node scripts/classify.mjs
node scripts/check_congruent.mjs
node scripts/census.mjs 5 6 7 8 9 10 11 12 13

Interpretation guards: moves/evals/restarts are not verdicts; every negative scan
above is a failed bounded search; the s_12 <= 11 / s_13 <= 12 bounds of K0320 are
not improved and not tightened here in either direction.
