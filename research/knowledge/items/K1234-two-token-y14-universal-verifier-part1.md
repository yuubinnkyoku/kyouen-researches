---
id: K1234
title: "2トークン残余ゲーム y=14族の全称証明 part1: 正本検証器 verify_y14_universal.py 12機械チェック全 PASS（正本監査2段階のpart1・昇格判定はpart2。part2は2026-11-22に実行されK1233のobserved→proved昇格が完了）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier part 1 for the two-token y=14 residual family H(R;(x,14);z): raw-engine anchored 12-check machine, overall PASS with 6,377,860 comparison points and bad 0"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, type machine with clip window 2y+2=30 sentinel 31 and 281,912 types, tightness probe showing clip 29 has 2,480 confluence violations (first (60,92,92)) so 30 is tight (10-family streak y=5..14: 12/14/16/18/20/22/24/26/28/30)"
  - "census anchor z=0..79, x=14..70, R<=x+z+15 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (444,600 points each, 14.8s/16.6s in run 1) and fail-closed merged in the C11 mode with recomputed expected counts (points 444,600 / merge 144,534 / tail 4,560 per engine)"
  - "merge corollary x<=z-15 implies single_token(x+14,z,R) verified at 1,370,848 points and tail corollary R>=x+z+15 implies (x+14) mod 2 verified at 212,713 points, both with 0 mismatches"
  - "3 byte-identical runs total: audit.json plus both census part files identical across same-cwd reruns and an isolated tree/cwd/HOME run with PYTHONHASHSEED=random; K1233 status remains observed until part2 (C1d published-slice anchors at y=14 plus census_rows.py third implementation)"
  - "part2 executed 2026-11-22 under the same single-owner note: C1d 138,846 pts vs published z=8/9/10/15/16/17 anchors specialised at y=14 (pre-flighted fail-closed, 4-way anchor verification 13,824 pts + low-R reduction 9,636 pts) and C11r 449,160 pts row-by-row re-derivation of the third-implementation census.txt (4,560 rows, z=0..79, x=14..70, R=0..x+z+16); full 14-check audit PASS 6,965,866 pts bad 0, 3 byte-identical runs (census and preflight regenerated on the isolated side), K1233 promoted observed to proved"
