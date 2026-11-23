# Part CR completion: batch-30 (closure class 34269) drive-1 4行 ac001..ac004 第三実装交叉検証 + 本host pinned-replica 2-pass + Part CO adoption出版物unadopted補強gate (2026-11-23)

Part CR完結。publish-then-execute規約どおり、宣言 `research/log/2026-11-23-part-cr-b30drive1-thirdimpl-declaration.md`
(observed HEAD `dd68c4d6`・fetch-back byte一致 sha256 `b9b3d4a5…`) → A scaffold
(初回push `83af1235` は誤path事故・下記誠実記録 → cleanup 47 commits → 正path再push
`20991ead` 46 files → A2 canonical cache `fb8a1476` → A-fix audit_cr.py `d986927f`)
→ B outputs `001278ac` (37 files) → C README+MANIFEST `c30a5ab` → 本完了log。
**verdict不消費・11×11 UNKNOWN担保不変**。

## 成果

1. **batch-30 drive-1 4行の three-implementation corroboration成立**。
   published drive-1 replica 2-pass (Part CP) + 本host pinned-replica 2-pass
   (budget 15M fresh-cold) + 第三実装 minimax 2-run (a/b) がすべてverdict一致:
   - **ac001 LOSS (result 2)**: replica nodes 5,635,468 (p1=p2 node-exact)・
     third-impl expansions 6,522,042 (a=b det-pair clean)
   - **ac002 WIN (result 1)**: replica nodes 10,752,246・third-impl expansions
     12,569,497
   - **ac003 WIN (result 1)**: replica nodes 8,036,766・third-impl expansions
     9,415,378
   - **ac004 LOSS (result 2)**: replica nodes 5,816,333・third-impl expansions
     6,802,090
   **drive-1 4行の最初の独立セッション再現 + 独立第三実装 (非df-pn AND/ORミニ
   マックス) による交叉検証**。pass-one third-impl拡張数合計 35,309,007。
   WALL-INCONCLUSIVE 0・DIVERGENCE 0・EXHAUSTED 0・mismatch 0。
2. **rules gate PASS**: pinned `verify_tbl.js` `c8c52528…`・replica quads
   95,670 == third-impl quads 95,670・triples 195,044・mismatches 0。
3. **val-gate this-host 4/4 node-exact** (published baselinesと完全一致・
   `.cr-host.out` 4件出版)。
4. **anchors 4/4 node-exact** (k02a 9,106,337/4,991,527・l1a 7,660,602/
   3,951,175・a/b det-pair PASS)。**negatives 2/2 GATE_FAIL設計どおり**。
5. **監査 ALL 148 GATES PASS × 3回byte一致** (`audit_cr.py` corrected
   `2ab974c3…`・決定的)。G6 unadopted補強: 4行ともPart CO merged canonical
   cache (6,301行 `854800f3…`) / increment (`bd5ef7d7…`・7 rows) /
   increments-manifest (`b47e07ca…`) 内のいかなるid listにも不在・対象row不在
   0回・同key競合rowゼロ (verdict不消費の機械担保)。
6. **tamper batteries**: maker 8/8検出 (sha≠pin ABORT ×8・clean control PASS・
   実験dir bytes不変)・audit 4/4検出 + clean control PASS。

## output sha pin表 (B commit `001278ac…`・全37ファイルはMANIFESTに個別pin)

| file | sha256 |
| --- | --- |
| `output/status.log` | `65065b973a106839da56955e53440bb90e1ca87a8ab9ccffa21a443ffffab66f` |
| `output/rules-gate.txt` | `88c0b78b2251ea799dbe3a91df0fb56f532ec95e991290ff179ebb918466c863` |
| `output/audit-summary.json` | `c0c73e0d53652e9ec431523933165649e847e365c919bfbc0b1a004bb420365b` |
| `output/audit-run1.txt` | `1c48a39c4194e89f5ecf1c614fd46db2b8c12e791144a7e10f07658f0e63f536` |
| `output/targets/ac001.a.out` | `c5b81087c12db74c664c68aea725567e2be507e1feb6765f8797db7d3192de6c` |
| `output/targets/ac001.b.out` | `21257c7e87c07ee5aaa9044c11a8a1180d12452a4d12f9ef51d528ef34aae9ce` |
| `output/targets/ac002.a.out` | `1cd4bf66f7ff0218eac9fcdc40670d7dfd9894a73e75f63227f8b8c32c654e49` |
| `output/targets/ac002.b.out` | `0748107ea3b6ca12d2327f5e89aa6fa1b01c0a9520c365584c2cc4c1b0ea7cc2` |
| `output/targets/ac003.a.out` | `17424345091f487115613771a1b0c7e8d14842f3b74ffa324494c54b73f81298` |
| `output/targets/ac003.b.out` | `259a9579f536b205197b521f6157019973832da38ad44dddf282e404cbc27058` |
| `output/targets/ac004.a.out` | `393f45deaa624b223850b6af67588b5c72c7c8c1e152bf7077473a00ea98c131` |
| `output/targets/ac004.b.out` | `95da6600bd2da2d031c80e68a75c680c63fbf0a31838c1909beda956cc9be702` |
| `output/replica/ac001.p1.out` | `38d821ef3814578c06c6a68848ad0c5ea2c7a46b58a5ff45f198a782d1622223` |
| `output/replica/ac001.p2.out` | `9c3cbd0d9c37a6ef4bcd77c08d7753432489258ba73c10ec71325de0356e1c40` |
| `output/replica/ac002.p1.out` | `df09f3654d306cf47dc63aaa1dacd159f18f884ed7d27ffdfe6e0f729ddbf2dc` |
| `output/replica/ac002.p2.out` | `df09f3654d306cf47dc63aaa1dacd159f18f884ed7d27ffdfe6e0f729ddbf2dc` |
| `output/replica/ac003.p1.out` | `5ccf0f4f8967bec327dfd8d0afd3f1ba60fd30d0bbd844ef87bfb9d9daf97812` |
| `output/replica/ac003.p2.out` | `5b656bb4a3f9ff2facb78d24c12a8542b92724d10c336032d265db860e090967` |
| `output/replica/ac004.p1.out` | `db2abad6c05d19a9e0a687483bedbdb70fb54b1c3abf11aa8458b7d2ec3df3ce` |
| `output/replica/ac004.p2.out` | `db2abad6c05d19a9e0a687483bedbdb70fb54b1c3abf11aa8458b7d2ec3df3ce` |

