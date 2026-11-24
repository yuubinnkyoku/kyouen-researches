# Part CV 単一オーナー宣言: batch-29 (closure class 2251) checkpoint-1/3 の row-audit + 全16キー pinned-replica + 第三実装交叉検証 (publish-then-execute)

- 仮採番: **Part CV** (時刻はpush体に記録)・単一オーナー: 本宣言セッション。
- observed HEAD (宣言前最終確認・fetch): push時にlist_commitsで機械確認し、対抗宣言がないことを認証付きコミット一覧で確認する (下記「対抗確認手順」のとおり、push直前にPart CU宣言 d8276573 を検知して本レーンをCVに改番済み)。
- 対象: published **Part CI takeover checkpoint 1/3** (batch-29, closure class 2251, rank 35) の
  **ab001..ab016 16行** (公開値: 16 LOSS / 0 WIN / 0 EXHAUSTED, 2-pass fresh-cold budget 15M,
  commit `a5a159d7` の同dir output/, dir `n11-centralreply-closure-class2251-batch29-20261123`)。
- 本Partの位置づけ: Part CI scaffold README が「**row-auditは別セッションで実施予定**」と明記した委任作業の実行、
  およびPart CG/CL/CM/CR系の交叉検証方式 (this-host pinned-replica + 第三実装 third_impl.js) の適用。
  **Part CIのdrive continuation (ab017..ab054のprobe) はPart CIオーナーの専権レーンであり本Partは一切接触しない**
  (停滞takeoverの要不要は本宣言の対象外・別宣言条件)。**Part CU (batch-29 16-LOSS canonical adoption・宣言 d8276573
  00:14:48Z) は並走非接触レーン**: 本Partのrow-audit/replica/第三実装は採用とは独立に成立する検証資産であり、
  採用の可否はPart CUが pinned merger `90711961…` で決する (本Partは関与しない)。Part CT (aa050 30M reprobe) は
  宣言直近の最新mainで完了 (WIN解決・完了log 30af9f49) したことを確認済み・非接触。
  K1274/K1275 (ストリップレーン)、その他すべての並走レーンに非接触。
  BASE canonical cache `854800f3…` (6,301行) は read-only 不変のまま本Partのsourcesにbyte-pinして使用する
  (Part CU採用後の新cacheが生じても本Partのsource pinはd06c4d92時点のbyte正本のまま変更しない)。

## 宣言前探査 (read-only・本宣言前に実施・全開示)

1. batch-29実験dirのckpt-1/3 bytes を commit-pinned (HEAD `d06c4d92`) でfetchし、
   sha256 73エントリの機械pin表 `sources/pins-b29ckpt1.json` を生成
   (**sha256 `59cd84093bac8a0e114913a6dedf38069ba27980a7fc20a59e606b9ddc1fb60f`**。
   pin対象: sources/… 32 raw + status-ckpt13.log + batch-keys-b29.json + canonical cache
   `854800f3…` + Part CR出版 anchor/negative third-impl 出力4+2件 + scripts byte-clone 4件 +
   input csv 20件 + val-gate baseline/input 8件)。
2. published bytesの機械検査 (solver実行なし):
   - 16/16キーとも p1==p2 が (id,stones,legal,is_or,budget,result,nodes,lo,hi) 全字段で完全一致 (wall_sのみ自由)。
   - `replay_done` 32/32・quads header 95670 32/32・budget=15,000,000 32/32・stones=5/order id=0 32/32。
   - status.log は正確に16行・すべて PASS。16/16が raw (budget,result,nodes) と完全一致。
     HALT/EXHAUSTED/MISMATCH/TRUNCATED行ゼロ。
   - batch-keys.json: lo/hi/legal/s5_index 16/16完全一致。
   - **全16行 result=2 (LOSS・honest label・adoption候補のみ・不消費)**・nodes合計 **57,463,971**。
     ノード数を勝敗として読まない。WIN/EXHAUSTED ゼロ (commit a5a159d7の公開主張と機械一致)。
