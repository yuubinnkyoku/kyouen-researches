# 単一オーナー宣言: n11 residual72 worker-partition割当目的関数の精密閉包とUB witness測定（2026-11-21）

- 宣言: 2026-11-21T13:50Z（本ノートの出版が宣言時点）
- 宣言時 HEAD: 直前確認 `3ceba86b`（three-row q4 K0351 replay session log出版直後・push前に再取得して確認する）
- レーン: `research/experiments/n11-residual72-worker-partition-exact-closures-20261121/`
- 並走上の位置づけ: 本レーンは既出版の一次素材のみを使う2次測定であり、
  掃引オーナーレーン（driver・runner・roots・residual72・output）・reply27 S5 probe レーン・
  seven-row/three-row q4 レーン・36root exact-class-membershipレーンのいずれのファイルにも触れない。
  worker partition candidateレーン（`f7466198`・「one-swap local optimum, not a global optimum」と明示）と
  exact-class-membershipレーン（`432db238`・クラス計数のみで最適値なし）が残した2つの測定ギャップ
  （割当目的関数の大域最適値・下界）を埋める。
- 透明性: 計算・独立検証は本セッション内で宣言前に完了している（別レーンとの衝突余地は出版時点まで存在しない。
  本ノートは出版4部構成の素材の単一オーナー宣言であり、同時実行の同一レーンに本素材を主張しないよう求めるもの）。

## 本レーンが出版するもの

1. **精密閉包（B&B）**: W∈{2,3}のbalanced割当についてclass10/pair10両目的の大域最適値を確定
   （732/737・908/913。UB未満の全割当を列挙する閉包であり、閉包時のみ大域最適を主張）。
2. **UB witness（非閉包の正直言報）**: W=4 class10 1937 / pair10 1939 / cross9 47を同一分割が同時達成
   （super-witness・T2非適合: d4 spread 10.79% > 8%）、W=6 2558/2562、9石層0、47。
   いずれも大域最適性は主張しない。B&B node数・予算は実行条件として記録。
3. **1-swap証明書**: T1（制約なし）486 feasible / 3 improving / best 13↔19 → 1937/1939。
   T2（8% cap）222 / 0 / 1998・2000（出版one_swap_checkの完全再現）。
   T1/T2大型anneal（1,500・2,500 restarts）でも1937・1939・1998・2000を破れず、
   **T2大域最適性はUNKNOWNのまま**と明記。
4. **独立検証器**: 入力5点pin・目的関数のraw再構築・出版candidate統計・exactclass partition_stats・
   全witness再計算・閉包表記・same-partition性・super-witness性・T2非適合の全142 gate。
   出版レイアウト（repo rootから実行）での再実行が結果JSON byte-identicalであることを確認済み。

受入条件は上記のとおり全て満たしている。pushごとに最新main再取得・自path非接触確認・
fetch-back byte照合を行う。K itemは作成しない（candidate・exact-membership両レーンと同じ
探索的測定系の先例に従う）。

## 非目標

- 掃引オーナーレーンへの関与・割当変更の提案・適用は一切ない（super-witnessはT2非適合であり、
  実測TT hitもない段階でsweep割当の根拠にはしない）。
- 勝敗・行閉鎖・root資格・S6行の簿記は一切変更しない。
- W=4/6・x9の閉包主張は行わない（強LBまたは別手法が必要）。

## 解釈規約

幾何的クラス重複は実探索費用・表命中率ではない。nodes数・目的関数値を勝敗として読まない。
REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 verdictsはすべてUNKNOWNのまま。**
