# seven-row-q6-m32-surgery-negative-20261115

高速レーン。(7,6) 前線 **7×32** に対する 2 編集 surgery 完全列挙の**有限完全負記録**。

## Claim

- 種: (7,6) m=31 witness（34 石・rows [5,5,5,4,5,5,5]・
  seven-row-q6-m31-frontier-20261115・3 系統検証済み）。
  7×32 で唯一の未遮断セルは T=(31,3)（probe_free_column.py）。
- 手法: surgery_m31.py の 7×32 への直接移植（surgery_m32.py・同一アルゴリズム・
  完全最終状態場合分け・純 Fraction・自己テスト組み込み・repo コード不使用）。
- **結果: 2,224,675 一意候補・safe かつ maximal 0 件**（31s）。
  T=(31,3) センサス: c4=1（直線 y=3 のみ・空セル 27）・c3=10。
  m=31 を遮断した c4 円 {(22,2),(23,3),(25,4),(28,4)} は (31,3) を通らない。
- **対照 PASS**: 同一コードを m=30 witness seed・7×31・T=(30,3) に戻した
  レプリカ（control_m30seed_replica.py）が m=31 記録を完全再現
  （curves 5342/88/29・census c4=2 c3=11・2,140,633 候補・unique witness
  R={(19,2),(25,4)} → A={(27,2),(29,4)}）— end-to-end 陽性対照。

## 解釈

- m=31 witness の ≤2 編集近傍には 7×32 witness が存在しない（有限完全負記録）。
  m=29→30（1,781,021 候補・0・3 系統合意）と同様の疎分布観測。
  **7×32 全体の不在主張ではない**。
- M_{7,6} ∈ [32, 862] 不変・前線 7×32 のまま。
  残るルート: class {3} (7,32,6) SAT・3 編集 surgery・別 seed。

## Not claimed

- 7×32 全体の不在・(7,q≠6) 家族・Grundy 値・11×11 関連（すべて不在主張なし/UNKNOWN）。

## files

- scripts/surgery_m32.py — 7×32 移植本体（自己テスト組み込み）。
- scripts/control_m30seed_replica.py — m=30 seed 陽性対照レプリカ。
- output/surgery-m32.json / surgery-m32.log — 本体記録。
- output/control-m30seed-replica.json / control-m30seed-replica.log — 対照記録。
