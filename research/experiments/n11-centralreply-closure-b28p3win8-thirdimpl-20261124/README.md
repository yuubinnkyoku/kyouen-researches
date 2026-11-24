# n11-centralreply-closure-b28p3win8-thirdimpl-20261124 (Part DG)

Part DG: batch-28 (closure class 5343) b28-win46 third-impl queue registry
(REVISION 3) P3パッケージ8行 (aa052/aa044/aa041/aa048/aa026/aa039/aa043/
aa045・drive-4/5 15M-probe solved WIN・全てUNCONSUMED honest labels) の
第三実装交叉検証 (publish-then-execute)。

- 宣言: `research/log/2026-11-24-part-dg-b28p3win8-thirdimpl-declaration.md`
  (commit `e05d73fd`・observed HEAD `26fc5352`・対抗宣言なし機械確認済み・
  maker gates PASS byte-stable ×2 + tamper 8/8事前実行済み・
  本レーンのP2 kitは未出版のまま破棄しP3へpivotした経緯を宣言に誠実記録)。
- 本READMEはkit scaffold出版時点 (A1/A2) の初版。実行 (D1-D8) 後にREADME最終版と
  MANIFEST-sha256.txtをC commitで出版する。

## kit構成 (A1+A2 commits)

- `scripts/` 7: make_inputs_dg.py (`d3fefbca…`・宣言済みDE maker適応系譜・
  registry rev3 pin修正 `334f6209…` は宣言記載) / audit_dg.py
  (`e3a1c74f…`・宣言済み DE `a57e220c` / DF `76934660` 同一G-gate系譜適応・
  target 8キー・P3-package文言・PIN_RAW_DG 16 pin・`.dg-host.out` suffix) /
  run_replica_dg.sh (`de1d1fbc…`・published DE runner `3e4263cc…`のヘッダcommentのみ
  書換・body byte不変・budget 15M不変) / run_thirdimpl.sh (`a0b77d83…`・CW版
  byte-clone) / third_impl.js (`08ea958f…`) / verify_tbl.js (`c8c52528…`) /
  jsreplay.js (`84585617…`) — 下3つはpinned byte-clone。
- `sources/` 39: drive-4/5実験
  (`n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123`) からの
  commit-pinned fetch (raw 16: 8キー×p1/p2・決定ドライブ側正本・aa026はdrive-4・
  残り7キーはdrive-5 / published-input 8・published-input-bf 4) +
  status-drive4.log `59817444…` (61行) + status-drive5.log `ca1e98cc…` (109行) +
  batch-keys-b28.json `af19208f…` + queue-registry.json (rev3) `334f6209…` +
  README-queue.md (rev3) `4b20c6a0…` + Part CO 7-LOSS adoption出版物 (merged
  canonical cache `854800f3…` 6,301行 / increment `bd5ef7d7…` (7行) /
  increments-manifest `b47e07ca…`) + Part DB 37-LOSS re-adoption出版物
  (merged canonical cache `04b0a239…` 6,354行・現canonical chain head /
  increment `85bd4469…` (37行) / increments-manifest `1b51f30d…`)。
- `input/` 13: rows.json (`22de9dd7…`・maker 2回実行byte-stable) + 8対象 +
  anchors k02a/l1a + negatives ng1/ng2 のinput CSV (publishedとbyte一致)。
- `val-gate/` 8: at2m×2 + first-15m/second-15m published baselines + inputs
  (CWから不変再利用・**本PartはA1 commitでkit内に出版しself-contained**・
  host出力は `.dg-host.out` として生成)。

## 対象8行 (published・全てUNCONSUMED)

| key | key (lo,hi) | s5 | legal | verdict | nodes | 決定drive |
| --- | --- | --- | --- | --- | --- | --- |
| aa052 | 1152921504606851072,4228 | 199737 | 93 | WIN | 8,976,982 | drive-5 |
| aa044 | 1152921521786716160,4228 | 199729 | 86 | WIN | 9,219,778 | drive-5 |
| aa041 | 1171516445255794688,8 | 199726 | 93 | WIN | 10,283,599 | drive-5 |
| aa048 | 1152921504615235584,4228 | 199733 | 87 | WIN | 10,553,343 | drive-5 |
| aa026 | 1171516445255794688,32 | 199711 | 88 | WIN | 11,019,409 | drive-4 (両log一致) |
| aa039 | 1152921504606846984,4228 | 199724 | 88 | WIN | 11,349,776 | drive-5 |
| aa043 | 1152921513196781568,4228 | 199728 | 90 | WIN | 12,069,965 | drive-5 |
| aa045 | 1152921642045800448,4228 | 199730 | 84 | WIN | 12,371,943 | drive-5 |

## 目標と主張の限定

- 8行の第三実装verdict一致と本host pinned-replica 2-pass node-exact再現は
  **three-implementation corroboration** (jsreplay runner×2系 + 第三実装) の
  証拠であり、採用ではない。verdict不消費: 対象8行はhonest labelのまま・
  adoptionは scrutiny owner C++第二実装 gate `9193f5b6…` を経て別adoption Part
  (pinned merger `90711961…` 経由) のみ。
- 閉鎖・被覆・secured・root勝敗の主張をしない。
- **標準11×11空盤・19 central-reply roots・class 5343・全キー (対象8キー含む) は
  この時点でUNKNOWN**。nodes数・expansions数・ttHits数を勝敗や距離として
  読まない。
