# 全残余hypergraphの交換可能class kernel

現在の正本はK0344。全辺族を保存する内部二点交換を条件に、classを内部容量か
混合深さ付き偶奇へ圧縮する。通常Grundyとmisère補助mexを別々に保存する。

- [通常プレイ証明](reports/exchangeable-kernel.md): 全称帰納・安価な検出・n11の測定と限界。
- [misère証明](reports/misere-kernel.md): 終端値1の補助mex保存。成分xorを使わない。
- [全rank最良性](reports/rank-sharpness.md): 誘導点削除kernelの上限が全rankで鋭い証人族。
- [独立監査](reports/independent-kernel-audit.md): 別count-subset定式化の全称証明と検算。

```sh
python research/experiments/n11-reduction-followup-20261005/scripts/verify_modules.py \
  --samples research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json \
  --output /tmp/n11-module-audit.json
python research/experiments/n11-reduction-followup-20261005/scripts/independent_count_audit.py
python research/experiments/n11-reduction-followup-20261005/scripts/verify_sharpness.py
```

標準ライブラリと既存の全残余更新・整数幾何を再利用する。全小clutterと保存実局面を
別の占有subset mexで確認する。全称結果の根拠は証明であり、greedy標本は完全列挙ではない。

Python prototypeはmemo状態を減らしたが測定実時間を増やした。
共有df-pnの速度改善は主張せず、11×11空盤勝敗はUNKNOWN。
