# Part EU scenario-refresh pin repair decision (2026-11-26)

Owner-session decision record for the wave-D blocker disclosed in the
Part EU resumption log (commit baa8a0c0, section 3) and probed by the
throwaway diagnostic (commit f353dbe5).  This commit takes the deferred
decision under option 2 of the resumption log, publishes the repaired kit
bytes, and unblocks waves D..F.

## The blocker (unchanged facts)

The Part EU declaration (7136d22c) pre-registered
`SCEN_REFRESH_SHA = a377eea0cf5fac65fc248a7d50b5b8672c442dd9f26a80d3cd2
cb08954ba067c` for the scenario reaudit refresh fork.  Those exact bytes
were never published (wave B carried only the three kit scripts) and the
declaring session's environment is gone; repo-wide search finds only the
pin (resumption log section 3).  The diagnostic fork `353f15d3...`
(commit f353dbe5) is likewise throwaway-local and was never published, so
no verifiable byte stream for either sha exists or can exist.  Option 1
(exact `a377eea0` byte recovery) is therefore closed; option 2 (a
disclosed repair of the pin to published, byte-verifiable fork bytes) is
the only route that keeps the Part's verification independent.

## Decision (option 2, with a published fork)

* `reaudit/scripts/refresh_adoption_eu.py` is published in THIS commit:
  sha256 `6dc24c15e0ddfa9043d715dd09a794819ef0c393fe15d0491c5beb04042e9fad`
  (26,281 bytes) - a byte-clone of the published Part ER refresh
  `6c91e0ce...` differing in EXACTLY the three declared regions (the
  CACHE path, the expected cache sha, the docstring); machine-verified
  3-hunk diff, every computation byte identical to `6c91e0ce`.
* The kit extractor `scripts/compare_deltas_eu_adoption.py` is repaired
  in THIS commit: sha256 `9bc5f06aa01aed86fd48f5d17704f5a5c0b97b3c960a3b
  6795ddc47fb7741666` (was wave-B `aaf13bdc...`).  Byte-diff vs the
  published wave-B bytes is EXACTLY two hunks, both disclosed: (1) the
  `SCEN_REFRESH_SHA` pin superseded to the published fork sha with this
  decision referenced in an inline comment; (2) the extractor docstring
  mention updated.  No other byte changed.
* NOTHING else about the Part changes: the four scenario refresh output
  pins pre-registered by the declaration (refresh-summary `2b70bb55`,
  closure-classes `59a4c85f`, per-root-coverage `cfc2bfe1`, probe-worklist
  regen pin `397a4379`, unpublished per the size policy) are
  docstring-insensitive, UNCROSSED here, and remain the authoritative
  post-conditions; the wave-C output pins (increment `d9365d80`, manifest
  `793f68c5`, merged `3ba48608`, merge-audits `9f807c95` x3) are
  untouched.

## Honest basis of the repair (what carries the guarantee)

The identity claim does NOT rest on reproducing `a377eea0` (no preimage
claim is made or possible; the fork docstring wording is this session's
choice).  It rests on two machine facts: (a) the fork is a 3-region
byte-clone of the published, pinned ER refresh `6c91e0ce` (all
computation bytes identical); (b) executing the fork reproduces the four
pre-registered output pins byte-for-byte - executed this session rc=0
(wall 64.7 s): summary `2b70bb55...`, closure `59a4c85f...`, prc
`cfc2bfe1...`, worklist `397a4379...` (3,717,712 B, exactly the declared
size).

## Machine verification this session (all from published bytes plus the
two repaired members above)

* Repaired extractor full battery rc=0, TWICE (wall 2m15.8s / 2m12.8s),
  stdout byte-identical between runs; the four output pins re-verified
  through the extractor's own scratch re-execution of BOTH refresh forks
  (the published ER refresh `6c91e0ce` reproducing the ER reaudit trio,
  and the new fork reproducing the scenario trio, both including the
  publication-exempt worklist regen pins `78e499dd` / `397a4379`);
* decomp-deltas-euwin2-adoption.json sha256 `8d4a574359dd8f5c8e1bc140fbd
4fefc533fcf71049bc80f9d06a9fdc8dcba00` byte-identical across both runs
  - and container-invariant across sessions: the throwaway diagnostic
  (f353dbe5, pin `353f15d3`, identical single substitution) reported the
  same `8d4a5743...`, so the decomp does not depend on the choice of
  fork docstring;
* all declaration post-conditions confirmed by the full battery: exactly
  6 UNKNOWN->excluded_now flips {12846,12875,13801,30282,30308,30326}
  with 30345 NOT double-flipping, class-30345 cost-unknown 7->5 (51 raw/
  50 cost boundary), 30354 static (97/97, 96), census 34,436/84/39/390 ->
  34,430/90/39/390, closure 805->805 with zero rows left/entered and the
  exact rank swap {30345: 8->7, 20421: 7->8}, win_hit groups unchanged,
  per-root deltas only 12: 2850->2848 and 36: 3007->3005, joint greedy
  36,619 static, update8 static (31,859/260/131), worklist 64,309 ->
  64,307.

## Sequencing and guarantees

Waves D (reaudit outputs + decomp), E (close-out README + MANIFEST) and
F (completion log) follow this decision, each preceded by a fresh main
refetch (hourly parallelism) and each verified by commit-pinned
fetch-back.  Until the Part closes at wave F, the operating canonical
BASE stays the Part ER head `9c4dd94e`; the EU merged cache `3ba48608`
is published but not yet adoption-complete.  This decision consumes NO
verdict on its own; the Part's verdict scope remains exactly the 2
ET-gate-verified WIN rows ai007/ai040.  The standard 11x11 empty board
and every central-reply root stay UNKNOWN; nodes are bookkeeping; no
coverage or secured-coverage claim is made anywhere.
