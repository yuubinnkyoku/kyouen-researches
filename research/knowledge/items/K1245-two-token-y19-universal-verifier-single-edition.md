---
id: K1245
title: "2トークン残余ゲーム y=19族の全称検証: 正本検証器 verify_y19_universal.py 単一機体14チェック全 PASS（K1243 を observed→proved へ昇格）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier for the two-token y=19 residual family H(R;(x,19);z), single-edition 14-check machine: overall PASS with 6,941,913 comparison points and bad 0, promoting K1243 observed -> proved"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, C1d published-slice anchors pre-flighted fail-closed 4-way (12,069+9,306 pts bad 0), type machine with clip window 2y+2=40 sentinel 41 and 590,877 types (series: y=14: 281,912 -> y=15: 335,658 -> y=16: 394,686 -> y=17: 457,645 -> y=18: 523,398 -> y=19: 590,877), tightness probe showing clip 39 has 770 confluence violations (first (60,102,102)) so 40 is tight (15-family streak y=5..19: 12/14/16/18/20/22/24/26/28/30/32/34/36/38/40)"
  - "census anchor z=0..79, x=19..70, R<=x+z+20 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (436,800 points each engine, 52 x-rows per z, ~19-22 s each) and fail-closed merged in the C11 mode with recomputed expected counts (points 436,800 / merge 102,459 / tail 4,160 per engine); independent census ledger consumer C11r over census_rows.py's census.txt (4,160 rows, 440,960 points) bad 0"
  - "merge corollary x<=z-20 implies single_token(x+19,z,R) verified at 1,062,109 points (census merge rows first non-empty at z=39, 5th consecutive family whose probe box contained zero merge rows) and tail corollary R>=x+z+20 implies (x+19) mod 2 verified at 192,520 points, both with 0 mismatches; staged 12-check battery kept as a separate audit (5,627,353 pts bad 0, audit-part1-12checks.json)"
  - "single-edition variant pre-registered in declaration da6c1f5f: the machine is built in full 14-check form from the start (part1-style 12 checks + C1d anchors + C11r census consumer) and executed in stages; every declaration pre-computation (predict_y19_counts.py, loop-geometry only, cross-validated against the published y=18 audit 14/14) matched the machine measurements exactly, no amendment needed"
