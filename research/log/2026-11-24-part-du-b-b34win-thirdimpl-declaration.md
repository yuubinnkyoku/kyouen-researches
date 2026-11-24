# Part DU-b 単一オーナー宣言: batch-34 small-pocket WIN 2行 (ag001 / ag002) 第三実装交叉検証 (publish-then-execute)

- 仮採番: **Part DU-b** (時刻はpush体に記録)・単一オーナー: 本宣言セッション。
- observed HEAD (宣言前最終確認・fetch): `ca42291b` (21:03:37Z。
  push時に再度list_commitsで機械確認し、対抗宣言・
  同名実験dirの不在を認証付きコミット一覧とtree APIで確認する)。
- 対象: published **Part DU batch-34** (small-pocket closure classes 23101 / 1849
  last-unknown-children probe) の **WIN 2行**:
  - **ag001** (class 23101, s5 745184): key (1152921505747697664, 1032)・legal 85・
    2-pass fresh-cold budget 15M・result **1 (WIN)**・nodes **9,149,084** (48/47s)。
  - **ag002** (class 1849, s5 81011): key (1153485622925590528, 0)・legal 88・
    2-pass fresh-cold budget 15M・result **1 (WIN)**・nodes **4,893,014** (25/24s)。
  outputs commit `1039a95d000...` (実験dir
  `n11-centralreply-closure-smallpockets-batch34-20261124`)。宣言 `5ec15665`・
  kit `a0d40d47` は DU 宣言どおり fetch-back byte検証済みの出版物。
- 本Partの位置づけ: Part CZ方式 (`n11-centralreply-closure-b29ab028win-thirdimpl-20261124`)
  のWIN行交叉検証 (pinned第三実装 third_impl.js によるverdict-level一致 + 本host
  pinned-replica 2-pass再現 + val-gate fresh + rules gate + unadopted機械gate) を
  b34の2行に適用。**verdict不消費** (両行ともhonest labelのまま。採用・解放・閉鎖は
  一切なし。WIN採用はscrutiny owner C++第二実装 gate
  (`cpp/solvers/kyouen_dfpn_root.cpp` pin `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`)
  経由で別adoption Part のみ。本実行環境にC++コンパイラがなく同gateを実行不能な事実は
  Part DU宣言に記載済みで不変)。閉鎖・被覆・secured・root勝敗の主張はしない。
- 並走レーン (K1303 pre-diag fast lane・PG(2,9)盤面系・その他) に非接触。
  canonical cache `973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b`
  (6,547 s5verdict行) は read-only 不変のままsourcesにbyte-pinして使用する。

## 宣言前探査 (read-only・本宣言前に実施・全開示・solver未実行)

1. **published bytes検査** (commit `1039a95d` 正本をfetch・sha256全照合):
   - raw 4件: ag001 p1 `3ac9ab81…` / p2 `829b960a…`・ag002 p1 `f99796ae…` / p2
     `7ab4cbb4…`。両キーとも p1==p2 が (id,stones,legal,is_or,budget,result,nodes,lo,hi)
     全字段一致 (2-pass node-exact)・`replay_done`・quads header 95,670・budget 15,000,000。
   - status.log `2b5c0aa5…`: 正確に4行 = ag001 PASS + WIN-HALT・ag002 PASS + WIN-HALT。
     PASS行の (budget,result,nodes) が raw と完全一致・EXHAUSTED/MISMATCH/TRUNCATED行ゼロ
     (commit主張と機械一致)。
   - batch-keys-b34.json `47754a70…`: lo/hi/legal/s5_index/serving_class/
     membership_class_count/canonical_cache_same_lo_rows_context 2/2完全一致。
   - **両行 result=1 (WIN行・honest label・adoption候補のみ・不消費)**。nodes数を勝敗として読まない。
   - canonical cache `973bcd19…` (6,547行): **両キーの exact (lo,hi) 組は不在**
     (ag001は same-lo 8行存在するが全て hi != 1032 の別位置・ag002は lo 自体が不在。
     WIN/LOSS conflictなし)。same-lo コンテキスト計数 8/0 が batch-keys
     `canonical_cache_same_lo_rows_context` と機械一致。
2. **kit組立**: published bytesを `sources/` にbyte-pin (raw 4・status-b34.log・
   batch-keys-b34.json・published target CSV 2・CZ chain anchor/negative CSV 4・
   canonical cache 1 = 14ファイル) + scripts (byte-clone 6 + DU-b新規4) +
   val-gate 8 (published batch-34 kit byte)。Fisher探査にsolverは使っていない。
