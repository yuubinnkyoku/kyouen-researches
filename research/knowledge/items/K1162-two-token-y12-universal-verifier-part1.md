---
id: K1162
title: "2トークン残余ゲーム y=12族の全称証明 part1: 正本検証器 verify_y12_universal.py 12機械チェック全 PASS（正本監査2段階のpart1・昇格判定はpart2。part2は2026-11-20に実行されK1152のobserved→proved昇格が完了）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier part 1 for the two-token y=12 residual family H(R;(x,12);z): raw-engine anchored 12-check machine, overall PASS with 6,311,993 comparison points and bad 0"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, type machine with clip window 2y+2=26 sentinel 27 and 191,789 types, tightness probe showing clip 25 has 3,540 confluence violations (first (60,88,88)) so 26 is tight (8-family streak y=5..12: 12/14/16/18/20/22/24/26)"
  - "census anchor z=0..79, x=12..70, R<=x+z+13 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (446,040 points each, ~14s, ~550MB) and fail-closed merged in the C11 mode with recomputed expected counts"
  - "merge corollary x<=z-13 implies single_token(x+12,z,R) verified at 1,417,623 points and tail corollary R>=x+z+13 implies (x+12) mod 2 verified at 232,510 points, both with 0 mismatches"
  - "3 byte-identical runs total: audit.json plus both census part files identical across same-cwd reruns and an isolated tree/cwd/HOME run with PYTHONHASHSEED=random; K1152 status remains observed until part2 (C1d published-slice anchors at y=12 plus census_rows.py third implementation)"
  - "part2 executed 2026-11-20 under the same single-owner note: C1d 139,860 pts vs published z=8/9/10/15/16/17 anchors specialised at y=12 (pre-flighted fail-closed, 4-way anchor verification 14,484 pts) and C11r 450,760 pts row-by-row re-derivation of the third-implementation census.txt; full 14-check audit PASS 6,902,613 pts bad 0, 3 byte-identical runs (census regenerated on the isolated side), K1152 promoted observed to proved"
relations:
  - type: extends
    target: "K1152"
    note: "K1152（y=12族 fit・cand12・出版時 observed）の正本監査段階 part1。A子=cand12(z,x-1,R-1)（x=12は合流子(11,12)≡(12,11)でcand11(z,12,R-1)）・B子=出版cand11（K1143）・C子=1 xor cand12(z-1,x,R-1)の12チェック。observed→provedの昇格判定はpart2（C1d・census_rows.py第三実装）で行い、part2は同一単一オーナー宣言の下で2026-11-20に実行・出版済み（K1152はprovedに昇格・フル14チェック監査6,902,613点・全bad 0）"
  - type: depends_on
    target: "K1143"
    note: "正本検証器の機械的母体（生2エンジン・K0832単一トークン表・cand11ブロックの逐語転写元・verify_y11_universal.py SHA-256 c57baf5c...）"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary）"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/README.md
  role: document
  note: "実験README（機械構成・転写照合・12チェック結果表・bounded-memoization twin設計と前身試行のOOM/timeout実験事実・3回決定性・fail-closed 3件・再現コマンド・解釈規約）"
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/verify_y12_universal.py
  role: verifier
  note: "正本検証器。part1出版byte（12チェック版・commit 60622f35・36,170 bytes・SHA-256 f73614f7eb4fe8b0afd0c810d4a72450ee4c65a657ec068c51750d5bc0f5938f・C11ordered/C11canonical/C11モード）とpart2拡張正本（14チェック版・SHA-256 e209297603f68c9a82a50f90cac0bc678211d1517f137b5d490dfca3c492eb04・49,295 bytes・1,287行・C1d/C11r追加・anchor blockはy=10 part2正本検証器 f9169449… から238行verbatim）の2段階。part1の12チェックは挙動不変"
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/output/audit.json
  role: data
  note: "12チェック入り監査正本（3,141 bytes・SHA-256 7dcc4505b270596b7cef7e395761b1741f54edb74b4732efb1d64b1ac78249db・3実行byte-identical）"
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/output/census-ordered.json
  role: data
  note: "C11ordered part正本（486 bytes・446,040点・bad 0・merge 161,700/tail 4,720付帯）"
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/output/census-canonical.json
  role: data
  note: "C11canonical part正本（488 bytes・446,040点・bad 0）"
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/output/published_run.txt
  role: log
  note: "実行記録（転写照合・census前身試行のOOM/timeout・3回決定性・fail-closed・環境）"
- path: research/log/2026-11-20-y12-parametric-allz-proof-part1.md
  role: log
  note: "part1研究log（着手から出版までの記録・採番3点確認）"
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/scripts/preflight_c1d_y12.py
  role: verifier
  note: "part2: C1dアンカー組み込み前fail-closed事前検証（4方照合14,484点+低R縮約9,768点・不一致0・SHA-256 c796478f…・2回byte-identical）"
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/census_rows.py
  role: verifier
  note: "census第三実装（z=0..79・x=12..70・R=0..x+z+14・4,720行450,760点・値0点225,361・misses 6,121,227・LRU上限1.6M明示キャップ・SHA-256 4fee620e…）"
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/output/census.txt
  role: data
  note: "census行表正本（828,655 bytes・SHA-256 67e48cbe…・C11rで全行cand12再導出照合・不一致0）"
