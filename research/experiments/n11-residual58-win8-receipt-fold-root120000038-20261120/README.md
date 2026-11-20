# n11-residual58-win8-receipt-fold-root120000038-20261120

fold15（第22 receipt・5番目の WIN8 receipt fold）。K1114 で抽出・三重検証済みの WIN8-D10 証明書
（root `00000000012000003800080009000000`・証明書 SHA-256 `5a1359033325e918cf5d9cd2d60ff63fc2fd45e30b926e79330560a7a3a23c4c`・
32,470 行 1,171,958 bytes・19 gate 正本 `n11-residual58-win8-cert-extract-root120000038-20261120`・
監査正本 SHA-256 `ab8cd535c14637c150c02ceeb688b335eb2da9dc1c5778b6a7c05a1a0906f67e`・
K1086 addtwo-greedy23 掃引由来の 53-mobility・主張 3 行候補）を、
五親 S6 frontier receipt チェーン（… fold12 → fold13 → fold14）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold15-win8-root120000038-single-owner-note.md`（commit `3f149dc3`・先行出版）。

## 目的

1. root 120000038 の S6 被覆行（K1086 greedy 主張 == K1097 win16 intrinsic footprint の主張 3 行）を frontier から閉じ、5親 target 54/112 → 57/112・残余 58 → 55 行へ進める。
2. K1114 証明書が被覆しうる open 行のうち target 外の行（worklist 上・5親112行の外）も機械判定で自動的に閉じ、余剰として記録する。
3. 被覆幾何を 2 方法（8 D4像×C(8,2) 2石除去 224 操作、root の C(8,6)=28 部分集合の直列挙）で独立計算し、両者の canonical 行集合の一致（D4 同変性）を gate する。refsolve `coverage_of82` と同一規約。
4. fold14（`fold_win8_root9090022.py`・出版済み）を本実行環境で隔離 W 複写（FOLD14_W env）の下で再実行し、出版正本（SHA-256 `ed3159fd…`）と byte-identical であることを gate してから接続する。

## 入力（fail-closed pin）

チェーン入力は fold14 と同一の 12 blob SHA-1 pin + 22 SHA-256 pin
（worklist / ledger / globalFold / previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth / fold7 / fold8 / resolve6 / fs13 / sv17 正本 / sv17 証明書 / fold10 正本 / K1096 正本 / K1096 証明書 / K1097 正本 / fold11 正本 / K1106 正本 / K1106 証明書 / fold12 正本 / K1108 正本 / K1108 証明書 / fold13 正本 / K1109 正本 / K1109 証明書）。
追加入力の SHA-256 pin:

- fold14 正本 `n11-residual62-win8-receipt-fold-root9090022-20261120/output/win8-root9090022-receipt-fold-20261120.json`（`ed3159fd…`・本環境で fold14 機械を隔離 W 複写の下で再実行し byte-identical を gate で確認）
- fold14 機械 `n11-residual62-win8-receipt-fold-root9090022-20261120/scripts/fold_win8_root9090022.py`（rerun gate の実行対象）
- K1114 監査正本 `n11-residual58-win8-cert-extract-root120000038-20261120/output/win8-cert-extract-verification-20261120.json`（`ab8cd535…`・19 gate 再検証・g01 K1086 正本 SHA pin 3045e152…・g07 主張 3 行〔`g07_k1086_root_claimed_coverage_3rows`・`== 3` 定数による fail-closed〕・g05 root mobility 53・g06 uncapped probes 825,127/657,152 と terminal 石数範囲 [14,18]・g13 nodes 2,723,200/2,141,807・g16 第三方法 miss 0/extra 0/failure null・g19 footprint 照合を含む）
- K1114 証明書本体 `n11-residual58-win8-cert-extract-root120000038-20261120/certs/win8-root-00000000012000003800080009000000-20261120.n11`（`5a135903…`・header/root/行数 32,470/sorted-unique/byte 数 1,171,958 全検証）

合計 37 input pins（12 blob SHA-1 + 25 SHA-256）。

## 機械

`scripts/fold_win8_root120000038.py`（fold14 機械の移行型・純 Python・乱数・時刻なし・825 行・約 23 秒）。主要 gate:

- チェーン段階別 frontier 再計算 6,259/495,507 → … → fold10 6,206/491,497 → fold11 chaining（6,201/491,110・residual 68）→ fold12 chaining（6,193/490,526・residual 65）→ fold13 chaining（6,184/489,813・residual 62）→ fold14 レコード chaining: 被覆 5 行の open 性・記録 cost 照合・frontier_after 出版値（6,179/489,440・solved 1,669・incidence 11,765・s6_needed 4,487・cost_needed 355,888）・residual58 == residual62 − fold14 主張 4 行の差分照合・closed target 54
- fold11 機械 byte-identical rerun gate（subprocess・FOLD11_W）・fold12 機械 byte-identical rerun gate（隔離 W 複写 FOLD12_W）・fold13 機械 byte-identical rerun gate（隔離 W 複写 FOLD13_W）
- **fold14 機械 byte-identical rerun gate（subprocess・隔離 W 複写 FOLD14_W）**: fold14 機の出力先が published record と同パスのため、W 全体の隔離複写を作って再実行し、出力 SHA-256 が出版正本（`ed3159fd…`）と一致しなければ fail-close。fold13→fold12→fold11 の再帰 rerun もこの中で走る（5 機連鎖 rerun）。
- K1114 19 gate 全再検証（g01 K1086 master SHA pin・g07 は 3 行版 gate 名 `g07_k1086_root_claimed_coverage_3rows`・`== 3` 定数・`recorded.k1086_claimed_coverage_rows` の二重照合・g05 mobility 53・g06 uncapped probes 825,127/657,152 に加え今 fold から terminal 石数範囲 [14,18] も固定・g13 nodes 2,723,200/2,141,807・g16 第三方法 miss 0/extra 0/failure null を新規固定・g19 footprint claimed == CLAIM（3 行）・k1097 SHA pin）・証明書全文 byte 検証（1,171,958 bytes・32,470 行・sorted unique・合法手 53 の独立再導出・D4 正準・quadruple-free）
- K1097 27 gate・win16 footprint の root 120000038 行の intrinsic == claimed == 3 行・49 行 exactly-once partition・residual23 と win16 主張の不交差・主張 3 行が residual58 内
- WIN8 被覆幾何 2 方法一致（224 操作 vs 28 部分集合）
- 再導出 target 行 == K1114 g07 主張 3 行・chain 不整合（worklist-but-not-open）0

## 結果

- **receipt は open 6 行を閉じた**（初の 53-mobility 候補の fold）:
  K1114/K1086/K1097 主張 3 行（5親 target 内）`00000000000000003800000248000000`（cost 85）・`00000000000000801202000001000100`（cost 76）・`00000000000080003800000048000000`（cost 77）に加え、
  **target 外・worklist 上の open 行 3 行** `00000000000000801202000020000008`（cost 80）・`00000000010000003800080008000000`（cost 87）・`00000000012000003800000008000000`（cost 81）（いずれも同じ root の C(8,6) 部分集合幾何に内在・unswept・c2×2 需要行）を併閉。
- 宣言ノートの事前計算（C(8,6) 28 canonical join と残余 58 行〔5親 target〕の交差）は主張 3 行ちょうどを返し target 予測は正確だったが、閉鎖予測「主張 3 行のみ」は target 外 open 行 3 行を見落としていた。機械の 2 方法被覆幾何再導行が target を問わず open frontier 全体との交差で 6 行を閉じ、余剰 3 行を `extra_s6_rows_not_in_target` として正確に記録した（fail-closed 設計どおり target は機械判定のみで決まる）。
- closed edge cost 486・5親112行 target: 54 → 57 行・残余 58 → 55 行。
- frontier: 6,179/489,440 → **6,173/488,954**・solved S6 1,669 → 1,675・parent 行 incidence 11,765 → 11,753
  （影響 4 parent・全 c2: 13→10・62→59・54→51・40→37・完全閉鎖 0）。
- s6_needed_by_open_classes 4,487 → 4,481・cost_needed_by_open_classes 355,888 → 355,402。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 6（本 receipt で閉鎖）・not-in-worklist 22（closed-before-this-receipt 0・fold14 で現れた初例型の閉済み行は本 root にはなし）。
- win16 候補の残り 11 根（主張 32 行）・K1097 の残余23行掃引計画は不変（residual23 と全 win16 主張の不交差を機械再確認）。残り候補には K1113 root `…889002`（並走出版済み・fold16 候補・着手時に別途宣言必要）と K1086 第 7 候補 `…8180000`（並走が抽出宣言済み）を含む。

## 再現

```
python3 scripts/fold_win8_root120000038.py   # env FOLD15_W で W ルートを上書き
```

出力 `output/win8-root120000038-receipt-fold-20261120.json`（SHA-256 `bae2b3c182da6b0b06be530604f43d1bfa3bf008190860dad6d27f2b9c285aef`・同一 cwd 2 回 + 別 cwd・別プロセス・別 HOME 1 回の 3 実行で byte-identical・3 実行とも GATE FAILED 0）。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
