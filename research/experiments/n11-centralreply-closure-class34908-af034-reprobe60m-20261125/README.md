# Part ED — af034 (class 34908) 単一キー 60M re-probe kit (2026-11-25)

実験dir: `research/experiments/n11-centralreply-closure-class34908-af034-reprobe60m-20261125/`
宣言: `research/log/2026-11-25-part-ed-af034-reprobe60m-declaration.md` (commit `8cc8ed0c`)。

## 何であるか・何でないか

- Part EA が 30M 条件で EXHAUSTED (honest UNKNOWN) とした batch-33 キー af034
  = (1152921504607911937, 68719476736) (class 34908 境界子・legal 95) を
  事前宣言済み予算 60M 条件で再 probe する単一オーナー Part の kit。
- **verdict は不消費。** result が LOSS でも canonical cache への採用は
  行わない (将来 Part の loss-only adoption が別途 pinned merger
  (`90711961…`) で行う)。WIN なら probe-level WIN として
  scrutiny-owner C++ gate (`9193f5b6…`) 待ち。EXHAUSTED@60M なら honest
  UNKNOWN (更なる高budget条件は別宣言)。
- **標準 11×11 空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 34908 (56キーすべて) は本 Part の前後を
  通じてすべて UNKNOWN のまま。** 勝敗・被覆・secured coverage の主張は
  本 dir のどこにもない。

## 構成 (kit = 本 README + MANIFEST + scripts 3 + input 4 + val-gate 8 + sources 6)

- `scripts/jsreplay.js` — Part EA kit byte-clone `84585617…` (変更なし)。
- `scripts/runbatch_af034-60m.sh` — Part EA 30M runner (`3b5083b4…`) の
  BUDGET 行 (30000000→60000000) 以外 byte 同一。派生 sha256
  `b0c5f714f926a923d35692672fbfc6aaf2da0081cdf4217c074e0f64d3a29f92`。
  two-pass fresh-cold・HARD-STOP on MISMATCH・truncated-sidecar guard・
  WIN-HALT / honest EXHAUSTED label は Part EA と同一。
- `scripts/audit_ed.py` — fail-closed audit。全 kit pin・fresh-increment
  gate (canonical `cecc1a0f` と quarantine `81d23160` への af034 不在)・
  15M/30M exhaustion 履歴・val-gate 4 行・anchor 3 キー node-exact・
  本 probe raw p1/p2 (key/legal/budget/two-pass node-exact + honest label)
  を検査し `output/audit_ed.json` を書く。1 gate でも破損があれば rc=1。
- `input/af034.input.csv` (`a4bff566…`) + anchor 用 af001 (`b2ef3588…`) /
  af029 (`b5500b8d…`) / af039 (`e51a3c9d…`) — すべて Part EA kit
  byte-clone。
- `val-gate/` — Part EA kit val-gate 4 行の byte-clone (input 2種 +
  published-baseline 4件)。fresh host 走 `.ed-host.out` (実行フェーズで
  生成) との比較は wall_s 列を除く全 replay 列一致で行う。
- `sources/` — b33-status.log (`1f663fc8…`)・ea-status.log
  (`db7c7017…`)・exh30m/af034.p1.out (`9ecfdc77…`) / p2
  (`3978990d…`)・canonical-cache-ec-merged-cecc1a0f-20261125.cache
  (`cecc1a0f…`・277,523B・Part EC chain head)・
  n11-s5-evidence-quarantine.json (`81d23160…`)。

## 事前登録 anchor / val-gate (宣言どおり)

- anchors (ED runner 60M cap・2-pass): af001 → LOSS 2,952,432・
  af029 → WIN 4,862,485 (WIN-HALT rc45)・af039 → LOSS 19,234,232
  (30M 条件値と同一 node = budget-crossing 検証)。
- val-gate (published 条件 budget・1-pass fresh): at2m 2行 →
  EXHAUSTED (2000000,0,2000000)・first-15m → (15000000,2,3651923)・
  second-15m → (15000000,2,5040200)。

## 実行記録 (run record)

- (pending — 実行フェーズ後に README 最終化 wave で更新する)
