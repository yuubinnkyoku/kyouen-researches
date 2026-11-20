# 2026-11-20 2トークン残余ゲーム y=5族パラメトリック全称証明（K1126）

## 経緯と選定

- 実行開始時に最新 main を再取得し（本出版直前 HEAD 801a391480・K1125 index
  出版まで確認）、AGENTS.md・research/knowledge/README.md・未解決事項を
  再照会した。単一オーナー宣言ノート
  research/log/2026-11-20-two-token-y5-parametric-allz-single-owner-note.md
  （宣言時 HEAD ef18cc3566・宣言 commit 1a22a23fec・宣言 2026-11-20T05:2xZ）
  は先行出版済みで、並走 n11 レーンの K1123 bullet が
  「y=5族全称証明〔1a22a23fec〕着手禁止」と明記していることを確認した。
- K1112（y=4 パラメトリック全称証明）の「未解決」が「y=5 族の同型機械化
  （着手前に単一オーナー宣言を先行出版）」と明記しており、宣言ノートの
  「方針」が cand5 テンプレート導出 → K1104/K1112 同型の監査機械 →
  3 実行 byte-identical → 出版（3コミット実験 dir＋item/log＋index）
  を指定していたため、その直接実行として選定した。
- 並走レーンは n11 系（K1113..K1125 の WIN8 cert/fold 連続出版・fold19 候補
  宣言済み）・K1058 円整数論（q=5,7 境界の tightness 検証）に向かっており、
  y=5 全 z パラメトリック一般化は宣言ノート（本レーン）以外に着手・出版なし。
  y=5 固定 z 切片は z=6..18 まで出版済み（K0884/K0981/K0991/K0992/K1007/
  K1037/K1043/K1045/K1047/K1049/K1074/K1080/K1092）で逐語アンカーが揃っている。
- この主張は上記 13 切片をすべて含意し、z=19,y=5（未着手だった次候補）を
  含む z>=19 の y=5 行を一挙に閉じ、K1101 マージ命題の y=5 版、tail 開始式
  x+z+y+1 の y=2..5 帯確定、基底点 y 点仮説の y=5 全 z 確定を同時に運ぶ。

## 導出

- 生エンジン（出版済み K1099/K1104/K1112 機械と同一の H_ordered/H_canonical）
  で z=0..79・x=5..70・R<=x+z+12 の行センサス（475,200 点・行 5,280）を
  取り、z 偶奇別のパラメトリック T/P テンプレート（cand5）を導出した。
  マージ行 x<=z-6（S=x+5<=z-1）は単一トークン閉形式 single_token(x+5,z,R)
  そのもの、基底点は 5 点 {z+1,z+3,z+5,z+7,z+9}、掃引行 x=z+6・帯
  O[z+10,2z+11]（奇z）/O[z+11,2z+11]（偶z）、定常 pin {z+10}/{z+11}、
  前倒し pin（奇z は {z+6} at x=z-3・{z+8} at x=z+1・{z+10} at x=z+5 の
  3 つ、偶z は {z+7} at x=z-1・{z+9} at x=z+3 の 2 つ）、tail R>=x+z+6 で
  (x+5) mod 2（値1無限帯が偶数 x 行に戻る）。
- **K1112 レポートの erratum を検出**: マージ行 P の導出中に、出版済み
  y=4 レポートのマージ行 P 表（z 奇表・z 偶表の冒頭 2 行ずつ）とマージ系
  本文の S 奇/S 偶の割り当てが反転していることに気づいた。生エンジンの
  直接照合（z=20・26・x 奇偶両方）で確定: 正しくは S=x+4 の偶奇は x と同じ
  なので値1無限帯 I[x+5,∞) は x 奇 の行（出版表は「x 偶」と誤記）。
  tail（奇数 x 行は tail で 1）との整合でも反転が裏付けられる。
  K1112 の検証器・閉形式コード（cand4）は最初から正しく、本項検証器の
  C1b（48,411 点・bad 0）が y=4 閉形式の逐語転写を raw 再照合している。
  erratum コミットで該当 5 行を修正した（主張・証明・監査に影響なし）。
