# batch-28 (class 5343) WIN46 thirdimpl交叉検証 queue registry (2026-11-24)

batch-28 (closure class 5343・54キー aa001..aa054) の第三実装交叉検証候補を published status log 群 + 公式採用記録から機械導出した bookkeeping 成果物。
作成時刻 2026-11-24T02:48:57Z / 観測 HEAD-before-push `d2d60645d26b2eae88ffc87fdd5e6160cfcae8e1`。

**rev2 (2026-11-24T03:57Z)**: P1パッケージ8行の第三実装交叉検証完了 (Part DE・完了 `1eead030`) を反映。queue-registry.json該当8行のthirdimpl state (open→done)・queue_state_counts (done 8→16・open 33→25)・thirdimpl_publications (DE追記)・packages P1 (done) を更新。それ以外のview (open33_by_est_cost・P2〜P4) はrev1時点のまま。本revも solver実行・probe・cache書込なしの純bookkeeping。

**rev3 (2026-11-24T05:15Z)**: Part CX完了 (takeover宣言 `c48aa56b`・完了 `46687096`) を反映。claimed-5行 (aa005/aa030/aa031/aa047/aa053) のthirdimpl state (claimed→done)・queue_state_counts (done 16→21・claimed 5→0)・claimed5 takeover規約 (resolved)・thirdimpl_publications CX (done) を更新。原宣言 `1300c10d` は3.5h停滞後にtakeover規約どおり単一オーナーtakeoverで解決 (対抗宣言なし機械確認)。open25・P2〜P4 viewは不変。本revも solver実行・probe・cache書込なしの純bookkeeping。

## 何であるか・何でないか

- **本registryの作成にあたり solver は一つも実行していない** (probeなし・cache書込なし・単一オーナーlane宣言なし)。純粋な整理であって、いかなる計算laneの占有でも宣告でもない。
- **verdict不消費。**登録行のWIN/LOSSはいずれも honest labels (WIN行 = unconsumed closure WIN候補・採用判断は scrutiny owner C++第二実装 gate のまま、LOSS行 = canonical cacheへのadoption事実) で、閉鎖・被覆・secured・root勝敗の主張を一切含まない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて) は本registryの前後を通じてすべてUNKNOWNのまま。** nodes数を勝敗として読まない。

## データ源 (すべて再fetch + sha256再計算で既知pinと一致をassert済み)

- `drive2-15m` research/experiments/n11-centralreply-closure-class5343-batch28-drive2-20261123/output/status.log / sha256 `343097c268425cc62263935f1063c26689515bc797c68bbdb82389c713952c98` / git blob `undefined` / budget 15,000,000
- `drive3-15m` research/experiments/n11-centralreply-closure-class5343-batch28-drive3-20261123/output/status.log / sha256 `1a5c08c516dbc34bde466a55a39f7e9acdfef57f09bc1bd7e19d2efb9fd5137c` / git blob `undefined` / budget 15,000,000
- `drive4-15m` research/experiments/n11-centralreply-closure-class5343-batch28-drive4-20261123/output/status.log / sha256 `598174447fa878c2e0a6d6db6f892c5c279063174d763746456476e3051633f8` / git blob `undefined` / budget 15,000,000
- `drive5-15m` research/experiments/n11-centralreply-closure-class5343-batch28-drive5-20261123/output/status.log / sha256 `ca1e98ccd952b29e8295147add50e6b4a3ff3732748bf544b9c3a7018d495df0` / git blob `undefined` / budget 15,000,000
- `cq-20m` research/experiments/n11-centralreply-class5343-b28exhausted-reprobe-20261123/output/status.log / sha256 `afc4873482219ec605f62da9a2b543ca8a10f5a2a08d3b3a5ac6de36475704af` / git blob `undefined` / budget 20,000,000
- `cs-25m` research/experiments/n11-centralreply-class5343-b28exhausted-reprobe25m-20261123/output/status.log / sha256 `cea47a0c887b0380ebb9604a11ad1bf7fab78a1c58e5e3a1b8e9c555b394524f` / git blob `undefined` / budget 25,000,000
- `ct-30m` research/experiments/n11-centralreply-class5343-b28aa050-reprobe30m-20261123/output/status.log / sha256 `efd18b3c21a375864d11e740397d9d2aba833a9911cd287f881aa6df8c7f9865` / git blob `undefined` / budget 30,000,000
- batch-keys: research/experiments/n11-centralreply-closure-b28cqwin5-thirdimpl-20261124/sources/batch-keys-b28.json / sha256 `af19208fafb61cc20892fa968bc373fe2c4f79da94744dfeed9d2f40ea8481e5` / git blob `8fa79ae14abca39e39e23d7222074776ec8bd731` (Part CX kit `3185a672` sources)

