# Session log: n11 third-implementation bank full-band recalibration (2026-11-21)

Lane: the n11 long-term lane of
`research/log/2026-11-21-n11-thirdimpl-bank-full-recalibration-single-owner-note.md`
(declaration commit `451e0fe8`, HEADs recorded there). This session executed the
bank full-band recalibration, the first of the two follow-up items the `ea73c3e3`
session deferred. All acceptance conditions C1-C5 of the declaration pass; no
condition, gate, verdict, or corpus row was consumed or changed anywhere.

## Executed

1. **Calibration on this host before any bank row counted (C1).** Kit
   `third_impl.js` byte-verified against the published MANIFEST pin (sha256
   `08ea958f...`); kit probe-13 cache byte-verified against its pin (`60e0dc34...`,
   5,756 s5verdict rows; 158 WIN / 5,598 LOSS, stones 5). `verify_tbl.js`:
   replica quads 95,670 == mine 95,670; 195,044 random triples, 0 mismatches.
   Anchor w1 `10376293541461626880:67109120`: WIN(1), expansions 11,663,909,
   ttHits 6,284,843, ttOverwrites 7,469,605; identical to the published
   fixed-implementation fields (33.80s wall vs 34.24/34.43s).
2. **Bank batch (C2 protocol: run_bank.py, one clean or aborted run per row).**
   Set: all 158 WIN rows + 40-row LOSS sample (`--wins all --loss-sample 40`),
   wall cap escalated 55s -> 90s as declared. The 14 clean-agreed `bank-fixed-A`
   rows were seed-copied (same fixed implementation; not re-proven); its 2
   wall-inconclusive rows re-ran clean WIN here (58.99s / 54.71s). Raw stdout of
   every non-seeded row was produced fresh this session on this host.
3. **Escalated straggler.** `10448351135499550786_0` did not finish at the 90s
   batch cap (aborted runlimit attempt preserved as a comment inside its file); an
   escalated 240s-cap single-row run returned WIN(1), 33,369,967 expansions,
   94.11s, clean. Final batch state: no runlimit rows remain.
4. **Result: 198/198 rows agree verdict-level with the cache rows (158 WIN +
   40 LOSS sample). 0 disagreements (so the C3 hard stop never fired), 0 gate
   fails, 0 unresolved rows.**
5. **Determinism spot checks (fresh reruns on this host).**
   `10376293541461622792:65600` -> WIN(1) 10,898,228 / 5,964,726 / 6,703,924 and
   `13019119616:16448` -> LOSS(2) 7,660,602 / 3,951,175 / 3,466,722, identical to
   their batch fields and to the published legacy witness values (walls excluded).

## Publication byte-fidelity audit and repair (same follow-up)

Unauthenticated raw fetches had failed for the whole `ea73c3e3` session (repo
momentarily unfetchable), so its session log honestly left "MANIFEST.sha256 pins
published bytes pending a later byte-exact fetch-back". Raw fetches work again
(re-verified this session), so this session ran that deferred fetch-back. Two
findings, honestly recorded:

1. **One trailing newline was stripped from every text file at that session's
   push.** Repo bytes end without the final `\n` for README.md, third_impl.js,
   verify_tbl.js, run_bank.py, out/witness-outputs.txt, out/bank-fixed-A-outputs.txt
   and MANIFEST.sha256 itself; the canonical lane-kit copies (kept from that
   session) hash exactly to the published MANIFEST pins, i.e. the kit copies are
   the pre-strip intended bytes and the discrepancy is exactly one inert byte per
   file (verified: push of a kit file alone reproduces the manifest pin, and a
   kit-minus-final-byte reproduces the repo bytes). A pilot push of one bank-full-B
   row showed the push path used in THIS session is byte-exact (trailing newline
   preserved), so the stripping came from the earlier session's content assembly,
   not from GitHub or the tool.
2. **The per-file raw outputs were never pushed.** `out/witness/*.txt` (18 files)
   and `out/bank-fixed-A/*.txt` (16 files) were named in that session's Artifacts
   section, but only the two concatenated summaries exist in the repo.

