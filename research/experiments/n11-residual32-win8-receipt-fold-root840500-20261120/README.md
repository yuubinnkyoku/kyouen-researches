# n11-residual32-win8-receipt-fold-root840500-20261120

fold22（第29 receipt・12番目の WIN8 receipt fold）。出版済み K1125 の WIN8-D10 証明書
（root `00000000000000801202000000840500`・石 [8,10,18,23,49,57,60,71]・証明書 SHA-256 `21ad61959f6b2ae13e2e24fd98842788c88ada50643ccfd1f88a459701d0cbcc`・
29,468 行 1,067,425 bytes・19 gate 正本 `n11-residual45-win8-cert-extract-root840500-20261120`・
監査正本 SHA-256 `06c65f7611b7fea17131d5e13b28792aee1b7d723e7b8cdb1cb3b54012282886`・
K1089 replacement16 掃引由来の両 AND 順序 uncapped probes 736,409/878,391〔andclose1/andclose0・loss=true・terminal 石数範囲 [14,18]〕・
抽出 node 会計 A1 2,310,103 / B 1,984,636・third-method terminal 9,810・visited 59,990・winner 38,458・loser 11,722・応手辺 52,360・
mobility 58・主張 3 行・K1097 win16 footprint intrinsic == claimed == 3 行）を、五親 S6 frontier receipt チェーン（… fold20 → fold21）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold22-win8-root840500-single-owner-note.md`（先行出版・fold21 出版後の残余 35 baseline）。

## 候補選定（fold21 適用後状態での機械比較）

着手前に fold21 出版機のチェーン再計算部を複写した事前検証 probe で fold21 正本（SHA-256 `9a4da2f6…`）を pin し、
fold21 適用後 open 6,136 行 / 486,243 cost に対して出版済み WIN8 候補 K1123（root `00000000020809002000480100000`）・
K1125（root `00000000000000801202000000840500`）の 6 石部分幾何 28 正準行を機械分類した:
K1123 は open 4 行（主張 3 + 余剰 1・閉鎖 edge cost 321）・**K1125 は open 6 行（主張 3 + 余剰 3・cost 484・影響 4 親すべて class 2）**。
fold21 の閉鎖 8 行は両根の 6 石部分幾何と不交差（closed-by-fold21 0・機械確認）。frontier 削減最大として K1125 を fold22 に選定した。

## 本実験の設計（FOLD_PREVERIFIED_CHAIN 第4適用機）

fold22 は `research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md`（commit `fbea3ecc`）で採用した rerun-gate 再設計の第4適用機である。

1. rerun gate は「直前機（fold21 出版機）のみ 1 回再実行」。上流（fold10〜fold20 正本・証明書・監査群）は SHA-256 pin + チェーン全段 frontier 再計算で検証する。
2. fold21 出版機（SHA-256 `44399cc59ef088ad25e90411f4404dbd0bad8ff14bc7c8a50be1a91bcc04102b`）自身が PREVERIFIED スイッチを持つため、
   fold22 の rerun gate は fold21 出版機を**pristine のまま**隔離 W 複写（FOLD21_W）の下で実行し、
   出力 SHA-256 が出版 fold21 正本（`9a4da2f6…`）と一致することだけを gate する。fold20 rerun gate・K1124 gate 群は
   この rerun の内部で推移的に再検証される（fold22 機は preverified 写しの生成・reverse patch 機構を持たない）。
3. fold22 機自身も PREVERIFIED スイッチを実装し、fold23 が本機を preverified モードで 1 回再実行できる
   （`FOLD_PREVERIFIED_CHAIN=1` で fold21 rerun gate のみをスキップ）。

実測では本機は**約 8.1 秒/実行**（fold21 出版機 pristine rerun 約 6.8 秒〔その内部の fold20/19/18 系再検証を含む〕を含む）であり、
fail-closed 検証内容は上流 SHA pin + チェーン全段 frontier 再計算で保たれている。

## 入力（fail-closed pin）

チェーン入力は fold21 と同一系統の 12 blob SHA-1 pin + **43** SHA-256 pin の**合計 55 pin**（worklist / ledger / globalFold /
previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth 正本 /
sv17 正本・証明書 / fold10 正本 / K1096 正本・証明書 / K1097 正本 / fold11〜21 正本とその証明書・監査 / K1119 監査正本・証明書 /
**fold21 正本**・**K1125 監査正本**・**K1125 証明書本体**〔fold22 用の追加 3 pin〕）を W 相対パスで全照合する。
さらに rerun gate 用に fold21 出版機（`44399cc5…`）の機械 SHA-256 pin を組み込む。

## 機械

`scripts/fold_win8_root840500.py`（fold21 出版機を `scripts/build_fold22.py` で変換生成・1,148 行・純 Python・乱数・時刻なし・約 8.1 秒/実行）。主要 gate:

- チェーン全段（fold4/56/9-12/13-16/17/18/19/20/21）frontier 再計算・出版値照合。fold21 chaining は被覆 8 行の open 性・記録 cost 照合・
  frontier_after 出版値（6,136/486,243・solved 1,712・incidence 11,683・s6_needed 4,444・cost_needed 352,691）・
  residual35 == residual38 − fold21 主張 3 行の差分照合・closed target 77 を fail-closed で検証。
- **fold21 pristine rerun gate**: fold21 出版機（SHA pin）を隔離 W 複写（FOLD21_W）の下で pristine 実行し、
  出力 SHA-256 が出版 fold21 正本と一致しなければ fail-close。fold20 rerun gate・K1124 gate 群はこの rerun の内部で推移的に再検証される。
- K1125 19 gate 全再検証（g01 K1089 master SHA pin `808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc`・
  g05 mobility 58・g06 uncapped probes 736,409/878,391〔andclose1/andclose0・loss=true・terminal 石数 [14,18]〕・
  g07 主張 3 行〔`g07_k1089_root_claimed_coverage_3rows`・`== 3` 定数 fail-closed〕・g08 probe 再現 pilot_d6 4・andclose 2/2・
  g13 node 会計 A1 2,310,103 / B 1,984,636・g16 第三方法 miss 0/extra 0/failure null〔terminal 9,810・visited 59,990・winner 38,458・loser 11,722・応手辺 52,360〕・
  g17 三方法集計一致〔Bareiss 58 subroot〕・g19 K1097 footprint claimed == intrinsic == 3 行と k1097 SHA pin `2896deb0…`）・
  証明書全文 byte 検証（1,067,425 bytes・29,468 行・sorted unique・header/root 行・row 形式・
  root 幾何〔8 石・quadruple-free・D4 正準〕・合法手 58 の独立再導出・third_method 集計）。
- K1097 27 gate・win16 footprint の root 840500 行の intrinsic == claimed == 3 行・49 行 exactly-once partition・
  residual23 と win16 主張の不交差・主張 3 行が residual35 内。
- WIN8 被覆幾何 2 方法独立計算の一致（8 D4 像 × C(8,2) 2 石除去 224 操作 vs root の C(8,6)=28 部分集合直列挙。refsolve `coverage_of82` と同一規約・D4 同変性）。
- 再導出 target 行 == K1125 g07 主張 3 行・chain 不整合（worklist-but-not-open）0。

## 結果

- **receipt は open 6 行を閉じた**: K1089/K1125/K1097 主張 3 行（5親 target 内）`00000000000000801202000000800100`（cost 75・unswept・c2×2 需要行）・
  `00000000000000801202000000800400`（cost 74・unswept・c2×2 需要行）・`00000000000000801202000000840000`（cost 73・unswept・c2×2 需要行）に加え、
  **target 外 open 3 行** `00000000000000801202000000000500`（cost 87・c2×2）・`00000000000000801202000000040100`（cost 89・c2×2）・`00000000000000801202000000040400`（cost 86・c2×2）
  （いずれも unswept・同じ root の C(8,6) 部分集合幾何に内在）を併閉。余剰 3 行は主張から分離記録（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 484・5親112行 target: 77 → **80 行**・残余 35 → **32 行**。
- frontier: 6,136/486,243 → **6,130/485,759**・solved S6 1,712 → **1,718**・parent 行 incidence 11,683 → **11,671**
  （影響 4 parent・すべて class 2〔`00000000000000003800000008002000` 14→11・`00000000000000801202000000000100` 51→48・`00000000000000801202000000000400` 47→44・`00000000000000801202000000040000` 69→66〕・完全閉鎖 0・parent-delta 計 12 == incidence 減分）。
- s6_needed_by_open_classes 4,444 → **4,438**・cost_needed_by_open_classes 352,691 → **352,207**。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 6（本 receipt で閉鎖）・not-in-worklist 22・closed-before-this-receipt 0
  （fold21 の閉鎖 8 行と本根の部分幾何の不交差と整合）。
- win16 候補は 5 → **4 根**（主張 12 → 9 行）。K1097 の残余23行掃引計画は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root840500.py   # env FOLD22_W で W ルートを上書き
```