3. 第三実装・anchor・negative資材: Part CR出版kit (dir `n11-centralreply-closure-class34269-batch30drive1-thirdimpl-20261123`)
   から: `third_impl.js` (`08ea958f…`)・`run_thirdimpl.sh` (`a0b77d83…`)・出版anchor出力
   k02a (result 1, expansions 9,106,337, ttHits 4,991,527), l1a (result 2, expansions 7,660,602, ttHits 3,951,175)、
   negative ng1 (legal count mismatch: derived=87 declared=88), ng2 (stone count mismatch: bits=5 declared=6)。
4. `make_rows_cu.py` が sources/のbyte列のみから機械生成した `input/rows.json`
   (**sha256 `c144e2a66be274cc0ab3cb3fd3173ed9b68ae2652fd25fc9b590fd83c5a330bd`**・手転写ゼロ・61-bit lo は
   精密Python intとしてraw/csv/batch-keysの三方一致をfail-closed検証の上で使用)。
5. **本宣言時点で solver は一度も実行していない** (read-only探査と機体組立のみ)。

## 事前登録: 実行quotaと期待値 (protocol D1-D9)

- D1 (A commit): kit一式 (scripts 8・input 21 (16+4+rows.json+…)・val-gate 8・sources 41・計78ファイル)
  を実験dir `research/experiments/n11-centralreply-class2251-b29ckpt1-audit-thirdimpl-20261124/` にpush。
  実行前にpush。全ファイルのfetch-back sha256照合が前提。
  kit pins: pins.json `59cd8409…`・rows.json `c144e2a6…` がpush時にbyte不変であること。
 保驾byte-clone: jsreplay.js `84585617…`・runbatch.sh `f591f8c2…`・third_impl.js `08ea958f…`・
  run_thirdimpl.sh `a0b77d83…` (改変ゼロ。replica出力が output/raw/ なのはpublished runbatch.shの設計踏襲)。
- D2 (val-gate fresh): `run_valgate_cu.sh` で val-gate 4キー this-host実行 (fresh-cold 1-passずつ)。
  期待 (published baseline とnode-exact): at2m 2キー = result 0, nodes 2,000,000 (budget 2M exhaustion) ×2、
  first-15m = result 2, nodes 3,651,923 (budget 15M)、second-15m = result 2, nodes 5,040,200 (budget 15M)。
- D3 (pinned-replica): published `runbatch.sh` byte-clone で16キー全てを本hostで 2-pass fresh-cold
  (budget 15M・並列度4以内)。**事前登録期待値 (published値。node-exact再現を要求)**:
  ab001: 2/4,265,342・ab002: 2/3,662,776・ab003: 2/4,447,441・ab004: 2/2,687,012・
  ab005: 2/3,714,648・ab006: 2/3,855,756・ab007: 2/3,763,776・ab008: 2/2,890,562・
  ab009: 2/1,786,048・ab010: 2/4,242,063・ab011: 2/4,806,135・ab012: 2/2,606,954・
  ab013: 2/2,284,195・ab014: 2/4,280,600・ab015: 2/3,912,106・ab016: 2/4,258,557
  (いずれも p1==p2 かつ published p1/p2双方と一致。逸脱は誠実記録)。
- D4 (第三実装): `run_thirdimpl.sh` byte-clone で targets 16キー×2 run (a,b) + anchors k02a/l1a×2 +
  negatives ng1/ng2×1。期待: (a) anchors = published第三実装値の完全再現
  (k02a: clean result 1, expansions 9,106,337, ttHits 4,991,527;l1a: clean result 2, expansions 7,660,602,
  ttHits 3,951,175)・(b) negatives = 出版GATE_FAIL文言と機械一致・(c) targets = a/b det-pair clean +
  **third=replica=2 のverdict agreement 16/16** (three-implementation corroboration)。targets の
  expansions/ttHits は初観測のため事前登録値なし (実測をB commit機械記録する。宣言設計上の非登録点)。
  wall-cap 240s超過時は WALL-INCONCLUSIVE gate fail として誠実記録 (verdict主張しない)。
