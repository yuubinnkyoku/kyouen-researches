# batch-28 (closure class 5343) b28-win46 thirdimpl queue registry P1パッケージ8行 (aa046/aa016/aa025/aa033/aa027/aa038/aa012/aa042) 第三実装交叉検証 — Part DE (2026-11-24)

Part DE (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-24-part-de-b28p1win8-thirdimpl-declaration.md` 出版 `5de0f35f` + 訂正 `707be9a5`)。
b28-win46 thirdimpl queue registry
(実験 `n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124`・出版 `69e391a3`)
上の open 33 WIN行のうち **P1パッケージ8行** (est昇順 aa046→aa042) に対するpinned第三実装
(非df-pn AND/ORミニマックス `third_impl.js` `08ea958f…`) による verdict-level交叉検証 +
本host pinned-replica (`jsreplay.js` `84585617…`) 2-pass fresh-cold再現。
8行はすべて drive-4/drive-5 (`n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123`)
の 15M-probe (budget 15,000,000) で解決した honest WIN labels (rc=1)・pinned nodes
2,185,149〜5,800,791 (合計 31,778,254)。

出版pathについて: A1-A3 scaffoldは誤ってrepo root直下へpushされたため、byte同一を検証の上
宣言済みpath `research/experiments/n11-centralreply-closure-b28p1win8-thirdimpl-20261124/`
へ再出版しroot側を完全除去した (記録
`research/log/2026-11-24-part-de-b28p1win8-thirdimpl-pathrepair.md`・repair commits
R1 `a3b6361f` / R2 `fd1eb53f` / R3 `5465b6da`・誤path側67/67 sha検証・正path側67/67 fetch-back)。
scaffoldの中身 (全sha pin) は宣言と同一byteであり、検証内容への影響はない。

## 対象 8行 (rows.json `ce3d562b`・maker ×2 byte-stable)

- aa046 (1152921779484753920, 4228) legal 78・drive5-15m・replica result 1 nodes 2,185,149
- aa016 (1171516445255860224, 0) legal 78・drive4-15m・replica result 1 nodes 2,621,847
- aa025 (1171516720133701632, 0) legal 80・drive4-15m・replica result 1 nodes 3,056,950
- aa033 (1171516445255794688, 128) legal 86・drive5-15m・replica result 1 nodes 3,347,117
- aa027 (1171516445255794688, 64) legal 81・drive4-15m・replica result 1 nodes 4,860,191
- aa038 (1152921504606849024, 4228) legal 82・drive5-15m・replica result 1 nodes 4,911,996
- aa012 (1171516445255798784, 0) legal 81・drive4-15m・replica result 1 nodes 4,994,213
- aa042 (1152921504606847008, 4228) legal 88・drive5-15m・replica result 1 nodes 5,800,791

anchors k02a (1297036692683751424, 68157440) expect 1 / l1a (13019119616, 16448) expect 2、
negatives ng1 (legal+1) / ng2 (stones 6) はBF chain byte-clone。

## 実行結果 (D1-D8 全green・audit 323 gates PASS)

- **D1 rules gate**: `replica quads 95670 mine quads 95670`・`triples checked 195044
  mismatches 0` (rc=0)。
- **D2 val-gate fresh 4本** (budget 2M/2M/15M/15M): 全て published baseline と
  wall_s 以外 node-exact (G7 4/4)。first-15m LOSS nodes 3,651,923・second-15m LOSS
  nodes 5,040,200・at2m 2行 budget-exhausted (result 0) 再現。
- **D3 negatives** (fail-closed期待): ng1 `GATE_FAIL "legal count mismatch: derived=87
  declared=88"`・ng2 `GATE_FAIL "stone count mismatch: bits=5 declared=6"`、期待どおり
  rc=1。実行注記: 最初のD3実行でtagに "ng1x"/"ng2x" を用いたが、audit `read_run` は
  tag "a" を読むため `ng1.a.out`/`ng2.a.out` として再実行した (両tagとも同一GATE_FAIL
  内容。出版は宣言どおり tag "a" 側 negative 2ファイル)。
- **D4 anchors a/b det-pair**: k02a result 1・expansions 9,106,337・ttHits 4,991,527
  (a=b同一・published pin一致) / l1a result 2・expansions 7,660,202・ttHits 3,951,175
  (a=b同一・published pin一致)。
- **D5 replica 8キー×2-pass fresh-cold** (budget 15M): 16/16 pass rc=0・det-pair 8/8
  (wall_s以外の determinism fields 全一致)・published raw 16/16 node-exact
  (result・nodes完全一致)。
- **D6 third-impl 8キー×2 run (a/b)**: 16/16 rc=0・det-pair 8/8 (expansions
  aa046 2,503,964 / aa016 3,029,875 / aa025 3,527,308 / aa033 3,911,275 / aa027 5,653,876 /
  aa038 5,727,888 / aa012 5,888,866 / aa042 6,797,666・a=b同一)・verdict agree 8/8
  (third result 1 == published WIN行)。third-implノード数は実装依存のため pinned
  replica nodes との直接比較はgate対象外 (宣言どおり・verdict一致のみ主張)。
- **D7 audit** (`audit_de.py` ×3 byte-identical): **ALL 323 GATES PASS**・verdict
  agreements 8/8 (WIN=8 LOSS=0)・wall-inconclusive 0・pass-one third-impl expansions 計
  **37,040,718**・audit-summary.json 3回ともbyte同一 (`38b46204…`)。
- **D8 audit tamper battery 4種**: 全捕捉 (各 rc=1・期待gate発火) と復帰green:
  (a) replica aa046.p1 nodes +1 → `replica-aa046-det-pair` FAIL
  (b) targets aa016.a result 1→2 → `target-aa016-det-pair` FAIL
  (c) anchors k02a.a expansions +1 → `anchor-k02a-a-expansions` FAIL
  (d) rows.json replica_nodes (aa046) +1 → `replica-aa046-verdict-vs-published` FAIL。
  復帰後 ALL 323 GATES PASS・audit-summary.json は改竄前とbyte同一 (完全復元確認)。

## 成果物

- `output/status.log` (honest journal・D1-D8実行順記録)
- `output/rules-gate.txt`・`output/audit-run{1,2,3}.txt` (byte同一)・`output/audit-summary.json`
- `output/replica/` 16 (8キー×p1/p2)・`output/targets/` 16 (8キー×a/b)・`output/anchors/` 4・
  `output/negative/` 2 (ng1.a.out / ng2.a.out)
- `val-gate/*.de-host.out` 4 (scaffold baseline 8と併置)
- `MANIFEST-sha256.txt`: 本READMEを含む全116ファイルのsha256 (MANIFEST自身を除く)。

## 主張の限定

- 本Partは交叉検証のみ。**verdict不消費**: 対象8行は honest WIN labels のままで、
  adoptionは scrutiny owner C++第二実装 gate `9193f5b6…` 通過後・pinned merger `90711961…`
  経由の別adoption Part 専権。
- 閉鎖・被覆・secured・root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 5343 (54キーすべて・対象8キー含む) は本Partの前後を通じてすべてUNKNOWNのまま。**
- nodes数・expansions数・ttHits数を勝敗や距離として読まない。
