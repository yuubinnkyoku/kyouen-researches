# m=33/m=34 second census: concurrent blind replication of the kit-9 pre-declaration census (kit-9b)

- kit id: kit-9b (hourly lane, session 2026-11-26, ~12:36Z build)
- runclass: publish-then-execute BLIND SECOND CENSUS of the second
  row set of the kit-8 frozen future constants; frozen before the
  literal push; candidate-vs-measured committee by machine observation
  only
- commit base: 7af915fb (kit-8 publish-priority census). PARALLEL
  DISCLOSURE: the concurrent kit-9 census of the SAME territory was
  pushed (c660fe15) BEFORE this kit was assembled; its commit subject
  was read at build time ("30/34 FULL HIT, 4 co-split-shadow
  deviations, rule v2 codified", the 21st/22nd parity data); NO kit-9
  output byte was read before this kit's own frozen .out was pinned
  (see S6 item 1 for the exact blindness scope). Main head at push
  08f9fd14 (part-sn wave B; re-verified immediately before the push;
  the push-time counter-probe re-ran over the kit-9b territory, 0
  hits; neither target path exists on main at push time).
- files:
  `research/experiments/strip-newband-m33m34-second-census-20261126/{engine_block.py, explore_m33m34_second_census.py, explore_m33m34_second_census.out, derive_check_kit9b.py, verify_new_anchors_kit9b.py, audit_kit9b.py, README.md}`
- engine: published chain clone, sha
  582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0,
  startup pin
  bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92
  (gate PASS in the frozen output). SAME engine as kit-9: this kit is
  NOT an engine-independent replication (S6 item 2).
- explorer sha256:
  `a66746f1fde042b8676b9c03590c552ea89b5d55940e315c5cfcb43f808acb30`
  (137,837 bytes)
- frozen output sha256:
  `7f19e0071de98a515250881eaf7d9cb2fe12da881d52b432c77939dd94fc2787`
  (198,906 bytes)
- status: EXECUTED, VERIFIED, PUSHED (run rc 0, ~67 s; see S4)

## S1. Anchor re-verification (232/232) and battery (1,594/1,594)

The 180 inherited chain anchors verbatim plus the 52 kit-8 separation
spots NOT already spot-identical to inherited rows (the kit-8 .out
spots (R=84,X={30,27},z=56) and (R=86,X={30,28},z=57) are
spot-identical to inherited anchor rows and excluded here by design;
kit-9 re-lists both, S3). Pre-freeze independent verification on the
published canonical engine (verify_new_anchors_kit9b.py, run BEFORE the
census): the embedded 232 anchors re-measured 232/232 exact, the 52
new spots value-checked 52/52 against the published kit-8 .out; both
re-runs in the publish environment ALL PASS. In the frozen run every
anchor re-executed and hit exactly (232/232 match). Battery
1,594/1,594 all-match (closed == canonical == ordered; a strict
superset of the published kit-8 battery, machine-checked in
derive_check). No prior datum lost.

## S2. Registered vs measured (43/43 FULL HIT under the kit-9b registration)

59 rows executed (1,072 shapes, 91 separations): 34 binding kit-8
frozen rows + 6 lifecycle rows (m=13/15/17 at z=3m-1 and z=3m; the
kit-9 z=3m+1 slice NOT registered here) + 3 even-mid probes + 16
below-frontier window rows.

- 43/43 registered-candidate rows measured as registered: every named
  seat exact (frontier m=33 {33,34}@S=67 UP 2v0 and m=34 (34,34)@S=68
  UP 2v1, exactly the kit-8 frozen registration; the 32 ladder rows
  items 1-32 including the CONTINGENT m=31/m=32 mini-ladders; the
  m=19/m=20 d=11 births with their registered co=42 split stacks); the
  registered item-9 split stacks measured as exact numeric mimics of
  their host seats at every slice where registered; the L8
  family-tracker seats mimic-or-conform (all measured mimics); the
  m=13/15/17 lifecycle one-past/birth seats and trio trackers as
  registered (the one-past trios UP 1v0 exact mimics, the z=3m trios
  DOWN 1v2 stick mimics and the co=2m+2 birth split stacks UP 2v0
  exact mimics); the even-mid equistack trios {14,14,14}/{16,16,16}/
  {18,18,18} UP 2v1 exact mimics of the NEW birth seats sharing S.
- Window sweeps 16/16 clean (0 separations each, as registered):
  m=31 z in {53..60}, m=32 z in {54..61}.

REGISTRATION-DESIGN NOTE (the honest reading of 43 vs kit-9's 30+4):
this kit's registration pre-registered the co-split shadow shapes at
the stick/one-past seats as explicit mimic candidates (the kit-8 log
S5 item-9 operative rule generalized over the territory the kit-9
commit subject named). Under the kit-9 registration (named seats
only) the SAME measured rows count 30 FULL HIT + 4
HIT-with-unregistered-shadow. Both classifications describe the same
measured bytes; neither upgrades any claim; firsts belong to kit-9.

## S3. Cross-check with the concurrent kit-9 (POST-census, disclosed as such; the independent replication content)

All comparisons made after this kit's freeze against the published
kit-9 frozen output (sha
eb0c0c146c3d16090a604377a1aafc50bd56faee48a81cbdfa6d995df7db7a3f,
byte-verified against its README pin before comparing):

- Rows: the common (R,z,m) row set is this kit's 59 rows; kit-9
  additionally measured the 3 z=3m+1 lifecycle slices. Separation
  lists BYTE-IDENTICAL on all 59/59 common rows (91 separations this
  side, identical there), including the two frontier rows and the
  m=19/m=20 d=11 birth rows.
- The 3 kit-9-only rows re-measured with THIS kit's engine POST census
  (disclosed machine check, not a blind row): 3/3 identical (9
  separations).
- Anchors: the kit-9 234-row table and this kit's 232-row table
  deduplicate to the SAME 231 unique (R,X,z) keys; all 231 values
  identical. Both tables contain the inherited-block duplicate
  (R=77,X=(26,26),z=50); kit-9 additionally re-lists the two
  duplicate spots named in S1.
- Battery: 1,426 triples common, 1,426/1,426 identical values, both
  sides all-match; the union differences are registration-driven only
  (168 literals here-only, 28 kit-9-only, mostly each kit's own
  lifecycle/probe registration literals; machine-enumerated,
  disclosed).
- FIRSTS: the m=33/m=34 first contacts (21st/22nd parity data), the
  m=19/m=20 d=11 births, the even-mid probes, the window sweeps and
  every other first measurement of this territory belong to kit-9
  (c660fe15). This kit's role is the blind replication, which
  reproduced every common measured value byte for byte.

## S4. Verification (all executed)

1. Pre-freeze derivation: derive_check_kit9b.py -- engine-free paper
   derivation of every registered literal: fail=0, 149 literals
   checked; the kit-8 frozen future constants regenerated and
   byte-matched items 1-34; the 180 inherited anchors content-identical
   to the kit-8 explorer; the 52 new spots value-identical to the
   published kit-8 .out; the battery superset check passed; run BEFORE
   the first row sweep.
2. Pre-freeze anchor verification: verify_new_anchors_kit9b.py --
   232/232 canonical re-measurement + 52/52 published-value agreement,
   BEFORE any census row ran (ALL PASS; re-run in the publish
   environment ALL PASS).
3. Frozen run: rc 0, ~67 s, stdout sha 7f19e007....
4. Determinism: the frozen run plus verification runs (default,
   PYTHONHASHSEED=random, env -i isolated x2) are all byte-identical
   (4 executions, one byte string).
5. Independent ordered-engine audit: audit_kit9b.py re-executed every
   row with the ordered product: 59/59 rows recomputed, 0 separation
   mismatches; battery 1,594/1,594 ordered exact; anchors 232/232
   ordered exact; classification 43/43 reproduced; fail=0 (re-run in
   the publish environment, fail=0).
6. Standard caveats: the K0832 closed form remains the only PROVED
   statement; every item above is a finite machine observation; the
   standard 11x11 cell remains UNKNOWN at all times; no K slot is
   claimed; no residual verdict is consumed.

## S5. Handoff: kit-10 registrations (embedded future section; engine-free)

The .out future_slice_registration_constants section registers the
kit-10 handoff, engine-free: the m=19/m=20 d=12 one-past/birth rows
with the rule-v2 split enumerations (stick co=42 and NEW co=44 splits
registered), the m=21..m=28 continuations, the m=29/m=30 z=65..68
rows, the m=31 z=65/66 and m=32 z=66/67 rows, the frontier proposals
m=35@z=69 EXACTLY ONE {35,36}@S=71 UP 2v0 (23rd parity datum
candidate) and m=36@z=70 EXACTLY ONE (36,36)@S=72 UP 2v1 (24th), the
m=33/m=34 below-frontier window sweep proposals, the L8
family-size tracker continuation and the smax note. The shared
handoff literals re-checked at this log (the m=19 z=60/61 and
m=20 z=61/62 rows, the m=35/m=36 frontier proposals) agree
literal-for-literal with the kit-9 S5 handoff. TWO DATED
DISCLOSURES (frozen-bytes rule: the .out keeps its bytes, the log
records the errata):

1. WINDOW-PROPOSAL z-FIELD TRANSCRIPTION SLIP (unexecuted future
   registration, no measured row affected): the two window sweep
   proposal entries carry z fields "61..68" / "62..69" that contradict
   their own prediction text "z*(m)-8..-1" (z*(33)=65, z*(34)=66;
   the text ranges are 57..64 / 58..65) and the kit-9 S5 item 6
   handoff. The prediction TEXT is authoritative; kit-10 registers
   the text ranges z in {57..64} / {58..65}.
2. REDUNDANT RE-LISTINGS inherited from the kit-8-era future list
   (the kit-9 S6 item 3 class): the future section re-lists m=31 z=64
   / m=32 z=65, slices already measured by both censuses (kit-9 items
   29/32, both HIT). Kit-10 skips or contract re-measures both
   (agreement expected); no datum is affected.

## S6. Honest record / caveats

1. BLINDNESS SCOPE, exact: the kit-9 commit subject (c660fe15) was
   read at this kit's build time and is the reason the co-split
   shadows were pre-registered here; no kit-9 output byte (README
   body, .out, per-row outcome or value) was read before this kit's
   own frozen .out sha256 was pinned. The blind content of this kit
   is therefore the MEASUREMENT reproduction (59/59 + 232/232 +
   battery), not the registration-template test (the registration
   was informed by the commit subject). Disclosed in the frozen
   explorer docstring before the run.
2. ENGINE REUSE: this kit reuses the published chain ENGINE_BLOCK
   byte-clone (same engine as kit-9). The replication therefore
   re-verifies determinism, sweep structure, row assembly, literal
   derivation and audit implementation -- NOT engine independence.
   The kit-series second/third implementations for engine
   independence are the ordered-product audit (in-kit) and the C++
   gate lane (Part SM/SN precedent).
3. The 43-vs-(30+4) classification difference is a registration
   design difference, not a measurement difference (S2); no claim is
   upgraded or downgraded by either reading; K0832 is untouched.
4. Anchor-table bookkeeping: the inherited 180-row block contains one
   spot listed twice, (R=77,X=(26,26),z=50) (kit-5 frontier recheck +
   kit-7-era block); this kit's table keeps the inherited bytes as
   published (232 raw rows, 231 unique keys), matching the kit-9
   table after deduplication (231/231 identical values).
5. Battery union differences vs kit-9 are registration-driven only
   (168 here-only, 28 kit-9-only), all literals all-match on both
   sides; the strict-superset claim in derive_check is vs the
   published KIT-8 battery only, and it is machine-passed.
6. DATED DISCLOSURE (kit-9 published README PIN TEXT, not bytes; found
   by this kit's machine pin-check): the kit-9 README states the
   engine_block.py clone sha256 as 582c93c1...bbcc8841... (one hex
   digit off at the 52nd position); the published kit-9 AND kit-8
   engine_block.py blobs both machine-hash to
   582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0,
   byte-identical to this kit's clone. The kit-9 published BYTES are
   consistent; the typo is README pin-text only. This kit's frozen
   output, assembler assertion, README and log record the true value.
7. No universal claim is made here. K0832 is the only PROVED
   statement. The 11x11 standard cell remains UNKNOWN at all times.
   No K slot is claimed. No residual verdict is consumed. The hourly
   lane runs concurrently; the push-time counter-probe and head
   record are recorded above.
