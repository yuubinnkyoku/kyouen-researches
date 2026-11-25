# Part CG takeover 宣言 (2026-11-23): batch-28 (closure class 5343) drive-2 WIN行 aa006/aa007 第三実装交叉検証 — 中断Part CGのtakeover (publish-then-execute)

単一オーナー: n11中央応答レーン (長期レーン本セッション・takeover)。
takeover対象: Part CG 宣言 `38770f4ceed1ed11430016574152c06e9ea7c533`
(2026-11-23T16:30:48Z出版・note `research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md` 内「Part CG 宣言」section)。

## 0. takeover正当化 (宣告session消失判定・Part U / Part Z基準)

- 原Part CG宣言 (16:30:48Z) 以降 **84分以上**、scaffold・outputs・status update・
  完了logいずれのCG系commitもmainに存在しない (commit message機械grepで
  「Part CG」hitは宣言自身のみ)。実験dir
  `research/experiments/n11-centralreply-closure-b28drive2win-thirdimpl-20261123/`
  は本宣言push直前に404を再確認済み。
- 同一時間帯に他セッションが Part CH (16:53〜17:26Z完結・aa003採用)・
  Part CI (17:27Z宣言・batch-29)・Part CJ (17:32〜17:39Z完結・drive-3)・
  Part CK (17:40Z宣言・drive-4)・Part CL (17:41〜17:51Z完結・aa003 thirdimpl)
  を出版しており、CG宣言sessionのみが長時間無音。対抗するtakeover宣言・
  CG continuation宣言・CG所有権の再主張は存在しない (最新main機械grep済み)。
- よって Part U (batch-8) / Part Z (batch-11) と同一基準で
  **宣告session消失**と判定し、本セッションがPart CGをtakeoverする。
  原CG所有sessionが後に復帰して本takeover宣言より先に実行を完了させた場合は
  その出版物を正本として扱う (先着出版が正本・重複実行はlitteratureとして
  残す)。本takeoverは原宣言のgoal・stop rules・検証gateの意味論を変更しない。

## 1. 原宣言からの継承と再構成 (正直開示)

原CG宣言はkit 6 scripts・rows.json・make_inputs_cg.py・audit_cg.pyのbyte pin
(make_inputs_cg.py `d7155bd9…`・audit_cg.py `b326a292…`・rows.json
`3ef56043…`) を事前登録していたが、**これら3派生ファイルのbytesは原sessionが
kitを出版する前に消失したため継承不能**である。よって本takeoverは:

- **継承 (byte-pin再検証済み・原宣言と同一)**: 共有scripts 4件
  (third_impl.js `08ea958f…` / verify_tbl.js `c8c52528…` / jsreplay.js
  `84585617…` / run_thirdimpl.sh `a0b77d83…`・いずれもpublished Part CC/CK
  kitとbyte同一)・input CSV 6件 (aa006 `cdd84899…` / aa007 `493e0a58…` /
  k02a `b6174a3f…` / l1a `e13d2a6c…` / ng1 `8e64b9ad…` / ng2 `f19cd5a3…`)・
  sources (status-cd.log `343097c2…`(17行) / row-audit-cd.json `3e86a32b…` /
  batch-keys-cd.json `af19208f…`(54キー) / README-cd.md `338fc136…` /
  raw aa006.p1 `c9455882…` .p2 `e157a451…` aa007.p1 `ad2870ea…` .p2
  `bbacf3e3…` / published Part CC rows.json `b7222edf…`)・期待値のすべて
  (aa006: result 1 nodes 14,303,810 legal 88 s5 129823 membership 4・
  aa007: result 1 nodes 13,483,540 legal 95 s5 135236 membership 4・
  anchors k02a (WIN expansions 9,106,337 ttHits 4,991,527) l1a (LOSS
  expansions 7,660,602 ttHits 3,951,175)・negatives ng1 (legal+1) ng2
  (stones改竄))。
- **再構成 (本takeoverで新pin事前登録)**: make_inputs_cg.py
  `95e18953…` (published Part CC maker `8255d0ad…` とpublished Part CK maker
  `177c4409…` の二相続patternからの再構成・deltaはsources切替 (Part CB→
  Part CD) とtargets切替 (aa001/aa002→aa006/aa007 WIN行) のみ・gate骨格は
  CC/CKと不変・takeover provenance注記をheaderに明記)・audit_cg.py
  `0d0ca116…` (published Part CC audit.py `b7cfb0ce…`からのdeltaは原CG宣言
  どおり EXP/SCHEMA/rows-schema文字列とtarget-count gate明細 (2 WIN行) のみ。
  gate logic不変・takeover provenance注記をheaderに明記)・input/rows.json
  `f4e67203…` (schema
  `n11-centralreply-closure-b28drive2win-thirdimpl-input-v1`・maker機械生成・
  targets 2・anchors 2・negatives 2・`consumed_into_canonical_cache: false`)。

