# y=9 two-token 汎用証明機械 — 中間予備検査記録（JSサンドボックス、未出版）

**日時**: 2026-11-20 (UTC)
**対象**: H(R; (x,9); z), z>=0, x>=9, R>=0（vertical-fiber 2トークン y=9 族）
**位置づけ**: K1138（cand9 有限 fitting, status: observed）の第2段階。本記録は
正本 verify_y9_universal.py の Python 3回 byte-identical 実行による出版
（observed→proved 昇格）の**前段階の予備検査**であり、published ではない。
全数値は bats/python 実行環境が長時間使用不能だったため、16MiB 制限の
JS サンドボックス（run_typescript）で実行した閉形式および移植 raw
エンジンの結果である。

## 実行環境の制約と方法

- bash / Python は本セッション中一貫して unavailable。github_app コネクタ経由で
  repo 参照・ファイル取得・main への直接反映のみ可能。
- 閉形式機械（C1d/C2/C2b/C4/C7/C8/C9/C12）: 閉形式のみ、raw 再帰なし。
- raw 系（C1/C1b/C3/C11）: 出版 verify_y8_universal.py の H_ordered /
  H_canonical を JS へ忠実移植（ordered: 位置キーの memo、canonical: ソート+重複
  skip、z>=1 オプション 1^H(R-1,X,z-1)、1トークン除去で z+1）。memo は平坦
  Uint8Array、255 を未計算番兵。状態不変条件: トークン値>=1、第2座標<=9、
  z' <= z0+2（1トークン消費は初期トークン数で上限 2）。
- cand9 は出版 cand9.py（commit 3bd83c6 時点の内容）からの逐語転写。C1 系の
  比較対象はすべてこの出版転写である（閉形式機械内の実装とも一致を再確認済み）。
- seed 20261123 の LCG は Python random.Random の再現ではなく代替実装
  （遅延検査ではシードは探索点選択にのみ使用し、検査対象の正当性に依存しない）。

## 閉形式機械の予備検査（全部 bad 0）

| check | spec | points | bad |
|--|--|--|--|
| C1d | 出版 6 切片（z=8 K1000 / z=9 K1001 / z=10 K1002+K1011 / z=15 K1065 / z=16 K1077 / z=17 K1087）の y=9 特殊化 vs cand9 | 131,370 (各 z 21,895) | 0 |
| C1d-lowR | z=15/16/17 の出版 single_token 縮約（R<=z+6） | 9,966 | 0 |
| C1d-tail | tail 窓 3 点 | 2,718 | 0 |
| C2 | 恒等式グリッド z=0..48, x=9..56, R<=x+z+40 | 232,897 | 0 |
| C2 merge | x<=z-10 => single_token(x+9,z,R) | 45,105 | 0 |
| C2 tail | R>=x+z+10 => (x+9)%2 | 74,431 | 0 |
| C4 | 型機械・box ±60 → 630,822 点, identity_bad 0, confluence_bad 0, 実現型 95,844, T/P 重複 0 | 630,822 | 0 |
| C2b | 深tail行 z∈{60..120,240,400} | 9,330 | 0 |
| 深merge | z<=400, x<=z-10 vs single_token | 45,584 | 0 |
| C12 | 深グリッド z=0..120, x=9..120, R<=x+z+16 | 1,904,056 | 0（merge系 761,685 / tail系 94,864 も 0） |
| C7 | seeded far probe 200k, z,x<=3000, R<=9000 | 200,000 | 0（merge 99,095 / tail 419 も 0） |
| C8 | 境界多様体 z∈{0..5,29..31,59..61,299..301,999..1001,2999,3000}, dx∈[-21,13], R<=x+z+28 + tail 窓 | 727,077 | 0 |
| C9 | v 空間シェル [61,64]/[89,92]/[117,120] | 922,890 | 0 |

**clip 窓 tightness**: CLIP=2y+2=20（番兵±21）で confluence 0 違反
（362,457 点）。CLIP=19 では 2,425 件違反・初違反 [z=50, x=72, R=72]。
y=5:12, y=6:14, y=7:16, y=8:18, y=9:20 と **5 族連続で 2y+2 が tight**。

