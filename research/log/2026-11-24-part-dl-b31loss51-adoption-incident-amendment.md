# Part DL b31loss51 adoption — incident amendment (2026-11-24)

- 単一オーナー宣言 Part DL (commit `00e17cda04ce29dc5ea4d7011c12baef5d9437b6`,
  2026-11-24T08:20:29Z, `research/log/2026-11-24-part-dl-b31loss51-adoption-declaration.md`)
  に対する事後修正記録。本修正は verdict を一切消費しない。**11×11 空盤は
  引き続き UNKNOWN**。batch-31 51-LOSS canonical adoption の法的実体 (merged cache
  `60222707…` 6,405行, WIN 158 / LOSS 6,247) は本修正の前後で不変。

## 時系列 (honest)

1. 宣言前の機械計算・公式隔離 rerun 一式が完了し、宣言原稿に pin を記載。
2. 2026-11-24T08:16..08:19Z (近似): 実行環境 reset により、宣言より前に
   作成済みだった DL 作業成果物 (scripts 4・increments・merged cache・
   refresh outputs・decomp) が全て消失。この時点で出版済みの成果物は皆無
   (worktree は未出版だった)。宣言出版後の回収手段は GitHub 上の bytes のみ。
3. 2026-11-24T08:20:29Z: 宣言のみ出版 (上記 commit)。宣言文面は事前登録された
   機械観測を全て含み、唯一の生き残り資料となった。
4. 同日 (本修正の執筆時点まで): 宣言 bytes からの完全再構築を実施。
   249 個の入力 file (batch-31 kit 194 + DI kit 40 + BASE/DB 出版物 + graph/
   update8/board/policy/quarantine) を全て sha 検証のうえ再取得・再構成。

## 再検証された機械観測

- merged cache =
  `merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-20261124.cache`
  `60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84`
  (6,405行・264,619 bytes・WIN 158 / LOSS 6,247): BASE `04b0a239…` (6,354行) +
  increment 51行の fail-closed union merge として**宣言 pin どおり byte 再現**
  (3回実行・全回同一)。
- refresh 4出力も宣言 pin どおり byte 再現:
  refresh-summary `fea0b0d4…`・closure-classes `50841fa4…`・
  per-root-coverage `136e308a…`・probe-worklist `006ccd78…` (repo外 regen)。
- BASE 側 (Part DB) 3出力 `1fc531d3` / `b37425d7` / `8f69d5bb` 再現、
  BASE worklist regen `4ecb9a0a…` (repo外) 再現。
- その他の宣言 pin (kit manifest 194/40 files・status.log 59行・val-gate 6-host
  node-exact・raw 110 files・DI 30M ad043 WIN (1, 18,247,029)・DI anchors
  ad054 (2, 1,644,957) / ad055 (1, 3,364,655) 15M/30M budget 独立 node-exact・
  exh15m clone byte-equal): 全て再取得 bytes と照合し一致。
- 本セッションで公式隔離 rerun (clean copy tree: maker→merger merge×3→
  refresh regen→extractor) を改めて実施し、下記の再生成 pin が独立環境から
  再現することを確認した (decomp 出力は 2つの独立 tree で byte 一致)。

## SUPERSEDED pin (宣言時 → 再構築後)

宣言に記載された以下の tool/output sha は、環境 reset 後の再構築で**置き換え**
られる。理由はいずれも「再構築された script bytes と再生成出力」であり、
内容の gate (行数・検証 gate・機械観測値) は全て宣言どおり:

