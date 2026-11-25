---
id: K1249
title: "2トークン残余ゲーム y=20族の全称検証: 正本検証器 verify_y20_universal.py 単一機体14チェック全 PASS（K1246 を observed→proved へ昇格）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier for the two-token y=20 residual family H(R;(x,20);z), single-edition 14-check machine: overall PASS with 6,947,960 comparison points and bad 0, promoting K1246 observed -> proved; two-token universal now complete through y=1..20"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, C1d published-slice anchors pre-flighted fail-closed 4-way (11,700+9,240 pts bad 0), type machine with clip window 2y+2=42 sentinel 43 and 658,978 types (series: y=14: 281,912 -> y=15: 335,658 -> y=16: 394,686 -> y=17: 457,645 -> y=18: 523,398 -> y=19: 590,877 -> y=20: 658,978), tightness probe showing clip 41 has 570 confluence violations (first (60,104,104)) so 42 is tight (16-family streak y=5..20: 12/14/16/18/20/22/24/26/28/30/32/34/36/38/40/42)"
  - "census anchor z=0..79, x=20..70, R<=x+z+21 over both raw engines via bounded-memoization twins (published code object rebound to an LRU-capped recursive cache, cap 1,600,000) run as separate commands C11ordered/C11canonical (434,520 points each engine, 51 x-rows per z, ~19-22 s each) and fail-closed merged in the C11 mode with recomputed expected counts (points 434,520 / merge 94,380 / tail 4,080 per engine); independent census ledger consumer C11r over census_rows.py's census.txt (4,080 rows, 438,600 points) bad 0"
  - "merge corollary x<=z-21 implies single_token(x+20,z,R) verified at 1,003,367 points (merge rows first non-empty at z=41, 6th consecutive family whose probe box contained zero merge rows) and tail corollary R>=x+z+21 implies (x+20) mod 2 verified at 192,254 points, both with 0 mismatches; staged 12-check battery kept as a separate audit (5,640,320 pts bad 0, audit-part1-12checks.json)"
  - "single-owner declaration c1987caa published before execution; every declaration pre-computation matched the machine measurements exactly (cross-validated against the published y=19 audit 14/14), no amendment needed; B-child verbatim chain extended to cand9..cand19 (proved B-child usage cand10/cand12..cand19)"
