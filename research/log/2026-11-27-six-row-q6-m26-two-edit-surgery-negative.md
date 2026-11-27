# 2026-11-27 (6,6) 前線 6x26 two-edit surgery 負 (高速レーン)

単一オーナー宣言

[2026-11-27-six-row-q6-m26-two-edit-surgery-declaration](2026-11-27-six-row-q6-m26-two-edit-surgery-declaration.md)
(宣言時 HEAD `76181b40`・宣言 commit `26c25331`)の下で実行。実験キット:

[six-row-q6-m26-two-edit-surgery-20261127](../experiments/six-row-q6-m26-two-edit-surgery-20261127/)

(commit `7081aa2b`・fetch-back 19/19 sha256 byte 完全一致)。

## 結果

- **6x26 完全 two-edit surgery 負**: K1217 の 6x25 witness (29石・rows [5,5,4,5,5,5]) を種に、
  6x26 ボードで **836,890 一意候補・safe 0・safe-maximal 0**。
  m=25 witness の <=2 編集近傍に 6x26 witness なし(局所的負・不在主張ではない)。
- 種は 6x26 で一石不足: 未遮断セルは **T=(25,2) のみ**(crunch kit crosscheck の
  not-maximal (23,2) は bbox 正規化座標系・raw 配置では (25,2) と機械特定)。
  T-curve census c3=3・c4=3(遮断閾値 5・need<=2 の場合分け完全)。
- **M_{6,6} ∈ [26, 495] 不変・前線 6x26 のまま**。csv (6,6) 行 note 追記済み。
- 観測: m=25 witness は両 m=24 witness (K1215 class{1}/class{2}) から
  4鏡像 x 全並進で sd >= 34 (>= 17 手)。連続幅 witness ジャンプは大きい
  (five-row m=26/m=24・seven-row m=32 レーンと同型)。

## 検証 (詳細は kit README)

- 器具は出版 7x32 q=6 エンジン (`surgery_m32.py` sha `fe277e8a...`) の Q・盤面汎化
  fresh 実装。**較正**: 出版 m=31 seed・T=(31,3) 構成で出版 `surgery-m32.json` の
  candidates 2,224,675 / safe 0 / witnesses 0 / T-curve c4=1 c3=10 を完全再現。
- 決定性 2 走 byte 同一 (run1=run2 sha `7cfe56c7...`)・環境 reset を挟んだ
  cross-reset 再現も同一 sha。
- 独立整数 conic 検証器 (method-disjoint) でエンジン棄却 300/300 を再確認
  (missed witness 0・単体対照: 3点円の格子点集合・6点共線の unsafe 判定)。
- tamper 電池: T1 target 遮断済みセル -> fail-closed・T2 seed 不安全化 -> fail-closed
  (seed unsafe)・T3 safety gate 緩和 -> 計数同一 (sha pin で検出・開示)・
  T3b blocking gate 緩和 -> fail-loud (spurious 64,262・計数発散)。

## 正直な開示

- 宣言前に予備実行(較正・予備列挙)を済ませ、宣言文に開示。公式記録 run は
  宣言 commit `26c25331` の後。
- 環境 reset 1 回で作業 tree を喪失(未出版)・main から再構築し公式 run をやり直し
  (reset 前 run と byte 同一)。以後の作業 tree は knowledge mount
  `_q66-m26-kit/` (reset 耐性)。
- m=24 -> m=25 rediscovery 陽性対照は sd >= 34 で不成立 (開示)。
- verdict 不消費。11x11 空盤・二石 root・第三手・S2・closure class は全時点 UNKNOWN。
  candidates/safe 数は bookkeeping。

## 次の実行可能課題

1. 6x26 の SAT 側: class-split (K1217 機材の 6x26 移植)・または 3 編集 surgery。
2. (7,32,6) class {3} 深い単発 kissat (長時間 cap 環境) は q6 7行レーンのまま。
3. (6,7) 6x22 (m=21 witness 35石からの two-edit surgery は未着手)。
