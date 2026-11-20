# n11-residual51-win8-receipt-fold-root22081000-20261120

fold17（第24 receipt・7番目の WIN8 receipt fold）。K1117 で抽出・三重検証済みの WIN8-D10 証明書
（root `00000000000000801202000022081000`・証明書 SHA-256 `f62f6704a0d9a1366d333529dd9e742813fe87814f3857a00406d6cfc87f3c8f`・
9,460 行 341,498 bytes・19 gate 正本 `n11-residual55-win8-cert-extract-root22081000-20261120`・
監査正本 SHA-256 `3d97ac6d90e239638b019c95218f0051b432ccdcc6dd2d25e805dcbab11024d9`・
K1095 掃引由来の 39-mobility（歴代抽出根最小）・主張 3 行候補・K1097 win16 footprint intrinsic == claimed == 3 行・並走レーン出版）を、
五親 S6 frontier receipt チェーン（… fold14 → fold15 → fold16）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold17-win8-root22081000-single-owner-note.md`（commit `7f824364`・先行出版・fold16 出版後の residual-51 baseline）。

## 目的

1. root 22081000 の S6 被覆行（K1095 主張 == K1117 g07 == K1097 win16 intrinsic footprint の主張 3 行）を frontier から閉じ、5親 target 61/112 → 64/112・残余 51 → 48 行へ進める。
2. K1117 証明書が被覆しうる open 行のうち target 外の行（worklist 上・5親112行の外）も機械判定で自動的に閉じ、余剰として記録する。
3. 被覆幾何を 2 方法（8 D4像×C(8,2) 2石除去 224 操作、root の C(8,6)=28 部分集合の直列挙）で独立計算し、両者の canonical 行集合の一致（D4 同変性）を gate する。refsolve `coverage_of82` と同一規約。
4. fold16（`fold_win8_root8890020.py`・出版済み）を本実行環境で隔離 W 複写（FOLD16_W env）の下で再実行し、出版正本（SHA-256 `edd55258…`）と byte-identical であることを gate してから接続する。

## 入力（fail-closed pin）

チェーン入力は fold16 と同一の 12 blob SHA-1 pin + 28 SHA-256 pin
（worklist / ledger / globalFold / previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth / fold7 / fold8 / resolve6 / fs13 / sv17 正本 / sv17 証明書 / fold10 正本 / K1096 正本 / K1096 証明書 / K1097 正本 / fold11 正本 / K1106 正本 / K1106 証明書 / fold12 正本 / K1108 正本 / K1108 証明書 / fold13 正本 / K1109 正本 / K1109 証明書 / fold14 正本 / K1114 正本 / K1114 証明書 / fold15 正本 / K1113 正本 / K1113 証明書）。
追加入力の SHA-256 pin:

- fold16 正本 `n11-residual55-win8-receipt-fold-root8890020-20261120/output/win8-root8890020-receipt-fold-20261120.json`（`edd55258…`・本環境で fold16 機械を隔離 W 複写の下で再実行し byte-identical を gate で確認）
- fold16 機械 `n11-residual55-win8-receipt-fold-root8890020-20261120/scripts/fold_win8_root8890020.py`（rerun gate の実行対象）
- K1117 監査正本 `n11-residual55-win8-cert-extract-root22081000-20261120/output/win8-cert-extract-verification-20261120.json`（`3d97ac6d…`・19 gate 再検証・g01 K1095 正本 SHA pin 335eca5e…・g07 主張 3 行〔`g07_k1095_root_claimed_coverage_3rows`・`== 3` 定数による fail-closed〕・g05 root mobility 39・g06 uncapped probes 126,683/137,565 と terminal 石数範囲 [14,18]・g13 nodes 731,232/534,121・g16 第三方法 miss 0/extra 0/failure null・g19 footprint 照合を含む）
- K1117 証明書本体 `n11-residual55-win8-cert-extract-root22081000-20261120/certs/win8-root-00000000000000801202000022081000-20261120.n11`（`f62f6704…`・header/root/行数 9,460/sorted-unique/byte 数 341,498 全検証）

合計 43 input pins（12 blob SHA-1 + 31 SHA-256）。

## 機械

`scripts/fold_win8_root22081000.py`（fold16 機械の移行型・純 Python・乱数・時刻なし・943 行・約 95 秒）。主要 gate:

- チェーン段階別 frontier 再計算 6,259/495,507 → … → fold15 chaining（6,173/488,954・residual 55）→ fold16 レコード chaining: 被覆 5 行の open 性・記録 cost 照合・frontier_after 出版値（6,168/488,575・solved 1,680・incidence 11,743・s6_needed 4,476・cost_needed 355,023）・residual51 == residual55 − fold16 主張 4 行の差分照合・closed target 61
- fold11 機 byte-identical rerun gate（subprocess・FOLD11_W）・fold12/13/14/15 機 rerun gate（隔離 W 複写 FOLD12_W/FOLD13_W/FOLD14_W/FOLD15_W）・**fold16 機 byte-identical rerun gate（subprocess・隔離 W 複写 FOLD16_W）**: W 全体の隔離複写を作って再実行し、出力 SHA-256 が出版正本（`edd55258…`）と一致しなければ fail-close。fold16→fold15→…→fold11 の再帰 rerun もこの中で走る（7 機連鎖 rerun）。
- K1117 19 gate 全再検証（g01 K1095 master SHA pin・g07 は 3 行版 gate 名〔`g07_k1095_root_claimed_coverage_3rows`〕・`== 3` 定数・`recorded.k1095_claimed_coverage_rows` の二重照合・g05 mobility 39・g06 uncapped probes 575,570→126,683/137,565〔K1095 出版値〕と terminal 石数範囲 [14,18]・g13 nodes 731,232/534,121・g16 第三方法 miss 0/extra 0/failure null・g19 footprint claimed == CLAIM（3 行）・k1097 SHA pin）・証明書全文 byte 検証（341,498 bytes・9,460 行・sorted unique・合法手 39 の独立再導出・D4 正準・quadruple-free・third_method 集計〔terminal 3,282・visited 23,542・winner 15,228・loser 5,032・loser_reply_edges 22,031〕）
- K1097 27 gate・win16 footprint の root 22081000 行の intrinsic == claimed == 3 行・49 行 exactly-once partition・residual23 と win16 主張の不交差・主張 3 行が residual51 内
- WIN8 被覆幾何 2 方法一致（224 操作 vs 28 部分集合）
- 再導出 target 行 == K1117 g07 主張 3 行・chain 不整合（worklist-but-not-open）0

## 結果

- **receipt は open 7 行を閉じた**（単一 WIN8 receipt としては fold10 の 9 行に次ぐ規模・余剰 4 行は WIN8 receipt 史上最多）:
  K1095/K1117/K1097 主張 3 行（5親 target 内）`00000000000000003800000808001000`（cost 73・unswept・c2×2 需要行）・`00000000000000801202000000081000`（cost 66・unswept・c2×2+c4×2 需要行）・`00000000000000801202000020001000`（cost 74・unswept・c2×2 需要行）に加え、
  **target 外・worklist 上の open 行 4 行** `00000000000000801002000002081000`（cost 64・c4×1）・`00000000000000801002000002102000`（cost 64・c4×2）・`00000000000000801002000022002000`（cost 70・c4×1）・`00000000000000801202000020080000`（cost 70・c2×2+c4×2）
  （同じ root の C(8,6) 部分集合幾何に内在）を併閉。余剰 4 行は `extra_s6_rows_not_in_target` として正確に分離記録した。
- closed edge cost 481・5親112行 target: 61 → 64 行・残余 51 → 48 行。
- frontier: 6,168/488,575 → **6,161/488,094**・solved S6 1,680 → 1,687・parent 行 incidence 11,743 → 11,729
  （影響 6 parent: c2 18→15〔3行〕・c4 79→76〔3行〕・c2 49→48〔1行〕・c4 67→64〔3行〕・c2+c4 50→48〔2行〕・c2 37→35〔2行〕・完全閉鎖 0）。
- s6_needed_by_open_classes 4,476 → 4,469・cost_needed_by_open_classes 355,023 → 354,542。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 7（本 receipt で閉鎖）・not-in-worklist 21・closed-before-this-receipt 0。
- win16 候補の残り 9 根（主張 25 行）・K1097 の残余23行掃引計画は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root22081000.py   # env FOLD17_W で W ルートを上書き
```

出力 `output/win8-root22081000-receipt-fold-20261120.json`（SHA-256 `1175244d1da269b1851d5298a824b12a6ed445edc99307acc9c0fefd803bd674`・同一 cwd 2 回 + 別 W 複写・別プロセス・別 HOME 1 回の 3 実行で byte-identical・3 実行とも GATE FAILED 0）。

## 履歴の注記

fold16 の出版時（K1116）に PIN256 への fold15 正本 SHA 転写ミス（`…da0b…`→正`…da6b…`）が初回実行の `input sha256 mismatch` 即座 fail-close で捕捉された実例（raw 再取得で修正後に完走）が本 fold17 の入力 pin 設計でも有効である点は変わらず、fold17 の 43 input pin は全て初回実行で一度に検証された。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
