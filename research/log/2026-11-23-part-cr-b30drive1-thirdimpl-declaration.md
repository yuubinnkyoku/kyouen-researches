# Part CR 宣言 (2026-11-23): batch-30 (class 34269) drive-1 4行 (ac001/ac002/ac003/ac004) 第三実装交叉検証 — publish-then-execute

単一オーナー: n11中央応答長期レーン (本セッション本host)。対抗宣言なし
(push直前の最新main最近コミット機械走査で batch-30 drive-1行の第三実装交叉
検証・「Part CR」・「class 34269 thirdimpl」の言及ゼロを確認の上で出版する・
observed HEADまたはその再取得HEADを本宣言push時にコミットメッセージへ明記)。

## 1. スコープ

Part CP batch-30 (closure class 34269) drive-1で出版済みの **4行**
(ac001 LOSS nodes 5,635,468 / ac002 WIN nodes 10,752,246 / ac003 WIN
nodes 8,036,766 / ac004 LOSS nodes 5,816,333・いずれも2-pass fresh-cold
node-exact・verdict不消費のunconsumed honest label) に対する
(a) pinned第三実装 (`third_impl.js` `08ea958f…`・非df-pn AND/ORミニマックス)
によるverdict-level交叉検証 (2-run determinism pair a/b)、
(b) 本host pinned-replica (`jsreplay.js` `84585617…`) 2-pass fresh-cold再現、
(c) Part CO 7-LOSS adoption出版物 (merged canonical cache `854800f3…` 6,301行 /
increment `bd5ef7d7…` / increments-manifest `b47e07ca…`) に対する
unadopted補強gate (4行がcanonical採用系列のどこにも現れない機械保証)、
を実行・出版する。**verdict不消費** (4行はhonest labelのまま・新規採用・
解放・閉鎖は一切なし・採用はscrutiny owner C++第二実装 gate pin
`9193f5b6…` を経て別adoption Part (pinned fail-closed merger `90711961…`
経由) のみ)。閉鎖・被覆・secured・root勝敗の主張はしない。結果は宣言で
非予告 (下記はゲート設計の事前登録であって勝敗の予告ではない)。

誠実な開示: batch-30 drive-1 (acu001..ac004の出版元) は Part CP実行hostの
単一環境出版物であり、4行の第二実行環境同時再現は出版されていなかった。
本Partのthis-host pinned-replica 2-passが4行の最初の独立セッション再現
となる (実行hostの物理的相違までは主張しない)。

## 2. 対象 (published正本から機械導出済み・maker `make_inputs_cr.py`)

- **ac001** (LOSS行): key (1152921504758890496, 68719476736)・s5 36668・
  membership 2・legal 88・published result 2・nodes 5,635,468。
- **ac002** (WIN-HALT行): key (10376293541479448576, 68719476736)・s5 38891・
  membership 2・legal 87・published result 1・nodes 10,752,246。
- **ac003** (WIN-HALT行): key (1153484454578094080, 68719476736)・s5 178184・
  membership 2・legal 85・published result 1・nodes 8,036,766。
- **ac004** (LOSS行): key (1152921779502579712, 68719476736)・s5 257581・
  membership 4・legal 89・published result 2・nodes 5,816,333。
- anchors k02a (clean WIN result 1・expansions 9,106,337・ttHits 4,991,527) /
  l1a (clean LOSS result 2・expansions 7,660,602・ttHits 3,951,175) と
  negatives ng1/ng2 (derived legal/stones mismatch GATE_FAIL) はPart CMと
  同一のpublished定数 (provenance chain AR→BF→BK→BM→BS→BV→BW→BX→BY→CC→
  CL→CM→CR・input CSVはpublished Part BF byte-equality)。

## 3. sources pin (commit-pinned raw fetch・全sha256機械照合済み)

batch-30 kit (scaffold commit `281d58e6`のMANIFEST): batch-keys
`79fbd166…`・README-cp `94bf0517…`・published-input ac001..ac004
4ピン・val-gate baselines `6e902ab1`/`eeafe3ac`/`8035fe54`/`91dffdec`
+ input CSV 2ピン。drive-1 outputs: **raw 8ファイルはPart CP drive-1
完了log (`9903944e…`) の9行pin表から機械転写** (手転写ゼロ・
sha再照合済み)・status-cp.log `43fcad17…` (9行・開示済みv1 harness由来の
重複3行を含むまま)。Part CO: merged `854800f3…`・increment
`bd5ef7d7…`・manifest `b47e07ca…`・merger `90711961…`。完了log
pin表との機械一致もmaker gate。

## 4. kit設計 (宣言後にscaffold出版)

- 実験dir: `research/experiments/n11-centralreply-closure-class34269-batch30drive1-thirdimpl-20261123/`
- scripts: `third_impl.js`/`verify_tbl.js`/`jsreplay.js`/`run_thirdimpl.sh`
  はPart CM kitのbyte-clone (sha `08ea958f`/`c8c52528`/`84585617`/
  `a0b77d83`)。`make_inputs_cr.py` (Part CM maker `f926b5be…`のfork・
  宣言済みdelta: CP sources・4 target battery (verdict両kind)・
  Part CO unadopted battery・完了log pin表gate)・`audit_cr.py`
  (Part CM audit `3f9a29fa…`のfork・同一delta・schema
  `n11-centralreply-closure-class34269-batch30drive1-thirdimpl-audit-v1`)・
  session-local `run_replica_cr.sh` (1キー/p1+p2・timeout 260 wrap・
  stop rulesなし・drive semanticsとは独立)。
