# Part ED age修正 (amendment): af034 本probeのオーケストレーション修正 (2026-11-25)

単一オーナー Part ED の執行時 honest 修正記録。本修正は af034 本probe 実行
**前**に出版する (val-gate 4/4 と anchors 3/3 の実行と可干渉なし・本probe
は未実行)。ega宣言
`research/log/2026-11-25-part-ed-af034-reprobe60m-declaration.md` (commit
`8cc8ed0c`) からの変更点はこの1点のみで、対象キー・予算条件 (60M)・
two-pass fresh-cold node-exact・honest label 規約・kit bytes・anchor/val-gate
中身は一切不変。

## 事実 (機械観測)

- anchor 実行の wall 計測 (本host): af001 2-pass (5,904,864 nodes / 約28s),
  af029 2-pass (9,724,970 / 約48s)・af039 2-pass (38,468,464 / 約218s)。
  sustained rate は 約176k-227k nodes/s で変動し、60M 1 pass は
  **約265-341s** と推定される。
- 宣言の当初設計は「290s inner window に 1 pass」を仮定していた (af001
  pre-measurement 227k nodes/s から 60M ≈ 265s と参された)。sustained
  rate が低下した場合 60M pass が単一 invocation window (最大300s) を
  超える可能性が実測で判明した。
- 環境の detached プロセスは invocation 境界を生存する (canary 検証
  2026-11-25T05:11:47Z 起動 → 05:12:12Z 別 invocation で出力確認済み)。

## 修正内容 (オーケストレーションのみ)

- af034 本 probe の実行は、publish 済み runner
  `scripts/runbatch_af034-60m.sh` (byte 不変 `b0c5f714…`) を
  **detached (nohup + disown)** で起動し、複数 invocation にわたり
  完了を監視する。runner は p1 → p2 を同一プロセス内で順に実行する
  (published runner の file-existence + truncated-sidecar guard が
  停止・kill に際しても誤採用を防止する: `# replay_done` の無い
  pass は証拠にならず fresh-cold 再実行される)。
- 環境 reset で detached プロセスが kill された場合も truncated
  sidecar + P1/P2-TRUNCATED-RETRY が作用し、再起動時に fresh-cold
  で再実行される (同一 15M/30M 条件の再probe禁止には抵触しない:
  未完了 pass は一度も verdict を生んでいない)。
- **WINDOW-EXCEEDED 規約の再解釈 (honest)**: 従来は「同一 pass で
  TRUNCATED-RETRY 2回 → 当該 host window に収まらないので skip」
  だった。本修正後は「detached 再起動を含め同一 pass の TRUNCATED-RETRY
  2回以降も再実行は可能だが、各試行が依然 window を跨いで生き残る
  証拠が取れない場合」に honest unresolved として記録する。実行の
  事実 (試行回数・wall・環境killの有無) は status.log と完了log に
  そのまま残す。
- BUDGET = 60,000,000・two-pass node-exact・EXH なら nodes==60,000,000
  検証・LOSS なら nodes>30,000,000 検証・WIN なら WIN-HALT (verdict
  不消費) は全部不変。

## 影響を受ける出版物

- なし (kit bytes 不変・status.log は本 probe 実行の fact を追記する
  だけ)。本 amendment は宣言 commit `8cc8ed0c` に対する執行時の
  honest 記録であり、宣言の予算条件・honest label を変更しない。

- 11×11 空盤・class 34908 は引き続き UNKNOWN。本 probe の結果如何に
  よらず verdict は本 Part では消費されない。
