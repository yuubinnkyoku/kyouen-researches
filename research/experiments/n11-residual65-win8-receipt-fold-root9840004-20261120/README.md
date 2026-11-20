# n11-residual65-win8-receipt-fold-root9840004-20261120

fold13（第20 receipt・3番目の WIN8 receipt fold）。K1108 で抽出・三重検証済みの WIN8-D10 証明書
（root `00000000000000003800000009840004`・証明書 SHA-256 `5b114b9e739b7a0a300434afb7ec5326564fc54b0d234df5e3d61abc44541143`・
45,286 行 1,640,220 bytes・19 gate 正本 `n11-residual65-win8-cert-extract-root9840004-20261120`・
監査正本 SHA-256 `2e453a76fc3168b8eb2e5c224d4a271eea0839eb5256d51fd9c02eb54bb1f648`・n11-terminal-strategy-v1 全証明書中最大行数）を、
五親 S6 frontier receipt チェーン（… seventeenth/fold10 → fold11 → fold12）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold13-win8-root9840004-single-owner-note.md`（commit `d2521aa4`・先行出版）。

## 目的

1. root 9840004 の S6 被覆行（K1097 win16 intrinsic footprint の主張 3 行）を frontier から閉じ、5親 target 47/112 → 50/112・残余 65 → 62 行へ進める。
2. K1108 証明書が被覆しうる open 行のうち target 外の行（worklist 上・5親112行の外）も機械判定で自動的に閉じ、余剰として記録する。
3. 被覆幾何を 2 方法（8 D4像×C(8,2) 2石除去 224 操作、root の C(8,6)=28 部分集合の直列挙）で独立計算し、両者の canonical 行集合の一致（D4 同変性）を gate する。refsolve `coverage_of82` と同一規約。
4. fold12（`fold_win8_root8005021.py`・出版済み）を本実行環境で隔離 W 複写（FOLD12_W env）の下で再実行し、出版正本（SHA-256 `0f73795c…`）と byte-identical であることを gate してから接続する。

## 入力（fail-closed pin）

チェーン入力は fold12 と同一の 12 blob SHA-1 pin + 13 SHA-256 pin
（worklist / ledger / globalFold / previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth / fold7 / fold8 / resolve6 / fs13 / sv17 正本 / sv17 証明書 / fold10 正本 / K1096 正本 / K1096 証明書 / K1097 正本 / fold11 正本 / K1106 正本 / K1106 証明書）。
追加入力の SHA-256 pin:

- fold12 正本 `n11-residual68-win8-receipt-fold-root8005021-20261120/output/win8-root8005021-receipt-fold-20261120.json`（`0f73795c…`・本環境で fold12 機械を隔離 W 複写の下で再実行し byte-identical を gate で確認）
- fold12 機械 `n11-residual68-win8-receipt-fold-root8005021-20261120/scripts/fold_win8_root8005021.py`（rerun gate の実行対象）
- K1108 監査正本 `n11-residual65-win8-cert-extract-root9840004-20261120/output/win8-cert-extract-verification-20261120.json`（`2e453a76…`・19 gate 再検証・g06 uncapped probes 1,143,198/1,528,656・g13 nodes 4,109,768/3,075,922・g19 footprint 照合を含む）
- K1108 証明書本体 `n11-residual65-win8-cert-extract-root9840004-20261120/certs/win8-root-00000000000000003800000009840004-20261120.n11`（`5b114b9e…`・header/root/行数 45,286/sorted-unique/byte 数 1,640,220 全検証）

合計 31 input pins（12 blob SHA-1 + 19 SHA-256）。

## 機械

`scripts/fold_win8_root9840004.py`（fold12 機械の移行型・純 Python・乱数・時刻なし・約 5.6 秒・701 行）。主要 gate:

- チェーン段階別 frontier 再計算 6,259/495,507 → … → 6,206/491,497（fold10）→ fold11 レコード chaining（6,201/491,110・incidence 11,803・residual 68）→ fold12 レコード chaining: 被覆 8 行の open 性・記録 cost 照合・frontier_after 出版値（6,193/490,526・solved 1,655・incidence 11,790・s6_needed 4,501・cost_needed 356,974）・residual65 == residual68 − fold12 主張 3 行の差分照合・closed target 47
- fold11 機械 byte-identical rerun gate（subprocess・FOLD11_W）
- **fold12 機械 byte-identical rerun gate（subprocess・隔離 W 複写 FOLD12_W）**: fold12 機械の出力先が published record と同パスのため、W 全体の隔離複写を作って再実行し、出力 SHA-256 が出版正本と一致しなければ fail-close。fold11 の `fold/output/` 分離慣行と異なる新しい rerun gate 形式。
- K1108 19 gate 全再検証・証明書全文 byte 検証（1,640,220 bytes・45,286 行・sorted unique・合法手 57 の独立再導出）
- K1097 27 gate・win16 footprint の root 9840004 行の intrinsic == claimed == 3 行・49 行 exactly-once partition・residual23 と win16 主張の不交差・主張 3 行が residual65 内
- WIN8 被覆幾何 2 方法一致（224 操作 vs 28 部分集合）
- 再導出 target 行 == K1108 g07 主張 3 行・chain 不整合（worklist-but-not-open）0

## 結果

- **receipt は open 9 行を閉じた**（単一 WIN8 receipt として最多を更新。fold12 の 8 行を上回る）:
  K1108/K1097 主張 3 行 `00000000000000003800000009000004`（cost 82・c2×2）・
  `00000000000000003800000009040000`（cost 76・c2）・
  `00000000000000003800000009800000`（cost 69・c2+c4・5親 target 内）に加え、
  **target 外・worklist 上の open 行 6 行** `00000000000000003800000000840004`（cost 92・c4×2）・
  `00000000000000003800000001800004`（cost 77・c4×2）・
  `00000000000000003800000001840000`（cost 78・c4×2）・
  `00000000000000003800000008004100`（cost 82・c2）・
  `00000000000000003800000008800004`（cost 79・c2+c4）・
  `00000000000000003800000008840000`（cost 78・c4）
  （いずれも同じ root の C(8,6)=28 部分集合幾何に内在）を併閉。**余剰行が主張行を数で上回ったのは fold12 に続いて2例目・余剰 6 行は単一 receipt として最多**。
- closed edge cost 713・5親112行 target: 47 → 50 行・残余 65 → 62 行。
- frontier: 6,193/490,526 → **6,184/489,813**・solved S6 1,655 → 1,664・parent 行 incidence 11,790 → 11,775
  （影響 5 parent: c4 3 parent〔87→84・90→87・75→72〕・c2 2 parent〔61→58・16→13〕・完全閉鎖 0）。
- s6_needed_by_open_classes 4,501 → 4,492・cost_needed_by_open_classes 356,974 → 356,261。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier（本 receipt で閉鎖）9・not-in-worklist 19。
- win16 候補の残り 13 根（主張 39 行）・K1097 の残余23行掃引計画（第5ラウンド・並走宣言済み）は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root9840004.py   # env FOLD13_W で W ルートを上書き
```

出力 `output/win8-root9840004-receipt-fold-20261120.json`（SHA-256 `c2bf80511e816306bbb8dcf4efb450214234f020c513386c3b3a82045f71e9ae`・同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写 1 回の 3 実行で byte-identical）。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
