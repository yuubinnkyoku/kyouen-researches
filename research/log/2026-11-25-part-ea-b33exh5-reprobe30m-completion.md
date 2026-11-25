# Part EA 完了log (2026-11-25): batch-33 (closure class 34908) remaining-EXHAUSTED 5行 (af003/af023/af034/af039/af048) higher-budget 30M reprobe — drive完走 5/5・MISMATCH 0・verno不消費・11×11 UNKNOWN担保不変

Part EA 宣言
`research/log/2026-11-25-part-ea-b33exh5-reprobe30m-declaration.md`
(commit `a280180d`) の publish-then-execute 執行フェーズ (手順3–8) を本実行で
完走した。実験dir:
`research/experiments/n11-centralreply-closure-class34908-b33exh5-reprobe30m-20261125/`。
Part CT/DI 先行例と同一設計・同一pinned機体 (jsreplay `84585617…` /
runner 30M `3b5083b4…` / maker `97b28dd4…` / step `0e210e90…` /
audit `452cd817…`)。

## 結果 (honest label・verdict不消費)

batch-33 の 15M条件 EXHAUSTED 5行を新条件 budget 30,000,000 で 2-pass
fresh-cold reprobe (全行 pass pair node-exact・MISMATCH 0・WINDOW-EXCEEDED 0):

| key | s5 | 30M結果 | nodes/pass | 備考 |
|-----|-----|---------|-----------|------|
| af003 | 153030 | **LOSS** | 23,126,072 | honest label・adoption候補 (別Part) |
| af023 | 810351 | **WIN** | 28,933,179 | honest label・verdict不消費・C++ gate `9193f5b6…` 待ち |
| af034 | 514726 | **EXHAUSTED @30M** | 30,000,000 | 30M条件でもhonest UNKNOWN (同一条件再probeなし) |
| af039 | 2621520 | **LOSS** | 19,234,232 | honest label・adoption候補 (別Part) |
| af048 | 265799 | **WIN** | 17,816,616 | honest label・verdict不消費・C++ gate `9193f5b6…` 待ち |

- targets合計 nodes 119,110,099/pass。anchors: af001 LOSS nodes 2,952,432 /
  af029 WIN nodes 4,862,485 — ともに published 15M値と node-exact
  (30M budget flagで再実行・search determinism gate PASS)。
- batch-33 (class 34908) 54キー全体の15M-era集計 (LOSS 45・WIN 4・EXH 5) は
  本30M再probeで EXH 5行のうち2行LOSS・2行WIN・1行EXH(@30M) という
  honest label bookkeeping に変化したのみ。**閉鎖・被覆・secured coverage・
  root勝敗の主張は一切しない (class 34908 は UNKNOWNのまま・採用は未実施)。**

## 実行経過 (protocol順・全fetch-back byte検証)

1. 宣言 `a280180d` (observed HEAD `04c132fd`) → kit scaffold A1–A3b
   (`59588a30` / `369b8d18` / `bd6616c5` / `04c132fd`)。
2. **B1-fix (honest deviation・commit `f9420860`)**: fetch-back で A3a
   (`bd6616c5`) の sources/ 15ファイル (b33-status.log + exh15m×10 +
   anchor-15m×4) が **push時 mojibake** (b33-status.log 実測 `1b5d96a9` ≠
   pin `1f663fc8`、raws全pin不一致) と判明。published batch-33 正本
   (commit `72877473` 出版物) から再取得し全15ファイル pin 一致を確認のうえ
   byte-exact修復出版 (API git blob sha1 15/15 厳密一致で検証)。修復kit上で
   maker G1–G7 全PASS・`reprobe-keys.json` 再生成 `3744b522` byte-identical・
   maker tamper battery 4/4 fail-closed (T1/T2/T3/T4) を再実行した。
   A1/A2/A3b の他ファイル (scripts 6・input 9・val-gate 8・canonical cache
   `4a30b88d…`) は初回から全pin一致 (無傷)。DU-b「ASCII簡易デコーダ由来
   mojibake → B1-fix」と同一ska本の事故で、fail-closed pin が publishes-side
   崩壊も捕捉した最初の事例。
3. val-gate fresh 4/4 node-exact (`.ea-host.out`): at2m×2 (budget 2M →
   result 0 nodes 2,000,000・wall 9/9s)・first-15m (budget 15M → result 2
   nodes 3,651,923・17s)・second-15m (budget 15M → result 2 nodes 5,040,200・
   25s)。published baselines と完全一致。
