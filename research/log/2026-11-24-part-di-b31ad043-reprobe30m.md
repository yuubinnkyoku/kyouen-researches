# Part DI 完了log (2026-11-24): batch-31 (closure class 5804) last-remaining-EXHAUSTED 1行 ad043 30M再probe — **RESOLVED-WIN (honest label・verdict不消費)**

Part DI (宣言 `b3f068ab`・publish-then-execute・単一オーナー) 完了。
batch-31 (class 5804) のEXHAUSTED最終1行 **ad043** を新条件
**budget 30,000,000** で2-pass fresh-cold再probeした結果、
**result 1 (WIN)・nodes 18,247,029** (p1==p2 node-exact・fresh-cold・
決定的探索・truncated sidecarなし) で解決した。Part CT (batch-28 aa050
30M再probe) と同一設計・同一protocol。**verdict不消費**: 本行は
probe-level honest label。canonical adoption は pinned fail-closed merger
`90711961…` 経由の別adoption Part 専権・WIN行はscrutiny owner C++第二実装
gate `9193f5b6…` 待ち。閉鎖・被覆・secured・root勝敗の主張はしない。

## 集計 (probe-level honest label)

batch-31 (closure class 5804) 55キー: **LOSS 51・WIN 4
(ad024/ad028/ad043/ad055)・EXHAUSTED 0** — 55/55キーがhonest labelを
持つ状態に初到達 (ad043のpublished 15M exhaustion (nodes 15,000,000) は
新条件30Mでの解決により置き換え。同一条件再probeは不実施。
no-same-condition-re-search規約は無傷)。

## 執行記録 (出版chain・全fetch-back検証済み)

1. **宣言** commit `b3f068ab` (observed HEAD `7abca71f`・対抗宣言なし
   直近100コミット機械走査: Part DI/ad043再probe/class 5804継続probeの
   対抗レーン 0件) — fetch-back byte-identical (API resource全文一致)。
2. **A scaffold** commit `a5e32648` (observed HEAD `c9e534f4` = Part CP
   drive-3 checklist1・ac030..ac040・別レーン非接触): kit 28 files
   (scripts 6 + input 5 + sources 8 + val-gate 8 + README 実行記録空欄)。
   cache 262,326Bはpush前chunked-read再構成byte-identical検証
   (sha `04b0a239…`) 後に出版。fetch-back 28/28 remote blob sha一致。
3. **val-gate fresh 4**: 4/4 NODE-EXACT vs published baselines
   (budget 2M×2: result 0・nodes 2,000,000 / 15M×2: result 2・nodes
   3,651,923 / 5,040,200。wall_sは許容差分)。
4. **anchors** (derived 30M runner・end-to-end gate): ad054 result 2・
   nodes 1,644,957 = published値完全一致 (p1==p2)・ad055 result 1・
   nodes 3,364,655 = 同 (WIN-HALT rc=45は事前登録どおり正常)。
5. **target ad043**: `di_local_step.sh` invocation 1 (07:14-07:16Z) で
   p1+p2とも単一invocation内完走 (~102s/pass・260s inner window内)。
   cross-invocation resume設計は不用起動に終わった (honest記録)。
   invocation 2: remaining=0 ALL-DONE。
6. **audit ×3**: byte-identical (audit.json sha `8415f48a…`) PASS
   (probed 1/1・win 1・loss 0・exhausted 0・window-exceeded 0・unprobed 0)。
   **tamper電池 4/4 fail-closed** (scratch copy上・本番output非破壊):
   T1 p2 nodes+1 → p1/p2 mismatch捕捉・T2 WIN→LOSS反転 → 同捕捉・
   T3 replay_done削除 → truncated fragment捕捉・T4 registry budget
   29999999 → A gate捕捉。clean control・restore後再確認とも同一sha。
7. **B outputs** commit `487eacd3` (observed HEAD `a5e32648`): 12 files
   (status.log + raw 6 + audit.json + val-gate `.di-host.out` 4)。
   fetch-back 12/12 blob sha一致。**コミットメッセージの「11 files」は
   誤記 (実際12 files)** — 本logとC段階README実行記録で訂正 (Part CY
   B3計数誤記訂正と同種・内容・件数とも検証済みで実害なし)。
8. **C** commit `6562f244` (observed HEAD `487eacd3`): README最終版
   (実行記録追記) + MANIFEST-sha256 (40 entries・path-sorted)。fetch-back
   2/2 blob sha一致 (README 9,335B・MANIFEST 7,526B)。

## 誠実記録

- maker段階: 宣言草案でad043 input CSV sha転記ミス1件を宣言前機械照合で
  捕捉・修正済み (宣言文記載どおり・未出版段階)。
- B commitメッセージ計数誤記 (11→12 files): 上記のとおり検証済み・訂正記録。
- 環境リセット事故は本Partでは発生せず (truncated sidecar 0件・
  status.log にTRUNCATED-RETRY行なし)。
- 非接触確認: Part CP drive-3 (batch-30・ac系キー・宣言 `3f0aeb55`)・
  Part DH (batch-28 P4・outage記録 `879ae475` 後の再実行待ち)・
  K1284 fast lane・batch-31 reaudit/adoption (merger `90711961…` 別Part
  専権・本Partは代行しない・ad043の30M WIN行もadoption候補としてmergerに
  渡るのみ)。実験dir・対象キー完全分離。

## UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 5804 (55キーすべて・ad043の30M WIN labelを
含む) はこの時点で UNKNOWN のまま。** nodes数 (18,247,029)・wall秒数は
探索打刻であり、勝敗の確定・距離・証明サイズとして読まない。

## 実験dir

`research/experiments/n11-centralreply-closure-class5804-b31ad043-reprobe30m-20261124/`
(MANIFEST-sha256 40 entries・独立検証可能: 全byte-pins + audit script
`72fc4dda…` + registry `6fbf61eb…`)