relations:
  - type: extends
    target: "K1233"
    note: "K1233（y=14族 fit・cand14・出版時 observed）の正本監査段階 part1。A子=x==14 なら cand13(z,14,R-1)（合流子 (13,14)≡(14,13) の多重集合同値・x>=15 は cand14(z,x-1,R-1)）・B子=出版 cand13（K1231 全称）・C子=1 xor cand14(z-1,x,R-1) の12チェック。observed→proved の昇格判定は part2（C1d・census_rows.py 第三実装）で行い、part2 は同一単一オーナー宣言の下で 2026-11-22 に実行・出版済み（K1233 は proved に昇格・フル14チェック監査 6,965,866 点・全 bad 0）。K1233 の独立第二検証（判定等価 2,241,162 点）が確定した同一閉形式が監査対象"
  - type: depends_on
    target: "K1232"
    note: "機械的母体（y=13 part1 正本機械・commit ee3b6f73・SHA-256 b73d9aaa…）とB子の逐語転写元（cand13 ブロックは同機械の cand13 セクションをブロック内 Y→Y13 改名のみで転写・本ブロックは出版 cand13.py〔K1231・SHA-256 cb903c56…〕の fit driver 除外逐語転写で全称証明は K1231）"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary）"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/README.md
  role: document
  note: "実験README（機械構成・転写照合・12チェック+part2 C1d/C11r 14チェック結果表・bounded-memoization twin設計〔y12/y13 part1と同一設計〕・3回決定性・fail-closed 5件・再現コマンド・observed→proved昇格判定・CI step不登録の理由・解釈規約）"
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/verify_y14_universal.py
  role: verifier
  note: "正本検証器。part1出版byte（12チェック版・commit 677ced40系・37,439 bytes・SHA-256 4ecdec11bb4b5d2c7047114228c8482eff2b09db1eb7251c37c5787dda91c34e・946行・C11ordered/C11canonical/C11モード・機械組み立てscriptの再生成物とbyte一致）とpart2拡張正本（14チェック版・51,537 bytes・SHA-256 6ac219cfe27e55e3d6057ea9dcf5db76631b8ef1c50ced0edd63f64d590f2205・1,317行・C1d/C11r追加・anchor blockはy13 part2正本検証器 079b49ad… から関数byteをverbatim抽出〔provenanceヘッダはy=14行向け実測事前検証値に書き換え〕・y13 part2と同一のin-place手続きでpart2組み立てscriptは出版せず）の2段階。part1の12チェックは挙動不変"
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/scripts/build_verify_y14.py
  role: verifier
  note: "機械組み立てscript（32,478 bytes・SHA-256 24246a5d…・segment抽出+置換カウントassert・cand13ブロック Y→Y13 改名39行count-assert・cand14ブロックは出版 cand14.py〔K1233・commit b6f74dfc・SHA-256 61782b6e…〕からfit driver省きverbatim）"
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/output/audit.json
  role: data
  note: "part2フル14チェック入り監査正本（3,674 bytes・SHA-256 b91e88a0a6dc4797220fb9dc246433907faecda654e41586cd4b0a2eb0ab3c5c・total_points 6,965,866・total_bad 0・3実行byte-identical・チェック名明示フル実行で正本確定。part1出版時は12チェック版 f8f7180f… 3,105 bytes）"
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/output/census-ordered.json
  role: data
  note: "C11ordered part正本（486 bytes・444,600点・bad 0・merge 144,534/tail 4,560付帯）"
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/output/census-canonical.json
  role: data
  note: "C11canonical part正本（488 bytes・444,600点・bad 0）"
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/output/published_run.txt
  role: log
  note: "実行記録（part1・part2両段階: run1 transcript・run2/3・fail-closed 5種捕捉・builder再生成・監査上書き注意・seed・環境）"
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/scripts/preflight_c1d_y14.py
  role: verifier
  note: "part2: C1dアンカー組み込み前fail-closed事前検証（4方照合13,824点+低R縮約9,636点・不一致0・z別2,160/2,192/2,224/2,384/2,416/2,448・2回byte-identical・SHA-256 fd449b78…）"
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/census_rows.py
  role: verifier
  note: "census第三実装（z=0..79・x=14..70・R=0..x+z+16・4,560行449,160点・値0点224,566・状態計算misses 7,146,027・LRU上限1.6M明示キャップ・約14.2秒・maxrss 639,424KB・SHA-256 aa3fe56e…）"
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/output/census.txt
  role: data
  note: "census行表正本（824,003 bytes・4,560行＋空行80・SHA-256 baad513c…・C11rでcand14から再導出して全行照合・不一致0・tailアサート全行成立）"
- path: research/experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/output/preflight-c1d-y14.json
  role: data
  note: "事前検証結果正本（SHA-256 c7369b4c…）"
- path: research/log/2026-11-22-y14-universal-verifier-part1.md
  role: log
  note: "part1研究log（宣言・機械構成・実行・出版系列・採番3点確認・scripts/誤配置修正の誠実記録）"
- path: research/log/2026-11-22-y14-parametric-allz-proof-part2.md
  role: log
  note: "part2研究log（C1d事前検証・census第三実装・14チェック監査・3回byte-identical・K1233 observed→proved昇格・fail-closed 5種・出版記録・CI step不登録の理由）"
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,14)に対する正本検証器12チェック（C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12）
  の機械監査。cand14（K1233出版閉形式）が両生エンジン・K0832単一トークン表・出版cand13（B子）・
  x=14合流子 (13,14)≡(14,13) の生アンカーで照合され、型機械（clip窓2y+2=30・番兵31）がbox ±60で
  (value, sorted子) の完全収束を示し、総照合点6,377,860・全bad 0。corollary merge（x<=z-15 →
  single_token(x+14,z,R)）1,370,848点・corollary tail（R>=x+z+15 → (x+14) mod 2）212,713点も
  bad 0。C4t tightness probeでclip 29（2y+1）に2,480点の型収束違反（最初 (60,92,92)）があるため
  clip 2y+2=30がtightで、2y+2 clip tightが10族連続（y=5..14）。census box（z=0..79・x=14..70・
  R<=x+z+15・444,600点/エンジン）はbounded-memoization twin（LRU cap 1,600,000）でengine別
  コマンド分割し幾何再計算期待値でfail-closed merge。3回実行byte-identical・fail-closed 3種捕捉。
  K1233のobserved→proved昇格判定（C1d出版固定z切片アンカーのy=14行特殊化+census_rows.py第三実装）
  はpart2に留保されたが、part2（2026-11-22・同一単一オーナー宣言）で実行・出版されK1233は
  provedに昇格した（フル14チェック監査6,965,866点・全bad 0）。
