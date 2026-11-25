# n11-residual68-win8-receipt-fold-root8005021-20261120

fold12（第19 receipt・2番目の WIN8 receipt fold）。K1106 で抽出・三重検証済みの WIN8-D10 証明書
（root `00000000000000003800000008005021`・証明書 SHA-256 `69f32661d80ae0887ecf385cb690e0d4300c5ad28686ec42fc83e93da79ac6f5`・
26,083 行 945,298 bytes・19 gate 正本 `n11-residual72-win8-cert-extract-root8005021-20261120`・監査正本 SHA-256 `0bd2dd10c1d5b735a04f31425003c635d80266e4c03a6bef0fdff212d499408f`）を、
五親 S6 frontier receipt チェーン（… seventeenth/fold10 → fold11）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold12-win8-root8005021-single-owner-note.md`（commit `7bb492cd`・先行出版）。

## 目的

1. root 8005021 の S6 被覆行（K1097 win16 intrinsic footprint の主張 3 行）を frontier から閉じ、5親 target 44/112 → 47/112・残余 68 → 65 行へ進める。
2. K1106 証明書が被覆しうる open 行のうち target 外の行（worklist 上・5親112行の外）も機械判定で自動的に閉じ、余剰として記録する。
3. 被覆幾何を 2 方法（8 D4像×C(8,2) 2石除去 224 操作、root の C(8,6)=28 部分集合の直列挙）で独立計算し、両者の canonical 行集合の一致（D4 同変性）を gate する。refsolve `coverage_of82` と同一規約。
4. fold11（`fold_win8_root8003180.py`・出版済み）を本実行環境で再実行し、出版正本（SHA-256 `d7bf2cd5…`）と byte-identical であることを gate してから接続する。

## 入力（fail-closed pin）

チェーン入力は fold11 と同一の 12 blob SHA-1 pin + 10 SHA-256 pin
（worklist / ledger / globalFold / previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth / fold7 / fold8 / resolve6 / fs13 / sv17 正本 / sv17 証明書 / fold10 正本 / K1096 正本 / K1096 証明書 / K1097 正本）。
追加入力の SHA-256 pin:

- fold11 正本 `n11-residual72-win8-receipt-fold-root8003180-20261120/output/win8-root8003180-receipt-fold-20261120.json`（`d7bf2cd5…`・本環境で fold11 機械を再実行し byte-identical を gate で確認）
- fold11 機械 `n11-residual72-win8-receipt-fold-root8003180-20261120/scripts/fold_win8_root8003180.py`（rerun gate の実行対象）
- K1106 audit 正本 `n11-residual72-win8-cert-extract-root8005021-20261120/output/win8-cert-extract-verification-20261120.json`（`0bd2dd10…`・19 gate 再検証・g06 uncapped probes 619,138/751,581・g13 nodes 3,272,039/2,876,091・g19 footprint 照合を含む）
- K1106 証明書本体 `n11-residual72-win8-cert-extract-root8005021-20261120/certs/win8-root-00000000000000003800000008005021-20261120.n11`（`69f32661…`・header/root/行数 26,083/sorted-unique/byte 数 945,298 全検証）

合計 25 input pins（12 blob SHA-1 + 13 SHA-256）。

## 機械

`scripts/fold_win8_root8005021.py`（fold11 機械の移行型・純 Python・乱数・時刻なし・約 2.8 秒）。主要 gate:

- チェーン段階別 frontier 再計算 6,259/495,507 → … → 6,206/491,497（fold10・全段値 gate）→ fold11 レコード chaining: 被覆 5 行の open 性・記録 cost 照合・frontier_after 出版値（6,201/491,110・solved 1,647・incidence 11,803・s6_needed 4,504）・residual68 == residual72 − fold11 主張 4 行の差分照合・closed target 44
- fold11 機械 byte-identical rerun gate（subprocess・FOLD11_W・出力 SHA-256 == 出版正本）
- K1106 19 gate 全再検証・証明書全文 byte 検証・root 幾何（8石・quadruples 0・D4 正準・合法手 41 の独立再導出）
- K1097 27 gate・win16 footprint の root 8005021 行の intrinsic == claimed == 3 行・49 行 exactly-once partition・residual23 と win16 主張の不交差
- WIN8 被覆幾何 2 方法一致（224 操作 vs 28 部分集合）
- 再導出 target 行 == K1106 g07 主張 3 行・chain 不整合（worklist-but-not-open）0

## 結果

- **receipt は open 8 行を閉じた**（単一 WIN8 receipt としては最多。fold11 の 5 行を上回る）:
  K1106/K1097 主張 3 行 `00000000000000003800000008001001`（cost 74・c2）・`00000000000000003800000008001020`（cost 65・c1+c2）・
  `00000000000000003800000008005000`（cost 71・c2・5親 target 内）に加え、
  **target 外・worklist 上の open 行 5 行** `00000000000000003800000000004021`（cost 79・c1×2）・
  `00000000000000003800000000005020`（cost 80・c1×2）・`00000000000000003800000008000021`（cost 69・c1）・
  `00000000000000003800000008004001`（cost 77・c2）・`00000000000000003800000008004020`（cost 69・c1）
  （いずれも同じ root の C(8,6)=28 部分集合幾何に内在）を併閉。**余剰行が主張行を数で上回った初の receipt**。
- closed edge cost 584・5親112行 target: 44 → 47 行・残余 68 → 65 行。
- frontier: 6,201/491,110 → **6,193/490,526**・solved S6 1,647 → 1,655・parent 行 incidence 11,803 → 11,790
  （影響 5 parent: c1 3 parent〔58→56・65→63・75→72〕・c2 2 parent〔44→41・25→22〕・完全閉鎖 0）。
- s6_needed_by_open_classes 4,504 → 4,501・cost_needed_by_open_classes 357,196 → 356,974。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier（本 receipt で閉鎖）8・not-in-worklist 20。
- win16 候補の残り 14 根（主張 42 行）・K1097 の残余23行掃引計画（第5ラウンド・並走宣言済み）は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root8005021.py   # env FOLD12_W で W ルートを上書き
```

出力 `output/win8-root8005021-receipt-fold-20261120.json`（SHA-256 `0f73795ce71aec83ba4a9f1b97a530891f3e6d1c807bfa47c9fbb88a1b33f5bd`）は
同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写 1 回の 3 実行で byte-identical。

## 解釈上の制限（不変）

- WIN8-D10 はこの 8 石 root のゲーム木のみを証明する。
- receipt fold は行の閉鎖簿記であり、閉じた行や 5親 target のゲーム理論的値を主張しない。REFUTED-D10 は LOSS 証明ではない。
- pn/dn・nodes 数・solved 数を勝敗として読まない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
