# pair-upper-20261124 — 上半畳み込みパッケージ機体（K1308）

publish-then-execute: 単一オーナー宣言ノート
`research/log/2026-11-24-pair-upper-collapse-single-owner-note.md` が先に出版
されており、本キットはその §4 機体宣言の実体。定理・証明・非主張の区別はすべて
宣言ノート参照（この README は重複正本としない）。

## 主張の要約（詳細は宣言ノート §1/§6）

- **T-UH**: ∀ z≥0, m≥1, g≥1, k≥z+1: H(2m+g+k; (m,m+g); z) = [g odd]
- **T-DU′**: ∀ z≥0, a≥1, k≥z: H(2a+k; (a,a); z) = 0（k≥z は正確な閾値）
- **Z-DIAG**: ∀ z≥0, m≥1, g≥1, k=z: [g odd] (g≤z) / 2 (g=z+1) / [g even] (g≥z+2)
- **L-SB**: v(x,p,x+j) = x%2 (x≥2, p≥1, j≥p) + B-exit 境界読み
- C-SUM は **census 予想**（全称主張しない）・窓偶奇交互予想は **REFUTED**
  （29 反例）・OBS-WC/OBS-BW は観測登録（未証明）。

## ファイル（sha256）

| file | sha256 |
|---|---|
| verify_k1308.py | `973c97a52a03137fbb7be4af6965593f2bb1c6c384d75ce18f3d34f3fde5c3ac` |
| engine_block.py | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`（K1282..K1305 chain と同一 bytes） |
| explore_upper.py | `f8b6b3e30a1ba94508622634216ea2f13a6bc20f4e8075c2cea9c3c093db88b5` |
| explore_upper.out | `84df9a1b92e1a4553a2369010193909d7ba7283899f0a1aa90c4679ef5fa1de9`（宣言前探索・凍結） |
| output/dryrun1-4.out | 4 走とも `d3e244f42f290db0cb0a28d15cd9dec482386e808fcc673db6e4995e16c88d25`（byte-identical） |

埋込み engine block の起動 sha gate: pin
`bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
（verify_k1308.py 内蔵・不一致なら即時 abort）。

## 電池（宣言ノート §4・総計 20,588 点・期待 overall_bad = 0）

D1 T-UH census 5,760 / D2 T-DU′ census 972 / D3 Z-DIAG census 1,260 /
D4 typed self-check（主張表+K0832 閉形式のみで子構成・tail 均一化
set(children)=={1−claim}・床 0∉children 点検証）1,512 / D5 L-SB+境界読み
（閉形式・両 engine 三方照合）2,623 / D6 公刊アンカー（K1285 T-PS0/1/2・T-ALM
六床・K1286 Z1(1,·)/z2k1/Z2(2,·)・T-B1/T-B2/T-B0・b1(0)=1 シャープネス照合）
1,941 / D7 面 0/1/2 上半完全閉包 census 1,440 / D8 C-SUM census（予想・obs 明記）
2,364 / D9 REFUTED recheck（z=3 clean・z≥4 counters 再生産・全 29 反例を obs
凍結）6 / D10 cross-engine 1,116 / D11 stress 1,594。

## 変異電池（fail-closed・事前宣言）

- `--tamper-engine` → rc=2（変異 sha `0ea47a80…` ≠ pin）
- `--tamper=uh` → rc=1, bad 5,760 / `du` → 972 / `zd` → 1,260 / `ty` → 1,502
  （§2.6: z=0 床 10 cell の正当通過を含む） / `sb` → 2,623 / `ps` → 1,941 /
  `cs` → 2,364 / `rw` → 6

## 公式監査（本キット出版後に fetch-back bytes から実行・成果物は audit_* として追記出版）

1. fetch-back: 全ファイル size+sha256 byte 照合（verify・engine_block は全文照合）
2. 公式 4 走: 同一 cwd ×2（PYTHONHASHSEED=random/1）+ 隔離 tree/env -i ×2
   （PYTHONHASHSEED=99/7）→ 全走 rc=0・stdout byte-identical
   （predry と同一 sha `d3e244f4…` を確認）
3. 変異電池 9 種 → 全 fail-closed 確認
4. audit_run1-4.out/.info・tamper レコード・detcheck.json・MANIFEST-sha256 出版

## 規約

verdict 不消費・11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4
は全時点 UNKNOWN。engine は K1138 転写（sha pin 実装）・census は照合であって
証明の代替ではない。証明は宣言ノート §2（手証明全文）。
