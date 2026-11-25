# Part EK — aj030/aj039 (class 30484) 2キー 30M re-probe kit (2026-11-25)

実験dir: `research/experiments/n11-centralreply-closure-class30484-aj030aj039-reprobe30m-20261125/`
宣言: `research/log/2026-11-25-part-ek-aj030aj039-reprobe30m-declaration.md`。

## 何であるか・何でないか

- Part EH (batch-39) が 15M 条件で EXHAUSTED (honest UNKNOWN) とした
  class 30484 の2キー aj030 = (1152922604135251976, 65536) (legal 83) と
  aj039 = (1152922606282735616, 65536) (legal 88) を、事前宣言済み予算
  30M 条件 (order=0・fresh-cold・share_tt=0) で再 probe する単一オーナー
  Part の kit。EH 完了log resume note #2・Part EI resume 候補②・
  Part EJ 宣言の guardrail が登録していた「高budget ladder の別宣言」を
  本 Part が引き受ける。
- **verdict は不消費。** result が LOSS でも canonical cache への採用は
  行わない (将来 Part の loss-only adoption が別途 pinned merger
  (`90711961…`) BASE `73482be0…` (Part EI chain head) で行う)。WIN なら
  probe-level WIN として scrutiny-owner C++ gate (`9193f5b6…`) 待ち
  (本環境は g++ 等コンパイラ不在を再確認済み)。EXHAUSTED@30M なら
  honest UNKNOWN (更なる高budget条件は別宣言)。
- **標準 11×11 空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 30484 (52キーすべて) は本 Part の前後を
  通じてすべて UNKNOWN のまま。** 勝敗・被覆・secured coverage の主張は
  本 dir のどこにもない。

## 構成 (kit = 本 README + MANIFEST + scripts 3 + input 5 + val-gate 8 + sources 7 = 23 files、
実行後に output ファイルを追加)

- `scripts/jsreplay.js` — Part EA/ED/EH/EJ kit byte-clone `84585617…` (変更なし)。
- `scripts/runbatch_ek-30m.sh` — Part ED 60M runner published bytes
  (`b0c5f714…`) の BUDGET 行 (60000000→30000000) 以外 byte 同一。
  派生 sha256
  `3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4`
  は published Part EA 30M runner の byte-clone と一致 (同一予算条件の
  runner bytes が先行 Publication に既存であることの確認済み)。
  two-pass fresh-cold・HARD-STOP on MISMATCH (rc=42)・truncated-sidecar
  guard・WIN-HALT (rc=45) / honest EXHAUSTED label は Part ED と同一。
- `scripts/audit_ek.py` — fail-closed audit (Part ED `audit_ed.py`
  `6f76e8e5…` の 2_target 拡張 fork)。全 kit pin・fresh-increment gate
  (canonical `73482be0` (6,712行) と quarantine `81d23160` への
  aj030/aj039 不在)・15M exhaustion 履歴・val-gate 4 行・anchor 3キー
  node-exact・本 probe raw p1/p2×2 (key/legal/budget/two-pass node-exact +
  honest label) を検査し `output/audit_ek.json` を書く。1 gate でも破損が
  あれば rc=1。
- `input/` — aj030 `520ee52a…` / aj039 `82f8dff3…` (batch-39 kit
  byte-clone) + anchor 用 aj001 `2f6daea5…` / aj049 `46349391…`
  (batch-39 kit byte-clone) / af039 `e51a3c9d…` (Part ED kit byte-clone)。
- `val-gate/` — Part EA/ED/EH/EJ kit val-gate 4行の byte-clone (input 2種 +
  published-baseline 4件・sha セット `ecc0299b`/`6e902ab1`/`56aacb71`/
  `eeafe3ac`/`8035fe54`/`91dffdec` 既存どおり)。fresh host 走
  `.ek-host.out` (実行フェーズで生成) との比較は wall_s 列を除く全
  replay 列一致で行う。
- `sources/` — b39-status.log (`08d70bb7…`・54行)・exh15m/aj030.p1.out
  (`843a0a0c…`) / aj030.p2.out (`661c8e41…`) / aj039.p1.out
  (`60ae21db…`) / aj039.p2.out (`c51899d5…`) (batch-39 EXHAUSTED raws)・
  canonical-cache-ei-merged-73482be0-20261125.cache (`73482be0…`・279,805B・
  Part EI chain head)・n11-s5-evidence-quarantine.json (`81d23160…`)。

## 事前登録 anchor / val-gate (宣言どおり)

- anchors (EK runner 30M cap・2-pass): aj001 → LOSS 5,156,075 (published
  b39 15M 条件値と同一 node = cap 非依存検証・class 30484 resolved 代表)・
  aj049 → WIN 4,998,452 (published b39 15M WIN anchor。runner は WIN-HALT
  rc=45・status.log に WIN-HALT 行。**verdict 不消費**)・af039 → LOSS
  19,234,232 (published Part EA 30M 条件値 (15M, 30M] budget-crossing
  regime 代表・ED 60M cap でも同一 node を再確認済み)。
- val-gate (published 条件 budget・1-pass fresh): at2m 2行 →
  EXHAUSTED (2000000,0,2000000)・first-15m → (15000000,2,3651923)・
  second-15m → (15000000,2,5040200)。
- anchor 合計は約 2×(5,156,075+4,998,452+19,234,232) = 58,777,518
  nodes/pass。val-gate 合計約 12,684,046 nodes 単走。

## 実行記録 (run record, 2026-11-25T13:55-14:20Z)

