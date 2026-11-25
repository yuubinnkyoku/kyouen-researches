# 2026-11-14 深除去列拡張（extend6）による (6,5)(6,6) 前線突破

高速レーン第7回。実験正本: [research/experiments/extend6-deep-removal-20261114/](../experiments/extend6-deep-removal-20261114/report.md)
（K0815 第5弾として統合）。

## 成果

- **M_{6,5} ≥ 31**: 6×30 q=5 に 23石欠損極大witness 2件
  （6×29 23石base から rem=4/add=4・off=1・行 4,4,4,4,3,4）。
  SA 14 run・kissat 複数回・列追加拡張（K0815 第1弾）が不発だった 6×30 を
  深除去（r=4）で突破。M_{6,5}=30 可能性を反証。境界 [31,658]。
- **M_{6,6} ≥ 24**: 6×23 q=6 に 29石欠損極大witness 8件
  （6×22 29石base から rem=3/add=3・off=0/1・行 5,4,5,5,5,5）。
  境界 [24,495]。
- いずれも JS census 不使用 verifyConfig + Python Fraction 独立検証器の
  2系統で safe+maximal PASS。repo 版 extend6.js（パスの環境変数化）
  での再実行で distinct 2件・8件を再現。
- 較正: 6×28→29 r=0・6×21→22 r=0 で K0815 の既知witnessを再現。
- 陰性（pool相対・ただし uOverflow スキップが支配的で証拠力は限定的）:
  6×31 q=5 r≤5 ← 30base 0件（leaves 44,552・uOverflow ≈99.8%）、
  6×24 q=6 r≤4 ← 23base 0件（leaves 27,841・uOverflow ≈99%）。

## 運用の記録（次回レジューム用）

- 実行環境リセットが本セッション中に2回発生し、作業dir（krwork）が都度消滅した。
  成果は stdout 経由で本文に残すか即 push する運用が有効だった。
  本エントリの分はリセット後に witness JSONL（extend6_*.jsonl）と
  found.jsonl が残っていたため復元できた。
- GitHub API 無認証枠（60/hr）が枯渇した場合は raw + SHA 指定取得で回避できた。
- extend6.js の u>24 / maxA>6 の葉スキップ（uOverflow）は、幅の広い target
  （targetM ≥ baseM+2）では支配的になる。6×30・6×23 では1葉のみ完全列挙で
  witness に到達した一方、6×31・6×24 の陰性はほぼ全葉がスキップ。
  次の一手: maxA 制限の緩和（u の bitmask を 2語に分割）、または
  6×31/6×24 を SA/kissat の直接探索に回す。
- push 前に最新 main を再取得したところ、並走レーン（n11 class2-lane・
  素数census・encoding-symmetry）が K0815 を第4弾まで更新済みだった
  （6×12 q=8 最小極大=37 確定・K0816 新設）。本成果は第5弾として追記し、
  重複なし。次の空き K 番号は K0817。