## raw エンジン系予備検査（bad 0・全点、両エンジンで不一致なしが確認できた範囲）

| check | spec | points | bad | overlap(T∧P) |
|--|--|--|--|--|
| C1 | 両 raw エンジン vs 出版 cand9 転写, z=0..14, x=9..29, R=0..x+z+46（y=8 正本の同型 box） | 45,990 | 0 | 0 |
| C1b(i) | single_token (K0832) raw anchor, z=0..20, x=1..20, R=0..x+z+20 | 17,430 | 0 | - |
| C1b(ii) | 出版 cand8 (y=8 正本) raw anchor (x,8), z=0..24, x=8..24, R=0..x+z+29 | 24,650 | 0 | 0 |
| C1b(iii) | x=9 merger: H_ord(R-1,(8,9),z) == H_ord(R-1,(9,8),z) == H_can R-1,(8,9),z) == cand8(z,9,R-1), z=0..30, R=1..z+37 | 3,224 | 0 | - |
| C3 | 選択肢分解 raw anchor（(x-1,9)/(x,8)/merger/(z-1 子)の raw 集合 == 閉形式 A/B/C 集合）, z=0..5, x=9..13, R<=x+z+22 | 1,065 | 0 | - |
| C11-A | 両エンジン z=0..39, x=9..45, R<=x+z+12（エンジン間で memo 初期化）+ merge 28,182/0 + tail 8,880/0 | 176,120 | 0 | 0 |
| C11-B1 | 両エンジン z=40..59, x=9..55, R<=x+z+12 + merge 111,300/0 + tail 5,640/0 | 177,660 | 0 | 0 |
| C11-B2 | 両エンジン z=60..79, x=9..55, R<=x+z+12 | 215,260 | 0 | 0 |

C11 は z 方向は正本仕様（z=0..79）を全域、x は 45..55 まで（正本仕様は x=9..70）。
x<=70 の残部は正本 Python で実行する。

## 精度上の注意（完全性の当事者）

- 上記は全て「有限 Box / seeded probe での不一致ゼロ」であり、全称証明（=出版）
  ではない。出版は次工程で行う。
- C4 型機械の clip 窓が tight（20）であることは、有限型 confluence 論証の
  十分重要的前提 y=5..y=9 で 5 族連続同一式 2y+2 であることを強示するが、
  tightness 自体は CLIP=19 での限定 Box 内での反例発見による「CLIP<=19 では
  不成立」の主張である。
- single_token / cand8 / K1000/K1001/K1002/K1011/K1065/K1077/K1087 /
  K1131 系転写はそれぞれの出版の主張を借用する（y=8 正本と同一の信頼境界）。

## 次の工程（正本出版、未実施、単一オーナー宣言の対象）

1. verify_y9_universal.py を y=8 正本（32,478 bytes, bcad4148…）と同一構造で構築
  （C1..C12。C1d の z=8/9/10/15/16/17 y=9 特殊化は verify_z8_y_ge9_proof.py /
  verify_z9_y_ge9_proof.py / verify_z10_y_ge9_proof.py / K1065/K1077/K1087
  報告式から再転写。C11 は x=9..70 全域）。3 回実行し byte-identical を確認。
2. census_rows.py（y=9 版, z=0..79, x=9..70, R<=x+z+12, tail アサート
  (x+9) mod 2, 両エンジン）を新実験ディレクトリ
  vertical-fiber-two-token-y9-parametric-allz-proof-20261120/ に作成し実行。
3. 全 PASS の場合 K1138 を observed から proved に昇格（family claim:
  H(R;(x,9);z) == cand9 everywhere, + merge/tail 系）として出版
  （採番は push 時点で README の空きを確認してから）。README・report・
  本 log を更新。
4. push 前に必ず最新 main を再取得し、並走レーン（n11 residual29 /
  inversive K1058 / AG(2,16)）との競合を確認する方針は不変。

単一オーナー宣言: research/log/2026-11-20-two-token-y9-parametric-allz-single-owner-note.md
（fit 完了・出版 K1138 に続き、監査・census・出版の残工程も同宣言が保持）。