- 実行hostは Vibe upgraded sandbox (node v22.20.0, 2コア, コンパイラなし)。
  出版 chain は宣言 dd448fec → kit B1 5d54005e (24 files) → kit B2
  e33c3526 (canonical cache 279,805B) で、実行は B2 bytes からの
  clean-room 再構成 tree (MANIFEST rev1 pin 23/23 照合) で行った。
  途中 (anchors 並走の最初の同期呼び出しで 300s shell cap 超過)
  実行環境が reset され工作 dir が消滅したが、**全 kit bytes が出版済み
  fetch-back 検証済みだったため B2 bytes からの再構成 23/23 pin で
  完全に復旧**した (Part EE wave F と同じ復旧 pattern の再実証)。
  以後の長時間 pass は detached (nohup+disown) 起動 + cross-invocation
  監視 + truncated-sidecar guard (Part ED amendment 2a0c3318 型) で実行。
- val-gate 4/4 PASS (fresh host 走 `.ek-host.out`): at2m 2行 = EXHAUSTED
  (2000000,0,2000000)・first-15m = (15000000,2,3651923)・second-15m =
  (15000000,2,5040200)。published baseline と wall_s 列以外全 replay 列
  一致 (byte 一致は at2m 2行も含む)。**drive-start 要件満たす。**
- anchors 3/3 PASS (EK 30M cap・2-pass fresh-cold node-exact):
  aj001 = LOSS 5,156,075 (published b39 15M 条件値)・aj049 = WIN
  4,998,452 (WIN-HALT rc=45・verdict 不消費)・af039 = LOSS 19,234,232
  (published Part EA 30M 条件値・budget-crossing regime (15M,30M] 代表)。
- 本 probe (2 workers):
  - **aj030: p1/p2 = 30000000,1,15284699 (two-pass node-exact・wall
    181s/190s)。nodes は予算区間 (15M, 30M] にあり 15M EXHAUSTED 履歴と
    整合。probe-level WIN として WIN-HALT rc=45 を記録。verdict は
    不消費 (scrutiny-owner C++ gate `9193f5b6…` 専権)。**
  - **aj039: p1/p2 = 30000000,2,16549916 (two-pass node-exact・wall
    96s/98s)。nodes は予算区間 (15M, 30M] にあり 15M EXHAUSTED 履歴と
    整合。fresh exact LOSS (probe-level)。verdict は不消費・将来 Part の
    loss-only adoption 候補 (BASE `73482be0…`)。**
- 0 MISMATCH・0 TRUNCATED 残置・0 EXHAUSTED@30M。両キーとも 30M で
  解決したため 60M ladder は不要。
- audit_ek.py (修正版 sha256 `7636def1…`) clean run: **79/79 gates
  PASS**・`output/audit_ek.json` (10,375B・sha256 `d9aa8aab…`)。
- **修正 commit (honest 記録)**: wave B1 で出版した audit_ek.py
  (`0e06d210…`) の JSREPLAY_SHA 定数に転記ミス
  (84585617… の `3f1c` を `3d1c` と打ち損じ) があり、初回 audit が
  `pin:scripts/jsreplay.js` で fail-closed 検出した。実 jsreplay bytes
  (84585617…) と MANIFEST rev1 は正しく、実測値への影響なし。
  定数のみ修正した版 (`7636def1…`) を CORRECTION commit で出版し
  その bytes から 79/79 PASS を取り直した (**fail-closed pin 設計が
  転写ミスを工程内で捕捉した Part EE 第52条①(a) 型の再実例**)。
- tamper battery (fail-closed 確認。実行後はすべて復元し、clean run
  79/79 PASS を取り直した):
  - T-EK1: aj030 p1 nodes 桁を-1 → `aj030:two-pass-node-exact` fail。
  - T-EK2: status.log の aj039 verdict 桁 (2→1) → `status:aj039-win-line`
    fail。
  - T-EK3: aj049 anchor p1 nodes 桁を+1 → `anchor:aj049:two-pass-exact`,
    `anchor:aj049:node-exact` fail。

## 実行プロトコル (宣言どおり・binding)

1. drive-start要件: val-gate 4/4 fresh host 走 (.ek-host.out) が published
   baseline と wall_s 以外全列一致。
2. anchors: runbatch_ek-30m.sh を 1 invocation = 1 anchor、two-pass
   node-exact 必須 (anchor は resolved キーの機械照合であって verdict
   消費ではない・Part ED anchor 実績と同一運用)。
3. 本 probe: aj030 → aj039 の順 (2 workers 併走可)。1 invocation = 1 pass
   原則 (truncated-sidecar guard で cross-invocation resume)。two-pass
   fresh-cold node-exact、MISMATCH は HARD-STOP rc=42。
4. honest label: result=2 (LOSS) は nodes > 15,000,000 を検証して fresh
   解決 (nodes <= 15M は 15M EXHAUSTED 履歴と矛盾 = fail-closed)。
   result=1 (WIN) は WIN-HALT (verdict 不消費)。result=0 は nodes ==
   30,000,000 厳密で EXHAUSTED@30M honest UNKNOWN・60M 条件は別宣言。
5. 出力: output/status.log + output/drive 行 + output/raw/*.out +
   val-gate .ek-host.out 4件 + output/audit_ek.json。

## 本 Part で行わないこと

- canonical cache / increment / merger / refresh / extractor の実行
  (adoption は将来 Part。BASE は `73482be0…` のまま)
- Part EJ (batch-40 class 30118) のキー全般への言及以外の接触
- Part EF (batch-38) 所有キー (ai044/ai048 等) への一切の接触
- af034 の 30M 条件再実行 (af034 の 30M は Part EA で EXHAUSTED 済み
  = 同一条件再実行禁止。af039 は resolved LOSS 行なので anchor 照合可)
- 11×11 空盤・class 30484 の勝敗・coverage・secured coverage 主張
- jsreplay・pinned runner の BUDGET 行以外の改変
