---
id: K1300
title: "s-パラメータ共演ゲーム — キャップ・ゲームとブロッキング・ゲームの完全 Grundy と parity-graded 境界"
kind: computation
status: computed
topics: [grundy, geometry, statistics]
aliases:
- cap game on PG(2,q) and AG(2,q)
- s-parameter Kyouen complete Grundy
- parity-graded boundary AG(2,5)
relations:
- type: extends
  target: K1253
  note: s=3 の共演ゲームを一般の s（キャップ s=2、ブロッキング s=q−2）へ拡張
- type: related
  target: K1298
  note: 全極大サイズのパリティ一様が Grundy {0,1} の必要十分条件であることを決定的に実証（AG(2,4) s=2 と AG(2,5) s=2）
- type: related
  target: K1295
  note: PG(2,q) の s=3 ゲームの s 方向への拡張
artifacts:
- path: research/experiments/s-parameter-kyouen-20261125/report.md
  role: log
  note: 全ゲームの完全 Grundy 表・parity-graded 境界・構造の総括
- path: research/experiments/s-parameter-kyouen-20261125/scripts/build_ag2.py
  role: source
  note: PG(2,q) から AG(2,q) を導出し点対の一意性を全数検査
- path: research/experiments/s-parameter-kyouen-20261125/scripts/grundy_general.py
  role: solver
  note: 安全集合の DFS 列挙とサイズ降順 DP による Grundy/misère（n≤25、bytearray）
- path: research/experiments/s-parameter-kyouen-20261125/output/grundy_general.json
  role: data
  note: 10 ゲームの完全 Grundy（safe 数・極大サイズ・分布・G(∅)・misère）
- path: research/experiments/s-parameter-kyouen-20261125/independent/claims_check.json
  role: certificate
  note: 独立実装による 3 ゲームの全項目一致（all_pass=true）
- path: research/experiments/s-parameter-kyouen-20261125/independent/parity_lemma_ag24_s2.json
  role: certificate
  note: AG(2,4) s=2 の全 1,793 局面で parity-graded 補題が成立（violations 0）
- path: research/experiments/s-parameter-kyouen-20261125/independent/REPORT.md
  role: log
  note: 独立検証の総括（全 PASS、盤検証・再計算・parity 補題・クロスチェック）
- path: research/experiments/s-parameter-kyouen-20261125/independent/verify.py
  role: verifier
  note: 独自実装（DFS 2 順序＋Grundy/misère ハッシュ）による再計算
- path: research/experiments/s-parameter-kyouen-20261125/independent/crosscheck.json
  role: certificate
  note: 全 2^16 部分集合・組合せ列挙・2 実装 SHA-256 一致のクロスチェック
- path: research/experiments/s-parameter-kyouen-20261125/output/board_ag2q4.txt
  role: data
  note: AG(2,4) の 16 点・20 直線の盤（点対一意性検査済み）
scope: PG(2,q)（q=2,3,4）と AG(2,q)（q=2,3,4,5）上の「各直線と高々 s 点」共演ゲーム。s=2（キャップ・ゲーム）と s=3（AG ではブロッキング・ゲーム）の完全 Grundy（通常・misère、全安全局面）。
evidence: 盤は出版済み PG ボードから導出し点対の一意性を全数検査。安全集合を DFS で全列挙しサイズ降順 DP で Grundy（bytearray(2^n)、n≤25）と misère（打てない方が勝ち）を計算。主結果は (i) PG(2,q) s=2 は全極大が最大サイズ（q=2,3,4,5 で 4/4/6/6）で Grundy {0,1}、極大アーク数 7/234/168/3,100（q=5 は全 41,572 キャップ、6-キャップ 3,100＝円錐曲線）。(ii) AG(2,4) s=2 は極大サイズ 4 と 6 の混在だが全て偶数で、Grundy は {0,1} のみ（parity-graded 補題の仮定がサイズ一様でなくパリティ一様であることを示す決定的例）。(iii) AG(2,5) s=2 は極大サイズ 5 と 6 でパリティ混在、Grundy 2 が 3,000 局面に出現。(iv) AG(2,4) s=3 は極大 8/9 混在で Grundy 2 が 960 局面。(v) AG(2,5) s=3 は 1,365,826 局面で Grundy 0..4（4 が 54,000 局面。これらの幾何盤（PG/AG/設計）の共演ゲームでは最大値。n×n 盤族には Grundy 11 の例があり、リポジトリ全体の最大ではない）。(vi) PG(2,4) s=4 は 1,234,016 局面、極大サイズ 12/13/14/16、Grundy 2,3 が出現。misère の基底は「打てない方が勝ち」。PG(2,5) s=2 は dict ベース DP で計算（41,572 局面、全極大 6）。独立検証（別実装）が AG(2,4) s=2・AG(2,5) s=2・AG(2,4) s=3 の safe 数・サイズ別個数・極大サイズ・Grundy 分布・G(∅)・misère をすべて一致確認（claims_check.json の all_pass=true）。AG(2,4) s=2 の全 1,793 安全局面で parity-graded 補題が成立（violations 0）。クロスチェックとして n=16 は全 2^16 部分集合の完全 DP、AG(2,5) はサイズ別列挙で level 7 が空（列挙の完全性）、増加/減少 DFS の一致、2 実装の Grundy/misère 表の SHA-256 一致を確認（crosscheck.json）。
---

