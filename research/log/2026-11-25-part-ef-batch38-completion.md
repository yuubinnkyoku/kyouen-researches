# Part EF batch-38 (closure class 30345, rank 12): COMPLETE - takeover lane closed the part; class-30484 route 2 of 2 measured

Publication chain (all on main, fetch-back byte-verified where bytes matter):

1. `16d7336e` - original Part EF single-owner declaration (2026-11-25T16:07:09+09:00).
2. Owner waves inc1..inc5 (ai001..ai043, 43/49 keys; inc5 last `d4a1792c` 08:43Z, no
   counter-declaration). Stall exceeded the 3.5h single-owner takeover rule.
3. `bb97def1` - Part EF takeover declaration
   (`research/log/2026-11-25-part-ef-batch38-takeover-declaration.md`, sha256 833c0d1b).
4. Val-gate fresh 4/4 node-exact vs the published batch-31 kit baselines before any
   takeover drive step (2M exhaustion x2, 15M LOSS pair 3,651,923 / 5,040,200).
5. `c5a42798` - inc6 outputs: ai044..ai049 (6 keys, 12 raws + final status.log
   81 lines, sha256 8ca390768e317...), 3 pinned drive38_local_step.sh invocations,
   0 EXHAUSTED / 0 MISMATCH / 0 TRUNCATED in inc6. Fetch-back 13/13 byte-exact.
6. `a6bee0fb` - takeover-lane machine audit: audit_b38.py (b39-pattern fail-closed
   A1-A9, 105-file raw set incl. 7 pinned truncated artifacts with a replay-done
   prohibition, 81-line status accounting, exact-int lo semantics past 2^53,
   50-pair canonical-cache absence); 3x clean runs byte-identical
   batch-audit.json 73652099...; tamper battery 9/9 fail-closed incl. 2 deep
   coordination attacks (audit-battery.log 385bae6a).
7. `d08a493e` + `17489a6b` - kit run record: README.md (49/49 honest results,
   drive record, machine verification, verdict discipline) and MANIFEST-sha256.txt
   (181 entries). HONEST INCIDENT RECORD: the first MANIFEST push in d08a493e
   carried 6 sha256 fields corrupted by a manual retyping mistake
   (ai010 / ai021 / ai011.p2 / ai019.p2 / ai022.p2 / ai023.p2); the follow-up
   17489a6b streamed the locally machine-verified MANIFEST bytes directly and the
   fetch-back is byte-identical (MANIFEST sha256 4dbf88565977...). No kit file
   changed between the two commits; the kit bytes were never wrong, only the
   first-published digest table. Lesson recorded: never hand-retype a manifest;
   always stream from the verified local SSOT and fetch-back compare.

Inc6 (takeover lane) results, all two-pass fresh-cold node-exact @15M order0:
- ai044 LOSS 5,677,449 (class-30484 dual-class claim-reserved child, first-ever probe)
- ai045 LOSS 7,700,102
- ai046 WIN-HALT 5,256,793 (unconsumed)
- ai047 WIN-HALT 2,946,085 (unconsumed)
- ai048 WIN-HALT 2,232,854 (class-30484 dual-class claim-reserved child, unconsumed)
- ai049 WIN-HALT 832,069 (unconsumed)

Batch-38 final: 49/49 keys = 24 LOSS + 19 WIN (all unconsumed) + 6 EXHAUSTED
(ai007/ai024/ai030/ai038/ai040/ai041, honest UNKNOWN, no same-condition re-probe),
total nodes single pass 396,892,270.

## What this does and does NOT change

- Class 30345 (rank 12 in the closure table): all 49 target children now carry
  honest first-run labels; the 6 EXHAUSTED keys remain honest UNKNOWN, so class
  30345 is NOT closed (fresh-unknown 49 -> 6 remains for any future refresh; no
  closure, coverage, or secured-coverage is claimed for 30345).
- Class 30484: this part completes route 2 of the two candidate routes toward
  bringing 30484's unknown children down. The reserved child ai044 measured LOSS
  (admissible for a future loss-only adoption Part, EI/EL pattern) and ai048
  measured WIN (unconsumed; adoption is the scrutiny-owner C++ gate 9193f5b6's
  exclusive prerogative). Until such an adoption Part runs, class 30484's
  unknown count is UNCHANGED at 5; nothing here shrinks it.
- Canonical cache chain head is untouched (machine check A9: all 50 batch-38
  child pairs absent from the canonical cache). Batch-38 verdicts are NOT
  consumed anywhere.
- The standard 11x11 empty board, all 19 central-reply roots, the two-stone
  roots, S2, and classes 30345/30484/30118 all remain UNKNOWN.

## Resume notes for the next lane run

(a) 30484 route 1 (probe-level WIN adoption): the scrutiny-owner C++ gate
`9193f5b6` must adjudicate the probe-level WIN adoptions (incl. aj030/aj049/
aj050 and now batch-38's ai048/ai046/.../ai002...). This lane CANNOT run it:
the upgraded sandbox has no g++ and package installation is explicitly
forbidden ("Package installation is forbidden in this sandbox"). If the user
can provide a C++-capable environment or run the gate on their own machine,
that is the single highest-value contribution for class 30484.
(b) 30484 route 2 (most promising next Part): a NEW declared single-owner
loss-only adoption Part adopting ai044's LOSS (EI/EL pattern). Requirements:
fresh declaration log first; pinned merger byte-clone of the EI-era merged
cache 73482be0... as merger input, BASE = EL merged canonical cache
cf08e181... (6,713 rows, WIN 158 / LOSS 6,555); loss-only adoption removes
exactly ai044 (and only claim-free LOSS children), shrinking class 30484
unknown 5 -> 4 after the removal is machine-verified.
(c) Independent re-verification open item: the second-env lane covered inc1-3
21 keys + 86-raw crosscheck (wave V1 614f58ff); the inc4-5 22-key re-run was
interrupted (secondenv README final 4e002320). inc6's 6 keys have no second
re-run either; a future wave can cover both gaps.
(d) 11x11 empty board: UNKNOWN. No batch-38 number is a win/distance claim.
(e) Hourly parallel-run caution: re-fetch latest main before any push;
  d4a1792c/519438b5-style stalls (EJ, batch-40 class 30118) follow the 3.5h
  takeover rule - check Part EJ freshness before any takeover move.
