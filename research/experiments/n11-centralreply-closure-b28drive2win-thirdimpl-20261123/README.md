# batch-28 drive-2 WIN行 aa006/aa007 第三実装交叉検証 (Part CG re-takeover, 2026-11-23)

Part CG (publish-then-execute・単一オーナー)。原Part CG宣言 (16:30:48Z) の後、
first takeover宣言 `d5e9acc2` (18:01:16Z) までに両 session が消失したため、
本sessionが re-takeover (takeover-of-takeover) を宣言して実行した
(宣言: `research/log/2026-11-23-part-cg-retakeover-b28drive2win-thirdimpl-declaration.md`
commit `b8ae515b`・宣言原稿sha256
`197651c3798e6f7b4ff10b2edecfd1a8b56ffba8269c0482b0ef7a59ea8764e1`)。
Part CDで出版された **batch-28 drive-2 WIN行 aa006/aa007** (いずれもhonest label・
2-pass node-exact @budget 15M) に対して、pinned第三実装 (非df-pn AND/ORミニマックス)
`third_impl.js` によるverdict-level交叉検証と、本host pinned-replica
(`jsreplay.js`) 2-pass fresh-cold再現を行う。**verdict不消費**。
閉鎖・被覆・secured・root勝敗の主張はしない。

## kit (scripts 6・全件byte-pin)

- 共有4件 (published Part CC kit `n11-centralreply-closure-b28win-thirdimpl-20261123`
  とbyte-clone検証済み): `third_impl.js` `08ea958f…` / `verify_tbl.js`
  `c8c52528…` / `jsreplay.js` `84585617…` / `run_thirdimpl.sh` `a0b77d83…`。
- 本re-takeoverで再構成し宣言でpin事前登録した2件: `make_inputs_cg.py`
  `b92cc4f2e4c1c9c404fa4098e0144728e3750dd33cf8e250dd3c984f1a819a76`
  (published Part CC maker `8255d0ad…`からのdelta再構成・sources切替 Part CB→CD・
  targets切替 aa001/aa002→aa006/aa007)・`audit_cg.py`
  `9f5a36fbec19bff3724b958e66b1d35a2aef1d63728a2bf3cc9ff63f7221f055`
  (published Part CC audit.py `b7cfb0ce…`からのdelta再構成・EXP/SCHEMA文字列と
  target-count gate明細のみ差分・gate logic不変)。
  first takeover宣言のpin (`95e18953…`/`0d0ca116…`/`f4e67203…`) はbytes未出版の
  まま消失しており継承不能 (宣言§1正直開示どおり)。

## input / sources / val-gate (published pins)

- `input/rows.json` `51e65756…` (schema
  `n11-centralreply-closure-b28drive2win-thirdimpl-input-v1`・maker機械生成・
  targets 2 (aa006/aa007・replica_result 1・replica_nodes 14,303,810/13,483,540・
  expect_third 1)・anchors 2・negatives 2・`consumed_into_canonical_cache: false`)。
- input CSV 6件 (derived-vs-published byte同一性gate済み): aa006 `cdd84899…` /
  aa007 `493e0a58…` / k02a `b6174a3f…` / l1a `e13d2a6c…` / ng1 `8e64b9ad…` /
  ng2 `f19cd5a3…`。期待値: aa006 result 1 nodes 14,303,810 legal 88・aa007
  result 1 nodes 13,483,540 legal 95。
- sources 15件 (published Part CD/CC/BF kitからbyte-pin取得・全件sha256一致): 
  status-cd.log `343097c2…` (17行) / row-audit-cd.json `3e86a3a2b…` /
  batch-keys-cd.json `af19208f…` (54キー) / README-cd.md `338fc136…` /
  raw aa006.p1 `c9455882…` .p2 `e157a451…` aa007.p1 `ad2870ea…` .p2
  `bbacf3e3…` / published-rows-cc.json `b7222edf…` / BF anchor/negative基底CSV 4件。
- val-gate 12件: sanctioned 4キー input CSV (`ecc0299b…`/`56aacb71…`) +
  published baselines 4件 (`6e902ab1…`/`eeafe3ac…`/`8035fe54…`/`91dffdec…`) +
  本host fresh `.cg-host.out` 4件。

## 実行記録 (宣言protocol D1..D8・宣言後 宣言どおり実行)

1. **rules gate PASS**: 「replica quads 95670 mine quads 95670 /
   triples checked 195044 mismatches 0」 (output/rules-gate.txt)。
2. **val-gate fresh 4/4 node-exact** (published baseline比較・wall_s比較外):
   at2m×2 (budget 2M・nodes 2,000,000 各keys
   1152921504606851072:536870946 / 1188950301626860544:536870912)・
   first-15m (budget 15M・nodes 3,651,923)・second-15m (budget 15M・nodes
   5,040,200)。本host wall_s 9/9/17/24。
