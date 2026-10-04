# 共円ゲームの計算・証明・構造研究

完全指摘ルールの共円ゲームについて、標準 **1×1〜10×10の空盤勝敗を確定**しています。
**1×1〜8×8は全安全局面のGrundy数まで解析済み、9×9・10×10は弱解決、11×11は未解決**です。
8×8の全状態独立再計算と全局面証明書は未整備で、計算範囲と検証範囲を区別します。

固定幅q点版の一般定理と厳密閾値（**M_{3,5}=12、M_{4,8}=11**）に加え、misère、最大・極大安全配置、格子幾何、再配置、探索方式も研究対象です。
現在の命題・計算結果・反証・未解決問題・検証境界の唯一の正本は
[research/knowledge/items/](research/knowledge/README.md)です。
以下の解決状況は正本から生成します。実験記録や旧まとめは現在の結論を維持する場所ではありません。

<!-- BEGIN GENERATED SOLUTION STATUS -->
## 解決状況

現在の研究結果と未解決問題は [research/knowledge/](research/knowledge/README.md) に整理しています。各結果には参照用の `K0001` のような番号を付けています。以下は、そのうち盤面の解決状況に関する結果を自動生成した一覧です。

| 盤面・条件 | 参照・状態 | 段階・勝敗 | 分類・範囲 | 検証 | 証明書・独立検査・留保 |
|---|---|---|---|---|---|
| 1×1〜6×6; 標準q=4・完全指摘・通常プレイ | [K0004](research/knowledge/items/K0004-n1-n6-all-safe-grundy.md) · computed | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全安全局面 | exhaustive-enumeration | 空盤は各nのAND/OR証明書あり; 小盤参照実装照合、空盤C++検査; 勝者は各盤の個別項目を参照 |
| 7×7; 標準q=4・完全指摘・通常プレイ | [K0005](research/knowledge/items/K0005-n7-all-safe-grundy-audit.md) · computed | strong; second-player-win | root, all-safe-win-loss, all-safe-grundy; 179,810,350/179,810,350安全局面 | exhaustive-enumeration, independent-enumeration | 空盤証明書あり。強解決単独証明書は未整理; 全層独立再帰照合; README旧説明に全Grundy結果を補完 |
| 8×8; 標準q=4・完全指摘・通常プレイ | [K0006](research/knowledge/items/K0006-n8-all-safe-grundy-computed.md) · computed | strong; second-player-win | root, all-safe-win-loss, all-safe-grundy; 6,700,711,937/6,700,711,937安全局面 | reported-streaming-dp | 全局面証明書なし。空盤証明書は別項目; n=6で既知値と全一致、n=7で既知層サイズを照合。8×8全状態の独立再計算は未実施; 全局面Grundy DP完走済み。独立全状態検査・強解決証明書は未整備 |
| 1×1; 標準q=4・完全指摘・通常プレイ | [K0011](research/knowledge/items/K0011-n1-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 2×2; 標準q=4・完全指摘・通常プレイ | [K0012](research/knowledge/items/K0012-n2-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 3×3; 標準q=4・完全指摘・通常プレイ | [K0013](research/knowledge/items/K0013-n3-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 4×4; 標準q=4・完全指摘・通常プレイ | [K0014](research/knowledge/items/K0014-n4-second-player-win.md) · proved | weak; second-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 5×5; 標準q=4・完全指摘・通常プレイ | [K0015](research/knowledge/items/K0015-n5-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 6×6; 標準q=4・完全指摘・通常プレイ | [K0016](research/knowledge/items/K0016-n6-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 7×7; 標準q=4・完全指摘・通常プレイ | [K0017](research/knowledge/items/K0017-n7-second-player-win.md) · proved | weak; second-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 8×8; 標準q=4・完全指摘・通常プレイ | [K0018](research/knowledge/items/K0018-n8-second-player-win.md) · proved | weak; second-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 9×9; 標準q=4・完全指摘・通常プレイ | [K0019](research/knowledge/items/K0019-n9-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 10×10; 標準q=4・完全指摘・通常プレイ | [K0020](research/knowledge/items/K0020-n10-second-player-win.md) · proved | weak; second-player-win | root; 15 D4代表＝100初手 | exact-search, csv-audit, partial-kyoenc4 | 空盤面の単一KYOENC4証明書は未統合; CSV構造監査＋選択局面Rust証明検査; 勝敗確定。全巨大探索の独立再求解ではない |
| 9×9（全初手）; 標準q=4・完全指摘・通常プレイ | [K0021](research/knowledge/items/K0021-n9-all-81-first-moves-win.md) · computed | weak; first-player-win | root, first-moves; 81/81 first moves | exact-search | 中央初手の空盤証明書あり。全81初手は別探索; 14非中央D4クラスの独立探索記録; 全81初手が先手勝ち |
| 10×10（全初手）; 標準q=4・完全指摘・通常プレイ | [K0022](research/knowledge/items/K0022-n10-all-100-first-moves-classified.md) · computed | weak; second-player-win | root, first-moves; 100/100 first moves; 15 D4 representatives | exact-search, csv-audit, partial-kyoenc4 | 空盤全体の単一KYOENC4なし; CSV監査と選択局面独立Rust検査; 100初手完全分類と空盤証明書未統合を区別 |
| 11×11; 標準q=4・完全指摘・通常プレイ | [K0023](research/knowledge/items/K0023-n11-exact-safe-layers-and-unknown-winner.md) · computed | unsolved; unknown | safe-layers; 厳密列挙は層0〜5のみ | exhaustive-enumeration | 空盤勝敗証明書なし; 禁止四点独立再計数・小盤回帰; 打切りP/Nは真の勝敗ではない |
| w×m・q点版; q≥4,w固定,m≥T_{w,q}=min(A,B) | [K0024](research/knowledge/items/K0024-fixed-width-q-point-threshold.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全安全局面 | mathematical-proof | 一般証明。具体盤の巨大証明書は不要; 67盤の有限検算は支持資料; 先手勝ち iff q偶数かつw奇数 |
| w×m・q>2w; q≥4,q>2w,m≥1 | [K0025](research/knowledge/items/K0025-q-above-two-width-all-lengths.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof | 一般分離証明; 整数幾何と容量の証明; g=(w min(m,q−1)−\|S\|) mod2 |
| w×m・標準q=4; w固定、m≥T_w=3+2{C(3w−2,3)−(w−1)} | [K0068](research/knowledge/items/K0068-standard-fixed-width-parity-threshold.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全安全局面 | mathematical-proof | 全称証明; 有限長方形検算は支持; g=(3w−\|S\|) mod2 |
| 2×m・q=4; q=4,m≥1 | [K0069](research/knowledge/items/K0069-two-row-all-lengths-strong-solution.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | exhaustive-enumeration, mathematical-proof | 短盤全数＋長盤一般証明; 短盤参照mex検算; m≥6は空盤後手勝ち。短盤は個別分類 |
| 3×m・q=6; q=6,w=3,m≥9 | [K0070](research/knowledge/items/K0070-width-three-q6-stabilization.md) · proved | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; m≥9の全安全局面 | mathematical-proof, exhaustive-enumeration | 解析証明＋有限排除; 下界証人と有限補完検査; M_{3,6}=9、g=(15−\|S\|) mod2 |
| 3×m・q=5; q=5,w=3,m≥12 | [K0071](research/knowledge/items/K0071-width-three-q5-exact-stabilization.md) · proved | strong; second-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; m≥12の全安全局面 | mathematical-proof, exhaustive-enumeration, independent-enumeration | 解析上界m≥40＋m=12..39有限完全排除; 小盤subset DPと独立determinant監査; g(S)=(12-\|S\|) mod 2 |
| 高qの標準整数格子; 連続整数行、(q=2w,w≥5)または(q=2w−1,w≥6) | [K0072](research/knowledge/items/K0072-mod9-integer-row-separation.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof | mod9有限剰余証明; 円条件の独立determinant照合; M=q−1 |
| line-only w×m; line-only,q≥4,q>w | [K0075](research/knowledge/items/K0075-line-only-all-lengths-solution.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof | 幾何分離証明; 有限検算を一般証明と区別; g=(w min(m,q−1)−\|S\|) mod2 |
| circle-only w×m; circle-only,q≥4,q>2w | [K0076](research/knowledge/items/K0076-circle-only-all-points-legal.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全局面 | mathematical-proof | 禁止なしの一般証明; 円と直線の交点上界; g=(wm−\|S\|) mod2 |
| 4×m・q=8; q=8,w=4,m≥11 | [K0077](research/knowledge/items/K0077-width-four-q8-stabilization.md) · proved | strong; second-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; m≥11の全安全局面 | mathematical-proof, exhaustive-enumeration | m≥13の一般計数＋m=11,12完全排除＋m=10不足極大証人; m=10証人を全三点曲線生成で独立検査; g(S)=(28-\|S\|) mod 2 |
| 5×m・q=8; 標準整数格子・q=8,w=5,m≥16・通常プレイ | [K0331](research/knowledge/items/K0331-width-five-q8-exact-stabilization.md) · proved | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; m≥16の全安全局面 | mathematical-proof, exact-search, independent-enumeration | m=16..185の510 CNFを全DRAT検査、m≥186は曲線充填一般証明; 全有限長の円集合が別C++生成と一致、m=15証人は全三点曲線で検査; g(S)=(35-\|S\|) mod2。境界3トレースを保存、他はhashと再生成コードを保存 |
<!-- END GENERATED SOLUTION STATUS -->

## 読み方

- 現在の研究結果と未解決問題：[knowledgeの入口](research/knowledge/README.md)、[全K項目](research/knowledge/generated/index.md)、[検証境界・警告](research/knowledge/generated/summary.md)。
- ルール・使い方・証明方式：[reader向け文書](docs/README.md)。
- 再現コード・入力・出力・監査：[実験の入口](research/experiments/README.md)。
- 発見順・判断・失敗：[研究ログ](research/log/README.md)。旧計画・撤回済みまとめ・当時の索引：[archive](research/archive/README.md)。
- 構造整理の履歴とprovenance：[MIGRATION](research/MIGRATION.md)。

## リポジトリ構成

```text
research/
  knowledge/       現在知識の正本items、生成ビュー、schema、語彙、template
  experiments/     再現可能な実験単位：scripts、input/output、report、hash
  log/             研究の時系列、発見・失敗・引き継ぎ
  archive/         歴史的資料、旧索引、移行時のpath対応表
  README.md        研究全体の恒久的な入口
  MIGRATION.md     移行履歴
docs/             現在有効なreader向け説明
results/          公開・横断集計のmachine-readable outputs
certificates/     証明書の案内・公開資産
tools/knowledge/  knowledge検査・生成と参照検査
cpp/              共通C++ solver・証明書生成器・検査器
scripts/          共通再現runner・監査・共有研究ライブラリ
rust/             独立verifier
Kyouen/           Leanのルール・証明書健全性定理
```

実験固有の小さな出力は各experimentのoutputに置き、横断集計をresultsに置きます。
巨大証明書の圧縮配布とhashは[release-assets](release-assets/README.md)を参照してください。

## ビルドと検査

repo rootで実行します。

```sh
uv sync --locked
uv run --locked python tools/knowledge/check.py
uv run --locked python -m unittest discover -s tools/knowledge/tests
uv run --locked python tools/knowledge/build.py
git diff --exit-code -- README.md research/knowledge/generated
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel 2
lake build
```

C++検査器の使用方法は[reproducibility guide](docs/REPRODUCIBILITY.md)、
証明書形式は[順位付きAND/OR形式](docs/CERTIFICATE_FORMAT.md)と[KYOENC4](docs/KYOENC4.md)、
検証の信頼境界は[証明方式の説明](docs/PROOF_STATUS.md)を参照してください。
CIは小盤証明書、固定幅・幾何・ゲーム構造・飽和配置の既存回帰検査、Lean、knowledge integrityを検査します。

## English

Research on Kyouen covers square-board optimal play, fixed-width q-point games, misère play, safe configurations and lattice geometry.
The canonical current knowledge is in research/knowledge/items; experiments, chronological logs and historical archives have separate physical homes.
