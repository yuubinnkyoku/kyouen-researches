# 2026-11-20 2トークン残余ゲーム y=4族パラメトリック全称証明（K1112）

## 経緯と選定

- 実行開始時に最新 main（着手時 HEAD 45920e13ed 以前 → 再取得、単一オーナー
  宣言ノート research/log/2026-11-20-two-token-y4-parametric-allz-single-owner-note.md
  は先行出版済み）を確認し、AGENTS.md・research/knowledge/README.md・
  未解決事項を再照会した。
- K1104（y=3 パラメトリック全称証明）の「未解決」が「y=4 族の同型機械化
  （B 子は本項・C 子は 1⊕K1100 で両子が出版済みに揃った・着手前に単一
  オーナー宣言を先行出版）」と明記しており、宣言ノートの「方針」が
  cand4 テンプレート導出 → K1104 同型の監査機械 → 3 実行 byte-identical →
  出版を指定していたため、その直接実行として選定した。
- 並走レーンは n11 系（着手時 K1105..K1109・出版時点で K1106..K1111 まで
  WIN8 cert/fold 連続出版）・
  AG(2,q) degeneration（K1058）・y>=6 一様族（z12..17 y-ge6 proof）・
  z=20/21 y=2 切片に向かっており、y=4 全 z パラメトリック一般化は
  宣言ノート（本レーン）以外に着手・出版なし。y=4 固定 z 切片は z=6..19 まで
  出版済み（K0880/K0980/K0987/K0990/K1006/K1015/K1024/K1027/K1031/K1048/
  K1064/K1076/K1083/K1100）で逐語アンカーが揃っている。
- この主張は上記 14 切片をすべて含意し、z>=20 の未着手 y=4 スライスを一挙に
  閉じ、K1101 が有限観察にとどめていた対角線下マージの y=4 版、K1104 が
  「y=4 の全称表が決め手」としていた tail 開始式 x+z+y+1 の y=2..4 帯確定、
  基底点 y 点仮説の y=4 全 z 確定を同時に運ぶ。

## 導出

- 生エンジン（出版済み K1099/K1104 機械と同一の H_ordered/H_canonical）で
  z=0..79・x=4..70・R<=x+z+12 の行センサス（479,720 点）を取り、z 偶奇別の
  パラメトリック T/P テンプレート（cand4）を導出した。マージ行 x<=z-5 は
  単一トークン閉形式 single_token(x+4,z,R) そのもの、基底点は 4 点
  {z+1,z+3,z+5,z+7}、掃引行 x=z+5・帯 O[z+8,2z+9]（奇z）/O[z+9,2z+9]（偶z）、
  定常 pin {z+8}/{z+9}、前倒し pin（奇z {z+6} at x=z・偶z {z+5} at x=z-2 と
  {z+7} at x=z+2 の 2 つ）、tail R>=x+z+5 で (x+4) mod 2（値1無限帯が
  奇数 x 行に反転）。y=3 の表と異なる点はすべて行センサスで直接確認した。
- 閉形式のみの恒等式 cand4(z,x,R)=mex{A,B,C}（A：x-1 行、B：K1104の y=3
  閉形式、C：1⊕cand4(z-1,・,・)、x=4 は A≡B 合流）を z<=400 帯のグリッドで
  照合してテンプレートを確定した後、監査機械に固定した。

## 証明と検証

- K1104 の verify_y3_universal.py を y=4 に適応し verify_y4_universal.py を
  作成（13 チェック構成・C11 深 z 生 census アンカーを追加）。子の評価は
  K1104 の y=3 閉形式（逐語転写・diff 検証済み）と cand4 自身の z 外帰納。
  C1 生エンジン錨・C1b 子アンカー（単一トークン・y=3 子・x=4 合流子 (3,4)≡(4,3)）・
  C1d 出版 z=16/17/18/19 候補（K1064/K1076/K1083/K1100）の逐語一致・C2/C2b/C12
  恒等式グリッド＋マージ・tail 系・C3 選択肢分解アンカー・C4 型機械ボックス±60・
  C7 seeded 遠方 probe 20 万点・C8 境界多様体＋tail 値照合・C9 v 空間シェル掃引・
  C11 生 census アンカー z=0..79・C12 深グリッド掃引の計 5,058,763 照合点
  （うちマージ系 1,991,409 点）で全チェック不一致 0。
