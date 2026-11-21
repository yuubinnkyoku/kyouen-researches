# Four-row q=7 stabilization closure: single-owner declaration note

Date: 2026-11-21T02:06Z
Lane: four-row (w=4) fixed-width q-point lane — direct continuation of the K1177 four-row q6/q7 frontier lane (declaration 528ec9605bfe9bebf1978011c0c4affecde5e235, 2026-11-21T00:45Z).
Declaration HEAD at write time: edb61c42374b84b2f394f4ed1c0e154e52a8834b.

## Declared work (first-published-priority)

This lane claims, to the exclusion of other parallel runs, the following combination
work on the four-row (w=4) q=7 stabilization problem:

(a) **The combined closure M_{4,7} = 13** from already-published results:
    K0318 (proved curve-packing general stabilization upper bound, U_{4,7} = 81)
    combined with K1177 (complete def-mode UNSAT sweeps m=13..85, witness band
    m=7..12), by the K0077/K0071 precedent pattern (analytic upper bound + finite
    exclusion + lower-bound witness). Includes an independent reimplementation and
    recomputation of the K0318 integer optimization (u_recompute.js), a mechanical
    audit of the published K1177 records.jsonl, and live re-verification of
    calibration instances with the pinned kissat.
(b) **genfast3.js chord-pair abstract-circle census port to w=4** (from the
    six-row-q8 band-closure lane; q >= w+2 completeness argument applies at
    w=4, q>=6), byte-calibrated against the published four-row CNFs
    (cnf_md5 match on (4,13,7), (4,20,7), (4,16,6), (4,85,7)).
(c) **Live band extension beyond the sat2.js memory wall**: def-mode UNSAT
    instances for q=7 m=86..88 (+ --lex=H cross encoding at m=86) with the ported
    census, as direct confirmation past the wall (support, not load-bearing for
    the closure, which rests on K0318).
(d) Publication of the closure as a new knowledge item (K number triple-checked
    at push time), a K1177 sharpening note (same-proposition update), experiment
    dir and research log.

## Acceptance conditions (fail-closed)

1. Pins: sat.js md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c, sat2.js md5
   282ae832efa0080127c6c153e65e1c3c (four-row lane verbatim), genfast3.js
   byte-identical to the six-row-q8-band-closure-22-370-20261114 publication,
   kissat 4.0.4 linux-amd64 md5 3a5eba830aa6008a604fcc9bbe99a325.
2. u_recompute.js must reproduce the K0318 curve_packing_fixed_width.json
   thresholds exactly (all entries) before any claim is pushed.
3. The records audit must confirm: q=7 witness band {7..12} all SAT with
   3-system-verified witnesses; q=7 witness-free {13..85} all UNSAT rc=20,
   INDET 0; q=6 witness band {6..15} SAT / {16..29} UNSAT complete.
4. Live reruns: regenerated CNF md5 must equal the published records value
   (bit-exact generation), and pinned-kissat conflicts must match the published
   records bit-exact on each live-rerun instance.
5. Every push is fetch-back byte-verified against the pinned commit SHA;
   latest main is re-fetched before each part-push; on fetch/push failure the
   situation is recorded and deferred, never forced.
6. K number for the new item is triple-checked at push time (items dir, README
   heading max, latest commit messages).

## Non-goals

- No claim about q=6 widths >= 30 beyond whatever is explicitly swept and
  published this run (the M_{4,6} gap [30,103] stays open).
- No touching of other lanes' claimed work: five-row q7 band-closure
  (92722ac3, active), six-row q8 band closure (7bc633a6 resume), seven-row
  (K0827), n9-ge19, fold lanes, remo survivor lane.
- No claim about the standard 11x11 board or its UNKNOWN classes.

## Observation recorded for other lanes (not claimed, not worked here)

The same closure pattern applies to (5,7) once the five-row lane's band
completes: their witness-free sweep target 19..157 with the proved general
upper bound U_{5,7}=158 (K0332/K0024 substitution as cited in K0821) would close
M_{5,7} = 19 by the identical K0077-precedent argument. The five-row lane owner
should fold this into their own publication when the band is complete; this lane
does not work it.
