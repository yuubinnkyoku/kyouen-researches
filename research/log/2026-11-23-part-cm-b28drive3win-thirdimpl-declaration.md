# Part CM 宣言: batch-28 (class 5343) drive-3 WIN-HALT行 aa008/aa009 第三実装交叉検証 + 本host pinned-replica 2-pass + 未採用WIN行補強 (publish-then-execute・2026-11-23)

単一オーナー・publish-then-execute。本宣言の出版後に実行する。実行前に読み取り
専用で行ったのはkit取得・sources sha検証・maker 4回実行byte一致のみ (下記
「宣言前の正直開示」)。

## 対象 (すべてpublished正本から機械導出)

Part CJ (batch-28 drive-3・宣言 `42cecf36…`・outputs B `55fe0a81`・README+MANIFEST
C `eed9f348`) で出版された **drive-3 wave-1の2 WIN-HALT行**:

- **aa008**: key (1171516445255794704, 0)・s5 140489・membership 4・legal 85・
  budget 15,000,000・result 1 (WIN行)・nodes **5,270,340** (2-pass node-exact)。
- **aa009**: key (1747977197559218176, 0)・s5 142299・membership 4・legal 91・
  budget 15,000,000・result 1 (WIN行)・nodes **7,319,605** (2-pass node-exact)。

意味はroute statementのみ (**unconsumed closure WIN候補34/35番目**)。**verdict不消費**。
aa008/aa009はhonest WIN labelのままで、採用はscrutiny owner C++第二実装 gate pin
`9193f5b6…` を経て別adoption Part (pinned fail-closed merger `90711961…`) のみが
行える。閉鎖・被覆・secured・root勝敗の主張はしない。**標準11×11空盤・19
central-reply roots・class 5343 (54キーすべて・aa008/aa009を含む) はどの時点でも
UNKNOWNのまま。** nodes数・expansions数・wall秒数を勝敗として読まない。

## 実験dir・kit (Part CL/CC byte-clone構成)

- 実験dir: `research/experiments/n11-centralreply-closure-b28drive3win-thirdimpl-20261123/`
- scripts (pinned byte-clone・変更なし): `third_impl.js` `08ea958f…` (非df-pn
  AND/ORミニマックス第三実装)・`verify_tbl.js` `c8c52528…`・`jsreplay.js`
  `84585617…` (C++ STANDALONE EXACT REPLAY pathのNode.js replica)・
  `run_thirdimpl.sh` (1 solver/1 row/1 process・cap 300M・wallcap 240・memo
  power 22)。session-local: `make_inputs_cm.py` (inputs/rows.json機械導出・
  fail-closed・published Part CL maker `177c4409…` 適応) と `audit_cm.py`
  (gate battery・published Part CL audit `edf0ae7c…` 適応)。provenance chain
  AR→BF→BK→BM→BS→BV→BW→BX→BY→CC→CL→CM。
- sources (commit-pinned raw fetch・sha256全機械照合済み): status-cj.log
  `1a5c08c5…` (21行: PASS 9・WIN-HALT 6・EXHAUSTED 2・TRUNCATED-RETRY 4)・
  row-audit-cj `eb1d1e98…` (probed 9・win 6 [aa001,aa002,aa006,aa007,aa008,aa009]・
  loss [aa003]・exhausted [aa004,aa005]・fileless 45 [aa010..aa054]・mismatch 0)・
  README-cj `3615b5c1…`・raw aa008.p1 `f87c2ae9…` / aa008.p2 `5546ed29…` /
  aa009.p1 `50c32fd5…` / aa009.p2 `d79fc6d8…`・published-input aa008
  `3aaf4e1b…` / aa009 `47ce8cf9…`・batch-keys `af19208f…`。未採用性補強用
  (read-only・Part CH出版物): merged canonical cache `3124461b…` (6,294行)・
  increment `dc857bfd…`・increments-manifest `017c7c30…`・merger `90711961…`。
- val-gate: published baselines 4キー (at2m×2 budget 2M・15m×2 budget 15M・
  published-baseline.out + input.csv・drive-3 kitのものとbyte同一を確認済み)。
  本host fresh `.cm-host.out` 4件を出版する。

## 宣言protocol (逐次実行)

1. **rules gate**: pinned `verify_tbl.js` — replica quads 95,670 == third-impl
   quads 95,670・triples 200,000点掃引 mismatches 0。
