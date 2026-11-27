# n11 ninth-cost 4 LOSS row third-implementation corroboration declaration (wave A, publish-then-execute)

Date: 2026-11-27. Lane: long-term (11x11 weak-solution lane). This Part is
the third-implementation corroboration pillar for the four ninth-cost
15M-stage LOSS rows of the exclusive S5 probe class
`1297036692683751424:134217728` (wave C6, commit 95883e09) - the same
four rows whose C++ second-implementation scrutiny gate just published
GATE-PASS node-exact (kit n11-ninthcost-4loss-cppgate-20261127,
commit 652e19f7). Single-owner claim: no other lane has corroboration
raws for k01/k03/k05/k06 of the ninth-cost batch at declaration time
(the concurrent k12 WIN-row corroboration kit
n11-ninthcost-k12-win-thirdimpl-corroboration-20261127 is disjoint).

## Pre-registered targets and protocol

Standing third implementation `third_impl.js` (pinned sha256
08ea958f..., byte-clone of the published k12 corroboration kit copy,
byte-verified on this host). Protocol per the seventh-cost SY batch and
the k12 precedent: `--cap=400000000 --wallcap=260 --memo-power=22`,
two fresh cold passes per key (one node process per pass, cold), row
name = key, stones=5, legal = the published legal counts. The node
process exit code is captured directly by the shell in the same command
(`node_rc=$?` trailer).

Targets (replica at15m cold pairs, published wave C6):

- k01 `1297036692683751424:134283264`, legal 89, replica LOSS(2) nodes 2,163,556
- k03 `1297036761403228160:134217728`, legal 86, replica LOSS(2) nodes 7,753,840
- k05 `1152921504624672768:536903680`, legal 91, replica LOSS(2) nodes 8,687,533
- k06 `1152923703764321280:68719476736`, legal 99, replica LOSS(2) nodes 8,130,387

Expected (pre-registered): each key reports result 2 (LOSS) in both
passes with reason clean and mutually identical expansions; cross-
implementation node/expansion equality is NOT expected (the replica
nodes and the third-impl expansions are different counters; both are
bookkeeping). The `legal` field must equal the published legal count.

## Acceptance

CORROBORATION-PASS (verdict-level) iff all 8 passes (4 keys x 2 cold)
report result 2, reason clean, node_rc=0, legal == published, and the
two passes per key are mutually expansions-identical. Any INDET
(runlimit:cap), crash, node_rc!=0, or per-key pair disagreement: honest
negative, published as such, no retry-until-match.

No verdict is consumed. No cache increment, no class-status change, no
coverage claim, no adoption. This Part adds the third pillar for the
four rows; adoption of any ninth-cost row stays a separately declared
Part under the parent batch's WIN/LOSS conflict policy. The standard
11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN.
S2, class 1/2/4 and all closure classes: UNKNOWN. Nodes and expansions
are bookkeeping, never verdicts.