relations:
  - type: extends
    target: "K1243"
    note: "K1243（y=19族 fit・cand19・出版時 observed）の正本監査段階。A子=x==19 なら cand18(z,19,R-1)（合流子 {18,19}≡{19,18} の多重集合同値・x>=20 は cand19(z,x-1,R-1)・y=14 合流事故の知見を y=18 機と同型に適用）・B子=出版 cand18（K1242 全称・K1244 機で proved 昇格済み）・C子=1 xor cand19(z-1,x,R-1) の14チェック。overall PASS + 4回 byte-identical + fail-closed 12種全捕捉で K1243 を observed→proved に昇格した"
  - type: depends_on
    target: "K1242"
    note: "B子の逐語転写元・K1242 の全称証明（y=18族）。cand18 ブロック（3,307 bytes）は出版 verify_y18_universal.py part2（commit d29acbd8・SHA-256 8ddd0c2f…）の cand18 ブロックからブロック内 Y→Y18 改名（改名を除きbyte照合・出版 cand18.py〔K1242 fit・commit 9e898f45〕とも二重にbyte一致・両ソース byte一致）。y=19 における使用範囲は B子 x>=19 行と A子 x=19 合流で K1242 の定義域 x>=18 の内側"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary・low-R reduction）"
  - type: extends
    target: "K1241"
    note: "y=17 全称 part1/part2 機械（K1241）と同型のチェック構成を y=19 定数へ適合（マージ行 x==19・clip 40・census x=19..70=52行・C7 seed 20261192・C8 の x=18 拡張整合行・tail x+z+20・C1d アンカーは出版y18機のanchor block逐語）。機械組み立てscriptは出版せず転写marker+check_transcriptions_y19.py の二重正本方式（y=13..y=18 手続き）"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/README.md
  role: document
  note: "実験README（単一機体14チェック版の機械構成・転写marker検証・段階実行結果表・C4t tight（15族連続・7観測目の歩み）・決定性4実行〔2同一cwd+2隔離、うち1回は全pipeline完全ゼロ再生成〕・fail-closed 12種全捕捉・宣言予想と実測の完全一致の記録〔amendment不用〕・再現コマンド・昇格判定・解釈規約）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/verify_y19_universal.py
  role: verifier
  note: "正本検証器（単一機体14チェック版・52,631 bytes・SHA-256 76525717…・@@TRANSCRIPTION marker 3ブロック〔engine 1,957 bytes・cand18 3,307 bytes二ソース・cand19 3,411 bytes〕・C1dアンカー前のpreflight fail-closedゲート設計）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/scripts/check_transcriptions_y19.py
  role: verifier
  note: "転写二重正本検証（engine 出版y18機part2から逐語・cand18 出版y18機ブロックと出版cand18.pyの両方とY→Y18改名差分のみで一致・sources_agree・cand19 出版cand19.py逐語・構造アンカー抽出・repo root は AGENTS.md 探索・SHA-256 56a999bd…）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/scripts/preflight_c1d_y19.py
  role: verifier
  note: "C1d事前検証（SHA-256 9bc154ee…・出版6切片アンカー4方照合12,069点+低R単一トークン縮約9,306点・bad 0・anchor block は出版y18 preflightからbyte-verbatim・JSON SHA-256 1cfabdcf…）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/census_rows.py
  role: verifier
  note: "census第三実装（SHA-256 e4eed396…・XMIN=19・XMAX=70・RBUF=21・ZHI=80・LRU cap 1,600,000・440,960点・zero_points 219,556・misses 9,806,027・約21秒・census.txt 4,160行を生成）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/audit.json
  role: audit-output
  note: "フル14チェック監査正本（SHA-256 59b6fded…・total_points 6,941,913・total_bad 0・type_count 590,877・4実行byte-identical〔2同一cwd+2隔離〕・corollaries merge 1,062,109 / tail 192,520 全bad 0・stageはsingle-edition 14-check machine）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/audit-part1-12checks.json
  role: audit-output
  note: "段階実行12チェック電池の監査退避正本（SHA-256 63617241…・total_points 5,627,353・total_bad 0・宣言の段階実行プロトコルの記録・型590,877）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/census.txt
  role: data
  note: "census行台帳正本（809,842 bytes・SHA-256 07213ab1…・C11rが全行をcand19から再導出し440,960点bad 0）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/census-ordered.json
  role: audit-output
  note: "census ordered部（SHA-256 df767357…・436,800点・bad 0・merge 102,459・tail 4,160）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/census-canonical.json
  role: audit-output
  note: "census canonical部（SHA-256 afdf9e60…・436,800点・bad 0・merge 102,459・tail 4,160）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/preflight-c1d-y19.json
  role: audit-output
  note: "C1d preflight結果正本（SHA-256 1cfabdcf…・12,069+9,306点bad 0・per z 1,890/1,917/1,944/2,079/2,106/2,133）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/transcriptions-check-y19.json
  role: audit-output
  note: "転写検査結果（engine/cand18二ソース/cand19 全equal・overall PASS・隔離側でも再実行PASS・SHA-256 8a68ecb4…）"
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/published_run.txt
  role: log
  note: "正典run transcript（段階実行の全記録〔転写検査→preflight→census→12チェック→14チェック〕・rc=0・4回決定性・fail-closed 12種・宣言の事前予想と全照合点数の一致）"
- path: research/log/2026-11-23-y19-universal-verifier-single-owner-note.md
  role: log
  note: "単一オーナー宣言ノート（commit da6c1f5f・検証器run前に出版・観測HEAD 6f5419b5・対抗宣言なしの確認記録・単一機体14チェック版の事前登録〔part1/part2の一体化変形〕・事前横断予想の機械算出〔predict_y19_counts.py・出版y18 audit 14/14でcross-validated・clip 40 tight・最初違反(60,102,102)予想〕・K1245仮採番）"
