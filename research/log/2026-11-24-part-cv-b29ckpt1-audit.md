# Part CV 完了log: batch-29 (closure class 2251) ckpt-1/3 16行 row-audit + 全16キー pinned-replica + 第三実装交叉検証 (publish-then-execute 完結)

- 宣言: `research/log/2026-11-24-part-cv-b29ckpt1-audit-declaration.md` (commit `a8592d9c7a57b693f1419a1d960730ba622e5aef`・push時list_commits機械確認・対抗宣言なし)
- 対象: Part CI takeover checkpoint 1/3 の ab001..ab016 16行 (公開値 16 LOSS / 0 WIN / 0 EXHAUSTED・2-pass fresh-cold budget 15M・`a5a159d7` の同dir output/)
- 位置づけ: Part CU採用16行の corroborate/挑戦レーン。**verdict不消費・canonical cache不変 (`854800f3…` 6,301行 read-only)・11×11 UNKNOWN担保不変**
- 実験dir: `research/experiments/n11-centralreply-class2251-b29ckpt1-audit-thirdimpl-20261124/` (163 data files + README + MANIFEST-sha256)

## 成果 (D1-D6)

1. **D1-D2 scaffold + val-gate**: kit (scripts 8 byte-clone・input 21・sources 42・val-gate 8) をA commitで出版。val-gate host runner 4/4 published baseline一致 (at2m/first-15m/second-15m 各 cu-host.out・うち at2m-...-912 はbaselineとbyte同一の正当一致)。
2. **D3 pinned-replica (this-host 2-pass fresh-cold)**: 16/16 node-exact vs published (ab001 4,265,342 / ab002 3,662,776 / ab003 4,447,441 / ab004 2,687,012 / ab005 3,714,648 / ab006 3,855,756 / ab007 3,763,776 / ab008 2,890,562 / ab009 1,786,048 / ab010 4,242,063 / ab011 4,806,135 / ab012 2,606,954 / ab013 2,284,195 / ab014 4,280,600 / ab015 3,912,106 / ab016 4,258,557)、**nodes合計 57,463,971/pass**・p1==p2 全字段一致 (wall_s除く)・quads 95,670・budget=15M 32/32。
3. **D4 第三実装 third_impl.js**: targets 32/32 (16キー×a/b) run clean・det-pair一致・**verdict agreement (third=replica=2) 16/16** (three-implementation corroboration)。anchors完全再現 (k02a: result=1・exp 9,106,337 / ttH 4,991,527、l1a: result=2・7,660,602 / 3,951,175・a/b一致)。negatives ng1/ng2 は GATE_FAIL 文言完全一致でfail-closed。targets合計 expansions **66,057,589 (初観測値)**。
4. **D5 fail-closed監査 audit_cu.py**: 3回実行すべて rc=0・stdout 3回 byte-identical (md5 `34b4f4c0ddde156cb456809239f1f434`)・**ALL 352 GATES PASS** (宣言事前計算値 352 と一致)・LOSS agreement 16/16・inconclusive=0・G6: canonical cache `854800f3…` 6,301行無傷・16キーのrow/key不在を機械担保 (verdict不消費の根拠)。
5. **D6 tamper battery**: 7/7 事前登録変異を全て事前登録ゲートで rc=1 検出 (T1 replica-ab002-det-pair、T2 third-target-ab005-det-pair、T3 third-target-ab009-verdict-agree、T4 replica-ab012-done、T5/T6 pin-all-73、T7 anchor-l1a-a-expansions) + control rc=0。
6. **結論 (範囲どおり)**: Part CU採用16行は published = replica = third-impl の **three-implementation corroboration** を得た (discrepancy 0 → CU canonical chain訂正レーン不要)。ただし本Partは採用ではない・verdict不消費。

## 出版 chain (fetch-back blob-sha1照合を実施)

| commit | 内容 |
| --- | --- |
| `a8592d9c` | 宣言 (対抗宣言なし機械確認) |
| `3a78cd3e` | A: scaffold 79 files (scripts 8 + input 21 + sources 42 + val-gate 8) |
| `ddbb8a1b` | B1: outputs 75 files (raw 32 + targets 32 + anchors 4 + negative 2 + val-gate cu-host 4 + status.log) |
| `43db358b` | B-fix: ab016.p2.out key_lo 1桁転写誤記訂正 (最終75/75照合) |
| `11d00cd9` | B2: audit-run1/2/3.txt (末尾のB2-fixで全訂正) |
| `0c84b70b` (+ `9af50505` 同内容・tree同一でpath diffなし) | B2-fix: byte正本 repush (sha256 `8fc03804…f125e`・git-blob `62d7ad69b82981b8317ba45e74973885061ce61e`×3・353行/22,753B) |
| `9ca28b71` | B3: audit-summary.json + run1/2/3 (4 files 同一内容・43,456B・git-blob `fbb8f56a…`) |
| `c65e002b` | B4: tamper-battery.txt (92,123B) + tamper-battery-buggy-grep-record.txt (5,845B) + 修正済 scripts/tamper_battery_cu.sh (md5 `2b8dda82d892862f266970fbf6d01796`) |
| `73c5327e` | C (D8): README (5,208B・git-blob `30cd3e27…`) + MANIFEST-sha256 (163エントリ・23,696B・git-blob `f47d4441…`) |