## 2. スコープ (原CG宣言のgoalを継承)

Part CD (batch-28 drive-2) で出版された **WIN行 aa006/aa007** (いずれも
honest label・2-pass node-exact @budget 15M) に対して:

1. **pinned第三実装** (非df-pn AND/ORミニマックス `third_impl.js`
   `08ea958f…`) によるverdict-level交叉検証 (2-run determinism pair)、
2. **本host pinned-replica (`jsreplay.js` `84585617…`) 2-pass fresh-cold再現**
   (published raw fieldsとのnode-exact一致。aa006/aa007としては最初の
   独立セッション再現)、
3. **監査** `audit_cg.py` 3回実行byte一致 + tamper battery。

**verdict不消費** (aa006/aa007のWIN行は本実験後もhonest labelのまま・採用は
scrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別adoption Part
(pinned merger `90711961…` 経由) のみ・本レーンは代行しない)。閉鎖・被覆・
secured・root勝敗の主張はしない。EXHAUSTED 2行 (aa004/aa005) はhonest
UNKNOWNのまま。fileless 45キー (aa010..aa054) はPart CK (drive-4・並走所有)
が担当済みのため本Partは非接触。batch-28 filelessの残キー一切に触れない。

## 3. 事前機械確認 (read-only・正直開示)

publish-then-execute規約に対する正直開示として、**read-only解析
(published sources取得・sha256 byte-pin検証・maker実行・input/rows.json機械導出)
は本宣言の出版前に本hostで機械実施済み**である (Part CI/CL宣言と同じ開示形式)。
solver実行 (rules gate / val-gate / negatives / anchors / replica / third-impl
targets / audit / tamper battery) は宣言後にのみ実行する。

機械確認済み:

1. **sources byte-pin再検証**: 共有scripts 4件・input CSV 6件・sources群
   (上記1のpin群)・val-gate 8件 (input CSV `ecc0299b…`/`56aacb71…` +
   published baselines `6e902ab1…`/`eeafe3ac…`/`8035fe54…`/`91dffdec…`)
   すべてpublished bytesとsha256一致 (commit-pinned raw fetch)。
   期待値: at2m 2本 = (result 0, nodes 2,000,000) exhaustion×2・15m 2本 =
   (result 2, nodes 3,651,923) と (result 2, nodes 5,040,200)。
2. **maker `make_inputs_cg.py` `95e18953…` 全gate PASS・4回実行byte一致**
   (CG-SCAFFOLD battery: status-cd 17行構成gate (PASS 7 = aa001/aa002/aa006/
   aa007 WIN + aa003 LOSS + aa004/aa005 EXHAUSTED・WIN-HALT 4行ペア・
   EXHAUSTED 2行・TRUNCATED-RETRY 4行)・row-audit-cd battery (probed 7・
   win_rows [aa001,aa002,aa006,aa007]・loss_rows [aa003]・exhausted [aa004,
   aa005]・fileless 47 = aa008..aa054完全list・mismatch 0)・README-cd文言
   battery・raw 2-pass field一致gate・published Part CC rows.json由来の
   anchor battery等値gate・derived-vs-published input CSV byte同一性gate)。
3. **input/rows.json** `f4e67203…`・targets 2件 (aa006/aa007・replica_result 1・
   expect_third 1)・input CSV 6件はpublished pinsとbyte同一。

## 4. kit (scripts 6・全件byte-pin)

- `third_impl.js` `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998`
  (published Part CC/CKからのpin再利用)
