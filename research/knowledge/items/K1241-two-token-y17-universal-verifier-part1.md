---
id: K1241
title: "2トークン残余ゲーム y=17族の全称証明: 正本検証器 verify_y17_universal.py part1 12チェック+part2 C1d/C11r の14機械チェック全 PASS（K1240 observed→proved 昇格完了）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier part 1 for the two-token y=17 residual family H(R;(x,17);z): raw-engine anchored 12-check machine, overall PASS with 6,343,825 comparison points and bad 0"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, type machine with clip window 2y+2=36 sentinel 37 and 457,645 types (y=13: 234,180 clip 28 -> y=14: 281,912 clip 30 -> y=15: 335,658 clip 32 -> y=16: 394,686 clip 34 -> y=17: 457,645 clip 36), tightness probe showing clip 35 has 1,300 confluence violations (first (60,98,98)) so 36 is tight (13-family streak y=5..17: 12/14/16/18/20/22/24/26/28/30/32/34/36)"
  - "census anchor z=0..79, x=17..70, R<=x+z+18 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (440,640 points each engine, 54 x-rows per z, ~17 s each) and fail-closed merged in the C11 mode with recomputed expected counts (points 440,640 / merge 119,025 / tail 4,320 per engine)"
  - "merge corollary x<=z-18 implies single_token(x+17,z,R) verified at 1,182,632 points (first full raw-engine anchoring of the y=17 merge region - third consecutive family whose probe box contained zero merge rows; census merge rows first non-empty at z=35 as pre-registered) and tail corollary R>=x+z+18 implies (x+17) mod 2 verified at 193,096 points, both with 0 mismatches"
  - "part2 completed (2026-11-23, same declaration b099a974 + geometry amendment 03ca97ad): preflight_c1d_y17.py 4-way published-slice anchors 12,789 pts + low-R 9,438 pts bad 0 (fail-closed gate before inclusion), census_rows.py third implementation (rows 4,320 / points 444,960 / zero_points 221,578 / misses 8,725,227) consumed by C11r (rows==80*54, values range(0,x+z+20), tail (x+17)%2), full 14-check audit 6,926,065 pts bad 0 (audit.json SHA-256 fd4b7d8c..., verifier part2 SHA-256 4253cf29... in-place extension with part1 12 checks byte-identical), K1240 promoted observed -> proved"
