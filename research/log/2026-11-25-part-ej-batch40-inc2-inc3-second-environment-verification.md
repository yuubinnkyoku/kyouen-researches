# Part EJ batch-40 inc2+inc3 second-environment verification (takeover drive ak011..ak030)

- Executing lane: independent long-term-lane run (this session). NOT the Part EJ
  owner. The EJ chain verified here, byte-frozen at the published commits:
  declaration `2baf7e34` -> kit 1..4 (`c2019313`/`c91a8ece`/`c3aca5b1` ->
  val-gate `10259859`) -> drive-step correction `62a0bff9` -> drive inc1
  `519438b5` (all covered by the inc1 second-environment verification) ->
  **takeover `90c75f9f` -> inc2 `ddb56a2a` (18:24:47Z, ak011..ak020) ->
  inc3 `efd81f83` (18:33:40Z, ak021..ak030)**. inc1's second-environment
  verification log (published via `0a7e7263`'s session) is the process SSOT for
  this lane; this log covers the takeover increments only.
- Verification tree: every number below was re-derived on this host from
  published bytes only (raw CDN fetches pinned at `ddb56a2a` and `efd81f83`),
  including a full 20-key two-pass fresh-cold replica with the pinned
  jsreplay.js bytes. See H1 for what the session's environment resets cost and
  how the tree was rebuilt (nothing below depends on unsaved local state).
- At the final check (20:49Z) main's `output/status.log` for the EJ experiment
  dir is byte-identical to the inc3 snapshot (sha256 `c6351835...`), i.e. inc4+
  is not yet published; the frozen verification target remains the live drive
  state. This log does not touch the drive state (inc4..inc5, audit, README,
  completion log remain the owner's).
- Untouched by this verification: every unconsumed WIN row (ak002 from inc1),
  batch-38 keys (ai001..ai049 Part EF scope), aj030/aj039 (Part EK scope),
  all verdicts, all coverage. Nothing here consumes a verdict.
- **The standard 11x11 empty board, the 19 central-reply roots, the two-stone
  roots {49,60}/{59,60}, S2 {59,60}, and closure classes 1/2/4/16371/20421/
  34908/30484/30118/30345 all remain UNKNOWN. This verification does not
  change that.**

## E1 pins and fetch verification (ALL PASS)

- scripts at `efd81f83`: drive40_local_step.sh `5e613cce...`, runbatch.sh
  `f591f8c2...`, jsreplay.js `84585617...` (3/3 identical to the kit pins and
  to the inc1-verification pins).
- inputs: batch-keys-b40.json `2414d644...`; ak011..ak030.input.csv fetched at
  `efd81f83` on four independent occasions (see H1); all refetches identical.
- sources at `efd81f83`: canonical cache `73482be0...` (6,712 `s5verdict`
  rows + 1 comment line), prior-probe-universe base/`ext`/quarantine
  `81d23160...`/worklist extract and the other kit sources all hash-equal to
  the kit pins recorded in the inc1 verification -> the sources are
  byte-stable from kit through inc3.
- val-gate-host kit 12 files present and hash-stable at `efd81f83` (first
  published at `10259859`).

## E2 publication ordering (append-only PASS at file granularity)

- `ak001..ak010` raws exist at inc1 but not at the takeover commit
  `90c75f9f` (spot-checked ak011 -> 404 at takeover; raw dir is born with
  inc1's wave and the takeover continues it).
- At `ddb56a2a`: ak011..ak020 raws present (spot 200), ak021+ absent (404).
- At `efd81f83`: ak011..ak030 all present (60 files + status + earlier
  increments).
- **Raws append-only check: all 20 ak011..ak020 raw files (p1+p2) are
  byte-identical between `ddb56a2a` and `efd81f83` (20/20 `cmp` equal).**
  Pair sha equality of the raw wave across increments is PASS.

## E3 published raws: structure + two-pass + verdict (20/20 keys, 40 files)

For every ak011..ak030 raw (both passes): exactly one `replay,` row, the
pre-registered `# forbidden quadruples: 95670` header, and the terminal
`# replay_done` line (the runbatch truncation guard's completion marker);
p1 vs p2 equal on `id,stones,legal,is_or,budget,result,nodes,key_lo,key_hi`
(wall_s excluded, nodes INCLUDED; see H2c); every key result=2 (LOSS),
budget=15,000,000, order 0. Node counts (both passes equal):

- inc2: ak011 3,902,613 / ak012 10,505,070 / ak013 2,293,741 / ak014
  2,772,493 / ak015 2,884,083 / ak016 3,560,392 / ak017 3,411,665 / ak018
  4,803,912 / ak019 3,946,390 / ak020 6,160,576 (sum 44,240,935).
- inc3: ak021 6,203,259 / ak022 1,740,435 / ak023 3,402,567 / ak024
  5,071,799 / ak025 2,046,315 / ak026 2,839,530 / ak027 3,670,506 / ak028
  5,376,311 / ak029 10,199,307 / ak030 3,011,200 (sum 43,561,229).

All-loss, no EXHAUSTED, no PASS-with-exhaustion relabeling: the snapshot
matches the declared design (batch-17 honesty delta intact).

## E4 status snapshots: accounting PASS, but NOT byte-append-only (observed)

Published snapshot bytes: inc2 = 21 lines (10 inc1-arena PASS + ak002
WIN-HALT + 10 inc2 PASS = 20 PASS + 1 WIN-HALT), inc3 = 31 lines (30 PASS +
1 WIN-HALT), zero MISMATCH/EXHAUSTED/FAIL lines.

- Accounting: every one of the 20 new PASS rows' (budget,result,nodes) equals
  its raw's replay fields (20/20), and the inc2-subset rows reconcile against
  the inc2-commit raws (10/10). ak002's WIN-HALT line is byte-identical in
  both snapshots (the drive did not touch the inc1 arena).
- **Honest observation (functionally harmless, provenance-relevant).** The
  published status.log between inc2 and inc3 is NOT byte-append-only:
  `cmp -l` shows exactly 4 differing bytes. Offsets 865 and 916 (lines 18 and
  19, the ak017 and ak018 PASS rows' timestamp separators) changed 0x54 -> 0x55
  (`T` -> `U`, a single-bit flip). Offsets 1059-1060: the inc2 snapshot ends
  with a bare `c3 bf` (UTF-8 "y-umlaut", NO trailing newline, appended after
  the ak020 row's final newline), while at the same offsets the inc3 snapshot
  continues with '2''0' of the next appended line (ak021). I.e. the trailing
  2-byte artifact was removed and two earlier-line bytes were mutated
  in-place between publications. The functional fields (key/budget/result/
  nodes) are intact in both snapshots, and every PASS row reconciles with its
  primary evidence (the raws, E3) in BOTH snapshots, so the accounting is
  unaffected. The pinned runner scripts only ever append (`>>`) to
  status.log and `date -u +%FT%TZ` emits a literal 'T', so the pinned scripts
  cannot produce either artifact; the mutation happened outside their action
  space (cause not determinable from public bytes; both patterns look like an
  editing/tooling artifact - 0x54->0x55 is a +1 bit flip - not like a
  determinism failure).
- Consequence recorded for future audits: byte-prefix append-only checks
  against this status.log must NOT assume snapshot stability (the takeover
  declaration's append-only design claim holds at content granularity, not at
  byte granularity for status.log; raws are byte-clean, E2). The owner is
  invited to append a one-line honest note if convenient (same pattern as the
  Part EG/EO pin-drift notes).

## E5 val-gate molecules (4/4 node-exact, third host)

Fresh-cold re-runs with the published jsreplay bytes and the published
val-gate inputs, compared to the owner's host sidecars (fields
id..result,nodes,key_lo,key_hi; wall_s excluded from the gate):

- at2m A @2M: (0, 2,000,000, wall 9); at2m B @2M: (0, 2,000,000, wall 9) -
  both byte-identical to the owner sidecars this window (walls coincide 9/9).
- first-15m A @15M: (2, 3,651,923, wall 18 vs owner 17); second-15m B @15M:
  (2, 5,040,200, wall 25 vs owner 25).

4/4 node-exact vs the owner host baselines (and the published baselines);
wall_s agreement is informational only (host class matches; earlier windows
of this session reproduced the same molecules twice more with the same
fields, walls 18/17 and 27/25-26).

## E6 full replica probes (20 keys x 2 passes @ 15M, 20/20 node-exact)

Replica of the published two-pass wave using only published bytes (pinned
jsreplay `84585617...`, published per-key inputs), budget 15,000,000, order
0, fresh-cold, max 2 workers per pair, every invocation rc=0 with terminal
`# replay_done`:

- 16 keys (ak013..ak027, ak030) were completed and compared node-exact - both
  passes - in an earlier live window of this session (between the
  second and third environment resets, see H1): ak013 2,293,741 / ak014 2,772,493 / ak015
  2,884,083 / ak016 3,560,392 / ak017 3,411,665 / ak018 4,803,912 / ak019
  3,946,390 / ak020 6,160,576 / ak021 6,203,259 / ak022 1,740,435 / ak023
  3,402,567 / ak024 5,071,799 / ak025 2,046,315 / ak026 2,839,530 / ak027
  3,670,506 / ak030 3,011,200.
- 4 keys (ak011, ak012, ak028, ak029) were completed in the final live window
  with the probe files still present: ak011 3,902,613 / ak012 10,505,070 /
  ak028 5,376,311 / ak029 10,199,307; two-pass determinism re-asserted
  file-to-file; ak029's p1/p2 files are fully byte-identical (sha `a5e03fef...`).
- Every pass reproduces the published (budget,result,nodes,key_lo,key_hi)
  exactly; 20/20 keys x 2 passes. Replica totals: 87,802,164 nodes/pass;
  175,604,328 probe expansions for the full wave (bookkeeping only).
- Host wall_s run consistently 5-40% faster than the takeover lane's host
  on the big keys (ak012 mine 56s vs published 95s; ak029 57 vs 90) and
  ~10% slower on small ones - a different host class, unrelated to the gate
  (node-exactness is the criterion).

## E7 absence matrix and batch-keys joins (20/20 PASS, redone with string joins)

- All 20 (lo,hi) pairs of ak011..ak030 are ABSENT from: canonical cache
  `73482be0...` (6,712 `s5verdict` rows, no `s5verdict,<lo>,<hi>,` row),
  prior-probe-universe base (2,104), prior-probe-universe-b40 ext (2,154),
  and the active quarantine registry (no `[lo,hi]` entry). No fresh target
  was a re-probe of an adjudicated or quarantined key. (20/20; the five
  near-collision masking bugs are in H2.)
- batch-keys-b40.json (`2414d644...`): for each key, (legal, probe_order,
  s5_index, lo, hi) match the worklist-class30118-extract row (string-typed
  join on `^[0-9]+,[0-9]+,<lo>,<hi>,`), and the per-key input CSV equals
  `target,0,5,<lo>,<hi>,<legal>,0,0,0,0,0` (20/20). The 20 keys are exactly
  rows in probe_order order from the 52-row extract, claim-reserved
  ai033/ai034 excluded, consistent with the inc1 verification's R4/R5.

## Honest note H1 (three environment resets; everything rebuilt from pins)

This sandbox aborts and RESETS the whole workspace when a single command
exceeds its time cap. It happened three times mid-verification, all three from
over-packed probe calls (my own pacing error); each reset also wipes the
session scratch. The working tree (scripts/inputs/raws/snapshots/probe
outputs) was rebuilt from pinned raw-CDN bytes each time; final-window
redoes of the static checks (E1-E4 and E7 above were recomputed in the
final window; the val-gate E5 was recomputed identically in
both the second and third windows) and of the 4 remaining replica keys
completed the wave.
No claim below depends on wiped scratch: the 16 earlier-window replica keys
are recorded from their live comparison outputs; the final 4 keys' probe
files are sha-frozen above. Lesson (matches the Part EN lesson, stronger):
never size a probe call near the cap, and treat the scratch tree as
disposable - verify everything into the published log as you go.

## Honest note H2 (this session's own bug catches, all before any claim)

- (a) awk field-extraction bug: probe-key lines are whitespace-split 2-field
  lines, so `$(NF-1)` was the key id itself; the first absence-matrix loop
  therefore grepped nonsense patterns and reported "ABSENT everywhere."
  Caught by reading the extracted columns; redone with exact comma-splits.
- (b) awk DOUBLE-PRECISION bug on 61-bit keys: `-v` passed lo values become
  strnum, and `==` compared NUMERICALLY; doubles near 2^61 have ULP 256, so
  ak022/ak023's lo "matched" a worklist row 16/32 bytes away and falsely
  reported MISMATCH against the true rows. Redone with string-typed regex
  joins (20/20). Lesson: joins on 61-bit keys must be string-typed.
- (c) a p1/p2 comparison used `cut -f1-7,10-11`, silently EXCLUDING the
  nodes field (the same class as the prior session's f-cut bug). Caught by
  self-review before log-writing; redone with `-f1-8` (20/20 including
  nodes). Lesson: field-excluding comparisons must assert field counts.
- (d) in one wiped call, missing published AND probe files yielded two empty
  grep results, which compared "equal" as spurious NODE-EXACT rows. All
  comparison helpers now assert file existence and non-empty replay lines
  (the inc1 H2 output-accounting lesson, hardened).

## Resume (for the next runs, before touching anything: re-fetch latest main)

1. Part EJ single-owner continues the drive (inc4..inc5 + audit + README +
   completion log). Once those land, an inc4+ second-environment
   verification (and the close-out) is the natural next verification target;
   this log freezes at `efd81f83` / inc2+inc3 and does not conflict.
2. The 20 verified LOSS rows here are bookkeeping until the EJ owner's own
   audit/adoption chain consumes them; no verdict is consumed by this log.
3. While this log was being written the lane landscape moved twice: Part EP
   declared the first-ever WIN canonical adoption (epwin10, 10 gate-verified
   rows of class 34908, `2d8d24a7` 20:27Z) and Part EQ executed and closed
   the 3rd C++ scrutiny gate (18 unconsumed batch-38 WIN rows of class
   30345, 21/21 GATE-PASS, `233ebe38`->`81310623`->`697b50de` 20:37-51Z).
   Adoption/close-out of those is their owners' chain; re-confirm on latest
   main before starting any work that touches classes 34908/30345.
4. **The standard 11x11 empty board and every root/class named above remain
   UNKNOWN; nodes are bookkeeping; no win/loss, coverage, or secured-coverage
   claim is made or implied by this log.**
