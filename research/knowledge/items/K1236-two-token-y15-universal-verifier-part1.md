---
id: K1236
title: "2トークン残余ゲーム y=15族の全称証明 part1: 正本検証器 verify_y15_universal.py 12機械チェック全 PASS（正本監査2段階のpart1・昇格判定はpart2）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier part 1 for the two-token y=15 residual family H(R;(x,15);z): raw-engine anchored 12-check machine, overall PASS with 6,349,309 comparison points and bad 0"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, type machine with clip window 2y+2=32 sentinel 33 and 335,658 types, tightness probe showing clip 31 has 2,030 confluence violations (first (60,94,94)) so 32 is tight (11-family streak y=5..15: 12/14/16/18/20/22/24/26/28/30/32)"
  - "census anchor z=0..79, x=15..70, R<=x+z+16 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (443,520 points each, 15s/19s in run 1) and fail-closed merged in the C11 mode with recomputed expected counts (points 443,520 / merge 135,975 / tail 4,480 per engine)"
  - "merge corollary x<=z-16 implies single_token(x+15,z,R) verified at 1,304,870 points (first raw-engine anchoring of the y=15 merge region, containing no probe-box merge row by construction) and tail corollary R>=x+z+16 implies (x+15) mod 2 verified at 195,917 points, both with 0 mismatches"
  - "3 byte-identical runs total: audit.json plus both census part files identical across same-cwd reruns and an isolated tree/cwd/HOME run with PYTHONHASHSEED=random (census parts regenerated on the isolated side); K1235 status remains observed until part2 (C1d published-slice anchors at y=15 plus census_rows.py third implementation)"
relations:
  - type: extends
    target: "K1235"
    note: "K1235（y=15族 fit・cand15・出版時 observed）の正本監査段階 part1。A子=x==15 なら cand14(z,15,R-1)（合流子 (14,15)≡(15,14) の多重集合同値・x>=16 は cand15(z,x-1,R-1)）・B子=出版 cand14（K1233 全称）・C子=1 xor cand15(z-1,x,R-1) の12チェック。observed→proved の昇格判定は part2（C1d・census_rows.py 第三実装・C11r）で行う"
  - type: depends_on
    target: "K1233"
    note: "B子の逐語転写元・K1233 の全称証明（y=14族・K1234 part1/part2 機械で observed→proved 昇格済み）。cand14 ブロックは出版 verify_y14_universal.py part2 正本（commit 7026c860・SHA-256 6ac219cf…）からブロック内 Y→Y14 改名（24箇所 count-assert）のみで転写。y=15 における使用範囲は x>=15 行で K1233 の定義域 x>=14 の内側"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary）"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/README.md
  role: document
  note: "実験README（機械構成・転写照合・12チェック結果表・bounded-memoization twin設計〔y12/y13/y14 part1と同一設計〕・3回決定性・fail-closed 3件・再現コマンド・昇格判定はpart2に保留・CI step不登録の理由・解釈規約）"
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/verify_y15_universal.py
  role: verifier
  note: "正本検証器 part1出版byte（12チェック版・37,381 bytes・SHA-256 583252cc…・942行・C11ordered/C11canonical/C11モード・機械組み立てscriptの再生成物とbyte一致）"
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/scripts/build_verify_y15.py
  role: verifier
  note: "機械組み立てscript（SHA-256 034683a4…・marker限定segment抽出+cand14ブロック Y→Y14 改名24箇所count-assert・part1コードの禁止/必須トークンgate）"
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/published_verify_y14_universal.py
  role: verifier
  note: "母体の出版byte pin（y=14 part2正本・SHA-256 6ac219cf…・builderがSHA照合で消費）"
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/published_cand15.py
  role: verifier
  note: "cand15転写元の出版byte pin（K1235 fit正本・SHA-256 f61997dd…・builderがSHA照合で消費・fit driver省き）"
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/output/audit.json
  role: data
  note: "12チェック監査正本（total_points 6,349,309・total_bad 0・type_count 335,658・SHA-256 9f12d6e7…・3実行byte-identical・チェック名明示フル実行で正本確定）"
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/output/census-ordered.json
  role: data
  note: "C11ordered part正本（486 bytes・443,520点・bad 0・merge 135,975/tail 4,480付帯・run1実測15秒）"
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/output/census-canonical.json
  role: data
  note: "C11canonical part正本（488 bytes・443,520点・bad 0・run1実測19秒）"
- path: research/experiments/vertical-fiber-two-token-y15-parametric-allz-proof-20261122/output/published_run.txt
  role: log
  note: "実行記録（builder組立・出版前smoke spot 6種2万2千点・run1-3 transcript・fail-closed 3種捕捉・監査上書き注意・seed・環境）"