status.logの行形式は `\d{2}:\d{2}:\d{2}Z aaNNN PASS <budget>,<rc>,<nodes>` + (WIN時) `WIN-HALT` 行・`EXHAUSTED <budget>,<rc>,<nodes>`・`P1/P2-TRUNCATED-RETRY` (junk行 `P1-FAIL ` は既知非verdict行として除外・Part CN誠実記録1)。
rc = 0/1/2 (EXHAUSTED/WIN/LOSS・drive README群の定義どおり)。decisive row = 各キーで最初にrc=1 (WIN) が出た行、なければrc=2 (LOSS)。

## batch-28 最終状態 (機械導出・全assert PASS)

- 54キー = **WIN 46** (15M×35 + 20M×7 + 25M×3 + 30M×1) + **LOSS 8** (aa003採用済み + 7行Part CO採用済み) + EXHAUSTED 0。
- EXHAUSTED 11行 (15M) は予算違いの別宣言条件 (20M/25M/30M再probe) で解決済み。同一条件再probe禁止規約は無侵害。
- anchor再観測のnode一致: aa004 (rc=1・nodes 15,616,012 が20M/25M/30Mで同一)・aa036 (rc=2・nodes 955,659 が15M/20M/25M/30Mで同一)・aa046 (rc=1・nodes 2,185,149 が15M/20Mで同一)。

## 第三実装交叉検証の現状

- **done 21 WIN行 (rev3)**: aa001/aa002 (Part CC・完了 `9eb30494`)・aa006/aa007 (Part CG・完了 `699a13bc`)・aa008/aa009 (Part CM・完了 `2102800b`)・aa004/aa035 (Part CW・完了 `8f03ed3d`)・aa046/aa016/aa025/aa033/aa027/aa038/aa012/aa042 (P1パッケージ8行・Part DE・完了 `1eead030`・three-implementation corroboration 8/8 agree・replica 16/16 node-exact・audit 323 gates PASS・verdict不消費)・aa005/aa030/aa031/aa047/aa053 (**P5 (claimed-5) 5行・Part CX・takeover `c48aa56b` 完了 `46687096`**・three-implementation corroboration 5/5 agree・replica 10/10 node-exact・audit 178 gates PASS×3 byte-identical・verdict不消費)。加えて LOSS行 aa003 (Part CL・完了 `660fe238`)。
- **claimed 0行 (rev3)**: なし。Part CX (原宣言 `1300c10d`・2026-11-24T00:49:31Z) は3.5h停滞後、takeover規約 (earliest_takeover 2026-11-24T04:19:31Z以降かつ停滞・対抗宣言なし機械確認) に従いtakeover宣言 `c48aa56b` (2026-11-24T04:20:09Z) で解決・完了 `46687096`。claimed5_do_not_retake_until_takeover_ruleはrev3でresolved。
- **open 25 WIN行 (rev2時点)**: P1パッケージはPart DEで交叉検証済み (done)。残りはP2/P3/P4パッケージ25行 (下記queue表・P1〜P4の分割はrev1時点のコスト順viewとして不変)。
- **L-optional 7 LOSS行**: aa018/aa036/aa023/aa024/aa015/aa029/aa017 (Part CO採用済み・交叉検証は冗長性のみで任意)。

## 見積りモデル (planning heuristic・計測値ではない)

Part CC 出版観測比 (thirdimpl pass nodes / pinned pass nodes): aa001 15,677,345/13,183,855 = 1.189・aa002 7,624,309/6,527,041 = 1.168 (キャリブレーション n=2)。
 Planning factor 1.18/pass × 2-pass ⇒ est = round(2.36 × pinned nodes)。**行列の第三実装node数は実装依存で、交叉検証の主張はverdict一致のみ。** estはpackage選定の目安。

## open33 queue (est昇順・package構成)

