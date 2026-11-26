# Part SQ completion: sixthwin3 WIN-only canonical adoption closes complete

Date: 2026-11-26 (long-term lane session).  This completion log closes
Part SQ (declaration log
research/log/2026-11-26-part-sq-sixthwin3-adoption-declaration.md,
commit 33f8f371).

## What closed

The canonical head of record advances cc3694bb -> 02db5ab3 at the
Part SQ kit path (merged-exact-s5-chain-plus-sixthwin3-20261126.cache,
6,801 rows WIN 201 / LOSS 6,600, 284,230 bytes; this Part publishes
the merged head itself, no pre-decl dossier).  Consumed: exactly the 2
unconsumed parked4rest2 L50M ladder exact-WIN rows k20
(10376293541461626880:33619968, s5 111843) and k33
(12682136550675320832:65536, s5 97791), adopted node total 32,038,980
(bookkeeping, never verdicts), adopt-eligibility re-verified live by
the maker and again by the extractor (parked4rest2 ladder kit
MANIFEST-verified file-by-file 26/26; Part SN C++ gate 28/28, 67/67
gates, GATE-PASS x2 passes per row; k20/k33 third-impl addendum
auditor re-run live rc=0 49/49 x2 deterministic), win_ties = [].

Measured (fail-closed, extractor-independent recount EXACT):
census 34,407/113/39/390 -> 34,405/115/39/390 with exactly the 2
unknown->excluded_now win-hit flips {2402 (1873498544497754112:0,
owner of k33), 3054 (1297037794341814272:0, owner of k20)}, no class
freed; serving class 3077 stays excluded_now (Part EW) with
cost-unknown 93 -> 91; owner classes 30156/6233 already excluded_now
at BASE and unchanged; closure churn 0 (804 -> 804, zero enter/leave,
zero unknown_now and rank churn), per-root coverage byte-identical,
update8 281 -> 281 (both adopted s5 indices 97791/111843 outside the
frozen baseline requirement), joint greedy 35,155 unchanged, worklist
64,276 unchanged.

Standing unconsumed (recorded, NOT emitted, in NO cache): the
still-parked k38 of the same probe selection (15M park-at-UNKNOWN, no
L50M follow-up claimed) and the 30 fifth-resumption verified LOSS
rows of the Part SL batch (no delegated C++ gate; coverage asymmetry
disclosed).

## Kit of record

research/experiments/n11-centralreply-sixthwin3-adoption-reaudit-20261126
(17 files pinned in MANIFEST-sha256.txt).  Increment 47f7dfb0...,
manifest 07181de7... (adopted-table digest d89ccfbb...), merged head
02db5ab3..., merge audits 622ac17f... x3 byte-identical, census json
8d8329d0..., decomp json 88cf5338... (schema
sixthwin3-decomp-deltas-v1), reaudit refresh-summary de205c31... /
closure-classes 350e269a... / per-root-coverage 9c5b2774...;
probe-worklist regen pin 24301312... (3,715,904 bytes) NOT published
per the size policy.

## Determinism, battery, publication verification

Maker 2 runs rc=0 byte-identical increment + manifest; measurer 2 runs
rc=0 byte-identical census json; extractor 2 runs rc=0 byte-identical
decomp json; merger 3 runs byte-identical.  Tamper battery:
increment-row WIN->LOSS flip, merge-audit mutation and manifest
mutation each fail-closed rc=1 with byte-verified restore; clean
control rc=0.  Waves A-D published to main with raw-CDN fetch-back
sha256 verification: all 16 content files (declaration log, 5 kit
scripts, 10 output/reaudit files incl. the 284,230-byte merged cache,
README, MANIFEST) byte-exact; no truncated push, no push conflict,
no parallel-run interference observed this session.

## Provenance note

This Part was rebuilt after a full local environment loss (session
timeout during a tamper battery batch) by deterministic reconstruction
from published-byte-verbatim inputs: the rebuilt maker reproduced the
pinned increment 47f7dfb0... and manifest 07181de7... bytes exactly,
the rebuilt refresh fork reproduced all pinned reaudit outputs
exactly (de205c31.../350e269a.../9c5b2774.../24301312...), and the
rebuilt measurer/extractor regenerated the census/decomp jsons with
every measured field identical to the pre-loss recorded values.  One
corrected pin during rebuild: the k20 cold verify-legal third-impl
witness sha (bd6d..., transcribed bd4d in the first rebuild, caught by
the maker's fail-closed byte gate on first run).  The census/decomp
json shas of record are 8d8329d0.../88cf5338... (the pre-loss local
transcripts were not byte-reproducible after the loss; all measured
values are identical).

## Verdict scope

WIN-only canonical adoption asserts NO root verdict, frees no class
and makes no coverage claim.  The standard 11x11 empty board and
every central-reply root stay UNKNOWN.  Nodes are bookkeeping, never
verdicts.