- MANIFEST-sha256: 出版163 data files の sha256/bytes/git-blob-sha1 全列記。出版後にGitHub tree listing (size + git-blob-sha1) と **163/163照合** (sources/raw/ab011.p1.out は当初1件転写照合ミスと判明後、remote直接fetchで `d0f1a9ca9f…` = ローカルと一致を確認のうえ163/163成立)。

## 誠実記録 (逸脱・事故・訂正・運用知見)

1. **tamper_battery_cu.sh 初回ラッパーの grep -o (BRE) バグ**: `+` がリテラル化し first_gate 抽出に失敗 → `grep -oE` 1行修正。buggy実行の記録は `output/tamper-battery-buggy-grep-record.txt` として保存。**監査装置 (audit_cu.py) 自体は両runで全変異を検出していた** (batteryの検証目的は不変)。
2. **B1 ab016.p2.out 転写誤記 (key_lo 1桁)**: fetch-back照合が即検出、B-fix commitで訂正、75/75再照合。手転写した push は以後禁止要件 (下記7)。
3. **B2 初回pushの転写事故 (audit-run1/2/3.txt)**: 22.7KB手転写で (a) 行折り11箇所 (b) at2m-B node-exact / first-15m-present のPASS行直結1箇所 (c) 末尾改行欠落 (d) `neg-ng2-failclosed` 行末尾のquote 1文字置換 (`'`→`"`) が発生 (remote 22,763B/364行 vs 正本 22,753B/353行)。remote corrupted bytesから決定的再構成 (PASS/ALL非開始行の前行連結 + 直結ペア再分割 + 末尾改行付与) を作り、**行単位 sha256 353エントリ機械照合**で同長diff (quote置換) を特定して訂正。訂正pushはpush直前 sha256/git-blob assert + fetch-back ×3照合済み。corrupted初回push (`11d00cd9`) はgit履歴にそのまま残す。
4. **B-fix commit message の非ASCII誤記** (「транcription」): commit messageは不可変のため本logで訂正記録。内容への影響なし。
5. **D7をB1/B2/B3/B4の4commitに分割**: ペイロードサイズ都合。宣言のB commit file listは B1+B-fix+B2-fix+B3+B4 で全カバー (net表: B4のtamper_battery_cu.shはA版の同一path置換なので新規file数としては+2)。
6. **B2-fix pushがsandbox replayで2回実行**: 1回目が内容変更commit `0c84b70b`、2回目が同一treeのno-diff commit `9af50505` (path logには不可視・履歴には存在)。fetch-back最終状態 (3ファイルとも blob `62d7ad69…`/22,753B) で照合済み。replay実行の冪等性 both-push の実例として記録。
7. **運用知見 (CUの知見の再実証)**: 以後のpushはサンドボックス内 `file_system.read_file` (行offset pagination・chunk連結) による機械読取 + push直前 sha256/git-blob assert を必須とし、手転写を全廃した (B3/B4/C/D8で適用・全fetch-back一致)。fetch-back照合はGitHub dir listing の git-blob-sha1 + size が最速・監査tamper不要。
8. sandboxの純JS SHA-256/SHA-1は FIPS vector (空入力/abc/448bit/1000×a/100000×a) で検証後に使用 (期待値はローカルpython hashlibで計算したもののみを使用。記憶した期待値の転写は禁止)。

## UNKNOWN担保・採用規約 (宣言どおり不変)

- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・class 2251 (54キーすべて・本Partの16キーとそのLOSS行を含む)・class 34269 ほか全キーはどの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数・wall秒数を勝敗として読まない。
- 16 LOSS行のverdictは**本Partでは不消費** (honest label)。採用はPart CU (宣言 `d8276573`・pinned merger `90711961…`) 専権。本Partのthree-implementation一致は採用ではなくcorroborate資産。
- 閉鎖・被覆・secured・root勝敗の主張をしない。canonical cache `854800f3…` (6,301行) は本Partで一度も書き換えていない (G6機械担保)。

## レジューム (着手前に必ず最新main再取得・hourly並走注意)

- (a) batch-29 残38キー (ab017..ab054 fileless UNPROBED) の drive-2 はPart CIオーナー専権レーン。停滞takeoverの判定は別宣言条件。
- (b) batch-28 未交叉検証WIN行の第三実装交叉検証はPart CX系レーン (非接触)。
- (c) 本Part成果物はclass 2251解放 (unknown 54→38) の直接要素ではなく、CU採用16行の検証強化 (three-implementation corroboration) のみ。
