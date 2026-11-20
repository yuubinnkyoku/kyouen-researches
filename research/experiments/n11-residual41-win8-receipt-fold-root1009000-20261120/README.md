# n11-residual41-win8-receipt-fold-root1009000-20261120

fold19（第26 receipt・9番目の WIN8 receipt fold）。並走レーンが抽出・三重検証・出版した K1119 の WIN8-D10 証明書
（root `00000000000000801212000001009000`・石 [12,15,24,49,52,57,60,71]・証明書 SHA-256 `b4dd1e065ca2fdea4715e5b97e1145288a9861f738ccec5a241dd3c3c70d390c`・
16,262 行 587,989 bytes・19 gate 正本 `n11-residual51-win8-cert-extract-root1009000-20261120`・
監査正本 SHA-256 `4696ce1475fd3313c6bb46ebf553e48db4eff2d7182edb0f2b8015258fd17100`・
K1091 掃引由来の両 AND 順序 uncapped probes 192,365/229,502〔andclose1/andclose0〕・terminal 石数範囲 [14,18]・
抽出 node 会計 A1 865,602 / B 712,106・third-method terminal 5,783・visited 37,696・winner 24,352・loser 7,561・応手辺 34,261・
mobility 44・主張 4 行・K1097 win16 footprint intrinsic == claimed == 4 行）を、五親 S6 frontier receipt チェーン（… fold17 → fold18）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold19-win8-root1009000-single-owner-note.md`（先行出版・fold18 出版後の残余 45 baseline）。

## 本実験の設計（FOLD_PREVERIFIED_CHAIN）

fold19 は `research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md`（commit `fbea3ecc`）で採用した rerun-gate 再設計の最初の適用機である。

1. rerun gate は「直前機（fold18 出版機）のみ 1 回再実行」。fold11〜fold17 機の再帰 rerun 連鎖は fold19 機から削除し、
   上流（fold10〜fold17 正本・証明書・監査群）は SHA-256 pin + チェーン全段 frontier 再計算で検証する。
2. fold18 出版機は**改変しない**。通すのは marker-reversible な preverified 写し
   （`scripts/fold_win8_root00901010_preverified.py`・SHA-256 `d342f1f883d2e22ecca25903ec14ed24f16c77a0895e3ed022ab8832736e7f9e`・
   `scripts/make_preverified_patch.py` が自動生成し、reverse patch が出版機 SHA-256 `dcdfbf92d62409cc3a92f9f16f319e1328180622660b39791921b5de72800091` と厳密一致することを検証済み）。
   preverified 写しは env `FOLD_PREVERIFIED_CHAIN=1` のときのみ rerun gate 群をスキップし、デフォルトの挙動は元の完全連鎖機と同一。
3. fold19 機自身も PREVERIFIED スイッチを実装し、fold20 が fold19 機を preverified モードで 1 回再実行できる
   （guard マーカー `FOLD_PREVERIFIED_CHAIN_GUARD` BEGIN/END でスキップ範囲を機械検証する）。

実測では、fold11〜18 の再帰 rerun 連鎖を持つ旧 fold18 機は約 186 秒/実行だったのに対し、本設計の fold19 機は約 3.0 秒/実行
（うち preverified fold18 rerun が約 1.5 秒）であった。検証内容は上流 SHA pin + チェーン全段 frontier 再計算の fail-closed 構成を保つ。
設計ノートの事前試算（150〜180 秒）は保守的すぎた。旧機 186 秒のほぼ全てが再帰 rerun 連鎖のオーバーヘッドだったことが確定した。

## 入力（fail-closed pin）

チェーン入力は fold18 と同一系統の 12 blob SHA-1 pin + 34 SHA-256 pin の**合計 46 pin**
（worklist / ledger / globalFold / previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 /
fold_fourth_fifth_sixth 正本 / sv17 正本・証明書 / fold10 正本 / K1096 正本・証明書 / K1097 正本 / fold11〜17 正本とその証明書・監査 /
K1120 正本・証明書 / **fold18 正本**・**K1119 監査正本**・**K1119 証明書本体**〔fold19 用の追加 3 pin〕）を W 相対パスで全照合する。
さらに preverified rerun gate 用に fold18 出版機（`dcdfbf92…`）と preverified 写し（`d342f1f8…`）の 2 本の機械 SHA-256 pin を組み込む。

## 機械

`scripts/fold_win8_root1009000.py`（fold18 出版機を `scripts/build_fold19.py` で変換生成・1,028 行・純 Python・乱数・時刻なし・約 3.0 秒/実行）。主要 gate:

- チェーン全段（fold4/56/9-12/13-16/17/18）frontier 再計算・出版値照合。fold18 chaining は被覆 4 行の open 性・記録 cost 照合・
  frontier_after 出版値（6,157/487,800・solved 1,691・incidence 11,721・s6_needed 4,465・cost_needed 354,248）・
  residual45 == residual48 − fold18 主張 3 行の差分照合・closed target 67 を fail-closed で検証。
- **fold18 preverified rerun gate**: preverified 写しを隔離 W 複写（FOLD18_W）の下で 1 回実行し、
  出力 SHA-256 が出版 fold18 正本（`18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026`）と一致しなければ fail-close。
  K1120 gate 群は preverified 機の内部で再検証される。
- K1119 19 gate 全再検証（g01 K1091 master SHA pin `edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25`・
  g05 mobility 44・g06 uncapped probes 192,365/229,502〔andclose1/andclose0〕・terminal 石数範囲 [14,18]・
  g07 主張 4 行〔`g07_k1091_root_claimed_coverage_4rows`・`== 4` 定数 fail-closed〕・g08 probe 再現 pilot_d6 4・andclose 2/2・
  g13 node 会計 A1 865,602 / B 712,106・g16 第三方法 miss 0/extra 0/failure null・g19 K1097 footprint claimed == CLAIM〔4 行〕と k1097 SHA pin）・
  証明書全文 byte 検証（587,989 bytes・16,262 行・sorted unique・header/root 行・row 形式・
  root 幾何〔8 石・quadruple-free・D4 正準〕・合法手 44 の独立再導出・third_method 集計〔terminal 5,783・範囲 [14,18]・visited 37,696・winner 24,352・loser 7,561・応手辺 34,261〕）。
- K1097 27 gate・win16 footprint の root 1009000 行の intrinsic == claimed == 4 行・49 行 exactly-once partition・
  residual23 と win16 主張の不交差・主張 4 行が residual45 内。
- WIN8 被覆幾何 2 方法独立計算の一致（8 D4 像 × C(8,2) 2 石除去 224 操作 vs root の C(8,6)=28 部分集合直列挙。refsolve `coverage_of82` と同一規約・D4 同変性）。
- 再導出 target 行 == K1119 g07 主張 4 行・chain 不整合（worklist-but-not-open）0。

## 結果

- **receipt は open 5 行を閉じた**: K1091/K1119/K1097 主張 4 行（5親 target 内）
  `00000000000000003800200008001000`（cost 72・unswept・c2×2 需要行）・`00000000000000003800200009000000`（cost 78・unswept・c2×2）・
  `00000000000801212000000001000`（cost 78・unswept・c2×2）・`00000000000801212000001000000`（cost 74・unswept・c2×2）に加え、
  **target 外・worklist 上の open 行 1 行** `00000000000801212000000008000`（cost 80・unswept・c2×2・同じ root の C(8,6) 部分集合幾何に内在）を併閉。
  余剰 1 行は主張から分離して正確に記録した（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- closed edge cost 382・5親112行 target: 67 → **71 行**・残余 45 → **41 行**。
- frontier: 6,157/487,800 → **6,152/487,418**・solved S6 1,691 → **1,696**・parent 行 incidence 11,721 → **11,711**
  （影響 4 parent・いずれも class 2・完全閉鎖 0）。
- s6_needed_by_open_classes 4,465 → **4,460**・cost_needed_by_open_classes 354,248 → **353,866**。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 5（本 receipt で閉鎖）・not-in-worklist 23・closed-before-this-receipt 0。
- win16 候補は 8 → **7 根**（主張 22 → **18 行**）。K1097 の残余23行掃引計画は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root1009000.py   # env FOLD19_W で W ルートを上書き
```