3. **maker `make_inputs_dv.py` (`cf6e0283…`)**: sources byte列のみから
   fail-closed gates M1-M6 (raw pin+2-pass+WIN・status 4行整合・batch-keys・
   anchor/negative pin・target CSV pin・canonical cache pin/same-lo整合/exact組不在) で
   input/ 6 CSV + rows.json を機械生成。**3回実行byte-identical**・rows.json
   **`e1aa1ecbe5045e8fd5d59cfb9ce1a81c1797fba0458e3549a2e3c84164919aa0`**。
   tamper battery 9変異 (M1 raw pin×2・M2 status nodes・M2 WIN-HALT欠落・M3・M5・M4・
   B34_KIT未設定・clean replica PASS対照) 全て想定gateでABORT。
4. **audit `audit_dv.py` (`2cecf421…`) 合成kit検証**: 期限前機体確認として
   想定出力を合成した仮想kit (third rowコピー・第三実装行は合成値・val-gate host行は
   baseline byteコピー) で **117 GATES ALL PASS ×3回 stdout byte-identical**。
   negative行は完全行byte比較 (parserのquote strip差をCZ実装と共有しない本実装の
   declared delta・rows.jsonの `expect_gate_fail_line` で完全行をpin)。
5. **tamper battery `tamper_battery_dv.sh` (`c1474235…`) 合成kit検証**: 10変異 +
   control、全て事前登録gateで検出 (下記D6のgate表どおり。T6はcache byte-pin gateが
   先発火することを合成kitで確認済み)。
6. **rules gate**: Part CZの `verify_tbl.js` `c8c52528…` の単一行diff版
   **`verify_tbl_b34.js` (`4ae13bff…`)**: require pathのみ
   `/home/user/knowledge/kyouen-research/_class1297036830122704896-lane-kit/inv/jsreplay.js`
   → `./jsreplay.js` (kit内byte-clone)。機能 diffなし。宣言開示済み。
7. **本宣言時点で本セッションは solver を一度も実行していない** (読み取り探査と機体組立のみ)。

## 事前登録: 実行quotaと期待値 (protocol D1-D9)

- D1 (kit commit): 本実験dir `research/experiments/n11-centralreply-closure-b34win-thirdimpl-20261124/`
  に **39ファイル** (scripts 10: jsreplay `84585617…` / runbatch `f591f8c2…` /
  third_impl `08ea958f…` / run_thirdimpl `a0b77d83…` / verify_tbl `c8c52528…` (diff base) /
  verify_tbl_b34 `4ae13bff…` / make_inputs_dv `cf6e0283…` / audit_dv `2cecf421…` /
  run_valgate_dv `a3f26c0b…` / tamper_battery_dv `c1474235…`・input 7: rows.json
  `e1aa1ecb…` + CSV 6 (pinはM4/M5)・sources 14・val-gate 8) をpush。
  宣言→kitの順でpushし、全ファイルfetch-back sha256照合が前提。
- D2 (val-gate fresh): `run_valgate_dv.sh` で val-gate 4キー本host fresh-cold 1-pass。
  期待 (published baseline と、replay行全字段 node-exact / wall_s除く):
  at2m 2キー = result 0, nodes 2,000,000 (budget 2M) ×2・
  first-15m = result 2, nodes 3,651,923 (budget 15M)・
  second-15m = result 2, nodes 5,040,200 (budget 15M)。
