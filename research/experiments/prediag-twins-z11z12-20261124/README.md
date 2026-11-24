# prediag-twins-z11z12-20261124（K1301 lane kit）

単一オーナー宣言ノート: `research/log/2026-11-24-prediag-twins-z11z12-single-owner-note.md`
（出版が本キットに先行・証明全文はノート §2）。

## 内容

- `verify_k1301.py` — 検証機体（sha256
  `6026e07f8f61f4434c5a23738d5471bdcf871b4c91fa8aac4286a15667ff5b05`）。
  T-PDT11/T-BDT11/T-PDT12/T-BDT12（z11/z12 pre-diag 双生児バンド・床・R 例外層込み・
  層厚 12）と L-BU11G/L-BU12G・sharpened C-PSF′ identity を、バンド/床 census
  （engine vs 申立・D1–D4）、typed 子 mex 電池（申立テーブルのみから子を構成・
  D5–D8）、均一性補題と公刊アンカー再照合（D9: L-BU11G/L-BU12G・K1299
  T-PDT9/T-BDT9/T-PDT10/T-BDT10・K1294 T-PDT7/8・K1290 T-PDT5/6・K1289
  T-PDT3/4・K1288 T-PDT1/2・K1286 T-PD0/T-B0・C-PSF′ identity w=0..12・
  T-TWIN・閉形式両 engine z∈2..13・B-exit w=1 edge）、交差 engine（D10）、
  OBS 登録（z13/z14 band・beds・far-row R≥14・low-R・L-BU13G/L-BU14G 発現
  probe・dedup sweep z=0..16・D11）で監査する。
  合計 101,503 比較点・期待 overall_bad 0。counts
  `[8928,360,8928,360,1939,114,1939,114,58911,1516,18394]`。
  決定的 stdout（揮発情報は stderr のみ）。TAMPER: `--tamper-engine`
  （rc 2・engine pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  ゲート）、`--tamper=z11s|z11b|z12s|z12b`（rc 1・D1–D4 の census 電池を
  fail させる: 期待 bad 8928/360/8928/360）。
- `engine_block.py` — 公開 engine block 単体（sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`・
  K1282–K1299 kit と同一 bytes。explore 系が import に使用）。
- `explore_k1301.py` / `explore_k1301.out` — 宣言前 discovery census
  （X1–X4: z11/z12 band・beds の (R,δ) 表・mixed cell 0・R 例外層（厚み 12・
  R=0..11 が 2·[R odd]）の特定。X5/X6: L-BU11G/L-BU12G の発現。
  X7: sharpened C-PSF′ probe z=0..14。X8: typed 子 self-check（申立テーブル
  のみからの子構成 vs claim vs engine・宣言前構文検証 3,878+228 点 bad 0））。
- `explore2_k1301.py` / `explore2_k1301.out` — 宣言前 wide census + z13/z14 OBS
  （Y1/Y2: z11/z12 band 8,928×2・beds 360×2 の主張照合 bad 0。
  Y3–Y5: z13/z14 の OBS（band 4,500×2・beds 120×2・far-row m=12 R≥14 215×2・
  low-R (R<14) hist {0:582,2:567}×2・cpsf 予測と一致 bad 0・全称主張なし）。
  Y6: ordered engine 交差 z=11..14。Y7: L-BU11G/L-BU12G w≤40 + L-BU13G/L-BU14G
  発現 probe（z=14,15 は OBS）。Y8: T-TWIN identity・z=0..16 dedup sweep
  （C-PSF′ 観測が plane 16 まで拡張））。
- `predry/` — 宣言前ローカル 4 走（同一 cwd PYTHONHASHSEED random/1 +
  隔離 tree・env -i ×PYTHONHASHSEED=99/7）。stdout は全走 byte-identical
  （sha256
  `70206d62b8a8e91d97bed7403dfaf6d970db47b4c32de4cecc98e7358a5d562c`）。
  `.info` は stderr（揮発・参考）。
- （公式監査後に追加出版）`audit_run1-4.out+.info`、`tamper_*.out+.info`
  （5 モード）、`detcheck.json`、`MANIFEST-sha256`。

## 再現

```sh
python3 verify_k1301.py                  # counts [8928,360,8928,360,1939,114,1939,114,58911,1516,18394] total 101503 bad 0
python3 verify_k1301.py --tamper-engine  # rc 2 (engine sha gate)
python3 verify_k1301.py --tamper=z11s    # rc 1 (D1 bad 8928)
```

census は定理の実機照合であって証明の代替ではない（証明は宣言ノート
§2 の手証明）。OBS な z13/z14 表・L-BU13G/L-BU14G 観測を全称と解釈しないこと。
