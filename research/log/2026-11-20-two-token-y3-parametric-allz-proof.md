# 2026-11-20 2トークン残余ゲーム y=3族パラメトリック全称証明（K1104）

## 経緯と選定

- 実行開始時に最新 main（着手時HEAD cdf3145119 → 単一オーナー宣言ノート
  commit b7a9f7c6a3 を先行出版）を確認し、AGENTS.md・
  research/knowledge/README.md・未解決事項を再照会した。
- K1099（y=2 パラメトリック全称証明）の「未解決」が「y=3族の同型機械化
  （B子=本項・C子は z 外帰納）の本項の手法の直接反復」と明記していた一方、
  並走レーンは z=19 y=4（K1100）・対角線下マージ（K1101）・n11 系
  （K1096/K1102/K1103）・AG(2,q) degeneration（K1058）に向かっており、
  y=3 族の全 z パラメトリック一般化は未着手・未宣言だったため、最も
  情報価値が高い作業として選定した。y=3 固定z切片は z=6..19 まで出版済み
  （K0879/K0979/K0986/K0989/K1005/K1014/K1021/K1026/K1030/K1034/K1050/
  K1067/K1078/K1098）で逐語アンカーが揃っており、B子は K1099（y=2 全z
  全称）・C子は 1⊕cand3 の z 外帰納で閉じる。
- この主張は上記14切片をすべて含意し（K1099 が K1023 の方向を継承した
  のと同じ向き）、z>=20 の未着手 y=3 スライスを一挙に閉じ、K1101 が
  有限観察にとどめていた対角線下マージの y=3 版を全称系に昇格する。

## 導出

- 生エンジン（出版済み K1099 センサス機械と同一の H_ordered/H_canonical）
  で z=0..80 の行センサスを取り、z 偶奇別のパラメトリック T/P テンプレート
  （cand3）を導出した。マージ行 x<=z-4 は単一トークン閉形式
  single_token(x+3,z,R) そのもの（S=x+3<z ブランチ）で、基底点は
  {z+1,z+3,z+5}、掃引行 x=z+4・定常 pin {z+6}/{z+7}・偶奇で分離する
  前倒し pin（奇z x=z-1 行 {z+4}、偶z x=z+1 行 {z+5}）と、y=2 にない
  過渡行構造を同定した。tail は R>=x+z+4 で (x+3) mod 2（y=2 の
  x+z+3 と異なる境界であることを確認）。
- 閉形式のみの恒等式 cand3(z,x,R)=mex{A,B,C}（A：x-1 行、B：K1099 の
  y=2 閉形式、C：1⊕cand3(z-1,・,・)、x=3 は A≡B 合流）を z<=400 帯の
  グリッドで照合（実行環境のみ 247,401＋深域点）し、テンプレートを確定。

## 証明と検証

- K1099 の verify_p2_universal.py の型機械構成を y=3 に適応し
  verify_y3_universal.py を作成。型に x==3 ビットと z==0 ビットを追加、
  子の評価は y=2 閉形式（K1099 依存・逐語転写）と cand3 自身の z 外帰納。
  C1 生エンジン錨・C1b 子アンカー・C1d 出版 z=18/z=19 候補（K1078/K1098）
  の逐語一致・C2/C2b/C12 恒等式グリッド・C3 選択肢分解アンカー・
  C4 型機械ボックス±60（実現型 10,850・confluence）・C7 seeded 遠方
  probe 20万点・C8 境界多様体・C9 v 空間シェル掃引・C12 深グリッド掃引の
  計 3,777,544 照合点（うちマージ系 1,818,314 点）で全チェック不一致 0。
  audit.json は同一cwd 2回＋別cwd別プロセス 1回で byte-identical
  （SHA-256 dcb163958d0abec06b36dd163b392c9a844c2973b91efb85b6cae44b7ae57a1b）。
- census_rows.py（z=0..80・x=3..70・R<=x+z+12・492,966 点の生二重再帰
  センサス・両エンジン×cand3 三方一致・マージ行 262,956 点・tail 一致）を
  同時出版し、census.txt も byte-identical 再生
  （SHA-256 860d60a3f0636e806bdcdade317d3813d905643c96a11be2121d0b94a58e548b）。

## 出版

- 実験 dir: research/experiments/vertical-fiber-two-token-y3-parametric-allz-proof-20261120/
  （report.md・verify_y3_universal.py・census_rows.py・output/audit.json・
  output/census.txt）
- item: research/knowledge/items/K1104-two-token-y3-parametric-allz-universal-proof.md
  （kind: proposition, status: proved。relations: depends_on K0832/K1099、
  generalizes K0879/K0979/K0986/K0989/K1005/K1014/K1021/K1026/K1030/K1034/
  K1050/K1067/K1078/K1098。push 直前に K1104 が空き（README grep 0 件・
  item slug 404）であることを再確認した）
- knowledge README 弾丸と CI workflow への検証器 2 ステップ（verify・census、
  git diff --exit-code 付き）を追記。
- 生成ビュー（README.md root・research/knowledge/generated/*）は
  tools/knowledge/build.py の再生成対象。本実行環境では repo 全体を
  clone できず uv 実行環境がないため再生成を行わず、追って
  「ci: refresh generated knowledge views」と同じ形での追い込みが必要
  （K1093/K1099 と同じ手順・実績あり）。

## 次の一手

- y=4 族の同型機械化（B 子に本項・C 子に 1⊕K1100 を使えば全 z y=4 表が
  直接導出できる。着手前に単一オーナー宣言を先行出版する）。
  y=4 の全称表は tail 開始の一般式（y=2 は x+z+2y-1、y=3 は x+z+2y-2）
  と pin 行位置 x=z+y-2 の決め手になる。
- 基底点 y 点仮説 {z+1,z+3,...,z+2y-1} と d+z 剰余格子規則・掃引帯公式の
  一般証明（y=1..3 の全 z incidence は確定済み）。
- 型機械ボックス外新規型ゼロの数学的補題化（K1023/K1099/K1104 共通の
  trust 境界を上げる）。
