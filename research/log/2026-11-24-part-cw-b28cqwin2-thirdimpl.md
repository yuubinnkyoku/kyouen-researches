# Part CW 完成 log: batch-28 (class 5343) Part CQ 20M再probe新解決WIN 2行 (aa004/aa035) の第三実装交叉検証 (2026-11-24)

宣言: `research/log/2026-11-24-part-cw-b28cqwin2-thirdimpl-declaration.md`
(commit `ba08e1cf`・observed HEAD `f6635144`)。実験dir:
`research/experiments/n11-centralreply-closure-b28cqwin2-thirdimpl-20261124/`
(kit 40 (内1 fileはA-fix適用済み) + outputs 24 = 64 files・
MANIFEST-sha256.txt 64 entries machine-pinned)。

## 成果

Part CQ (batch-28 EXHAUSTED 11行の20M再probe) で新解決された **WIN 2行**
aa004 (nodes 15,616,012) / aa035 (nodes 15,424,243) について
**three-implementation corroboration が成立**した:

- published CQ pinned-replica 2-pass (20M) — 両行 node-exact
- 本host pinned-replica 2-pass fresh-cold (budget 20M): aa004 p1/p2 =
  result 1, nodes **15,616,012** (86/85s)、aa035 p1/p2 = result 1,
  nodes **15,424,243** (85/85s)。published raw fields と node-exact。
- pinned第三実装 `third_impl.js` (08ea958f) a/b 2-run: aa004 result 1
  (clean) expansions **18,707,043** / ttHits 9,558,720 (53.31/51.77s)、
  aa035 result 1 (clean) expansions **18,461,728** / 9,389,275
  (52.45/52.10s)。det-pair 2/2・WALL-INCONCLUSIVE 0・DIVERGENCE 0。

**verdict不消費**: 両行は honest probe-level labelのまま (adoptionは別
adoption Part 経由のみ・WIN行は scrutiny owner C++第二実装 gate `9193f5b6…`
待ち)。audit **ALL 103 GATES PASS** (schema
`n11-centralreply-closure-b28cqwin2-thirdimpl-audit-v1`)・3回実行
byte-identical (stdout `72b07e76…`・json `684acf45…`)・audit tamper電池
4/4・maker tamper電池 8/8 (宣言記録)・clean control PASS。

- rules gate PASS (quads 95,670 machine match・triples 195,044・mismatches 0)
- val-gate fresh 4/4 node-exact (2M exhaustion ×2・3,651,923・5,040,200)
- anchors k02a/l1a 4/4 published-node-exact (9,106,337/4,991,527・
  7,660,602/3,951,175)・negatives 2/2 GATE_FAIL設計どおり
- G6 unadopted補強 (宣言済みbatch-28適合): aa004/aa035はPart CO出版物の
  adopted/win系id list全不在・exhausted_excluded_ids (CO-time roster 11行)
  + probed_ids/resolved_ids member bookkeepingに所在・merged canonical
  cache 6,301行に対象row/同key衝突ゼロ・**cross-artifact gate**: CQ status
  PASS roster (13キー) − anchors {aa036, aa046} == manifest
  exhausted_excluded_ids (機械一致)
- 補助確認: 最新canonical chain snapshot (Part CU merged 6,317行
  `30ddad9d…`) に両キーのrow 0行 (verdict不消費を最新snapshotでも確認)

これにより batch-28 の第三実装交叉検証済みWIN行は aa001/aa002/aa006/aa007/
aa008/aa009 + aa004/aa035 の **8行 + aa003 (LOSS)** (Wins 46行中8行)。

## 誠実な開示

- **A push 64KB打ち切り事故**: 読み取り側tool (file_system.read_file) は
  1回あたり64,000 bytesで打ち切るpagination仕様。初回A push
  (`ae00894d`) で 259,886 bytes の merged cache が 64,000 bytesのみ
  配置された (fetch-back検査で残39 filesはbyte一致・対象1 filesのみ
  不一致として検出)。
A-fix (`d56968e`) で行offset paginationにより全文再取得・上書きし
  sha `854800f3…` で確定。運用教訓: 64KB超fileはpagination必須。
- **実行環境リセット事故**: D1/D2実行直後 (~00:27Z) に環境同期失敗で
  ローカルscratchを喪失 (Part CRと同型)。kitはpublished commitsから
  sha検証付き復元 (maker再実行で
  rows.json byte-identical再生成)、**D1..D7を全再実行**し、published
  outputsは再実行版。決定的項目は1回目実行と全同一。
- **run_replica外側rc=1注記**: 成功時も `[ ... ] && exit` 短絡評価で
  外側終了コード1 (CR版runnerからの不変仕様)。per-pass rc=0は
  status.log記録どおり・成否判定はaudit G2bが機械検査。実害なし。
- maker tamper電池の初回T3/T5はsed不適合で無効果だったため
  efficacy-asserted sed/pythonで再実行し8/8検出 (Part CM/CRの
  efficacy-asserted設計踏襲)。

## 並走レーン (非接触・機械確認)

- Part CU (batch-29 16-LOSS adoption・完了): canonical merged chainを
  6,317行に更新 (本Partは読み書きせず・補助不在確認のみ)。
- Part CV (batch-29 ckpt-1/3 LOSS 16行の交叉検証): 進行中・非接触。
- Part CW (本Part): batch-28 class 5343・対象キー全く別で単一オーナー規約
  問題なし。

## Interpretation guard (verdict不消費)

**標準11×11空盤・19 central-reply roots・closure class 5343・全キー
(batch-28 54キーを含む) はこの時点で UNKNOWN**。nodes数・expansions数・
ttHits数を勝敗として読まない。閉鎖・被覆・secured・root勝敗の主張はしない。
batch-28のEXHAUSTED残3行 (aa021/aa028/aa032・20Mでも未解決) は別条件候補
としてopenのまま。

## commits

- 宣言 `ba08e1cf` (HEAD-before `f6635144`)・fetch-back byte一致
- A `ae00894d` (HEAD-before `ba08e1cf`)・fetch-back 39/40一致 → A-fix
  `d56968e` で対象1 file全文再出版後 40/40 byte一致
- B `a892601e` (HEAD-before `d56968e`)・fetch-back 24/24
- C `cac4e4da` (HEAD-before `a892601e`)・fetch-back 2/2
