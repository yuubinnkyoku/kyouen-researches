# Part EK 宣言: aj030/aj039 (class 30484・EXHAUSTED@15M 残2キー) 30M 再probe計画 (2026-11-25)

単一オーナー Part EK・publish-then-execute。観測 main HEAD (宣言直前)
`e0ca8d755a18674810519983b0e076a9e1ec1a53` (2026-11-25T13:40:08Z・z16-min11
predecl kit)。対抗宣言走査 (認証付き GitHub App commit-message 検索・
2026-11-25T13:53Z 時点): 「Part EK」0件・「reprobe30」0件。「aj030」/
「aj039」ヒットはすべて Part EH (batch-39 EXHAUSTED 報告)・Part EI
(46 LOSS 採用)・Part EJ 宣言 (高budget ladder を「別の未来の Part 宣言」と
して登録) の記述であり対抗宣言ではない。Part 文字は RS 記法どおり
既存 max が EJ (別レーン batch-40 in-flight) のため EK を使用。

**11×11 空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 30484 (52キーすべて) は本 Part の前後を通じて
すべて UNKNOWN のまま。** 本 Part は 2キーの probe-level honest label
取得のみを行い、verdict の消費 (canonical cache 系への採用) は一切行わない。

## 対象と事前状況 (すべて出版済み bytes の pin)

- 対象キー: aj030 = (lo, hi) = (1152922604135251976, 65536)・stones=5・
  legal 83・aj039 = (1152922606282735616, 65536)・stones=5・legal 88。
  いずれも class 30484 (mask `[1152922604135251968, 65536]`) の
  batch-39 fresh 子。
- 出版済み条件: batch-39 15M (order=0・fresh-cold・share_tt=0) で両キー
  EXHAUSTED (EH status.log `08d70bb7…` 54行中「aj030 PASS/EXHAUSTED
  15000000,0,15000000」「aj039 PASS/EXHAUSTED 15000000,0,15000000」・
  raws sources/exh15m 4件 `843a0a0c…`/`661c8e41…`/`60ae21db…`/
  `c51899d5…`・two-pass node-exact)。honest UNKNOWN・同一 15M 条件の
  再probeは禁止 (Part EH 完了log resume #2・Part ED 宣言の
  EXHAUSTED 行同一条件再実行禁止と同規約)。
- Part EI 後の class 30484 残 unknown 構成 (EI reaudit closure-classes
  `e12bf328…`): 6行 = EXHAUSTED 2 (本2キー) + 不消費 WIN 2 (aj049
  `15000000,1,4998452` / aj050 `15000000,1,1871594`・scrutiny-owner
  C++ gate `9193f5b6…` 専権で本環境は g++ 等コンパイラ不在により
  消費不能) + claim-reserved 2 (ai044/ai048・Part EF batch-38 所有)。
  46 LOSS 行は Part EI で canonical 採用済み (BASE `73482be0…`)。
  したがって本 2キーの高budget再probe が closure frontier 上で
  唯一の probe 可能な残作業である (Part EI 完了log resume 候補②・
  Part EJ 宣言 guardrail「registered high-budget ladder」の受領)。

## 事前宣言条件 (binding)

1. **BUDGET = 30,000,000** (30M)。batch-39 15M→30M の 2倍予算条件
   upgrade (Part EA (15M→30M)・Part ED (→60M) と同一の ladder 形式)。
   同一条件 (15M) の再probeは行わない。
2. **two-pass fresh-cold node-exact**: runner による p1/p2 2走の
   `replay,` 行 (budget,result,nodes) 一致を必須とする。不一致 (rc=42
   MISMATCH) は HARD-STOP。
3. **runner byte 規則**: scripts/jsreplay.js は byte-clone `84585617…`。
   scripts/runbatch_ek-30m.sh は Part ED 60M runner published bytes
   (`b0c5f714…`) の BUDGET 行 (60000000→30000000) のみ変更・
   派生 sha256
   `3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4`
   は published Part EA 30M runner bytes (pin `3b5083b4…`) と完全一致
   (30M 予算 runner の先行出版 bytes が存在することの確認済み・
   改変内容は BUDGET 行のみ)。truncated-sidecar guard (`# replay_done`
   欠落は証拠でなく再実行)・1 invocation = 1 pass 原則 (cross-invocation
   resume) は Part ED と同一。
4. **honest label 規約 (label-agnostic・publication 前に結果を固定)**:
   - result=2 (LOSS): nodes > 15,000,000 を検証して fresh 解決として
     記録 (nodes <= 15M は 15M EXHAUSTED 履歴と矛盾するため fail-closed。
     将来 Part で loss-only 採用候補になる。本 Part では採用しない)。
   - result=1 (WIN): probe-level WIN として記録し WIN-HALT (rc=45)・
     scrutiny-owner C++ gate 待ち (verdict 不消費)。
   - result=0 (EXHAUSTED): nodes == 30,000,000 厳密を検証して
     EXHAUSTED@30M honest UNKNOWN を記録・更なる高budget条件 (60M) は
     別宣言とする。
   - いずれの場合も 11×11・class 30484 の勝敗・coverage・secured の
     主張を行わない。
5. **fresh-increment gate**: 対象2キーが canonical chain head (Part EI
   merged cache `73482be0…` 6,712行) と quarantine registry
   (`81d23160…`) の両方に不在であることを kit audit で検証する。
