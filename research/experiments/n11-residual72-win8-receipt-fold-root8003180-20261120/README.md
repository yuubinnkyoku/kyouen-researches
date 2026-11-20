# n11-residual72-win8-receipt-fold-root8003180-20261120

fold11（第18 receipt・初の WIN8 receipt fold）。K1096 で抽出・三重検証済みの WIN8-D10 証明書
（root `00000000000000003800000008003180`・証明書 SHA-256 `1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c`・
18 gate 正本 `n11-residual72-win8-cert-extract-root8003180-20261120`）を、
五親 S6 frontier receipt チェーン（base → cost78c/79c → first → second/third → fourth → fifth/sixth → seventh → eighth → ninth-twelfth → thirteenth-sixteenth → seventeenth）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold11-win8-root8003180-single-owner-note.md`（commit `d36e15b6`・先行出版）。

## 目的

1. root 8003180 の S6 被覆行（K1097 win16 intrinsic footprint の主張 4 行）を frontier から閉じ、5親 target 40/112 → 44/112・残余 72 → 68 行へ進める。
2. K1096 証明書が被覆しうる open 行のうち target 外の行（worklist 上・5親112行の外）も機械判定で自動的に閉じ、余剰として記録する。
3. 被覆幾何を 2 方法（8 D4像×C(8,2) 2石除去 224 操作、root の C(8,6)=28 部分集合の直列挙）で独立計算し、両者の canonical 行集合の一致（D4 同変性）を gate する。refsolve `coverage_of82` と同一規約。
4. fold10（seventeenth）正本の出版機械を本実行環境でbyte-identical再実行し、チェーンの上流を検証してから接続する。

## 入力（fail-closed pin）

チェーン入力は fold10 と同一の 12 blob SHA-1 pin + 6 SHA-256 pin
（worklist / ledger / globalFold / previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth / fold7 / fold8 / resolve6 / fs13 / sv17 正本 / sv17 証明書）。
追加入力の 4 点は SHA-256 pin:

- fold10 正本 `n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json`（`bed7d331…`・本環境で再実行 byte-identical を事前確認）
- K1096 audit 正本 `n11-residual72-win8-cert-extract-root8003180-20261120/output/win8-cert-extract-verification-20261120.json`（`ad0d9fb3…`・18 gate 再検証）
- K1096 証明書本体 `n11-residual72-win8-cert-extract-root8003180-20261120/certs/win8-root-00000000000000003800000008003180-20261120.n11`（`13931289…`・header/root/行数 34,529/sorted-unique/byte 数 1,251,923 全検証）
- K1097 refsolve 正本 `n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json`（`2896deb0…`・27 gate 再検証）

## 機械

`scripts/fold_win8_root8003180.py`（純 Python・乱数・時刻なし・1.4 秒）。主要 gate:

- チェーン段階別 frontier 再計算 6,259/495,507 → … → 6,222/492,688（fold8 直後まで全段値 gate）
- fold9（ninth-twelfth）・fs13（thirteenth-sixteenth）・fold10（seventeenth）のレコード被覆行の open 性・parent incidence（11,826 → 11,818 → 11,810）・residual 74 → 72 の差分照合
- K1096 18 gate・証明書全文 byte 検証・root 幾何（8石・quadruples 0・D4 正準・合法手 53 独立再導出）
- K1097 27 gate・win16 footprint の root 8003180 行の intrinsic == claimed == 4 行・49 行 exactly-once partition・residual23 と win16 主張の不交差（本 receipt が残余23行掃引計画に触れないことの機械確認）
- WIN8 被覆幾何 2 方法一致（224 操作 vs 28 部分集合）
- 再導出 target 行 == K1096 g07 主張 4 行

## 結果

- **receipt は open 5 行を閉じた**: K1097 主張 4 行（`00000000000000003800000008001080`・`…8001100`・`…8002080`・`…8002100`・全て c2 需要行）に加え、
  target 外・worklist 上の open 行 `0000000000000000380000000800000c`（cost 83・c2・同 receipt の C(8,6) 部分集合として同じ root に内在）を併閉。
  closed edge cost 387。
- 5親112行 target: 40 → 44 行（残余 72 → 68）。
- frontier: 6,206/491,497 → **6,201/491,110**・solved S6 1,642 → 1,647・parent 行 incidence 11,810 → 11,803（影響 3 parent・完全閉鎖 0）。
- s6_needed_by_open_classes 4,509 → 4,504・cost_needed 357,583 → 357,196。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier（本 receipt で閉鎖）5・closed-before-this-receipt 1・not-in-worklist 22（`…8003000` は fold9 より前の receipt で閉鎖済み）。

## 再現

```
python3 scripts/fold_win8_root8003180.py   # env FOLD11_W で W ルートを上書き
```

出力 `output/win8-root8003180-receipt-fold-20261120.json`（SHA-256 `d7bf2cd53d99d836418678abd172f4d5890d70bf8a90633b1e434b784bf7e50e`）は
同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写 1 回の 3 実行で byte-identical。

## 解釈上の制限（不変）

- WIN8-D10 はこの 8 石 root のゲーム木のみを証明する。
- receipt fold は行の閉鎖簿記であり、閉じた行や 5親 target のゲーム理論的値を主張しない。REFUTED-D10 は LOSS 証明ではない。
- pn/dn・nodes・solved 数を勝敗として読まない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
