# 2026-11-14 six-row q8 m21 row split（並走高速レーン）

6x21 q=8 行欠損極大配置の非存在を、rowY 3クラス分解で確定した（K0829）。
双子レーン（毎時run）とは独立のrunで、着手前に最新main・既存成果（K0818/K0819・
K0825-K0827）を確認し重複を回避した。

## 実施内容

- 6x21 def-mode OR 実例（ある行 ≤ 6 石）: kissat 4.0.4、240s cap で **INDET**
  （5,011,833 conflicts）。正直な負記録として生ログ保存。
- rowY 行固定分解: 欠損行 y の3ミラークラス y=0,1,2（V対称 y↔5−y で6行を完全被覆）
  を `sat2.js --rowY=Y` で走査。**全3クラス UNSAT**（327,636 / 2,862,649 /
  1,767,690 conflicts）。被覆論: 欠損配置は必ずある行fixed実例の解として現れ、
  ミラー健全性（K0818で小盤面brute-force検証済み）で3クラスが全行を被覆する。
- 最難クラス y=1 を `--lex=H`（列鏡映lex-leader・rowY保存で健全）で再符号化し
  **UNSAT**（2,337,998 conflicts / 144.0s）— 第二符号化交差確認。
- 陽性対照 6x18 def-OR: **SAT** 492,432 conflicts、41石 rows [7,7,7,7,6,7]
  （K0815盤面の行鏡映）。sat.js census-free verifyConfig と Python Fraction
  `verify_witness.py` の2系統で safe+maximal+欠損 PASS。
  注意: 本対照は sat2.js def-OR 実例で、K0818/K0819 の sat3.js クラス{1}対照
  （511,895 conflicts）とは別実例（conflicts は直接比較不可）。

## 結論

- 6x21 に行欠損の極大安全配置は存在しない → witness-free 幅集合 **{19,20,21}**、
  **M_{6,8} ∈ {19,20,21} または ≥ 23**、上界 371 不変、witness 探索前線 **6x22**。
- CSV（results/fixed-width/mwq_stabilization.csv）(6,8) 行を更新。
- K0819 が予告していた分岐（frontier 6x21 の witness-free ⇒ free set {19,20,21}）
  を解決。

## その他（未反映・双子との重複）

- (7,9) 帯延長 m=101..112 の独立run再現は双子の記録と conflicts 12/12幅 bit-exact
  一致（較正 m=100 の 18,075 も一致）。双子が m=200 まで完了済みのため
  傍証価値のみで、重複として push していない。
- (7,4) m=22..27 kissat SAT（20石）は双子の構成的 m=35 拡張（K0827・M_{7,4} ≥ 36）
  に完全包摂されるため push していない。
- (7,7) m=27 rowY=3 + lex=H,V,HV も INDET（2,239,989 conflicts・265s・lex効果なし）。
  生ログは環境リセットで喪失、数値のみ本ログに記録。単発290sでは完結不可。

## 11x11 接続

rowY 分解は class 2 / class 4 レーンの枝刈りには直接効かないが、
「def OR が抵抗する幅で row 分解が予算内で反証できる」パターン
（(7,7) m=25/26 SAT 側と今回 (6,8) m=21 UNSAT 側）の両側実例が揃った。
11x11 の per-row 制約が必要な場面で再利用可能。

## 環境メモ

実行環境リセットを1回経験（成果は逐次push済みのため喪失なし）。復旧後に
scripts を main から再取得し、対照 witness の Python 検証を再実行して
records.jsonl の pyVerify フィールドを確定した。