| 成果物 | 宣言 pin (superseded) | 再構築 pin (正本) |
|---|---|---|
| maker `scripts/make_increments_b31loss51.py` | `65f5eec6e5f0ae710a7e4ef2096e308fd71990561921696d63fc90e5f27a7aaa` | `d3e0e07937a77db7773508af5b3c536f540365e08edbaf976ea5a56349c404a1` |
| increment `output/increment-b31loss51-20261124.cache` | `87ffb450a32b7409682e27efc258b5ed514d32dbc4c5a2b983d3846031403d67` | `e750a0e6ea4333f9705c0898914a289c388143ac78cbf58d337d640a7457c0d5` |
| manifest `output/increments-manifest.json` | `ad6c4e2336d71b951769e6c280b18988db0ba4acde2340a2b386f1d0f41d5d12` | `ae06f855a34cc186eb1811629f2911958fefc7ed073e220bdceba76388575f27` |
| merge-audit ×3 | `ed3577c464d89b3539d422d72f62d8e69e91f1736f0a12b994ce5db316adae7c` | `dc312c0720f81b61bbe3bb70e55736d2773de8714bd782992098c1341b531622` |
| refresh `reaudit/scripts/refresh_adoption_b31loss51.py` | `a6ed4b7eb280d9f21a9591c6d02c11293ed25918afbba115248b3d750ad44d52` | `e92fa80e7d8d9ac46f9dd66b90fab6cebab349948fdb14a916f180c2611b81e4` |
| extractor `scripts/compare_deltas_b31loss51_adoption.py` | `83825eb590106e66c747d35e084d3c602f5f4ef94224f0c973f0ddaa2d66a323` | `fab162676dd7452699af68978bcf2cecd75bed440e71d511e114172a62c55b9e` |
| decomp `output/decomp-deltas-b31loss51-adoption.json` | `1d55167920a8988daceb622424787b3deef227f379ded4e1b5ee96a0aac5fa7f` | `0af301b81fbac18eb1a8a844467eb294a141828203f4585971e736e483109120` |

注意: increment / manifest / merge-audit (そして merged cache である
`60222707…`) 再生成 bytes は**内容的に宣言機械観測と同一** (51行 =
header 42 + s5 verdict 51・row_counts {probed 55, adopted 51, prior 0,
wins 4, exhausted 0}・merge-audit は merger 起動時の path 表記差のみで
内容同一) であり、sha 差は docstring・路径表記に由来する。**merged cache
`60222707…` は宣言 pin のままで不変** (美感の随机性ではなく gate 済み再現)。

merge-audit の sha は merger 起動時の相対 path 表記に依存する
(実験dir を cwd とし `../n11-centralreply-class2251-…/output/…` 形式で
起動した場合に `dc312c07…` が再現する)。絶対 path 起動では内部的な
rows/sha は全て同一でも file 文字列が異なり sha が変わる
(本セッションで機械確認: 内容差は path 文字列のみ)。

## 宣言 erratum

- 宣言203行付近「holder union 126 (5804 own 51・8730 2・**8811 2**・…)」の
  うち **8811 は誤りで own 1 が正しい**。機械観測: member-loss 分布
  {1: 102, 2: 23, 51: 1} (102 + 23×2 + 51 = 126 ✓)、closure delta
  8730 (60,56)→(30,54) は −2、8811 (50,55)→(38,54) は **−1**。
  宣言自身の closure delta とも整合するのは own 1 のみ。
- 宣言132行の BASE refresh-summary pin
  `1fc531d32fcd8817ec2b4bcfafea2b2c40fecde409c62347da3d7e7e1d601148` は
  正しい (Part DB 出版物と byte 一致)。再構築中に extractor 定数へ
  `…faea6b2c…` という転写 typo が混入したが、extractor 自身の第一
  gate が即座に捕捉し、wave 出版前に修正して DB 出版 bytes と照合済み。

## 原因と工程修正

- 原因: 宣言前の成果物を「宣言出版 → 各 wave 出版」の間の数分、非出版の
  worktree に置いたまま実行環境維持に依存していた。環境 reset は予告なく
  発生しうる。
- 工程修正 (本修正自体が適用例): **各宣言の直後に成果物 wave を即時出版
  する** (publish-then-execute の徹底)。再計算した pin は再計算と同時に
  publish し、非出版の局所状態に唯一の証拠を置かない。失敗 (reset, timeout,
  upload error) も実験事実として log に残す。

## 出版の位置づけ

本修正は Part DL の wave A–E 出版に先行して出版される。各 wave 直前の
racing guard (list_commits) は宣言どおり維持する。11×11 UNKNOWN・
verdict 不消費・WIN 4行 (ad024/ad028/ad043/ad055) unconsumed の担保は
本修正によっても一切変わらない。
