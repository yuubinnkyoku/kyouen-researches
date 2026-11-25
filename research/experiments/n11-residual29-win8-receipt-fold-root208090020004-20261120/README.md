# n11-residual29-win8-receipt-fold-root208090020004-20261120

fold23（第30 receipt・13番目の WIN8 receipt fold）。出版済み K1123 の WIN8-D10 証明書
（root `00000000000020809002000480100000`・石 [20,31,34,49,60,63,71,77]・証明書 SHA-256 `b8145352cc1d8e21247595bdaedcb123c8e34cf0fb476502a561b46a106f701e`・
23,621 行 855,258 bytes・19 gate 正本 `n11-residual48-win8-cert-extract-root208090020004-20261120`・
監査正本 SHA-256 `6ea634c9fdd005626904669e08cb7139e59e78120a0b8c9e1dd48fde0b70ddf0`・
**fresh-probe 基盤**: fresh probes 350,792/442,824〔andclose1/andclose0〕の和 793,616 は出版済み K1119 fresh-probe 記録の総計と一致
（g01 は provenance log を git blob `51bad3fac4c36fcd1cbf6aeec01b7e153d9adb89`・SHA-256 `4d11ca896815b73e4e0616a07c81f7abc582d4f5401174462d63e3abd27a4472` で pin）・
抽出 node 会計 A1/B 3,009,765/3,009,765・third-method terminal 7,516・visited 49,094・winner 31,623・loser 9,955・応手辺 43,650・
終端石数範囲 [14,18]・Bareiss 54 subroot・mobility 54・主張 3 行・K1097 win16 footprint intrinsic == claimed == 3 行）を、
五親 S6 frontier receipt チェーン（… fold20 → fold21 → fold22）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold23-win8-root208090020004-single-owner-note.md`
（先行出版 `5a7e4f7c`・ファイル名記載の訂正 `62375b76`/`db5be5ad`・fold22 出版後の残余 32 baseline）。

## 候補選定（fold22 適用後状態での機械比較）

着手前に fold22 出版機のチェーン再計算部を複写した事前検証 probe で fold22 正本（SHA-256 `f6e011f4…`）を pin し、
fold22 適用後 open 6,130 行 / 485,759 cost に対して当該根の 6 石部分幾何 28 正準行を機械分類した:
**open 4 行（主張 3 + 余剰 1・閉鎖 edge cost 321）**。主張 3 行はすべて residual32 内かつ open、fold22 の閉鎖 6 行は 28 正準行と
不交差（機械確認）。影響 3 親はすべて class 2（`00000000000000003800000008001000` 9 → 8・
`00000000000000003800000008002000` 11 → 9・`00000000000000801202080000000000` 55 → 53）。
出版済み WIN8 証明書のうち未 fold は K1123 が最後（K1119 = fold19・K1121 = fold20・K1124 = fold21・K1125 = fold22 で fold 済み）であり、
fold23 として選定した。fold23 の成立により出版済み WIN8 証明書の receipt fold は枯渇する。

## 本実験の設計（FOLD_PREVERIFIED_CHAIN 第5適用機）

fold23 は `research/log/2026-11-20-n11-fold19-preverified-chain-adoption.md`（commit `fbea3ecc`）で採用した rerun-gate 再設計の第5適用機である。

1. rerun gate は「直前機（fold22 出版機）のみ 1 回再実行」。上流（fold10〜fold21 正本・証明書・監査群）は SHA-256 pin + チェーン全段 frontier 再計算で検証する。
2. fold22 出版機（SHA-256 `d5721408e7fb41e794175f3f3bb8b9d43fae13d18c244a831b81532aa9f1db1d`）自身が PREVERIFIED スイッチを持つため、
   fold23 の rerun gate は fold22 出版機を**pristine のまま**隔離 W 複写（FOLD22_W）の下で実行し、
   出力 SHA-256 が出版 fold22 正本（`f6e011f4…`）と一致することだけを gate する。fold21 rerun gate・K1125 gate 群は
   この rerun の内部で推移的に再検証される（fold23 機は preverified 写しの生成・reverse patch 機構を持たない）。
3. fold23 機自身も PREVERIFIED スイッチを実装し、fold24 が本機を preverified モードで 1 回再実行できる
   （`FOLD_PREVERIFIED_CHAIN=1` で fold22 rerun gate のみをスキップ）。

実測では本機は**約 10.0 秒/実行**（fold22 出版機 pristine rerun 約 8.1 秒〔その内部の fold21/20/19/18 系再検証を含む〕を含む）であり、
fail-closed 検証内容は上流 SHA pin + チェーン全段 frontier 再計算で保たれている。

## 入力（fail-closed pin）

チェーン入力は fold22 と同一系統の 12 blob SHA-1 pin + **46** SHA-256 pin の**合計 58 pin**（fold22 チェーン入力一式 +
**fold22 正本**・**K1123 監査正本**・**K1123 証明書本体**〔fold23 用の追加 3 pin〕）を W 相対パスで全照合する。
さらに rerun gate 用に fold22 出版機（`d5721408…`）の機械 SHA-256 pin を組み込む。

## 機械

`scripts/fold_win8_root208090020004.py`（fold22 出版機を `scripts/build_fold23.py` で変換生成・1,200 行・純 Python・乱数・時刻なし・約 10.0 秒/実行）。主要 gate:

- チェーン全段（fold4/56/9-12/13-16/17/18/19/20/21/22）frontier 再計算・出版値照合。fold22 chaining は被覆 6 行の open 性・記録 cost 照合・
  frontier_after 出版値（6,130/485,759・solved 1,718・incidence 11,671・s6_needed 4,438・cost_needed 352,207）・
  residual32 == residual35 − fold22 主張 3 行の差分照合・closed target 80 を fail-closed で検証。
- **fold22 pristine rerun gate**: fold22 出版機（SHA pin `d5721408…`）を隔離 W 複写（FOLD22_W）の下で pristine 実行し、
  出力 SHA-256 が出版 fold22 正本（`f6e011f4…`）と一致しなければ fail-close。fold21 rerun gate・K1125 gate 群はこの rerun の内部で推移的に再検証される。
- **K1123 19 gate 全再検証（fresh-probe 系 gate 名）**: g01 `g01_k1119_log_sha256_pin`（K1119 provenance log pin {git_blob `51bad3fac…`・sha256 `4d11ca89…`}）・
  g02 `g02_k1119_log_root_probe_total_published`（published_total 793,616・root_hex_in_log・uncapped_loss_true_statement_in_log）・
  g05 mobility 54・g06 `g06_fresh_probe_constants_match_k1119_total`（{andclose1 350,792・andclose0 442,824・sum 793,616}）・
  g07 主張 3 行〔`g07_k1097_root_claimed_coverage_3rows`・`== 3` 定数 fail-closed〕・g08 probe 再現 pilot_d6 4・andclose 2/2・
  g13 node 会計 A1 3,009,765 / B 3,009,765・g16 第三方法 miss 0/extra 0/failure null〔terminal 7,516・visited 49,094・winner 31,623・loser 9,955・応手辺 43,650〕・
  g17 三方法集計一致〔Bareiss 54 subroot〕・g19 `g19_k1097_footprint_and_fold18_residual_open`（claimed == 3 行・k1097 SHA pin `2896deb0…`・
  fold18 正本 SHA pin `18b543c4…`）・証明書全文 byte 検証（855,258 bytes・23,621 行・sorted unique・header/root 行・row 形式・
  root 幾何〔8 石・quadruple-free・D4 正準〕・合法手 54 の独立再導出・third_method 集計）。
- K1097 27 gate・win16 footprint の root 208090020004 行の intrinsic == claimed == 3 行・49 行 exactly-once partition・
  residual23 と win16 主張の不交差・主張 3 行が residual32 内。
- WIN8 被覆幾何 2 方法独立計算の一致（8 D4 像 × C(8,2) 2 石除去 224 操作 vs root の C(8,6)=28 部分集合直列挙。refsolve `coverage_of82` と同一規約・D4 同変性）。
- 再導出 target 行 == K1123 g07 主張 3 行・chain 不整合（worklist-but-not-open）0。

## 結果

- **receipt は open 4 行を閉じた**: K1123/K1097 主張 3 行（5親 target 内）
  `00000000000000801202040000001000`（cost 82・unswept・c2×1 需要行）・
  `00000000000000801202040000800000`（cost 75・unswept・c2×1 需要行）・
  `00000000000020809002000080000000`（cost 75・unswept・c2×2 需要行）に加え、
  **target 外 open 1 行** `00000000000020809002000400000000`（cost 89・unswept・c2×1 需要行）を併閉
  （いずれも同じ root の C(8,6) 部分集合幾何に内在・閉鎖 edge cost 321）。
  余剰 1 行は主張から分離記録（fail-closed 設計どおり閉鎖集合は機械判定のみで決まる）。
- 5親112行 target: 80 → **83 行**・残余 32 → **29 行**。
- frontier: 6,130/485,759 → **6,126/485,438**・solved S6 1,718 → **1,722**・parent 行 incidence 11,671 → **11,666**
  （影響 3 parent・すべて class 2〔`00000000000000003800000008001000` 9→8・`00000000000000003800000008002000` 11→9・
  `00000000000000801202080000000000` 55→53〕・完全閉鎖 0・parent-delta 計 5 == incidence 減分）。
- s6_needed_by_open_classes 4,438 → **4,434**・cost_needed_by_open_classes 352,207 → **351,886**。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 4（本 receipt で閉鎖）・not-in-worklist 22・closed-before-this-receipt 2
  （fold22 の閉鎖 6 行は 28 正準行と不交差・着手前機械確認と整合）。
- win16 候補は 4 → **3 根**（主張 9 → 6 行）。K1097 の残余23行掃引計画は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root208090020004.py   # env FOLD23_W で W ルートを上書き
```

