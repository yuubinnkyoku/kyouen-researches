# prediag-twins-z7z8-20261124（K1294 lane kit）

単一オーナー宣言ノート: `research/log/2026-11-24-prediag-twins-z7z8-single-owner-note.md`
（出版が本キットに先行・commit `8dce7a3d`。証明全文はノート §2）。

## 内容

- `verify_k1294.py` — 検証機体（sha256
  `b3974b63e43a67c32689d247377558d34720a66d303b54bda5485be5c69edf81`）。
  T-PDT7/T-BDT7/T-PDT8/T-BDT8（z7/z8 pre-diag 双生児バンド・床・R 例外層込み・
  層厚 8）と L-BU7G/L-BU8G・sharpened C-PSF′ identity を、バンド/床 census
  （engine vs 申立・D1–D4）、typed 子 mex 電池（申立テーブルのみから子を構成・
  D5–D8）、均一性補題と公刊アンカー再照合（D9: L-BU7G/L-BU8G・K1290
  T-PDT5/T-BDT5/T-PDT6/T-BDT6・K1289 T-PDT3/T-BDT3/T-PDT4/T-BDT4・K1288
  T-PDT1/2・T-BDT1/2・K1286 T-PD0/T-B0・C-PSF′ identity w=0..8・T-TWIN・
  閉形式両 engine z∈2..9・B-exit w=1 edge）、交差 engine（D10）、OBS 登録
  （z9/z10 band・beds・far-row・low-R・L-BU9G/L-BU10G 発現 probe・dedup sweep
  z=0..12・D11）で監査する。合計 80,059 比較点・期待 overall_bad 0。counts
  `[8928,360,8928,360,1939,114,1939,114,39671,1516,16190]`。
  決定的 stdout（揮発情報は stderr のみ）。TAMPER: `--tamper-engine`
  （rc 2・engine pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  ゲート）、`--tamper=z7s|z7b|z8s|z8b`（rc 1・D1–D4 の census 電池を
  fail させる: 期待 bad 8928/360/8928/360）。
- `engine_block.py` — 公開 engine block 単体（sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`・
  K1282–K1290 kit と同一 bytes。explore 系が import に使用）。
- `explore_k1294.py` / `explore_k1294.out` — 宣言前 discovery census
  （X1–X4: z7/z8 band・beds の (R,δ) 表・mixed cell 0・R 例外層（厚み 8・
  R=0..7 が 2·[R odd]）の特定。X5/X6: L-BU7G/L-BU8G の発現。
  X7: sharpened C-PSF′ probe z=0..10。X8: typed 子 self-check（申立テーブル
  のみからの子構成 vs claim vs engine・宣言前構文検証 3,878+228 点 bad 0））。
- `explore2_k1294.py` / `explore2_k1294.out` — 宣言前 wide census + z9/z10 OBS
  （Y1/Y2: z7/z8 band 8,928×2・beds 360×2 の主張照合 bad 0。
  Y3–Y5: z9/z10 の OBS（band 4,500×2・beds 120×2・far-row 216×2・low-R
  (R<10) hist {0:346,2:340}×2・cpsf 予測と一致 bad 0・全称主張なし）。
  Y6: ordered engine 交差 z=7..10。Y7: L-BU7G/L-BU8G w≤40 + L-BU9G/L-BU10G
  発現 probe（z=10,11 は OBS）。Y8: T-TWIN identity・z=0..12 dedup sweep
  （C-PSF′ 観測が plane 12 まで拡張））。
- `predry/` — 宣言前ローカル 4 走（同一 cwd PYTHONHASHSEED random/1 +
  隔離 tree・env -i ×PYTHONHASHSEED=99/7）。stdout は全走 byte-identical
  （sha256
  `c424a680cb2b9711893edac4029c61faca253afe103d0e0d978554d572e8af50`）。
  `.info` は stderr（揮発・参考）。
- （公式監査後に追加出版）`audit_run1-4.out+.info`、`tamper_*.out+.info`
  （5 モード）、`detcheck.json`、`MANIFEST-sha256`。

## 再現

```sh
python3 verify_k1294.py                 # counts [8928,360,8928,360,1939,114,1939,114,39671,1516,16190] total 80059 bad 0
python3 verify_k1294.py --tamper-engine # rc 2 (engine sha gate)
python3 verify_k1294.py --tamper=z7s    # rc 1 (D1 bad 8928)
```

census は定理の実機照合であって証明の代替ではない（証明は宣言ノート
§2 の手証明）。OBS な z9/z10 表・L-BU9G/L-BU10G 観測を全称と解釈しないこと。