evidence: >-
  単一オーナー宣言（commit 24e418a9・2026-11-22T19:08:21Z・観測HEAD cd2c1095・対抗宣言不存在確認済み・
  part1 12チェック+part2昇格を保持範囲）の下で、y13 part1正本機械（commit ee3b6f73・SHA-256
  b73d9aaa…）と出版cand14.py（K1233・commit b6f74dfc・SHA-256 61782b6e…）から機械組み立てした
  verify_y14_universal.py（SHA-256 4ecdec11…）のフル12チェック実行:
  C1 22,230〔両生エンジン・z=0..14・x=14..32・R<=x+z+47〕/C1b 42,447〔K0832単一トークン・
  出版cand13（B子）raw anchor・x=14合流子 (13,14)≡(14,13)〕/C2 222,705〔閉形式恒等式格子〕/
  C2b 19,140〔深tail行 z∈{60..400}〕/C3 1,185〔選択肢分解の生エンジン子列挙照合〕/
  C4 606,427〔型機械clip 30/番兵31・C4時点248,232型・identity/confluence とも0〕/
  C4t clip 29で2,480違反・最初 (60,92,92)〔bad総計外〕/C7 200,000〔seed 20261142・z,x<=3000〕/
  C8 993,021〔境界多様体・dx∈[-30,17]・tail窓 [x+z+15, x+z+17]〕/C9 910,710〔v空間シェル〕/
  C11 889,200〔両part merge〕/C12 1,864,368〔深格子 z=0..120・x=14..120・R<=x+z+17〕の
  overall PASS・total_points 6,377,860・total_bad 0・型総数 281,912。
  組み立て時健全性spot 4種（cand14 vs 第二検証レーンcand14 55,692点・cand14 vs 生エンジン 2,268点・
  cand13 vs 生エンジン 1,533点・x=14 merger行 970点）はすべて不一致0。census 444,600点/エンジン・
  run1実測 ordered 14.8秒・canonical 16.6秒。決定性: audit.json・両census partとも同一cwd 2回＋
  隔離tree/cwd/HOME+PYTHONHASHSEED=random 1回（census partsは隔離側で再生成）の3実行byte-identical。
  fail-closed: census points改ざん（444,600→444,601）・merge corollary点数改ざん・part欠落の3種を
  すべてFAIL-CLOSED捕捉・正本復元＋フル12チェック再実行でbyte-identical再確認。
  builder再生成物は実行物とbyte一致（出版前に再確認）。
---

# 2トークン残余ゲーム y=14族 全称証明 part1（正本検証器12チェック）

単一オーナー宣言（[宣言ノート](../../log/2026-11-22-y14-universal-verifier-single-owner-note.md)・
commit 24e418a9・2026-11-22T19:08:21Z・part1 12チェック+part2昇格を保持）に基づく
y=14 族全称段階 part1。対象は [K1233](K1233-two-token-y14-parametric-closed-form-fit.md)
（fit・status observed・独立第二検証で同一閉形式の独立二導出が確定済み・「次段階の12チェック全称監査」
を明記）の正本監査段階である。

## 機械構成

