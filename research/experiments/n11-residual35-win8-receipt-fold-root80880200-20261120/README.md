# n11-residual35-win8-receipt-fold-root80880200-20261120

fold21（第28 receipt・11番目の WIN8 receipt fold）。出版済み K1124 の WIN8-D10 証明書
（root `00000000000000801202000800880200`・石 [9,19,23,35,49,57,60,71]・証明書 SHA-256 `eca214f0c53f966c912f3d18b9816dc74baa250a2fe538bfcb2734076512fabf`・
25,783 行 934,278 bytes・19 gate 正本 `n11-residual45-win8-cert-extract-root80880200-20261120`・
監査正本 SHA-256 `422e61095e80ee5ea6a52278e2ba52bb18d4ea301cab4c26e1e45d9c9701f172`・
K1089 replacement16 掃引由来の両 AND 順序 uncapped probes 618,359/669,067〔andclose1/andclose0・loss=true・terminal 石数範囲 [14,18]〕・
抽出 node 会計 A1 1,670,778 / B 1,383,269・third-method terminal 9,204・visited 57,636・winner 37,121・loser 11,311・応手辺 52,219・
mobility 46・主張 3 行・K1097 win16 footprint intrinsic == claimed == 3 行）を、五親 S6 frontier receipt チェーン（… fold19 → fold20）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold21-win8-root80880200-single-owner-note.md`（先行出版・fold20 出版後の残余 38 baseline）。

## 候補選定（fold20 適用後状態での機械比較）

着手時に fold20 出版機を隔離 W 複写で再実行して出力 SHA-256 `76fd255b…` と byte-identical であることを確認した上で、
出版済み WIN8 候補 K1123（root `00000000020809002000480100000`）・K1124（root 80880200）・K1125（root `00000000000000801202000000840500`）の
6 石部分幾何 28 正準行を fold20 適用後状態に対して機械分類した:
K1123 は open 4 行（主張 3 + 余剰 1・閉鎖 edge cost 321）・**K1124 は open 8 行（主張 3 + 余剰 5・cost 576・影響 7 親で class 2/4/6 混在）**・
K1125 は open 6 行（主張 3 + 余剰 3・cost 484）。frontier 削減最大として K1124 を fold21 に選定した。

## 本実験の設計（FOLD_PREVERIFIED_CHAIN 第3適用機）

fold21 は `research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md`（commit `fbea3ecc`）で採用した rerun-gate 再設計の第3適用機である。

1. rerun gate は「直前機（fold20 出版機）のみ 1 回再実行」。上流（fold10〜fold19 正本・証明書・監査群）は SHA-256 pin + チェーン全段 frontier 再計算で検証する。
2. fold20 出版機（SHA-256 `9e141d4a721025fd55a5bda68266a5f1b43cbcb65112f438839b0db351a06f72`）自身が PREVERIFIED スイッチを持つため、
   fold21 の rerun gate は fold20 出版機を**pristine のまま**隔離 W 複写（FOLD20_W）の下で実行し、
   出力 SHA-256 が出版 fold20 正本（`76fd255b…`）と一致することだけを gate する。fold19 rerun gate・K1121 gate 群は
   この rerun の内部で推移的に再検証される（fold21 機は preverified 写しの生成・reverse patch 機構を持たない）。
3. fold21 機自身も PREVERIFIED スイッチを実装し、fold22 が本機を preverified モードで 1 回再実行できる
   （`FOLD_PREVERIFIED_CHAIN=1` で fold20 rerun gate のみをスキップ）。

実測では本機は**約 6.8 秒/実行**（fold20 出版機 pristine rerun 約 4.8 秒〔その内部の fold19 rerun・fold18 系再検証を含む〕を含む）であり、
fail-closed 検証内容は上流 SHA pin + チェーン全段 frontier 再計算で保たれている。

## 入力（fail-closed pin）

チェーン入力は fold20 と同一系統の 12 blob SHA-1 pin + **40** SHA-256 pin の**合計 52 pin**（worklist / ledger / globalFold /
previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth 正本 /
sv17 正本・証明書 / fold10 正本 / K1096 正本・証明書 / K1097 正本 / fold11〜20 正本とその証明書・監査 / K1119 監査正本・証明書 /
**fold20 正本**・**K1124 監査正本**・**K1124 証明書本体**〔fold21 用の追加 3 pin〕）を W 相対パスで全照合する。
さらに rerun gate 用に fold20 出版機（`9e141d4a…`）の機械 SHA-256 pin を組み込む。

## 機械

`scripts/fold_win8_root80880200.py`（fold20 出版機を `scripts/build_fold21.py` で変換生成・1,099 行・純 Python・乱数・時刻なし・約 6.8 秒/実行）。主要 gate:

- チェーン全段（fold4/56/9-12/13-16/17/18/19/20）frontier 再計算・出版値照合。fold20 chaining は被覆 8 行の open 性・記録 cost 照合・
  frontier_after 出版値（6,144/486,819・solved 1,704・incidence 11,701・s6_needed 4,452・cost_needed 353,267）・
  residual38 == residual41 − fold20 主張 3 行の差分照合・closed target 74 を fail-closed で検証。
- **fold20 pristine rerun gate**: fold20 出版機（SHA pin）を隔離 W 複写（FOLD20_W）の下で pristine 実行し、
  出力 SHA-256 が出版 fold20 正本と一致しなければ fail-close。fold19 rerun gate・K1121 gate 群はこの rerun の内部で推移的に再検証される。
- K1124 19 gate 全再検証（g01 K1089 master SHA pin `808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc`・
  g02/g03 runner v17 blob pin `c132cc6425eee3feaeef1d697dd74f968cfedb59`・g05 mobility 46・g06 uncapped probes 618,359/669,067〔andclose1/andclose0・loss=true・terminal 石数 [14,18]〕・
  g07 主張 3 行〔`g07_k1089_root_claimed_coverage_3rows`・`== 3` 定数 fail-closed〕・g08 probe 再現 pilot_d6 4・andclose 2/2・
  g13 node 会計 A1 1,670,778 / B 1,383,269・g16 第三方法 miss 0/extra 0/failure null〔terminal 9,204・visited 57,636・winner 37,121・loser 11,311・応手辺 52,219〕・
  g17 三方法集計一致〔Bareiss 46 subroot〕・g19 K1097 footprint claimed == intrinsic == 3 行と k1097 SHA pin `2896deb0…`）・
  証明書全文 byte 検証（934,278 bytes・25,783 行・sorted unique・header/root 行・row 形式・
  root 幾何〔8 石・quadruple-free・D4 正準〕・合法手 46 の独立再導出・third_method 集計）。
- K1097 27 gate・win16 footprint の root 80880200 行の intrinsic == claimed == 3 行・49 行 exactly-once partition・
  residual23 と win16 主張の不交差・主張 3 行が residual38 内。
- WIN8 被覆幾何 2 方法独立計算の一致（8 D4 像 × C(8,2) 2 石除去 224 操作 vs root の C(8,6)=28 部分集合直列挙。refsolve `coverage_of82` と同一規約・D4 同変性）。
- 再導出 target 行 == K1124 g07 主張 3 行・chain 不整合（worklist-but-not-open）0。

## 結果

- **receipt は open 8 行を閉じた**: K1089/K1124/K1097 主張 3 行（5親 target 内）`0000000000000000380000000a002000`（cost 64・unswept・c2×2 需要行）・
  `00000000000000801202000000800200`（cost 74・unswept・c2×2 需要行）・`00000000000000801202000000880000`（cost 67・unswept・c2×2+c4×2 需要行）に加え、
  **target 外 open 5 行** `00000000000000801002000000880200`（cost 76・c4×2）・`00000000000000801002000800080200`（cost 72・c4×2）・`00000000000000801002000800880000`（cost 63・c4×2）・
  `00000000000000801202000000080200`（cost 78・c2×2+c4×2）・`00000000000000801202000800000200`（cost 82・c2×2）
  （いずれも unswept・同じ root の C(8,6) 部分集合幾何に内在）を併閉。余剰 5 行は主張から分離記録（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 576・5親112行 target: 74 → **77 行**・残余 38 → **35 行**。
- frontier: 6,144/486,819 → **6,136/486,243**・solved S6 1,704 → **1,712**・parent 行 incidence 11,701 → **11,683**
  （影響 7 parent・class 4 を 3・class 2 を 3・class 6 を 1・完全閉鎖 0）。
- s6_needed_by_open_classes 4,452 → **4,444**・cost_needed_by_open_classes 353,267 → **352,691**。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 8（本 receipt で閉鎖）・not-in-worklist 19・closed-before-this-receipt 1。
- win16 候補は 6 → **5 根**（主張 15 → 12 行）。K1097 の残余23行掃引計画は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root80880200.py   # env FOLD21_W で W ルートを上書き
```

出力 `output/win8-root80880200-receipt-fold-20261120.json`
（26,113 bytes・SHA-256 `9a4da2f61fb5010ebfbddf784cd76f5972b438c244fa29c1f96f2c3cde65cb39`・
同一 cwd 2 回 + 隔離 W 複写・別 cwd・別 HOME 1 回の 3 実行で byte-identical・3 実行とも GATE FAILED 0・52 input pin 全照合）。

構築した W では fold20 の入力一式に加えて fold20 正本・K1124 監査正本・K1124 証明書本体の 3 ファイルと
fold20 出版機（pristine）を配置し、全 52 pin を機械に照合させた。

## 生成の注記

機械は `scripts/build_fold21.py`（全置換が出現回数 assert で機械検証・stale 定数 grep 検査・py_compile・ast 解析）で
fold20 出版機（SHA pin `9e141d4a…`）から生成した。生成段階で転写ミス 3 件を捕捉・修正した
（print 行の k1121 アンカー残存・retired_root_predecessor hex 32 桁化・fold20 record パス出現回数 7 の assert）。
fold21 機の preverified 写しピン・reverse patch 機構は「直前機は pristine 再実行でよい」設計を踏襲した。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