- path: research/log/2026-11-23-two-token-y19-universal-verifier.md
  role: log
  note: "全称段階の実行記録（選定・機体ビルド・段階実行・宣言予想との完全一致・決定性・fail-closed 12種・K1243昇格判定・出版記録・次のレジューム）"
scope: >-
  κ=1残余ゲームHの2トークン族X=(x,19)、全z>=0・全x>=19・全R>=0 の全称命題
  （K1243）に対する正本検証として、実行・出版された単一機体14チェック
  （C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12・総6,941,913照合点・
  全bad 0・4回実行byte-identical〔うち1回は隔離側での完全ゼロ再生成〕・
  fail-closed 12種全捕捉）。宣言で事前登録された単一機体版変形: part1相当
  12チェック電池の監査もaudit-part1-12checks.json（総5,627,353点・bad 0）
  として別正本で保存。本監査のoverall PASSによりK1243はobserved→provedに
  昇格（昇格はK1243側に記録）。系のマージ命題y=19版（x<=z-20）とtail
  （R>=x+z+20→(x+19) mod 2）はcorollary掃引で1,062,109 / 192,520点 bad 0
  でマージ命題はy=1..19で全称確定。標準11×11の空盤・二石root・
  S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNのまま。
  3トークン以上・y>=20族・固定幅・q点版も範囲外。
evidence: >-
  2026-11-23出版・単一オーナー宣言 da6c1f5f 配下:
  (1) 転写の二重正本検証: engine/cand18/cand19 の3ブロックが出版bytesと
  byte一致（cand18は出版y18機part2ブロックと出版cand18.pyの2ソースで
  一致・sources_agree・隔離側でもPASS）。
  (2) 段階実行12チェック PASS: 総5,627,353点・bad 0（C1 24,510 / C1b 44,027 /
  C1d 136,206 / C2 229,663 / C2b 19,580 / C3 1,335 / C4 579,657 /
  C4t 579,657〔probe〕 / C7 200,000 / C8 1,057,317 / C9 897,930 /
  C12 1,857,471）・audit-part1-12checks.jsonに退避。
  (3) フル14チェック PASS: 総6,941,913点・bad 0・型590,877
  （12チェック小計 6,364,747 + C1d 136,206 + C11r 440,960・C11 873,600は
  両engine 436,800×2をC11 modeでfail-closed検証の上merge）。
  宣言noteの事前機械算出（predict_y19_counts.py・loop幾何のみ）と全照合
  点数で完全一致（同関数が出版y18 auditの14点数を完全一致で再現することを
  宣言時にcross-validate済み・amendment不用）。
  (4) clip窓2y+2=40 は tight: C4tで clip 39 が 770違反・最初 (60,102,102)
  で band bottom とともに歩く最初違反の系列が7観測目
  （y=13..18の6観測に (60,102,102) を追加・y=5..19の15族tight連続確定）
  （宣言の事前横断予想〔違反>0・最初違反(60,102,102)〕と完全一致）。
  (5) census: z=0..79・x=19..70・R<=x+z+20・両エンジン各436,800点 bad 0
  （bounded-memoization twin・LRU 1.6M・~1.0GiB cgroup host・分離コマンド
  C11ordered/C11canonical・C11 modeでFAIL-CLOSED検証の上 merge）。
  merge帰結は宣言どおり z>=39 で初めて非空（merge 102,459/engine）。
  C11rはcensus_rows.py（第三実装・4,160行・440,960点・zero_points
  219,556・misses 9,806,027）の台帳をcand19から行単位再導出してbad 0
  （rows==80*52=4,160の斉一性はFAIL-CLOSED）。
  (6) C1d: 出版固定z切片アンカー（z0∈{8,9,10,15,16,17}・出版y18 preflight
  からanchor block逐語）をpreflight（4方照合12,069点+低R縮約9,306点
  bad 0・組み込み前fail-closedゲート）を経て機内掃引 x=19..159・R<=x+61
  は136,206点 bad 0（anchor掃引126,900+lowR 9,306）。
  (7) 決定性: audit/census台帳/census部品/preflight/転写検査出力 4実行
  byte-identical（run1/run2同一cwd・run3/run4隔離tree/cwd/HOME+env -i+
  PYTHONHASHSEED=random・run3は全pipeline（転写検査・preflight・
  census_rows・census両部・フル14チェック）をゼロ再生成）。
  (8) fail-closed 12種全捕捉: census.txt欠落/行削除/重複行のFAIL-CLOSED・
  P-set/T-set改ざん→C11r bad 1・C11r tail反転→bad 4,160（全行・宣言
  予想どおりrows数）・アンカー誤結合→C1d bad 1,743・lowR参照ずれR+1
  →bad 9,306（全lowR点が独立に識別）・merge境界 z-20→z-19→merge bad>0・
  clip窓 40,41→38,39→C4 bad 2,520・in_P19 tail偶奇反転→C1 bad 2,449・
  band_base偶奇改ざん→C1 bad 935（12種すべてrc=1・スクラッチtreeで実施・
  各probe後にbaselineをbuild bytesとcmp検証し復元・正典treeは無傷）。
