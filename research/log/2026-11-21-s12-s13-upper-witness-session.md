# s_12 / s_13 constructive upper bounds, session 1 log (2026-11-21, ~14:00-15:00Z)

Lane: research/log/2026-11-21-s12-s13-minimal-maximal-upper-witness-single-owner-note.md
(declaration commit 593a567a, 13:59Z). This session: publication of session-1 experiments
and knowledge items. No branch, direct to main, per lane note.

## Commits (this session)

- 7ad490bc — experiment dir research/experiments/s12-s13-upper-witness-20261121/
  (README + scripts/{census,witnesses,hunt,verify_witness.py,verify_witness.mjs,
  witness_reproduce}.mjs + neg_ctrl.json + witness_s12_11b.json + witness_s12_11c.json).
  Byte-fidelity of all 10 files fetch-back verified immediately after push.
- 8b921f3c — records/ 27 machine-readable files (census anchors n=5..13, transplant
  host12..15, nets n12/n13, probe/probe2, SLS + honest scratch controls, 3-system
  witness verifications, negative control).
- 1bea1ff3 — knowledge items K1204 (census third implementation verification),
  K1205 (transplant full placement scans), K1206 (two new 11-stone 12x12 witnesses +
  complete nets + strict 2-swap optimality). K-numbers triple-checked free immediately
  before push (items dir probes empty, README grep empty, recent-commit scan; latest
  known item was K1203 at 13:36Z).
- (this commit) — session log.

Parallel traffic observed mid-session: n11 S5 frontier census/union lane declared and
published (6f858074..c20511db), four-row q4 lane declared (a423c2f0), s(q) wording
clarification (0a76535f). None touch the s_12/s_13 upper-witness lane; no conflicts.

## Session-1 results summary (published in the experiment dir + K items)

1. Census third implementation (canonical circle keys + Cramer, integer arithmetic):
   n = 5..13 all published anchors PASS (F, D/C splits n=9..13, line/circle catalog
   sizes n=10..12, circle-group triple-consistency gate). Two implementation bugs were
   caught by the anchor gate during development ((a) non-primitive horizontal directions
   duplicated rows -> D overcount, (b) gcd(0,0) mishandling -> non-canonical
   origin-centered circle keys); both fixed before any hunting. -> K1204 (verifies K0057).
2. All 7 published witnesses (K0031, K0038, K0320 n=11..15) reproduce under the new
   State engine. validates the whole machinery end to end.
3. Transplant complete placement scans (D4 x all fitting translations, cell-set
   deduplicated): no isometric copy of any published witness is maximal on a larger
   host board (min uncovered 4/10/9/8 for hosts 12/13/14/15; uncovered-0 placements
   are exactly the self-board D4 images). -> K1205 (related K0320, related K0149).
4. Complete local nets around the published 12/13-stone witnesses: remove-2/add-1
   complete scans (55x1,735 and 66x2,457) negative for 10-stone (12x12) / 11-stone
   (13x13) witnesses in that neighborhood. Labeled as failed bounded searches.
5. Complete 2-out/2-in scans of the two plateau states: the 12x12 score-4 wall
   (413,100 pair checks) and the 13x13 score-6 plateau (699,600) are strict local
   optima of their exhausted nets; no witness, no k-2-stone maximal subset.
