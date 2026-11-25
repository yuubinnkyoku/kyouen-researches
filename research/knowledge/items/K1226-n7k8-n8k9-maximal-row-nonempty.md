---
id: K1226
title: 7×7 k=8 行・8×8 k=9 行の極大安全配置は非空虚（M_7 ≥ 8・M_8 ≥ 9）
kind: computation
status: computed
topics: [maximal-safe, geometry, sat]
aliases: ["n7 eight-stone maximal safe", "n8 nine-stone maximal safe", "M_7 >= 8", "M_8 >= 9"]
relations:
- type: depends_on
  target: K1224
  note: 7×7の7石行カタログ（16配置・2軌道）の SAT-convention lex-leader O1/O2 が at-most-k 行判定のブロック前提
- type: depends_on
  target: K1221
  note: enc_sat2 v2.1 lex-leader鎖の軌道被覆100%機械検査（leader-blocking 方式の正當性手段）
- type: depends_on
  target: K0032
  note: n=8 の k=8 行カタログ51軌道（D4閉包408を本環境で再検証）が n8 k=9 行判定のブロック前提
- type: depends_on
  target: K0212
  note: s_8=8（7石以下の極大安全不在）により at-most-9 の ≤8石モデルが51リーダーに限る
- type: extends
  target: K1225
  note: M_3..M_6=5/7/9/11 の確定に続き M_7・M_8 の下界を初めて上げた
- type: contrasts
  target: K1224
  note: 7石行の全16配置が三点共線を持つのに対し8石行には三点共線ゼロの配置が2軌道存在
artifacts:
- path: research/experiments/n7-rows-k8plus-sat-20261122/README.md
  role: source
  note: 主張・leader-blocking方式の健全性議論・較正・非主張
- path: research/experiments/n7-rows-k8plus-sat-20261122/output/determinism.json
  role: verification
  note: CNF sha256ピン・両ショット記録・検証記録の統合レコード
- path: research/experiments/n7-rows-k8plus-sat-20261122/output/census_k8_state.json
  role: data
  note: 8石行 bounded census の331 leader（完全性不主張・resume可）
- path: research/experiments/n7-rows-k8plus-sat-20261122/output/verify_census8_partial.json
  role: verification
  note: 331/331独立幾何検証・indicator-lex-min・重複ゼロ
---

# 7×7 k=8 行・8×8 k=9 行の極大安全配置は非空虚（M_7 ≥ 8・M_8 ≥ 9）

標準共円盤（q=4）について、**7×7 の8石極大安全配置**と**8×8 の9石極大安全配置**が
存在することを SAT（leader-blocking 方式）で確定し、witness を独立検証した。
どちらの行もこれまで未着手だった（K0030分布は6×6まで、K1224は7×7の7石行、
K0032は8×8の8石行）。

## 主張（有限計算）

1. **M_7 ≥ 8**: witness [[3,2],[5,2],[1,3],[5,3],[6,3],[0,4],[2,4],[3,4]]
   （0-based cell index [17,19,22,26,27,28,30,31]）。7×7初の8石極大安全配置。
2. **8×8 k=9 行は ≥2つの D4 軌道を含む**:
   witness1 [[7,0],[7,1],[0,2],[2,2],[7,2],[0,3],[1,3],[0,6],[1,7]]、
   witness2 [[6,2],[2,3],[6,3],[7,3],[2,4],[3,4],[4,4],[1,5],[2,5]]
   （互いに非合同・両方とも独立検証済み）→ **M_8 ≥ 9**。
3. **7×7 k=8 行の軌道数は ≥331**（bounded census・打ち切り・完全性不主張）。
   全331 leader を独立Python幾何（Fraction 4×4行列式・単体検査済みoracle）で
   SAFE+MAXIMAL・indicator-lex-min・重複ゼロを確認。軌道サイズは 8 が330件に
   加え**安定化群位数2の軌道が1件**（180°回転不変 `[3,6,14,19,29,34,42,45]`）
   — 7石行の全16配置が自明安定化群だったのと対照的。
   **三点共線ゼロの8石配置が2軌道** `[10,12,15,20,25,27,42,45]`・
   `[10,12,14,23,39,40,45,46]`（7石行は全配置が三点共線を持つ、K1224）。
   trip/dirs ヒストグラム（331 leader 上）: trips {0:2,1:34,2:119,3:131,4:36,5:8,6:1}・
   dirs {0:2,1:40,2:126,3:123,4:36,5:3,6:1}。

## 方式の要点

- enc_sat2 v2.1（出版正本・byte同一）at-most-k に、既知の小さい行の
  lex-leader をブロックする7/8リテラル節を付加:
  n7 は O1/O2（K1224）、n8 は51リーダー（K0032/B371 出版51代表の
  D4閉包408を再検証のうえ SAT規約 indicator-lex-min を計算）。
  Sinzカウンタがone-wayのため「単位節でexactly-k」は不健全（逆充足を許す）で
  あり、leader-blocking が行判定の健全な手段（詳細は実験README）。
- 較正: ブロックなし at-most-7 は O1 を即返す（24.8s・陽性対照）。
  O1+O2 をブロックした at-most-7 は UNSAT（51.8s）で「≤7石モデルは O1/O2 のみ」
  を本環境で再導出。
- 両判定とも default と --shuffle=42（独立変数順序・ブロック節も同順序で再計像）
  の2ショットで同一結論（n7: 同一witness・n8: 異なるwitnessだが両方検証済み）。
- witness は出版正本 verify_witness.py（整数学・独立実装）で
  SAFE+MAXIMAL、1石除去の tamper は全件 SAFE かつ NOT-MAXIMAL。
- kissat 4.0.4 は公式 binary を md5/sha256 ピン（repo 内再出版なし）。
  CNF 本体は非刊行・sha256 は determinism.json にピン、決定的再生成可。
- census の決定性スポット検査: 先頭20反復の leader 列は再実行で完全一致。

## 非主張

- 331件の census は打ち切りであり、7×7 k=8 行の軌道数の正確な値ではない
  （≥331 のみ主張）。n8 k=9 行の census も未実施（≥2軌道のみ）。
- M_7・M_8 の上界は扱わない（k=9..13行の判定には各行の完全leader censusが前提）。
  有限計算であり形式証明ではない（実装・kissat・符号化の trust 込み・K1224/K1225 と
  同水準）。
- 標準 11×11 空盤・二石 root・S2・closure class は本レーン非接触で UNKNOWN のまま。