4. anchors: af001 (LOSS 2,952,432・13/13s) → af029 (WIN 4,862,485・23/23s・
   PASS + WIN-HALT・runner rc=45 設計通り)。published値と node-exact。
5. targets (`ea_local_step.sh` cross-invocation resume・2-pass fresh-cold
   @30M): af003 LOSS 23,126,072 (126/129s) → af023 WIN 28,933,179
   (155/157s・p2が260s窓で切れ sidecar `af023.p2.truncated.024331.out` +
   P2-TRUNCATED-RETRY 1回 → 次invocation完走・resume設計実働) → af034
   EXHAUSTED@30M 30,000,000 (163/165s・sidecar
   `af034.p2.truncated.025034.out` + retry 1回 → 完走) → af039 LOSS
   19,234,232 (105/105s) → af048 WIN 17,816,616 (97/89s)。
   MISMATCH 0・WINDOW-EXCEEDED 0・UNPROBED 0。当host実測 ~222k nodes/s
   (2M val-gate 9s・30M pass ~135s)。
6. audit (`audit_ea.py`) ×3 byte-identical 全PASS (audit.json `5b83d166…`):
   probed 5/5・win 2・loss 2・exhausted@30M 1・window-exceeded 0・
   anchors 2・val-gate 4・mismatches 0。audit tamper電池 (scratch copy上):
   TA raw nodes改変 (af003 …072→…073) → GATE FAILED (p1/p2 row mismatch)・
   TB af023 WIN-HALT行除去 → GATE FAILED・TD val-gate fresh行改変 → GATE
   FAILED・明control 2回 PASS (本番output byte不変 `5b83d166`)。観察:
   status.log片側only改変 (raw SSOT無傷) は設計上gate対象外
   (raw行がSSOT・status行はcorroboration)。
7. outputs push `b63569ab` (status.log `db7c7017` 13行 + raw 14 + truncated
   sidecar 2 + val-gate `.ea-host.out` 4 + audit.json) — fetch-back API git
   blob sha1 22/22 厳密一致。README最終 + MANIFEST-sha256 (61 entries・
   sha256+git-blob-sha1+path・README/MANIFEST self-excluded) push
   `89bd7036` — fetch-back blob sha1 2/2 一致。

## verdict不消費・UNKNOWN担保 (再掲)

- WIN/LOSS/EXHAUSTED は全て honest label。canonical adoption は pinned
  fail-closed merger `90711961…` 経由の別adoption Part 専権 (af003/af039 の
  2 LOSS行は次回adoption Partの候補)。WIN行 (af023/af048) は scrutiny
  owner C++第二実装 gate `9193f5b6…` 通過まで採用されない。
- af034 は 30M条件でも honest UNKNOWN (同一条件再probeはしない・さらなる
  高budget/窓設計は別Partの対象)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 34908 (54キーすべて・本実験の結果行を
  含む) は本Partの実行・出版のどの時点でも UNKNOWN**。nodes数・wall秒数を
  勝敗や距離として読まない。

## 次回レジューム (着手前に必ず最新main再取得・hourly並走注意)

- (a) batch-33系: 15M-era集計の EXH 5行は本Partで全行honest label確定
  (af034のみ30M EXH継続・honest UNKNOWN)。**af003/af039 の2 LOSS行 +
  af023/af048 の2 WIN行の正味の採用判定は別adoption Part の専権**
  (WIN 2行はC++ gate待ち・adoption Part では採用対象外が濃厚)。
- (b) closure表 (807行・Part EB reaudit `3a8059aa` 時点) の rank上位
  (23101/1849/2251/16371/16757/5804/20421/34269/5343) は不変のまま本Partの
  影響を受けていない (本Partはadoptionを行っていないため・class 34908 の
  rank/unknown構成の変化は次回adoption Partでのreaudit refresh後に機械導出
  される)。af034 の高budget再probe (例: budget 60M・窓設計変更) は別宣言
  必須。
- (c) kit sources/ の A3a mojibake 事故の再発防止: 本レーンのpush経路は
  「file_system.read_file → push_files 直接content渡し」(EB実績ルート・
  今回B1-fix/outputs/READMEも全blob sha一致) に限定し、b64経路は使わない。
- (d) **標準11×11空盤・二石root・S2・class 1/2/4・class 34908 は全時点で
  UNKNOWNのまま。本Partのnodes数を勝敗や距離として読まない。**
