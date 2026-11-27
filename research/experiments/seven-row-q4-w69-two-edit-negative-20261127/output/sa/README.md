# width-69 seeded SA negative (2026-11-27, same session)

Engine: published `search_seeded.js` of seven-row-q4-band-42-56-20261115,
unmodified, run as `node search_seeded.js 7 69 4 SEED BUDGET_MS w68_seed.json`
with w68_seed.json = the 20-stone width-68 witness of
seven-row-q4-witness-band-60plus-20261121 (output/w68/witnesses_68.json).

- seed1 (260s): best 21 stones, no improve events (single stdout line,
  captured from the foreground run; no other output was produced).
- seed5, seed7 (900s each): best 21 stones, identical config,
  improve events 0, rejects 0.
- seeds 2,3,4,6: launched 6-way concurrently and died silently with no
  output (not counted; environment limit).
- curve census 1,161,122; build 12.3s solo / ~74s under concurrency.

Honest heuristic-search negative: no descent below 21 stones in 3 completed
runs. NOT an absence claim for 7x69 witnesses.