6. **anchor 事前登録 (EK runner = 30M cap で再現・2-pass node-exact)**:
   - aj001 → LOSS result=2 nodes 5,156,075 (published b39 15M 条件値。
     resolved-under-cap・cap 非依存検証・class 30484 同 class anchor)。
   - aj049 → WIN result=1 nodes 4,998,452 (published b39 15M WIN anchor。
     runner は WIN-HALT rc=45・status.log に WIN-HALT 行。anchor は
     resolved/adjudicated キーの機械照合であり verdict 消費ではない
     (Part ED が不消費 WIN 行 af029 を anchor に使用した前例と同一運用))。
   - af039 → LOSS result=2 nodes 19,234,232 (published Part EA 30M 条件値。
     (15M, 30M] budget-crossing regime (本 probe の予期解決域) の代表。
     ED 60M cap でも同一 node が確認済み)。
   - af034 は anchor に使用しない (af034 の 30M 条件は Part EA で
     EXHAUSTED の honest UNKNOWN 行であり、30M 条件の再実行は禁止)。
   - anchor 合計は約 2×(5,156,075+4,998,452+19,234,232) =
     58,777,518 nodes/pass。
7. **val-gate 事前登録 (published 条件 budget で再現・1-pass fresh)**:
   Part EA/ED/EH/EJ と同一の 4分子 (sha セット `ecc0299b`/`6e902ab1`/
   `56aacb71`/`eeafe3ac`/`8035fe54`/`91dffdec`): at2m 2行 → EXHAUSTED
   (2000000,0,2000000)・first-15m → (15000000,2,3651923)・second-15m →
   (15000000,2,5040200)。jsreplay は byte-clone で budget はコマンド
   ライン引数 (--exact-replay-budget=2000000 / 15000000) で指定し
   published 条件を再現する。fresh host 走 `.ek-host.out` との比較は
   wall_s 列を除く全 replay 列一致。**val-gate 4/4 が drive-start 要件。**

## kit 構成 (実験dir)

`research/experiments/n11-centralreply-closure-class30484-aj030aj039-reprobe30m-20261125/`

- scripts/jsreplay.js: byte-clone `84585617…`
- scripts/runbatch_ek-30m.sh: `3b5083b4…` (ED runner の BUDGET 行のみ
  変更・EA 30M runner と byte 一致)
- scripts/audit_ek.py: `0e06d210…` (ED `audit_ed.py` `6f76e8e5…` の
  2-target 拡張 fork・fail-closed)
- input/: aj030 `520ee52a…`・aj039 `82f8dff3…` (b39 kit byte-clone)・
  aj001 `2f6daea5…`・aj049 `46349391…` (b39 kit byte-clone)・af039
  `e51a3c9d…` (ED kit byte-clone)
- val-gate/ 8ファイル: byte-clone (b39/EA/ED kit と同一 sha セット)
- sources/: b39-status.log `08d70bb7…`・exh15m/ 4 raws
  (`843a0a0c…`/`661c8e41…`/`60ae21db…`/`c51899d5…`)・
  canonical-cache-ei-merged-73482be0-20261125.cache `73482be0…`
  (279,805B・Part EI chain head)・n11-s5-evidence-quarantine.json
  `81d23160…`
- README.md (run record pending) + MANIFEST-sha256.txt (kit 23 rev1)

## 出版 wave 計画 (各 wave fetch-back byte 照合)

1. wave A: 本宣言log
2. wave B: kit (scripts 3 + input 5 + val-gate 8 + sources 7 + README +
   MANIFEST)
3. wave C: 実行 (val-gate → anchors → 本 probe) の後・outputs
   (status.log + drive 行 + raw/ anchors 6 + 本 probe 4 + val-gate
   .ek-host.out 4) 出版
4. wave D: audit_ek.py 実行結果 (audit_ek.json) + tamper battery + README
   最終化 + MANIFEST-sha256 rev2 出版
5. wave E: 完了log `research/log/2026-11-25-part-ek-aj030aj039-reprobe30m-completion.md`

実行はこの順で行い、各 wave の fetch-back byte 照合 (raw CDN・commit sha
固定 URL) を必須とする。書込み競合・push 競合・fetch 失敗が生じた場合は
無理に押し進めず状况を記録して本 Part を中断する (hourly 並走あり・
Part EJ batch-40 と Part EF batch-38 のパスには触れない)。

## 本 Part で行わないこと

- canonical cache / increment / merger / refresh / extractor の実行
  (adoption は将来 Part。BASE は `73482be0…` のまま)
- WIN 行 (aj049/aj050 とその他全不消費 WIN 行) の scrutiny・C++ 第二実装
  gate の代替実装 (専権尊重・本環境はコンパイラ不在を再確認済み)
- af034 の 30M 条件再実行 (Part EA EXHAUSTED 行の同一条件再実行禁止)
- Part EJ (batch-40 ak001..ak050)・Part EF (batch-38 ai001..ai049) 所有
  キーへの一切の接触
- 11×11 空盤・class 30484 の勝敗・被覆・secured coverage 主張 (nodes は
  bookkeeping)
- jsreplay・pinned runner の BUDGET 行以外の改変
