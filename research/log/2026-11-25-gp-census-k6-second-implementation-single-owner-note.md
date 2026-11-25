# 2026-11-25 GP-census K_6 上界の第二実装クロスチェック: 単一オーナー宣言

- **target**: K0568 の下地にある「K_6 = 9 上界根拠 (binary-cube-gp-census-k6-20261121 の s10=0)」について、
  項目自身が残課題として挙げている「独立第二実装による全走査」を今回は実施する。
- **lane / ownership**: binary-cube GP-census second implementation (integer-Bareiss 系)。
  並走実行があるため、本レーンの成果物はこの note のオーナーが
  research/experiments/binary-cube-gp-census-k6-second-impl-20261125/ に順次 push する。
  同一レーンを他の実行が開始する場合はこの note に追記すること。
- **design** (第一実装 census2.js からの独立性: 実装は読まず、出力規約のみを複製):
  - GF(p) 分数なしフレーム + 2大素数を使わない。素数・剰余なしの純整数演算のみ。
  - 小行列式: Bareiss (fraction-free, 厳密整数、符号追跡)。
  - k<=d 層: hom 行の rank 検査 (fraction-free 消去、minor サイズで有界)。
  - k=d+1 (=m) 層: 「行置換座標」g_i(x) := det(M_B[row i <- x])。ゲート = 全 g_i != 0。
    (det([B - b_i, x]) = ±g_i(x) の符号は (i,d) だけで確定するため、零判定として同値。)
  - k>=d+2 層: 全ゲートを g 行の「射影マイナー」(2x2/3x3/4x4 整数行列式) に還元して判定。
    導出: 極大配置の行集合から Y (|Y|=d) を省略 index C で取ると、ゲート汎関数 mu は
    B の C 外の行ですべて消えるので span{g_i : i in C} に属し、mu(他プール要素)=0 の解が
    小行列式で与えられる。列ごとの符号 σ_i は σ^2=1 で零判定に影響しない。
  - float64 の中で全中間値が厳密: |det| <= Hadamard(7)=907, |g| <= 1512,
    4x4 マイナー < 24 * 1512^4 ≈ 1.26e14 < 2^53 (battery で主張・検査)。
- **実施済み validation** (ローカル、成果物は battery.txt として公開予定):
  - selftest: det vs BigInt Laplace 400 cases、rank 200、gate-identity fuzz (60 seeds, d=3..6,
    fast 判定 vs 直接 determinant 全照合)、published 9点証人 3 種 + XOR 正規化像の GP 検査、
    d3/d4 fast census 全一致。全 PASS。
  - brutecensus (完全独立の直接行列式全走査参照実装):
    d=3 → [0,1,7,21,29,5,0,...]、d=4 → [0,1,15,105,430,940,408,0,...]、
    d=5 → [0,1,31,465,4405,27990,104286,67606,0,...]。すべて published anchored table と一致。
    d=5 は第一実装の brute (サイズ<=6) より深く、全ブレートで完走して s8=0 も全数確認した。
  - fast census d=3/4/5: published と完全一致。
  - d=6: pair (0,1) 単体 = published と完全一致 (約40s)。
- **公式 d=6 実行** (宣言時点で実行中; 進捗は後続 commit で公開):
  - 63 ペア (v2=1..63) を2並列 worker で全走査。奇数 v2 32 ペアは宣言時点で完了・全一致済み。
  - gatecheck: pair (0,1) の先頭 600,000 child-decisions を直接 determinant で全再検査、
    さらに軽量ペアの全ゲート再検査を battery に含める。
  - determinism: 代表ペアの再実行が byte-identical であることを battery に含める。
- **honest labels**: 本研究は「既存の有限計算の独立再現・二重化」が目的。
  per-pair・合計テーブルがすべて一致した場合に限り「独立第二実装による corroboration」と
  K0568 に記録し、数学的な新規主張は行わない。内部開発中に発見した実装バグ 2 件
  (rankExact の引数破壊に起因する S 行の汚染、scratch 行コピー忘れ) は run log 側に正直に残す。
- **成果物 (予定)**: census3.js / agg3.mjs / README.md / r3-results.jsonl (63行) /
  results3.json (集計+照合) / battery.txt / census-d3.json, census-d4.json, census-d5.json /
  check-pair01.txt / determinism.txt。
