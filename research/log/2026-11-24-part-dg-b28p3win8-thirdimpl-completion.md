# Part DG 完了: batch-28 (class 5343) b28-win46 queue registry P3パッケージ8行 第三実装交叉検証 — 全工程green・323 gates PASS

- 2026-11-24T05:58Z (authoring time; commit timestampはGitHub側)
- 宣言: `research/log/2026-11-24-part-dg-b28p3win8-thirdimpl-declaration.md` (出版 `e05d73fd`・observed HEAD `26fc5352`)
- 実験dir: `research/experiments/n11-centralreply-closure-b28p3win8-thirdimpl-20261124/`

## 結果 (D1-D8 全green)

- D1 rules gate: quads 95,670 一致・triples 195,044 mismatches 0 (rc=0)。
- D2 val-gate fresh 4本 (2M/2M/15M/15M): published baselineと wall_s 以外 node-exact 4/4
  (first-15m result 2・nodes 3,651,923 / second-15m result 2・nodes 5,040,200 /
  at2m 2行 budget-exhausted (result 0・nodes 2,000,000) 再現)。
- D3 negatives: ng1 GATE_FAIL "legal count mismatch: derived=87 declared=88"・
  ng2 GATE_FAIL "stone count mismatch: bits=5 declared=6" (期待どおり fail-closed・rc=1)。
- D4 anchors a/b det-pair: k02a result 1・exp 9,106,337・ttHits 4,991,527 / l1a result 2・
  exp 7,660,202・ttHits 3,951,175 (a=b同一・published pin一致)。
- D5 replica 8キー×2-pass fresh-cold (budget 15M・inner timeout 260・4並列上限): 16/16 pass
  rc=0・det-pair 8/8 (wall_s以外全字段一致)・published raw (PIN_RAW_DG 16) と **node-exact
  16/16** (pinned nodes 合計 85,844,795と一致)。`run_replica_dg.sh` の invocation-level
  exit 1 は script末尾 `[ "$RC" -ne 0 ]` idiom由来の benign (各pass rc=0・audit gates全PASS)。
  aa026 (drive-4決定) の決定的2行が drive-5 logでも byte同一である cross-log gateもPASS。
- D6 third-impl 8キー×2 run (a/b): 16/16 rc=0・det-pair 8/8・**verdict agreement 8/8
  (WIN=8・inconclusive 0・third result 1 == published WIN行)**。pass-one expansions計
  **101,925,010** (aa052 10,672,229 / aa044 10,904,035 / aa041 12,153,804 /
  aa048 12,498,855 / aa026 13,051,334 / aa039 13,569,936 / aa043 14,412,813 /
  aa045 14,662,004)。third-implノード数は実装依存のため pinned replica nodesとの直接比較は
  gate対象外 (宣言どおり・verdict一致のみ主張)。
- D7 audit ×3 byte-identical (stdout sha256 `d6251ad0…` + audit-summary.json
  `fd68c562…`): **ALL 323 GATES PASS**・verdict agreements 8/8 (WIN=8 LOSS=0)・
  wall-inconclusive 0。
- D8 tamper battery 4/4捕捉 (各rc=1・期待gate発火: replica-aa052-det-pair /
  target-aa052-det-pair / anchor-k02a-a-expansions /
  replica-aa052-verdict-vs-published) + 復帰green (`ALL 323 GATES PASS` rc=0・
  maker gates PASS・stdoutは宣言前 clean run と byte同一)。

## 出版 (全出版物 fetch-back byte照合)

- 宣言 `e05d73fd` (declaration log)
- A1 `c927951b` (kit scaffold 29 files: scripts 7 + input 13 + val-gate 8 + README初版)
- A2 `d49930a8` (sources 39) — **出版直後の fetch-back blob sha照合で3ファイル (CO cache /
  DB cache / queue-registry.json) の truncation (64,000/63,997/63,984 bytes) を機械検出**
  (file_system取得経路の64KB read cap)、**A2fix `ca69da9f`** で正本bytes
  (259,886/262,326/114,535) を再出版・blob sha一致を検証して修復。