- path: research/log/2026-11-22-y15-universal-verifier-part1.md
  role: log
  note: "part1研究log（宣言・機械構成・実行・出版系列・採番3点確認）"
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,15)に対する正本検証器12チェック（C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12）
  の機械監査。cand15（K1235出版閉形式）が両生エンジン・K0832単一トークン表・出版cand14（B子・K1233全称）・
  x=15合流子 (14,15)≡(15,14) の生アンカーで照合され、型機械（clip窓2y+2=32・番兵33）がbox ±60で
  (value, sorted子) の完全収束を示し、総照合点6,349,309・全bad 0。corollary merge（x<=z-16 →
  single_token(x+15,z,R)）1,304,870点（fit probe box内マージ行0行を埋める初の全域raw anchor）・
  corollary tail（R>=x+z+16 → (x+15) mod 2）195,917点もbad 0。C4t tightness probeでclip 31（2y+1）に
  2,030点の型収束違反（最初 (60,94,94)）があるためclip 2y+2=32がtightで、2y+2 clip tightが
  11族連続（y=5..15: 12/14/…/30/32・最初違反がband下端とともに歩く (60,90,90)/(60,92,92)/(60,94,94)
  の3点観測）。census box（z=0..79・x=15..70・R<=x+z+16・443,520点/エンジン・80*56=4,480行）は
  bounded-memoization twin（LRU cap 1,600,000）でengine別コマンド分割し幾何再計算期待値で
  fail-closed merge。3回実行byte-identical・fail-closed 3種捕捉。K1235のobserved→proved昇格判定
  （C1d出版固定z切片アンカーのy=15行特殊化+census_rows.py第三実装+C11r）はpart2に留保される。
evidence: >-
  単一オーナー宣言（commit c34a19ff・2026-11-22T20:33台・観測HEAD bcc761b8・対抗宣言不存在確認済み・
  part1 12チェック+part2昇格を保持範囲・宣言は検証器実行前に出版）の下で、出版 y=14 part2 正本機械
  （commit 7026c860・SHA-256 6ac219cf…）と出版 cand15.py（K1235・commit 8222f6f6・SHA-256 f61997dd…）
  から機械組み立てした verify_y15_universal.py（SHA-256 583252cc…）のフル12チェック実行:
  C1 22,515〔両生エンジン・z=0..14・x=15..33・R<=x+z+47〕/C1b 43,228〔K0832単一トークン・
  出版cand14（B子）raw anchor・x=15合流子 (14,15)≡(15,14)〕/C2 218,834〔閉形式恒等式格子〕/
  C2b 19,228〔深tail行 z∈{60..400}〕/C3 1,215〔選択肢分解の生エンジン子列挙照合〕/
  C4 601,255〔型機械clip 32/番兵33・C4時点279,619型・identity/confluence とも0〕/
  C4t clip 31で2,030違反・最初 (60,94,94)〔bad総計外〕/C7 200,000〔seed 20261152・z,x<=3000〕/
  C8 993,180〔境界多様体・dx∈[-30,17]・tail窓 [x+z+16, x+z+18]・x=14行は閉形式extension-consistency行〕/
  C9 908,202〔v空間シェル〕/C11 887,040〔両part merge〕/C12 1,853,357〔深格子 z=0..120・x=15..120・
  R<=x+z+17〕のoverall PASS・total_points 6,349,309・total_bad 0・型総数 335,658。
  組立時健全性spot 6種（cand15 vs 生エンジン 2,016点・merger (14,15)≡(15,14) 808点・y=14 B子
  8,580点・raw選択肢集合 vs 閉形式選択肢 3,060点・マージ行の生エンジン全域照合 3,960点〔z=31..40・
  40行・fit probe boxが構成上含めなかったマージ領域の初のraw anchor〕・tail行 4,030点）はすべて
  不一致0（機械実行前にpublished_run.txt記録）。census 443,520点/エンジン・run1実測 ordered 15秒・
  canonical 19秒・12チェック一括実行33秒。決定性: audit.json・両census partとも同一cwd 2回＋
  隔離tree/cwd/HOME+PYTHONHASHSEED=random 1回（census partsは隔離側で再生成しbyte一致）の
  3実行byte-identical。fail-closed: census points改ざん（443,520→443,521）・part欠落・
  corollary merge境界改ざん（x<=z-16→x<=z-15・total_bad 223でoverall FAIL）の3種をすべて捕捉・
  baseline復元byte確認。builder再生成物は実行物とbyte一致（出版前に再確認）。
---

# 2トークン残余ゲーム y=15族 全称証明 part1（正本検証器12チェック）

単一オーナー宣言（[宣言ノート](../../log/2026-11-22-y15-universal-verifier-single-owner-note.md)・
commit `c34a19ff`・observed HEAD `bcc761b8`・part1 12チェック+part2昇格を保持）に基づく
y=15 族全称段階 part1。対象は [K1235](K1235-two-token-y15-parametric-closed-form-fit.md)
（fit・status observed・初稿一発一致74,865点・「次段階は別宣言」と明記）の正本監査段階である。