出力 `output/win8-root1009000-receipt-fold-20261120.json`
（SHA-256 `c02d9a549fb685a1310813e47726598417907fe1e007495b06799ec0b57052ae`・
同一 cwd 2 回 + 別 W 複写・別プロセス 1 回の 3 実行で byte-identical・3 実行とも GATE FAILED 0・46 input pin 全照合）。

構築した W では fold18 の入力一式に加えて fold18 正本・K1119 監査正本・K1119 証明書本体の 3 ファイルと
fold18 出版機（pristine）・preverified 写しの 2 機械を配置し、全 46 pin を機械に照合させた。

## 生成と教訓の注記

機械は `scripts/build_fold19.py`（全置換が出現回数 assert 1 で機械検証・stale 定数 grep 検査・py_compile・ast 解析）で
fold18 出版機（SHA pin `dcdfbf92…`）から生成した。fold18 の教訓（転写漏れは fail-closed gate か数値照査で捕捉）に加え、
今回は説明文字列の転写ミスを出版前レビューで発見した: 証明書来源の説明文字列（K1097 claims_record）に
「intrinsic == claimed == 3 rows」（fold18 の root 00901010 では正しい値）が残っており、root 1009000 の正しい値は 4 行。
gate は最初から 4 行を検証しており数値への影響はないが、変換スクリプトに当該置換を追加して機械を再生成し、
3 実行 byte-identical をやり直した上で出版した（出版正本は修正後のみ）。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
