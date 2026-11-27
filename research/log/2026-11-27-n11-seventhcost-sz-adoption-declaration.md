# n11 Part SZ declaration: seventh-cost 42-row adoption into the canonical head (wave A)

Single-owner declaration, publish-then-execute. HEAD at declaration:
36cb3ab720bbfe8d369be41e4e94873c1fa4a1b3 (Part SY wave C third-host
corroboration completion). Counter-probe clean at this HEAD: no
seventh-cost adoption declaration, kit or note of any kind exists on
main for these rows (checked immediately before this publication).

Scope: adopt ALL 42 published seventh-cost rows into the canonical head
of record 42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4
(merged-exact-s5-chain-plus-sixthlossk38-20261126.cache, 6,832 rows
WIN 201 / LOSS 6,331), producing the next canonical head:

- the 41 LOSS rows k01..k42 minus k05 (published Node replica cold
  pairs, 39 rows at the 15M stage, k16/k17 at the 2M stage), and
- the single WIN row k05 1152921504607932416:536870912 (published
  at50m cold pair WIN(1) ff750cc6 x2).

Adoption eligibility, all re-verified on this host before this
declaration (this session, independently re-fetched from main):

- Part SW C++ gate kit 145/145 files sha256-verified against its
  MANIFEST (MANIFEST sha256 09a8bca07a468a0e63899d8b27bd5d6f154dea449f
  d7e23b33e07b778c66a05f), gate-rows.json sha256 24c74bc289cac2d21c5b1
  ae8931207496e2682aa7c80a7fe199f6bf2437e9f5a, C++ gate 44/44 GATE-PASS
  previously published;
- Part SX C++ gate kit 24/24 files verified (MANIFEST sha256 68f91473
  d27edf227bb8ed8f9a95dedd866a2162d9017881058d41433e9570d0), gate-rows
  .json sha256 306030a78972725a4b45388e465c8b5f2dc933168c8fb07423e225d6
  9b0421bc, C++ gate 4/4 GATE-PASS; the k05 input csv (sha256 a73a6c70
  a221619b94ce29c188434d24a1f8af43653b37c1019a3286ba2ddb91) re-derived
  byte-exactly from the published SX gate G1 detail;
- Part SY third-implementation corroboration kit 143/143 files verified
  (MANIFEST sha256 366771ff974b9826969cb05c4be6b3391ef0664e64ca82a51c5a
  f5e6b19763e0, gate-rows.json sha256 fc8fc5c2a6532b4179a1182c85f8ed64
  cffa65f207b7eed59c744a04e1f9a10), wave C third-host corroboration
  audit published at HEAD 36cb3ab7;
- the 42 adoption pins re-derived independently from the published
  SW/SX gate-rows.json expected quadruples and replica_verdict fields:
  42/42 exact match, 41x LOSS(2) + k05 WIN(1), replica node total
  227,552,924;
- freshness and conflict against the base head of record, checked
  locally on the byte-verified base cache (42dbb58f, re-fetched as
  ballast this session, byte-identical): all 42 (key,occup) pairs
  absent from the base (freshness 42), WIN/LOSS conflict 0, duplicate 0.

Frozen provenance pins carried unchanged from the parent batch:
quarantine.json 81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc6
7d17fe9, s5_evidence_policy.py 78655e94480920de48a6fe8792e02e611513ddee7f
685b422bbb2b08af5c95e2, dependency-graph.json.gz 54f9c3643eeba139ea5e8d3b
abb1db9744d19f00f3cf024bbf192ec0d408c00b.

Pre-registered protocol (waves B..F, publish-then-execute):

- Wave B: fresh SZ maker (structural descendant of the sixth-cost
  adoption maker st_maker.py sha256 d4949f71114d8e36531b1e26684dfea225
  6554769e671578787db97a21c31ea9), fail-closed gates, 2-run
  byte-identical output requirement, per-row expected quadruple
  emission (k05 emits result=1 nodes=15763505), increment +
  MANIFEST generated.
- Wave C: merger s5_union_merge.py (sha256 907119610034fb2aebfde012550a
  4129dfa3b086c6de11194e856747ac74606a, the pinned svkit merger) run
  3 times byte-identical against the base head of record; merged head
  published. Expected shape (pre-registered): 6,874 rows,
  WIN 202 / LOSS 6,672; the merged bytes themselves are the ground
  truth, shape mismatch is a HARD-STOP.
- Wave D: merge-audit x3 (fresh fail-closed audit, WIN/LOSS conflict /
  duplicate / freshness re-checked on the merged bytes), kit README +
  MANIFEST publication, adoption log.
- Wave E: census measurer (structural descendant of st_measurer.py
  sha256 b43da34ab445f156a9240ba480e96b1d967c19a3cae9518d2e284b291f503
  098) measures BASE vs SCEN head census deltas; reaudit refresh
  (sv_refresh.py sha256 9500cc66389aa6c92b784e292baf8f0adb540a2f798ea17
  6102e84194ac11b7b protocol) and publication.
- HARD-STOP on any gate failure, conflict, duplicate, byte divergence
  between merger runs, crash or truncation; partial state disclosed,
  never trusted as-is.

Meaning and non-meaning: this Part only admits published, corroborated
S5 raw verdicts into the canonical solver-trusted cache chain. NO root
verdict is consumed, no class-status change, no closure claim. The 42
rows are S5 level rows under the frozen quarantine and evidence policy.

Status guard: the standard 11x11 empty board is UNKNOWN. All 19
central-reply roots are UNKNOWN. The two-stone root {60,27} is UNKNOWN.
Its remaining third moves {100,108} are UNKNOWN. S2 and closure classes
1/2/4 and all closure classes are UNKNOWN. A WIN(1) or LOSS(2) S5 raw
is not a class closure claim, not a root verdict, and transfers
nothing. Nodes and expansions are bookkeeping, never verdicts.
