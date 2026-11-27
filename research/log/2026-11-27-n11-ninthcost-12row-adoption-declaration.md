# 2026-11-27 n11 ninth-cost 12-row canonical adoption: single-owner declaration (wave A)

## Claim

This lane claims the ninth-cost canonical adoption Part: the canonical
head of record advances from
`merged-exact-s5-chain-plus-eighthcost-k01-20261127.cache` (sha256
0935c94c03a9a3fbdf2a55aca90bb986a019dfd26c0097ab2c75709d590e9ca4,
6,875 rows WIN 203 / LOSS 6,672, 287,808 bytes) by consuming exactly
the 12 published ninth-cost rows (9 LOSS + 3 WIN), all of which now
have 3/3 implementation pillars.

Single-owner: no other lane has declared a ninth-cost adoption Part
(main HEAD at push time is dace530b, commit list machine-checked; the
SZ 42-row and eighth-cost k01 adoptions are prior, disjoint Parts).

Publish-then-execute: this declaration is pushed before the maker or
merger runs on this host. No cache increment, merger run, or manifest
for these rows has been made by this lane before this push.

## Adopted rows (all pillars published on main; freshness machine-checked)

| key | s5 state (lo,hi) | legal | verdict | budget | nodes | pillars |
| --- | --- | --- | --- | --- | --- | --- |
| k01 | 1297036692683751424, 134283264 | 89 | LOSS(2) | 15M | 2,163,556 | 4loss gate + 4loss third-impl |
| k03 | 1297036761403228160, 134217728 | 86 | LOSS(2) | 15M | 7,753,840 | 4loss gate + 4loss third-impl |
| k05 | 1152921504624672768, 536903680 | 91 | LOSS(2) | 15M | 8,687,533 | 4loss gate + 4loss third-impl |
| k06 | 1152923703764321280, 68719476736 | 99 | LOSS(2) | 15M | 8,130,387 | 4loss gate + 4loss third-impl |
| k08 | 1152956688979984384, 536903680 | 98 | LOSS(2) | 15M | 3,306,768 | 4lossrest gate + 4loss-rest third-impl |
| k09 | 1224979098645823488, 536903680 | 92 | LOSS(2) | 15M | 4,711,230 | 4lossrest gate + 4loss-rest third-impl |
| k10 | 1297036692683751424, 134217730 | 96 | LOSS(2) | 15M | 5,542,083 | 4lossrest gate + 4loss-rest third-impl |
| k11 | 1297036692683751424, 134217744 | 97 | LOSS(2) | 15M | 5,931,960 | 4lossrest gate + 4loss-rest third-impl |
| k12 | 1297036692683751424, 134217792 | 92 | WIN(1) | 15M | 14,521,862 | k12 gate + k12 third-impl |
| k02 | 1297036692683751424, 201326592 | 87 | WIN(1) | 50M | 18,123,017 | parked3-L50M gate + parked3 third-impl |
| k04 | 1152921504607903744, 536903680 | 98 | LOSS(2) | 50M | 24,309,957 | parked3-L50M gate + parked3 third-impl |
| k07 | 1152923703765368832, 68719476736 | 96 | WIN(1) | 50M | 27,621,128 | parked3-L50M gate + parked3 third-impl |

Census: 12 rows, WIN 3 (k12/k02/k07), LOSS 9, adopted node total
130,803,321 (bookkeeping). All 12 (lo,hi) pairs are ABSENT from BASE
0935c94c (fresh-increment gate, machine-checked 12/12 on this host
before this push); with 12/12 absent the WIN/LOSS conflict review is
vacuously clean (no key can conflict with a BASE verdict); no
duplicates (machine-checked).

## Pre-registered execution policy

- Maker: fresh single-owner maker
  `make_kit_ninthcost12_adoption_20261127.py`, structural descendant
  of the published Part SZ maker (sha256 d4949f71-lineage
  make_kit_sz_adoption_20261127.py): G0 anchor byte gates (BASE head
  0935c94c, merger 90711961, quarantine 81d23160, policy 78655e94,
  frozen graph 54f9c364), G1/G2/G3 pillar gates: the four C++ gate kits
  (n11-ninthcost-4loss-cppgate / -4lossrest-cppgate / -k12-win-cppgate
  / -parked3-l50m-cppgate, every MANIFEST file byte-verified, every
  audit_gate.py re-run LIVE rc=0 with N9_HEAD) and the four
  third-impl corroboration kits (every MANIFEST file byte-verified,
  verdict-level agreement re-derived from the published raws; the
  ninth-cost third-impl kits carry no audit script, so no live audit
  re-run exists for them - DISCLOSED structural deviation from Part
  SZ, which had a live audit_sy.py), G4 the 12 adoption pins re-derived
  against the published gate-rows expected quadruples and the
  third-impl raw result fields, G5 freshness 12 / WIN-LOSS conflict 0 /
  duplicate 0 / quarantine-free / canonical-safe per s5_evidence_policy,
  G6 increment emit (12 rows, WIN rows emit result=1), G7 manifest.
  Two-run byte-identical requirement.
- Merger: the pinned union merger `s5_union_merge.py` (sha256
  90711961...) applied BASE + increment, three runs, byte-identical,
  with the merger's own fail-closed audit records. Pre-registered
  merged shape: 6,875 + 12 = 6,887 rows, WIN 203 + 3 = 206,
  LOSS 6,672 + 9 = 6,681, name
  `merged-exact-s5-chain-plus-ninthcost12-20261127.cache`.
- Flip-census review for the three WIN rows (k12/k02/k07) is NOT part
  of this Part: per the SZ wave E / k05 precedent it is a separately
  declared reaudit+census Part that must run against the new head
  before any class-status use of the WIN rows. This Part admits
  solver-trusted cache rows only and consumes NO root verdict, frees
  or excludes NO class.

## Freshness basis

Canonical head of record at declaration time: sha256 0935c94c...
(6,875 rows WIN 203 / LOSS 6,672, 287,808 bytes), fetched and
byte-verified on this host; 12/12 adopted pairs machine-checked ABSENT.
No other adoption Part is open.

## Guards

Verdict NOT consumed. Adoption of solver-trusted S5 cache rows only:
NO root verdict, NO 11x11 outcome, NO class freed, NO class excluded.
The standard 11x11 empty board, all 19 central-reply roots, the
two-stone root {60,27}, its remaining third moves {100,108}, S2, class
1/2/4 and all closure classes stay UNKNOWN. WIN(1)/LOSS(2) S5 raws
are not class closure claims, not root verdicts, and transfer nothing.
Nodes are bookkeeping, never verdicts. This lane runs without access
to the user's computer (scheduled task); publication is via the
GitHub API only.
