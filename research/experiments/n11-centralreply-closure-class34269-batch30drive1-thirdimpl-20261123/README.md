# batch-30 (closure class 34269) drive-1 4行 ac001..ac004 (Part CR) 第三実装交叉検証 + 本host pinned-replica 2-pass + Part CO adoption出版物に対するunadopted補強gate (2026-11-23)

Part CR (宣言: `research/log/2026-11-23-part-cr-b30drive1-thirdimpl-declaration.md`
observed HEAD `dd68c4d6`・publish-then-execute・単一オーナー・fetch-back byte一致
sha256 `b9b3d4a5…`)。Part CP (batch-30 drive-1) で出版された **drive-1 4行
(ac001/ac002/ac003/ac004)** に対するpinned第三実装 (非df-pn AND/ORミニマックス
`third_impl.js` `08ea958f…`) によるverdict-level交叉検証 + 本host pinned-replica
(`jsreplay.js` `84585617…`) 2-pass fresh-cold再現 + **Part CO adoption出版物**
(Part CH merged 6,294行 + batch-28 LOSS 7行採用後 merged canonical cache 6,301行)
に対するunadopted補強機械gate。**verdict不消費** (4行はhonest labelのまま・本Part
の新規採用・解放・閉「閉」は一切なし・採用はscrutiny owner C++第二実装 gate を経て
別adoption Part のみ)。閉鎖・被覆・secured・root勝敗の主張はしない。

## 対象 (published正本から機械導出・maker `make_inputs_cr.py` `364a217f…`)

- **ac001**: key (1152921504758890496, 68719476736)・s5 36668・legal 88・
  published replica result **2 (LOSS行)**・nodes 5,635,468 (2-pass node-exact)。
- **ac002**: key (10376293541479448576, 68719476736)・s5 38891・legal 87・
  published replica result **1 (WIN行=drive-1 WIN-HALT波)**・nodes 10,752,246。
- **ac003**: key (1153484454578094080, 68719476736)・s5 178184・legal 85・
  published replica result **1 (WIN行=drive-1 WIN-HALT波)**・nodes 8,036,766。
- **ac004**: key (1152921779502579712, 68719476736)・s5 257581・legal 89・
  published replica result **2 (LOSS行)**・nodes 5,816,333 (2-pass node-exact)。

rows.json `37f55157…` (maker ×5回実行byte-stable PASS)。sources pin (commit-pinned
raw fetch・sha256全照合): batch-keys-b30 `79fbd166…` (54キー・drive-1 wave先頭4行
= ac001..ac004)・status-cp.log `43fcad17…`・README-cp `94bf0517…`・
log-cp-drive1 `9903944e…` (9行pin表機械検証)・raw 8 pin (ac001.p1 `1bef2dc2…`
/ ac001.p2 `bde8b236…` / ac002.p1 `e58cc061…` / ac002.p2 `ad06a109…` /
ac003.p1 `c585df3b…` / ac003.p2 `0f886d38…` / ac004.p1 `4572f41d…` /
ac004.p2 `ed39eb75…`)・published-input 4 pin (ac001 `a7502c05…` / ac002
`d02d876d…` / ac003 `9d1bb2b5…` / ac004 `b49fa290…`)・BF anchor/negative CSV 4
pin (k02a `b6174a3f…` / l1a `e13d2a6c…` / ng1 `8e64b9ad…` / ng2 `f19cd5a3…`)
・**Part CO出版物** (read-only不変): merged canonical cache `854800f3…`
(259,886 bytes・6,301 rows = Part CH 6,294 + batch-28 LOSS 7) / increment
`bd5ef7d7…` (7 rows) / increments-manifest `b47e07ca…` / merger `90711961…`。
val-gate baselines 4 (publishedとのpin一致済み)。provenance chainはAR→BF→…→
CL→CM→CO→CP→CR。

## 実行結果 (宣言protocol順)

1. **rules gate PASS** (pinned `verify_tbl.js` `c8c52528…`): replica quads
   95,670 == third-impl quads 95,670・triples checked 195,044・mismatches 0。
