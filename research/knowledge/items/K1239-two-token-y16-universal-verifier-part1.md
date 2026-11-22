---
id: K1239
title: "2トークン残余ゲーム y=16族の全称証明 part1: 正本検証器 verify_y16_universal.py 12機械チェック全 PASS（正本監査2段階のpart1・昇格判定はpart2）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier part 1 for the two-token y=16 residual family H(R;(x,16);z): raw-engine anchored 12-check machine, overall PASS with 6,331,848 comparison points and bad 0"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, type machine with clip window 2y+2=34 sentinel 35 and 394,686 types (y=13: 234,180 clip 28 -> y=14: 281,912 clip 30 -> y=15: 335,658 clip 32 -> y=16: 394,686 clip 34), tightness probe showing clip 33 has 1,638 confluence violations (first (60,96,96)) so 34 is tight (12-family streak y=5..16: 12/14/16/18/20/22/24/26/28/30/32/34)"
  - "census anchor z=0..79, x=16..70, R<=x+z+17 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (442,200 points each engine, 55 x-rows per z, 18.1 s / 19.5 s run 1) and fail-closed merged in the C11 mode with recomputed expected counts (points 442,200 / merge 127,464 / tail 4,400 per engine)"
  - "merge corollary x<=z-17 implies single_token(x+16,z,R) verified at 1,243,466 points (first full raw-engine anchoring of the y=16 merge region - the first family whose probe box contained zero merge rows) and tail corollary R>=x+z+17 implies (x+16) mod 2 verified at 193,300 points, both with 0 mismatches"
  - "3 byte-identical runs total: audit.json plus both census part files identical across same-cwd reruns and an isolated tree/cwd/HOME run with PYTHONHASHSEED=random (census parts regenerated on the isolated side); K1237 status remains observed until part 2 (C1d published-slice anchors at y=16 plus census_rows.py third implementation)"
relations:
  - type: extends
    target: "K1237"
    note: "K1237（y=16族 fit・cand16・出版時 observed）の正本監査段階 part1。A子=x==16 なら cand15(z,16,R-1)（合流子 (15,16)≡(16,15) の多重集合同値・x>=17 は cand16(z,x-1,R-1)）・B子=出版 cand15（K1235 全称）・C子=1 xor cand16(z-1,x,R-1) の12チェック。observed→proved の昇格判定は part2（C1d・census_rows.py 第三実装）で行う"
  - type: depends_on
    target: "K1235"
    note: "B子の逐語転写元・K1235 の全称証明（y=15族・K1236 part1/part2 機械で observed→proved 昇格済み）。cand15 ブロックは出版 verify_y15_universal.py part2 正本（commit 0bf18752・SHA-256 a39e7ab1…）からブロック内 Y→Y15 改名（102行ブロック・改名を除きbyte照合）のみで転写。y=16 における使用範囲は x>=16 行で K1235 の定義域 x>=15 の内側"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary）"
  - type: extends
    target: "K1238"
    note: "偶数y統一テンプレート機械検証の次段階として宣言ノートが指名した verify_y16_universal.py 着手。K1238 の再生物ではなく独立の12チェック機械（cand16 は出版 cand16.py から逐語・fit driver省き・92行byte照合）"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/README.md
  role: document
  note: "実験README（機械構成・転写照合・12チェック結果表・bounded-memoization twin設計〔y=12..y=15 part1と同一設計〕・3回決定性・fail-closed 6件〔census部品gate 4種+Y/Y15定数改ざん2種〕・(x,15)族入れ替え事故の誠実記録〔fail-closedが147,972 badで自捕獲→修正→全面再実行〕・再現コマンド・解釈規約）"
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/verify_y16_universal.py
  role: verifier
  note: "正本検証器 part1出版byte（12チェック版・37,042 bytes・SHA-256 79e21b2d…・C11ordered/C11canonical/C11モード・機械組み立てscript scripts/build_verify_y16.py の再生成物とbyte一致〔2回〕）"
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/output/audit.json
  role: audit-output
  note: "12チェックフル実行の正本監査（overall PASS・total_points 6,331,848・total_bad 0・types 394,686・verifier_sha256 79e21b2d…・SHA-256 7b5acc8c…・3実行byte-identical）"
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/output/census-ordered.json
  role: audit-output
  note: "C11ordered 部品（442,200点 bad 0・merge 127,464 bad 0・tail 4,400 bad 0・SHA-256 fd94dda3…）"
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/output/census-canonical.json
  role: audit-output
  note: "C11canonical 部品（同幾何 bad 0・SHA-256 3934307f…）"
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/output/published_run.txt
  role: run-log
  note: "実行順序・事前smoke anchor・HONEST INCIDENT RECORD（(x,15) slip→147,972 bad自捕獲→修正→全面再実行）・決定性sha 3回・fail-closed battery T1-T5b・解釈規約"
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/scripts/build_verify_y16.py
  role: build-script
  note: "機械組み立てscript（pinned source 2本を読み込み・count-asserted substitution・再生成byte-identical）"
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/published_verify_y15_universal.py
  role: pinned-source
  note: "出版 y=15 part2 正本検証器（commit 0bf18752・SHA-256 a39e7ab1…）のpin・正本機械の転写元"