- 閉形式のみの恒等式 cand5(z,x,R)=mex{A,B,C}（A：x-1 行、B：K1112 の y=4
  閉形式、C：1⊕cand5(z-1,・,・)、x=5 は A≡B 合流 (4,5)≡(5,4)）を
  z<=400 帯のグリッドで照合してテンプレートを確定した後、監査機械に固定した。

## 証明と検証

- K1112 の verify_y4_universal.py を y=5 に適応し verify_y5_universal.py を
  作成（12 チェック構成・y=4 版の C1/C1b/C1d/C2/C2b/C3/C4/C7/C8/C9/C11/C12
  に対し C1c なしの構成）。子の評価は K1112 の y=4 閉形式（逐語転写・
  diff 検証済み）と cand5 自身の z 外帰納。C1 生エンジン錨・C1b 子アンカー
  （単一トークン・y=4 子・x=5 合流子 (4,5)≡(5,4)）・C1d 出版 z=16/17/18
  y=5 切片（K1074 set-based・K1080/K1092 predicate-based）の逐語一致・
  C2/C2b/C12 恒等式グリッド＋マージ・tail 系・C3 選択肢分解アンカー・
  C4 型機械ボックス±60・C7 seeded 遠方 probe 20 万点（seed 20261122）・
  C8 境界多様体＋tail 値照合・C9 v 空間シェル掃引・C11 生 census アンカー
  z=0..79・C12 深グリッド掃引の計 5,456,418 照合点
  （うちマージ系 1,655,267 点・tail 系 390,940 点）で全チェック不一致 0。
- **clip 窓の再利用**: y=3 の ±8/9 では y=5 も合流違反が系統的に出るが、
  y=4 機械の ±12/±13 がそのまま使え、±60 ボックスで confluence 違反 0・
  新規型 0 が確定した（前の族の窓を再利用した初例。y=5 の特徴距離
  R-z 最大 12（掃引帯下端 2y+z+2）・R-2z=11（帯上端）・pin 10/11・
  tail 開始 R-x-z=6 はすべてクリップ窓内）。
- audit.json は同一 cwd 2回＋別 cwd 別ディレクトリ（/tmp）1回で byte-identical
  （SHA-256 838e1e5dce9619660d9add4a138f8f05a6e9536cc886ad5826c18cb0cf58a3b0）。
- census_rows.py（z=0..79・x=5..70・R<=x+z+12・475,200 点の生二重再帰
  センサス・行ごと Thue-Morse 指数・T・P・tail 抽出・tail アサート全行成立・
  エンジン状態数 2,879,588）を同時出版し、census.txt も byte-identical 再生
  （SHA-256 617751ba9fa6f8eed62028b2e7e1a3c0477bb3ed1777c07bc7e20e7eaba67559）。

## 出版

- 実験 dir: research/experiments/vertical-fiber-two-token-y5-parametric-allz-proof-20261120/
  （report.md・verify_y5_universal.py・census_rows.py・output/audit.json・
  output/census.txt）
- item: research/knowledge/items/K1126-two-token-y5-parametric-allz-universal-proof.md
  （kind: proposition, status: proved。relations: depends_on K0832/K1112、
  generalizes K0884/K0981/K0991/K0992/K1007/K1037/K1043/K1045/K1047/K1049/
  K1074/K1080/K1092。K番号はpush直前に3点確認（README grep・items ツリー・
  list_commits）で K1126 を取得した）
- K1112 レポート erratum: 対角線下マージ行 P 表の偶奇ラベル反転
  （4 テーブル行＋本文 2 行）を別コミットで修正。
- index: research/knowledge/README.md に bullet 追加、
  .github/workflows/knowledge.yml に CI audit step 2 件
  （verify_y5_universal.py・census_rows.py・git diff --exit-code）追加。

## 次に開くもの

- y=6 族の同型機械化（着手前に単一オーナー宣言。y=6 は偶数 y で tail・
  マージ行 P の偶奇が y=4 型に戻る。クリップ窓 2y+2=14 の広げ直しが
  必要になる最初の候補）。
- 基底点 y 点仮説・tail x+z+y+1・掃引帯族式・前倒しpin位置式・対角行上端
  格子規則 r=z+y-[2(z-y)≡0 mod 4] の一般証明（y<=5 で全称確定済み）。
- 型機械 clip 窓の一般式（y=5 が示した「前の族の窓の再利用」条件の補題化）
  とボックス外新規型ゼロの補題化。