relations:
  - type: extends
    target: "K1240"
    note: "K1240（y=17族 fit・cand17・出版時 observed）の正本監査段階 part1。A子=x==17 なら cand16(z,17,R-1)（合流子 {16,17}≡{17,16} の多重集合同値・x>=18 は cand17(z,x-1,R-1)）・B子=出版 cand16（K1237 全称）・C子=1 xor cand17(z-1,x,R-1) の12チェック。observed→proved の昇格判定は part2（C1d・census_rows.py 第三実装 C11r）で実施し、2026-11-23 に K1240 を proved に昇格した"
  - type: depends_on
    target: "K1237"
    note: "B子の逐語転写元・K1237 の全称証明（y=16族・K1239 part1/part2 機械で observed→proved 昇格済み）。cand16 ブロックは出版 verify_y16_universal.py part2 正本（commit b706b214・SHA-256 bdf4fe04…）からブロック内 Y→Y16 改名（3,298 bytes・改名を除きbyte照合・出版 cand16.py とも二重にbyte一致）。y=17 における使用範囲は x>=17 行で K1237 の定義域 x>=16 の内側"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary）"
  - type: extends
    target: "K1239"
    note: "y=16 全称 part1 機械（K1239）と同型の12チェック構成を y=17 定数へ適合（マージ行 x==17・clip 36・census x=17..70・C7 seed 20261172・C8 の x=16 拡張整合行・tail x+z+18）。機械組み立てscriptは出版せず転写marker+check_transcriptions_y17.py の二重正本方式"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/README.md
  role: document
  note: "実験README（機械構成・転写marker検証・12チェック結果表・bounded-memoization twin設計〔~1.0GiB cgroup host・y=12..16と同一設計〕・3回決定性〔2同一cwd+1隔離tree/cwd/HOME+env -i+PYTHONHASHSEED=random〕・fail-closed 6件〔T1 Y定数1,243 / T2 pin mod4類 28 / T5b 真の合流順序バグ2,209 / T3 census points FAIL-CLOSED / T4 part欠落 FAIL-CLOSED / T5設計初案のbad 0は拡張整合性観察として誠実記録〕・再現コマンド・解釈規約）"
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/verify_y17_universal.py
  role: verifier
  note: "正本検証器（part2正本・51,925 bytes・SHA-256 4253cf29…・14チェック。part1出版byte〔12チェック版・37,970 bytes・SHA-256 2110ecbb…・commit 33e0a062〕の in-place 拡張で C1d/C11r 追加・@@TRANSCRIPTION marker 3ブロック・part1の12チェック本体はbyte不変・y=13..16 part2と同一手続き）"
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/scripts/check_transcriptions_y17.py
  role: verifier
  note: "転写二重正本検証（engine 1,957 bytes・cand16 3,298 bytes 二ソース一致〔出版verify_y16機ブロックと出版cand16.pyの両方とbyte一致〕・cand17 3,379 bytes〔出版cand17.py driver省き〕・構造アンカー抽出・repo root は AGENTS.md 探索・SHA-256 ac40c03c…）"
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/output/audit.json
  role: audit-output
  note: "part2フル14チェック監査正本（SHA-256 fd4b7d8c…・total_points 6,926,065・total_bad 0・型457,645・3実行byte-identical・C1d 137,280=127,842+9,438・C11r 444,960・corollaries merge 1,182,632 / tail 193,096 全bad 0。part1 12チェック正本はSHA-256 301f7690…・total_points 6,343,825・commit 33e0a062）"
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/output/published_run.txt
  role: log
  note: "正典run transcript part2版（転写検査→preflight→census_rows→フル14チェック・rc=0）"
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/output/census-ordered.json
  role: audit-output
  note: "census ordered部（SHA-256 12234496…・440,640点・bad 0・merge 119,025・tail 4,320）"
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/output/census-canonical.json
  role: audit-output
  note: "census canonical部（SHA-256 1ca205a5…・440,640点・bad 0）"
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/output/transcriptions-check-y17.json
  role: audit-output
  note: "転写検査結果（engine/cand16二ソース/cand17 全equal・overall PASS・隔離側でも再実行PASS）"
- path: research/log/2026-11-23-y17-universal-verifier-single-owner-note.md
  role: log
  note: "単一オーナー宣言ノート（commit b099a974・検証器run前に出版・対抗宣言grep clean・事前横断予想〔clip 36 tight・census幾何・型総数4点目〕・K1241仮採番・part1持範囲+part2継続保持の宣言）"
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/census_rows.py
  role: verifier
  note: "census第三実装 y=17版（XMIN=17・XMAX=70・RBUF=19・ZHI=80・token (x,17)・tail (x+17)%2・SHA-256 1188bcd1…・output/census.txt 817,882 bytes 4,320行+空行80・SHA-256 597370b4…・約17.5秒）"
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/scripts/preflight_c1d_y17.py
  role: verifier
  note: "C1d事前検証（出版6切片アンカーの4方照合12,789点+低R縮約9,438点・bad 0・組み込み前fail-closedゲート・SHA-256 fc1d4ec0…・output/preflight-c1d-y17.json SHA-256 c8e0e0a9…・約2.8秒）"
- path: research/log/2026-11-23-y17-universal-verifier-part1.md
  role: log
  note: "part1実行記録（選定・経緯・出版記録・part2への引き継ぎ）"
- path: research/log/2026-11-23-y17-universal-verifier-part2.md
  role: log
  note: "part2実行記録（C1d事前検証・census第三実装・14チェック監査・3回決定性・fail-closed 6種・K1240昇格実施・出版記録）"
