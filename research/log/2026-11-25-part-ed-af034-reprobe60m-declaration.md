# Part ED 宣言: af034 (class 34908・EXHAUSTED@30M 残) 60M 再probe計画 (2026-11-25)

単一オーナー Part ED・publish-then-execute。観測 HEAD (宣言直前)
`5085d19f5734f594cdd396724274ce5a4b5c8430` (2026-11-25T04:25:52Z・K1314 run log
update)。commit message 機械走査: 「Part ED」total_count=0・「af034 60m」
total_count=0・「reprobe60m」total_count=0 (Excel 世代は log ファイル名
2026-11-25-part-ed-* を直接 probe しても未使用であることを本宣言出版後に
再確認する)。「af034 reprobe」3件はすべて完結済み Part EA (30M) の記述で
対抗宣言ではない。Part 文字は RS 記法どおり既存 max が EC のため ED を使用。

**11×11 空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 34908 (56キーすべて) は本 Part の前後を通じてすべて
UNKNOWN のまま。** 本 Part は probe 1キーの honest label 取得のみを行い、
verdict の消費 (canonical cache 系への採用) は一切行わない。

## 対象と事前状況 (全て出版済み bytes の pin)

- 対象キー: af034 = (lo, hi) = (1152921504607911937, 68719476736)・
  stones=5・legal=95 (batch-33 キー。class 34908 (
  1152921504607895553, 68719476736) の境界子)。
- 出版済み条件: batch-33 15M で EXHAUSTED (b33-status.log `1f663fc8…` 39-40行目
  「af034 PASS/EXHAUSTED 15000000,0,15000000」) → Part EA 30M で再probe
  EXHAUSTED (ea-status.log `db7c7017…`「af034 PASS 30000000,0,30000000」+
  raw p1 `9ecfdc77…` / p2 `3978990d…`・wall 163s/p1)。いずれも
  honest UNKNOWN。
- class 34908 の現在の unknown 構成 (Part EC reaudit closure `0ae9749c…`・
  unknown 7): 不消費WIN 6行 {af023 (s5 810351), af029 (900646), af047
  (961976), af048 (962172), af050 (962386), af053 (962470)} + 本キー af034
  (930660)。WIN 6行は scrutiny-owner C++ gate `9193f5b6…` 専権で本環境では
  消費不能 (g++ 等コンパイラ不在・パッケージインストール禁止を本実行で
  再確認済み)。したがって af034 の高budget再probe が本 Part 時点で
  closure frontier 上唯一の probe 可能な残作業である (rank 上位 class
  23101/1849/2251 (各WIN 1行)・16371 (WIN 2行)・16757 (WIN 3行)・5804
  (WIN 4行 {ad024,ad028,ad043,ad055})・20421 (WIN 6行)・34269 (WIN 11行
  {ac002,ac003,ac006,ac020,ac026,ac027,ac034,ac041,ac045,ac048,ac054})・
  5343 (WIN 46行) は全行 C++ gate 待ち・Part DL/DN README の機械記述と
  b28win46 queue registry で確認)。

## 事前宣言条件 (binding)

1. **BUDGET = 60,000,000** (60M)。Part EA の 15M→30M と同一の 2倍
   予算条件 upgrade。同一条件 (15M/30M) の再probeは行わない
   (同一条件再probe禁止規約・EXHAUSTED 行の 15M/30M 条件は再実行しない)。
2. **two-pass fresh-cold node-exact**: runner による p1/p2 2走の
   `replay,` 行 (budget,result,nodes) 一致を必須とする。不一致 (rc=42
   MISMATCH) は HARD-STOP。
