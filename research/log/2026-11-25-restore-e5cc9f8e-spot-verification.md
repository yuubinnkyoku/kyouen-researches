# 2026-11-25 Restore spot-verification of main after the 31/31 RESTORE chunk sequence (d0755ecc wipe recovery)

Lane: high-speed lane (this run). Document type: verification log, report-only.
This run did NOT restore, revert or rewrite anything; the restore was
executed by the owner. This document records an independent spot
verification of the completed restored tree, performed BEFORE this lane
resumed publishing to main.

## 1. Timeline (observed from the commit list)

- 16:02:12Z `d0755ecc` — accidental empty-index commit wiped all content
  except the pg2q8-cap-game experiment (incident report `dcc39bab`,
  16:08:57Z; nothing lost, full tree intact in history at `e5cc9f8e`).
- Published on the wiped tip afterwards (additive, byte pins verifiable):
  K1325 item + completion log `e3a2f749` (16:04:22Z), incident report
  `dcc39bab` (16:08:57Z).
- 16:34:26Z `5d3f64aa` — owner "TEST push capability (will be reverted)"
  commit.
- 16:44:20Z `e0655179` — owner RESTORE chunk 1/21 begins; restarted as
  chunk 1/31 at 16:53:00Z (`14de6150`); the 31-chunk sequence completes
  at 17:03:30Z with chunk 31/31 = 
  `567a84e41e62ac060faa4dae1bba5ed4d9095fd6`.
- 17:05:15Z `166ebb51` — owner close-out commit: "restore complete:
  e5cc9f8e6 content in stages (chunked pushes), add PG(2,8) orbit
  verification artifacts, remove push test file". The restore is
  DECLARED COMPLETE by the owner; the `PUSH_TEST_TMP.txt` residue
  (item 2.1 below) is removed here and the pg2q8-cap-game artifacts are
  formally re-added.

## 2. Spot verification performed by this run (tip = 567a84e4…)

All checks were run against the fixed tip sha, fetched via raw CDN
(tip and e5cc9f8e) and authenticated directory listings. Results:

1. ROOT TREE: the root listing at tip is IDENTICAL to `e5cc9f8e` (26
   pre-wipe entries, all present) with exactly ONE added entry at the
   moment of verification: `PUSH_TEST_TMP.txt` — the residue of the
   owner's test-push commit `5d3f64aa` ("will be reverted"). This lane
   flagged it and did NOT act on it; the owner removed it in the
   close-out commit `166ebb51` (17:05:15Z, "remove push test file"),
   which also formally re-adds the PG(2,8) orbit verification
   artifacts. Resolved by the owner before this lane's pushes.
2. BYTE PINS vs the pre-wipe commit `e5cc9f8e` (fetch both shas, cmp,
   sha256):
   - `AGENTS.md` — 3,993 B, sha256
     `f8b4f78f43ab1fc7d398e045795513879cafcd1bed8645e9b4d239a651d180d9`
     — BYTE-IDENTICAL to `e5cc9f8e` (and equal to the incident-report
     pin).
   - `research/knowledge/README.md` — 1,136,882 B, sha256
     `fee4f5d78260ba0b1818f29bd2122e6bf8db64eb93a8bab42ed34a8e7cb7a1db`
     — BYTE-IDENTICAL to `e5cc9f8e` (equal to the incident-report pin).
3. ADDITIVE POST-WIPE PUBLICATIONS present at tip (absent at
   `e5cc9f8e`, as expected), sha256 re-verified against the published
   pins:
   - `research/knowledge/items/K1325-strip-z17-min12.md` — 20,465 B,
     sha256 `f91e0b430725b1b0a566552b207e1de21b5b31e9cc776d4c5c29ca3a7637aa73` MATCH.
   - `research/log/2026-11-25-strip-z17-min12.md` — 7,542 B, sha256
     `3211a3812907b3d02a6f480c17b139430373b5f8cb2d862931a105e41b9280c5` MATCH.
   - `research/log/2026-11-25-main-tip-wipe-incident-report.md` —
     7,234 B, sha256
     `19b805d4b10faecf7b466b97a11d89587a0d3cd0f254ce6bca61596a6a2b9144`
     MATCH (the incident log published by the parallel lane at
     `dcc39bab`).
4. DIRECTORY-LISTING WINDOW IDENTITY: the first-1000-entry listings of
   `research/knowledge/items/`, `research/experiments/` and
   `research/log/` at tip are IDENTICAL to the `e5cc9f8e` listings
   (0 missing, 0 added inside the window; the listing surface caps at
   1000 entries per directory — see limits).
5. SELECTED INFRASTRUCTURE PROBES at tip: published kit directories
   `research/experiments/strip-z15-min10-20261125/` (6 files),
   `strip-z16-min11-20261125/` (7), `strip-z17-min12-20261125/` (7);
   `cpp/` (6 entries), `tools/` (3), `certificates/` (1), `Main.lean`
   (Lean 4 Kyouen module content fetched intact), `Kyouen/` module set
   per the Main.lean imports. All present.

## 3. Judgment and limits

- JUDGMENT (scope-limited): the restored main carries the pre-wipe
  ROOT, the pinned SSOT entry files byte-identical, the published
  additive post-wipe artifacts at their pinned bytes, and identical
  directory windows. This is sufficient for additive publishing to
  resume (this lane's z=18 census kit + logs are the first such
  additions, published on top of tip 567a84e4).
- LIMITS (disclosed, not hidden): this is a SPOT verification, NOT a
  full-tree byte equality proof. A 65k-file full-tree comparison was
  NOT performed: this environment has no recursive git-trees API
  surface and the directory listing caps at 1000 entries per
  directory. Files outside the probed set are verified only through
  the owner's own 31-chunk restore commits (each message asserts
  restoring e5cc9f8e content). A full byte-diff (recursive git trees
  of tip vs e5cc9f8e, expecting exactly the 3 additive post-wipe
  publications + PUSH_TEST_TMP.txt) is a cheap owner-side close-out
  check and is recommended.
- Honest note: during this run's local kit build the restore was still
  in progress; all published bytes consumed locally were fetched
  sha-pinned (`e5cc9f8e` and the per-publication commits) per the
  incident guidance. Nothing was pushed before the restore completed
  and this spot verification passed.

## 4. Standard caveats

This document makes no claim about any game position verdict. Standard
11x11 empty board, two-stone roots, S2, classes 1/2/4, and all
central-reply roots: all UNKNOWN, unchanged. The incident never
consumed any verdict and neither does this verification.
