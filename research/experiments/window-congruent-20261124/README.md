# window-congruent-20261124 — 遷移窓合同行パッケージ機体（K1309）

publish-then-execute: 単一オーナー宣言ノート
`research/log/2026-11-24-window-congruent-single-owner-note.md` が先に出版
されており、本キットはその §4 機体宣言の実体。定理・証明・非主張の区別はすべて
宣言ノート参照（この README は重複正本としない）。

## 主張の要約（詳細は宣言ノート §1/§4.5）

- **T-WC**: ∀ z≥3, m≥1, g≥1, k∈[1,z−1]（k ≡ z mod 2）:
  H(2m+g+k; (m,m+g); z) = D(g,z) = [g odd] (g≤z) / 2 (g=z+1) / [g even] (g≥z+2)
  （K1308 OBS-WC の全称化・値は k・m 非依存）
- **T-WBC**: ∀ z≥3, a≥1, k を窓合同として: H(2a+k; (a,a); z) = 0
- **L-BE**（導出）: m=1 窓ペアの B-exit = [g even] (g≤z−1) / 2 (g=z) /
  [z even] (g=z+1) / [g odd] (g≥z+2)・窓内 k 非依存
- **L-C**（導出）: 窓ペアの C 子値 = D(g,z−1)・例外 cell（k=1 かつ 2m+g≤z−2）のみ
  2·[g odd]。窓床の C 子値 = 0
- 到達点: ペア・床とも**全 k 軸の未確定は非合同窓行のみ**（K1303 帯域 + K1308
  上半 + 本定理の和集合が残り全部）。非合同行は D10 凍結表を obs 登録（主張なし）。

## ファイル（sha256）

| file | sha256 |
|---|---|
| verify_k1309.py | `cd1328e37acb445d67e8525877582814ee39ef61508689c9e7542657a5bd3414` |
| engine_block.py | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`（K1282..K1308 chain と同一 bytes） |
| explore_wc.py | `0c253020cf0b00eef60513c6ed642e20b5c3d48f80c9f5960e43e8626633aeb1` |
| explore_wc.out | `7e57e2e4181bc17eda1244dfe1bd203aadc8b099d51965b099f9de2f6ded43d7`（宣言前探索・凍結） |
| predry/dryrun1-4.out | 4 走とも `3b5aa0b153569026d1e3312d5e1a1a6ffb46a6046417e388fdd5f0c0049cc8dd`（byte-identical） |

埋込み engine block の起動 sha gate: pin
`bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
（verify_k1309.py 内蔵・不一致なら即時 abort）。

## 電池（宣言ノート §4・総計 40,412 点・期待 overall_bad = 0）

D1 T-WC census 10,752 / D2 T-WC far 3,456 / D3 T-WC m 距離 3,840 /
D4 T-WBC census 888 / D5 typed self-check（手手表 T-WC/T-WBC/L-BE/L-C のみで子構成・
mex == 申立 == engine 三点一致）8,736 / D6 L-BE vs 転写閉形式 vs 両 engine 1,344 /
D7 帯域・L-C engine ゲート（K1303 cpsfG 転写照合込み）3,740 / D8 公刊アンカー
（K1308 Z-DIAG/T-DU′/T-UH）2,600 / D9 cross-engine 341 / D10 非合同行 obs 凍結表
35 / D11 k=1 行 stress（例外 cell 650 含む）4,680。

## 変異電池（fail-closed・事前宣言）

- `--tamper-engine` → rc=2（変異 sha `0ea47a80…` ≠ pin）
- `--tamper=wc1` → rc=1, bad 11,424（D1 10,752 + D5 672・D5 typed 表 FLIP 由来の
  honest 値）/ `wc2` → 4,128 / `wc3` → 4,512 / `bw` → 888 / `ty` → 8,736 /
  `be` → 1,344 / `cp` → 3,740 / `ps` → 2,600 / `xg` → 341 / `rw` → 1 /
  `ex` → 4,680

## 公式監査（本キット出版後に fetch-back bytes から実行・成果物は output/ に追記出版）

1. fetch-back: 全ファイル size+sha256 byte 照合（curl raw・全ファイル）
2. 公式 4 走: 同一 cwd ×2（PYTHONHASHSEED=random/1）+ 隔離 tree/env -i ×2
   （PYTHONHASHSEED=99/7）→ 全走 rc=0・stdout byte-identical
   （predry と同一 sha `3b5aa0b1…` を確認）
3. 変異電池 12 種 → 全 fail-closed 確認
4. output/audit_run1-4.out/.info・tamper レコード・detcheck.json・MANIFEST-sha256 出版

## 規約

verdict 不消費・11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4
は全時点 UNKNOWN。engine は K1138 転写（sha pin 実装）・census は照合であって
証明の代替ではない。証明は宣言ノート §2（手証明全文）。