# s-パラメータ共演ゲーム

## 全表

| game | v | s | safe | K | 極大サイズ（個数） | パリティ | G(∅) | misère | Grundy 分布 |
|---|---:|---:|---:|---:|---|---|---:|---:|---|
| PG(2,2) s2 | 7 | 2 | 64 | 4 | 4 (7) | 偶数 | 0 | 1 | 0:29, 1:35 |
| PG(2,3) s2 | 13 | 2 | 560 | 4 | 4 (234) | 偶数 | 0 | 1 | 0:313, 1:247 |
| PG(2,4) s2 | 21 | 2 | 5,048 | 6 | 6 (168) | 偶数 | 0 | 1 | 0:2899, 1:2149 |
| PG(2,5) s2 | 31 | 2 | 41,572 | 6 | 6 (3,100) | 偶数 | 0 | 1 | 0:19066, 1:22506 |
| AG(2,2) s2 | 4 | 2 | 16 | 4 | 4 (1) | 偶数 | 0 | 1 | 0:8, 1:8 |
| AG(2,3) s2 | 9 | 2 | 172 | 4 | 4 (54) | 偶数 | 0 | 1 | 0:91, 1:81 |
| AG(2,4) s2 | 16 | 2 | 1,793 | 6 | 4 (120), 6 (48) | 偶数 | 0 | 1 | 0:1009, 1:784 |
| AG(2,5) s2 | 25 | 2 | 16,426 | 6 | 5 (600), 6 (1000) | 混在 | 0 | 1 | 0:5401, 1:8025, 2:3000 |
| AG(2,4) s3 | 16 | 3 | 26,073 | 9 | 8 (120), 9 (1120) | 混在 | 1 | 0 | 0:12184, 1:12929, 2:960 |
| AG(2,5) s3 | 25 | 3 | 1,365,826 | 11 | 9 (12500), 10 (28000), 11 (9000) | 混在 | 1 | 1 | 0:402925, 1:323901, 2:227000, 3:358000, 4:54000 |
| PG(2,4) s4 | 21 | 4 | 1,234,016 | 16 | 12 (280), 13 (10080), 14 (360), 16 (21) | 混在 | 0 | 1 | 0:402633, 1:381983, 2:262920, 3:186480 |

## 発見

1. **parity-graded 補題の境界**: `AG(2,4), s=2` は極大サイズが 4 と 6 で混在するが
   両方偶数。Grundy は `{0,1}` のみ（1,793 局面）。これにより補題の仮定が
   「サイズ一様」でなく「パリティ一様」であることが決定的に示された。
   パリティ混在の 4 ゲーム（AG(2,5) s2, AG(2,4) s3, AG(2,5) s3, PG(2,4) s4）では
   いずれも Grundy ≥ 2 が出現。
2. **Grundy 4 の初出現（幾何盤族）**: `AG(2,5), s=3` で Grundy 値 0..4（4 が 54,000 局面）。
   反転平面 M(q) の最大 Grundy 3 を超える。n×n 整数盤族には Grundy 11 の例があり、
   リポジトリ全体の最大値ではない。
3. **キャップ・ゲームの構造**: PG(2,q) s=2 は全極大 = 最大サイズ
   （4/4/6、極大アーク数 7/234/168）。AG(2,4) s=2 は complete caps により
   4 と 6 が混在（120/48）。AG(2,5) s=2 は 5（600）と 6（1000）。
4. **多重ブロッキングとの関係**: `PG(2,4), s=4` の極大サイズの補集合は最小
   1 重ブロッキング集合（16←直線 21、14←Baer 360、13←8 点 10,080、12←9 点 280）。
   10,080 と 280 は Round 5 の 12 点 2 重ブロッキング集合の 2 軌道サイズと一致。

## 限界

- v≤25 まで。`PG(2,5)`（v=31）は全列挙不可。
- Grundy 4 の構造的理由、10,080/280 の再出現の意味は未解明。