relations:
  - type: extends
    target: "K1246"
    note: "K1246（y=20族 fit・cand20・出版時 observed）の正本監査段階。A子=x==20 なら cand19(z,20,R-1)（合流子 {19,20}≡{20,19} の多重集合同値・x>=21 は cand20(z,x-1,R-1)）・B子=出版 cand19（K1243 全称・本項の親機 K1245 で proved 昇格済み）・C子=1 xor cand20(z-1,x,R-1) の14チェック。overall PASS + 4回 byte-identical + fail-closed 12種全捕捉で K1246 を observed→proved に昇格した"
  - type: depends_on
    target: "K1243"
    note: "B子の逐語転写元・K1243 の全称証明（y=19族）。cand19 ブロック（3,501 bytes）は出版 cand19.py（fit eaea0f6a blob cb05633f）と出版 y19 機ブロックの二系統 byte一致（Y→Y19 改名を除き・両ソース byte一致・sources_agree）。y=20 における使用範囲は B子 x>=20 行と A子 x=20 合流で K1243 の定義域 x>=19 の内側"
  - type: depends_on
    target: "K1245"
    note: "機体構成の手続き的正本（y=19 単一機体14チェック版を y=20 定数に適合・C1d preflight anchor block は出版 y19 preflight から byte-verbatim で連鎖継続・段階実行プロトコル・C4t 歩み予想・fail-closed 電池の構成を同一適用）"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary・low-R reduction）"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/README.md
  role: document
  note: "実験README（単一機体14チェック版の機械構成・転写marker検査・段階実行結果表・C4t tight（16族連続・歩み8観測目）・決定性4実行〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種全捕捉・宣言予想と実測の完全一致の記録〔amendment不用〕・再現コマンド・昇格判定・解釈規約）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/verify_y20_universal.py
  role: verifier
  note: "正本検証器（単一機体14チェック版・53,146 bytes・SHA-256 1e2a519f0bf81c401a3d18e0183a24d333ffd5eafabcd4b37032b0ed41a96bc9・@@TRANSCRIPTION marker 3ブロック〔engine 1,957 bytes・cand19 3,501 bytes二ソース・cand20 3,212 bytes〕・C1dアンカー前のpreflight fail-closedゲート設計）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/scripts/check_transcriptions_y20.py
  role: verifier
  note: "転写二重正本検証（engine 出版y19機〔blob c0cec1d5〕から逐語・cand19 出版cand19.py〔fit eaea0f6a blob cb05633f〕と出版y19機ブロックの両方とY→Y19改名差分のみで一致・sources_agree・cand20 出版cand20.py〔7a2d3f9a blob a54cfb40〕逐語・構造アンカー抽出・repo root は AGENTS.md 探索・SHA-256 82420958…）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/scripts/preflight_c1d_y20.py
  role: verifier
  note: "C1d事前検証（SHA-256 3e9932d7…・出版6切片アンカー4方照合 11,700点+低R単一トークン縮約 9,240点・bad 0・anchor block は出版y19 preflightからbyte-verbatim・JSON SHA-256 d2aabc6e…）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/census_rows.py
  role: verifier
  note: "census第三実装（SHA-256 af93fcc7…・XMIN=20・XMAX=70・ZHI=80・LRU cap 1,600,000・438,600点・zero_points 219,325・misses 10,354,827・約20秒・census.txt 4,080行を生成）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/audit.json
  role: audit-output
  note: "フル14チェック監査正本（SHA-256 a09cad0e…・total_points 6,947,960・total_bad 0・type_count 658,978・4実行byte-identical〔3同一cwd+1隔離full-pipeline再生成〕・corollaries merge 1,003,367 / tail 192,254 全bad 0・stageはsingle-edition 14-check machine）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/audit-part1-12checks.json
  role: audit-output
  note: "段階実行12チェック電池の監査退避正本（SHA-256 ff347b9c…・total_points 5,640,320・total_bad 0・宣言の段階実行プロトコルの記録・型658,978）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/census.txt
  role: data
  note: "census行台帳正本（801,508 bytes・SHA-256 b858c496…・C11rが全行をcand20から再導出し438,600点bad 0）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/census-ordered.json
  role: audit-output
  note: "census ordered部（SHA-256 ed073fa8…・434,520点・bad 0・merge 94,380・tail 4,080）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/census-canonical.json
  role: audit-output
  note: "census canonical部（SHA-256 1f420269…・434,520点・bad 0・merge 94,380・tail 4,080）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/preflight-c1d-y20.json
  role: audit-output
  note: "C1d preflight結果正本（SHA-256 d2aabc6e…・11,700+9,240点bad 0・per z 1,833/1,859/1,885/2,015/2,041/2,067）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/transcriptions-check-y20.json
  role: audit-output
  note: "転写検査結果（engine/cand19二ソース/cand20 全equal・overall PASS・隔離側でも再生成一致・SHA-256 db16070a…）"
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/published_run.txt
  role: log
  note: "正典run transcript（段階実行の全記録〔転写検査→preflight→census→12チェック→14チェック〕・rc=0・4回決定性〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種・宣言の事前予想と全照合点数の一致）"
- path: research/log/2026-11-23-y20-universal-verifier-single-owner-note.md
  role: log
  note: "単一オーナー宣言ノート（commit c1987caa・検証器run前に出版・観測HEAD-before-push 69f76309・対抗宣言なしの確認記録・単一機体14チェック版の事前登録〔publish-then-execute〕・事前横断予想の機械算出〔出版y19 audit 14/14でcross-validated〕・K1249仮採番）"
- path: research/log/2026-11-23-two-token-y20-universal-verifier.md
  role: log
  note: "全称段階の実行記録（選定・機体ビルド・段階実行・宣言予想との完全一致・決定性・fail-closed 12種・K1246昇格判定・出版記録・次のレジューム）"
