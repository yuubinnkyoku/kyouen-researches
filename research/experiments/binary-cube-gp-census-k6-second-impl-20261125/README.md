# binary-cube-gp-census-k6-second-impl-20261125

K_6 = 9 上界根拠 (binary-cube-gp-census-k6-20261121 の s10 = 0) のための
**独立第二実装**による anchored GP census ({0,1}^d, d=3..6)。
宣言: research/log/2026-11-25-gp-census-k6-second-implementation-single-owner-note.md
対象知識: items/K0568 (二値6次元 K_6 = 9) の上界側の裏付け二重化。

## 第一実装からの独立性

第一実装 census2.js は GF(p) 分数なしフレーム + 2大素数 (83rd primes) で零判定していた。
本実装は**素数・剰余を一切使わない純整数演算**のみで構成する。

- 小行列式: Bareiss (fraction-free, 行swapの符号を追跡し、det として正確に返す)。
- k<=d 層: hom 座標 [1, bits...] の rank 検査 (fraction-free 前進消去、
  中間値は対応する小行列式で抑えられ Hadamard 限界内)。
- k=d+1 (=m) 層: **行置換座標函数** g_i(x) := det(M_B[row i <- x])。
  children のゲート = g_i(x) != 0 for all i (det([B - b_i, x]) と符号違いのみで同値)。
- k>=d+2 層: 全ゲートを g 行間の**射影マイナー** (2x2 / 3x3 / 4x4 整数行列式) に還元。
  導出の骨子: ゲート汎関数 mu は B の省略 index 集合 C 外の行ですべて消えるため
  span{g_i : i in C} に属し、mu(他プール要素)=0 の解として小行列式 の det が現れる。
  列ごとの符号 u8126き σ_i は σ🕳 ... [σ_i^2=1 ゆえ零判定不変]。
- float64 内で全中間値が厳密: |det| <= Hadamard(7) = 907, |g| <= 1512,
  4x4 マイナー <= 24 * 1512^4 ≈ 1.26e14 < 2^53 (battery B8 で実測主張)。

列挙規約は第一実装と同一 (頂点0アンカ、昇順正準 DFS、63ペア {0,v2} 分割、
per-pair counts[1]=1 は subtree 帳簿)。

## ファイル

- census3.js: 本体。全モードで決定的・全出力整数 JSON。
- agg3.mjs: 63ペア集計 + 第一実装 r6-results.jsonl との全行照合 (fail-closed)。
- README.md: 本ファイル。
- 出力 (公式実行後に push): r3-results.jsonl, results3.json, battery.txt,
  census-d3.json, census-d4.json, census-d5.json, check-pair01.txt, determinism.txt

## 使い方

```sh
node census3.js selftest            # B1 det vs BigInt Laplace / B2 rank / B3 gate fuzz /
                                    # B4 9点証人 / B8 magnitude / B6 d3+d4 census 全一致
node census3.js brutecensus 5       # 完全独立の直接行列式全走査 (参照実装)
node census3.js census 5            # fast 全 census
node census3.js pair 6 1 3 5 ...     # per-pair (1 JSON 行 / ペア)
node census3.js gatecheck 6 1 600000 # pair 実行中の先頭 N child-decisions を直接再検査
node agg3.mjs r3-*.jsonl ../binary-cube-gp-census-k6-20261121/r6-results.jsonl
```

## honesty labels

- 本研究は既存の有限計算 (**第一実装の全走査結果**) の独立再現が主目的。
  per-pair counts・Σテーブルが全て一致した場合に「独立第二実装による corroboration」
  として K0568 に記録する。数学的な新規命題の主張は行わない。
- brutecensus は fast とは別アルゴリズム (ゲート毎に直接 7x7 determinant を評価) の
  完全列挙であり、d=3/4/5 で published anchored table と一致済み。
  d=6 の brute は計算量上実施しない (fast census + gatecheck で代替)。
- gatecheck は pair (0,1) の先頭 600,000 child-decisions の直接再検査であり、
  探索全体の全ゲート検査ではない (選択は lexicographic-prefixバイアスあり、として明記)。
