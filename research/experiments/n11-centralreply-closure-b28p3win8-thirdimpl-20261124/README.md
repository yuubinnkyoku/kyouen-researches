# batch-28 (closure class 5343) b28-win46 thirdimpl queue registry P3パッケージ8行 (aa052/aa044/aa041/aa048/aa026/aa039/aa043/aa045) 第三実装交叉検証 — Part DG (2026-11-24)

Part DG (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-24-part-dg-b28p3win8-thirdimpl-declaration.md` 出版 `e05d73fd`・observed HEAD
`26fc5352`)。
b28-win46 thirdimpl queue registry (REVISION 3・実験
`n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124`・出版 `43932d74`・
queue-registry.json `334f6209…` / README-queue `4b20c6a0…`) 上の open 25 WIN行のうち
**P3パッケージ8行** (est昇順 aa052→aa045) に対するpinned第三実装
(非df-pn AND/ORミニマックス `third_impl.js` `08ea958f…`) による verdict-level交叉検証 +
本host pinned-replica (`jsreplay.js` `84585617…`) 2-pass fresh-cold再現。
8行はすべて drive-4/drive-5 experiment
(`n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123`) の 15M-probe
(budget 15,000,000) で解決した honest WIN labels (rc=1)・pinned nodes 8,976,982〜12,371,943
(合計 **85,844,795**)。aa026 のみ drive-4決定 (決定的2行は drive-5 logでも byte同一・
cross-log gate実施)・残り7キーは drive-5決定。

本レーンの経緯 (宣言に誠実記録): 当レーンは当初 Part DF として P2パッケージ8行の kitを
準備したが、push直前の最新main再取得で並走レーン (`59b6540f`/`2245e85e`/`26fc5352`) が
P2 scopeの宣言・scaffold出版を完了済みと判明したため、**P2 kitは未出版のまま破棄**し
(1 byteも出版せず) P3パッケージへ pivotした。また sources 取得時に一時的に保持した
queue-registry.json の sha が出版正本 (`334f6209…`) と不一致だったことを宣言前の
machine-checkで検出し、`PIN_QREG_JSON` を修正してから出版した (誤pinのまま出版・実行
した事実はない)。

## 対象 8行 (published・全てUNCONSUMED honest labels・rows.json `22de9dd7…`・maker ×2 byte-stable)

| key | key (lo,hi) | s5 | legal | verdict | pinned nodes | 決定drive |
| --- | --- | --- | --- | --- | --- | --- |
| aa052 | 1152921504606851072,4228 | 199737 | 93 | WIN | 8,976,982 | drive-5 |
| aa044 | 1152921521786716160,4228 | 199729 | 86 | WIN | 9,219,778 | drive-5 |
| aa041 | 1171516445255794688,8 | 199726 | 93 | WIN | 10,283,599 | drive-5 |
| aa048 | 1152921504615235584,4228 | 199733 | 87 | WIN | 10,553,343 | drive-5 |
| aa026 | 1171516445255794688,32 | 199711 | 88 | WIN | 11,019,409 | drive-4 (両log一致) |
| aa039 | 1152921504606846984,4228 | 199724 | 88 | WIN | 11,349,776 | drive-5 |
| aa043 | 1152921513196781568,4228 | 199728 | 90 | WIN | 12,069,965 | drive-5 |
| aa045 | 1152921642045800448,4228 | 199730 | 84 | WIN | 12,371,943 | drive-5 |

anchors k02a (1297036692683751424, 68157440) expect 1 / l1a (13019119616, 16448) expect 2、
negatives ng1 (legal+1) / ng2 (stones 6) はBF chain byte-clone。

## kit構成 (A1 `c927951b` scripts 7 + input 13 + val-gate 8 + README / A2 `d49930a8` sources 39 / A2fix `ca69da9f`)

- `scripts/` 7: make_inputs_dg.py (`d3fefbca…`・DE maker適応系譜) / audit_dg.py
  (`e3a1c74f…`・同一G-gate系譜適応・PIN_RAW_DG 16 pin・`.dg-host.out` suffix) /
  run_replica_dg.sh (`de1d1fbc…`・published DE runnerのヘッダcommentのみ書換・body byte不変) /
  run_thirdimpl.sh (`a0b77d83…`) / third_impl.js (`08ea958f…`) / verify_tbl.js (`c8c52528…`) /
  jsreplay.js (`84585617…`) — 下3つはpinned byte-clone。
- `sources/` 39: drive-4/5 experimentからのcommit-pinned fetch (raw 16: 8キー×p1/p2・
  決定ドライブ側正本 / published-input 8・published-input-bf 4) +
  status-drive4.log `59817444…` (61行) + status-drive5.log `ca1e98cc…` (109行) +
  batch-keys-b28.json `af19208f…` + queue-registry.json (rev3) `334f6209…` +
  README-queue.md (rev3) `4b20c6a0…` + Part CO 7-LOSS adoption出版物 (merged canonical cache
  `854800f3…` 6,301行 / increment `bd5ef7d7…` / increments-manifest `b47e07ca…`) +
  Part DB 37-LOSS re-adoption出版物 (merged canonical cache `04b0a239…` 6,354行・現canonical
  chain head / increment `85bd4469…` / increments-manifest `1b51f30d…`)。
- `input/` 13: rows.json + 8対象 + anchors k02a/l1a + negatives ng1/ng2 のinput CSV。
- `val-gate/` 8: at2m×2 + first-15m/second-15m published baselines + inputs
  (CWから不変再利用・**本PartはA1 commitでkit内に出版しself-contained**・host出力は
  `.dg-host.out` として生成)。

## 実行結果 (D1-D8 全green・audit 323 gates PASS)

- **D1 rules gate**: `replica quads 95670 mine quads 95670`・`triples checked 195044
  mismatches 0` (rc=0)。
- **D2 val-gate fresh 4本** (budget 2M/2M/15M/15M): 全て published baseline と
  wall_s 以外 node-exact。first-15m result 2 (LOSS) nodes 3,651,923・second-15m result 2
  nodes 5,040,200・at2m 2行 budget-exhausted (result 0・nodes 2,000,000) 再現。
- **D3 negatives** (fail-closed期待): ng1 `GATE_FAIL "legal count mismatch: derived=87
  declared=88"`・ng2 `GATE_FAIL "stone count mismatch: bits=5 declared=6"`、期待どおり
  rc=1。
- **D4 anchors a/b det-pair**: k02a result 1・expansions 9,106,337・ttHits 4,991,527
  (a=b同一・published pin一致) / l1a result 2・expansions 7,660,202・ttHits 3,951,175
  (a=b同一・published pin一致)。
- **D5 replica 8キー×2-pass fresh-cold** (budget 15M・inner timeout 260・4並列上限):
  16/16 pass rc=0・det-pair 8/8 (wall_s以外の determinism fields 全一致)・
  published raw 16/16 **node-exact** (result・nodes完全一致・pinned nodes合計
  85,844,795と一致)。`run_replica_dg.sh` の invocation-level exit 1 はscript末尾の
  `[ "$RC" -ne 0 ]` idiomによる benign (各pass rc=0・audit G2 gates全PASS・宣言の
  published DE runner byte不変系譜どおり)。
- **D6 third-impl 8キー×2 run (a/b)**: 16/16 rc=0・det-pair 8/8 (a=b同一)・
  **verdict agreement 8/8 (WIN=8・inconclusive 0)**。pass-one third-impl expansions
  計 **101,925,010** (aa052 10,672,229 / aa044 10,904,035 / aa041 12,153,804 /
  aa048 12,498,855 / aa026 13,051,334 / aa039 13,569,936 / aa043 14,412,813 /
  aa045 14,662,004)。third-implノード数は実装依存のため pinned replica nodes との
  直接比較はgate対象外 (宣言どおり・verdict一致のみ主張)。
- **D7 audit** (`audit_dg.py` ×3 byte-identical): **ALL 323 GATES PASS**・verdict
  agreements 8/8 (WIN=8 LOSS=0)・wall-inconclusive 0・audit-run stdout sha256
  `d6251ad0…` (3回ともbyte同一)・audit-summary.json `fd68c562…`。
- **D8 audit tamper battery 4種**: 全捕捉 (各 rc=1・期待gate発火)・復帰 green
  (audit-tamper-clean.txt・`ALL 323 GATES PASS` rc=0):
  (T1) replica aa052.p1 nodes +1 → `replica-aa052-det-pair` FAIL
  (T2) targets aa052.a result 1→2 → `target-aa052-det-pair` FAIL
  (T3) anchors k02a.a expansions +1 → `anchor-k02a-a-expansions` FAIL
  (T4) rows.json replica_nodes (aa052) +1 → `replica-aa052-verdict-vs-published` FAIL。
  復帰後 maker gates PASS・stdoutは宣言前 clean run と byte同一。

## 成果物

- `output/status.log` (honest journal)・`output/run-log.txt` (D1-D8実行順記録)・
  `output/rules-gate.txt`・`output/audit-run{1,2,3}.txt` (byte同一)・
  `output/audit-summary.json`・`output/audit-tamper-{1..4}.txt`・
  `output/audit-tamper-clean.txt`
- `output/replica/` 16 (8キー×p1/p2)・`output/targets/` 16 (8キー×a/b)・
  `output/anchors/` 4・`output/negative/` 2 (ng1.a.out / ng2.a.out)
- `val-gate/*.dg-host.out` 4 (scaffold baseline 8と併置)
- `MANIFEST-sha256.txt`: 本READMEを含む全122ファイルのsha256 (MANIFEST自身を除く)。

## 誠実記録 (インシデントと復旧)

1. **A2 sources truncation事故 (出版時に発生・出版内で即検出・修正)**: A2 commitでの
   push取得時に3ファイル (merged canonical cache CO `854800f3…` / DB `04b0a239…` /
   queue-registry.json `334f6209…`) が取得経路の 64KB read cap で truncation
   (64,000/63,997/63,984 bytes) した。**fetch-back blob sha照合が機械検出**し
   (published tree blob sha vs 正本)、chunked readで正本bytes
   (259,886/262,326/114,535 bytes) を再出版して A2fix `ca69da9f` で全blob sha一致を
   確認した。truncated bytesが証拠として使われた事実はない。
2. **実行環境リセット (B commit後・成果物喪失なし)**: B commit出版後に沙汰した実行
   環境リセットで作業用ローカルkitが消滅したが、**全 kit + output は publish済み**
   だったため喪失なし。published scaffold (commit `9abe5e6` GitHub snapshot) から
   実験dir 122ファイルを復元し、**GitHub tree blob sha 122/122 一致・過不足ゼロを
   機械検証**した (宣言の stop rule「published evidenceだけが証拠」どおり)。
3. **宣言の aa039.p2 pin転写typo (本README執筆時の機械検証で発見)**: 宣言文の
   raw 16 pin群のうち aa039.p2 (sources/raw/aa039.p2.out) の記載は
誤って65文字 (`…568c5cfb8…`・位置45に余分な `c`) になっている。正しいsha256は
`11b19ad3ad4b8f5868945af7b7149230053b8cbb568c5fb83934f2d0e0784a07` であり、
audit_dg.py `PIN_RAW_DG` の pin・MANIFEST・実ファイルの三者が一致している
(当該gateは D7 で PASS)。宣言のその他35 pin (audit/maker/runner/ inputs/sources/
queue-registry/CO/DB caches) は全て MANIFEST entry と完全一致
(DE runner `3e4263cc…` は系譜記載の外部参照)。実行・検証への影響なし。

## 主張の限定

- 本Partは交叉検証のみ。**verdict不消費**: 対象8行は honest WIN labels のままで、
  adoptionは scrutiny owner C++第二実装 gate `9193f5b6…` 通過後・pinned merger
  `90711961…` 経由の別adoption Part 専権。
- 閉鎖・被覆・secured・root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 5343 (54キーすべて・対象8キー含む) は本Partの前後を通じて
  すべてUNKNOWNのまま。** nodes数・expansions数・ttHits数を勝敗や距離として読まない。