- D5 (fail-closed audit): `audit_cu.py` を3回実行し stdout/json byte-identical + all gates PASS。
  gate構成 (機体順序): P0 pin層 (pins table自体のpin・schema・全73エントリ照合) → G0 rows構造 →
  G1 published証拠整合 (3×16 + status 3種 + batch-keys + 公開主張16-LOSS機械検 + rows再導出一致) →
  G2 replica 7×16 (present/done/quads/det-pair/schema/key/**node-exact-vs-published**) →
  G3 anchors (2×8) → G4 negatives (2) → G5 targets (9×16: present/2×(key/legal/quads)/det-pair/verdict-agree) →
  G6 unadopted (canonical cache pin 854800f3…・6,301行・16キーのrow/key衝突ゼロ = verdict不消費の機械担保) →
  G7 val-gate (3×4)。**機体実装から機械的に定まるgate総数計算値: 352** (実装・ドリフト時は誠実記録)。
- D6 (tamper battery): `tamper_battery_cu.sh` で7変異 + control。**事前登録**:
  T1 replica ab002.p1 nodes 3662776→3662777 → `replica-ab002-det-pair`・
  T2 third ab005.b expansions+1 → `third-target-ab005-det-pair`・
  T3 third ab009 a+b result 2→1 → `third-target-ab009-verdict-agree`・
  T4 replica ab012.p2 replay_done行削除 → `replica-ab012-done`・
  T5 sources/raw ab013.p2 nodes+1 → `pin-all-73`・
  T6 canonical cacheに偽装採用行 append → `pin-all-73`・
  T7 anchor l1a.a expansions 7660602→7661602 → `anchor-l1a-a-expansions`・
  CONTROL 無変異copy → rc=0 ALL PASS。各変異はfrozen kit copyへ適用し本体kitは無傷。
- D7 (B commit): outputs (val-gate host 4・replica raw 32・targets 32・anchors 4・negative 2・status.log・
  audit-run1..3.txt・audit-summary*.json 4種・tamper-battery.txt) をpush・fetch-back全照合。
- D8 (C commit): README + MANIFEST-sha256 (出版全ファイル分)・fetch-back全照合。
- D9 (完了log): 本Partの実行記録として別logをpush。

## UNKNOWN担保・採用規約 (不変)

- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 2251 (54キーすべて・本Partの16キーとそのLOSS行を含む)・class 34269 ほか全キーは
  どの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数・wall秒数を勝敗として読まない。
- 16 LOSS行のverdictは**本Partでは不消費** (honest label = adoption候補のみ)。採用は別宣言のadoption Part
  (pinned fail-closed merger `90711961…` 経由) のみ。第三実装一致は採用ではない。
  並走Part CUが宣言済みの採用を行う場合、採用時刻との前後は出版順で記録し、本PartのG6 gate
  「本Partがcacheに書かないこと・pin済み854800f3に16キーが存在しないこと」は採用の有無に依らず成立する。
- canonical cache `854800f3…` (6,301行) は本Partで一度も書き換えない (G6で機械担保)。
- 閉鎖・被覆・secured・root勝敗の主張をしない。

## 対抗確認手順

push前にlist_commitsで最新mainを再取得し、(a) 本ノートパスが既存でないこと、
(b) 対抗する batch-29 ckpt-1/3 row-audit/replica/thirdimpl 宣言が出ていないことを機械確認する。
競合・同時push・取得失敗時は無理に押し進めず状況を記録して次回実行に回す。

## 実行環境の開示

本sandbox (Node v22.20.0・Python 3.12.14)。CPU並列は4以内。長時間占有なし・中間巨大ファイルなし。
失敗・timeoutも実験事実として全てstatus.logと本Partの記録に残す。