- B `9abe5e66` (outputs 54: status.log / run-log.txt / rules-gate.txt /
  audit-summary.json / audit-run1-3.txt (byte同一) / audit-tamper-1-4.txt /
  audit-tamper-clean.txt / replica 16 / targets 16 / anchors 4 / negative 2 /
  val-gate 4 host out)
- C `756330f6` (README最終版 (実行結果・誠実記録section込み) + MANIFEST-sha256.txt
  (122 files・READMEを含む・MANIFEST自身を除く)・fetch-back byte一致検証済)
- 完了log (本ファイル)

## インシデントの誠実記録

1. **A2 sources truncation → A2fix** (出版内で即検出・修正)。truncated bytesはどの検証にも
   使われていない (audit は A2fix 後の kit bytesで実行)。
2. **実行環境リセット (B commit後)**: 作業用ローカルkitが消滅したが全 kit + outputは
   publish済みのため喪失なし。published scaffold (`9abe5e66` GitHub snapshot) から実験dir
   122ファイルを復元し、**GitHub tree blob sha 122/122 一致・MANIFEST自己照合OK・宣言pin群
   36/36 照合** (上記typoを含む説明は下記) を機械検証した (宣言の stop rule
   「published evidenceだけが証拠」どおり)。
3. **宣言 aa039.p2 pin転写typo (C commit執筆時の機械検証で発見)**: 宣言文の raw 16
   pin群のうち aa039.p2 だけ誤って65文字 (`…568c5cfb8…`・位置45に余分な `c`)。
   正しいsha256 `11b19ad3…5fb83934f2d0e0784a07` は audit_dg.py `PIN_RAW_DG` pin・MANIFEST・
   実ファイルの三者一致 (当該gate PASS)。実行・検証への影響なし。
4. **P2 kit pre-emptionからのpivot** (宣言記載どおり): 当レーンのP2 kitは未出版のまま
   破棄 (1 byteも非出版) し P3へ pivot。registry rev3 pin (`334f6209…`) 誤検出も出版前に
   机上machine-checkで検出し修正済み。

## queue registry rev4 bookkeeping (見送り・次回合流)

- 本宣言 D9 どおり、rev4 (P3 8行 open→done bookkeeping-only・verdict不消費) を検討したが、
  実行時点の最新mainで **Part DF (P2 8行) がscaffold A1/A2出版までで未完了**
  (実験dirに output なし・完了logなし・`2026-11-24-part-df-scaffold-verified-a3.md` まで)。
  DF executor側の今後の rev 反映と競合する可能性があるため、**本runではrev4更新を見送り状況
  を記録する** (宣言の競合時規約どおり)。P3 8行の thirdimpl交叉検証完了という事実自体は本
  完了logと実験dir (audit gates全PASS) が証拠。次回以降・DF完了後に P2+P3 をまとめた
  純bookkeeping revN を実施するか、DF側がrev4を出版した後の P3 差分revN+1
  を検討する (いずれも bookkeeping-only・adoptionは別Part専権・verdict不消費)。

## 主張の限定 (宣言と同一・変わらず)

- 本Partは交叉検証のみで**完結**。**verdict不消費**: 対象8行 (aa052/aa044/aa041/aa048/
  aa026/aa039/aa043/aa045) は honest WIN labels のまま。adoption は scrutiny owner C++
  第二実装 gate `9193f5b6…` 通過後・pinned merger `90711961…` 経由の別adoption Part 専権。
- 閉鎖・被覆・secured・root勝敗の主張はしない。nodes数・expansions数・ttHits数を勝敗や
  距離として読まない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 5343 (54キーすべて・対象8キー含む) は本Partの前後を通じてすべてUNKNOWNのまま。**

## 次のcandidates (本レーン外参考)

- queue registry P4パッケージ (aa011/aa054/aa022/aa034/aa037/aa032/aa028/aa021/aa050・9行)
  と tier-L LOSS 7行 (第三実装optional redundancy) は未着手・未宣言 (いずれも別宣言が必要)。
- Part DF (P2)・Part DA takeover (batch-29) は他レーン進行中・非接触。
- 上記 rev4 見送りの解消 (DF完了待ち)。
