# csum-multitoken-20261125 — C-SUM 多重トークン tail collapse 機体（K1312）

publish-then-execute: 単一オーナー宣言ノート
`research/log/2026-11-25-csum-multitoken-single-owner-note.md` が先に出版
されており、本キットはその §4 機体宣言の実体。定理・手証明・非主張の
区別はすべて宣言ノート参照（この README は重複正本としない）。

## 主張の要約（詳細は宣言ノート §1/§2/§4.5）

- **T-CSUM（全称）**: ∀ n≥1, 多重集合 X（n トークン・各≥1）, S=sum(X),
  ∀ z≥0, ∀ k ≥ z+n−1: **H(S+k; X; z) = S mod 2**（§2 二重帰納の手証明が
  正本。K1308 O3/F1 の C-SUM census 予想を解決）。
- **L-1**: 単一トークン tail k≥z で H(x+k; (x); z) = x mod 2
  （公刊 K0832 閉形式の 4 分枝スライス）。**L-2**: H(R; (); z) = 0。
- **C-SHARP**: n≥2 では閾値は下げられない（k=z+n−2 に反則セルが必ず
  存在・公刊 K1311 T-DB から厳密に従う系・D12 で 140 点有限確認）。
- **インターロック**: K1311 T-DB（境界行 k=z+n−2）+ 本項（tail
  k≥z+n−1）で全多重集合 n≥2 の k≥z+n−2 が確定。E6 の 149 witness が
  全て D(E,k) に一致（D11・149/149）。all-ones では公刊 K0832 tail 系
  と閾値・値が一致。
- 規約上: verdict 不消費・11×11 巨大探索への影響は literary。

## ファイル（sha256）

| file | sha256 |
|---|---|
| verify_k1312.py | `eba59473aca206b95bb032547963f685a7c1dc21a8d058882f8c90f7ef628184` |
| engine_block.py | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`（K1282..K1311 chain と同一 bytes） |
| explore_csum.py | `ee40aaaeabfdbc7834cde2f41e7d4afe8199a3a51c5891a5d403d65508e35f96` |
| explore_csum.out | `4467429dc2991a1cd90cbf697dcb76c6560b684f7e272e43e80fdadd6f117b17`（宣言前探索 E6/E7/E8 の正本） |
| predry/dryrun1-4.out | 4 走とも `b22b9b022461cc5b7e1927a180f92b37a7768f48ce2ace1ccb8a0e05d9404e3b`（byte-identical） |

埋込み engine block の起動 sha gate: pin
`bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
（verify_k1312.py 内蔵・不一致なら即時 abort）。

## 電池（宣言ノート §4・総計 26,302 点・期待 overall_bad = 0）

D1 T-CSUM census n=3（z=0..12・tokens≤6・k=z+2..z+4）2,184 / D2 census
n=4 + far n=3 stress 2,310 / D3 census n=5（z=0..7・ tokens≤5）3,024 /
D4 census n=6/n=7 + far n=4 stress 1,748 / D5 typed self-check
（n=2..5・z≤8・tokens≤5・k=z+n−1..z+n+1。子は申立表+公刊閉形式のみで
構成・mex==申立==engine・均一性）6,642 / D6 基底補題（L-2・L-1 両
エンジン・n=1 子均一性）920 / D7 公刊アンカー転写（K1308 D8 C-SUM
boxes 2,364 + T-UH 5,760 + L-SB 264 = 8,388） / D8 cross-engine E9 boxes
616 / D9 sharpness witnesses（E6 149 セル再評価）149 / D10 OBS 表
（E7 20 + E8 12・主張なし）32 / D11 T-DB interlock（149/149） /
D12 sharp construction（n=2..11・z=0..6・2 家族）140。約 8.2 秒/走。

## 変異電池（fail-closed・事前宣言）

- `--tamper-engine` → rc=2（変異 sha `0ea47a80…` ≠ pin）
- `--tamper=c3` → rc=1, bad 2,184 / `c4` → 2,310 / `c5` → 3,024 /
  `c67` → 1,748 / `ty` → 24,648 / `lm` → 920 / `ps` → 8,388 /
  `ce` → 616 / `sw` → 149 / `ob` → 1 / `db` → 149 / `sc` → 140

## 公式監査（本キット出版後に fetch-back bytes から実行・成果物は output/ に追記出版）

1. fetch-back: 全ファイル byte 照合（API 側・sha256）
2. 公式 4 走: 同一 cwd ×2（PYTHONHASHSEED=random/1）+ 隔離 tree
   `env -i` ×2（PYTHONHASHSEED=99/7）→ 全走 rc=0・stdout byte-identical
   （predry と同一 sha `b22b9b02…` を確認）・総計 26,302・overall_bad=0
3. 変異電池 12 種 → 上表 bad count・rc で全 fail-closed 確認
4. output/audit_run1-4.out/.info・tamper レコード 12 種・detcheck.json・
   MANIFEST-sha256 出版

## 規約

verdict 不消費・11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN。
engine は K1138 転写（K1257 と同一 bytes・pin gate 実装）・census は照合
であって証明の代替ではない。証明は宣言ノート §2（手証明全文）。
E7/E8 は OBS（無主張）。
