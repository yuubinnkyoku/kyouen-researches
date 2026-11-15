# w4-w5-q5-surgery-20261115 — bounded-edit surgery at the (5,5) and (4,5) q=5 frontiers

Bounded-edit witness surgery (the machine built for `eight-row-q9-m29-surgery-20261115`,
same code, pruning lemmas L1/L2/L3 with proofs recorded there) applied to the two
smallest open q=5 witness frontiers. One lower-bound update and one local negative.

## (5,5) m=24: 22 witnesses, M_{5,5} >= 25 (main result)

Prior state: witness band m=5..23 (19-stone single-deficiency, `four-six-row-q4-q5-witness-search-20261114`),
frontier m=24 INDET 90s. The band-extension lane had m=24 as its next target.

Seed: the m=23 witness (`seeds/s5x23q5_HVHVHV.witness.json`, rows [3,4,4,4,4], deficient
row 0). Embedding into 5x24 at offX=0/1, the empty cell of the deficient row is the unique
T' cell ((23,0) resp. (0,0)): every other empty cell lies on a (q-1)=4-stone curve of the
seed, so maximality forces exactly one new stone in the deficient row (lemma L3).

Complete enumeration of final states F = seed ∪ P \ Rm with |P| <= 2, |Rm| <= 2
(|F| <= targetMax = w(q-1)-1 = 19):

| run (board 5x24) | safe leaves | maximal | witnesses |
|---|---|---|---|
| offX=0, (2,2) | 20,732 | 2 | 2 |
| offX=0, (2,3) | 114,577 | 2 | 2 |
| offX=1, (2,2) | 19,176 | 16 | 16 |
| offX=0, (3,3) | 2,964,891 | 6 | 6 |

Union: **22 distinct witnesses**, all 19 stones, rows [3,4,4,4,4], deficient row 0.
Nearest witness is at edit distance 2 from the seed embedding: one stone removed,
one added (witness index 2 vs seed@offX=1, `+1/-1`). So the (5,5) band extends by
a single-stone relocation, unlike the (8,9) band where witnesses sit 46-80 apart.

**Witness band m=5..24 => M_{5,5} ∈ [25, 336]** (upper U_{5,5}=336 unchanged, K0318).

Verification, all 22 (`output/q55_m24_witnesses.json`):
- surgery.js final check (complete curve census safety + per-empty-cell maximality)
- `verify_witness.py` (Python Fraction, the repo's canonical verifier) — 22/22 PASS
- `verify_witness_int.py` (integer-exact cross-multiplied second implementation,
  validated against the canonical verifier on known band witnesses + cluster sample,
  `eight-row-q9-m29-surgery-20261115`) — 22/22 PASS

Raw run records: `output/q55_m24.jsonl` (4 summaries + witness events, deterministic machine).

## (5,5) m=25: local negative (not absence)

All 22 m=24 witnesses used as seeds, each embedded at offX=0/1 in 5x25 with
(2,2) and (2,3) (94 runs total; the three archived seeds 0/2/18 additionally at
(3,3) both offsets, 6 runs): **0 witnesses**. The m=24 cluster does not chain to
m=25 within edit distance ~4-6 of these seeds. LOCAL ONLY: distant witnesses are
not excluded; m=25 remains the open frontier.

Raw run records: `output/q55_m25_local_negative.jsonl` (94 summaries, all nWitness=0;
seed index i refers to `q55_m24_witnesses.json` witness i embedded at offX 0/1).

## (4,5) m=21: local negative (not absence)

Seed: m=20 witness minus its row-3 stone (14 stones; the empty (19,3) is the unique
T' cell at offX=0 — a "rowY=3" anchor mirroring the eight-row construction).
`seeds/ctrl45_seed.json`. targetMax = 15.

- Positive control: 4x20 (2,2) from the 14-stone seed **re-finds the m=20 witness**
  (1 witness, 54 ms) — the machine rediscovers a known witness from a 1-stone hole.
- 4x21 complete enumerations: (2,2), (2,3) offX=0/1; (3,3) offX=0 (8.5 s);
  (3,4) offX=0 (35.8 s) — **all 0 witnesses**.
- (4,4) offX=0 exceeded the 220 s session cap: incomplete, **no claim**.

LOCAL ONLY: 4x21 remains INDET (band-extension lane). Raw: `output/q45_m21.jsonl`.

## Machine

`scripts/surgery.js` — identical to `eight-row-q9-m29-surgery-20261115` (v2 with the
L3 occupancy fix); usage `node surgery.js <w> <q> <m> <seed.json> <maxP> <maxRm> <targetMax> [offX]`,
seed JSON `{"stones":[[x,y],...]}`. Deterministic (no RNG).

## Status ledger

- M_{5,5}: 24 -> **25** (witness band m=5..24; frontier m=25).
- M_{4,5}: unchanged [21,140]; m=21 local negative recorded.
- All bounded-edit claims here are complete enumerations over the stated edit
  neighborhoods — they are existential positives (witnesses) or local negatives,
  never absence claims for the full board.
