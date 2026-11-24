# n11-centralreply-closure-b28cqwin5-thirdimpl-20261124 (Part CX)

Part CX: batch-28 (closure class 5343) Part CQ 20M-reprobe 新解決WINのうち
Part CW未カバーの残5行 (aa005/aa030/aa031/aa047/aa053・全てUNCONSUMED
honest labels) の第三実装交叉検証 (publish-then-execute)。

- 宣言: `research/log/2026-11-24-part-cx-b28cqwin5-thirdimpl-declaration.md`
  (commit `1300c10d`・observed HEAD `1dcd7cc5`・対抗宣言なし機械確認済み)。
- 本READMEはkit scaffold出版時点 (A) の初版。実行 (D1-D7) 後にREADME最終版と
  MANIFEST-sha256.txtをC commitで出版する。

## kit構成 (このA commit)

- `scripts/` 7: make_inputs_cx.py (`7abf48c5…`・宣言済みCW maker適応) /
  audit_cx.py (`87152e94…`・宣言済みCW audit適応) / run_replica_cx.sh
  (`6d05701c…`・published CW runner `8c123b65…`のヘッダcomment diffのみ・
  機能body機械diff照合済み) / run_thirdimpl.sh (`a0b77d83…`・CW版byte-clone) /
  third_impl.js (`08ea958f…`) / verify_tbl.js (`c8c52528…`) /
  jsreplay.js (`84585617…`) — 下3つはpinned byte-clone。
- `sources/` 26: CQ実験 (`n11-centralreply-class5343-b28exhausted-reprobe-20261123`)
  からのcommit-pinned fetch (raw 10: 5キー×p1/p2・published-input 5・
  published-input-bf 4: anchors/negatives) + Part CO 7-LOSS adoption出版物
  (merged canonical cache `854800f3…` 259,886B・6,302行 = 6,301 s5verdict + header /
  increment `bd5ef7d7…` / increments-manifest `b47e07ca…`) + batch-keys-b28.json
  `af19208f…` + status-cq.log `afc48734…` + README-cq.md `e0153971…` +
  log-cq-reprobe.md `be208f9c…`。
- `input/` 10: rows.json (`3a87c5b6…`・maker 2回実行byte-stable) + 5対象 +
  anchors k02a/l1a + negatives ng1/ng2 のinput CSV (publishedとbyte一致)。
- `val-gate/` 8: at2m×2 + first-15m/second-15m published baselines + inputs
  (CWから不変再利用・host出力は `.cx-host.out` として生成)。

## 目標と主張の限定

- 5行の第三実装verdict一致と本host pinned-replica 2-pass node-exact再現は
  **three-implementation corroboration** (jsreplay runner×2系 + 第三実装) の
  証拠であり、採用ではない。verdict不消費: aa005/aa030/aa031/aa047/aa053は
  honest labelのまま・adoptionは scrutiny owner C++第二実装 gate `9193f5b6…`
  を経て別adoption Part (pinned merger `90711961…` 経由) のみ。
- 閉鎖・被覆・secured・root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・class 5343・全キーはこの時点で
  UNKNOWN**。nodes数・expansions数・ttHits数を勝敗として読まない。
