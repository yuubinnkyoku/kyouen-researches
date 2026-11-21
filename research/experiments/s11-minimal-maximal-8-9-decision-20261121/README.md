# s11 minimal-maximal decision lane, session 1: census, encoding, control ladder (interim — decision runs INDET)

Lane: standard-board minimal-maximal size s_n (K0026 / K0312 / K0147 / K0148 / K0149 family).
Single-owner declaration: research/log/2026-11-21-s11-minimal-maximal-8-9-decision-single-owner-note.md
(commit a45a626d). This directory is the working record of the declared lane, session 1.
**No verdict on s_11 is claimed in this snapshot**: at freeze time every (11, k) decision run is
INDET (see records/kissat_inprogress_snapshot.txt). The bound remains 8 <= s_11 <= 10 (K0312 + K0320).

## Scope of session 1 (what is claimed here)

1. **Independent census of n=5..12 grids** (System A, exact Fraction/integer arithmetic):
   maximal 4+-point lines and nondegenerate 4+-point circles; F_n = D_n + C_n quartet counts.
   All published anchor values reproduced exactly (see "Calibration" below). The previously
   unpublished n=10/11/12 D/C splits and catalog statistics are published into K0057.
2. **Second implementation of D_n** (scripts/d_count.py): primitive-direction ray enumeration,
   no circle machinery at all. Agrees with the catalog census on D_5..D_12, including all
   published anchors (660 / 1,524 / 3,156 / 17,154).
3. **Third implementation of the >=12-point-circle counts** (scripts/big_circle.py):
   half-lattice center scan with scaled-integer distance histograms, no quartet enumeration.
   Agrees with census circle histograms: n=9: 4, n=10: 9, n=11: 21, n=12: 42 (with the 42 =
   {12:37, 14:4, 16:1} split matching). Includes the first catalogued 16-point lattice circle
   in the n=12 grid: center (5.5, 5.5), r^2 = 65/2, i.e. (2x-11)^2 + (2y-11)^2 = 130 = 9^2+7^2 = 11^2+3^2.
4. **Fixed SAT encoding (gen_cnf.py v2)** of "exists maximal safe S with |S| <= k" on n x n
   (safety = at-most-3 per forbidden quartet; maximality cover clauses over curve 3-subsets;
   sequential at-most-k counter). v1 had a self-reference bug in the counter (s[(i,j)] read
   where s[(i-1,j)] was intended); v2 is deterministic with md5-pinned CNFs for every instance.
5. **Control ladder, all PASS** (pinned kissat 4.0.4, md5 3a5eba830aa6008a604fcc9bbe99a325):
   - n=5: k=4 UNSAT (rc 20) / k=5 SAT (rc 10)  — s_5 = 5 (K0030).
   - n=7: k=6 UNSAT (71s, conflicts 798,605) / k=7 SAT (14s) — s_7 = 7 (K0031). The k=7 SAT
     model independently rediscovered the K0031 published witness stone set (verify_geom VALID).
   - n=9 both sides (k=8 UNSAT / k=9 SAT) queued in the driver (control for the published s_9 = 9
     row); at freeze not yet reached.
6. **Clause-level positive/negative controls, solver-independent** (scripts/cnf_check.py, records/
   cnf_control_check.txt): K0320 10-stone witness satisfies all 523,640 clauses of the n=11 k=10
   CNF literally (positive control for the encoding); its 9-stone subset violates exactly 17 cover
   clauses (negative control); K0031 witness satisfies all 40,311 clauses of n=7 k=7 and violates
   exactly the single cardinality unit clause of n=7 k=6.
7. **Local witness hunt, negative** (scripts/hunt_fast.py, records/hunt_snapshot.*): around the
   K0320 witness, all remove-1 nets (10 subsets) are non-maximal and the remove-2/add-1 net
   (45 stone pairs x ~113 candidates = 5,085 candidates) contains no 9-stone maximal safe set.
   This is a failed search inside a small neighborhood, **not** a nonexistence proof; distance >= 3
   remains unexplored.