scope: >-
  κ=1残余ゲームHの2トークン族X=(x,17)、全z>=0・全x>=17・全R>=0 の全称命題
  （K1240）に対する正本検証のpart1として、実行・出版された12機械チェック
  （C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12・総6,343,825照合点・全bad 0・
  3回実行byte-identical）。part2（C1d事前検証 12,789+9,438点 bad 0・
  census_rows.py第三実装のC11r 444,960点・フル14チェック監査 総6,926,065点
  bad 0・audit SHA-256 fd4b7d8c…・3回byte-identical・fail-closed 6種）を
  同一宣言 b099a974 配下で実施し、K1240 を observed→proved に昇格した
  （2026-11-23）。系のマージ命題y=17版（x<=z-18）とtail
  （R>=x+z+18→(x+17) mod 2）はpart1のcorollary掃引で1,182,632 / 193,096点
  bad 0。標準11×11の空盤・二石root・S2 {59,60}・class 1/2/4は範囲外かつ
  UNKNOWNのまま。3トークン以上・y>=18族・固定幅・q点版も範囲外。
evidence: >-
  2026-11-23出版・単一オーナー宣言 b099a974 配下:
  (1) 転写の二重正本検証: engine/cand16/cand17 の3ブロックが出版bytesと
  byte一致（cand16は出版verify_y16機と出版cand16.pyの2ソースで一致・
  隔離側でもPASS）。
  (2) フル12チェック PASS: 総6,343,825点・bad 0（C1 23,370 / C1b 42,565 /
  C2 221,235 / C2b 19,404 / C3 1,275 / C4 590,634 / C4t 590,634〔probe〕 /
  C7 200,000 / C8 1,014,174 / C9 903,114 / C11 881,280 / C12 1,856,140）。
  (3) clip窓2y+2=36 は tight: C4t で clip 35 が 1,300 違反・最初 (60,98,98)
  で band bottom とともに歩く最初違反の系列（y=13..16: (60,90,90)→(60,98,98)）
  が y=5..17 の13族連続に伸長（宣言の事前予想どおり）。
  (4) census: z=0..79・x=17..70・R<=x+z+18・両エンジン各440,640点 bad 0
  （bounded-memoization twin・LRU 1.6M・~1.0GiB cgroup host・C11mode で
  FAIL-CLOSED 検証の上 merge）。merge帰結領域は宣言どおり z>=35 で初めて非空。
  (5) 決定性: audit/census parts 3実行byte-identical（run3 は隔離
  tree/cwd/HOME+env -i+PYTHONHASHSEED=random・転写検査も隔離側PASS）。
  (6) fail-closed 6件: T1 Y定数改ざん1,243bad / T2 pin mod4類改ざん28bad /
  T5b 真の合流子順序バグ（{16,16}）2,209bad で捕捉、T3 census points改ざん・
  T4 part欠落は FAIL-CLOSED。T5設計初案（cand17(z,16,·)子）は bad 0 で、
  これは同一多重集合 {16,17} の拡張整合性（cand17 x=16 拡張行 ≡ cand16 x=17
  行）の観察として誠実記録（報告書参照）。
  part2（同宣言継続・幾何訂正amendment 03ca97ad〔C2b掃引行x∈{17,22,…,67}〕配下・
  2026-11-23出版）:
  (7) C1d事前検証: 出版6切片アンカー（K0999/K1001/K1011/K1065/K1077/K1087の
  y=17行）をpreflight_c1d_y17.pyで4方照合12,789点+低R縮約9,438点 bad 0
  （組み込み前fail-closedゲート・約2.8秒・preflight-c1d-y17.json c8e0e0a9…）。
  (8) census第三実装: census_rows.py（rows 4,320・points 444,960・
  zero_points 221,578・misses 8,725,227・約17.5秒・census.txt 597370b4…）
  をC11r（rows==80*54機・values range(0,x+z+20)・tail (x+17)%2）として消費。
  (9) フル14チェック監査: total 6,926,065点 bad 0・audit.json SHA-256
  fd4b7d8c…・run1/run2同一cwd+run3隔離（転写検査・preflight・census・両census
  partを隔離側でゼロ再生成）で全出力byte-identical。
  (10) fail-closed 6種全捕捉: census part points改ざん FAIL-CLOSED /
  canonical part欠落 FAIL-CLOSED / census.txt P-set改ざん C11r bad 1 /
  census.txt欠落 FAIL-CLOSED / merge境界 z-18→z-17改ざんでmerge bad 176 /
  重複行注入 FAIL-CLOSED。
  (11) K1240をobserved→provedに昇格（同一単一オーナー宣言のpart1+part2完走）。
  検証器part2正本はpart1出版byteのin-place拡張（4253cf29…）でpart1の
  12チェック本体はbyte不変・拡張部はy16 part2正本からverbatimのanchor block。
