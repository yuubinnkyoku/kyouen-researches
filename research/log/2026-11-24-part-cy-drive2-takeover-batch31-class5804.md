# Part CY drive-2 takeover宣言 (2026-11-24): batch-31 (closure class 5804) drive-2 残27キー ad029..ad055 — WIN-CONTINUE・publish-then-execute

単一オーナーtakeover宣言 (Part CX `c48aa56b` / Part DA `f2b36862` と同一規約)。
observed HEAD は出版時点でpush直前に再取得し commit message に記載。

## takeover 事由の機械確認

- 原宣言: `21fef631` (Part CY drive-2 単一オーナー宣言・
  2026-11-24T02:10:13Z・`research/log/2026-11-24-part-cy-batch31-class5804-drive2-declaration.md`):
  drive-1 WIN-HALT により未probeの残27キー ad029..ad055 を WIN-CONTINUE
  設計で 2-pass fresh-cold (budget 15M) probeするもの。
- 原sessionの進行: drive-2 val-gate fresh 4 (published `.d2-host.out`・
  `68f80a85`・02:11:39Z) → drive-2 wave開始 → 02:16Z ad033/ad034 dispatch中に
  インフラ障害 (zombie-race) → **incident amendment `7ff09bb8`**
  (02:20:27Z・診断 + `drive2b_local_step.sh` 事前登録・ad033/ad034 honest label
  LOSS(2) 3-pass一致の記録) — 以降、実験dir
  `research/experiments/n11-centralreply-closure-class5804-batch31-20261124/`
  への commitは**皆無** (amendmentから丸4時間超停滞)。
- **原sessionの drive-2 wave成果 (ad029..ad034分の raw p1/p2・status行) は
  一切出版されていない** (observed 時点の published `output/` は drive-1分
  のみ: raw/ ad001..ad028 + status.log 30行 (1,502B))。よってtakeoverは
  published 状態から ad029..ad055 全27キーを fresh-cold に再probeする
  (原sessionのローカル進行はevidenceでないため最初からやり直し。
  ad033/ad034 は amendment診断 (LOSS・3-pass一致) が published evidence
  であり、takeoverの fresh 2-pass は独立追試として両立する)。
- earliest_takeover = 原宣言 02:10:13Z + 3.5h = 2026-11-24T05:40:13Z を通過。
  規約時刻以降の直近commit列を機械走査し、(a) 本実験dirへの新commit・
  (b) batch-31 drive-2 / class 5804 継続probe・これらのtakeoverを宣言した
  対抗レーン、のいずれも存在しないことを確認。
- takeover実行者は原宣言sessionとは別の長期レーン定期実行 (Part DA takeover
  `f2b36862` 完了直後に着手・DA実験dir・batch-29キーとは完全分離)。

## kit復元とpin検証 (takeover着手時に実施・solver実行は宣言後)

published bytesから復元し、sha256照合:

- 宣言pin一致: runbatch.sh `f591f8c2…`・jsreplay.js `84585617…`・
  drive1_local_step.sh (参考)・drive2_local_step.sh `8baf929b…`・
  **drive2b_local_step.sh `4fcb5775…`** (amendment事前登録版・本takeoverの
  step script)・make_batch31_keys.py `2681c841…`・
  input/batch-keys.json `d058fddc…` (55キー ad001..ad055)。
- input CSV 55件・val-gate (input/baseline/.b31-host.out/.d2-host.out 16件)
  fetch完了・published `.d2-host.out` 4/4 が baselines と node-exact
  (budget/result/nodes・wall_s以外) であることを本host側で再機械確認済み
  (原sessionの出版済み val-gate evidence は破棄せずそのまま引用)。
- published status.log (30行・drive-1分) が drive-2 の append-only base。

## 継承protocol (原宣言 + amendment から変更なし・再掲)

- step: `timeout 290 bash scripts/drive2b_local_step.sh` 反復
  (1 invocation最大2キー×2 worker・`timeout 260` 内側ガード)。
- WIN-CONTINUE: WIN (result 1) が出ても停止せず27キー続行 (runner は正規の
  WIN-HALT status lineをappendするのみ・labelとして読む)。
- MISMATCH: genuine (p1・p2 両fieldに値) の場合は即時 hard-stop (rc=42)。
  artifact (p2 field空) 行はappend-only記録として扱う (amendment規約)。
- EXHAUSTED (result 0): honest UNKNOWN・続行 (同一条件での再probeはしない)。
- 27キーすべてが PASS/EXHAUSTED で終了 (ALL-DONE) または誠実打ち切り。
- 本takeover host でも val-gate fresh 4 を実施し `.tk-host.out` として出版
  (原session分 `.d2-host.out` と併存・takeover hostの独立再現)。
- 出版: B1 outputs (output/raw/ ad029..ad055 p1/p2 + sidecar + status.log
  (drive-1 30行 + drive-2分) + val-gate `.tk-host.out` 4) → C README drive-2
  節追記 + MANIFEST-sha256 更新 → 完了log。全push直前に最新main再取得・
  競合時は無理押しせず記録して次回へ。

## verdict不消費・UNKNOWN担保 (原宣言・amendmentの担保を全部継承)

- WIN/LOSS/EXHAUSTED は honest label (verdict不消費)。canonical adoption は
  pinned fail-closed merger `90711961…` 経由の別adoption Part 専権。
  WIN行scrutiny は C++第二実装 gate `9193f5b6…` 専権。閉鎖・被覆・secured・
  root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 5804 (55キーすべて) は本takeoverの実行・
  出版のどの時点でもUNKNOWNのまま。nodes数・wall秒数を勝敗や距離として
  読まない。**
- 非接触: Part DF/DG (batch-28 P2/P3・aa*キー)・Part DA takeover 完了済み
  (`b5a7ce1a`・b29d2loss15)・queue registry (batch-28 WIN46)・K1278-K1282
  (fast lane)・batch-30レーン (class 34269) は対象キー・実験dir完全分離。