Repairs (all byte-verified by fetch-back at this session's commits; log below):
the five non-README stripped files were re-published with the canonical kit bytes
(restoring the final newline, making repo bytes equal the pre-existing MANIFEST
pins); the 34 missing raw files were published from the lane-kit canonical copies
after machine verification that each raw's stdout line appears verbatim in the
pinned summary blocks (witness 18/18, bank 16/16); the experiment README appendix
was appended (its MANIFEST line updated accordingly); MANIFEST.sha256 was
regenerated to enumerate every artifact of the experiment dir (239 entries,
including every raw row file). The lane kit remains the local canonical mirror.

## Incidents and honest notes

- One "Failed to execute Koyeb remote command" infrastructure failure hit a mid-
  batch slice; its 3 completed rows persisted in the kit-run outdir (all batch
  outputs live under the knowledge kit, which is reset-resistant) and the
  idempotent runner resumed without loss.
- Writing the escalated row file, one digit of a preserved-comment line was
  initially transcribed wrong (ttOverwrites=28849398 instead of the raw 28049398);
  the preservation gate (diff against the saved raw .aborted90 copy) caught it
  before publication and it was fixed; both raw lines are now preserved exactly.
- The probe-13 cache row `s5verdict,1297036692683751424,65792,5,2,0` is a
  different key from the sixth-cost k03 re-run row `10376293541461626880:65792`
  (WIN at 15M, unconsumed). No conflict exists; recorded here so future sessions
  do not conflate the two keys.
- node reproducibility: this host (Node v22.20.0, 2 cores, serial) reproduces the
  previous session's exact expansion/tt counts on all tested rows and anchors.

## Status after this session

- The fixed third implementation now agrees verdict-level with the published
  probe-13 cache on the full pre-registered bank: 198/198 rows (all 158 WIN rows
  plus the 40-row LOSS sample), plus the earlier anchor rows (k02, parked pair,
  legacy 4). This is cross-implementation evidence only. The pre-registered
  adoption gate for WIN rows is unchanged: delegated C++ second-implementation
  verification (`cpp/solvers/kyouen_dfpn_root.cpp` sha256 `9193f5b6...` at 15M);
  adoption and judgment stay with the scrutiny owner.
- The sixth-cost k03..k43 batch remains halted by its own stop rule; its verdicts
  stay unconsumed. No cache increment, no chain merge, no class-status change.
- **No verdict was consumed. The standard 11x11 empty board, the two-stone root
  {60,27}, and third moves {100,108} remain UNKNOWN. Node/expansion counts are
  never read as verdicts.**

## Resume (next runs of this lane)

1. Stretch item 4 of the lane declaration (37 third-cost exclusive LOSS rows of
   `merged-exact-s5-after-class-excl-1.cache`, sha256 `bb4495e0...`) remains
   unstarted; it is still optional and needs no new declaration beyond the lane's
   existing one (verify the lane declaration is still first against latest main).
2. The LOSS population beyond the 40-row sample (5,558 rows) has not been spun
   by the third implementation; a deeper LOSS-band sweep is the natural next
   calibration extension if compute allows.
3. Re-fetch latest main before any push; watch the parallel non-n11 lanes
   (five-row species sweep, seven-row m69, six-row m52) for path collisions.

## Artifacts pushed this session

- `research/log/2026-11-21-n11-thirdimpl-bank-full-recalibration-single-owner-note.md`
  (declaration, commit `451e0fe8`)
- `out/bank-full-B/` (198 row files, incl. the pilot row) and
  `out/bank-full-B-outputs.txt`
- byte repairs: README.md, third_impl.js, verify_tbl.js, run_bank.py,
  out/witness-outputs.txt, out/bank-fixed-A-outputs.txt;
  newly published raws: out/witness/*.txt (18), out/bank-fixed-A/*.txt (16)
- MANIFEST.sha256 (regenerated, 239 entries) and this log.
