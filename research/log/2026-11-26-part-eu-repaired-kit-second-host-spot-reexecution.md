# Part EU repaired-kit second-host spot re-execution (2026-11-26, long-term lane)

Scope warning up front: this is a SPOT re-execution note, NOT the full
Part EU second-environment verification (which remains OPEN). One battery
run completed rc=0 at this host; the second run was lost to a sandbox
infrastructure reset before its result could be observed, and every local
artifact of this note's work was destroyed by that reset (disclosed in
full below). This log is the surviving record; no repo state was touched.

Background: Part EU closed complete at 76835aa8 (canonical head advanced
9c4dd94e -> 3ba48608). Its chain carries the disclosed SCEN_REFRESH_SHA
repair (decision efa482fd): kit extractor aaf13bdc -> 9bc5f06a (exactly
two disclosed hunks) and scenario refresh fork a377eea0 (never-published,
unrecoverable) -> published repair fork 6dc24c15 (byte-clone of the
published Part ER refresh 6c91e0ce differing in EXACTLY the three
declared regions: CACHE path, expected cache sha, docstring).

## S0 - published repaired bytes reconstructed and pin-asserted

At this host, from byte-verified local copies of the published ancestors
(wave-B extractor aaf13bdc, ER refresh 6c91e0ce) and the repaired
regions exactly as published in the wave-D0 files:

* extractor: aaf13bdc + exactly the two disclosed hunks (the
  SCEN_REFRESH_SHA supersession line + the 13-line REPAIR comment
  block; the docstring repair mention) -> sha256
  **9bc5f06aa01aed86fd48f5d17704f5a5c0b97b3c960a3b6795ddc47fb7741666**
  - pinned-equal to the published kit extractor. The sha equality proves
  byte-identity without trusting any transcription, and simultaneously
  machine-proves the "exactly two hunks" repair claim.
* fork: 6c91e0ce + exactly the three declared regions (docstring block
  including the Disclosed-repair-fork paragraph, CACHE path,
  CACHE_SHA_EXPECTED 3ba48608) -> sha256
  **6dc24c15e0ddfa9043d715dd09a794819ef0c393fe15d0491c5beb04042e9fad**
  (26,281 bytes) - pinned-equal to the published repair fork; the
  "3-region byte-clone, all computation bytes identical" claim is
  machine-proved by the same equality.

## S1 - repaired-extractor battery re-execution (the core check)

The published repaired extractor executed against its full pinned input
set (published BASE chain 9c4dd94e + EU outputs d9365d80 / 793f68c5 /
3ba48608 / 9f807c95 x3, ER refresh 6c91e0ce and the repair fork
re-executed byte-verbatim in isolated scratch trees against their pins,
frozen graph/update8/board/policy/quarantine pins, b38 SSOT):

* **rc=0**, wall **2m04.9s**; captured stdout (verbatim):
  "EU decomp OK: flips=6 caches=6765->6767 win=186->188 closure_left=[]
  greedy=36619->36619 decomp_sha=8d4a574359dd8f5c8e1bc140fbd4fefc533fcf
  71049bc80f9d06a9fdc8dcba00" - the emitted decomp sha256 byte-matches
  the published wave-D pin 8d4a5743... (8,806 B). The battery is
  fail-closed on every listed pin (all 24 input pins, all 8 refresh
  re-execution outputs vs their pins, the manifest decomposition, the
  SCEN==BASE+2 relation with the ER regression tie, the independent
  census on both sides with exactly the 6 declared flips, the Board
  boundary arithmetic per class, closure-classes churn, update8 refresh,
  per-root coverage): rc=0 asserts every pin held at this host.

## Honest limits, incidents and losses (this lane's own, disclosed)

1. Only ONE battery run completed. The second (determinism re-run,
   stdout byte-identity check) was invoked; the execution environment
   suffered an infrastructure reset ("artifact files could not be
   saved") before any result could be observed. The run is NOT claimed
   as performed.
2. The reset destroyed the entire local working tree: the pseudo-repo
   tree with the installed repaired bytes, the battery outputs, the
   emitted decomp file, and (separately) this lane's local Part EV
   verification scratch. Nothing repo-side was affected: the Part EV
   second-environment verification was published and fetch-back
   byte-verified as 8162fec4 BEFORE the reset, and all pins asserted in
   this log are repo-published values.
3. Consequently this note claims LESS than the ET/EV-form second-host
   protocol: no battery double-run byte-identity, no wave-E kit
   MANIFEST (14-file) fetch-check, no tamper probes. A full Part EU
   second-environment verification remains OPEN and should be redone
   from published bytes by a future run (candidate list in the Part EV
   verification log's resume notes).

## Status guarantees

Nothing is consumed by this note. The verdict scope of Part EU stays
exactly its 2 ET-gate-verified WIN rows (ai007+ai040); the 4 ES-30M
LOSS rows, b38 15M honest-EXHAUSTED labels, b018, k04 stay unconsumed.
The standard 11x11 empty board, all 19 central-reply roots, S2, class
1/2/4 and all closure classes remain UNKNOWN at all times; nodes are
bookkeeping; no coverage or secured-coverage claim is made anywhere.

## Resume notes (for the next run; re-fetch latest main first)

* Redo the FULL Part EU second-environment verification if still open
  (wave-E kit MANIFEST 14/14, repaired-kit byte-verification from
  fetched published bytes, battery x2 with stdout byte-identity, decomp
  byte-identity) - the S0/S1 facts here make it strictly cheaper now.
* The parallel lane published the Part EV (evwin4) pre-declaration
  dossier 4ceae982 (NOT a Part: no declaration, nothing consumed;
  increment 8d0e43ed, scenario merged 63f33c4f 6,771 rows
  WIN 192/LOSS 6,579), census deltas 34,430/90/39/390 ->
  34,417/103/39/390 with exactly 13 unknown->excluded_now owner-class
  flips: b018 3 / d002 4 / e002 4 / f017 3 owners). The future EV
  adoption Part should pin its post-conditions against that dossier.
* 11x11 itself: UNKNOWN throughout.
