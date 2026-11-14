# four-to-six-row q=4/q=5 row-deficient witness bands (2026-11-14)

5 families: (4,4), (5,4), (6,4), (4,5), (5,5). All were absent from
`results/fixed-width/mwq_stabilization.csv` and from the knowledge base.
This lane establishes the first lower bounds for all five.

## Claims (all bounds = witnessed lower bounds, not thresholds)

| family | witness band | single-deficiency | M lower | M upper | frontier (unswept, not absence claims) |
|---|---|---|---|---|---|
| (4,4) | m=4..34 all SAT | 11 stones (=w(q-1)-1) from m=8 | 35 | 237 (K0068 T_4) | m=35 |
| (5,4) | m=5..36 all SAT | 14 stones from m=14 | 37 | 567 (T_5) | m=37 (sat2 census OOM wall) |
| (6,4) | m=6..31 all SAT | 17 stones from m=23 | 32 | 1113 (T_6) | m=32 (census OOM wall) |
| (4,5) | m=5..19 all SAT | 15 stones from m=12 | 20 | 140 (K0318 U_{4,5}) | m=20 (INDET 210s / 3.30M conflicts) |
| (5,5) | m=5..23 all SAT | 19 stones from m=10 | 24 | 336 (K0318 U_{5,5}) | m=24 (INDET 90s / 699k conflicts) |

Every family has a continuous witness band from m=q (consistent with the
K0827 observation for 7-row q<=w families).

## Method

- Encoding: K0810 `sat2.js` verbatim (all-triples census + sequential counter +
  maximality; def-mode). `genfast.js` NOT used: PAIRTHRESH=12 is unsound for
  (4,5) since C(5,2)-(5-4)=9 < 12.
- Primary encoding lex=H,V,HVHV. Negative method note: def-mode **without**
  lex is catastrophically hard — control (3,23,4): 100s INDET at 445k
  conflicts without lex vs 17.7s SAT at 66,895 conflicts with lex.
- Solver: kissat 4.0.4 official static binary. Per-instance cap from env
  KSCAP (60..210s).
- Witnesses decoded by decode_verify.js and dual-verified:
  jsVerify (sat.js verifyConfig, census-free) + pyVerify (Python Fraction).
- **Constructive extension** (no solver): at the w(q-1)-1 stone cap, pure
  column-append/shift of a SAT base (spare=0; offsets 0..dm swept) is
  verified by verifyConfig. This resolved (4,4) m=29, 31 (off=0 from the
  m=28/m=30 bases) and m=33, 34 (off=0/1 from the m=32 base), each
  dual-verified like solver witnesses. The same sweep failed at (4,4) m=30
  for all bases <= m=28 and at (5,4) m=37 — where full SAT search
  succeeded (m=30: 105.1s / 119,905 conflicts) or the frontier remains
  open (m=37 blocked by CNF generation, see below).
- **Third system**: the five frontier witnesses (4,4) m=34, (5,4) m=36,
  (6,4) m=31, (4,5) m=19, (5,5) m=23 all PASS `verify_independent.ts`
  (pure TS/BigInt, algorithmically independent; used verbatim from
  seven-row-q7-witness-search-20261114) —
  `output/ts-verify-cross-family.json`. All five frontiers are
  **triple-verified**.

## Controls (exact thresholds reproduced before production runs)

(3,5) m=11 SAT / m=12 UNSAT (M_{3,5}=12); (3,6) m=8/9 (M=9); (4,6) m=15/16
(M=16); (4,7) m=12/13 (M=13); (4,8) m=10/11 (M=11); (3,4) m=23 SAT with
8-stone witness rows [3,2,3] (consistent with M_{3,4}=24). All in
`output/controls/records.jsonl` (11 records, 6 with witnesses).

## Honest negatives / walls

- (4,4) m=29,30: 60s-cap INDET runs (38,235 / 36,819 conflicts) superseded
  by longer runs/constructive extension. m=35 unswept.
- (5,4) m>=37 and (6,4) m>=32: `sat2.js` all-triples census CNF generation
  OOMs (4GB heap; empty META, lean4.sh emits rc=1 INDET lines that were
  pruned from records). Solver wall, not an absence claim. The known fix is
  the sat3.js streaming census of the seven-row lane
  (seven-row-q4-extension-band-sat3-20261115, DIMACS byte-identical) — next task.
- (4,5) m=20: INDET at 210s / 3,296,257 conflicts — the hardest unswept
  instance of this lane. (4,5) m=19 SAT needed 262,918 conflicts; the jump
  is steep. Candidate for a rowY fixed-row split (the technique that
  resolved the (7,5)/(7,6) frontiers).
- (5,5) m=24: INDET at 90s / 698,672 conflicts.
- def-mode UNSAT attempts at already-closed widths (3,24,4), (3,30,4):
  100s INDET — def-mode UNSAT is encoding-hard even where K0351's complete
  enumeration already closed the width. Recorded as a method note.
- Witness sizes fluctuate near the cap ((5,4) m=20: 13 stones), then settle
  at exactly w(q-1)-1; conflicts are non-monotone in m ((4,4) m=27:
  12,475 vs m=28: 1,746).

## Structure observations

1. Single-deficiency witnesses (exactly w(q-1)-1 stones, row multiset with
   one q-2 row and w-1 rows of q-1) exist from moderate m in every family
   ((4,4) m>=8, (5,4) m>=14, (6,4) m>=23, (4,5) m>=12, (5,5) m>=10).
   These are exactly the configs whose extinction defines stabilization:
   the K0068 parity regime requires all maximal configs to have w(q-1)
   stones. Each family's frontier is a search for the last
   single-deficiency maximal config.
2. Pure constructive extension (spare=0) crosses some frontiers but not
   all: it resolved 29/31/33/34 for (4,4) but failed at 30 (SAT by solver,
   105s) and 37 for (5,4) (open). Same pattern as the seven-row lane,
   where SAT search also pushed past the constructive limit (m=36..40).

## Next tasks (highest information value first)

1. (4,5) m=20 rowY fixed-row split (sat2.js --rowY=Y, the 5th/6th
   successful application of the technique) or a 600s+ run — first
   candidate for a small-w q=5 exact threshold below U_{4,5}=140.
2. sat3.js streaming census to cross the (6,4) m=32 and (5,4) m=37 OOM
   walls (byte-identical CNF, gen ~6s/width at 7x28..35 — cheap at these
   sizes).
3. (4,4) m=35+ and (5,5) m=24+ with longer caps.
4. Blocking-coverage analysis of the (4,4) m=32 base (which extended to
   34 with shifts): a K0827-style greedy-add/hill-climb band extension
   could push (4,4) far past 35 without SAT.

## Provenance

- All records: `output/{q4-w4,q4-w5,q4-w6,q5-w4,q5-w5}-def-search/records.jsonl`
  (+ `output/controls/`), schema as in scripts/README.md; witnesses are
  `s{w}x{m}q{q}_{lex}.witness.json` per width.
- Cross-environment-reset determinism: (4,4) m=4..25 conflicts bit-exact
  identical before/after a full container reset (kissat 4.0.4 official
  binary re-downloaded; script byte-identical from repo).
- Env incident note (methodology, not math): two container resets during
  the lane destroyed unpushed local outputs; all records pushed to main
  were regenerated deterministically where they were lost. Batches were
  re-run after restore; records.jsonl lines for CNF-gen OOM (rc=1) were
  pruned.
