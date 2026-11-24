# prediag-twins-z1z2-20261124（K1288 lane kit）

単一オーナー宣言ノート: `research/log/2026-11-24-prediag-twins-z1z2-single-owner-note.md`
（出版が本キットに先行。証明全文はノート §2）。

## 内容

- `verify_k1288.py` — 検証機体（sha256
  `25c6bdc7f0207b48de0c90e9d67a14b9001f0a09c1c79c710e86b0fb734f2fb5`）。
  T-PDT1/T-BDT1/T-PDT2/T-BDT2（z1/z2 pre-diag 双生児バンド・床）と
  subsumption C1–C4 を、バンド/床 census（engine vs 申立・D1–D4）、
  typed 子 mex 電池（申立テーブルのみから子を構成・D5–D8）、均一性
  補題 L-BU1G/L-BU2G と公刊アンカー再照合（D9）、交差 engine（D10）、
  OBS 登録（z3/z4 遠方行 g1(δ−2)/f0(δ−4)・z3 例外層 probe・D11）で
  監査する。合計 30,440 比較点・期待 overall_bad 0。
  決定的 stdout（揮発情報は stderr のみ）。公式 4 走は byte-identical
  （宣言済み期待 sha256
  `6d19ef62ecb6cd4b6342569758f5f29e1ed16c9614e0061fe557659906f54d04`）。
  TAMPER: `--tamper-engine`（rc 2・engine pin
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  ゲート）、`--tamper=z1s|z1b|z2s|z2b`（rc 1・census 電池を fail させる）。
- `engine_block.py` — 公開 engine block 単体（sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`・
  K1282–K1287 kit と同一 bytes。explore 系が import に使用）。
- `explore_k1288.py` / `explore_k1288.out` — 宣言前 census（X1/X1b:
  z1 pre-diag スライス・X2: z1 床・X3: z2 pre-diag スライス・X4: z2 床。
  m 分裂が R∈{0,1} 例外層に還元できることの発見一次資料）。
- `explore2_k1288.py` / `explore2_k1288.out` — 宣言前 wide census +
  z3/z4 先行観測（主張 4 則の広域照合: z1/z2 スライス各 39,160 点・
  床 1,350 点・ordered engine 交差 6,080 点すべて bad 0。
  z3/z4 の δ-law: R≥4 広 box 各 6,250 点 bad 0〔g1(δ−2)/f0(δ−4)〕、
  R≥2 域の δ-split（R∈{2,3} 汚染）の分離・δ-unique for R≥4/R≥6。
  これらは OBS〔全称主張なし〕）。
- `predry/` — 宣言前ローカル 4 走（同一 cwd PYTHONHASHSEED=random/1 +
  隔離 tree・env -i ×PYTHONHASHSEED=99/7）。stdout は全走 byte-identical
  （sha256 上記）。`.info` は stderr（揮発・参考）。
- （公式監査後に追加出版）`audit_run1-4.out+.info`、`tamper_*.out+.info`
  （5 モード）、`detcheck.json`、`MANIFEST-sha256`。

## 再現

```sh
python3 verify_k1288.py                 # counts [8928,360,8928,360,1939,114,1939,114,5720,1318,720] total 30440 bad 0
python3 verify_k1288.py --tamper-engine # rc 2 (engine sha gate)
python3 verify_k1288.py --tamper=z1s    # rc 1 (D1 bad 8928)
```

census は定理の実機照合であって証明の代替ではない（証明は宣言ノート
§2 の手証明）。observed な z3/z4 表を全称と解釈しないこと。
