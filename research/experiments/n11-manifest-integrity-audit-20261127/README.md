# n11 manifest-integrity audit (2026-11-27)

Full-repo integrity sweep of every n11 experiment kit MANIFEST on main
(148 MANIFEST files under research/experiments/, fetched from the raw CDN
against the current git tree). Purpose: make every published sha256 pin
independently checkable, and find rows whose pinned sha no longer matches
the published bytes.

## Method

- scripts/manifest_fullsweep.py: resumable sweep. Inputs: the current git
  tree listing (tree2.json snapshot, not republished; regenerable via the
  GitHub git/trees API) and raw CDN fetches. Each MANIFEST data row is
  parsed as `sha256 [size] path`; the path is resolved kit-relative first,
  then repo-root. sha256 of the fetched bytes is compared against the pin;
  size is compared when the row carries one. Anomalies are logged to
  output/sweep-anomalies-raw.txt; completed MANIFESTs to
  output/sweep-manifests-done.txt (148 = all).
- Known false-positive classes (noise, NOT defects): 4-column
  `sha256 bytes git-blob-sha1 path` formats (class2251, b34win) and
  dual-sha formats (class20421, class34908) that the row parser cannot
  consume; cross-kit `sources/MANIFEST-*.txt` files whose kit-relative
  paths (README.md, output/status.log, ./input/...) resolve inside a
  DIFFERENT kit or the repo root (e.g. repo-root README.md 79,102B and
  output/status.log 500B) and are therefore pinned by their OWN kit's
  MANIFEST; `(UNPUBLISHED per size policy; pin only)` probe-worklist rows
  (intentionally unpublished, pinned only).

## Findings and repairs (all published in this session)

Real MANIFEST-row defects found and repaired:
1. n11-ninthcost-k12-win-thirdimpl kit: README row carried the
   third_impl.js sha and raw-row size column was wrong. Repaired in
   commit 6b34e8a6 (post-fix MANIFEST sha256
   aec78ad74b9806780a39285ea611d7ee85047c5f4ec289bba01ccb603dcafbb3).
2. n11-eleventhcost-k01-win-cppgate kit: scripts/kyouen_dfpn_root.cpp was
   truncated to 63,993B at publication (read cap); full 189,384B canonical
   bytes (sha256 9193f5b6... per the kit pin) republished in commit c931276a.
3. n11-centralreply-chain-integrity-tsaudit kit: README row was stale
   (sha of the pre-update 3,509B README). Updated to the current
   ca3fe97754b2a385f685188f8c8e73978f28bb1de2034729c500f42d7d4e2efc
   (4,809B), commit 32a58629.
4. n11-centralreply-evwin4-adoption-reaudit kit: single-hex transcription
   error in the scripts/compare_deltas_ev_adoption.py row
   (70a5b2077f57... -> 70a5b2078f57...), commit 32a58629.
5. n11-centralreply-sixthwin5-adoption-reaudit kit: single-hex
   transcription error in the output/increments-manifest.json row
   (...4644d4512... -> ...4634d4512...), commit 32a58629.

Publication gaps (MANIFEST references files never published to main;
verified 404 at the historical commits 783f6a2c/95586531/d0755ecc/
d4564f98/048b69c5 as well, i.e. not a casualty of any later removal;
disclosed as open items for the owner lanes):
- n11-centralreply-b39loss46-adoption-reaudit-20261125 references
  scripts/compare_deltas_ei_adoption.py from the (unpublished)
  n11-centralreply-b39loss46-adoption-20261125 kit.
- n11-centralreply-closure-class30484-cppgate-20261125: declaration.md
  (pinned b606b27d0993a8e8b997d295b7e34fa566760bf2b5cc0e8224505cd6ead4787d,
  8,428B) never published.
- n11-centralreply-closure-class34269-batch30-exh6-20m-20261124: 19 rows
  (raw/ac006..ac047 p1/p2/truncated outs + status.log) never published.

## Verdict status

The 11x11 empty board remains UNKNOWN. This audit consumed no verdicts and
changed no verdict-bearing content; node counts remain bookkeeping only.
