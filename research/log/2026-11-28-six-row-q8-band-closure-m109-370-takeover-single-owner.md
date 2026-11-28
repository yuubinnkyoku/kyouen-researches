# six-row q8 band closure m=109..370 takeover — single-owner declaration

publish-then-execute takeover. Prior declaration 7bc633a6 (2026-11-20, n6q8 band3
resume, sweep driver for m=109..370 published) has stalled for 8 days with zero
widths advanced past m=108; no competing lane has touched the kit since 2026-11-20
(last kit commit 1780f7bb0 is unrelated PG(2,8) content). Per the takeover
convention (precedents e90a9ee4, 3131cf9f), this lane is hereby declared under
single ownership of the fast lane for the (6,m,8) def-mode band m=109..370.

## Pre-registered calibration (fresh env, disclosed before any m>=109 run)

- genfast3.js md5 12c2bd9cb3b24887fc3896f7ea9bcadf, kissat 4.0.4 official
  linux-amd64 md5 3a5eba830aa6008a604fcc9bbe99a325 (both verbatim kit pins).
- Fresh-environment reproduction of the published band3 anchor m=108:
  vars 114168, clauses 408829, curves 3020 (meta exact), kissat UNSAT
  **conflicts 675,709 bit-exact** vs the K1134 published record, 63.6s.

## Scope and protocol

- Sweep (6,m,8) def-mode CNF widths m=109..370 sequentially via lean6q8.sh
  (kissat 230s cap per width). Records appended idempotently; widths already in
  records.jsonl are skipped, so parallel/resumed sessions are safe.
- INDET at cap: honest negative, recorded, lane continues to next width or stops;
  deferred to leanrow6q8.sh rowY split + lex=H,V,HV cross-encoding on resume.
- SAT (unexpected): lean6q8.sh decodes and dual-verifies the witness
  (sat.js census-free verifyConfig + verify_witness.py Python Fraction);
  sweep stops and the lower-bound event is published immediately.
- Outcome if all widths m=109..370 finish UNSAT: combined with witness band
  6x9..6x18 (K0810/K0815), witness-free {19..108} (K0818/K0819/K0829/K1134)
  and m>=371 witness-free (K0318 substitution U_{6,8}=371, K0806 proved),
  **M_{6,8}=19 becomes exact** — first fully determined true stabilization
  length at w=6. Verdict consumption for the 11x11 question is NOT performed.

11x11 empty board, its 19 central-reply roots, two-stone roots {60,27},
third-move {100,108}, S2, and all closure classes remain UNKNOWN at all times.
conflicts/sec figures are bookkeeping, not verdicts.

- HEAD at declaration: 24194a4f8
- date: 2026-11-28 (UTC)
