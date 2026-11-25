# n11 S5 true-vs-adaptive cost re-measurement - single-owner declaration (2026-11-21)

Single-owner lane. Measurement only: no solver run, no cache write, no key claimed.
Scope: re-run of the true-vs-adaptive cost measurement requested as a next-step
coordination item by the third-cost session log (commit 047d3d51,
research/log/2026-11-21-n11-class1297036830122704896-exclusive-s5-session.md):
"Re-run the true-vs-adaptive cost measurement against the 63 remaining unknowns of
this class before spending more budget". This lane consumes published pinned bytes
only, emits scheduling hints only, and touches no other lane's files.

## Pin-level finding recovered during re-measurement (no new claim)

The 15 rows censored at the 2M row stage of the pinned reconciliation-findings.json
(reply27 cohort) are all RESOLVED inside the probe-13 base pin 60e0dc34
(merged-exact-s5-after-js-probe-13.cache): 15/15 verdict LOSS, true cost
3,651,923-12,626,043 nodes. The 13-probe campaign continued past row publication and
resolved them. The row-era censoring is superseded; the 15 keys are recovered as the
new cohort `reply27_late` with strict machine-gated disjointness from every other
cohort (reply27 / thirdcost / fourthcost) re-verified fresh from bytes.

## Planned publication (this session)

research/experiments/n11-s5-true-vs-adaptive-remeasurement-20261121/
- README.md (method, pins, headline results, guards)
- scripts/pub_paths.py (dual-layout resolver: published repo / authoring kit)
- scripts/measure_tva.py (674 fail-closed gates, deterministic output)
- output/measurement.json (schema n11-s5-true-vs-adaptive-remeasurement-v2,
  sha256 2ec25636987efc0a5b57ade2cc0eddbade1ee23653527ca85b64c6b54ccedc22)

plus this declaration note and a session log in research/log/.

## Pins (all sha256-gated fail-closed inside the measurement script)

- research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz
  146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54
- research/experiments/n11-strategy-redesign-20261010/output/historical-cost-profile.json
  6b2971e53059ac36af7bf161a61d90d65f85e604e27b93d013e7a2853fdceddc
- research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/post-probe/shared-s5-tasks.csv
  31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954
- research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/post-probe/candidate-classes.csv
  2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80
- research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache
  60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6
- research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/output/merged-exact-s5-after-class-excl-1.cache
  bb4495e0586404876db05856c5b8573c62361dadd826b6f68f6f8cae611190b0
- research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/output/exclusive-selection.json
  ef048309b3bd3ae3134c583374712e0c6aff64175006879063995c0eaeafafb7
- research/experiments/n11-s5-frontier-census-20261121/output/reconciliation-findings.json
  a93d87dc436f28ffea63760c766178a55af259f545884a8557300f7eb7e2e9cb
- research/experiments/n11-fourthcost-class-s5-exclusive-probe-1297107061427929088-20261121/output/fourth-cost-exclusive-keys.json
  b9f4d9419e5f9edf5b97c6867568a30b3ac149811edeb4c98ef5ec0fcd9bbb6a
- research/log/2026-11-21-n11-fourthcost-exclusive-probe-pass1-complete.md
  96ad1dfebbe4ef0b7105f8236abe340bc357e37367ea6b5f13a2aa410e20cd0e
- research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py
  954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f
- research/experiments/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py
  78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2

## Claim hygiene

- No key claimed, no probe launched, no cache write, no other lane's file touched.
- The 2 single-live-parent unknown children of 1297036830122704896:0 are recorded in
  the allocation table with `claimed_by` = parked-pair L50M ladder lane (single-owner
  declaration commit b1a38144); they appear here as scheduling rows only.
- No K item and no knowledge-README bullet (measurement-lane precedent: frontier
  census 2026-11-21).
- No branch/PR; direct to main per lane policy; the HEAD-before-push of each commit is
  recorded in its commit message; fetch-back byte verification after each push.

## Status guard

The standard 11x11 empty board remains UNKNOWN. The two-stone root {60,27} and both
remaining third moves 100/108 remain UNKNOWN. `1297036830122704896:0` remains UNKNOWN
(44 LOSS / 63 unknown / 107 children). Node counts, proxy values, ratio estimates and
allocation ranks are never verdicts, never authorize skipping any key, and claim no
resolution probability.
