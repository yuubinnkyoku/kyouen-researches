# n11 central-reply closure batch-18 WIN rows third-implementation cross-verification (Part AZ, 2026-11-22)

Part AZ of the central-reply 19-root closure grind (K0415/K0417 line): 第三実装
(third implementation) による、**published batch-18 (class 16131, Part AY) の
2つのWIN行 v001/v002** のverdict-level交叉検証。単一オーナー宣言 (note
amendment・commit `a5ea2aa0`)・**実行前に宣言出版**。前例はPart G
(closure WINs b018/d002/e002/f017 の第三実装再検証) および
Part AR/AX (LOSS行の第三実装交叉検証)。

**verdict消費ゼロ。v001/v002のWINは本Partでは採用しない。** 採用判断は
scrutiny owner (C++第二実装 gate pin `9193f5b6…`) のままである。

## 対象

- `input/rows.json` (schema `n11-centralreply-closure-b18win-thirdimpl-input-v1`):
  targets 2行 (v001, v002) + anchors 2行 (k02a/l1a) + negatives 2種
  (ng1/ng2)。targetsはpublished batch-18の2-pass fresh-cold node-exact WIN行:
  - **v001**: s5 153671・[1154610354467115008, 64]・legal 83・replica WIN
    5,656,151 nodes (publication commit `938e34f2`・MANIFEST pin)。
  - **v002**: s5 207534・[3459890413727387648, 64]・legal 84・replica WIN
    7,898,204 nodes。

## 入力の機械導出 (maker)

`scripts/make_inputs_az.py` (fail-closed・手転写ゼロ・3回実行byte一致):
- source pins: batch-18 batch-keys sha256 `1bb3ed41…` (53キー・class 16131・
  v001 s5 153671 / v002 s5 207534・membership 2/3)、raw 4ファイル
  (sha256 `24b45c8a`/`1fc367bd`/`41c10ec2`/`e9f578fc`・published MANIFEST
  固定)、status.log `4b785add…`・README `8b6a85b3…`。
- raw gate: 両passとも `# replay_done`・stones 5・is_or 0・budget 15,000,000・
  **result 1 (WIN)・budget内**・p1==p2 node-exact (compared fields)。
- status.log 3-way gate: `vXXX PASS 15000000,1,<nodes>` 行・`vXXX WIN-HALT`
  行 (2行)・WIN-ROW-DETAIL行 (nodes/legal/keys完全一致)・AY host VAL-GATE 4/4行・
  EXECUTION-HALTED行・「51 keys UNPROBED」行・「17候选」行。
- README gate: `**v001: WIN (result 1)**` / `**v002: WIN (result 1)**` 結果節と
  nodes表記 (5,656,151 / 7,898,204) の存在。
- derived-vs-published input CSV byte-equality: targets 2件
  (`edee9be8…`/`e8bbbaed…` pins) + anchors/negatives 4件
  (published Part AR CSVとbyte一致)。

## 手法

pinned `third_impl.js` (sha256 `08ea958f…`・非df-pn AND/ORミニマックス)・
1行=1 solver=1プロセス・cap 300,000,000 expansions・wallcap 240s・
`--memo-power=22`・全target/anchor a/b 2回のdeterminism gate
(result/expansion/ttHits/reason同一必須)。本hostは逐次実行
(同時2 solver起動でper-solver CPU quotaが半減するPart AX観測を継承・
決定性フィールドはwall非依存)。

## 結果 (verdict-level corroboration literature)

- **targets 2/2 clean WIN (result 1)・replica verdict一致 2/2**:
  - **v001: third-impl WIN 6,558,484 expansions / 3,610,051 ttHits**
    (replica 5,656,151 nodes・ratio 1.16)。
  - **v002: third-impl WIN 9,204,329 expansions / 5,027,672 ttHits**
    (replica 7,898,204 nodes・ratio 1.17)。
  - a/b pair全同一 (determinism gate PASS)。総expansions 15,762,813/pass。
    WIN 2・LOSS 0・WALL-INCONCLUSIVE 0・DIVERGENCE 0。
- anchors: k02a WIN 9,106,337/4,991,527・l1a LOSS 7,660,602/3,951,175 とも
  published第三実装値にnode-exact再現 (a/b同一)。negatives ng1/ng2は
  設計どおりfail-closed文言 (GATE_FAIL)。
- rules gate (`output/rules-gate.txt`): replica quads 95,670 == third-impl
  quads 95,670・triples checked 195,044 mismatches 0。
- audit (`scripts/audit.py`): **53/53 gates PASS**・2回実行byte一致
  (schema `n11-centralreply-closure-b18win-thirdimpl-audit-v1`)。全summaryは
  `output/audit-summary.json`。

## 意味と消費規則 (route statement・閉鎖主張なし)

batch-18の最初のwaveの2つのWIN (v001/v002) が独立実装 (第三実装) でも
clean WINとして再現された。これは**verdict-level補強文献**であり、
verdict消費ゼロ。17 unconsumed closure WIN候选 (15 prior + v001 + v002) の
採用判断は一切代行しない (scrutiny owner・C++第二実装 gate pin
`9193f5b6…` のまま)。canonical cache (6,120行 `be9cb24e…`) は不変・
本Partはいかなるcacheにも書込まない。AY宣言の残51キー (v003..v053,
fresh・未着手) とPart AV (batch-17 adoption, in flight) には一切触れていない。

**標準11×11空盤・19 central-reply roots・class 16131 (残51子)・全53キーは
本Partのどの時点でもUNKNOWNのまま。nodes数・expansions数を勝敗として読まない。**

## ファイル

- `scripts/`: third_impl.js (`08ea958f…`), verify_tbl.js (`c8c52528…`),
  jsreplay.js (`84585617…`), run_thirdimpl.sh, make_inputs_az.py, audit.py。
- `input/`: rows.json + input CSV 6件。
- `sources/`: published batch-18原本体 (raw 4 + status-b18.log +
  README-b18.md + batch-keys-b18.json + MANIFEST-b18.txt +
  published-input 2 + published-input-ar 4)。すべてpublication commit
  固定raw fetchのbyteコピー。
- `output/`: status.log (宣言header + maker capture + RUN行 + RUNNER-NOTE)、
  targets a/b 4、anchors a/b 4、negative 2、rules-gate.txt、
  audit-summary.json、audit-run1/2.txt。
