# Part CG re-takeover 宣言 (2026-11-23): batch-28 drive-2 WIN行 aa006/aa007 第三実装交叉検証 — 消失takeoverの再takeover (publish-then-execute)

単一オーナー: n11中央応答レーン (長期レーン本セッション・re-takeover)。
takeover対象: Part CG 宣言 (2026-11-23T16:30:48Z出版・note「Part CG 宣言」section・
prepare session vanished) → Part CG takeover 宣言
`research/log/2026-11-23-part-cg-takeover-b28drive2win-thirdimpl-declaration.md`
(commit `d5e9acc251eaf3af9465bbc64666ddb1520a48a3`・2026-11-23T18:01:16Z出版・
takeover session vanished)。本宣言は Part CG を再takeoverする
(takeover-of-takeover)。Part CGのgoal・stop rules・検証gateの意味論は原宣言から
一切変更しない。

## 0. 再takeover正当化 (宣告session消失判定・Part U / Part Z / Part CG / Part CI takeoverと同一基準)

- 原Part CG宣言 (16:30:48Z) は84分以上無音で、first takeover session (宣言
  18:01:16Z `d5e9acc2`) がtakeoverを宣言した。first takeover宣言 (18:01:16Z)
  以降、本宣言push直前 (2026-11-23T22:3xZ) まで **4時間30分以上**、Part CG系の
  scaffold・outputs・status update・完了logいずれのcommitもmainに存在しない
  (最新main直近15コミット機械確認: 21:00Z以降の全コミットはK1273/K1058/Part CI
  takeover/Part CP batch-30のみ・「Part CG」「b28drive2win」hitゼロ)。
- 実験dir `research/experiments/n11-centralreply-closure-b28drive2win-thirdimpl-`
  `20261123/` は本宣言push直前に404を再確認済み (GitHub contents API機械確認。
  HEAD `7aaa0525…` 時点のexperiments treeにも当該dirは存在しない)。
- 同一時間帯に他セッションが Part CI takeover (20:57Z宣言・21:41/21:52Z出版)・
  Part CP batch-30 (21:43-21:56Z出版) を進行中であり、両宣言ともPart CGを
  「outputs停滞・非接触」と明記している。Part CG continuation宣言・re-takeover
  宣言・所有権の再主張は存在しない。
- よって Part U (batch-8) / Part Z (batch-11) / Part CG takeover / Part CI takeover
  と同一基準で **first takeover sessionも消失** と判定し、本セッションがPart CGを
  再takeoverする (沈黙時間4時間30分はPart CI takeoverが使用した3時間30分基準を
  上回る)。原CG session・first takeover sessionが後に復帰して本宣言より先に実行を
  完了させた場合はその出版物を正本として扱う (先着出版が正本・重複実行は
  literatureとして残す)。

## 1. 継承と再構成 (正直開示)

- **継承 (byte-pin再検証済み・原宣言・first takeover宣言と同一)**: 共有scripts 4件
  (third_impl.js `08ea958f…` / verify_tbl.js `c8c52528…` / jsreplay.js
  `84585617…` / run_thirdimpl.sh `a0b77d83…`・published Part CC kitとbyte同一)、
  input CSV 6件 (aa006 `cdd84899…` / aa007 `493e0a58…` / k02a `b6174a3f…` /
  l1a `e13d2a6c…` / ng1 `8e64b9ad…` / ng2 `f19cd5a3…`)、sources 15件
  (status-cd.log `343097c2…` (17行) / row-audit-cd.json `3e86a3a2b…` /
  batch-keys-cd.json `af19208f…` (54キー) / README-cd.md `338fc136…` / raw
  aa006.p1 `c9455882…` .p2 `e157a451…` aa007.p1 `ad2870ea…` .p2 `bbacf3e3…` /
  published Part CC rows.json `b7222edf…` / Part BF anchor/negative基底CSV 4件)・
  val-gate 8件 (input CSV `ecc0299b…`/`56aacb71…` + published baselines
  `6e902ab1…`/`eeafe3ac…`/`8035fe54…`/`91dffdec…`)・期待値のすべて
  (aa006: result 1 nodes 14,303,810 legal 88 s5 129823 membership 4・aa007:
  result 1 nodes 13,483,540 legal 95 s5 135236 membership 4・anchors k02a
  (WIN expansions 9,106,337 ttHits 4,991,527) l1a (LOSS expansions 7,660,602
  ttHits 3,951,175)・negatives ng1 (legal+1) ng2 (stones改竄)・rules-gate期待
  「replica quads 95670 mine quads 95670 / triples checked 195044 mismatches 0」)。
  上記31ファイルを本hostでcommit-pinned raw fetchしsha256全件一致を確認済み
  (first takeover宣言のpin群と同一)。
