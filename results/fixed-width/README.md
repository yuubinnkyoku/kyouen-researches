# 固定幅盤の横断結果（P(w) と M_{w,q}）

標準整数格子の固定幅 w×m 盤（q点共円・共線禁止版）の横断集計。
命題の唯一の正本は [knowledge](../../research/knowledge/README.md)。
ここにある数値は K0795 の時点の集計資料であり、P(w) や閾値が改訂された場合は
本表も更新が必要（出典は各行の source 列）。

- [pw_circle_point_max.csv](pw_circle_point_max.csv): 円の格子点数の確定値 P(w)（w=6..82・全 m≥1・全称・等号付き）。
  16プラトー w=12..21・跳躍帯 w=22..25・24プラトー w=26..42・漸増帯 w=43..48・32プラトー w=49..82。
  出典: K0763..K0767, K0778, K0784, K0788, K0789, K0790, K0792, K0793, K0794, K0798, K0799, K0801, K0802, K0804。
- [mwq_stabilization.csv](mwq_stabilization.csv): 真の満容量安定化長 M_{w,q}。
  - `exact-threshold`: 確定値 8 件（(2,4)=9・(3,4)=24・(3,5)=12・(3,6)=9・(4,6)=16・(4,7)=13・(4,8)=11・(5,8)=16）。
  - `bounds`: open な境界 6 件・いずれも両側（(5,6)=19..249・(5,7)=19..158・
    (6,5)=28..658・(6,6)=22..495・(6,7)=20..402・(6,8)=18..371）。
    (5,6)/(6,5)/(6,6)/(6,8) の下界は K0808/K0809 の貪欲witness に加え
    K0810 のSAT探索と K0811 のSA探索による検証済み欠損極大witness
    （24石@5×18・23石@6×27・29石@6×21・41石@6×17 が最大、
    すべて census 不使用独立検証で safe+maximal PASS・K0809 の候補予想 M=16/22/17/12 を全て反証）。
    上界は K0318 代入（(6,7) の402は K0806 による初の明示的記録）。
  - `separation-band`: 行分離公式 M_{w,q}=q−1 が全 m≥1 で成立する合成分離帯
    `q ≥ max(P(w), w)+1`（w=6..82・P(w) 確定幅。K0767 の系と P(w) 確定値の合成）。
    全安全局面で g(S)=(w·min(m,q−1)−|S|) mod2。
  - `parametric`: P(w) が未確定の幅（w≥83 を含む）に効く既証明の無限族
    （K0025・K0072・K0776・K0784）。
- 整合性検証（289点の文書化済み (w,q) が全て合成分離帯に包含・P(w) 単調）:
  [mwq_results_check.ts](../../research/experiments/mwq-results-integration-20261113/scripts/mwq_results_check.ts) /
  [output](../../research/experiments/mwq-results-integration-20261113/output/mwq_results_check.json)。

注意: separation-band の数学的内容は K0767 の系（q>P(w) かつ q>w ⟹ 行分離）と
各行の出典 K 項目が証明した P(w) に完全に依存する（K0795）。