出力 `output/win8-root840500-receipt-fold-20261120.json`
（25,349 bytes・SHA-256 `f6e011f4a16e6fe257694c3cd3ed90490623f84e1c24113c3f55df68ba3e3488`・
同一 cwd 2 回 + 隔離 W 複写・別 cwd・別 HOME 1 回の 3 実行で byte-identical・3 実行とも GATE FAILED 0・55 input pin 全照合）。

構築した W では fold21 の入力一式に加えて fold21 正本・K1125 監査正本・K1125 証明書本体の 3 ファイルと
fold21 出版機（pristine）を配置し、全 55 pin を機械に照合させた。

## 隔離 W 再構築の注記（実行環境リセットからの復元）

本実験の W は、実行環境が途中でリセットされ前段の隔離 W（W21）が失われたため、**repo に出版済みの chain 入力一式
（12 blob pin + 40 SHA-256 pin・fold21 出版機・fold18/19/20 出版機・fold18 preverified 写し）を raw で再取得して再構築した**。
再構築 W 上で fold21 出版機を pristine 実行し、出版 fold21 正本（`9a4da2f6…`）と byte-identical であることを最初に確認してから
fold22 を生成した（52 pin 全照合・チェーン全段再計算・fold20 rerun gate 推移的再検証すべて成立）。
重要証拠が再現不能なローカル状態にのみ存在しないことの実証例にもなっている。

## 生成の注記

機械は `scripts/build_fold22.py`（全置換が出現回数 assert で機械検証・stale 定数 grep 検査・py_compile・ast 解析）で
fold21 出版機（SHA pin `44399cc5…`）から生成した。生成時に stale 定数検査の誤陽性 1 件
（`FOLD21_W' は fold21 rerun gate が W21X 隔離複写に合法使用するため stale ではない）を修正した。
PIN256 は 40 → 43 件（fold21 正本・K1125 監査・K1125 証明書）。K1124 の残存参照は fold21 rerun gate の推移的再検証用 pin・controls 行のみ。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