- input/val-gate/sources: maker出力 (rows.json schema
  `…-input-v1`・targets 4・anchors 2・negatives 2) +
  published byte-copies。val-gate baselines 4組 (sanctioned at2m×2 /
  first-15m / second-15m) はbatch-30 kitのbyte-copy。
- publish-then-executeに対する正直開示: **宣言前に本hostで実施したのは
  read-only解析のみ** (kit取得・sources sha機械照合・maker x3実行byte-stable
  [sha `37f55157…` (rows.json入出力)]・solver実行ゼロ)。

## 5. 事前登録protocol (宣言後の実行順・全てmachine-gated)

1. **rules gate**: `verify_tbl.js` (pinned byte-clone・knowledge lane-kit
   のpublished `jsreplay.js` saltを用いたTBL対比) — replica quads 95,670
   == mine quads 95,670・triples 195,044点mismatches 0を期待 (Part CMと
   同一機体・同一期待値)。
2. **val-gate fresh 4/4**: 本host fresh実行 (at2m 2キー budget 2,000,000
   exhaustion result 0 nodes 2,000,000 ×2・first-15m result 2 nodes
   3,651,923・second-15m result 2 nodes 5,040,200)・published baselinesと
   node-exact (wall_s比較外)・`.cr-host.out` 4件を出版 (audit G7)。
3. **negatives 2/2 GATE_FAIL** (ng1 legal count mismatch derived=87
   declared=88・ng2 stone count mismatch bits=5 declared=6) — fail-closed
   設計どおりrc=1を期待。
4. **anchors 4/4**: k02a/l1a本host a/b determinism pair PASS・published
   第三実装値 (expansions/ttHitsまでも) 再現を期待。
5. **本host pinned-replica 2-pass ×4キー**: ac001/ac002/ac003/ac004の
   p1/p2 = published raw fields (result/nodes) node-exact一致を期待
   (EXHAUSTED 0・MISMATCH 0)。**4行の独立セッション再現**となる。
6. **targets 2-run determinism + verdict agreement 4/4**: 第三実装
   cap 300,000,000・wallcap 240・memo-power=22・a/b determinism pair・
   第三実装verdictがpublished replica verdictと一致することを期待
   (cleanのみverdict・runlimitはhonest WALL-INCONCLUSIVE・DIVERGENCEは
   反証として記録)。
7. **audit x3 byte-identical**: `audit_cr.py` ALL GATES PASS・3回実行の
   audit-summary.jsonがbyte一致 (timestamp不読)・
   unadopted battery (raw pins×8・merged `854800f3` 6,301行・row絶対
   absent・increment 7行byte-exact・manifest id-list全走査) PASS。
8. **maker tamper battery (scratch copy上)**: 少なくとも (T1) raw p1
   nodes+1・(T2) 完了log pin表sha改変・(T3) README-cp文言反転・(T4)
   status-cp PASS verdict反転・(T5) published-input legal反転・(T6)
   BF anchor lo+1・(T7) batch-keys s5_index+1・(T8) merged-cache採用行
   nodes+1 の8種全部fail-closed ABORT検出。各tamper適用実効性assert。
9. **audit tamper battery + clean control (scratch copy上)**: 少なくとも
   (T1) PIN_THIRD末尾反転・(T2) target det-pair破壊・(T3) input CSV vs
   rows.json不一致・(T4) merged-cache pin改変の4種GATE FAILED検出 +
   clean control byte-identical PASS。
10. **status.log機械生成**: PROTOCOL行は全出力確定後に出力ファイル群から
    機械生成 (Part CMと同型・判定には無影響)。

## 6. 期待機械簿記 (事前登録・勝敗の予告ではない)

- 意味論: 第三実装verdict一致 (期待: ac001 third=2 replica=2・ac002
  third=1 replica=1・ac003 third=1 replica=1・ac004 third=2 replica=2)
  が得られた場合にのみ **three-implementation corroboration**
  (published CP replica 2-pass + 本host replica 2-pass + 第三実装
  minimax 2-run) が4行で成立する。nodes/expansions/ttHits/wall_sは
  bookkeepingであり勝敗ではない。第三実装の拡張数がpublished df-pn
  nodesと異なる値をとることは既知の設計差 (Part CM: 比率≈1.18)。
- unadopted: 4行ともPart CO merged canonical cache 6,301行に絶対現れない
  (machine-gated)・canonical cache `854800f3…`はread-only不変。
- 本Partはdrive-2 (ac005..ac054・Part CPオーナー進行中) と完全に独立:
  drive-2の行は本Partでは1行も扱わない。

## 7. UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて)・
class 2251 (batch-29全キー)・class 34269 (batch-30全54キー・ac001..ac004
を含む) は本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数・
expansions数・ttHits数・wall秒数を勝敗として読まない。WIN採用は
scrutiny owner C++第二実装 gate (`9193f5b6…`) 通過後の別adoption Part
(pinned merger `90711961…` 経由) のみ (本レーンは代行しない)。
被覆・secured・root勝敗の主張をしない。

## 8. 不接触

Part CP drive-2 (batch-30 ac005..ac054・宣言 `7aaa0525`進行中) のdir・
outputs・進行 (本Partはdrive-1完了出版物のみを読む)、Part CI takeover
(batch-29 class 2251) のdir・outputs・進行、Part CG re-takeover (aa006/
aa007・宣言 `b8ae515b`) のdir・outputs・進行、batch 1..30各published dir
(不変)、BASE caches (`3124461b…`・`854800f3…`) read-only不変、fast lane
(K1273以降)・finite-field lane・inversive lane・19root計画、EXHAUSTED行の
高budget再probe (別宣言条件)・scrutiny owner C++ gate (`9193f5b6…`)
専権事項。