---

## 14チェックの構成と実績値（単一機体版）

y=18 機（K1244）と同一構成のチェック群を y=19 定数へ適合:
A子は x==19 の合流子 {18,19}≡{19,18} で cand18(z,19,R-1)、
B子は出版 cand18（K1242 全称・x>=19 行は定義域内側）、
C子は 1 xor cand19(z-1,x,R-1)、型機械 clip 2y+2=40・番兵 41、
census z=0..79・x=19..70（80*52=4,160行）・R<=x+z+20、
C7 seed 20261192、C8 の x=18 行は拡張整合行としてのみ。

**実績値: overall PASS・総6,941,913照合点・全bad 0・型590,877**
（系列: y=14 281,912 → y=15 335,658 → y=16 394,686 → y=17 457,645 →
y=18 523,398 → y=19 590,877）。段階実行12チェック電池（part1相当）の
監査は audit-part1-12checks.json（総5,627,353点・bad 0）としても保存。

## C4t tight と最初違反の歩み（15族連続）

clip 39（2y+1）で 770 型収束違反・最初違反 (60,102,102)。最初違反は
band bottom とともに歩む系列
（(60,90,90)→(60,92,92)→(60,94,94)→(60,96,96)→(60,98,98)→(60,100,100)
→(60,102,102)）7観測目で、**clip窓 2y+2 tight 判定は15族連続（y=5..19:
12/14/…/38/40）**に伸長した（宣言の事前横断予想〔違反>0・(60,102,102)〕
と完全一致）。

## 宣言予想との完全一致（amendment 不用）

宣言note（da6c1f5f）は全14チェックの照合点数・preflight box（12,069+9,306）・
census幾何（4,160行・436,800/engine・merge 102,459・tail 4,160）・C11r
440,960・12チェック小計 6,364,747・総点 6,941,913・C4t違反（>0・最初違反
(60,102,102)）・C11r tail反転probe 4,160 を predict_y19_counts.py
（ループ幾何のみの算術関数・ゲーム評価なし）で事前機械算出し、
同一関数が出版y18 part2 auditの全点数（6,934,616・14点数）を完全一致で
再現することを宣言時に確認済みだった。**実測は全項目で宣言予想と完全一致**
し、y18 part1 のcensus merge予測スリップ（105,651→110,682）のような
amendmentは不発生した。機体の組み立て（build_y19.py・count-asserted）は
ビルド段階のローカル作業で数回のcount修正を経て完成・出版bytesは修正後のみ。

## 昇格判定（2026-11-23・K1243 observed→proved）

フル14チェック監査 PASS・fail-closed事前検証済みC1dアンカー・census第三
実装のC11r消費・4回byte-identical決定性（うち1回は隔離側での全pipeline
完全ゼロ再生成）・fail-closed電池12種全捕捉により、**K1243 を
observed→proved に昇格した**（同一K項目・K1141/K1152/K1231/K1233/K1235/
K1237/K1240/K1242 前例）。マージ命題は y=1..19 で全称、tail
R>=x+z+20 => (x+19) mod 2、clip 2y+2=40 tight は15族連続（y=5..19）。
B子逐語連鎖は cand9..cand18 に拡大（証明済みB子使用は cand10/cand12..cand18）。

