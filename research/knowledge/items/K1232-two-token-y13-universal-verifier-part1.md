---
id: K1232
title: "2トークン残余ゲーム y=13族の全称証明 part1: 正本検証器 verify_y13_universal.py 12機械チェック全 PASS（正本監査2段階のpart1・昇格判定はpart2）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier part 1 for the two-token y=13 residual family H(R;(x,13);z): raw-engine anchored 12-check machine, overall PASS with 6,353,143 comparison points and bad 0"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, type machine with clip window 2y+2=28 sentinel 29 and 234,180 types, tightness probe showing clip 27 has 2,987 confluence violations (first (60,90,90)) so 28 is tight (9-family streak y=5..13: 12/14/16/18/20/22/24/26/28)"
  - "census anchor z=0..79, x=13..70, R<=x+z+14 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (445,440 points each, 13-16s, ~549-562MB) and fail-closed merged in the C11 mode with recomputed expected counts (points 445,440 / merge 153,117 / tail 4,640 per engine)"
  - "merge corollary x<=z-14 implies single_token(x+13,z,R) verified at 1,391,747 points and tail corollary R>=x+z+14 implies (x+13) mod 2 verified at 217,342 points, both with 0 mismatches"
  - "3 byte-identical runs total: audit.json plus both census part files identical across same-cwd reruns and an isolated tree/cwd/HOME run with PYTHONHASHSEED=random; K1231 status remains observed until part2 (C1d published-slice anchors at y=13 plus census_rows.py third implementation)"
relations:
  - type: extends
    target: "K1231"
    note: "K1231（y=13族 fit・cand13・出版時 observed）の正本監査段階 part1。A子=cand13(z,x-1,R-1)（x=13は合流子(12,13)≡(13,12)でcand12(z,13,R-1)）・B子=出版cand12（K1152全称）・C子=1 xor cand13(z-1,x,R-1)の12チェック。observed→provedの昇格判定はpart2（C1d・census_rows.py第三実装）で行う"
  - type: depends_on
    target: "K1152"
    note: "B子の逐語転写元（y=12族全称・出版 verify_y12_universal.py の cand12 ブロックをブロック内 Y→Y12 改名のみで転写）と機械的母体（y=12 part2 正本機械・SHA-256 e2092976...）"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary）"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/README.md
  role: document
  note: "実験README（機械構成・転写照合・12チェック結果表・bounded-memoization twin設計〔y12 part1と同一設計〕・3回決定性・fail-closed 3件・再現コマンド・解釈規約）"
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/verify_y13_universal.py
  role: verifier
  note: "正本検証器（12チェック版・36,457 bytes・937行・SHA-256 b73d9aaa94f04f1f4922d84808ac7afe6f5bfb55631b4c990cae29734279141f・C11ordered/C11canonical/C11モード・機械組み立てscriptの再生成物とbyte一致）"
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/output/audit.json
  role: data
  note: "12チェック入り監査正本（3,103 bytes・SHA-256 db7c5fa56f407f09ed6604d7677aaab681d78649dc85379d977c5bd58c8e42de・3実行byte-identical）"
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/output/census-ordered.json
  role: data
  note: "C11ordered part正本（486 bytes・445,440点・bad 0・merge 153,117/tail 4,640付帯）"
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/output/census-canonical.json
  role: data
  note: "C11canonical part正本（488 bytes・445,440点・bad 0）"
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/output/published_run.txt
  role: log
  note: "実行記録（機械構成・転写照合・実行・3回決定性・fail-closed・環境）"
- path: research/log/2026-11-22-y13-parametric-allz-proof-part1.md
  role: log
  note: "part1研究log（着手・宣言・機械構成・実行・出版系列・採番3点確認）"
---

# 2トークン残余ゲーム y=13族 全称証明 part1（正本検証器12チェック）

単一オーナー宣言（[宣言ノート](../../log/2026-11-22-y13-universal-verifier-single-owner-note.md)・
commit 7196cbd570c638ffbdcf8edfb17ccd8b6df8ead3・2026-11-22T17:59:40Z・part1+part2保持）に基づく
y=13 族全称段階 part1。対象は [K1231](K1231-two-token-y13-parametric-closed-form-fit.md)
（fit・status observed・commit 時点で12チェック全称監査を「次段階」と明記）の正本監査段階である。

## 機械構成と転写の provenance