8. **Fundament encoding lemma** (gen_cnf.gen_fund): appending the single clause "some stone lies
   in the D4 orbit transversal F of the board cells" (|F| = 21 for n=11) is equisatisfiable with
   the plain instance. (<=) clause-erasure is trivial; (=>) any solution S is nonempty (maximality
   fails for S = empty since cover clauses need a triple of stones), D4 maps lines to lines and
   circles to circles preserving incidence and cardinality, and F meets every cell orbit, so some
   g in D4 maps a stone of S into F and g(S) satisfies every clause. Used to accelerate SAT-side
   runs only; UNSAT results would also transfer by equisatisfiability, but any SAT witness will
   still be verified by geometry before any claim.

## Calibration table (published -> recomputed)

| quantity | published source | this session |
|---|---|---|
| F_5..F_12 | K0057 (0,1,14,194,826,2491,6364,14564,29152,54441,95670,158426) | all matched |
| D_7, D_8, D_9 | K0057 (660, 1,524, 3,156) | matched (2 implementations) |
| D_12 | K0057 f-n-13-16 extension (17,154) | matched (2 implementations) |
| C_12/n^5 ~ 0.568 | K0057 ratio note | 141,272/248,832 = 0.56800 matches |
| n=12 line sensor | K0057 machine-readable (326) | matched (326) |
| n=9 catalog 12-point circles | K0061 (4) | matched (third implementation) |
| s_5 = 5, s_7 = 7 | K0030 / K0031 | controls PASS (kissat + cnf_check) |

New (previously unpublished) values published into K0057: D_10 = 5,928, C_10 = 48,513,
D_11 = 10,428, C_11 = 85,242, C_12 = 141,272; catalog size hists for n=10..12 (see records/).

## Files

- scripts/: census_a.py (System A catalog census), d_count.py (D_n second implementation),
  big_circle.py (big-circle third implementation), brute_n.py (from-scratch Fraction geometry,
  n<=7 enumeration cross-check), verify_geom.py (fast stone-triple-transport witness verifier),
  gen_cnf.py v2 + gen_fund (CNF builder; deterministic, md5-pinned outputs), cnf_check.py
  (clause-level constructive satisfiability checker), hunt_fast.py, driver.sh (kissat ladder).
- records/: cnf_md5_pins.txt (binary + all instance pins), kissat_controls_summary.txt
  (verdict lines and run statistics of all control runs; full solver logs are bit-reproducible
  from the pinned binary + pinned CNFs and kept as trimmed records in follow-up commits),
  cnf_control_check.txt (clause-level controls), census_catalog_n10.txt (fresh n=10 census),
  census_catalog_n10_12.txt (fresh n=10..12 census; appended in a follow-up commit when the
  background run completes),
  d_count_v2_output.txt (anchor MATCH lines), big_circles_scan.txt (n=5..12),
  kissat_inprogress_snapshot.txt (decision-ladder freeze state, all INDET),
  hunt_snapshot.json / hunt_snapshot.out (negative neighborhood hunt).

## Interpretation guards

- Everything here is finite-machine work on explicit boards; no asymptotic claim about F_n/C_n
  beyond K0057's finite table, no claim about s_12 or higher, and no monotonicity claim beyond
  what a future (11, k) verdict literally decides (K0149 remains open as of this snapshot).
- Timeout / cut runs are recorded as partial (n11_k10 default mode: 470s, conflicts 8,246, cut by
  the foreground cap; superseded by the background driver run whose freeze state and, for
  finished runs, trimmed logs are the published record forms).
- nodes/conflicts counts are not win/loss statements; a missing verdict is INDET.
- Session environment: 3 execution-environment resets during the session; all canonical scripts
  and records were snapshotted to owner storage after each reset and re-derived deterministically
  (CNF md5 pins survived all rebuilds byte-exactly, which is the strongest available evidence of
  reconstruction fidelity).
