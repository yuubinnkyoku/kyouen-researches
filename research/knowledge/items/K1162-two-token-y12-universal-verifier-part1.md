---
id: K1162
title: "2トークン残余ゲーム y=12族の全称証明 part1: 正本検証器 verify_y12_universal.py 12機械チェック全 PASS（K1152 fit の正本監査段階・昇格判定は part2 まで行わない）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier part 1 for the two-token y=12 residual family H(R;(x,12);z): raw-engine anchored 12-check machine, overall PASS with 6,311,993 comparison points and bad 0"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, type machine with clip window 2y+2=26 sentinel 27 and 191,789 types, tightness probe showing clip 25 has 3,540 confluence violations (first (60,88,88)) so 26 is tight (8-family streak y=5..12: 12/14/16/18/20/22/24/26)"
  - "census anchor z=0..79, x=12..70, R<=x+z+13 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (446,040 points each, ~14s, ~550MB) and fail-closed merged in the C11 mode with recomputed expected counts"
  - "merge corollary x<=z-13 implies single_token(x+12,z,R) verified at 1,417,623 points and tail corollary R>=x+z+13 implies (x+12) mod 2 verified at 232,510 points, both with 0 mismatches"
  - "3 byte-identical runs total: audit.json plus both census part files identical across same-cwd reruns and an isolated tree/cwd/HOME run with PYTHONHASHSEED=random; K1152 status remains observed until part2 (C1d published-slice anchors at y=12 plus census_rows.py third implementation)"
relations:
  - type: extends
    target: "K1152"
    note: "K1152（y=12族 fit・cand12・observed）の正本監査段階 part1。A子=cand12(z,x-1,R-1)（x=12は合流子(11,12)≡(12,11)でcand11(z,12,R-1)）・B子=出版cand11（K1143）・C子=1 xor cand12(z-1,x,R-1)の12チェック。observed→provedの昇格判定はpart2（C1d・census_rows.py第三実装）で行う"
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
  note: "正本検証器（36,170 bytes・SHA-256 f73614f7eb4fe8b0afd0c810d4a72450ee4c65a657ec068c51750d5bc0f5938f・純stdlib・seed固定・sorted keys・C11ordered/C11canonical/C11モード）"
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

- K1152 の status は本出版後も **observed**。昇格判定は part2（C1d 出版固定z切片アンカーの
  y=12 特殊化 + census_rows.py 第三実装 + 3回 byte-identical）で行い、K1143（y=11）と同一手続き。
- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて **UNKNOWN** のまま。
  本項は残余ゲーム族 H(R;(x,12);z) の数学的構造の証明であり、標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=13 族・固定幅・q点版安定化長は範囲外。