verify_y13_universal.py（SHA-256 b73d9aaa…）は y=12 part2 正本機械（K1152/K1162・
SHA-256 e2092976…）と出版 cand13.py（K1231・SHA-256 cb903c56…）から機械組み立てし、
count-assert 付き全置換で照合した（engines+single_token verbatim〔y12 part1 出版時に y11 正本の
77 行 verbatim と確定済みの byte〕・cand12 ブロックのブロック内 Y→Y12 改名のみ〔改名行数
count-assert・差 0 行〕・cand13 ブロック verbatim〔docstring/fit driver 除去・差 0 行〕・
生成物の ast.parse・機械組み立てスクリプトの再生成物が実行物と byte 一致）。
B子 = 出版 cand12（全称証明済み族 y=12 をB子に逐語転写するのは y11 機械の cand10・y12 機械の
cand11 に続き 3 例目）、x=13 合流子 (12,13)≡(13,12) の子値は多重集合として同値で cand12(z,13,R-1)。
機械本体の差し替え点は clip 窓 2y+2=28・番兵 29・census box x=13..70/R<=x+z+14・merge x<=z-14・
tail (x+13)%2・y12 part2 版から C1d/C11r 系除去（part1 は 12 チェック構成）。

## 実行結果（overall PASS）

12チェック（C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12）総照合点 6,353,143・全 bad 0。
型機械は clip 窓 2y+2=28・番兵 ±29 で型総数 234,180 の (value, sorted子) 完全収束。
C4t tightness probe で clip 27（2y+1）は 2,987 点の収束違反・最初 (60,90,90) があるため
**clip 2y+2=28 が tight、2y+2 clip tight は 9 族連続（y=5..13: 12/14/16/18/20/22/24/26/28）**。
merge corollary（x<=z-14 → single_token(x+13,z,R)）1,391,747 点・tail corollary
（R>=x+z+14 → (x+13) mod 2）217,342 点、ともに不一致 0。

## C11 census の bounded-memoization twin

census box（z=0..79・x=13..70・R<=x+z+14・445,440 点/エンジン）は、本実行ホストの cgroup
RAM 上限（約1.0 GiB）の下で無制限 memo の生エンジンでは 1 プロセス実行が OOM する
（y12 前身試行で exit 137・maxrss 996MB・行ごと cache-clear 版は 300 秒コマンド上限超過を
y12 part1 published_run.txt が実測記録・y=13 は同一ホスト同一制約）。設計は y12 part1 と同一:
出版エンジンの code object を module globals の浅い複写に再束縛し、再帰参照を
LRU 上限 1,600,000 のキャップ付きキャッシュへ張り替えた双生機（再帰定義の byte は正本と同一・
決定的純関数の memo 化は透過・LRU 追い出しは固定訪問順の下で決定的）。
engine 別コマンド分割（C11ordered/C11canonical・実測 13.3-16.4 秒・maxrss 約 549-562MB）とし、
C11 モードが両 part を engine 名・box・cache 上限・幾何からの再計算期待値
（445,440/153,117/4,640）・bad==0 で fail-closed 検証して merge する。
part ファイルの 1 点改ざん・corollary 改ざん・欠落の 3 種を出版前に実施し全て捕捉。
無制限 verbatim エンジンは C1/C1b/C3/C2/C2b/C8 の生アンカーとして残る。

## 決定性

audit.json・census-ordered.json・census-canonical.json の 3 ファイルとも、
同一 cwd 2 回＋隔離 tree/cwd/HOME+PYTHONHASHSEED=random 1 回の 3 実行で byte-identical。

## 採番

part1 push 直前に最新 main で 3 点確認（knowledge README grep `K1232` 0 件〔2026-11-22・HEAD
175864a5 時点でREADME言及なし〕・item path 404・list_commits 30 件に K1232 言及 0 件）を実施して取得。

## 解釈規約

- K1231 の status は本 part1 出版後も **observed** のまま。昇格判定（observed→proved）は part2
  （C1d 出版固定z切片アンカーの y=13 特殊化 + census_rows.py 第三実装 + 3回 byte-identical）で行う
  （K1141/K1143/K1152/K1162 の前例と同一手続き・同一K項目・新規採番なし）。
- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて **UNKNOWN** のまま。
  本項は残余ゲーム族 H(R;(x,13);z) の数学的構造の証明であり、標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=14 族・固定幅・q点版安定化長は範囲外。
