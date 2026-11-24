# n11-centralreply-closure-b28cqwin5-thirdimpl-20261124 (Part CX)

Part CX: batch-28 (closure class 5343) Part CQ 20M-reprobe 新解決WINのうち
Part CW未カバーの残5行 (aa005/aa030/aa031/aa047/aa053・全てUNCONSUMED
honest labels) の第三実装交叉検証 (publish-then-execute)。

- 原宣言: `research/log/2026-11-24-part-cx-b28cqwin5-thirdimpl-declaration.md`
  (commit `1300c10d`・observed HEAD `1dcd7cc5`・対抗宣言なし機械確認済み)。
- takeover宣言: `research/log/2026-11-24-part-cx-b28cqwin5-thirdimpl-takeover.md`
  (commit `c48aa56b`・2026-11-24T04:19:31Z earliest_takeover後・原宣言から3.5h超の
  停滞 (cx dir最終commit `3185a672` のまま・output/無し・CX進捗log無し)・
  対抗takeover宣言なしを機械確認の上での単一オーナーtakeover。observed HEAD
  before-push `10b8e96d`)。継承: 原宣言の全pin・protocol D1-D8・stop rules・
  主張の限定をbyte不変でそのまま実行。

## kit構成 (A commit `3185a672`・takeover時に復元・sha256照合済み)

- `scripts/` 7: make_inputs_cx.py (`7abf48c5…`) / audit_cx.py (`87152e94…`・
  REPLICA_BUDGET=20000000・negativeはtag "a"読み・val-gate hostは`.cx-host.out`) /
  run_replica_cx.sh (`6d05701c…`) / run_thirdimpl.sh (`a0b77d83…`) /
  third_impl.js (`08ea958f…`) / verify_tbl.js (`c8c52528…`) / jsreplay.js
  (`84585617…`) — 全てpublished pinとbyte一致。
- `sources/` 26: CQ実験からのcommit-pinned fetch (raw 10・published-input 5・
  published-input-bf 4) + Part CO出版物 (merged canonical cache `854800f3…`
  6,301行 / increment / increments-manifest) + batch-keys-b28.json / status-cq.log /
  README-cq.md / log-cq-reprobe.md。
- `input/` 10: rows.json (`3a87c5b6…`) + 5対象 + anchors k02a/l1a + negatives ng1/ng2。
- `val-gate/` 8: at2m×2 + first-15m/second-15m published baselines + inputs。

## 実行結果 (takeover実行・2026-11-24D8完了)

全protocol green。終了時点で **11×11空盤・class 5343・対象5キーはすべてUNKNOWN
のまま (verdict不消費)**。

- D1 rules gate: `output/rules-gate.txt` — replica quads 95,670 = mine quads、
  triples checked 195,044 **mismatches 0** (rc=0)。
- D2 val-gate this-host fresh 4/4: budget 2M/2M/15M/15M・published baselinesと
  node-exact (audit G7比較式: replay fields (1-7,9,10)完全一致・wall_sはcomment
  行のみ相違)。ttHits (field index 8) はpublished baseline对此-host runで
  揮らぎ (8→9・17→18の2/4本) を観測したが、pinned auditの比較対象外
  (設計どおり)。host出力は `val-gate/*.cx-host.out` 4本出版。
- D3 negatives 2/2: ng1/ng2 とも tag "a" で設計どおり **GATE_FAIL** (rc=1)・
  文言完全一致 (ng1: `legal count mismatch: derived=87 declared=88` /
  ng2: `stone count mismatch: bits=5 declared=6`)。
- D4 anchors: k02a exp **9,106,337** ttH **4,991,527** / l1a exp **7,660,202**
  ttH **3,951,175** — いずれも det-pair a==b・published pins node-exact。
- D5 pinned-replica 10/10: 5キー×p1/p2 全pass fresh-cold budget 20M rc=0・
  p1==p2 nodes完全一致・published raw行とnode-exact (ttHits除く全gate fields):
  aa005 **15,957,877** / aa030 **16,765,560** / aa031 **17,185,014** /
  aa047 **16,230,465** / aa053 **16,685,872** (legal 89/90/92/92/95)。
  result=1 (WIN honest label)・満了budget消費で終了 (inconclusive=0)。
- D6 第三実装 targets 10/10: 5キー×a/b 全run clean (rc=0)・det-pair a==b
  10/10 (expansions/ttHits完全一致)・verdict **5/5 result=1 = published CQ
  honest WIN label一致**。pass-one expansions: aa005 19,039,348 / aa030
  20,088,051 / aa031 20,667,128 / aa047 19,721,784 / aa053 19,952,660
  (計 **99,468,971**)。
- D7 audit `audit_cx.py` (G6 CO unadopted補強gate込み): ×3 実行 **byte-identical**
  (sha256 `17785f7a…`) — **ALL 178 GATES PASS・verdict agreements 5/5
  (WIN=5 LOSS=0)・inconclusive=0**。tamper battery 4/4 gate発火+復帰green:
  A1 replica nodes改竄→`replica-aa005-det-pair` / A2 target result反転→
  `target-aa005-det-pair` / A3 anchor expansions改竄→`anchor-k02a-a-expansions` /
  A4 rows.json replica_nodes改竄→`replica-aa005-verdict-vs-published`
  (各tamperでaudit rc=1・byte復元後にALL 178 GATES PASSへ復帰)。
- D8 出版: B1 outputs (`output/` 32ファイル) → B2 val-gate host 4 →
  C (本README最終 + `MANIFEST-sha256.txt` 88ファイル) → 完了log
  `research/log/2026-11-24-part-cx-b28cqwin5-thirdimpl-completion.md`。
- 補助確認 (原宣言約定): 現canonical chain head (Part DB merged cache
  `04b0a239…`・6,354 s5verdict行・batch-29 adoption-reaudit出版物) に対象5キー
  のrow不在を機械確認 (5/5で `^s5verdict,<lo>,<hi>,` 行数=0)・
  同DB increments-manifestにも5キーのkey値出現なし (grep 0件)。よって本Partの
  証拠はchain側cacheと独立に成立している (cache不依存のcross-corroboration)。

## 目標と主張の限定

- 5行の第三実装verdict一致と本host pinned-replica 2-pass node-exact再現は
  **three-implementation corroboration** (jsreplay runner×2系 + 第三実装) の
  証拠であり、採用ではない。verdict不消費: aa005/aa030/aa031/aa047/aa053は
  honest labelのまま・adoptionは scrutiny owner C++第二実装 gate `9193f5b6…`
  を経て別adoption Part (pinned merger `90711961…` 経由) のみ。
- 閉鎖・被覆・secured・root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・class 5343・全キーはこの時点で
  UNKNOWN**。nodes数・expansions数・ttHits数を勝敗として読まない。