scope: >-
  κ=1残余ゲームHの2トークン族X=(x,20)、全z>=0・全x>=20・全R>=0 の全称命題
  （K1246）に対する正本検証として、実行・出版された単一機体14チェック
  （C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12・総6,947,960照合点・
  全bad 0・4回実行byte-identical〔うち1回は隔離側での完全ゼロ再生成〕・
  fail-closed 12種全捕捉）。宣言で事前登録された段階実行の12チェック電池の
  監査もaudit-part1-12checks.json（総5,640,320点・bad 0）として別正本で
  保存。本監査のoverall PASSによりK1246はobserved→provedに昇格
  （昇格はK1246側に記録）。系のマージ命題y=20版（x<=z-21）とtail
  （R>=x+z+21→(x+20) mod 2）はcorollary掃引で1,003,367 / 192,254点 bad 0
  でマージ命題はy=1..20で全称確定。標準11×11の空盤・二石root・
  S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNのまま。
  3トークン以上・y>=21族・固定幅・q点版も範囲外。
evidence: >-
  2026-11-23出版・単一オーナー宣言 c1987caa 配下:
  (1) 転写の二重正本検証: engine/cand19/cand20 の3ブロックが出版bytesと
  byte一致（cand19は出版cand19.py〔fit eaea0f6a blob cb05633f〕と出版y19機
  ブロックの2ソースで一致・sources_agree・隔離側の再生成でもPASS）。
  (2) 段階実行12チェック PASS: 総5,640,320点・bad 0（C1 25,080 / C1b
  44,758 / C1d 135,660 / C2 233,877 / C2b 19,668 / C3 1,365 / C4 574,040 /
  C4t 574,040〔probe〕 / C7 200,000 / C8 1,078,938 / C9 895,302 /
  C12 1,857,592）・audit-part1-12checks.jsonに退避。
  (3) フル14チェック PASS: 総6,947,960点・bad 0・型658,978
  （12チェック電池 5,640,320 + C11 869,040 + C11r 438,600。宣言noteの
  事前機械算出と全照合点数で完全一致〔出版y19 auditの14点数を完全一致で
  再現してcross-validated〕・amendment不用）。
  (4) clip窓2y+2=42 は tight: C4tで clip 41 が 570違反・最初 (60,104,104)
  で band bottom とともに歩く最初違反の系列が8観測目
  （y=13..19の7観測に (60,104,104) を追加・y=5..20の16族tight連続確定）
  （宣言の事前横断予想〔違反>0・最初違反(60,104,104)〕と完全一致）。
  (5) census: z=0..79・x=20..70・R<=x+z+21・両エンジン各434,520点 bad 0
  （bounded-memoization twin・LRU 1.6M・分離コマンド
  C11ordered/C11canonical・C11 modeでFAIL-CLOSED検証の上 merge）。
  merge帰結はcensus幾何では z>=41 で初めて非空（merge 94,380/engine）。
  C11rはcensus_rows.py（第三実装・4,080行・438,600点・zero_points
  219,325・misses 10,354,827）の台帳をcand20から行単位再導出してbad 0
  （rows==80*51=4,080の斉一性はFAIL-CLOSED）。
  (6) C1d: 出版固定z切片アンカー（z0∈{8,9,10,15,16,17}・出版y19 preflight
  からanchor block逐語）をpreflight（4方照合 11,700点+低R縮約 9,240点
  bad 0・組み込み前fail-closedゲート）を経て機内掃引は135,660点 bad 0
  （anchor掃引 126,420+lowR 9,240）。
  (7) 決定性: audit/census台帳/census部品/preflight/転写検査出力 4実行
  byte-identical（同一cwd 3回 + 隔離tree/cwd/HOME+env -i+
  PYTHONHASHSEED=random 1回・隔離側は全pipeline（転写検査・preflight・
  census_rows・census両部・フル14チェック）をゼロ再生成・census engine
  states まで同一）。
  (8) fail-closed 12種全捕捉: census.txt欠落/行削除（4079 != 4080）/重複行
  (0,20)のFAIL-CLOSED・P-set/T-set改ざん→C11r bad 1・C11r tail反転→
  bad 4,080（全行・宣言予想どおりrows数）・アンカー誤結合
  (17,A17u)→(17,A10u)→C1d bad 14,666・lowR参照ずれR+1→bad 9,240（全lowR点
  が独立に識別）・merge境界 z-21→z-20→merge bad 7,528・clip窓 42,43→
  40,41→C4 bad 1,881・in_P20 tail偶奇反転→C1 bad 4,898/C2 bad 24,024・
  band偶奇改ざん→C1 bad 1,763/C2 bad 24,451（12種すべてrc=1・スクラッチtree
  で実施・各probe後にbaselineをbuild bytesとcmp検証し復元・正典treeは無傷。
  探針(4)(8)の初回はprobe harness自体のno-op〔sed pattern不一致〕として
  正直記録し有効版で即再検出）。