- D3 (pinned-replica): published `runbatch.sh` byte-clone で ag001 / ag002 を本hostで
  2-pass fresh-cold (budget 15M・逐次実行。**事前登録期待値 (published値。node-exact
  再現を要求)**: ag001 = `15000000,1,9149084`・ag002 = `15000000,1,4893014`
  (p1==p2 かつ published p1/p2双方と全字段一致。逸脱は誠実記録)。
  runbatch.shはWINで rc 45 (WIN-HALT) を返す設計 (byte-cloneなので変更しない)。
  この再現はb34 probe publication (前セッションhost) に対する**独立セッション再現**。
- D4 (第三実装): `run_thirdimpl.sh` byte-clone で targets 2キー×2 run (a,b) +
  anchors k02a/l1a×2 + negatives ng1/ng2×1。期待:
  (a) anchors = published第三実装値の完全再現 (k02a: clean result 1,
  expansions 9,106,337, ttHits 4,991,527・l1a: clean result 2,
  expansions 7,660,602, ttHits 3,951,175)。
  (b) negatives = 出版GATE_FAIL完全行とbyte一致 (`third,ng1a,5,88,,GATE_FAIL,"legal count
  mismatch: derived=87 declared=88"`・`third,ng2a,6,87,,GATE_FAIL,"stone count mismatch:
  bits=5 declared=6"`)。
  (c) targets = a/b det-pair clean + **third=replica=1 のverdict agreement 2/2**。
  targets の expansions/ttHits は初観測のため事前登録値なし (実測をB commit機械記録。
  宣言設計上の非登録点・CZ D4と同一規約)。
  **wallcap事前登録**: run_thirdimpl.sh byte-cloneの `--wallcap=240` を超えた場合
  (ag001の replica nodes 9.15M は CV corpus最大4.8Mより大きく要注意) は
  WALL-INCONCLUSIVE gate fail として誠実記録しverdictを主張しない。その場合に限り、
  初回byte-clone試行の記録出版後、diffが wallcap 240→1200 のみの派生runner
  `run_thirdimpl_dv2400.sh` をB commitで宣言開示の上再用し、両試行を出版する。
  cap 300,000,000 nodes は不変。
- D5 (fail-closed audit): `audit_dv.py` を3回実行し stdout byte-identical +
  ALL GATES PASS。gate構成 (機体順): rows.json pin → G0 input⇔rows一致 6 →
  script pins 5 + diff-declared 1 + rows/schema/targets構造 2 →
  published整合 (det-pair/key-scheme/claim-win×2 + status 4行 4 + batch-keys 1) →
  rules gate 3 → replica 7×2 → anchors 10×2 → negatives 2 → targets 9×2+all 1 →
  unadopted (raw pin csv 2×3 + cache pin/rowcount + same-lo/exact欠落 3×2 +
  anchor-neg pin 4) → val-gate 2×4。**機体実装から機械的に定まるgate総数計算値: 117**
  (合成kitで実測済み・実行時逸脱は誠実記録)。
- D6 (tamper battery): `tamper_battery_dv.sh` で凍結copyに10変異 + control。
  **事前登録** (合成kitで実測検証済み):
  T1 replica ag001.p1 nodes+1 → `replica-ag001-det-pair`・
  T2 third ag002.b expansions+1 → `target-ag002-det-pair`・
  T3 third ag001 a+b result 1→2 → `target-ag001-verdict-agree`・
  T4 replica ag001.p2 replay_done削除 → `replica-ag001-done`・
  T5 sources raw ag002.p2 nodes+1 → `published-ag002-det-pair`・
  T6 canonical cacheに偽装WIN採用行 append → `unadopted-pin-canonical-cache`
  (byte-pin gateが先発火・rowcountも失敗)・
  T7 anchor l1a.a expansions +10,000 → `anchor-l1a-a-expansions`・
  T8 negative ng1 declared 88→89 → `neg-ng1-failclosed`・
  T9 rules-gate.txt mismatches 0→3 → `rules-gate-tbl-mismatch0`・
  T10 val-gate host at2m nodes 2,000,000→2,000,001 →
  `valgate-at2m-s5-1152921504606851072-536870946-node-exact`・
  CONTROL 無変異 → rc=0 ALL PASS。各変異はfrozen kit copyへ適用し本体kitは無傷。
- D7 (outputs commit): status.log・val-gate dv-host 4・replica raw 4・
  third-impl targets 4・anchors 4・negative 2・rules-gate.txt・
  audit-run1..3.txt・audit-summary*.json 4種・tamper-battery.txt (+合成kit機体検証記録)
  をpush・fetch-back全照合。
- D8 (README + MANIFEST commit): 実験README + MANIFEST-sha256 (出版全データファイル分)・
  fetch-back全照合。README 自己除外は規約どおり。
- D9 (完了log commit): Part DU-b完了log + **Part DU本体完了log**
  (`2026-11-24-part-du-batch34-smallpockets-completion.md`: batch-34 probe実行記録・
  val-gate 4/4・2-pass WIN 2行・C++ gate実行不能の誠実記録・verdict不消費) をpush。
- 実行quota: D2~D6の合計solver時間は目安として合計~10分以内を予測するが、
  wallcap・timeout・環境リセットは誠実記録しquota超過だけで主張を変えない。

## UNKNOWN担保・採用規約 (不変)

- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 23101・class 1849 (両キーとそのWIN行を含む)・その他全キーは
  どの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数・wall秒数を勝敗として読まない。
- 両WIN行のverdictは**本Partでは不消費** (honest label = adoption候補のみ)。採用は
  scrutiny owner C++第二実装 gate `9193f5b6…` 経由で別adoption Partのみ。
  第三実装一致・replica再現は採用ではない。
- canonical cache `973bcd19…` (6,547行) は本Partで一度も書き換えない (G6で機械担保)。
- 閉鎖・被覆・secured・root勝敗の主張をしない。
- repoへの反映前は毎回最新mainを取り直す。pushの競合・同時書き込み・取得失敗が
  起きた場合は無理に押し進めず状況を記録して次回実行に回す。