2. **val-gate this-host 4/4 node-exact**: pinned `jsreplay.js` vs published
   baselines (wall_s比較外・`# replay_done` + quads header必須・stdout+stderr
   統合で取得)。
3. **negatives ng1/ng2**: GATE_FAIL fail-closed設計どおり (rc=1)。
4. **anchors k02a/l1a a/b**: 本host node-exact・published第三実装値 (k02a
   result 1 exp 9,106,337 ttH 4,991,527・l1a result 2 exp 7,660,602 ttH 3,951,175)
   再現・a/b determinism PASS。
5. **本host pinned-replica 2-pass fresh-cold ×2 targets**: aa008 p1/p2・
   aa009 p1/p2 (`jsreplay.js` budget 15,000,000・fresh empty PnTT per pass)。
   published raw fields (result 1 nodes 5,270,340 / 7,319,605) との一致を
   audit G2bで機械検査。EXHAUSTED 0・mismatch 0を期待 (不一致は全量報告)。
   drive-3 host (Part CJ) の単一環境出版物に対する第二実行環境での再現を
   目指す (実行hostの物理的相違までは主張しない)。
6. **第三実装 targets a/b ×2**: `run_thirdimpl.sh` 1 row/1 process。期待:
   aa008/aa009とも clean result 1 (WIN) verdict agreement 2/2。DIVERGENCE
   (clean 0/2一致など) の場合はfail-openに全量報告しverdict不消費を維持。
7. **status.log機械生成** (PROTOCOL 1..10)。
8. **audit `audit_cm.py` 3回実行byte一致** (ALL gates PASS・決定的)。
9. **maker tamper battery 8種** (scratch /tmp copy上・適用実効性assert・
   battery後の実験dir bytes不変検証)。
10. **audit tamper battery 4種** (scratch copy上・clean control PASS・実験dir
    bytes不変検証)。

audit gate群 (published Part CL `edf0ae7c…` からのdeltaは宣言済み): G0 input
CSV×rows.json (61-bit key Python int完全一致)・G1 pinned scripts×3 + rows-schema
(`consumed_into_canonical_cache: false` + `unadopted_win_rows: true` +
canonical cache sha不変pin) + target-count (2 WIN行)・G2 rules gate×2・G2b
replica再現×2 targets (present/done/quads/det-pair/schema/key/verdict-vs-
published)・G3 anchors×2・G4 negatives×2・G5 targets (key/legal/quads/det-pair/
verdict-agree)・**G6 (新設) 未採用WIN行補強**: raw pin aa008/aa009 p1/p2×4・
merged cache pin `3124461b…` + 6,294行 + 対象row不在 (0回) + 同key競合row
ゼロ・increment pin (aa003単一rowのみ)・manifest pin + loss_ids [aa003] +
unadopted_win_ids [aa001,aa002,aa006,aa007] + row_counts (wins 4・fileless 47) +
**対象idがmanifest内のいかなるid listにも不在** (注記文中のfileless範囲言及
"aa008..aa054"はid listでなく許容・機械区別済み)・**G7 val-gate 4/4 node-exact**。

## 結果の出版

scaffold A (scripts・sources・val-gate baselines) → outputs B (raw 4・val-gate
cm-host 4・anchors 4・negatives 2・rules-gate・status.log・audit runs) →
README C + MANIFEST-sha256 (全ファイルpin・commit-pinned raw fetch-back全件
byte照合)。出版メッセージにverdict不消費を明記。

## 宣言前の正直開示

- 宣言出版前に実施したのは: kit取得 (commit-pinned raw・sha256全照合)・
  sources battery検証・`make_inputs_cm.py` 4回実行byte一致 (input 7ファイル
  同一digest・verdict計算は未実行)。publish-then-execute規約に対する逸脱として
  正直に開示する (Part CLと同型・宣言前探査は本宣言から実行へ影響しない)。
- Part CK採番事故の教訓: 本宣言のpush直前に最新mainを再取得し、Part採番の相剋
  (CM既使用・aa008/aa009第三実装レーン宣言の有無) を確認済み。相剋検知時は
  改番して再出版する。

## 非干渉

Part CG (aa006/aa007 thirdimpl・宣言 `38770f4c` outputs未出版)・Part CK
(batch-28 drive-4 aa010..aa054・宣言 `ad269701`)・Part CI (batch-29 probe
ab001..ab054・宣言 `efd2d488`)・Part CL (aa003完結) は非接触。本Partは
published aa008/aa009行のread-only交叉検証のみを行い、cache・manifest・他
Partの成果物には一切書き込まない。
