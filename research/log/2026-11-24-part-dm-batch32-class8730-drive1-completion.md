# Part DM completion (2026-11-24): batch-32 (class 8730) drive-1 ALL-DONE — 54/54キー probe-complete・全行 honest-label result=2 (LOSS)

Part DM (宣言 `88b7fc90` 10:59:34Z・publish-then-execute・単一オーナー
n11中央応答長期レーン)。本logは drive-1 の完了記録。**verdict不消費。**

## 1. 結果

- **status.log 54行・すべて PASS・honest-label result=2 (LOSS)。**
  WIN 0・EXHAUSTED 0・TRUNCATED 0・MISMATCH 0。108 raw出力 (54キー×p1/p2)
  すべて `# replay_done` 完備・p1/p2 の `replay,` 行 f1-8 完全一致
  (budget 15M・2-pass fresh-cold)。
- nodes合計 **223,769,637/pass** (2-pass node-exact 計447,539,274
  expansions)。最小 1,706,977 (ae042)・最大 8,966,840 (ae034)・平均 4,143,882。
  nodes数は勝敗ではなく計測値。
- status.log時刻窓 2026-11-24T13:34:29Z (ae002・host2) .. 14:48:51Z (ae054・host4)。

## 2. 実行・出版 chain (全published・fetch-back検証は各commit時点)

- 宣言 `88b7fc90` (10:59) → scaffold `8d852732` (11:01) → host val-gate
  `.b32-host.out` `6bcbbc95` (11:04)【宣言hostはここでsession終了・54キー
  UNPROBED】
- interim note (host2 resume) `5ff7e53a` (13:22) → drive-1 wave1 (ae001..ae008) →
  **increment 1** `1e1578a2` (13:40・raw 16 + status 8行 + host2 sidecar 4)
  【host2 session終了】
- interim 2 note (host3 resume) `c4fb42eb` (13:47) → increments 2-3
  (ae009..ae018 `37f51283` / ae019..ae034 `9c8cd171`・status 18→34行・
  host3 sidecar 4) → **外側timeout (300s cap) による実行環境reset**
  (未出版の ae035..ae046 PASS 12行ローカル成果が破棄・UNPROBEDに戻る)
- interim 3 note (honest事故開示 + host4 resume) `25f71289` (14:29・kitを
  pin `9c8cd171` から再建・MANIFEST 68/68・host4 val-gate `.b32-host4.out`
  4/4 node-exact sidecar同時出版) → increments 4-5
  (ae035..ae046 `4b5c4b73`・**破棄前host3計算値と同一nodes 12/12再現** /
  ae047..ae054 + status 54行【本commit】) → README結果section更新 +
  MANIFEST-sha256 (194行: 68 kit + 108 raw + status.log + sidecar 16) +
  本完了log【同commit】。
- **決定性補足**: host3/host4を跨ぐ ae035..ae046 12キーの nodes完全一致
  (各キー nodes 3,205,767〜8,966,840・12/12) は、2-pass (同一host内) に
  加えてhost間での
  追加の CROSS-HOST determinism 検証となった (未出版破棄値はevidenceで
  ないが、再現一致自体はhonest観測記録)。

## 3. class 8730 上の意味 (主張の範囲)

- rank 30 class 8730 (closure表・cost 58子) の54 unknown cost children
  (s5 30596..311727・batch-keys.json `f46e663f…`) の probe-level label
  は**すべて LOSS** になった (honest label・verdict不消費)。既知の4子
  (s5 144458/212464/310606/311726 = base内 LOSS(2)) と合わせて cost 58子
  の label が揃った。
- **canonical adoption は別adoption Part の専権** (pinned fail-closed
  merger `90711961…` 経由・b32loss54 枠)。閉鎖・被覆・secured・root勝敗・
  groups_free変動はadoption後のreauditが機械導出する。closure table上の
  unknown_now 54減算もadoption後の正本反映。
- 本batchにWIN行・EXHAUSTED行が存在しないため、scrutiny owner C++第二実装
  gate (`9193f5b6…`) を要する行は本batchにはない。

## 4. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 5804・class 8730 (本batch-32の54キーすべて・
LOSS label行を含む) は本driveの実行・出版のどの時点でもUNKNOWNのまま。**
nodes数・wall秒数を勝敗や距離として読まない。被覆・secured・root勝敗の
主張をしない。
