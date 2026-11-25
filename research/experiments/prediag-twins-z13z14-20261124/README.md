# prediag-twins-z13z14-20261124（K1302 lane kit）

単一オーナー宣言ノート: `research/log/2026-11-24-prediag-twins-z13z14-single-owner-note.md`
（出版 `4905228a`・本キットに先行・証明全文はノート §2）。

## 内容

- `verify_k1302.py` — 検証機体（sha256
  `336aaf7a80f518a56e5dee70307ffe6bfedc96d24b0420819fec0815e5fafb16`）。
  T-PDT13/T-BDT13/T-PDT14/T-BDT14（z13/z14 pre-diag 双生児バンド・床・R 例外層込み・
  層厚 14）と L-BU13G/L-BU14G・sharpened C-PSF′ identity を、バンド/床 census
  （engine vs 申立・D1–D4）、typed 子 mex 電池（申立テーブルのみから子を構成・
  D5–D8）、均一性補題と公刊アンカー再照合（D9: L-BU13G/L-BU14G・K1301
  T-PDT11/T-BDT11/T-PDT12/T-BDT12・K1299 T-PDT9/T-BDT9/T-PDT10/T-BDT10・K1294
  T-PDT7/8・K1290 T-PDT5/6・K1289 T-PDT3/4・K1288 T-PDT1/2・K1286 T-PD0/T-B0・
  sharpened C-PSF′ identity w=0..14・T-TWIN・閉形式両 engine z∈2..15・B-exit w=1
  edge）、交差 engine（D10）、OBS 登録（z15/z16 band・beds・far-row R≥16・low-R・
  L-BU15G/L-BU16G 発現 probe・dedup sweep z=0..18・D11）で監査する。
  合計 111,961 比較点・期待 overall_bad 0。counts
  `[8928,360,8928,360,1939,114,1939,114,68531,1516,19232]`。
  決定的 stdout（揮発情報は stderr のみ）。TAMPER: `--tamper-engine`
  （rc 2・engine pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  ゲート）、`--tamper=z13s|z13b|z14s|z14b`（rc 1・D1–D4 の census 電池を
  fail させる: 期待 bad 8928/360/8928/360）。
  （生成履歴の honest 記録: K1301 kit からの機械的 surgery で生成後、初回
  ローカル実行が D1–D8 の engine plane 実引数残留 (11/12) を bad 2,376 として
  指摘・宣言前に 13/14 修正済み。ノート §2.7 参照。探索系は元から正しい plane。）
- `engine_block.py` — 公開 engine block 単体（sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`・
  K1282–K1301 kit と同一 bytes。explore 系が import に使用）。
- `explore_k1302.py` / `explore_k1302.out` — 宣言前 discovery census
  （X1–X4: z13/z14 band・beds の (R,δ) 表・mixed cell 0・R 例外層（厚み 14・
  R=0..13 が 2·[R odd]）の特定・R=14 seam 行（z13 全 1・z14 全 0）。
  X5/X6: L-BU13G/L-BU14G の発現。X7: sharpened C-PSF′ probe z=0..16。
  X8: typed 子 self-check（申立テーブルのみからの子構成 vs claim vs engine・
  宣言前構文検証 3,878+228 点 bad 0））。
- `explore2_k1302.py` / `explore2_k1302.out` — 宣言前 wide census + z15/z16 OBS
  （Y1/Y2: z13/z14 band 8,928×2・beds 360×2 の主張照合 bad 0。
  Y3–Y5: z15/z16 の OBS（band 4,500×2・beds 120×2・far-row m=12 R≥16 210×2・
  low-R (R<16) hist {0:637,2:616}×2・cpsf 予測と一致 bad 0・全称主張なし）。
  Y6: ordered engine 交差 z=13..16。Y7: L-BU13G/L-BU14G w≤40 + L-BU15G/L-BU16G
  発現 probe（z=16,17 は OBS）。Y8: T-TWIN identity・z=0..18 dedup sweep
  （C-PSF′ 観測が plane 18 まで拡張））。
- `predry/` — 宣言前ローカル 4 走（同一 cwd PYTHONHASHSEED random/1 +
  隔離 tree・env -i ×PYTHONHASHSEED=99/7）。stdout は全走 byte-identical
  （sha256
  `f6f26e095f1cb44b597fd2a3b7043c170e111f99119524c3099ac34630b43b0e`）。
  `.info` は stderr（揮発・参考）。
- （公式監査後に追加出版）`audit_run1-4.out+.info`、`tamper_*.out+.info`
  （5 モード）、`detcheck.json`、`MANIFEST-sha256`。

## 再現

```sh
python3 verify_k1302.py                  # counts [8928,360,8928,360,1939,114,1939,114,68531,1516,19232] total 111961 bad 0
python3 verify_k1302.py --tamper-engine  # rc 2 (engine sha gate)
python3 verify_k1302.py --tamper=z13s    # rc 1 (D1 bad 8928)
```

census は定理の実機照合であって証明の代替ではない（証明は宣言ノート
§2 の手証明）。OBS な z15/z16 表・L-BU15G/L-BU16G 観測を全称と解釈しないこと。