| key | 解決tier | pinned nodes | est 2-pass | package |
|---|---|---|---|---|
| aa046 | 15m | 2,185,149 | 5,156,952 | P1 |
| aa016 | 15m | 2,621,847 | 6,187,559 | P1 |
| aa025 | 15m | 3,056,950 | 7,214,402 | P1 |
| aa033 | 15m | 3,347,117 | 7,899,196 | P1 |
| aa027 | 15m | 4,860,191 | 11,470,051 | P1 |
| aa038 | 15m | 4,911,996 | 11,592,311 | P1 |
| aa012 | 15m | 4,994,213 | 11,786,343 | P1 |
| aa042 | 15m | 5,800,791 | 13,689,867 | P1 |
| aa014 | 15m | 7,263,370 | 17,141,553 | P2 |
| aa049 | 15m | 7,272,703 | 17,163,579 | P2 |
| aa051 | 15m | 7,662,388 | 18,083,236 | P2 |
| aa019 | 15m | 7,967,030 | 18,802,191 | P2 |
| aa013 | 15m | 8,317,071 | 19,628,288 | P2 |
| aa020 | 15m | 8,432,253 | 19,900,117 | P2 |
| aa010 | 15m | 8,882,182 | 20,961,950 | P2 |
| aa040 | 15m | 8,916,641 | 21,043,273 | P2 |
| aa052 | 15m | 8,976,982 | 21,185,678 | P3 |
| aa044 | 15m | 9,219,778 | 21,758,676 | P3 |
| aa041 | 15m | 10,283,599 | 24,269,294 | P3 |
| aa048 | 15m | 10,553,343 | 24,905,889 | P3 |
| aa026 | 15m | 11,019,409 | 26,005,805 | P3 |
| aa039 | 15m | 11,349,776 | 26,785,471 | P3 |
| aa043 | 15m | 12,069,965 | 28,485,117 | P3 |
| aa045 | 15m | 12,371,943 | 29,197,785 | P3 |
| aa011 | 15m | 12,424,953 | 29,322,889 | P4 |
| aa054 | 15m | 13,227,570 | 31,217,065 | P4 |
| aa022 | 15m | 14,044,375 | 33,144,725 | P4 |
| aa034 | 15m | 14,097,048 | 33,269,033 | P4 |
| aa037 | 15m | 14,239,714 | 33,605,725 | P4 |
| aa032 | 25m | 20,312,294 | 47,937,014 | P4 |
| aa028 | 25m | 21,563,925 | 50,890,863 | P4 |
| aa021 | 25m | 22,942,323 | 54,143,882 | P4 |
| aa050 | 30m | 25,541,199 | 60,277,230 | P4 |

- **P1** (8行): aa046, aa016, aa025, aa033, aa027, aa038, aa012, aa042 / pinned計 31,778,254 nodes・est計 ≈ 74,996,681 nodes
- **P2** (8行): aa014, aa049, aa051, aa019, aa013, aa020, aa010, aa040 / pinned計 64,713,638 nodes・est計 ≈ 152,724,187 nodes
- **P3** (8行): aa052, aa044, aa041, aa048, aa026, aa039, aa043, aa045 / pinned計 85,844,795 nodes・est計 ≈ 202,593,715 nodes
- **P4** (9行): aa011, aa054, aa022, aa034, aa037, aa032, aa028, aa021, aa050 / pinned計 158,393,401 nodes・est計 ≈ 373,808,426 nodes

P4 は CS/CT解決4行 (aa032/aa028/aa021/aa050) を含む (Part CW〜CT継続の高tier群)。各packageの実施は次回以降のイベントが単一オーナー宣言 (publish-then-execute) で独自に前提条件を登録する。**本registryはどのpackageも予約しない。**

## 次回イベントの使い方

1. 必ず最新mainを取り直す (毎時並走)。本registryの行state・CXのoutputs出版状況を再確認。
2. 第三実装交叉検証を実施する場合は、先行partsのpublished kit (Part CX scaffold A `3185a672`・Part CW kit 等) の scripts/val-gate/pinned inputs (batch-keys.json `af19208f…` + input/aaNNN.input.csv 54本) を再利用し、publish-then-execute 宣言を先行出版する。
3. 結果の出版時は verdict不消費・honest labels・票面の勝敗文言は交叉検証の一致のみに限定する。
4. 宣言前に対抗宣言の有無を確認 (takeover規約・3.5h)。

## 限界と既知事項

- estコストは n=2 キャリブレーションに基づく大まかな見積り (planning only・実測保証なし)。
- 本registry自体は独立検証ではなく、published一次資料のsha256 pinnedな整理。交叉検証の実体は各Partの実験dirと監査に属する。
- drive5 status.logのjunk行 `P1-FAIL ` は空キーinvocation由来の既知非verdict行 (影響なし・Part CN誠実記録1)。
- thirdimpl node数は実装間で一致しない (pinned⇔thirdimpl間で比較可能なのはverdictと要件のみ・node一致は同実装間に限る)。

## 独立検証の手順

`output/queue-registry.json` の `how_to_verify` 参照。7 status log の sha256 が本README記載値と一致することを確認してから行をparseし、54行のlabel/tier/nodesとdecisive行を再導出して突き合わせる。
