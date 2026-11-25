# prediag-cpsfgen-allw-20261124（K1303 lane kit）

単一オーナー宣言ノート: `research/log/2026-11-24-prediag-cpsfgen-all-w-single-owner-note.md`
（出版 `5bd25b49`・本キットに先行・証明全文はノート §2）。

## 内容

- `verify_k1303.py` — 検証機体（sha256
  `1efdcf9e2776e4e57ee452f3d1fee823d1fa2d7eaa87e7ff853ba9a4edf2af0c`）。
  T-GEPSF/T-GEBED（一般 w ペア則・床則・L(w)=2⌈w/2⌉ 例外層込み）と
  L-BU-GEN（一般 w B-exit 均一性）を、一般 band/bed census（engine vs 申立・
  D1/D2）、typed 一般自己検査（子を一般申立テーブル plane w / w−1 + 閉形式のみ
  から構成した mex が申立値・engine と一致・D3）、crossing/seam 行 census
  （D4・床行 R≥0 guard 付）、L-BU-GEN 閉形式×CPSF-GEN×engine（D5）、単一
  トークン閉形式×両 engine（D6）、包摂 identity sweep（既刊 per-plane 主張転写
  z0..z14 == CPSF-GEN == engine・D7）、新規面 census w=17..20（D8）、T-TWIN
  代数恒等式（D9）、交差 engine ordered vs canonical（D10）、far-m 行 stress +
  dedup (R,δ) sweep z=0..20 + spot planes w=21..24（D11）で監査する。
  全 battery が同一の一般則関数 cpsfG を plane 0..24 で走査（per-plane 特殊
  分岐なし）。合計 332,446 比較点・期待 overall_bad 0。counts
  `[137700, 3808, 34901, 41124, 19499, 1440, 35175, 17952, 521, 3954, 36372]`。
  決定的 stdout（揮発情報は stderr のみ）。TAMPER: `--tamper-engine`
  （rc 2・engine pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
  ゲート・変異 sha `0ea47a80…` ≠ pin）、`--tamper=hl`（rc 1・D1 bad 137,700），
  `--tamper=hbd`（rc 1・D2 bad 3,808），`--tamper=ws`（rc 1・rc 1・bad 総
  212,232 = `[91832, 2072, 23274, 29788, 7145, 0, 26447, 4242, 0, 0, 27432]`），
  `--tamper=Ls`（rc 1・bad 総 21,102 =
  `[6880, 250, 2144, 8631, 270, 0, 1765, 705, 0, 0, 457]`）。
- `engine_block.py` — 公開 engine block 単体（sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`・
  K1282–K1302 kit と同一 bytes。explore 系が import に使用）。
- `explore_k1303.py` / `explore_k1303.out` — 宣言前 discovery census
  （X1: 一般 band census planes w=0..16 137,700 点 bad 0。X2: 一般 bed census
  3,808 点 bad 0。X3: typed 自己検査 34,901 点 bad 0。X4: crossing/seam 行
  徹底 77,060 点 bad 0〔当初 8 無効 cell guard はノート §2.7〕。X5: L-BU-GEN
  3 region 被覆 19,499 点。X6: 新規面 w=17..20 17,952 点。X7: dedup (R,δ)
  sweep z=0..20 全 21 面 mixed 0。X8: cross-engine 3,648 点）。
- `explore2_k1303.py` / `explore2_k1303.out` — 宣言前シンボリック照合
  （Y1: mex 表メタ検査 d∈[−3000..3000] 12,002 点 bad 0〔§2.3/§2.4 の 2 表が
  d の偶奇別全範囲で閉じる直接照合〕。Y2: L-BU-GEN wide w≤36, x≤48 45,288 点。
  Y3: 核心/核 cell 遠方 768 点。Y4: 奇数 w 横断・seam 行の C 子定数性 895 点）。
- `predry/` — 宣言前ローカル 4 走（同一 cwd・PYTHONHASHSEED
  random/1/99/7）。stdout は全走 byte-identical（sha256
  `af25dfac45327bea7769bffb03197b26f76f7e67799919e5d68f07b0d79109f2566`）。
  `.info` は stderr（揮発・参考）。
- （公式監査後に追加出版）`audit_run1-4.out+.info`、`tamper_*.out+.info`
  （5 モード）、`detcheck.json`、`MANIFEST-sha256`。

## 再現

```sh
python3 verify_k1303.py                   # counts [137700, 3808, 34901, 41124, 19499, 1440, 35175, 17952, 521, 3954, 36372] total 332446 bad 0
python3 verify_k1303.py --tamper-engine   # rc 2 (engine sha gate)
python3 verify_k1303.py --tamper=hl       # rc 1 (D1 bad 137700)
```

census は定理の実機照合であって証明の代替ではない（証明は宣言ノート §2 の
手証明・typed mex による全称 w 帰納）。