- **継承不能 (正直開示)**: first takeover宣言が再事前登録した maker `95e18953…` /
  audit `0d0ca116…` / input rows.json `f4e67203…` の3派生ファイルは、first
  takeover sessionがscaffoldを出版する前に消失したため **bytesは未出版のまま
  継承不能** である (原宣言の `d7155bd9…`/`b326a292…`/`3ef56043…` も同様)。
  よって本re-takeoverは **3派生ファイルを新規再構成して新pinを本宣言で事前登録**
  する (first takeoverが原宣言の失われたpinを再登録したのと同じ手続き):
  - `make_inputs_cg.py` sha256
    `b92cc4f2e4c1c9c404fa4098e0144728e3750dd33cf8e250dd3c984f1a819a76`
    (published Part CC maker `8255d0ad…`からの再構成・deltaは宣言どおり
    sources切替 (Part CB→Part CD) とtargets切替 (aa001/aa002→aa006/aa007
    drive-2 WIN行)・schema文字列・takeover provenance注記のみ。gate骨格はCCと
    不変。CG固有gate: status-cd 17行構成battery (PASS 7 = WIN 4 + LOSS 1 +
    EXHAUSTED 2・WIN-HALT 4行・EXHAUSTED 2行・TRUNCATED-RETRY 4行)・
    row-audit-cd battery (probed 7・win_rows [aa001,aa002,aa006,aa007]・
    loss_rows [aa003]・exhausted [aa004,aa005]・fileless 47 = aa008..aa054完全
    list・mismatch 0)・README-cd文言battery・raw 2-pass field一致gate・
    published Part CC rows.json由来のanchor/negative battery等値gate・
    derived-vs-published input CSV byte同一性gate (pin `cdd84899…`/`493e0a58…`)。
    本hostで4回実行byte-stable・全gate PASSを確認済み (宣言前read-only fair開示))。
  - `audit_cg.py` sha256
    `9f5a36fbec19bff3724b958e66b1d35a2aef1d63728a2bf3cc9ff63f7221f055`
    (published Part CC audit.py `b7cfb0ce…`からの再構成・deltaは宣言どおり
    EXP/SCHEMA/rows-schema文字列とtarget-count gate明細 (2 WIN行) のみ。
    gate logic不変・G0 input/rows交叉照合・G1 pinned script bytes (PIN_THIRD
    `08ea958f…`/PIN_VERIFYTBL `c8c52528…`/PIN_JSREPLAY `84585617…`)・G2
    rules-gate・G2b replica-thishost (budget 15M fresh-cold 2-pass・published
    raw fields node-exact)・G3 anchors・G4 negatives・G5 targets 2-run
    determinism + verdict agreement)。
  - `input/rows.json` sha256
    `51e65756337a5fa9f856cca076f9d7209cefab58a5d08b91190439b131ed3ce8`
    (schema `n11-centralreply-closure-b28drive2win-thirdimpl-input-v1`・
    maker機械生成・targets 2 (aa006/aa007・replica_result 1・replica_nodes
    14,303,810/13,483,540・expect_third 1)・anchors 2・negatives 2・
    `consumed_into_canonical_cache: false`)。

## 2. スコープ (原CG宣言のgoalを継承)

Part CD (batch-28 drive-2) で出版された **WIN行 aa006/aa007** (いずれも
honest label・2-pass node-exact @budget 15M) に対して:

1. **pinned第三実装** (非df-pn AND/ORミニマックス `third_impl.js` `08ea958f…`)
   によるverdict-level交叉検証 (2-run determinism pair)、
2. **本host pinned-replica (`jsreplay.js` `84585617…`) 2-pass fresh-cold再現**
   (published raw fieldsとのnode-exact一致。aa006/aa007としては最初の
   独立セッション再現)、
3. **監査** `audit_cg.py` 3回実行byte一致 + tamper battery (4種)。

**verdict不消費** (aa006/aa007のWIN行は本実験後もhonest labelのまま・採用は
scrutiny owner C++第二実装 gate `9193f5b6…` 通過後の別adoption Part
(pinned merger `90711961…` 経由) のみ・本レーンは代行しない)。閉鎖・被覆・
secured・root勝敗の主張はしない。batch-28のEXHAUSTED 11行・WIN 35行・
LOSS 8行 (aa003 + 7行はPart COで採用済み) の残る簿記は本Partでは非接触。
19 central-reply roots・二石root・S2の探索も本Partの範囲外。

## 3. 事前機械確認 (read-only・正直開示)

publish-then-execute規約に対する正直開示として、**read-only解析
(published sources取得・sha256 byte-pin検証 (31ファイル全件一致)・maker実行
×4 (byte-stable)・input/rows.json機械導出・derived-vs-published input CSV
byte同一性確認) は本宣言の出版前に本hostで機械実施済み**である (Part CG
takeover宣言・Part CI/CL宣言と同じ開示形式)。**solver実行 (rules gate /
val-gate / negatives / anchors / replica / third-impl targets / audit /
tamper battery) は宣言後にのみ実行する**。

## 4. kit (scripts 6・全件byte-pin)

- `third_impl.js` `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998`
  (published Part CC/CKからのpin再利用)
