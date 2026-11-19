# n11-seventeenth-win7-receipt-fold-20261120

第17 WIN7-D10 証明書（root `00004000000000821082000000000100`・child `00004000000000821082000000000000` + bit 8・
証明書 SHA-256 `21dd2f0e…7c8`・seventeenth 38 gate 正本・証明書本体 commit `b7a6db5fb0`）を
第17 receipt（fold10）として五親 S6 frontier チェーンに fold した記録。
単一オーナー宣言ノート `research/log/2026-11-20-n11-fold10-single-owner-note.md`（先行出版）に基づく実行。
branch/PR は作らず main に直接出版。

## 機械と入力（全て fail-closed・SHA pin）

- `fold/fold_seventeenth.py`: fold9（thirteenth-sixteenth）正規機械
  `research/experiments/n11-residual78-windfall4-receipt-fold-20261120/scripts/fold_windfall4.py`（正本 SHA-256 `24db2352…` を生成した版）の
  チェーン再構築ロジックをそのまま引き継ぎ、thirteenth-sixteenth 正本の chaining と
  seventeenth 証明書の検証・適用に差し替えた版。
- 入力は windfall4 版と同一の 12 個の blob-SHA-1 pin + 3 個の SHA-256 pin（worklist・ledger・globalFold・
  cost78c/79c・firstFold tarball・census・audit・second/third・fourth・fifth/sixth・seventh・eighth・
  ninth-twelfth・resolve6）に加え、
  - fs13 正本 `windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json`（SHA-256 `24db2352ad0d…`）
  - seventeenth 38 gate 正本 `seventeenth-cert-triple-verification-20261120.json`（SHA-256 `c1073bae1d05…`）
  - 証明書本体 `win7-root-00004000000000821082000000000100-20261120.n11`（SHA-256 `21dd2f0e…7c8`・1,791,541 bytes）
  の3本を SHA-256 pin 入力とする。**注記: windfall4 fold 機械の出版体（K1068 側
  `n11-windfall4-receipt-fold-thirteenth-sixteenth-20261120/fold/fold_thirteenth_sixteenth.py`）の
  ledger pin は `…0c03cc…` と1文字タイポがあり repo の実在版（`…0d03cc…`）に合わない。
  正規の K1067 側機械 `fold_windfall4.py` と repo 実在版は `…0d03cc…` で一致する。本機械は正規版を採用。**

## 検証 gate（全て PASS・fail-closed）

1. 18 入力 pin（12 blob SHA-1 + 6 SHA-256）完全一致。
2. frontier チェーン再構築: base 6,259/495,507 → cost78c/79c 6,240/493,965 → first 6,236/493,703 →
   second/third 6,229/493,184 → fourth 6,226/492,970 → fifth/sixth 6,224/492,830 →
   seventh 6,223/492,762 → eighth 6,222/492,688 → ninth-twelfth 6,213/492,021（solved 1,635・incidence 11,826）。
3. thirteenth-sixteenth 正本の chaining: 4 receipt 4 行を除去し
   6,209/491,722（solved 1,639・incidence 11,818・残余74行）を正本出版値と完全一致で再現。
4. seventeenth 証明書の再検証: 38 gate 全 PASS・child=root−bit8 数値分解・D4 正準形・7石・safe・
   法定手数 60 の独立再導出・証明書ヘッダ・root 行・49,591 行・fbt_drops 0・rerun 一致・
   三重検証数値（TS/py/BigInt）・pilot_d6 制御・掃引分類 WIN 1/REFUTED 38・両順序 node-exact rerun。
5. resolve6 witness 照合: witness_full 当該 root の rows が被覆主張2行と一致。
6. **被覆行の幾何再導出**: root の 8 D4 像 × 121 石除去の正準形 join で open 集合から独立に導出。

## 結果（fold/output/seventeenth-win7-receipt-fold-20261120.json が正本・SHA-256 `bed7d331…`）

- **閉鎖 3 行**（windfall4 の4 receipt に続いて初の extra 行つき receipt）:
  - 5親 target 2行: `00000000000000821082000000000001`（cost 66）・`00000000000000821082000000000004`（cost 73）
  - target 外 extra 1行: `00004000000000003800000100000020`（cost 86）
  - target 2行は seventeenth 実験の coverage claim および resolve6 witness の rows と完全一致。
- closed edge cost 225。影響 5 parent（rows_before 76/73/69/59/…から各1〜2行減・fully-closed parent 0）。
- frontier 6,209/491,722 → **6,206/491,497**・solved S6 1,639→1,642・parent incidence 11,818→11,810。
- 5親 target 38/112 → **40/112**。**残余 74 → 72 行**。
- 39-root live witness 計画（残余78行を完全被覆）は対象2行を失い、当該 witness root は retired。
  72行に対する計画の再解決は次回の resolve7 が担当する（本 fold では簿記のみ）。
- 決定論: 2回実行で正本 byte-identical。

## 解釈規約（不変）

- WIN7-D10 はこの7石 root に限定された depth-10 内での先手必勝を証明する。
- 本 fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値（LOSS 等）を主張しない。
- REFUTED-D10 は LOSS 証明ではない。pn/dn・solved 数を勝敗として読まない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

## 次の一手

1. 残余72行への resolve7 再照合（39 witness 計画の1根 retire 後の最大マッチング再解決・stranded 分類）。
2. 十七実験の item 化（本 fold と併せて knowledge README 弾丸に反映済みなら不要）。