verify_y14_universal.py（SHA-256 4ecdec11…）は y13 part1 正本機械（K1232・commit ee3b6f73・
SHA-256 b73d9aaa…）と出版 cand14.py（K1233・commit b6f74dfc・SHA-256 61782b6e…）から
`scripts/build_verify_y14.py`（SHA-256 24246a5d…）で機械組み立てし、count-assert 付き全置換で照合した
（生 2エンジン + K0832 単一トークン表 verbatim〔y11 正本の 77 行 verbatim と y12/y13 出版時に
確定済みの byte〕・cand13 ブロック（B子）はブロック内 Y→Y13 改名のみ〔改名 39 行 count-assert・
改名以外の差 0 行・Y13 = 13 併置で cand14 ブロックの Y = 14 と共存〕・cand14 ブロックは
出版 cand14.py から fit driver と docstring を除き verbatim〔差 0 行〕・生成物の byte は
組み立てscript再生成で一致）。B子 = 出版 cand13（K1231 全称・隣接前族をB子に逐語転写するのは
y11/y12/y13 機械〔B子=cand10/cand11/cand12〕に続き 4 連）。x=14 合流子 (13,14)≡(14,13) の
子値は多重集合として同値で cand13(z,14,R-1)。機械本体の差し替え点は clip 窓 2y+2=30・番兵 31・
census box z=0..79・x=14..70・R<=x+z+15・merge x<=z-15・tail (x+14)%2・C12 深格子 R<=x+z+17。

## 実行結果（overall PASS）

12チェック（C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12）総照合点 6,377,860・全 bad 0。
型機械は clip 窓 2y+2=30・番兵 ±31 で型総数 281,912 の (value, sorted子) 完全収束
（C4時点 248,232 型）。C4t tightness probe で clip 29（2y+1）は 2,480 点の収束違反・
最初 (60,92,92) があるため **clip 2y+2=30 が tight、2y+2 clip tight は 10 族連続
（y=5..14: 12/14/16/18/20/22/24/26/28/30）**。merge corollary（x<=z-15 →
single_token(x+14,z,R)）1,370,848 点・tail corollary（R>=x+z+15 → (x+14) mod 2）
212,713 点、ともに不一致 0。

## C11 census の bounded-memoization twin

census box（z=0..79・x=14..70・R<=x+z+15・444,600 点/エンジン）は、本実行ホストの cgroup
RAM 上限（約1.0 GiB）の下で無制限 memo の生エンジンでは 1 プロセス実行が OOM する
（y12 前身試行で exit 137・行ごと cache-clear 版は 300 秒コマンド上限超過を y12 part1
published_run.txt が実測記録・y=14 は同一ホスト同一制約）。設計は y12/y13 part1 と同一:
出版エンジンの code object を module globals の浅い複写に再束縛し、再帰参照を
LRU 上限 1,600,000 のキャップ付きキャッシュへ張り替えた双生機。engine 別コマンド分割
（C11ordered/C11canonical・run1 実測 14.8秒/16.6秒）とし、C11 モードが両 part を
engine 名・box・cache 上限・幾何からの再計算期待値（444,600/144,534/4,560）・bad==0 で
fail-closed 検証して merge する。part ファイルの 1 点改ざん・corollary 改ざん・欠落の
3 種を出版前に実施し全て捕捉。

## 決定性

audit.json・census-ordered.json・census-canonical.json の 3 ファイルとも、
同一 cwd 2 回＋隔離 tree/cwd/HOME+PYTHONHASHSEED=random 1 回（census parts は隔離側で
再生成）の 3 実行で byte-identical。

## 解釈規約

- K1233 の status は本 part1 出版の時点では **observed** のままだった。昇格判定は part2（C1d 出版固定z切片
  アンカーの y=14 行特殊化 + census_rows.py 第三実装 + 3回 byte-identical）で行い、part2
  （2026-11-22・同一単一オーナー宣言）の出版で **observed→proved に昇格した**
  （K1231/y=13・K1152/y=12 と同一手続き・同一K項目・新規採番なし・フル14チェック監査
  6,965,866 点・全 bad 0・[part2 log](../../log/2026-11-22-y14-parametric-allz-proof-part2.md)）。
  なお現行 main の knowledge.yml に y=11（K1143）・y=12（K1152）・y=13（K1231）実験機の CI step が存在
  しないため（CI 登録は y=10/K1141 まで）、本実験も CI step を登録せず出版 byte を監査正本とする
  （直近 3 族と同一の扱い）。
- 有限照合は有限観察の機械的証拠であって、trust 境界（選択肢分解の健全性・mex 恒等式・
  有限型空間の完全性）は y=5..14 系列と同一の機械分類に依存する。
- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
  **UNKNOWN** のまま。本項は残余ゲーム族 H(R;(x,14);z) の数学的構造の機械検証であり、
  標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=15 族・固定幅・q点版安定化長は範囲外。