3. **negatives 2/2 GATE_FAIL (rc=1)**: ng1「legal count mismatch: derived=87
   declared=88」・ng2「stone count mismatch: bits=5 declared=6」。
4. **anchors 4/4 published値完全一致 (det-pair含む)**: k02a (WIN) a/bともに
   result 1 expansions 9,106,337 ttHits 4,991,527・l1a (LOSS) a/bともに
   result 2 expansions 7,660,602 ttHits 3,951,175。
5. **targets pinned-replica 2-pass fresh-cold 4/4 node-exact** (aa006/aa007の
   最初の独立セッション再現): aa006 p1/p2ともに result 1 nodes 14,303,810・
   aa007 p1/p2ともに result 1 nodes 13,483,540。published raw fieldsと完全一致。
   本host wall 77/75/71/73s (published 203/195/183/186s・wall_sは比較対象外)。
6. **targets third_impl 2-run determinism pair 4/4 clean WIN**: aa006 a/bともに
   result 1 reason=clean expansions 16,976,575 ttHits 8,935,079・aa007 a/bともに
   result 1 reason=clean expansions 16,098,654 ttHits 8,465,953
   (cap 300,000,000・memo-power=22・quads 95,670全run一致)。→
   **verdict agreement 2/2 (third=1 replica=1)・三実装交叉検証成立**
   (published jsreplay (Part CD)・本host jsreplay replica・第三実装)。
   ただしverdict不消費 (honest WIN行のまま)。
7. **audit `audit_cg.py` 3回実行byte一致**: audit-run1/2/3.txt ともに
   `85cb0a7531767b1fea29a0ad84b5a90bdb8099f53e1f4f0b307b41ab2e4de952`・
   audit-summary 4件ともに
   `860b2e269e7e541518d4cab371eb80f679f730ef30fa7850c8d1a70e0d944c9c`。
   **ALL 67 GATES PASS・verdict agreements 2/2 (WIN=2 LOSS=0)・inconclusive 0・
   targets pass-one total third-impl expansions 33,075,229**
   (= 16,976,575 + 16,098,654)。
8. **tamper battery 4/4捕捉** (scratch copy上・適用実効性assert込み):
   T1 replica result反転 (aa006.p1 result 1→2) → replica-aa006-det-pair gate
   fail・T2 sources raw aa006.p1 nodes+1 → auditのraw sha pin gateが発火
   (誠実記録: 予想したmaker field gateよりsha pin層が先にABOTしたが、
   tamperは捕捉済み)・T3 input CSV aa006 legal 88→89 → G0
   input-aa006-matches-rows fail・T4 audit PIN_THIRD末尾反転 → pin-third_impl.js
   gate fail。battery後の実験dir全ファイルbyte不変を再検証 (commit-pinned
   fetch-backでA 40/40・B 23/23再照合)。
9. **status.log**: 10行RUN形式 (ng1/ng2/k02a a/b/l1a a/b/aa006 a/b/aa007 a/b・
   Part CC体裁と同一)。

## 出版記録 (observed HEAD `7aaa0525` 時点で対抗宣言なし・実験dir 404確認済み)

- Commit A `447ff294` (40 files: scripts 6 + input 7 + sources 15 +
  val-gate 12) → fetch-back 40/40 byte-identical。
- Commit B `486c1a6a` (23 files: output全件) → fetch-back 23/23 byte-identical。
- Commit C: 本README + `MANIFEST-sha256.txt` (全64エントリ sha256機械生成・
  MANIFEST自身は対象外)。
- 実務上の偏移 (正直開示): 宣言protocol §9のA/B配分は「A = val-gate 8 (published
  のみ)・B = val-gate this-host 4を含むoutputs」だったが、実際のpushはAに
  val-gate 12件全体 (published 8 + cg-host 4) を含め、Bはoutput 23件のみとした。
  出版内容の集合は宣言と同一 (計63 data files)。solver実行はすべて宣言後。

## 解釈ガード

- aa006/aa007の第三実装clean verdict一致と本host replica node-exact再現は、
  両キーの **unconsumed closure WIN候補としてのverdict-level
  three-implementation corroboration文献**である (Part CC aa001/aa002・Part CM
  aa008/aa009と同型)。採用はscrutiny owner C++第二実装 gate `9193f5b6…` 通過後の
  別adoption Part (pinned merger `90711961…` 経由) のみ・本レーンは代行しない。
  canonical cache (Part CO merged 6,301行 `854800f3…`・Part CH merged 6,294行
  `3124461b…`) はread-only不変。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa006/aa007を
  含む) は本実験のどの時点でもUNKNOWNのまま。** nodes・expansions・ttHits数・
  wall秒数を勝敗として読まない。被覆・secured・root勝敗の主張をしない。
- 不接触: Part CP batch-30 drive-2 (class 34269・並走所有)・Part CI takeover
  batch-29 (class 2251・並走所有)・batch-28のEXHAUSTED 11行の高budget再probe
  (別宣言条件)・batch 1..27各published dir (不変)。