- `verify_tbl.js` `c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251`
- `jsreplay.js` `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
- `run_thirdimpl.sh` `a0b77d8330c696a5a7da2883d49110ae8703dc1673be10d3a9972ea53c885a41`
- `make_inputs_cg.py` `95e189533c6d085350b8f5f3ec8b04a612721ea3d7b7edf4a36478dea63bf98c`
  (takeover再構成・pin差し替えは本宣言で事前登録)
- `audit_cg.py` `0d0ca116b1bda675947feb23751f3ddd6891f43a3dc0820fd1285810c70128d9`
  (takeover再構成・pin差し替えは本宣言で事前登録)

## 5. 実行protocol (宣言後・逐次・1 solver/1 row/1 process)

1. **rules gate**: `node scripts/verify_tbl.js` 期待「replica quads 95670
   mine quads 95670 / triples checked 195044 mismatches 0」。失敗ならhard-stop。
2. **val-gate fresh 4本** (jsreplay --exact-replay・budget 2M×2 / 15M×2) →
   published baseline 4件とのnode-exact比較 (wall_s除く)。
3. **negatives**: run_thirdimpl.sh ng1/ng2 → 期待GATE_FAIL (rc=1・legal count
   mismatch / stone count mismatch)。
4. **anchors**: k02a/l1a × (a,b) 計4 run → published expansions/ttHits一致
   (det-pair必須)。
5. **targets pinned-replica 2-pass fresh-cold** (aa006/aa007 × p1/p2・budget
   15M) → published raw fields (aa006: result 1 nodes 14,303,810・aa007:
   result 1 nodes 13,483,540) とのnode-exact一致。published wall 203/184s
   (aa006 p1) 程度を見込むがwall_sは比較対象外。
6. **targets third_impl 2-run pair** (aa006/aa007 × (a,b)・cap 300,000,000・
   wallcap 240・memo-power=22) → determinism (a==b) と published
   replica_result 1との **verdict agreement** (reason clean必須)。
   third-implのexpansions値は事前予想しない (出版後に実測を記録する)。
7. **audit**: `python3 scripts/audit_cg.py` 3回実行byte一致
   (audit-run1/2/3.txt + audit-summary-run1/2/3.json + audit-summary.json)。
   期待: 全gate PASS・verdict agreements 2/2 (third=1 replica=1)。
8. **audit tamper battery** (scratch copy上・原CG宣言どおり4種):
   T1 replica result反転 (aa006.p1 result 1→2) → G2b replica-verdict gate
   fail・T2 raw nodes+1 (sources raw aa006.p1 nodes+1) → maker fail・T3 input
   CSV legal改竄 (aa006 legal 88→89) → G0 input-matches-rows fail・T4
   third_impl pin反転 (audit PIN_THIRD末尾1桁) → pin-third gate fail。
   各tamperに適用実効性assert・clean control PASS・実験dir bytes不変を検証。
9. **出版**: A scaffold (scripts 6 + input 7 + sources 15 + val-gate 8) →
   B outputs (rules-gate + val-gate this-host 4 + replica 4 + negative 2 +
   anchors 4 + targets 4 + audit 7 + status.log) → C README + MANIFEST-sha256
   → 完了log (独立logファイル・Part CL形式)。全files commit-pinned raw URL
   fetch-back byte照合・branch path URL (CDN stale) は使わない。push直前に
   毎回最新mainを再取得し、並走コミットとのfast-forward競合はrefetch後の
   再pushで解消する。
10. **誠実記録**: 事前登録からの逸脱・no-op probe・再実行・timeout事故は
    すべてstatus.logとrun logに正直に記録する。

## 6. 事前登録stop rules (原CG宣言と同一)

- replica MISMATCH (published raw fieldsとのresult/nodes不一致) は
  hard-stop・即時honest記録。
- third_impl DIVERGENCE (2-run非決定性) や WALL-INCONCLUSIVE (cap 300M/
  wallcap 240到達) はevidenceとして記録するがverdictには変換しない。
- EXHAUSTEDなし・全target行はfresh-cold 1回ずつ (retryは誠実記録)。

## 7. 解釈ガード (route statementのみ)

- 第三実装のclean verdictがpublished replica verdict (result 1 = WIN行) と
  一致すること、および本host replicaがpublished nodes 14,303,810 /
  13,483,540を2-passで完全再現することは、aa006/aa007の **第32/33番目の
  unconsumed closure WIN候補としてのverdict-level three-implementation
  corroboration文献**である (Part CC aa001/aa002・Part CL aa003 LOSS行と
  同型)。採用・解放・閉鎖の新規主張は一切ない。canonical cache 6,294行
  `3124461b…` はread-only不変 (WIN行はどのcacheにも未書込)。
- aa006/aa007の採用判断は引き続き scrutiny owner C++第二実装 gate
  `9193f5b6…` 待ち (本レーンは代行しない)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・
  aa006/aa007を含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。**
  nodes数・expansions数・ttHits数・wall秒数を勝敗として読まない。被覆・
  secured・root勝敗の主張はしない。WIN/LOSS採用は別adoption Part (pinned
  merger `90711961…` 経由) のみ。