- path: research/experiments/vertical-fiber-two-token-y16-parametric-allz-proof-20261122/published_cand16.py
  role: pinned-source
  note: "出版 cand16.py（K1237 fit 実験・commit 33e1c22e・SHA-256 1fc9d22b…）のpin・cand16ブロックの逐語転写元（fit driver省き）"
---

# 計算結果（part1・2026-11-22）

単一オーナー宣言 `research/log/2026-11-22-y16-universal-verifier-single-owner-note.md`
（commit `432664f7`・2026-11-22T22:49:53Z・宣言時点観測 HEAD `76abc080`・対抗宣言 grep clean・
probe/検証器実行前に事前出版）の下、y=16族の全称検証器 part1 を実行した。

## 12チェックの実績値

- C1 22,800 / C1b 41,834 / C2 217,021 / C2b 19,316 / C3 1,245 / C4 595,990 /
  C4t 595,990（探査・bad総計外） / C7 200,000 / C8 992,652 / C9 905,670 /
  C11 884,400 / C12 1,854,930 = **総照合点 6,331,848・全 bad 0**
- 型総数 394,686（clip 34/sentinel 35・y=13 234,180→y=14 281,912→y=15 335,658に続く4点目）
- merge 帰結 x<=z-17 → single_token(x+16,z,R) 1,243,466点 bad 0
  （**マージ領域の初の全域raw anchor**・y=16はfit probe box内マージ0行の初族）
- tail 帰結 R>=x+z+17 → (x+16)%2 193,300点 bad 0
- **C4t: clip 33（2y+1）違反 1,638・最初 (60,96,96) → clip 2y+2=34 は tight・12族連続**
  （12/14/16/18/20/22/24/26/28/30/32/34・最初の違反がband下端と共に歩く即約2族連続も継続:
  y=13 clip27 (60,90,90)・y=14 clip29 (60,92,92)・y=15 clip31 (60,94,94)・y=16 clip33 (60,96,96)）

## 決定性・fail-closed

- audit.json（SHA-256 7b5acc8c…）・census両部品とも 3 実行 byte-identical
  （同一cwd 2回 + 隔離tree/cwd/HOME + PYTHONHASHSEED=random・census部品は隔離側で再生成しbyte比較）
- fail-closed battery 6件全捕捉（census部品 points改ざん 442,200→442,201・部品欠落・
  merge corollary bad改ざん・box field改ざん→FAIL-CLOSED、cand16ブロック Y 16→17→C1 903 bad・
  B子ブロック Y15 15→16→C1b 777 bad→FAIL）・復元byte確認済み

## 誠実な事故記録（fail-closedが設計どおり作動）

- 出版前の初回 C11ordered が 442,200点中 **147,972 bad** を自報告した。原因は run_census の
  rawエンジン呼び出しtupleが族15 `(x, 15)` のまま（builderのrenameが到達しなかった末尾リテラル）。
  bad の分布が y=15族バイアスと一致したことで診断・builder count-asserted修正・機械byte再生成・
  census全面再実行で bad 0。この事故は census raw anchor が捕捉する設計どおりの事故型
  （y=10 preflight が K1087 初稿の評価順序バグ 170点を捕捉したのと同型）であり、
  bad監査バイトは一つも出版していない。経緯は published_run.txt と実験READMEに全記録。

## 限界と次段階

- 本項は K1237 全称命題の機械的証拠（part1）であり、**observed→proved 昇格は part2**:
  C1d（出版固定z切片アンカー A8u..A17u の y=16 行・preflight fail-closed・
  出版 verify_y15 正本から逐語転写）と census_rows.py（y=16版第三実装・XMIN=16・XMAX=70・RBUF=18）
  による C11r を組み込んだフル14チェックで判定する（K1141/K1152/K1231/K1233/K1235 と同一手続き）。
- part1 は 11×11 標準盤・二石root・S2・class 1/2/4 には一切触れない（UNKNOWNのまま）。
  3トークン以上・y>=17族・固定幅・q点版安定化長は範囲外。
