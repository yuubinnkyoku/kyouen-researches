# 中心・隅rootのs4 cover

奇数n≥5の構造的最小class数と、n11の31-class skeletonの独立証明。
現在の結論は [K0335](../../knowledge/items/K0335-center-corner-s4-cover-exact-all-odd-squares.md)、
全称証明と検証境界は [report](reports/center-corner-cover.md) を参照。
全safe classを候補とする問題であり、各classの勝敗を判定しない。
11×11空盤の勝敗はUNKNOWN。

```sh
python research/experiments/n11-cover-duality/scripts/generate_cover.py
python research/experiments/n11-cover-duality/scripts/verify_cover.py \
  research/experiments/n11-cover-duality/output/center-corner-cover.json \
  --mutation-checks \
  --output research/experiments/n11-cover-duality/output/verified.json
```

生成器は共有整数geometryとD4を使い、検査器は別の整数行列式と八つの
座標変換で全safe classを再構成する。最適下界は分母2の整数dualで検査でき、
MILPのoptimalラベルを信頼する必要はない。追加依存パッケージは不要。
