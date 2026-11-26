# 2026-11-26 kit-10 (m35/m36 frontier + windows + even-life) pre-declared micro-kit log

## S1 Context and lane

High-speed lane, self-executed. Environment: user PC unreachable; GitHub API
publication only; bash sandbox with python3. Before any work: latest main
re-fetched (head `8d21dbe8`, 2026-11-26T13:28:57Z), AGENTS.md re-read,
knowledge/kyouen-research KNOWLEDGE.md resume items re-read (kit-9 / kit-9b /
Part SP bullets). Counter-probe before build: search_code for kit-10 /
m35m36 / frontier_m35 / explore_m35 in this repo -> 0 hits on the target
artifacts (the 'kit10' substring query returned 3 partial word hits all in
kit-9/kit-9b paths, none of them a kit-10 artifact). No concurrent lane had
started kit-10.

## S2 Registration and build

- Registration source: the kit-9 frozen .out future_slice_registration_constants (34 items) pulled from commit `c660fe15` via raw fetch; sha256 of the fetched .out byte-matched the published pin `eb0c0c14...` BEFORE any parsing (kit-9b lesson: get_file_contents/open_url text wrapping can corrupt; raw fetch + sha verify first).
- The frozen texts were parsed by machine (regex seat/dead-seat/collapse parsers) into 32 binding row structs; texts carried byte-verbatim into the kit (cand fields). Duplicated m31 z=64 / m32 z=65 registrations skipped (kit-9b disclosure).
- Rule v2: stack splits enumerated for BOTH the stick seats (co=42) and the NEW seats (co=44) of the m=19/m=20 d=12 births (kit-9b resume item (iii)).
- Even-m lifecycle rows regenerated as z=3m-1, 3m, 3m+1 (structural even analogue; the kit-9 proposal-text indices were regenerated and the regeneration disclosed in-row pre-run).
- Engine block byte-cloned from the kit-9 explorer's embedded ENGINE_BLOCK (pin `bd5f22e4...` asserted; the standalone `engine_block.py` published alongside is the kit-9 byte-clone `582c93c1...`).
- Battery literals: kit-9 1,454 carried + 150 new = 1,604 (union, sorted-unique). Anchors: kit-9's 234 (machine-extracted from the kit-9 explorer anchor_spec) + the 100 kit-9 published census separation spots (machine-extracted from the kit-9 .out row separations with role strings) = 334.

## S3 Official frozen run

- The explorer `explore_m35m36_frontier_windows.py` (sha256 `76a982ec...`) ran to completion rc=0; frozen output `explore_m35m36_frontier_windows.out` (234,659 bytes, sha256 `31dc6b2a...`).
- Determinism: runs 1-6 byte-identical (default, PYTHONHASHSEED=random, env -i, default, default, env -i). A shell timeout at run 7-in-progress reset the sandbox (documented lesson from kit-8b: long batteries must be chunked <=250s; the timeout cost was a discarded partial stdout only). Post-reset fresh-cold run 7 byte-identical. 7 clean byte-identical walks total.
- Runtime ~85 s/walk.

## S4 Results (finite observations; no universal claim)

- 30/30 binding ladder rows FULL HIT (registered seats exactly as predicted; zero unregistered separations beyond the rule-v2 shadow track; audit gate G14 = no unregistered residual).
- Frontier 23rd/24th datum candidates m=35@z=69 / m=36@z=70 BOTH EXACT (first-ever m>34 rows). Parity-scaffold observation count 24/24 (m=13..36).
- Windows m=33 z{57..64} / m=34 z{58..65}: 16/16 CLEAN. Measured lines: m=33 {57..65}, m=34 {58..66}.
- Even-m lifecycle m=14/16/18 z=3m-1..3m+1: 9/9 EXACT parity-flipped template (family DOWN 0v1 / stick DOWN 0v2 + NEW UP 2v1 + both rule-v2 splits as exact mimics / terminus DOWN 0v1 with shadows riding). First complete even-m lifecycle chain.
- Rule v2 stick-side shadows (m19 {19,19,23},{19,20,22},{19,21,21} @S=61; m20 {20,20,22},{20,21,21} @S=62) + NEW-side shadows (4/3 splits) all exact mimics. NEW finite observation: the m19 stick-side shadow stack ALSO separated as exact mimics one slice early, at the z=60 one-past slice (UP 1v0 with the host family). Shadow families appear to track hosts at every slice where the host separates. Registered as a kit-11 observable (post-hoc; not a law).
- Anchor rechecks 334/334 reproduce published values. Battery 1,604/1,604 (closed == vC == vO).
- Total: 57 row records, 95 separations, 0 contradictions.

## S5 Verification

- `audit_kit10.py`: 15 gates (engine pin, battery match + recompute, anchor count/match/recompute, row count, full per-row sweep recompute with parts regenerated and separation multisets compared, total separation count, frontier datum exactness, 16-window clean check, even-life parity template, rule-v2 mimic checks, no-unregistered-separations, future constants count). AUDIT-PASS, 2 runs byte-identical.
- `derive_check_kit10.py`: 433 engine-free arithmetic checks (R=m+z+1, seat sums, stack admissibility, K1268 z* formulas, every collapse literal in every registered prediction recomputed from the K0832 closed form). DERIVE-PASS, 2 runs byte-identical.
- Tamper battery: 3/3 fail-closed (battery literal flip rc=1; anchor value flip rc=1; phantom window separation rc=1). Original bytes verified unchanged (sha re-check).
- ASCII gate: non-ASCII byte scan over all published files = clean (kit-8 mojibake lesson).

## S6 Kit-11 registration (frozen in the kit-10 .out)

- Next one-past/birth pair per m=19..32 (m19: z=62/63 with stick co=44/NEW co=46 including the rule-v2 split enumerations for co>=2m; m20: z=63/64; ...; m31: z=66/67; m32: z=67/68).
- Frontier 25th/26th datum candidates: m=37@z=73 {37,38}@75 UP 2v0 (z*(37)=2*37-2+1=73, K1268) and m=38@z=74 (38,38)@76 UP 2v1 (z*(38)=74).
- Window proposals: m=35 z in {61..68}, m=36 z in {62..69} (both m are NOT strip-covered).
- Even-m lifecycle continuation contingent note (if the kit-10 even template held - it did - the next-depth rows stick z=3m+2 of {m,2m+2} + NEW {m,2m+4} are the kit-11 candidates) and the odd-m close-out note.
- The rule-v2 early-shadow track (shadows appearing with the host at every slice) should be registered explicitly for the m19/m20 next slices (one observation; verify before claiming).

## S7 No-claim caveats

The frontier parity count, the rule-v2 shadow observations, the even-m
lifecycle template, and all shape/collapse values are finite observations
from this kit's sweeps, not laws. The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27}, the third-move {100,108},
S2, and closure classes 1/2/4 remain UNKNOWN at all times. No verdict is
consumed. Nodes/shape counts are bookkeeping.
