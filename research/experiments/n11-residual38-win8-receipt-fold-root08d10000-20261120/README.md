# n11-residual38-win8-receipt-fold-root08d10000-20261120

fold20（第27 receipt・10番目の WIN8 receipt fold）。並走レーンが抽出・三重検証・出版した K1121 の WIN8-D10 証明書
（root `00000000000000003800000008d10000`・石 [16,20,22,23,27,59,60,61]・証明書 SHA-256 `8513e36613c2676fb82816f47a1ecdda674264eedb9c583dae2616346f4000d2`・
28,328 行 1,026,202 bytes・19 gate 正本 `n11-residual48-win8-cert-extract-root08d10000-20261120`・
監査正本 SHA-256 `0088ebab040a29e608c987fb8ae866abf59253d60455b0d2ca6b6ef963170940`・
K1091 掃引由来の両 AND 順序 uncapped probes 564,695/673,870〔andclose1/andclose0〕・terminal 石数範囲 [14,18]・
抽出 node 会計 A1 2,428,240 / B 1,748,509・third-method terminal 15,513・visited 83,544・winner 53,570・loser 14,461・応手辺 72,930・
mobility 50・主張 3 行・K1097 win16 footprint intrinsic == claimed == 3 行）を、五親 S6 frontier receipt チェーン（… fold18 → fold19）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold20-win8-root08d10000-single-owner-note.md`（先行出版・fold19 出版後の残余 41 baseline）。

## 本実験の設計（FOLD_PREVERIFIED_CHAIN 第2適用機）

fold20 は `research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md`（commit `fbea3ecc`）で採用した rerun-gate 再設計の第2適用機である。

1. rerun gate は「直前機（fold19 出版機）のみ 1 回再実行」。上流（fold10〜fold18 正本・証明書・監査群）は SHA-256 pin + チェーン全段 frontier 再計算で検証する。
2. **preverified 写しが不要になった**: fold19 出版機（SHA-256 `51442d96341fcffc17d9cb72e36946cb68cd97100abaa6939b27e0d6a20949e8`）自身が採用設計の PREVERIFIED スイッチを持ち、
   デフォルト実行が軽量であるため、fold20 の rerun gate は fold19 出版機を**pristine のまま**隔離 W 複写（FOLD19_W）の下で実行し、
   出力 SHA-256 が出版 fold19 正本（`c02d9a54…`）と一致することだけを gate する。fold18 preverified rerun・その reverse patch 検証・K1120 gate 群は
   この rerun の内部で推移的に再検証される（fold20 機は preverified 写しの生成・reverse patch 機構をもう持たない）。
3. fold20 機自身も PREVERIFIED スイッチを実装し、fold21 が本機を preverified モードで 1 回再実行できる
   （`FOLD_PREVERIFIED_CHAIN=1` で fold19 rerun gate のみをスキップ）。

実測では本機は**約 4.8 秒/実行**（fold19 機 pristine rerun ≈3.0 秒〔その内部の fold18 preverified rerun ≈1.5 秒を含む〕を含む）であり、
fail-closed 検証内容は上流 SHA pin + チェーン全段 frontier 再計算で保たれている。

## 入力（fail-closed pin）

チェーン入力は fold19 と同一系統の 12 blob SHA-1 pin + **37** SHA-256 pin の**合計 49 pin**（worklist / ledger / globalFold /
previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth 正本 /
sv17 正本・証明書 / fold10 正本 / K1096 正本・証明書 / K1097 正本 / fold11〜18 正本とその証明書・監査 / K1119 監査正本・証明書 /
**fold19 正本**・**K1121 監査正本**・**K1121 証明書本体**〔fold20 用の追加 3 pin〕）を W 相対パスで全照合する。
さらに rerun gate 用に fold19 出版機（`51442d96…`）の機械 SHA-256 pin を組み込む。

## 機械

`scripts/fold_win8_root08d10000.py`（fold19 出版機を `scripts/build_fold20.py` で変換生成・1,055 行・純 Python・乱数・時刻なし・約 4.8 秒/実行）。主要 gate:

- チェーン全段（fold4/56/9-12/13-16/17/18/19）frontier 再計算・出版値照合。fold19 chaining は被覆 5 行の open 性・記録 cost 照合・
  frontier_after 出版値（6,152/487,418・solved 1,696・incidence 11,711・s6_needed 4,460・cost_needed 353,866）・
  residual41 == residual45 − fold19 主張 4 行の差分照合・closed target 71 を fail-closed で検証。
- **fold19 pristine rerun gate**: fold19 出版機（SHA pin）を隔離 W 複写（FOLD19_W）の下で pristine 実行し、
  出力 SHA-256 が出版 fold19 正本と一致しなければ fail-close。fold18 preverified rerun・reverse patch・K1119/K1120 gate 群は
  この rerun の内部で推移的に再検証される。
- K1121 19 gate 全再検証（g01 K1091 master SHA pin `edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`・
  g05 mobility 50・g06 uncapped probes 564,695/673,870〔andclose1/andclose0〕・terminal 石数範囲 [14,18]・
  g07 主張 3 行〔`g07_k1091_root_claimed_coverage_3rows`・`== 3` 定数 fail-closed〕・g08 probe 再現 pilot_d6 4・andclose 2/2・
  g13 node 会計 A1 2,428,240 / B 1,748,509・g16 第三方法 miss 0/extra 0/failure null・g19 K1097 footprint claimed == CLAIM〔3 行〕と k1097 SHA pin）・
  証明書全文 byte 検証（1,026,202 bytes・28,328 行・sorted unique・header/root 行・row 形式・
  root 幾何〔8 石・quadruple-free・D4 正準〕・合法手 50 の独立再導出・third_method 集計〔terminal 15,513・範囲 [14,18]・
  visited 83,544・winner 53,570・loser 14,461・応手辺 72,930〕）。
- K1097 27 gate・win16 footprint の root 08d10000 行の intrinsic == claimed == 3 行・49 行 exactly-once partition・
  residual23 と win16 主張の不交差・主張 3 行が residual41 内。
- WIN8 被覆幾何 2 方法独立計算の一致（8 D4 像 × C(8,2) 2 石除去 224 操作 vs root の C(8,6)=28 部分集合直列挙。refsolve `coverage_of82` と同一規約・D4 同変性）。
- 再導出 target 行 == K1121 g07 主張 3 行・chain 不整合（worklist-but-not-open）0。

## 結果

- **receipt は open 8 行を閉じた**: K1091/K1121/K1097 主張 3 行（5親 target 内）`00000000000000003800000008011000`（cost 74・unswept・c2 需要行）・
  `00000000000000003800000008500000`（cost 75・unswept・c2×2 需要行）・`00000000000000003800000008900000`（cost 76・unswept・c2/c4 需要行）に加え、
  **target 外 open 行 5 行** `00000000000000003800000000c10000`（cost 80）・`00000000000000003800000000d00000`（cost 83）・
  `00000000000000003800000008410000`（cost 70）・`00000000000000003800000008810000`（cost 72）・`00000000000000003800000008c00000`（cost 69）
  （いずれも unswept・同じ root の C(8,6) 部分集合幾何に内在）を併閉。余剰 5 行は主張から分離記録（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 599・5親112行 target: 71 → **74 行**・残余 41 → **38 行**。
- frontier: 6,152/487,418 → **6,144/486,819**・solved S6 1,696 → **1,704**・parent 行 incidence 11,711 → **11,701**
  （影響 4 parent・class 4 を 2・class 2 を 2・完全閉鎖 0）。
- s6_needed_by_open_classes 4,460 → **4,452**・cost_needed_by_open_classes 353,866 → **353,267**。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 8（本 receipt で閉鎖）・not-in-worklist 20・closed-before-this-receipt 0。
- win16 候補は 7 → **6 根**（主張 18 → 15 行）。K1097 の残余23行掃引計画は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root08d10000.py   # env FOLD20_W で W ルートを上書き
```

出力 `output/win8-root08d10000-receipt-fold-20261120.json`
（24,684 bytes・SHA-256 `76fd255bf16f0e434d15579cf148015bd564929e85910172f0a0ef87015842a2`・
同一 cwd 2 回 + 別 W 複写・別プロセス 1 回の 3 実行で byte-identical・3 実行とも GATE FAILED 0・49 input pin 全照合）。

構築した W では fold19 の入力一式に加えて fold19 正本・K1121 監査正本・K1121 証明書本体の 3 ファイルと
fold19 出版機（pristine）を配置し、全 49 pin を機械に照合させた。

## 生成の注記

機械は `scripts/build_fold20.py`（全置換が出現回数 assert で機械検証・stale 定数 grep 検査・py_compile・ast 解析）で
fold19 出版機（SHA pin `51442d96…`）から生成した。fold19 機の preverified 写しピン・reverse patch 機構は
「直前機は pristine 再実行でよい」設計に置き換え、説明文字列の転写ミスは今回は発生しなかった
（root 08d10000 の K1097 footprint は intrinsic == claimed == 3 行であり、claims_record 文字列の定数も 3 行版が正しい）。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
