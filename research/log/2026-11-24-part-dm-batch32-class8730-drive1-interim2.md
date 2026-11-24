# Part DM interim note 2 (2026-11-24): batch-32 drive-1 resume (3rd host, same owner lane)

- 単一オーナー継続: Part DM 宣言 (commit `88b7fc90`, 2026-11-24T10:59:34Z) は
  n11中央応答長期レーンによるもの。本noteは同レーンの後継 hourly session
  (第3host) による **同Partの継続実行** の記録であり、新規Part宣言でも
  takeover宣言でもない (対抗/takeoverは不使用・先行対抗出版物なし)。
- 状況 (honest): 宣言host (scaffold `8d852732`・val-gate host 4/4
  `6bcbbc95`) の後、第2host (interim `5ff7e53a`・`.b32-host2.out`
  val-gate 4/4) が drive-1 wave 1 を実行し **increment 1**
  (`1e1578a2`, 13:40:09Z・ae001..ae008 p1/p2 16ファイル + status.log
  8行 + host2 sidecar 4ファイル) を出版して session終了。
  **ae009..ae054の46キーは fileless UNPROBED のまま**。
- 本hostでの再建: kitをcommit pin `1e1578a2` で raw fetch
  (scripts 4 sha pin一致 `e43f5f83`/`84585617`/`2ddf4903`/`f591f8c2`・
  MANIFEST-sha256 (68 entries) 全件 sha256 byte一致で復元・
  ae001..ae008 raw 16ファイル `# replay_done` 16/16確認・status.log 8行
  byte一致)。drive済みキーの再実行は行わない (pinned runnerは既存
  complete pass fileをskip)。
- 本host val-gate fresh 4/4 node-exact 実施後に drive-1 を開始する
  (sidecar接尾 `.b32-host3.out`・published baselines
  (at2m1/at2m2/first-15m/second-15m) と wall_s 以外全 field一致を
  4/4で要件とする。不一致なら hard-stop し成果は出版しない)。
  sidecar 4ファイルはdrive成果物とともに出版する。
- pinned session script `drive1_local_step_b32.sh` (`e43f5f83…`)・
  pinned runner `runbatch.sh` (`f591f8c2…`)・pinned solver
  `jsreplay.js` (`84585617…`)・pre-registered stop rules 不変
  (WIN rc=45 / MISMATCH rc=42 / p1/p2 fail rc=43/44 / budget 15M・
  2-pass fresh-cold・WIN-HALT 2行distinctでwave halt・EXHAUSTEDは継続)。
- 成果は部分完了でも honest に随時出版する (誠実打ち切り時は成果分のみ・
  未probeキーは fileless UNPROBED のまま次回driveに委ねる・宣言規約どおり)。
  observed HEAD `3a62c705` (2026-11-24T13:45:05Z・K1290 fast laneの
  publicationと非接触)。
- **verdict不消費。標準11×11空盤・19 central-reply roots・二石root・S2・
  class 5804・class 8730 (本batch 54キーすべて・WIN/LOSS/EXHAUSTED行を
  含む) はどの時点でもUNKNOWNのまま。** nodes数・wall秒数を勝敗や距離として
  読まない。WIN採用は scrutiny owner C++第二実装 gate (`9193f5b6…`)
  通過後の別adoption Part (pinned merger `90711961…` 経由) のみ。
