# 2026-11-18 N11 検証側: cost-16 parent A16/B16の第三実装（Node.js）クロスチェック全一致

## 背景

cost-16 parent（`00000000000000003800000008001000`・31行）のphase A/B最小cover計数A16/B16は、これまで2つのPython実装（checkpoint `d2901d15`のfresh-slice方式・shared-memo crosscheck `5bdc86f1`〜`45b1266f`、amendment後blob `41d37ed8`）で一致が確認されていた。本作業は言語と記憶方式の両面で独立な**第三実装（Node.js 22.20.0）**による全値再現である。

## 実装（node_crosscheck_cost16_ab_20261118.mjs）

- 31行のtarget行をpinned worklist/census/ledgerから再導出（census pinはamendment修正後の正pin）。
- 候補rootを整数det4で再生成し、D4正準化はBigInt maskで実施（JS Numberは121bit不可のため）。行ごとの候補数はpublished edge_costと31/31一致。
- 重み付きperfect matching計数はlazy memo DP。**DP内部のpm値はJS Numberで保持し、全値 < 2^53 を実行時にassert**（検証した範囲で最大pm値は1,798,095,446,108,235 < 2^53 ≈ 9.0e15）。Number演算は2^53未満で厳密なのでDPは終始厳密。
- 外側の積和（B_d・A16・B16）はBigIntで蓄積。B_d（31値とも2^53超）に丸め誤差なし。

## 実行方式（crosscheck_cost16_node_third_impl_20261118.py driver）

- **B slice 31本・A slice 31本はそれぞれ別nodeプロセス・完全なfresh memo**で実行（published両方式とも異なる記憶戦略。B slice各~8s・3.52M states、A slice各~2s）。
- 11行アンカー（cost-6 parent）: A=337,020・B=22,590・total=359,610・per-row singleton/ways10 11/11・**全757 rootのmembership（A型/B型別）がpublished membership outputと全一致**・Σmembership == 6×totalの恒等式も成立。B型membershipの3ケース（doubled行が第3行 `dp2[R][5]`・d=a `pm(full\\{b})`・d=b `pm(full\\{a})`）はpublished定義を正確に再現。
- driverはresumable（予算240s/実行・中断後再開可）。slice中間JSONは`output/node-third-impl-slices/`（公開せず）。

## 結果（82 checks all PASS・assemble二重実行byte-identical）

- **A16 = 2,305,787,291,293,934,388・B16 = 660,663,050,386,546,968・total = 2,966,450,341,680,481,356** — published両実装と完全一致。
- B_by_d 31値・degree/anchors 31組・A per-row pm 31値・singleton計数31値すべて一致。
- graph構造（31行+cost・候補発生2333・distinct root 1908・被覆ヒストグラム{1:1483,2:425}・pair型425・重複度{1:425}・singleton 1483・per-row次数）すべてpublishedと一致。
- fresh-memo slice 0の状態数3,524,183はpublished shared-memoのd=0後累積状態数と一致（以降はfreshが毎回~3.52Mでsharedが累積9.2Mへ成長する差が可視化される）。

## 解釈境界

A16/B16は31行の最小certificate-cover計数という計画簿記であり、cover意味論（root=行の1石D4正準形拡張候補）が各rootのcertificate妥当性を前提とする。どのrootもcertificateとしては未検証。REFUTED-D10とSTERILEはLOSS証明ではない。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべて**UNKNOWN**のまま。

## 成果物

- 第三実装: `node_crosscheck_cost16_ab_20261118.mjs`
- driver/verifier: `crosscheck_cost16_node_third_impl_20261118.py`（82 checks）
- output: `cost16-node-third-impl-crosscheck-20261118.json`
