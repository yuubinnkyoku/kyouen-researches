# prediag-twins-z3z4-20261124（K1289 lane kit）

単一オーナー宣言ノート: `research/log/2026-11-24-prediag-twins-z3z4-single-owner-note.md`
（出版が本キットに先行。証明全文はノート §2）。

## 内容

- `verify_k1289.py` — 検証機体（sha256
  `f8d86f9efead5667af3439a51a1aac7cb6079249bf9d332e4a54539b86759ea4`）。
  T-PDT3/T-BDT3/T-PDT4/T-BDT4（z3/z4 pre-diag 双生児バンド・床・R 例外層込み）
  と L-BU3G/L-BU4G・sharpened C-PSF′ identity を、バンド/床 census（engine vs
  申立・D1–D4）、typed 子 mex 電池（申立テーブルのみから子を構成・D5–D8）、
  均一性補題と公刊アンカー再照合（D9: L-BU3G/L-BU4G・K1286 T-PD0/T-B0・
  K1288 T-PDT1/2・T-BDT1/2・C-PSF′ identity・T-TWIN・閉形式両 engine）、
  交差 engine（D10）、OBS 登録（z5/z6 band・beds・far-row・low-R・D11）で
  監査する。合計 55,159 比較点・期待 overall_bad 0。
  counts `[8928,360,8928,360,1939,114,1939,114,20431,1516,10530]`。
  決定的 stdout（揮発情報は stderr のみ）。TAMPER: `--tamper-engine`
  （rc 2・engine pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  ゲート）、`--tamper=z3s|z3b|z4s|z4b`（rc 1・D1–D4 の census 電池を
  fail させる: 期待 bad 8928/360/8928/360）。
- `engine_block.py` — 公開 engine block 単体（sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`・
  K1282–K1288 kit と同一 bytes。explore 系が import に使用）。
- `explore_k1289.py` / `explore_k1289.out` — 宣言前 discovery census
  （X1–X4: z3/z4 band・beds の (R,δ) 表・mixed cell 0・R 例外層の特定。
  X5/X6: L-BU3G/L-BU4G の発見。X7: sharpened C-PSF′ probe z=0..6）。
- `explore2_k1289.py` / `explore2_k1289.out` — 宣言前 wide census + z5/z6 OBS
  （Y1/Y2: z3/z4 band 8,928×2・beds 360×2 の主張照合 bad 0。
  Y3–Y5: z5/z6 の OBS（band 4,500×2・beds 120×2・far-row 216×2・cpsf 予測と
  一致 bad 0・全称主張なし）。Y6: ordered engine 交差 z=3..6。
  Y7: L-BU3G/L-BU4G w≤40 + L-BU5G/L-BU6G 発見 probe（z=6,7 は OBS）。
  Y8: T-TWIN identity・z=0..6 dedup sweep）。
- `predry/` — 宣言前ローカル 4 走（同一 cwd PYTHONHASHSEED=random/1 +
  隔離 tree・env -i ×PYTHONHASHSEED=99/7）。stdout は全走 byte-identical
  （sha256
  `a9f0dabcc88c99063a5539163226b56bc46e145537c5c1e4e0f4044c7e748b37`）。
  `.info` は stderr（揮発・参考）。honest: 最初の隔離走は env -i の PATH に
  /usr/local/bin がなく空出力となった（python3 の所在）。同梱の iso_99/iso_7
  は PATH 修正後の正走。
- （公式監査後に追加出版）`audit_run1-4.out+.info`、`tamper_*.out+.info`
  （5 モード）、`detcheck.json`、`MANIFEST-sha256`。

## 再現

```sh
python3 verify_k1289.py                 # counts [8928,360,8928,360,1939,114,1939,114,20431,1516,10530] total 55159 bad 0
python3 verify_k1289.py --tamper-engine # rc 2 (engine sha gate)
python3 verify_k1289.py --tamper=z3s    # rc 1 (D1 bad 8928)
```

census は定理の実機照合であって証明の代替ではない（証明は宣言ノート
§2 の手証明）。OBS な z5/z6 表を全称と解釈しないこと。
