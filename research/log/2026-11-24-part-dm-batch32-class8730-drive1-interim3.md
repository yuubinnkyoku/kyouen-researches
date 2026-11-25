# Part DM interim note 3 (2026-11-24): drive-1 host3 environment reset — unpublished local work discarded, resume by 4th host

- 事故 (honest): 3rd host (interim 2 note `c4fb42eb`・val-gate host3 4/4 node-exact
  (sidecar `.b32-host3.out` 4ファイル increment 2 `37f51283` で出版済み)) は
  drive-1 を再開し **increment 2 (ae009..ae018, `37f51283`)** と
  **increment 3 (ae019..ae034, `9c8cd171`)** を出版した後、
  bash呼び出しの外側timeout (300s cap) で実行環境reset。
  **未出版のローカル成果 (ae035..ae046の12キーPASS honest-label result=2
  2-pass分・status.log 34行を超える追記分・host3側で一部再計算中だった分)
  はすべて破棄された** (Part DC 00:00Z頃の事故と同型)。
- 正本の状態: published status.log は34行 (ae001..ae034)・output/raw 68ファイル
  (34キー × p1/p2) すべて `# replay_done` 完備・remotesは increment 3
  (`9c8cd171`) まで。破棄された12キー (ae035..ae046) は出版されていないため
  **fileless UNPROBED に戻る** (protocol式どおり・矛盾なし)。
- 本host (4th) での再建: kitをcommit pin `9c8cd171` で raw fetch
  (MANIFEST-sha256 68/68 byte一致・scripts 4 sha pin一致・raw 68
  `replay_done` 68/68・status.log 34行 byte一致)。
- 本host val-gate fresh 4/4 node-exact 成立 (sidecar接尾
  `.b32-host4.out`・published baselinesと wall_s 以外全 field一致 4/4)。
  sidecar 4ファイルは本noteとともに出版する。
- これより drive-1 を **ae035から** 再開する (pinned session script
  `e43f5f83…`・pinned runner `f591f8c2…`・pinned solver `84585617…`・
  pre-registered stop rules 不変・WIN-HALT 2行distinct・EXHAUSTED継続)。
  bash呼び出しは2 invocation/call以下に縮小し再発防止を図る
  (worker inner `timeout 260` が外側 cap に触れないように)。
- **verdict不消費。標準11×11空盤・19 central-reply roots・二石root・S2・
  class 5804・class 8730 (本batch 54キーすべて) はどの時点でもUNKNOWNのまま。**
  nodes数・wall秒数を勝敗や距離として読まない。WIN採用は scrutiny owner
  C++第二実装 gate (`9193f5b6…`) 通過後の別adoption Part
  (pinned merger `90711961…` 経由) のみ。