## 機械構成

verify_y15_universal.py（SHA-256 583252cc…）は出版 y=14 part2 正本機械（SHA-256 6ac219cf…・
commit 7026c860）と出版 cand15.py（K1235・commit 8222f6f6・SHA-256 f61997dd…）から
`scripts/build_verify_y15.py`（SHA-256 034683a4…）で機械組み立てした（生2エンジン + K0832
単一トークン表 verbatim〔K1138以来のbyte〕・cand14ブロック（B子）はブロック内 Y→Y14 改名のみ
〔改名24箇所 count-assert・K1233全称証明済み族〕・cand15ブロックは出版 cand15.py から fit driver
を除き verbatim・消費 byte は実験dir内のpublished_* pin として同梱しbuilderがSHA照合）。
B子 = 出版 cand14（K1233 全称・全称証明済み族をB子に逐語転写するのは y11..y14 機械
〔B子=cand10/11/12/13/14〕に続き **5 連**）。x=15 合流子 (14,15)≡(15,14) の子値は多重集合として
同値で cand14(z,15,R-1)（y=14族 x=15 行・A子合流の正準順序扱いは y=14 の (13,14)事故知見を適用）。
機械本体の差し替え点は clip 窓 2y+2=32・番兵 33・census box z=0..79・x=15..70・R<=x+z+16
（80*56=4,480行）・merge x<=z-16・tail (x+15)%2・C12 深格子 R<=x+z+17。

## 実行結果（overall PASS）

12チェック（C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12）総照合点 6,349,309・全 bad 0。
型機械は clip 窓 2y+2=32・番兵 ±33 で型総数 335,658 の (value, sorted子) 完全収束
（C4時点 279,619 型）。C4t tightness probe で clip 31（2y+1）は 2,030 点の収束違反・
最初 (60,94,94) があるため **clip 2y+2=32 が tight、2y+2 clip tight は 11 族連続
（y=5..15: 12/14/16/18/20/22/24/26/28/30/32）**。merge corollary（x<=z-16 →
single_token(x+15,z,R)）1,304,870 点（y=15 のマージ領域 z>=31 は fit の probe box
z=0..30 に存在しなかったため、本行が**マージ命題の初の全域 raw anchor**）・
tail corollary（R>=x+z+16 → (x+15) mod 2）195,917 点、ともに不一致 0。

## C11 census の bounded-memoization twin

census box（z=0..79・x=15..70・R<=x+z+16・443,520 点/エンジン）は、y12/y13/y14 part1 と
同一設計の出版エンジン code object 再束縛 LRU 上限 1,600,000 キャップ付き双生機で
engine 別コマンド分割（C11ordered 15秒/C11canonical 19秒・run1 実測）し、C11 モードが両 part を
engine 名・box・cache 上限・幾何からの再計算期待値（443,520/135,975/4,480）・bad==0 で
fail-closed 検証して merge する。part ファイルの 1 点改ざん・part 欠落・corollary 境界改ざんの
3 種を出版前に実施しすべて捕捉した（published_run.txt）。

## 決定性

audit.json・census-ordered.json・census-canonical.json の 3 ファイルとも、
同一 cwd 2 回＋隔離 tree/cwd/HOME+PYTHONHASHSEED=random 1 回（census parts は隔離側で再生成）の
3 実行で byte-identical。

## 解釈規約

- K1235 の status は本 part1 出版時点で **observed のまま**。昇格判定は part2（C1d 出版固定z切片
  アンカーの y=15 行特殊化・preflight fail-closed + census_rows.py 第三実装 + C11r・3回
  byte-identical）で行う（K1141/K1152/K1231/K1233 と同一手続き・同一K項目・新規採番なし）。
- C8 内の x=14 行は閉形式 extension-consistency 行（x=15 未満への生claimはない・y=14 機械の
  x=13 行・y=13 機械の x=12 行と同一の扱い）で 0 bad。
- 有限照合は有限観察の機械的証拠であって、trust 境界（選択肢分解の健全性・mex 恒等式・
  有限型空間の完全性）は y=5..14 系列と同一の機械分類に依存する。
- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
  **UNKNOWN** のまま。本項は残余ゲーム族 H(R;(x,15);z) の数学的構造の機械検証であり、
  標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=16 族・固定幅・q点版安定化長は範囲外。
- 現行 main の knowledge.yml に y=11（K1143）・y=12（K1152）・y=13（K1231）・y=14（K1234）
  実験機の CI step が存在しないため（CI 登録は y=10/K1141 まで）、本実験も CI step を
  登録せず出版 byte を監査正本とする（直近 4 族と同一の扱い）。