- path: research/experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/output/preflight-c1d-y12.json
  role: data
  note: "事前検証結果正本（SHA-256 7562b8dd…）"
- path: research/log/2026-11-20-y12-parametric-allz-proof-part2.md
  role: log
  note: "part2研究log（C1d・census・14チェック監査・K1152 observed→proved昇格・出版記録）"
---

# 2トークン残余ゲーム y=12族 全称証明 part1（正本検証器12チェック）

単一オーナー宣言（[宣言ノート](../../log/2026-11-20-y12-universal-verifier-single-owner-note.md)・
commit d345c645・2026-11-20T17:03:31Z）に基づく y=12 族全称段階 part1。
対象は [K1152](K1152-two-token-y12-parametric-closed-form-fit.md)（fit・status observed・
commit da7f032cf8 出版）の正本監査段階である。

## 機械構成と転写の provenance

verify_y12_universal.py（SHA-256 f73614f7…）は y=11 正本検証器（K1143 part1・
SHA-256 c57baf5c…）と出版 cand12.py（K1152・SHA-256 79e588b3…）から機械組み立てし、
行単位照合で engines+single_token 77 行 verbatim・cand11 ブロック 102 行（Y→Y11 改名のみ・
差 0 行）・cand12 ブロック 92 行 verbatim（差 0 行）を確認した。
B子 = 出版 cand11（全称証明済み族 y=11 をB子に使うのは K1143 の cand10 に続き2例目）、
x=12 合流子 (11,12)≡(12,11) の子値は多重集合として同値で cand11(z,12,R-1)。

## 実行結果（overall PASS）

12チェック（C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12）総照合点 6,311,993・全 bad 0。
型機械は clip 窓 2y+2=26・番兵 ±27 で 191,789 型の (value, sorted子) 完全収束。
C4t tightness probe で clip 25（2y+1）は 3,540 点の収束違反・最初 (60,88,88)があるため
**clip 2y+2=26 が tight、2y+2 clip tight は 8 族連続（y=5..12: 12/14/16/18/20/22/24/26）**。
merge corollary（x<=z-13 → single_token(x+12,z,R)）1,417,623 点・tail corollary
（R>=x+z+13 → (x+12) mod 2）232,510 点、ともに不一致 0。

## C11 census の bounded-memoization twin

census box（z=0..79・x=12..70・R<=x+z+13・446,040 点/エンジン）は、実行ホストの cgroup
RAM 上限（約1.0 GiB）の下で無制限 memo の生エンジンでは 1 プロセス実行が OOM する
（前身試行で exit 137・maxrss 996MB・行ごと cache-clear 版は 300 秒コマンド上限超過を記録）。
そこで出版エンジンの code object を module globals の浅い複写に再束縛し、再帰参照を
LRU 上限 1,600,000 のキャップ付きキャッシュへ張り替えた双生機（bounded-memoization twin）で
再帰定義の byte は正本と同一・決定的純関数の memo 化は透過・LRU 追い出しは固定訪問順の下で
決定的、を構成。engine 別コマンド分割（C11ordered/C11canonical・実測 13-15 秒・
maxrss 約 550-563MB）とし、C11 モードが両 part を engine 名・box・cache 上限・
幾何からの再計算期待値（446,040/161,700/4,720）・bad==0 で fail-closed 検証して merge する。
part ファイルの 1 点改ざん・corollary 改ざん・欠落の 3 種を出版前に実施し全て捕捉。
無制限 verbatim エンジンは C1/C1b/C3 の生アンカーとして残る。

## 決定性

audit.json・census-ordered.json・census-canonical.json の 3 ファイルとも、
同一 cwd 2 回＋隔離 tree/cwd/HOME+PYTHONHASHSEED=random 1 回の 3 実行で byte-identical。

## 採番

part2 push 直前に最新 main で 3 点確認（knowledge README grep `items/K1162-` 0 件・
item path 404・list_commits の K1162 言及 0 件）を実施して取得。K1161 は同一実行の前段で
取得済み（残余23行禁止円構造第三検証）。

## 解釈規約

- K1152 の status は本 part1 出版の時点では **observed** のままだった。昇格判定は part2（C1d 出版固定z切片アンカーの
  y=12 特殊化 + census_rows.py 第三実装 + 3回 byte-identical）で行い、part2（2026-11-20・同一単一オーナー宣言）
  の出版で **observed→proved に昇格した**（K1143/y=11 と同一手続き・同一K項目・新規採番なし・フル14チェック監査
  6,902,613 点・全 bad 0・[part2 log](../../log/2026-11-20-y12-parametric-allz-proof-part2.md)）。
- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて **UNKNOWN** のまま。
  本項は残余ゲーム族 H(R;(x,12);z) の数学的構造の証明であり、標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=13 族・固定幅・q点版安定化長は範囲外。
