# n11-residual55-win8-receipt-fold-root8890020-20261120

fold16（第23 receipt・6番目の WIN8 receipt fold）。K1113 で抽出・三重検証済みの WIN8-D10 証明書
（root `00000000010000889002000080100000`・証明書 SHA-256 `105e1e2ad59f4f6baa85f37dde7306b98fc96d2164edf5b5d12205b1c71e2bc4`・
21,446 行 775,317 bytes・19 gate 正本 `n11-residual58-win8-cert-extract-root8890020-20261120`・
監査正本 SHA-256 `b8c264e671b9e26fa9caf8cd2454f75b13c992d548e2d5ed0b02f2bec75c5236`・
K1086 掃引由来の 50-mobility・主張 4 行候補・K1097 win16 footprint intrinsic == claimed == 4 行）を、
五親 S6 frontier receipt チェーン（… fold13 → fold14 → fold15）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold16-win8-root8890020-single-owner-note.md`（commit `d6a65fff`・先行出版・fold15 出版後の residual-55 baseline に更新済み）。

## 目的

1. root 8890020 の S6 被覆行（K1086 主張 == K1113 g07 == K1097 win16 intrinsic footprint の主張 4 行）を frontier から閉じ、5親 target 57/112 → 61/112・残余 55 → 51 行へ進める。
2. K1113 証明書が被覆しうる open 行のうち target 外の行（worklist 上・5親112行の外）も機械判定で自動的に閉じ、余剰として記録する。
3. 被覆幾何を 2 方法（8 D4像×C(8,2) 2石除去 224 操作、root の C(8,6)=28 部分集合の直列挙）で独立計算し、両者の canonical 行集合の一致（D4 同変性）を gate する。refsolve `coverage_of82` と同一規約。
4. fold15（`fold_win8_root120000038.py`・出版済み）を本実行環境で隔離 W 複写（FOLD15_W env）の下で再実行し、出版正本（SHA-256 `bae2b3c1…`）と byte-identical であることを gate してから接続する。

## 入力（fail-closed pin）

チェーン入力は fold15 と同一の 12 blob SHA-1 pin + 25 SHA-256 pin
（worklist / ledger / globalFold / previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth / fold7 / fold8 / resolve6 / fs13 / sv17 正本 / sv17 証明書 / fold10 正本 / K1096 正本 / K1096 証明書 / K1097 正本 / fold11 正本 / K1106 正本 / K1106 証明書 / fold12 正本 / K1108 正本 / K1108 証明書 / fold13 正本 / K1109 正本 / K1109 証明書 / fold14 正本 / K1114 正本 / K1114 証明書）。
追加入力の SHA-256 pin:

- fold15 正本 `n11-residual58-win8-receipt-fold-root120000038-20261120/output/win8-root120000038-receipt-fold-20261120.json`（`bae2b3c1…`・本環境で fold15 機械を隔離 W 複写の下で再実行し byte-identical を gate で確認）
- fold15 機械 `n11-residual58-win8-receipt-fold-root120000038-20261120/scripts/fold_win8_root120000038.py`（rerun gate の実行対象）
- K1113 監査正本 `n11-residual58-win8-cert-extract-root8890020-20261120/output/win8-cert-extract-verification-20261120.json`（`b8c264e6…`・19 gate 再検証・g01 K1086 正本 SHA pin 3045e152…・g07 主張 4 行〔`g07_k1086_root_claimed_coverage_4rows`・`== 4` 定数による fail-closed〕・g05 root mobility 50・g06 uncapped probes 575,570/409,407 と terminal 石数範囲 [14,18]・g13 nodes 4,424,758/4,424,758・g16 第三方法 miss 0/extra 0/failure null・g19 footprint 照合を含む）
- K1113 証明書本体 `n11-residual58-win8-cert-extract-root8890020-20261120/certs/win8-root-00000000010000889002000080100000-20261120.n11`（`105e1e2a…`・header/root/行数 21,446/sorted-unique/byte 数 775,317 全検証）

合計 40 input pins（12 blob SHA-1 + 28 SHA-256）。

## 機械

`scripts/fold_win8_root8890020.py`（fold15 機械の移行型・純 Python・乱数・時刻なし・883 行・約 47 秒）。主要 gate:

- チェーン段階別 frontier 再計算 6,259/495,507 → … → fold14 chaining（6,179/489,440・residual 58）→ fold15 レコード chaining: 被覆 6 行の open 性・記録 cost 照合・frontier_after 出版値（6,173/488,954・solved 1,675・incidence 11,753・s6_needed 4,481・cost_needed 355,402）・residual55 == residual58 − fold15 主張 3 行の差分照合・closed target 57
- fold11 機 byte-identical rerun gate（subprocess・FOLD11_W）・fold12/13/14 機 rerun gate（隔離 W 複写 FOLD12_W/FOLD13_W/FOLD14_W）・**fold15 機 byte-identical rerun gate（subprocess・隔離 W 複写 FOLD15_W）**: W 全体の隔離複写を作って再実行し、出力 SHA-256 が出版正本（`bae2b3c1…`）と一致しなければ fail-close。fold14→fold13→…→fold11 の再帰 rerun もこの中で走る（6 機連鎖 rerun）。
- K1113 19 gate 全再検証（g01 K1086 master SHA pin・g07 は 4 行版 gate 名に差し戻し・`== 4` 定数・`recorded.k1086_claimed_coverage_rows` の二重照合・g05 mobility 50・g06 uncapped probes 575,570/409,407 と terminal 石数範囲 [14,18]・g13 nodes 4,424,758/4,424,758・g16 第三方法 miss 0/extra 0/failure null・g19 footprint claimed == CLAIM（4 行）・k1097 SHA pin）・証明書全文 byte 検証（775,317 bytes・21,446 行・sorted unique・合法手 50 の独立再導出・D4 正準・quadruple-free・third_method 集計〔terminal 7,653・visited 48,855・winner 31,320・loser 9,882・loser_reply_edges 43,837〕）
- K1097 27 gate・win16 footprint の root 8890020 行の intrinsic == claimed == 4 行・49 行 exactly-once partition・residual23 と win16 主張の不交差・主張 4 行が residual55 内
- WIN8 被覆幾何 2 方法一致（224 操作 vs 28 部分集合）
- 再導出 target 行 == K1113 g07 主張 4 行・chain 不整合（worklist-but-not-open）0

## 結果

- **receipt は open 5 行を閉じた**:
  K1113/K1086/K1097 主張 4 行（5親 target 内）`00000000000000889002000000100000`（cost 74）・`00000000000000889002000080000000`（cost 67）・`00000000010000809002000000100000`（cost 81）・`00000000010000809002000080000000`（cost 75）に加え、
  **target 外・worklist 上の open 行 1 行** `00000000000000801222000100000000`（cost 82・unswept・c2×2 需要行・同じ root の C(8,6) 部分集合幾何に内在）を併閉。余剰 1 行は `extra_s6_rows_not_in_target` として正確に分離記録した。
- closed edge cost 379・5親112行 target: 57 → 61 行・残余 55 → 51 行。
- frontier: 6,173/488,954 → **6,168/488,575**・solved S6 1,675 → 1,680・parent 行 incidence 11,753 → 11,743
  （影響 4 parent・全 c2: 20→18・21→19・42→39・60→57・完全閉鎖 0）。
- s6_needed_by_open_classes 4,481 → 4,476・cost_needed_by_open_classes 355,402 → 355,023。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 5（本 receipt で閉鎖）・not-in-worklist 22・closed-before-this-receipt 1（`00000000000000003800000008003000`）。
- win16 候補の残り 10 根（主張 28 行）・K1097 の残余23行掃引計画は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root8890020.py   # env FOLD16_W で W ルートを上書き
```

出力 `output/win8-root8890020-receipt-fold-20261120.json`（SHA-256 `edd552588e265ada1cf015b4359584288cca3f18686c0fc8ca1536b6458b969b`・同一 cwd 2 回 + 別 W 複写・別プロセス・別 HOME 1 回の 3 実行で byte-identical・3 実行とも GATE FAILED 0）。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