- **clip 窓の発見**: y=3 機械の ±8/±9 をそのまま使うと型内 confluence が
  系統的に破れる。y=4 の特徴距離（偶 z 定常 pin R-z=9・掃引帯下端 2y+z+2 の
  R-z=10・C 子の掃引上端 R-2z=11）のためで、±9/±10 でも x-z・R-z が 10 と 12 の
  同型崩壊対（witness (z,x,R)=(60,70,70)/(60,72,72) 型）が残り、±12窓±13番兵で
  実現型 27,722・confluence 違反 0・ボックス外新規型 0 が確定した。
窓拡大の理由は report.md「証明構成」に記録した。
- audit.json は同一 cwd 2 回＋別 cwd 別ディレクトリ（/tmp）1 回で byte-identical
  （SHA-256 c2151805db9db4c3a3062d293d97fbe664033b44291d65b6b33c80d52d329788）。
- census_rows.py（z=0..79・x=4..70・R<=x+z+12・479,720 点の生二重再帰センサス・
  行ごと Thue-Morse 指数・T・P・tail 抽出・tail アサート全行成立・
  エンジン状態数 2,414,940）を同時出版し、census.txt も byte-identical 再生
  （SHA-256 7633c04779881dc2b661d299cd56411f6c04a2ea3ba233ed2885f918a7b6d8b5）。

## 出版と修復

- 実験 dir: research/experiments/vertical-fiber-two-token-y4-parametric-allz-proof-20261120/
  （report.md・verify_y4_universal.py・census_rows.py・output/audit.json・output/census.txt）
- item: research/knowledge/items/K1112-two-token-y4-parametric-allz-universal-proof.md
  （kind: proposition, status: proved。relations: depends_on K0832/K1104、
  generalizes K0880/K0980/K0987/K0990/K1006/K1015/K1024/K1027/K1031/K1048/K1064/
  K1076/K1083/K1100。K番号はpush直前に3点確認（README grep・itemsツリー・
  list_commits）でK1112を取得した。当初予定番号はK1110だったが、本実行中に
  並走レーンがfold13（K1110）・fold14（K1111）を連続出版したため差し替えた）
- index: research/knowledge/README.md に bullet 追加、.github/workflows/knowledge.yml に
  CI audit step 2 件（verify_y4_universal.py・census_rows.py・git diff --exit-code）追加。
- **K1104 実験 dir の誤配置修復**: y=3 の実験 dir
  vertical-fiber-two-token-y3-parametric-allz-proof-20261120/ が repo 直下
  （root）に push されており、K1104 の item artifact パス・研究 log の
  「実験 dir」記述・CI workflow の K1104 audit step
  （.github/workflows/knowledge.yml の2ステップ）がすべて指す
  research/experiments/vertical-fiber-two-token-y3-parametric-allz-proof-20261120/
  が 404 になっていた（CI audit step が次回実行から必ず失敗する状態）。本実行で
  5 ファイル（report.md・verify_y3_universal.py・census_rows.py・output/audit.json・
  output/census.txt）を byte-identical で research/experiments/ 配下へ再配置し、
  root の旧配置を削除した。内容は一切変更していない
  （root 版全 5 ファイルを fetch+sha256sum で取得し、verify_y3_universal.py=
  55b3e2d1…・output/audit.json=dcb16395…・output/census.txt=860d60a3… が
  K1104 report.md が pin する出版値と一致することを確認後に移動した）。

## 次に開くもの

- y=5 族の同型機械化（着手前に単一オーナー宣言。宣言ノートの横断観察は
  tail x+z+y+1・基底点 y 点・掃引行 x=z+y+1 の y=5 での検証が最初の関門）。
- 型機械 clip 窓の一般式（特徴距離 2y+z+2 からの要件式）
  とボックス外新規型ゼロの補題化。
- 基底点 y 点仮説・d+z 剰余格子規則の一般証明（y<=4 で全称確定済み）。
