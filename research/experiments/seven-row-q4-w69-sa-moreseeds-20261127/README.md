# Seven-row q=4, width 69: seeded SA with shifted w65-family seeds (2026-11-27)

Follow-up to the published width-69 seeded SA negative
(`seven-row-q4-w69-two-edit-negative-20261127/output/sa/README.md`,
w68-witness-seeded) using a different seed family: the two distinct
D4/translation images of the published w65 chain witnesses with the largest
deficient-row coverage, both covering width **67** (census TOP entries:
`id` dx=0 and `V` dx=6; selection reproduced with the published
`census_translate.py` functions).

- engine: published `search_seeded.js` of `seven-row-q4-band-42-56-20261115`,
  byte-clone fetched from main (sha256 `c4b5e904…`), unmodified;
  run as `node search_seeded.js 7 69 4 SEED 230000 seed.json`;
- run A (seed 11, `output/shiftA.jsonl`): curve census 1,161,122
  (published count reproduced exactly), 72,981 iters, best **21 stones**,
  0 improve events;
- run B (seed 13, `output/shiftB.jsonl`): curve census 1,161,122, 85,667
  iters, best **21 stones**, 0 improve events;
- both seeds maximalize to exactly 21 stones on 7x69 (20-stone witness
  family + 1 extra stone) and the annealer never descends below 21;
  accepts = iters (every random removal regenerates a maximal config with
  d <= 0), rejects 0 — same local-optimum signature as the published
  w68-seeded runs.

Honest heuristic-search negative: no descent below 21 stones in 2 further
completed runs from a different seed family. **NOT an absence claim for 7x69
witnesses.** M_{7,4} stays in [69, 1929]. Budget 230s per run (host shell
cap); wall-time-truncated annealing is not byte-reproducible across hosts,
so records are published as captured stdout. Verdicts are not consumed; the
standard 11x11 empty board and all roots remain UNKNOWN.

- `output/shiftA.jsonl`, `output/shiftB.jsonl`: captured stdout records.
- `seeds/shiftA.json`, `seeds/shiftB.json`: the two seed configurations
  (census-selected shifted w65 images).
