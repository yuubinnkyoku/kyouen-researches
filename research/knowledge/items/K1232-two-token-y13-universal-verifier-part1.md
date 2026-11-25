---
id: K1232
title: "2トークン残余ゲーム y=13族の全称証明 part1: 正本検証器 verify_y13_universal.py 12機械チェック全 PASS（正本監査2段階のpart1・昇格判定はpart2。part2は2026-11-22に実行されK1231のobserved→proved昇格が完了）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier part 1 for the two-token y=13 residual family H(R;(x,13);z): raw-engine anchored 12-check machine, overall PASS with 6,353,143 comparison points and bad 0"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, type machine with clip window 2y+2=28 sentinel 29 and 234,180 types, tightness probe showing clip 27 has 2,987 confluence violations (first (60,90,90)) so 28 is tight (9-family streak y=5..13: 12/14/16/18/20/22/24/26/28)"
  - "census anchor z=0..79, x=13..70, R<=x+z+14 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (445,440 points each, 13-16s, ~549-562MB) and fail-closed merged in the C11 mode with recomputed expected counts (points 445,440 / merge 153,117 / tail 4,640 per engine)"
  - "merge corollary x<=z-14 implies single_token(x+13,z,R) verified at 1,391,747 points and tail corollary R>=x+z+14 implies (x+13) mod 2 verified at 217,342 points, both with 0 mismatches"
  - "3 byte-identical runs total: audit.json plus both census part files identical across same-cwd reruns and an isolated tree/cwd/HOME run with PYTHONHASHSEED=random; K1231 status remains observed until part2 (C1d published-slice anchors at y=13 plus census_rows.py third implementation)"
  - "part2 executed 2026-11-22 under the same single-owner note: C1d 139,356 pts vs published z=8/9/10/15/16/17 anchors specialised at y=13 (pre-flighted fail-closed, 4-way anchor verification 14,157 pts + low-R reduction 9,702 pts) and C11r 450,080 pts row-by-row re-derivation of the third-implementation census.txt (4,640 rows, z=0..79, x=13..70, R=0..x+z+15); full 14-check audit PASS 6,942,579 pts bad 0, 3 byte-identical runs (census and preflight regenerated on the isolated side), K1231 promoted observed to proved"
relations:
  - type: extends
    target: "K1231"
    note: "K1231（y=13族 fit・cand13・出版時 observed）の正本監査段階 part1。A子=cand13(z,x-1,R-1)（x=13は合流子(12,13)≡(13,12)でcand12(z,13,R-1)）・B子=出版cand12（K1152全称）・C子=1 xor cand13(z-1,x,R-1)の12チェック。observed→provedの昇格判定はpart2（C1d・census_rows.py第三実装）で行い、part2は同一単一オーナー宣言の下で2026-11-22に実行・出版済み（K1231はprovedに昇格・フル14チェック監査6,942,579点・全bad 0）"
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
  note: "正本検証器。part1出版byte（12チェック版・commit ee3b6f73・36,457 bytes・SHA-256 b73d9aaa94f04f1f4922d84808ac7afe6f5bfb55631b4c990cae29734279141f・937行・C11ordered/C11canonical/C11モード・機械組み立てscriptの再生成物とbyte一致）とpart2拡張正本（14チェック版・SHA-256 079b49ad5d11c22c7c6c5f8d103eff9ee2194c7d587e7f2432172616c03c1114・50,865 bytes・1,314行・C1d/C11r追加・anchor blockはy=12 part2正本検証器 e2092976… からverbatim抽出）の2段階。part1の12チェックは挙動不変"
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/output/audit.json
  role: data
  note: "part2フル14チェック入り監査正本（3,673 bytes・SHA-256 2f5f56c0da4578252db8bf12d536764562ded134e5bad45ca832c58b17424bb1d・total_points 6,942,579・total_bad 0・3実行byte-identical。part1出版時は12チェック版 db7c5fa5… 3,103 bytes）"
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
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/scripts/preflight_c1d_y13.py
  role: verifier
  note: "part2: C1dアンカー組み込み前fail-closed事前検証（4方照合14,157点+低R縮約9,702点・不一致0・2回byte-identical）"
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/census_rows.py
  role: verifier
  note: "census第三実装（z=0..79・x=13..70・R=0..x+z+15・4,640行450,080点・値0点224,203・misses 6,630,827・LRU上限1.6M明示キャップ・SHA-256 85bafd2e…）"
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/output/census.txt
  role: data
  note: "census行表正本（829,622 bytes・SHA-256 505f05bf…・C11rで全行cand13再導出照合・不一致0）"
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/output/preflight-c1d-y13.json
  role: data
  note: "事前検証結果正本（SHA-256 a9307d33…）"
- path: research/log/2026-11-22-y13-parametric-allz-proof-part2.md
  role: log
  note: "part2研究log（C1d・census・14チェック監査・K1231 observed→proved昇格・出版記録・CI step不登録の理由）"
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

- K1231 の status は本 part1 出版の時点では **observed** のままだった。昇格判定は part2（C1d 出版固定z切片アンカーの
  y=13 特殊化 + census_rows.py 第三実装 + 3回 byte-identical）で行い、part2（2026-11-22・同一単一オーナー宣言）
  の出版で **observed→proved に昇格した**（K1152/y=12 と同一手続き・同一K項目・新規採番なし・フル14チェック監査
  6,942,579 点・全 bad 0・[part2 log](../../log/2026-11-22-y13-parametric-allz-proof-part2.md)）。
  なお現行 main の knowledge.yml に y=11（K1143）・y=12（K1152）実験機の CI step が存在しないため
  （CI 登録は y=10/K1141 まで）、本実験も CI step を登録せず出版 byte を監査正本とする（直近 2 族と同一の扱い）。
- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて **UNKNOWN** のまま。
  本項は残余ゲーム族 H(R;(x,13);z) の数学的構造の証明であり、標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=14 族・固定幅・q点版安定化長は範囲外。