出力 `output/win8-root208090020004-receipt-fold-20261120.json`
（25,106 bytes・SHA-256 `04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59`・
同一 cwd 2 回 + 隔離 W 複写・別 cwd・別 HOME 1 回の 3 実行で byte-identical・3 実行とも GATE FAILED 0・58 input pin 全照合）。

本実験の W は、chain 入力一式（12 blob pin + 43 SHA-256 pin 相当・fold18/19/20/21/22 出版機・fold18 preverified 写し）を
repo 出版物から再取得して再構築したものであり、まず fold21 出版機（SHA-256 `44399cc5…`）と fold22 出版機（`d5721408…`）を
pristine 実行して出版正本（`9a4da2f6…`/`f6e011f4…`）と byte-identical であることを確認してから fold23 を生成した
（W は fold22 出力の再現検証も兼ねており、fold23 機の rerun gate がこの再現性を毎実行 fail-closed で確認する）。
重要証拠が再現不能なローカル状態にのみ存在しないことの実証例にもなっている。

## 生成の注記

機械は `scripts/build_fold23.py`（全置換が出現回数 assert で機械検証・stale 定数 grep 検査・py_compile・ast 解析）で
fold22 出版機（SHA pin `d5721408…`）から生成した。生成段階で 3 件の構造的修正を行った
（(a) closedHistorical 置換アンカーの改行エスケープ誤り、(b) g02 gate 追記行の冗長閉じ括弧、
(c) fold21 chaining ブロック内の合法的 `open35` 参照に対する stale 検査の誤陽性マーカー除去）。
PIN256 は 43 → 46 件（fold22 正本・K1123 監査・K1123 証明書）。K1125 の残存参照は fold22 rerun gate の推移的再検証用 pin・
controls 行のみ（allowlist）。

## K1123 証明書の repo ファイル名表記について（訂正記録）

単一オーナー宣言ノートの初出版時に、出版証明書の repo ファイル名を「先行ゼロが 1 字多い」と誤記した。
検証の結果、repo の出版ファイル名は root 32 桁正規形と完全に同一の
`win8-root-00000000000020809002000480100000-20261120.n11` であった。宣言ノートに訂正追記した
（commits `62375b76`/`db5be5ad`・記載のみの修正・公開実体と SHA-256 は不変）。
本実験機の CERT_RELPATH・証明書 byte 検証は最初からこの公開実体（855,258 bytes・SHA-256 `b8145352…`）に対して行われている。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

fold23 の成立により出版済み WIN8 証明書の receipt fold は枯渇した。残余 29 行を閉じるためには
新規掃引（depth-10 または拡張 depth）による新証明書の出版が必要であり、着手時に単一オーナー宣言を要する。