---

## 14チェックの構成と実績値（単一機体版）

y=19 機（K1245）と同一構成のチェック群を y=20 定数へ適合:
A子は x==20 の合流子 {19,20}≡{20,19} で cand19(z,20,R-1)、
B子は出版 cand19（K1243 全称・x>=20 行は定義域 x>=19 の内側）、
C子は 1 xor cand20(z-1,x,R-1)、型機械 clip 2y+2=42・番兵 43、
census z=0..79・x=20..70（80*51=4,080行）・R<=x+z+21、
C7 seed 20261202、C8 の x=19 行は拡張整合行としてのみ
（x<20 のraw主張はしない・deep-tail窓は出版 cand19 のtail主張
R>=x+z+20 => (x+19)%2 を x>=19 で使用）。

**実績値: overall PASS・総6,947,960照合点・全bad 0・型658,978**
（系列: y=14 281,912 → y=15 335,658 → y=16 394,686 → y=17 457,645 →
y=18 523,398 → y=19 590,877 → y=20 658,978）。段階実行12チェック電池
（part1相当）の監査は audit-part1-12checks.json（総5,640,320点・bad 0）
としても保存。merge帰結 1,003,367点・tail帰結 192,254点 bad 0。

## C4t tight と最初違反の歩み（16族連続）

clip 41（2y+1）で 570 型収束違反・最初違反 (60,104,104)。最初違反は
band bottom とともに歩む系列
（(60,90,90)→(60,92,92)→(60,94,94)→(60,96,96)→(60,98,98)→(60,100,100)
→(60,102,102)→(60,104,104)）8観測目で、**clip窓 2y+2 tight 判定は16族連続
（y=5..20: 12/14/…/40/42）**に伸長した（宣言の事前横断予想
〔違反>0・(60,104,104)〕と完全一致）。

## 宣言予想との完全一致（amendment 不用）

宣言note（c1987caa）は全14チェックの照合点数・preflight box（11,700+
9,240）・census幾何（4,080行・434,520/engine・merge 94,380・tail 4,080）・
C11r 438,600・12チェック小計 6,373,700 = 5,504,660 + C11 869,040・総点
6,947,960・C4t違反（>0・最初違反 (60,104,104)）・C11r tail反転probe 4,080
を事前機械算出し、同一の算術関数が出版y19 auditの全点数（14点数）を
完全一致で再現することを宣言時に確認済みだった。**実測は全項目で宣言予想と
完全一致**し、amendmentは不発生した（機体の組み立てはビルド段階の
ローカル作業で完成・出版bytesは最終版のみ）。

## 昇格判定（2026-11-23・K1246 observed→proved）

フル14チェック監査 PASS・fail-closed事前検証済みC1dアンカー・census第三
実装のC11r消費・4回byte-identical決定性（うち1回は隔離側での全pipeline
完全ゼロ再生成）・fail-closed電池12種全捕捉により、**K1246 を
observed→proved に昇格した**（同一K項目・K1141/K1152/K1231/K1233/K1235/
K1237/K1240/K1242/K1243 前例）。マージ命題は y=1..20 で全称、tail
R>=x+z+21 => (x+20) mod 2、clip 2y+2=42 tight は16族連続（y=5..20）。
B子逐語連鎖は cand9..cand19 に拡大（証明済みB子使用は cand10/cand12..cand19）。
2トークン族の全称は y=1..20 で完結。
