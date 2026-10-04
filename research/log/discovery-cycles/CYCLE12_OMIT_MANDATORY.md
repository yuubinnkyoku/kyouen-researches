> **研究履歴**：本文の判定・数値・計画は記録時点のものです。現在の結論・未解決・検証境界の唯一の正本は[knowledge](../../knowledge/README.md)です。この資料を現在知識の正本として並行更新しません。

# Cycle 12 addendum — omitting mandatory orbit (0,2) on n=7

COMPLETE: max safe size with orbit `(0,2)` forbidden is **12**
(`cycle8_b_maxsafe.exe max 7 --forbid-orbit 0,2`, complete=true, 3464 at 12).

SAMPLE (`occ 7 12 --forbid-orbit 0,2 --max-nodes 3e6`):
- 3424 sets seen, **176 occupancy patterns**
- `(0,2)=0` by construction
- **(2,2) is frequently occupied** (replaces missing edge-2 stones)
- center orbit sometimes occupied
- corners span 0–3

## Reading

Omitting a mandatory orbit does **not** yield a smaller two-phase crystal.
The size-12 layer under `forbid (0,2)` is occupancy-rich (176 patterns in a
partial dump) and leans on the orbit `(2,2)` that is banned at K=14.

This supports the max-layer sharpness picture:
- K=14: highly selected, 2 vectors, empty (2,2)
- K=13 / forbid-mandatory@12: diffuse, many vectors, (2,2) in play

## Artifacts
- `results/cycle12_omit_02_sample.json` (Python DFS under-sampled; use exe occ)
- exe dump: see session log / `results/cycle12_occ_k13.json` sibling
- `research/log/discovery-cycles/CYCLE12_K13_LAYER.md`
- `research/log/discovery-cycles/CYCLE11_ORBIT_NECESSITY.md` (capacity table)