2. **val-gate this-host 4/4 node-exact** (pinned `jsreplay.js`・published
   baseline一致・wall_s比較外): at2m 2キー budget 2,000,000 exhaustion
   (result 0, nodes 2,000,000) ×2・15m基準キー budget 15M (result 2,
   nodes 3,651,923) と (result 2, nodes 5,040,200)。本host `.cr-host.out` 4件
   はval-gate/に出版 (audit G7で機械gate)。
3. **negatives 2/2 GATE_FAIL設計どおり** (ng1: legal count mismatch
   derived=87 declared=88・ng2: stone count mismatch bits=5 declared=6)。
4. **anchors 4/4 本host node-exact** (a/b determinism PASS): k02a clean
   result 1・expansions 9,106,337・ttHits 4,991,527 (wall 27.88/27.05s)・l1a
   clean result 2・7,660,602 / 3,951,175 (wall 23.58/22.95s)。published第三
   実装値 (Part CC/CL/CM/CPと同一) と同一。
5. **本host pinned-replica 2-pass fresh-cold** (budget 15M): ac001 p1/p2 =
   result 2・nodes **5,635,468** (wall 29/28s)・ac002 p1/p2 = result 1・nodes
   **10,752,246** (wall 59/59s)・ac003 p1/p2 = result 1・nodes **8,036,766**
   (wall 42/41s)・ac004 p1/p2 = result 2・nodes **5,816,333** (wall 31/31s)。
   published raw fields (result/nodes/key/legal) とのnode-exact一致をaudit
   G2bで機械検査。EXHAUSTED 0・mismatch 0。**batch-30 drive-1 4行の最初の
   独立セッション再現** (実行hostの物理的相違までは主張しない)。
6. **targets clean verdict一致 (agreement 4/4・WIN=2 LOSS=2)**: ac001
   third-impl a/b det-pair PASS・result **2 (clean)**・expansions 6,522,042・
   ttHits 3,571,857 (wall 19.14/20.22s)・ac002 result **1 (clean)**・
   expansions 12,569,497・ttHits 6,775,359 (38.42/38.17s)・ac003 result **1
   (clean)**・expansions 9,415,378・ttHits 5,058,105 (27.60/27.90s)・ac004
   result **2 (clean)**・expansions 6,802,090・ttHits 3,717,840 (20.82/21.49s)。
   cap 300,000,000・wallcap 240・memo-power=22・WALL-INCONCLUSIVE 0・DIVERGENCE
   0。pass-one third-impl拡張数合計 **35,309,007**。**drive-1 4行の
   three-implementation corroboration成立** (published drive-1 replica 2-pass
   + 本host pinned-replica 2-pass + 第三実装 minimax 2-run、すべてverdict一致:
   ac001 LOSS / ac002 WIN / ac003 WIN / ac004 LOSS)。

## 監査 (`audit_cr.py` corrected `2ab974c3…`・schema
`n11-centralreply-closure-class34269-batch30drive1-thirdimpl-audit-v1`)

**ALL 148 GATES PASS**・3回実行byte一致 (audit-run1/2/3.txt・
audit-summary.json + run1/2/3 同一sha)・決定的 (タイムスタンプ不読)・
verdict_agreements 4/4 (WIN=2 LOSS=2)・wall_inconclusive 0。gate内訳:
G0 input CSV×rows.json一致 (121-bit keyのPython int完全一致)・G1 pinned
script bytes×3・rows-schema (`consumed_into_canonical_cache: false` +
`unadopted_win_rows: true` + `unadopted_loss_rows: true` + canonical cache sha
不変pin `854800f3…`) + target-count 4・G2 rules gate×2・G2b replica再現×4
targets (present/done/quads/det-pair/schema/key/verdict-vs-published)・G3
anchors×2・G4 negatives×2 fail-closed・G5 targets ×4 (key/legal/quads/
det-pair/verdict-agree)・**G6 unadopted補強×4 targets** (raw pin ac001..ac004
p1/p2×8・merged cache pin・6,301行・対象row不在0回・同key競合rowゼロ・
increment pin (7 rows byte一致) + ADOPTED set header + manifest pin +
loss_ids [aa015,aa017,aa018,aa023,aa024,aa029,aa036] + 対象idがmanifest内
いかなるid listにも不在・merger `90711961…`)・**G7 val-gate 4/4 node-exact**。