- `verify_tbl.js` `c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251`
- `jsreplay.js` `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
- `run_thirdimpl.sh` `a0b77d8330c696a5a7da2883d49110ae8703dc1673be10d3a9972ea53c885a41`
- `make_inputs_cg.py`
  `b92cc4f2e4c1c9c404fa4098e0144728e3750dd33cf8e250dd3c984f1a819a76`
  (本re-takeover再構成・pin差し替えは本宣言で事前登録)
- `audit_cg.py`
  `9f5a36fbec19bff3724b958e66b1d35a2aef1d63728a2bf3cc9ff63f7221f055`
  (本re-takeover再構成・pin差し替えは本宣言で事前登録)

## 5. 実行protocol (宣言後・逐次・1 solver/1 row/1 process)

1. **rules gate**: `node scripts/verify_tbl.js` 期待「replica quads 95670
   mine quads 95670 / triples checked 195044 mismatches 0」。失敗ならhard-stop。
2. **val-gate fresh 4本** (jsreplay --exact-replay・budget 2M×2 / 15M×2) →
   published baseline 4件とのnode-exact比較 (wall_s除く)。不一致ならhard-stop。
3. **negatives**: run_thirdimpl.sh ng1/ng2 → 期待GATE_FAIL (rc=1・legal count
   mismatch / stone count mismatch)。
4. **anchors**: k02a/l1a × (a,b) 計4 run → published expansions/ttHits一致
   (det-pair必須)。
5. **targets pinned-replica 2-pass fresh-cold** (aa006/aa007 × p1/p2・budget
   15M) → published raw fields (aa006: result 1 nodes 14,303,810・aa007:
   result 1 nodes 13,483,540) とのnode-exact一致。published wall 203/195/
   183/186s程度を見込むがwall_sは比較対象外。
6. **targets third_impl 2-run pair** (aa006/aa007 × (a,b)・cap 300,000,000・
   wallcap 240・memo-power=22) → determinism (a==b) と published
   replica_result 1との **verdict agreement** (reason clean必須)。
   third-implのexpansions値は事前予想しない (出版後に実測を記録する)。
7. **audit**: `python3 scripts/audit_cg.py` 3回実行byte一致
   (audit-run1/2/3.txt + audit-summary-run1/2/3.json + audit-summary.json)。
   期待: 全gate PASS・verdict agreements 2/2 (third=1 replica=1)。
8. **audit tamper battery** (scratch copy上・first takeover宣言どおり4種):
   T1 replica result反転 (aa006.p1 result 1→2) → G2b replica-verdict gate
   fail・T2 raw nodes+1 (sources raw aa006.p1 nodes+1) → maker fail・T3 input
   CSV legal改竄 (aa006 legal 88→89) → G0 input-matches-rows fail・T4
   third_impl pin反転 (audit PIN_THIRD末尾1桁) → pin-third gate fail。
   各tamperに適用実効性assert・clean control PASS・実験dir bytes不変を検証。
9. **出版**: A scaffold (scripts 6 + input 7 + sources 15 + val-gate 8) →
   B outputs (rules-gate + val-gate this-host 4 + replica 4 + negative 2 +
   anchors 4 + targets 4 + audit 7 + status.log) → C README + MANIFEST-sha256
   → 完了log (独立logファイル・Part CL/CM形式)。全files commit-pinned raw URL
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

## 7. 解釈ガード (route statementのみ)・UNKNOWN担保・不接触

- 第三実装のclean verdictがpublished replica verdict (result 1 = WIN行) と
  一致すること、および本host replicaがpublished nodes 14,303,810 / 13,483,540
  を2-passで完全再現することは、aa006/aa007の **第32/33番目の unconsumed
  closure WIN候補としてのverdict-level three-implementation corroboration
  文献**である (Part CC aa001/aa002・Part CM aa008/aa009と同型)。採用・解放・
  閉鎖の新規主張は一切ない。canonical cache (Part CO merged 6,301行
  `854800f3…`・Part CH merged 6,294行 `3124461b…`) はread-only不変
  (WIN行はどのcacheにも未書込)。
- aa006/aa007の採用判断は引き続き scrutiny owner C++第二実装 gate
  `9193f5b6…` 待ち (本レーンは代行しない)。
- **不接触**: Part CP batch-30 drive-2 (closure class 34269・宣言
  `7aaa0525`・ac005..ac054・並走所有)・Part CI takeover batch-29
  (class 2251・checkpoint 1/3 `a5a159d7` 後続・並走所有)・fast lane・
  finite-field lane・inversive lane・EXHAUSTED行の高budget再probe
  (別宣言条件)・WIN行のscrutiny (C++ `9193f5b6…` 専権)・batch 1..27各
  published dir (不変)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・
  aa006/aa007を含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。**
  nodes数・expansions数・ttHits数・wall秒数を勝敗として読まない。被覆・
  secured・root勝敗の主張をしない。WIN/LOSS採用は別adoption Part (pinned
  merger `90711961…` 経由) のみ。

(observed HEAD-before-push: `7aaa05257c06cf5c0153a05c557601ff252efb8a`
(2026-11-23T21:56:11Z・Part CP drive-2宣言)。対抗宣言なし (最新main直近
15コミット機械grep済み)。実験dir 404再確認済み。)
