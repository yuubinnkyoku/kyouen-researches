# n11-residual62-win8-receipt-fold-root9090022-20261120

fold14（第21 receipt・4番目の WIN8 receipt fold）。K1109 で抽出・三重検証済みの WIN8-D10 証明書
（root `00000000000000909002200080100000`・証明書 SHA-256 `b8a15f9aac5e5f802f85459318247cb20bc983e3b2372167917ba8138cbc7a54`・
29,942 行 1,082,873 bytes・19 gate 正本 `n11-residual65-win8-cert-extract-root9090022-20261120`・
監査正本 SHA-256 `00836a6e859c780e2204b1aea427eefc044f0d4c5a6b8e8c33505a57fa950bb4`・主張 4 行の候補として初の証明書）を、
五親 S6 frontier receipt チェーン（… fold11 → fold12 → fold13）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold14-win8-root9090022-single-owner-note.md`（commit `48ad9c7d`・先行出版）。

## 目的

1. root 9090022 の S6 被覆行（K1097 win16 intrinsic footprint の主張 4 行）を frontier から閉じ、5親 target 50/112 → 54/112・残余 62 → 58 行へ進める。
2. K1109 証明書が被覆しうる open 行のうち target 外の行（worklist 上・5親112行の外）も機械判定で自動的に閉じ、余剰として記録する。
3. 被覆幾何を 2 方法（8 D4像×C(8,2) 2石除去 224 操作、root の C(8,6)=28 部分集合の直列挙）で独立計算し、両者の canonical 行集合の一致（D4 同変性）を gate する。refsolve `coverage_of82` と同一規約。
4. fold13（`fold_win8_root9840004.py`・出版済み）を本実行環境で隔離 W 複写（FOLD13_W env）の下で再実行し、出版正本（SHA-256 `c2bf8051…`）と byte-identical であることを gate してから接続する。

## 入力（fail-closed pin）

チェーン入力は fold13 と同一の 12 blob SHA-1 pin + 19 SHA-256 pin
（worklist / ledger / globalFold / previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth / fold7 / fold8 / resolve6 / fs13 / sv17 正本 / sv17 証明書 / fold10 正本 / K1096 正本 / K1096 証明書 / K1097 正本 / fold11 正本 / K1106 正本 / K1106 証明書 / fold12 正本 / K1108 正本 / K1108 証明書）。
追加入力の SHA-256 pin:

- fold13 正本 `n11-residual65-win8-receipt-fold-root9840004-20261120/output/win8-root9840004-receipt-fold-20261120.json`（`c2bf8051…`・本環境で fold13 機械を隔離 W 複写の下で再実行し byte-identical を gate で確認）
- fold13 機械 `n11-residual65-win8-receipt-fold-root9840004-20261120/scripts/fold_win8_root9840004.py`（rerun gate の実行対象）
- K1109 監査正本 `n11-residual65-win8-cert-extract-root9090022-20261120/output/win8-cert-extract-verification-20261120.json`（`00836a6e…`・19 gate 再検証・g07 主張 4 行〔`g07_k1086_root_claimed_coverage_4rows`・`== 4` 定数による fail-closed〕・g06 uncapped probes 512,590/614,246・g13 nodes 6,102,650/6,102,650・g19 footprint 照合を含む）
- K1109 証明書本体 `n11-residual65-win8-cert-extract-root9090022-20261120/certs/win8-root-00000000000000909002200080100000-20261120.n11`（`b8a15f9a…`・header/root/行数 29,942/sorted-unique/byte 数 1,082,873 全検証）

合計 34 input pins（12 blob SHA-1 + 22 SHA-256）。

## 機械

`scripts/fold_win8_root9090022.py`（fold13 機械の移行型・純 Python・乱数・時刻なし・約 11.2 秒・752 行）。主要 gate:

- チェーン段階別 frontier 再計算 6,259/495,507 → … → 6,206/491,497（fold10）→ fold11 chaining（6,201/491,110・residual 68）→ fold12 chaining（6,193/490,526・residual 65）→ fold13 レコード chaining: 被覆 9 行の open 性・記録 cost 照合・frontier_after 出版値（6,184/489,813・solved 1,664・incidence 11,775・s6_needed 4,492・cost_needed 356,261）・residual62 == residual65 − fold13 主張 3 行の差分照合・closed target 50
- fold11 機械 byte-identical rerun gate（subprocess・FOLD11_W）・fold12 機械 byte-identical rerun gate（隔離 W 複写 FOLD12_W）
- **fold13 機械 byte-identical rerun gate（subprocess・隔離 W 複写 FOLD13_W）**: fold13 機械の出力先が published record と同パスのため、W 全体の隔離複写を作って再実行し、出力 SHA-256 が出版正本と一致しなければ fail-close。
- K1109 19 gate 全再検証（g07 は 4 行版 gate 名・`== 4` 定数双方で照合）・証明書全文 byte 検証（1,082,873 bytes・29,942 行・sorted unique・合法手 50 の独立再導出）
- K1097 27 gate・win16 footprint の root 9090022 行の intrinsic == claimed == 4 行・49 行 exactly-once partition・residual23 と win16 主張の不交差・主張 4 行が residual62 内
- WIN8 被覆幾何 2 方法一致（224 操作 vs 28 部分集合）
- 再導出 target 行 == K1109 g07 主張 4 行・chain 不整合（worklist-but-not-open）0

## 結果

- **receipt は open 5 行を閉じた**（初の 4 主張行候補の fold）:
  K1109/K1097 主張 4 行 `00000000000000801222000000001000`（cost 76・c2×2）・
  `00000000000000801222000000800000`（cost 69・c2×2・transfer_partial）・
  `00000000000000909002000000100000`（cost 79・c2×2）・
  `00000000000000909002000080000000`（cost 69・c2×2・5親 target 内）に加え、
  **target 外・worklist 上の open 行 1 行** `00000000000000889002400000000000`（cost 80・c2×2・同じ root の C(8,6) 部分集合幾何に内在）を併閉。
- **root の 6 石部分幾何 28 canonical 行の分類で初めて closed-before-this-receipt 行（`00000000000000003800000008003000`・過去の receipt で閉鎖済み）が現れた**（fold13 までは open-frontier / not-in-worklist の 2 分類のみ）。閉済み行は二重閉鎖にならないよう chain gate の worklist-but-not-open 検査で自然に処理される。
- closed edge cost 373・5親112行 target: 50 → 54 行・残余 62 → 58 行。
- frontier: 6,184/489,813 → **6,179/489,440**・solved S6 1,664 → 1,669・parent 行 incidence 11,775 → 11,765
  （影響 4 parent・全 c2: 22→20・23→21・67→64・63→60・完全閉鎖 0）。
- s6_needed_by_open_classes 4,492 → 4,487・cost_needed_by_open_classes 356,261 → 355,888。
- win16 候補の残り 12 根（主張 35 行）・K1097 の残余23行掃引計画（第5ラウンド・並走宣言済み)は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root9090022.py   # env FOLD14_W で W ルートを上書き
```

出力 `output/win8-root9090022-receipt-fold-20261120.json`（SHA-256 `ed3159fdb8cf2dd8884beb845cd4ef776cbc8b4b7b442d568d895cd930a13f71`・同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写 1 回の 3 実行で byte-identical）。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