- **maker tamper battery 8/8検出** (scratch /tmp copy上: T1 raw ac001.p1
  nodes+1・T2 完了log pin表sha末尾反転・T3 README-cp文言反転・T4 status-cp
  ac001 PASS verdict反転・T5 published-input ac001 legal反転・T6 BF anchor
  k02a lo+1・T7 batch-keys s5_index +1・T8 merged-cache行nodes+1)。ABORT
  sha≠pinで全検出・clean control PASS (rows.json byte-identical)・battery後の
  実験dir bytes不変。
- **audit tamper battery 4/4検出 + clean control PASS** (scratch copy上: A1
  PIN_THIRD末尾反転 → `pin-third_impl.js` fail・A2 targets ac001.b expansions+1
  → `target-ac001-det-pair` fail・A3 input CSV ac001 legal 88→87 →
  `input-ac001-matches-rows` fail・A4 audit内PIN_MERGED_CANONICAL末尾反転 →
  `rows-schema` fail。実験dir bytes不変。

## 誠実な開示 (宣言に対する逸脱・事故・実装修正)

- **A1 push path事故** (最重大): A1初回push (commit `83af1235`) でpush_filesの
  path接頭辞 `research/experiments/` を欠落させ、46ファイルがrepo直下の誤path
  に配置された。47回のdelete_file cleanup commitsで**完全除去** (取り残し1件
  `published-input-bf/ng2.input.csv` 含む・root 404確認済み)。その後正しい完全
  pathで再push (commit `20991ead`・46ファイルfetch-back byte一致)。誤配备案外
  のファイルは作成されていないが、cleanup commits 47件が履歴に残る。
- **実行環境リセット事故**: D5 replica ac004 p2の初回実行中に実行環境の同期
  失敗で211B中断 (同一コマンド再実行で完走・status.logに追記開示)。その後
  D6完了時点で実行環境がリセットされ、ローカルscratch (kit一式+D1..D6実行
  出力) を喪失した。kitはpublished commits `20991ead`/`fb8a1476` から
  sha検証付きで復元し、**D1..D6を最初から全再実行した** (決定性のため全node
  数が1回目実行と同一であることを確認済み・wall秒数のみ再実行値)。出版され
  たoutputsは再実行版。判定への影響なし (auditはoutputsの実行値のみ機械検査)。
- **audit_cr.py構文欠陥と修正**: published A1版 (pin `13e69f88…`) は
  `PIN_RAW_CR` (8 sha値) と `PIN_INCREMENT_ROWS` (7行) のリテラル引用符が
  欠落しSyntaxErrorで起動不能だった。pin値自体は実ファイル再hashで全て
  byte正当と確認済み。A-fix (commit `d986927f`) で引用符のみ修正 (gate意味
  変更なし)・修正版 `2ab974c3…`。fetch-back byte一致確認済み。
- **maker battery初回のT2/T4 sed不適合**: 最初のbattery実行はT2/T4のsedが
  実ファイル形式と不一致で無効果 (makerが正常PASS) だったため、実効性の
  あるsedでbattery全体をやり直した (8/8検出・control PASS)。出版ファイルは
  再実行版。教訓: tamper probeは適用実効性を必ず確認する (Part CM
  「efficacy-asserted」設計踏襲)。
- A2 push時に並走セッション (K1274) のpushとfast-forward競合が1回発生・
  最新main再取得後に再pushで解消 (publish-then-execute規約どおり無理押し
  せず再取得)。

## 状態 (verdict不消費)

**標準11×11空盤・19 central-reply roots・closure class 34269 (batch-30 54キー
すべて)・および drive-1 4行 (ac001/ac002/ac003/ac004) はどの時点でもUNKNOWNの
まま。** nodes数・expansions数・ttHits数・wall秒数を勝敗として読まない。WIN行
(ac002/ac003) の採用判断もLOSS行 (ac001/ac004) と同様にscrutiny owner C++第二
実装 gate 待ちで不変 (unconsumed honest labels)。canonical cache 6,301行
`854800f3…` はread-only不変 (本Partの書込なし)。被覆・secured・root勝敗の主張
はしない。
