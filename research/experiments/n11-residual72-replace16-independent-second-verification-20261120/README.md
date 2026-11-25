# n11 残余72行 代替16根 depth-10掃引の独立第二検証（2026-11-20）

K1089の32 probe記録と、K1085→K1086→K1088から引き継いだ残余49行・代替16根の幾何を、元の掃引機械とは別の実装で照合する。対象は公開済み記録の整合性であり、DFPNエンジンの再実行ではない。

## 入力の固定

- K1085: `5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e`
- K1086: `3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`
- K1088: `16b38d04a488617b1b8c002c6a5f3171038f557cd3cca8b8e4dbd4657bc2f724`
- K1089: `808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc`
- runner v17 Git blob: `c132cc6425eee3feaeef1d697dd74f968cfedb59`

## 結果

**16/16 gate PASS。** D4正準形・整数行列式・72行の分割・49行のちょうど1回被覆・32 probeの未打切りと順序整合を確認した。16根の1,120四点組、72基底行の1,080四点組を検査。WIN8-D10 candidate 3根、REFUTED-D10 fact 13根、総節点6,339,079、最大878,391。

この検証器はrunner v17を再実行しない。探索器の正しさや32件すべての探索過程を独立に証明するものではなく、公開済みの探索記録・入力固定・幾何・集計の二次照合である。

- WIN8-D10 candidateは証明書ではない。receipt foldもS6行の閉鎖も行っていない。
- REFUTED-D10はLOSS証明ではない。
- 標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はUNKNOWNのまま。

再現: `python research/experiments/n11-residual72-replace16-independent-second-verification-20261120/verify_replace16_second_20261120.py`
