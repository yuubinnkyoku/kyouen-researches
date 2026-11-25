# Part CX完了: batch-28 (class 5343) Part CQ 20M再probe新解決WIN残5行 (aa005/aa030/aa031/aa047/aa053) 第三実装交叉検証 — takeover実行 (2026-11-24)

- 原宣言: `1300c10d` (2026-11-24T00:49:31Z)。
- takeover宣言: `c48aa56b` (2026-11-24T04:20:09Z・earliest_takeover 04:19:31Z後・
  cx dir停滞3.5h超・対抗宣言なし機械確認・observed HEAD `10b8e96d`)。
- 対象: aa005 (1171516445255794690, 0) / aa030 (1243574039293722624, 0) / aa031
  (1459746821407506432, 0) / aa047 (1152921504611041280, 4228) / aa053
  (1152921504606855168, 4228) — published CQ 20M 2-pass node-exact WIN行
  (UNCONSUMED honest labels・verdict不消費)。

## 実行結果 (D1-D8全green)

- **D1** rules gate: quads 95,670 / triples 195,044 / mismatches 0。
- **D2** val-gate this-host fresh 4/4 node-exact (budget 2M/2M/15M/15M・audit G7比較式
  fields (1-7,9,10)完全一致・wall_sはcomment行のみ相違)。ttHits (index 8) は
  比較対象外フィールドで揺らぎ (8→9・17→18の2/4本) を観測・pinned audit設計どおり除外。
- **D3** negatives ng1/ng2: tag "a" 両方GATE_FAIL (rc=1)・文言完全一致
  (ng1 legal count mismatch derived=87 declared=88 / ng2 stone count mismatch bits=5 declared=6)。
- **D4** anchors: k02a exp 9,106,337 ttH 4,991,527・l1a exp 7,660,202 ttH 3,951,175・
  det-pair a==b・published pins node-exact。
- **D5** pinned-replica 10/10: 5キー×p1/p2 fresh-cold budget 20M rc=0・p1==p2・
  published raw node-exact: aa005 15,957,877 / aa030 16,765,560 / aa031 17,185,014 /
  aa047 16,230,465 / aa053 16,685,872。全行 result=1 (WIN honest label)・満了終了。
- **D6** 第三実装 10/10 clean・det-pair a==b 10/10・
  **verdict 5/5 result=1 = published CQ honest WIN label一致**。
  pass-one expansions 99,468,971 (aa005 19,039,348 / aa030 20,088,051 /
  aa031 20,667,128 / aa047 19,721,784 / aa053 19,952,660)。
- **D7** audit `87152e94…` ×3 byte-identical (`17785f7a…`): **ALL 178 GATES PASS・
  verdict agreements 5/5 (WIN=5 LOSS=0)・inconclusive=0**。tamper battery 4/4
  gate発火+復帰green: A1 `replica-aa005-det-pair` (replica nodes+1) /
  A2 `target-aa005-det-pair` (result反転) / A3 `anchor-k02a-a-expansions`
  (expansions+1) / A4 `replica-aa005-verdict-vs-published` (rows.json
  replica_nodes+1)。rows.jsonはbyte復元後 sha256 `3a87c5b6…` pin再一致。
- **D8** 出版+fetch-back検証:
  - B1 `f5c84d9e` outputs 32ファイル — pinned raw fetch-back 32/32 byte一致。
  - B2 `73cc46cfd` val-gate host 4本 (`.cx-host.out`) — fetch-back 4/4 byte一致。
  - C `496ad7da` README最終 + MANIFEST-sha256 (88ファイル) —
    MANIFEST記載の88ファイル全て pinned raw fetch-back sha256一致 (88/88)。
  - publication時の並走状況: K1280 (z11スライス証明レーン) が同時間帯に活発に
    pushしていたが CX dir への干渉・競合は一切なし (各push前に最新main HEAD再取得)。
- **補助確認** (原宣言約定): 現canonical chain head (Part DB merged cache
  `04b0a239…` 6,354 s5verdict行・2026-11-24 `n11-centralreply-class2251-loss37-adoption-reaudit-20261124`
  出版物) に対象5キーのrow不在を機械確認 (`^s5verdict,<lo>,<hi>,` 5/5で0行)・
  同DB increments-manifestにも5キーのkey値出現なし。本Partの証拠はchain側cacheと独立。

## 意味 (three-implementation corroboration・採用ではない)

- 5行のCQ honest WIN labelは (1) published CQ pinned-replica (20M 2-pass)・
  (2) 本host fresh replica (20M 2-pass・node-exact)・(3) 独立第三実装 (det-pair
  2回ずつ) の3系で一致。batch-28 P1 8行 (Part DE `1eead030`) と合わせ、
  batch-28 CQ 20M新解決WIN 13行の交叉検証が完了した (queue registry P1+P5相当)。
- ただし**verdict不消費**: 本Partはadoption・解放・閉鎖を行わない。
  canonical adoptionは scrutiny owner C++ gate `9193f5b6…` 通過後・
  pinned merger `90711961…` 経由の別adoption Part専権。

## UNKNOWN担保 (勝敗の断定なし)

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・10968・23964・class 5343 (54キーすべて・対象5キーを含む) は
本Partの前後を通じてすべてUNKNOWNのまま。** nodes数・expansions数・ttHits数を
勝敗や距離として読まない。

## 次のレジューム候補 (参考)

- queue registry rev3 (P5 5行 thirdimpl done反映・claimed → done)。
- 次候補パッケージ: registry記載どおり P2 (~est 152.7M nodes) 等。
- batch-28 CQ 20M新解決WIN 13行のadoption前scrutiny (C++ gate `9193f5b6…`) は
  別レーンの専権事項。
