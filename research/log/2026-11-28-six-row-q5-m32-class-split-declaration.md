# 宣言: six-row q=5 6x32 class-split 直接評価 (単一オーナー・publish-then-execute)

- 日時: 2026-11-28 (UTC)
- 宣言時 HEAD: `5cc8e1fb8932c48d078a01981c027ef40029b2bc` (最新 main 再取得済み)
- オーナー: 高速レーン・本 session (単一オーナー)。同一タスクの並走 session は着手前に最新 main を再取得し、push 競合・同時書込み時は無理に押し進げず記録して次回に回す。

## 対象

(6,5) 未解決前線幅 **6x32** の行欠損極大安全配置 (def-mode witness) の SAT 側直接評価。
現状: M_{6,5} ∈ [32, 658] (K1216: 6x31 witness は純並進で確定済み・6x32 は手術系 rem≤4/add1・rem3add2 targeted (c009@off3 のみ) が陰性、UNDETERMINED)。class-split/krow/minpos 分解は未実施 (本宣言が初)。

## 手法

- 符号化: 出版済み six-row-q7-m22-class-split-20261127 kit の `sat3.js`/`sat2.js`/`sat.js`/`verify_frac.py` を byte-clone で使用 (sha256 pin は kit MANIFEST と照合)。q 一般化符号化 `node sat3.js 6 m 5 --class=D --krow=y:3 [--minpos=P]`。
- solver: kissat 4.0.4 公式 linux-amd64 binary (sha256 `21da5d984e38b74f620f14c62442f834f27b9158decdb722540d97f98aac93a1` を検証して使用)。
- 分解: 行ミラー V (y↔5−y) 正準類 {0},{1},{2} (欠缺行 y の類)、単一欠損 (欠損行の石数ちょうど k=3=q−2)、minpos=0..15 (m=32 の sound H-split、floor((m−1)/2)=15)。各片 cap 275s。深欠損 (k≤2)・複数欠損行クラスは本宣言の範囲外 (未掃引として開示)。
- 陽性対照: 6x31 class {0} krow=0:3 (plain) が SAT であること (既刊 6x31 witness の V 像 hits を期待・conflicts は初回観測をそのまま記録)。
- 決定性: 決着片は cold pair 2 走 (conflicts と model v-lines byte 一致)。

## 受入条件・結果の扱い

- いずれかの片が SAT → witness を decode し sat.js `verifyConfig` + fresh Fraction 検証器 `verify_frac.py` の 2 系統で safe+maximal を確認 (tamper 陰性対照つき) → **M_{6,5} ≥ 33** (下界のみ更新・上界 658 (K0806) 不変・mwq_stabilization.csv は不変 (K1201 前例))。WIN-stop 則で最初の SAT 後の残片は抑制可。
- 全片 UNSAT → 6x32 class {0}/{1}/{2} 単一欠損 minpos 0..15 の有限非存在 (範囲限定・深欠損等への拡大なし、全体不在主張はしない)。
- 片が cap で INDET → 正直な負として記録 (不在主張に数えない)。
- conflicts 数は bookkeeping。標準 11x11 空盤・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN・verdict 不消費。

## 事前開示

- 宣言前に本対象 (6x32 q5 class-split) の計算は未実施 (repo 検索で 6x32 class-split の前例なし・宣言済み単一オーナーは 6x23 q7・6x26 q6 multidef・7x28 q7・7x38 q5・5x28 q5・(6,8) band のみで本対象と不重複)。
- 宣言 push 後に実行する (publish-then-execute)。
