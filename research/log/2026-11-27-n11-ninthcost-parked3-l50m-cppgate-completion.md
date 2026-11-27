# 2026-11-27 n11 ninth-cost parked-3 L50M rows C++ scrutiny gate: completion

Wave A declaration: commit 30c7a43a
(`research/log/2026-11-27-n11-ninthcost-parked3-l50m-cppgate-declaration.md`).
Kit + run record: commit ca255659
(`research/experiments/n11-ninthcost-parked3-l50m-cppgate-20261127/`,
30 files, MANIFEST-sha256.txt 29 pins).

## Outcome

Official execution 12:42:43Z-12:50:10Z (pre-registered order,
publish-then-execute honored), **6/6 GATE-PASS node-exact**:

- anchor-at2m GATE-PASS 98,2000000,0,2000000
- anchor-aj001 GATE-PASS 84,30000000,2,5156075
- anchor-af039 GATE-PASS 89,30000000,2,19234232
- k02 GATE-PASS 87,50000000,1,18123017 (WIN side)
- k04 GATE-PASS 98,50000000,2,24309957
- k07 GATE-PASS 96,50000000,1,27621128 (WIN side)

The pinned C++ second implementation (source 9193f5b6 @154f3b7a,
headers 5976935d / 2e36d694 byte-verified, zig 0.13.0 tarball
d45312e6 byte-verified, -std=c++20 -O2) reproduces the published L50M
verdicts of all three cold pairs node-exactly, including the two
WIN-side rows (4th and 5th WIN-side gate rows of the lineage).

Audit: batch audit PASS, 3 runs byte-identical (sha256 3155fe03...).
Tamper battery 4/4 fail-closed (T1 expected-pin flip k02 -> G0+G3 /
T2 raw k02.p1 nodes edit -> G2+G3 / T3 phantom GATE-PASS -> G4
passes=7/6 / T4 head byte append -> G6:head-sha) + clean control rc=0
(scratch copies only). Audit G6 re-verified the canonical head
0935c94c (6,875 rows WIN203/LOSS6672) with all three [lo,hi] absent.

## Honest disclosures

- Publication defect, caught and corrected within the session: the
  first kit push (3fe864e3) was made by a kit-assembly tooling bug that
  pushed three directory-listing bytes as files named `input`, `output`,
  `scripts` instead of the real subtrees (29 real files missing). The
  three bogus files were deleted by explicit commits and the full
  correct kit republished as ca255659. No kit byte differs between the
  intended kit and the republished one; the declaration, the run, and
  all pins predate both pushes.
- Pre-declaration host sanity run anchor-at2m @2M (published anchor
  budget only) is disclosed in the declaration; no target-row pass ran
  before the declaration push.
- Waves B (kit) and C (outputs) were combined into the single
  publication ca255659 after the wave-A declaration; the official run
  happened between the two pushes, in the pre-registered order.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Pillar status after this Part

ALL twelve resolved ninth-cost rows (9 LOSS + 3 WIN) now have 3/3
implementation pillars (replica cold pair + C++ gate + third impl):
k01/k03/k05/k06, k08/k09/k10/k11, k12 (15M stage) and k02/k04/k07
(50M stage). The whole ladder is adoption-eligible as a set; the
adoption Part (fresh single-owner declaration, WIN/LOSS conflict
review, merger 90711961, BASE 0935c94c, flip-census review for the
three WIN rows k12/k02/k07 per the SZ/EM/k05 precedent) remains OPEN
and is the next lane step.

Verdict NOT consumed: no cache increment, no class-status change, no
coverage claim, no adoption. Standard 11x11 empty board UNKNOWN; all
19 central-reply roots UNKNOWN; two-stone root {60,27} UNKNOWN;
third-move pair {100,108} UNKNOWN; every closure class UNKNOWN unless
a published Part says otherwise. Nodes are bookkeeping.