3. **cross-invocation resume**: jsreplay byte-clone の改変禁止
   (`84585617…`)・runbatch 系 runner の file-existence + truncated-sidecar
   guard (\# replay_done 欠落は証拠でなく再実行) をそのまま使用し、
   1 invocation = 1 pass (60M pass は実測 ~256s (af001 2,952,432 nodes /
   wall 13s = 227k nodes/s 外挿) で 290s inner window に 1 pass のみ収まる
   ため、p1 と p2 は別 invocation で実行する。
   ただし partition 実行 (両passが file-existence guard で冪等に完了した
   後の再実行) は runner guard が自動排除する。
4. **WINDOW-EXCEEDED 事前登録**: 同一 pass で TRUNCATED-RETRY が 2回
   記録された場合、60M pass は本 host の invocation window に収まらない
   と判定し本 Part では honest unresolved として skip を宣言する
   (成果物には skip 事実と truncated sidecar を honesty 記録。将来 Part
   での別 window 設計に委ねる)。
5. **honest label 規約**: result=2 (LOSS) なら nodes > 30,000,000 を
   検証して fresh 解決として記録 (将来 Part で loss-only 採用候補に
   なる。本 Part では採用しない)。result=1 (WIN) なら probe-level
   WIN として記録し scrutiny-owner C++ gate 待ち (verdict 不消費)。
   result=0 なら EXHAUSTED@60M (nodes == 60,000,000) として honest
   UNKNOWN を記録し以後の更なる高budget条件 (例 120M) は別宣言とする。
   いずれの場合も 11×11・class 34908 の勝敗・coverage・secured の主張を
   行わない。
6. **fresh-increment gate**: 対象キーが canonical chain head (Part EC merged
   cache `cecc1a0f…` 6,665行) と quarantine registry (`81d23160…`) の
   両方に不在であることを kit audit で検証する (fresh であること・
   既知 verdict との衝突がないこと)。

## kit 構成 (実験dir)

`research/experiments/n11-centralreply-closure-class34908-af034-reprobe60m-20261125/`

- scripts/jsreplay.js: byte-clone `84585617…` (Part EA kit・変更なし)
- scripts/runbatch_af034-60m.sh: Part EA 30M runner (`3b5083b4…`) との
  diff は BUDGET 行 (6行目 30000000→60000000) のみ。派生 sha256
  `b0c5f714f926a923d35692672fbfc6aaf2da0081cdf4217c074e0f64d3a29f92`
- scripts/audit_ed.py: fail-closed audit (kit pin 全照合・anchor/val-gate/
  本probe raw の node-exact・honest label・fresh-increment gate)
- input/af034.input.csv: byte-clone `a4bff566…` (EA kit 対象行
  `target,0,5,1152921504607911937,68719476736,95,0,0,0,0,0`)
- input/af001.input.csv `b2ef3588…` / af029.input.csv `b5500b8d…` /
  af039.input.csv `e51a3c9d…`: anchor 用 byte-clone (EA kit)
- val-gate/ 8ファイル: Part EA kit val-gate 4行 (at2m 2行 = EXHAUSTED
  (2000000,0,2000000) ×2・first-15m (15000000,2,3651923)・second-15m
  (15000000,2,5040200)) の input.csv + published-baseline.out byte-clone。
  fresh host 走 (.ed-host.out) で budget,result,nodes (wall_s 以外の
  replay 行全列) の一致を要求
- sources/b33-status.log `1f663fc8…` / sources/ea-status.log `db7c7017…` /
  sources/exh30m/af034.p1.out `9ecfdc77…` / af034.p2.out `3978990d…` /
  sources/canonical-cache-ec-merged-cecc1a0f-20261125.cache `cecc1a0f…`
  (277,523B) / sources/n11-s5-evidence-quarantine.json `81d23160…`

## anchor・val-gate の事前登録 (node-exact 必須)

- **anchors (ED runner = 60M cap で再現・2-pass)**:
  af001 → LOSS result=2 nodes 2,952,432 (published b33 15M 条件値)。
  af029 → WIN result=1 nodes 4,862,485 (published b33 15M WIN anchor。
  runner は WIN-HALT rc=45・status.log に WIN-HALT 行)。
  af039 → LOSS result=2 nodes 19,234,232 (published Part EA 30M 条件値。
  budget-crossing 検証: 30M条件で解決済みのキーが 60M cap でも同一
  node 解決になることを要求)。
- **val-gate (published 条件 budget で再現・1-pass fresh)**: 上記 4行。
  jsreplay は byte-clone で budget はコマンドライン引数
  (--exact-replay-budget=2000000 / 15000000) で指定し published 条件を
  再現する。
- anchor 合計は約 2×(2,952,432+4,862,485+19,234,232) = 54,098,298
  nodes/pass。val-gate 合計約 12,684,046 nodes 単走。

## 出版 wave 計画 (各 wave fetch-back 照合)

1. wave A: 本宣言log
2. wave B: kit (scripts 3 + input 4 + val-gate 8 + sources 6 + README
   (run record pending) + MANIFEST-sha256 (kit 分))
3. wave C: 実行 (val-gate → anchors → af034 p1/p2 の cross-invocation
   resume) の後・outputs (status.log + raw/af034.p1.out + raw/af034.p2.out
   + anchors raw 6 + val-gate .ed-host.out 4) 出版
4. wave D: audit_ed.py 実行結果 (audit_ed.json) + README 最終化 +
   MANIFEST-sha256 刷新 (outputs 込み) 出版
5. wave E: 完了log `research/log/2026-11-25-part-ed-af034-reprobe60m-completion.md`

実行はこの順で行い、各 wave の fetch-back blob sha1 照合 (API
get_file_contents の SHA 冒頭行 vs ローカル git hash-object) を必須とする。
書込み競合・push 競合 (non-FF)・fetch 失敗が生じた場合は無理に押し進めず
状況を記録して本 Part を中断する (hourly 並走あり)。

## 本 Part で行わないこと

- canonical cache / increment / merger / refresh / extractor の実行
  (adoption は将来 Part。Base は `cecc1a0f…` のまま)
- WIN 行の scrutiny・C++ 第二実装 gate の代替実装 (専権尊重)
- 11×11 空盤・class 34908 の勝敗・coverage・secured coverage 主張
- jsreplay・pinned runner のバイナリ/テキスト改変 (BUDGET 行以外
  byte 同一・BUDGET 行は事前宣言のとおり)
