# (7,4) m=41 SAT で下界42 — sat3 dedup修正とソルバRAM壁の記録

Date: 2026-11-15
Lane: 高速レーン（witness-band-36-40 の続き）
Experiment: research/experiments/seven-row-q4-band-41-20261115/ (main push済み)

## 結果

- **m=41 SAT**（sat3 + kissat 4.0.4・281 conflicts・39.0s・8,704,218 clauses）。
  witness 20石・rows [3,3,3,3,3,3,2]・js+py 2系統検証 PASS。
  **M_{7,4} ∈ [42, 1929]**（下界42に更新・前線 7×42・未実施）。
- sat3 の dedup を ≥q点円のみ登録に修正（出力不変・q点未満の円は三つ組が1つ
  しかないため再遭遇しない）。byte-identity を小規模4対照 + 保存済み m=28/m=40
  CNF との cmp 一致で再検証。m=50 生成が 11.6s/305MB CNF で可能に。
- **ソルバRAM壁**: kissat は ~9M clauses（本コンテナRAM）でパース中に OOM kill
  （m=42: 9,337,618 clauses・13s・m=50: 15.5M clauses・2s・いずれも不在主張ではない）。
  witness 探索の続行には大メモリ環境・節削減符号化（対称性破壊強化・変数分割）・
  または構造論証が必要。

## 知識反映

- K0827: artifact 追加 + 追記。
- mwq_stabilization.csv: (7,4) `41..1929` → `42..1929`・frontier 7x42。
- results/fixed-width/README.md: (7,4)=42..1929・欠損witness 7×4..7×41・前線 7×42。
