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

## 構成 (kit = 本 README + MANIFEST + scripts 3 + input 4 + val-gate 8 + sources 6、
実行後に output 15 ファイルを追加)

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

## 実行記録 (run record, 2026-11-25T05:07-05:20Z)

- 実行hostは Vibe upgraded sandbox (node v22.20.0, 2コア, コンパイラなし)。
  amendment (`2a0c3318`) どおり runner は detached (nohup+disown) 起動し、
  invocation を跨いで監視した。
- val-gate 4/4 PASS。host fresh 走 4件のうち、at2m の2件は
  published baseline と byte 一致。first-15m / second-15m は
  budget・result・nodes 列が baseline と一致 (3651923 / 5040200)。
- anchors 3/3 PASS (60M cap で two-pass node-exact)。af001 = LOSS
  2,952,432・af029 = WIN 4,862,485 (WIN-HALT rc45)・af039 = LOSS
  19,234,232 (EA 30M 条件値と同一 node)。
- 本 probe af034: p1 result=2 (LOSS) nodes=32,012,059 (wall 176s)、
  p2 result=2 nodes=32,012,059 (wall 180s)。two-pass fresh-cold
  node-exact。key (1152921504607911937, 68719476736)・legal 95・
  forbidden quadruples 95670・order=0・share_tt=0。
- nodes 32,012,059 は予算区間 (30M, 60M] にある。exhaustion 履歴
  15M EXH → 30M EXH ののち 60M 条件で解決したため、af034 は
  本 Part の probe-level では fresh exact LOSS。
- audit_ed.py (sha256 `6f76e8e5…`) clean run: 58/58 gates PASS、
  `output/audit_ed.json` (8,139B・sha256 `5473eafb…`) 生成。
- tamper battery (fail-closed 確認。実行後はすべて復元し、clean run
  PASS を取り直した):
  - T2: raw p1 の nodes 桁を 1つ改変 → `af034:two-pass-node-exact` が
    fail。検出を確認。
  - T3: status.log の verdict 桁 (2→1) を改変 →
    `status:af034-win-line` が fail。検出を確認。
  - T1: status.log の af034 nodes 桁を 1つ改変 → audit は PASS の
    まま。これは kit 宣言時点で結果を未知とする label-agnostic な
    status gate 設計によるもので、node 数の権限は raw 側 gate が
    持つ。post-result の機械照合で status.log = raw p1 = raw p2 =
    audit main_probe = drive.out のすべてが (2, 32,012,059) である
    ことを確認した。検証者は node 数の根拠を raw/ 側に求められたい。
  - 運用ミス録: battery 中、audit の stdout を向ける先を
    audit スクリプト自身が書く `output/audit_ed.json` にしてしまい
    二重書き込みが発生した (起動側のミスであり、audit_ed.py は無実)。
    stdout を別ファイルに逃がして再生成した。

## 出力 (wave C, 15 ファイル。git blob sha1 fetch-back 15/15 一致)

- `output/status.log` (`26a97e02…`・242B)・`output/af034.drive.out`
  (`d2d52ed6…`・31B)・`output/audit_ed.json` (`5473eafb…`・8,139B)。
- `output/raw/` 8件: af001 p1/p2 (`9124225f…` 同一bytes)・af029 p1
  (`971a9b29…`) / p2 (`21c7b218…`)・af034 p1 (`63860f94…`) / p2
  (`eb64725f…`)・af039 p1 (`da227971…`) / p2 (`15abe72f…`)。
- `val-gate/*.ed-host.out` 4件: at2m×2 (`6e902ab1…`/`eeafe3ac…`)・
  first-15m (`2e8c1dd5…`)・second-15m (`45cb1348…`)。

## 結論と消費

- **af034 (s5 index 930660) = probe-level fresh exact LOSS @60M 条件
  (two-pass node-exact)。ただし verdict は不消費。** canonical cache
  への採用は、Part EC パターンの pinned loss-only adoption (別 Part、
  merger `90711961…` byte-clone) が行う。
- **class 34908 は unknown 7 のまま。標準 11×11 空盤・19 roots・
  二石root・S2・class 1/2/4 もすべて UNKNOWN のまま。** nodes は
  bookkeeping であり、勝敗・被覆・距離の主張ではない。
- commits: 宣言 `8cc8ed0c` → amendment `2a0c3318` → kit `15e973e6`
  → wave C `2b996b81` → wave D (本 README + MANIFEST 更新)。