---

## 12チェックの構成と実績値（part1）

y=16 機（K1239）と同一構成の12チェックを y=17 定数へ適合:
A子は x==17 の合流子 {16,17}≡{17,16} で cand16(z,17,R-1)、
B子は出版 cand16（K1237 全称・x>=17 行は定義域内側）、
C子は 1 xor cand17(z-1,x,R-1)、型機械 clip 2y+2=36・番兵 37、
census z=0..79・x=17..70（80*54=4,320行）・R<=x+z+18、
C7 seed 20261172、C8 の x=16 行は拡張整合行としてのみ。

**実績値: overall PASS・総6,343,825照合点・全bad 0・型457,645**
（clip 36 での型空間・系列5点目:
y=13: 234,180 → y=14: 281,912 → y=15: 335,658 → y=16: 394,686 →
y=17: 457,645）。

## C4t tight と最初違反の歩み（13族連続）

clip 35（2y+1）で 1,300 型収束違反・最初違反 (60,98,98)。最初違反は
band bottom とともに步む系列（60,90,90)→(60,92,92)→(60,94,94)→(60,96,96)→
(60,98,98)）どおりで、**clip窓 2y+2 tight 判定は13族連続（y=5..17:
12/14/.../34/36）**に伸長した（宣言の事前横断予想どおり・違反ゼロなら再審
と宣言していたところ違反>0でtight確定）。

## 誠実記録（T5 初案の拡張整合性観察）

fail-closed 電池の T5 初案（合流子を cand17(z,16,R-1) に置換）は bad 0
で「不補足」となった。これは機械の欠陥ではなく、y=17 閉形式の x=16 拡張行
と y=16 族の x=17 行が同一多重集合 {16,17} を記述していること（S=33 が同一
で merge/tail/pin 則が1族分ずれるだけ）による拡張整合性であり、C8 の
x=16 拡張整合行が依存する性質そのものである。真の合流順序バグ
（x=16 行・多重集合 {16,16}）で 2,209 bad を捕捉し、観察は実験READMEに
正本記録した。

## part2 の実施と昇格（2026-11-23 完了）

part2（C1d 出版固定z切片アンカーの y=17 行〔preflight fail-closed〕
+ census_rows.py 第三実装 y=17 版（XMIN=17・XMAX=70・RBUF=19・ZHI=80）
の C11r）を同一単一オーナー宣言 b099a974 配下（幾何訂正 amendment
03ca97ad 含む）で実施した:

- C1d 事前検証: 4方照合 12,789 点 + 低 R 縮約 9,438 点・bad 0
  （preflight_c1d_y17.py・組み込み前 fail-closed ゲート）。
- C11r: census_rows.py 4,320 行 444,960 点（zero_points 221,578・
  misses 8,725,227）を消費し rows==80*54・values range(0,x+z+20)・
  tail (x+17)%2 を機械検証。
- フル14チェック監査: 総 6,926,065 点 bad 0（audit.json SHA-256
  fd4b7d8c…・C1d 137,280=掃引127,842+preflight 9,438・C11r 444,960・
  3実行 byte-identical〔run3 は隔離・census/preflight/転写検査は隔離側で
  ゼロ再生成〕・fail-closed 6種全捕捉）。
- **K1240 を observed→proved に昇格**。trust境界（選択肢分解の健全性・
  mex恒等式・有限型空間）は y=1..16 系列と同一の機械分類に依存し、
  大域安定化長の引用は 14 チェック監査合格後に解禁した。
