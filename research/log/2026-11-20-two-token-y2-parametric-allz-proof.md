# 2026-11-20 2トークン残余ゲーム y=2族パラメトリック全称証明（K1099）

## 経緯と選定

- 実行開始時に最新 main（563f59160d → 本レーンの単一オーナー宣言ノート
  d435e76e09 先行出版直後）を確認し、AGENTS.md・research/knowledge/README.md・
  未解決事項を再照会した。K1023（y=1 パラメトリック全称証明）の残務
  「y>=2族の同型機械化」が未着手であること、y=2 固定z切片が z=6..21 まで
  出版済みで両アンカーが揃っていること、並走レーンが z=18 y>=6 族と
  z=19 y=3（宣言 commit 4dc6fc9cce）に向かっていることから、
  y=2 の全 z パラメトリック全称証明を最も情報価値が高い作業として選定した。
  この主張は K1019/K1025/K1028/K1032/K1042/K1044/K1051..K1054 の個別スライスを
  すべて含意し（K1023 が K1022 を generalize したのと同じ方向）、かつ
  z>=22 の未着手 y=2 スライスを一挙に閉じる。
- 単一オーナー宣言ノート（commit d435e76e09）で本項の単独進行を先行出版済み。

## 導出

- 生エンジン（出版済み z16/z17 センサス機械と同一の H_ordered/H_canonical）
  で z=0..80 の行センサスを取り、z 偶奇別のパラメトリック T/P テンプレート
  （cand2）を導出した。z=0..80 で行・tail とも三方不一致 0。
- 閉形式のみの恒等式 cand2(z,x,R)=mex{A,B,C}（A：x-1行、B：K1023 の y=1 閉
  形式、C：1⊕cand2(z-1,・,・)、x=2 は A≡B 合流）を z<=400 まで
  3,610,650 点照合（実行環境のみ）し、テンプレートを確定した。

## 証明と検証

- K1023 の verify_p1_universal.py の型機械構成を y=2 に適応し
  verify_p2_universal.py を作成。型に x==2 ビットと z==0 ビットを追加、
  子の評価は y=1 閉形式（K1023 依存）と cand2 自身。C1 生エンジン錨・
  C1b 子アンカー・C1d 出版 z=16/z=17 候補の逐語一致・C2/C2b/C12 恒等式
  グリッド・C3 選択肢分解アンカー・C4 型機械ボックス±60（実現型 11,090・
  confluence）・C7 seeded 遠方 probe 20万点・C8 境界多様体・C9 v 空間シェル
  掃引・C12 深グリッド掃引の計 4,573,605 照合点で全チェック不一致 0。
  audit.json は同一cwd 2回＋別cwd 1回で byte-identical
  （SHA-256 84198f02bfcd2a5efc9610b6207359d87a87790e591c1e7109c900c72ca5a397）。
- census_rows.py（z=0..80・x=2..70・R<=x+z+12・497,421 点の生二重再帰
  センサス）を同時出版し、census.txt も byte-identical 再生
  （SHA-256 e007bc784f1da2c352c2081a6aaea27c9cd0f57aba11074a5064ea59795f7129）。

## 出版

- 実験 dir: research/experiments/vertical-fiber-two-token-y2-parametric-allz-proof-20261120/
  （report.md・verify_p2_universal.py・census_rows.py・output/audit.json・
  output/census.txt）
- item: research/knowledge/items/K1099-two-token-y2-parametric-allz-universal-proof.md
  （kind: proposition, status: proved。relations: depends_on K0832/K1023、
  generalizes K0878/K1004/K1013/K1019/K1025/K1028/K1032/K1042/K1044/K1051/K1052/
  K1053/K1054。着手時は K1097 が空きと確認していたが、出版直前の再取得で
  並走レーンが K1097（n11 round-4 refsolve）・K1098（z=19・y=3）を相次いで
  取得したため、AGENTS.md の規約（衝突側が再採番）に従い K1099 へ再採番した）
- knowledge README 弾丸と CI workflow への検証器 2 ステップ（verify・census、
  git diff --exit-code 付き）を追記。
- 生成ビュー（README.md root・research/knowledge/generated/*）は
  tools/knowledge/build.py の再生成対象。本実行環境では uv 実行環境がない
  ため再生成を行わず、追って「ci: refresh generated knowledge views」と同じ
  形での追い込みが必要（K1093 と同じ手順・実績あり）。

## 次の一手

- y=3 族の同型機械化（B 子に本項・C 子に 1⊕K1052 を使えば全 z y=3 表が直接
  導出できるはず。z=19・y=3 は並走レーンが K1098 として出版済みで、
  y=3 パラメトリック表は K1098 も含意する形になる）
- 値1基底点 y 点仮説 {z+1,z+3,...,z+2y-1} と d+z 剰余格子規則の一般証明
  （y=2 の全 z incidence は本項で確定済み）。
- 低R高さのみ縮約の y=2 全 z 版（z=18..21 で R<=z+2 観測）。