ac002とac004のreplica p1/p2はbyte-同一 (wall_s同桁のため)・ac001/ac003は
wall_sのみ相違 (node-exact gate PASSは全キーで機械検査済み)。status.logは
RUN 12行 + REPLICA 8行 + PROTOCOL [1]..[9] (Part CM形式・出力ファイル群から
機械生成)。

## 誠実記録 (incidents)

1. **A1 push path事故 (本Part最大の事故)**: A1初回push (commit `83af1235`) で
   push_filesのfile pathに接頭辞 `research/experiments/n11-centralreply-…-20261123/`
   を欠落させ、46ファイルがrepo直下 (`scripts/`・`sources/`等) に誤配置された。
   対応: 誤配置46ファイルを1件ずつdelete_fileで除去 (47 cleanup commits・最後の
   取り残し `published-input-bf/ng2.input.csv` 1件も除去・connectorでroot 404確認)。
   その後正しい完全pathでA1再push `20991ead` (46ファイルfetch-back byte一致)。
   誤配備中に他セッションが誤ファイルを観測しなかったことを確認済み (競合push
   なし)。cleanup commits 47件は履歴に残る (削減手段なし)。
2. **実行環境リセット事故 (2件)**: (a) D5 replica ac004 p2の初回実行中に環境の
   同期失敗で211B中断 → 同一コマンド再実行で完走 (status.log追記開示)。その後
   (b) D6完了直後に環境リセットでローカルscratch (kit+D1..D6実行出力) を喪失。
   対応: kitをpublished commits `20991ead`/`fb8a1476` からsha検証付き復元し、
   **D1..D6を全再実行** (決定性により1回目実行と全node数同一を確認済み・wall
   秒数のみ再実行値)。出版outputsは再実行版。判定への影響なし。
3. **audit_cr.py構文欠陥**: published A1版 (`13e69f88…`) は `PIN_RAW_CR` 8 sha値
   と `PIN_INCREMENT_ROWS` 7行の引用符欠落でSyntaxError。pin値自体は実ファイル
   再hashで全て正当 (事故ではなくkit作成時の記載ミス)。A-fix `d986927f` で引用符
   のみ修正 (gate意味不変、G1はaudit_cr.py自体をpinしない設計)・修正版 `2ab974c3…`。
4. **maker battery初回のT2/T4 sed不適合**: pin表のshaが `9903944e…` 形式で本文に
   ない前提のsed・status行のパターン誤りで無効果tamper (maker正常PASS) → 実
   ファイル形式に合わせてbattery全体やり直し (8/8検出・efficacyはcontrol PASS
   + sha≠pin ABORTで担保)。出版は再実行版 (`output/tamper-maker-battery.txt`)。
5. **push競合1件**: A2 (canonical cache) pushでK1274 (高速レーン) のpushと
   fast-forward競合 → 最新main再取得後に再pushで解消 (`fb8a1476`)。規約どおり
   無理押しせず再取得。

## 解釈ガード (不変)

- 4行 (ac001/ac004 LOSS・ac002/ac003 WIN) は**honest labelのみ** (unconsumed・
  採用判断はscrutiny owner C++第二実装 gateのまま・本レーンは代行しない)。
  **三実装一致は採用ではない**。canonical cache 6,301行 `854800f3…` read-only
  不変 (書込なし)・closure table不変。
- **標準11×11空盤・19 central-reply roots・class 34269 (54キーすべて・ac005..
  ac054含む) はどの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数・
  wall秒数を勝敗として読まない。被覆・secured・root勝敗の主張はしない。
- drive-2 (WIN-CONTINUE)・Part CI (class 2251)・Part CQ (EXHAUSTED 20M re-probe)
  ・K1274 (高速レーン) は各オーナー所有・本Partは非接触。

## レジューム (次回の着手前に必ず最新main再取得・hourly並走注意)

- 本Partの成果物はすべてcommit-pinned (A1 `20991ead`・A2 `fb8a1476`・A-fix
  `d986927f`・B `001278ac`・C `c30a5ab`)。再検証は`audit_cr.py`単独で可能
  (ALL 148 GATES・実行不要の静的gate + outputs機械検査)。
- drive-2のrowsがPart CP側で出版された暁には、本Partと同一形式のthird-impl
  交叉検証 + unadopted補強gate (drive-1 Part CR先例踏襲・audit_cr.py型の継承)
  が第三実装レーンのNEXT。drive-2出版前に着手しない (単一オーナー規約)。
- batch-30の54キー全probed後のrow-audit・closure class 34269簿記更新はdrive完走
  Partの傘下 (Part CP completionレジュームどおり・本レーンは代行しない)。
