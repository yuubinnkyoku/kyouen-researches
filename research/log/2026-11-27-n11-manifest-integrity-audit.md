# 2026-11-27 n11 manifest-integrity audit (full 148-MANIFEST sweep)

Lane: long-term 11x11 lane (session on GitHub raw/CDN + connector only; user PC
unreachable this run). No branch/PR; direct main publication per repo policy.

## What was done

Completed the full integrity sweep of every n11 experiment kit MANIFEST on
main: 148 MANIFEST files under research/experiments/, all rows re-verified by
sha256 against the published bytes via the raw CDN (kit-relative path
resolution first, repo-root fallback). Raw anomaly log and the sweep script
are published in research/experiments/n11-manifest-integrity-audit-20261127/.

## Repairs published this session

- 6b34e8a6: ninthcost k12 third-impl kit MANIFEST stale rows fixed.
- c931276a: eleventhcost k01 cppgate kit truncated kyouen_dfpn_root.cpp
  (63,993B -> full 189,384B canonical, sha256 9193f5b6... matches the kit pin)
  republished.
- 32a58629: tsaudit README row updated to the current README sha
  (ca3fe977..., 4,809B); evwin4 and sixthwin5 reaudit MANIFEST single-hex
  transcription errors corrected (12th hex 7->8 in
  70a5b2078f57..., and 4644->4634 in a7376780687f...ba86). All fetch-back
  verified against commit-pinned raw bytes.

## Publication gaps disclosed (open items for owner lanes, not repaired here)

- n11-centralreply-b39loss46-adoption-20261125 kit: never published to main;
  its reaudit kit references scripts/compare_deltas_ei_adoption.py.
- n11-centralreply-closure-class30484-cppgate-20261125/declaration.md
  (pinned b606b27d..., 8,428B): never published.
- n11-centralreply-closure-class34269-batch30-exh6-20m-20261124: 19 raw
  rows (ac006/ac013/ac032/ac036/ac044/ac047 p1/p2/truncated outs +
  status.log): never published.
All three are 404 at every historical commit checked
(783f6a2c/95586531/d0755ecc/d4564f98/048b69c5), i.e. never-on-main rather
than removed later.

## Noise classes (not defects)

4-column git-blob formats (class2251, b34win), dual-sha formats (class20421,
class34908), cross-kit sources/MANIFEST-*.txt path resolution, and
"(UNPUBLISHED per size policy; pin only)" probe-worklist rows.

## Status

11x11 empty board: UNKNOWN (unchanged). No verdicts consumed; node counts
remain bookkeeping only. The parallel twelfth-cost lane published its
ladder pre-audit kit (785f80ff) before wave B; wave B results not yet on
main at the time of this entry.