6. Two NEW verified 11-stone maximal safe witnesses on 12x12 (W_b, W_c) — **this count
   was corrected by the addendum below: W_b is a lattice-isometric rediscovery of the
   published K0320 witness (same board, 180-degree rotation); W_c is the single net
   new configuration**, found by the
   SLS harness as positive controls for the feasible k, verified by 3 independent
   systems with full per-empty-point certificates (133/133 blocked), negative controls
   reject correctly. W_c is the second explicit witness configuration for s_12 <= 11
   (K0320's construction remains first and is not improved; W_b coincides with it).
   -> K1206 (supports K0320).
7. SLS bounded negatives: 12x12 k=10 seeded runs all plateau at score 4 in the same
   D4/translation basin; scratch at score 8; 13x13 k=11 at score 6. NO nonexistence
   claim. Honest weakness records: scratch runs cannot even re-find feasible k=11
   (12x12) / k=12 (13x13) at these budgets (score 2 basins).

## Acceptance conditions check (declaration 593a567a)

1. Census anchors reproduced before hunting: YES (9/9 PASS, see census_check_n5_13.json).
2. Every claimed witness verified by >= 2 independent verifier implementations with
   full empty-point certificates in machine-readable JSON: YES (3 systems for W_b/W_c).
3. Constructive-upper-bound-only wording: YES everywhere (K1206 explicitly "s_12<=11,
   not improved"; no lower bound / monotonicity / asymptotic claims anywhere).
4. Nets and transplant tables are finite scans with recorded task sizes, negatives
   labeled as such: YES.
5. Pushes byte-verified against pinned commit SHAs, latest main re-fetched before each
   push, no forcing: YES (7ad490bc fetch-back exact; 8b921f3c, 1bea1ff3 pushed after
   fresh HEAD checks; no conflicts encountered).
6. Finite-machine scope only; move/eval/restart counts are not verdicts: YES (recorded
   only as run metadata).

## Incidents

- One execution-environment reset mid-session (triggered by a 300+s bash call with
  parallel SLS runs). The first seeded k=11 control (seed 2024) found W_b but its
  record file was lost; the configuration was recovered from the in-chat record and
  re-verified in the rebuilt environment; W_c is a post-reset find (seed 5150).
  Script kit preserved at knowledge/kyouen-research/_s1213-lane-kit/scripts/ (refreshed
  with the probe2-era hunt.mjs at publication time, in this session).
- No push conflicts. n11/four-row lanes publishing in parallel were untouched.

## Handover to the next run

- s_12 <= 10 (12x12) and s_13 <= 11 (13x13) witnesses remain unfound. The score-4
  wall config's complete 2-swap net is exhausted (strict optimum), so future SLS
  effort should move to 3-swap neighborhoods, tabu/annealing schedules, or different
  seed families (e.g., circle-catalog-based constructions), not more restarts of the
  same policy.
- Canonical-form (D4 + translation) equivalence classification of {K0320 n=12 witness,
  W_b, W_c} is not done; a classification would tell whether the SLS is finding one
  basin or three. Cheap; recommended next.
- Transplant host=16 (does the K0320 n=15 witness give s_16 <= 14?) is intentionally
  not scanned (n >= 14 claims are outside this lane's declaration).
- All scripts runnable standalone: node scripts/hunt.mjs '{mode}' '{json}' from the
  experiment dir; census CLI takes an n list.

## Addendum (same session, ~30 min later): lattice-isometry classification + correction

The recommended-next task (witness equivalence classification) was executed in this
same session. Result, by two independent methods (canonical lex-min key over the 8
plane-D4 images with min-corner normalization, scripts/classify.mjs; and an explicit
8-transform x anchor-translation embedding search, scripts/check_congruent.mjs):

- **W_b IS the published K0320 n=12 witness**: the embedding is the same-board
  180-degree rotation (x,y) -> (11-x, 11-y), zero translation. Canonical keys equal.
- **W_c is NOT congruent to K0320's witness (nor to W_b)**: canonical keys differ,
  no embedding exists.

Therefore the earlier wording of this log's summary (item 6: "two NEW verified 11-stone
maximal safe witnesses ... second and third explicit witnesses") is CORRECTED: W_b is
an SLS rediscovery of the known witness (kept as a positive-control strength datum),
and the session's net new configuration is W_c, the second known witness for s_12 <= 11
up to lattice isometry. Corrections applied in the same session to: the experiment dir
README (item 6 retitled/rewritten), K1206 (retitled/rewritten, correction documented in
its body), and the knowledge README K1206 bullet (rewritten line). Machine-readable
classification record: records/classify_s12_11stone.json (canonical keys of K0320
n=11..15, W_b, W_c, pairwise tests, the found embedding, the corrected claim).

Additional commits (this session, correction):
- experiment dir README revision (item 6/Files/Reproduction retargeted) +
  scripts/classify.mjs + scripts/check_congruent.mjs +
  records/classify_s12_11stone.json + K1206 rewrite (title/body/relations corrected,
  correction documented in-body) + session-log addendum (this section; pushed
  together with the correction commit) + knowledge README K1206 bullet rewrite
  (line-1 rewrite of the bullet, byte-verified).

No other result of the session is affected: the census anchors, transplant scans,
nets, probe2 strictness, SLS negatives, negative controls, and W_c's 3-system
verification all stand unchanged.
