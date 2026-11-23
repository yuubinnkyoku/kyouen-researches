---
id: K1257
title: "2トークン残余ゲーム y=22族の全称検証: 正本検証器 verify_y22_universal.py 単一機体14チェック全 PASS（K1256 を observed→proved へ昇格）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier for the two-token y=22 residual family H(R;(x,22);z), single-edition 14-check machine: overall PASS with 6,956,320 comparison points and bad 0, promoting K1256 observed -> proved; two-token universal now complete through y=1..22; y=22 is the first family beyond the previously proved range (y<=21) and the machine consumes the series-first PROVED universal B-child (published cand21, K1248)"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, C1d published-slice anchors pre-flighted fail-closed 4-way (12,012+9,108 pts bad 0, per z 1,885/1,911/1,937/2,067/2,093/2,119), type machine with clip window 2y+2=46 sentinel 47 and 797,559 types (series: y=17: 457,645 -> y=18: 523,398 -> y=19: 590,877 -> y=20: 658,978 -> y=21: 727,229 -> y=22: 797,559), tightness probe showing clip 45 has 280 confluence violations (first (60,108,108)) so 46 is tight (18-family streak y=5..22: 12/14/.../44/46)"
  - "census anchor z=0..79, x=22..70, R<=x+z+23 over both raw engines via bounded-memoization twins (LRU cap 1,600,000) run as separate commands C11ordered/C11canonical (429,240 points each engine, 49 x-rows per z, 22.6/24.9 s each) and fail-closed merged in the C11 mode with recomputed expected counts (points 429,240 / merge 78,750 / tail 3,920 per engine); independent census ledger consumer C11r over census_rows.py's census.txt (3,920 rows = 80*49, 433,160 points) bad 0"
  - "merge corollary x<=z-23 implies single_token(x+22,z,R) verified at 887,200 points (merge rows first non-empty at z=45 within the census geometry) and tail corollary R>=x+z+23 implies (x+22) mod 2 verified at 191,158 points, both with 0 mismatches; staged 12-check battery kept as a separate audit (5,664,680 pts bad 0, audit-part1-12checks.json)"
  - "single-owner declaration e1e60cd4 published before execution; every declaration pre-computation matched the machine measurements exactly (cross-validated against the published y=19, y=20 AND y=21 audits, 14/14 counts each, totals 6,941,913 / 6,947,960 / 6,952,761), no amendment needed, no prose digit transposition (numbers machine-transcribed from predictor stdout); B-child verbatim chain extended to cand9..cand21 (proved B-child usage cand10/cand12..cand21); single-publication single-host record with sibling-lane independent reproduction registered as the natural next-execution corroboration task"
relations:
  - type: extends
    target: "K1256"
    note: "K1256（y=22族 fit・cand22・出版時 observed）の正本監査段階。A子 x==22 行は合流子 {21,22}≡{22,21} で cand21(z,22,R-1)（y=21族x=22行と同一状態）・B子 出版 cand21（K1248 全称・y=21機 K1255 で proved 昇格済み・**系列初の全称確定済み B-child**）・C子 1 xor cand22(z-1,x,R-1) の14チェック。overall PASS + 4回 byte-identical（第1実行・3同一cwd+1隔離full-pipeline再生成）+ fail-closed 12種全捕捉で K1256 を observed→proved に昇格した"
  - type: depends_on
    target: "K1248"
    note: "B子の逐語転写元・K1248 の全称証明（y=21族）。cand21 ブロック（3,502 bytes）は出版 verify_y21_universal.py の cand21 ブロックと出版 cand21.py（git blob 38613e92）の二系統 byte一致（block-local Y→Y21 改名のみ・両ソース sources_agree）。y=22 における使用範囲は B子 x>=22 行と A子 x=22 合流で K1248 の定義域 x>=21 の内側。deep-tail 窓検査は証明済み cand21 tail主張 R>=x+z+22 => (x+21)%2 を x>=21 で使用（窓 (x+z+23, x+z+24, x+z+25)）"
  - type: depends_on
    target: "K1255"
    note: "機体構成の手続き的正本（y=21 単一機体14チェック版を y=22 定数に適合・C1d preflight anchor block は出版 y21 preflight から byte-verbatim で連鎖継続〔blob ca5e8284 の engine block 逐語含む〕・段階実行プロトコル・C4t 歩み予想・fail-closed 電池の構成を同一適用）"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary・low-R reduction）"
  - type: generalizes
    target: "K0999"
    note: "C1dアンカーA8uがz=8の出版一様閉形式（K0999）のy=22行で4方照合 bad 0（preflight 1,885点+機内掃引 125,442のうち当該分）"
  - type: generalizes
    target: "K1001"
    note: "C1dアンカーのz=9一様閉形式K1001のy=22行4方照合 bad 0（preflight 1,911点+当該分）"
  - type: generalizes
    target: "K1011"
    note: "C1dアンカーのz=10一様閉形式K1011のy=22行4方照合 bad 0（preflight 1,937点+当該分）"
  - type: generalizes
    target: "K1065"
    note: "C1dアンカーのz=15一様閉形式K1065のy=22行4方照合+低R単一トークン縮約 bad 0（preflight 2,067点+低R縮約のうち当該分）"
  - type: generalizes
    target: "K1077"
    note: "C1dアンカーのz=16一様閉形式K1077のy=22行4方照合+低R縮約 bad 0（preflight 2,093点+当該分）"
  - type: generalizes
    target: "K1087"
    note: "C1dアンカーのz=17一様閉形式K1087のy=22行4方照合+低R縮約 bad 0（preflight 2,119点+当該分）"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/README.md
  role: document
  note: "実験README（単一機体14チェック版の機械構成・転写marker検査・段階実行結果表・C4t tight（18族連続・歩み10観測目）・決定性4実行〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種全捕捉・宣言予想と実測の完全一致の記録〔amendment不要・散文内転置なし〕・再現コマンド・昇格判定・解釈規約・単一ホスト出版の正直記録）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/verify_y22_universal.py
  role: verifier
  note: "正本検証器（単一機体14チェック版・53,422 bytes・SHA-256 96d9787fae441a39c1cf0475e446b9dfef9bcc8297818afc1bd82a9f3c19ec6b・@@TRANSCRIPTION marker 3ブロック〔engine 1,957 bytes・cand21 3,502 bytes二ソース・cand22 3,212 bytes〕・C1dアンカー前のpreflight fail-closedゲート設計・census.txtが無い場合はC11rがFAIL-CLOSED）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/scripts/check_transcriptions_y22.py
  role: verifier
  note: "転写二重正本検証（engine 出版y21機〔blob ca5e8284〕から逐語・cand21 出版cand21.py〔git blob 38613e92〕と出版y21機ブロックの両方とY→Y21改名差分のみで一致・sources_agree・cand22 出版cand22.py〔git blob fd50358e〕逐語・構造アンカー抽出・repo root は AGENTS.md 探索・SHA-256 08b02ddc…）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/scripts/preflight_c1d_y22.py
  role: verifier
  note: "C1d事前検証（出版6切片アンカー4方照合 12,012点+低R単一トークン縮約 9,108点・bad 0・anchor block は出版y21 preflightからbyte-verbatim・JSON SHA-256 a65b967d…）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/census_rows.py
  role: verifier
  note: "census第三実装（XMIN=22・XMAX=70・ZHI=80・RBUF=24・LRU cap 1,600,000・433,160点・zero_points 216,626・misses 11,469,227・hits 22,466,349・約65秒・census.txt〔3,920行+80空行区切り・791,080 bytes・SHA-256 3275cc74…〕を生成。台帳bytesは本editionでは実験dirに同梱せず生成器+SHA pinで再現する体裁〔y=21 editionと同一〕）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/audit.json
  role: audit-output
  note: "フル14チェック監査正本（SHA-256 41813df3…・total_points 6,956,320・total_bad 0・type_count 797,559・corollaries merge 887,200 / tail 191,158 全bad 0・verifier self-hash 96d9787f…）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/audit-part1-12checks.json
  role: audit-output
  note: "段階実行12チェック電池の監査退避正本（SHA-256 1d434dbd…・total_points 5,664,680・total_bad 0・宣言の段階実行プロトコルの記録・型797,559）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/census-ordered.json
  role: audit-output
  note: "census ordered部（SHA-256 246506b2…・429,240点・bad 0・merge 78,750・tail 3,920）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/census-canonical.json
  role: audit-output
  note: "census canonical部（SHA-256 da0c20fc…・429,240点・bad 0・merge 78,750・tail 3,920）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/preflight-c1d-y22.json
  role: audit-output
  note: "C1d preflight結果正本（SHA-256 a65b967d…・12,012+9,108点bad 0・per z 1,885/1,911/1,937/2,067/2,093/2,119）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/transcriptions-check-y22.json
  role: audit-output
  note: "転写検査結果（engine/cand21二ソース/cand22 全equal・overall PASS・SHA-256 7767d14c…）"
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/published_run.txt
  role: log
  note: "正典run transcript（段階実行の全記録〔転写検査→preflight→census→12チェック→14チェック〕・rc=0・4回決定性〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種〔探針(9)初回no-opの正直記録を含む〕・宣言の事前予想と全照合点数の一致・出版SHA-256 pin一式）"
- path: research/log/2026-11-23-y22-universal-verifier-single-owner-note.md
  role: log
  note: "全称段階の単一オーナー宣言ノート（commit e1e60cd4・機体run前に出版・観測HEAD-before-push db195667・対抗宣言なしの確認記録・単一機体14チェック版の事前登録〔publish-then-execute〕・事前横断予想の機械算出〔出版y19/y20/y21の3audit 14点数ずつでcross-validated〕・K1257仮採番）"
- path: research/log/2026-11-23-two-token-y22-universal-verifier.md
  role: log
  note: "全称段階の実行記録（単一実行の出版・宣言予想との完全一致・決定性・fail-closed 12種・K1256昇格判定・出版記録〔commit A 6360bb32〕・単一ホスト出版の正直記録・次のレジューム）"
scope: >-
  κ=1残余ゲームHの2トークン族X=(x,22)、全z>=0・全x>=22・全R>=0 の全称命題
  （K1256）に対する正本検証として、実行・出版された単一機体14チェック
  （C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12・総6,956,320照合点・
  全bad 0・4実行byte-identical〔うち1回は隔離側での完全ゼロ再生成〕・
  fail-closed 12種全捕捉・宣言の事前登録昇格条件を満たし K1256 は
  observed→proved 昇格〔昇格はK1256側に記録〕）。宣言で事前登録された段階
  実行の12チェック電池の監査もaudit-part1-12checks.json（総5,664,680点・
  bad 0）として別正本で保存。系のマージ命題y=22版（x<=z-23）とtail
  （R>=x+z+23→(x+22) mod 2）はcorollary掃引で887,200 / 191,158点 bad 0
  でマージ命題はy=1..22で全称確定。並走する毎時実行による独立ビルド・
  第二ホスト再現は出版時点でまだ無く（単一ホスト出版・4実行byte-identical
  〔3同一cwd+1隔離full-pipeline再生成〕が昇格の根拠）、次回実行の裏付け
  課題としてrun logに明記した。標準11×11の空盤・二石root・S2 {59,60}・
  class 1/2/4は範囲外かつUNKNOWNのまま。3トークン以上・y>=23族・固定幅・
  q点版も範囲外。
evidence: >-
  2026-11-23出版・単一オーナー宣言 e1e60cd4 配下:
  (1) 転写の二重正本検証: engine/cand21/cand22 の3ブロックが出版bytesと
  byte一致（cand21は出版cand21.py〔git blob 38613e92〕と出版y21機ブロックの
  2ソースで一致〔block-local Y→Y21改名・sources_agree〕・隔離側の再生成
  でもPASS）。
  (2) 段階実行12チェック PASS: 総5,664,680点・bad 0（C1 26,220 / C1b
  46,220 / C1d 134,550 / C2 242,305 / C2b 19,844 / C3 1,425 / C4 562,559 /
  C4t 562,559〔probe〕 / C7 200,000 / C8 1,122,279 / C9 889,974 /
  C12 1,856,745）・audit-part1-12checks.jsonに退避。merge帰結（この時点）
  729,700点 bad 0・tail帰結（この時点）183,318点 bad 0。
  (3) フル14チェック PASS: 総6,956,320点・bad 0・型797,559
  （12チェック電池 5,664,680 + C11 858,480 + C11r 433,160。宣言noteの
  事前機械算出と全照合点数で完全一致〔出版y19/y20/y21の3auditの14点数ずつを
  完全一致で再現してcross-validated〕・amendmentなし・散文内転置なし）。
  (4) clip窓2y+2=46 は tight: C4tで clip 45 が 280違反・最初 (60,108,108)
  で band bottom とともに歩く最初違反の系列が10観測目（y=13..21の9観測に
  (60,108,108) を追加・y=5..22の18族tight連続確定）（宣言の事前横断予想
  〔違反>0・最初違反(60,108,108)〕と完全一致）。
  (5) census: z=0..79・x=22..70・R<=x+z+23・両エンジン各429,240点 bad 0
  （bounded-memoization twin・LRU 1.6M・分離コマンド
  C11ordered/C11canonical・C11 modeでFAIL-CLOSED検証の上で merge）。
  merge帰結はcensus幾何では z>=45 で初めて非空（merge 78,750/engine）。
  C11rはcensus_rows.py（第三実装・3,920行=80*49・433,160点・zero_points
  216,626・misses 11,469,227 / hits 22,466,349）の台帳をcand22から行単位
  再導出してbad 0（rows==3920の斉一性はFAIL-CLOSED・行重複/欠損も
  FAIL-CLOSED）。
  (6) C1d: 出版固定z切片アンカー（z0∈{8,9,10,15,16,17}・出版y21 preflight
  からanchor block逐語）をpreflight（4方照合 12,012点+低R縮約 9,108点
  bad 0・組み込み前fail-closedゲート）を経て機内掃引は134,550点 bad 0
  （アンカー掃引 125,442+lowR 9,108）。
  (7) 決定性: audit/census台帳/census部品/preflight/転写検査出力・
  4実行byte-identical（同一cwd 3回 + 隔離tree/cwd/HOME+env -i+
  PYTHONHASHSEED=random 1回・隔離側は全pipelineをゼロ再生成・census
  engine statesまで同一）。
  (8) fail-closed 12種全捕捉: census.txt欠落/行削除（3,919 != 3,920）/
  重複行(0,22)のFAIL-CLOSED・P-set/T-set改ざん→C11r bad 1・C11r tail反転
  →bad 3,920（全行・宣言予想どおりrows数）・アンカー誤結合(17,A17u)→
  (17,A10u)→C1d bad 14,869・lowR参照ずれR+1→bad 9,108（全lowR点が独立に
  識別）・merge境界 z-23→z-22→merge bad 59（初回の探針はharness自身の
  no-op〔編集不発効〕として正直記録し有効版で即再検出）・clip窓
  46,47→44,45→C4 bad 945・in_P22 tail偶奇反転（x%2==1→==0）→C1 bad
  4,898/C2 bad 24,024・band偶奇改ざん（off%2==0→==1）→C1 bad 1,763/C2
  bad 24,451。12種すべてrc=1・スクラッチtreeで実施・正典treeは無傷。
  (9) 誠実記録: 本機体の実行・出版は単一ホストである（4実行byte-identical
  〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed電池が昇格条件の根拠）。
  y=21 editionが持った兄弟実行による独立ビルド（AST同一）・全数値再現・
  出版bytesの第二ホストbyte再現は出版時点でまだ無く、独立再現は次回実行の
  最優先裏付け課題としてrun log・K1256 item・実験READMEに明記した。
---

## 14チェックの構成と実績値（単一機体版）

y=21 機（K1255）と同一構成のチェック群を y=22 定数へ適合:
A子は x==22 の合流子 {21,22}≡{22,21} で cand21(z,22,R-1)、
B子は出版 cand21（K1248 全称・**系列初の全称確定済み B-child**・
x>=22 行は定義域 x>=21 の内側）、
C子は 1 xor cand22(z-1,x,R-1)、型機械 clip 2y+2=46・番兵 47、
census z=0..79・x=22..70（80*49=3,920行）・R<=x+z+23、
C7 seed 20261222（y=19 20261192 / y=20 20261202 / y=21 20261212 系列）、
C8 の x=21 行は拡張整合行としてのみ（x<22 のraw主張はしない・deep-tail窓は
出版 cand21 のtail主張 R>=x+z+22 => (x+21)%2 を x>=21 で使用・窓
(x+z+23, x+z+24, x+z+25)）。

**実績値: overall PASS・総6,956,320照合点・全bad 0・型797,559**
（系列: y=17 457,645 → y=18 523,398 → y=19 590,877 → y=20 658,978 →
y=21 727,229 → y=22 797,559。C4 in-box登録型数は clip 46/番兵 47 で
448,494〔y=21 機の clip 44 での 429,397 に対応・宣言はここを事前予想していない〕）。
段階実行12チェック電池（part1相当）の監査は audit-part1-12checks.json
（総5,664,680点・bad 0）としても保存。merge帰結 887,200点・tail帰結
191,158点 bad 0。

## C4t tight と最初違反の歩み（18族連続）

clip 45（2y+1）で 280 型収束違反・最初違反 (60,108,108)。最初違反は
band bottom とともに歩む系列
（(60,90,90)→(60,92,92)→…→(60,104,104)→(60,106,106)→(60,108,108)）
10観測目で、**clip窓 2y+2 tight判定は18族連続（y=5..22: 12/14/…/44/46）**
に伸長した（宣言の事前横断予想〔違反>0・(60,108,108)〕と完全一致）。

## 宣言予想との完全一致（amendment なし・散文内転置なし）

宣言note（e1e60cd4）は全チェックの照合点数（C1 26,220 / C1b 46,220 /
C1d 134,550 / C2 242,305 / C2b 19,844 / C3 1,425 / C4=C4t 562,559 /
C7 200,000 / C8 1,122,279 / C9 889,974 / C11 858,480 / C12 1,856,745）・
preflight box（12,012+9,108・per-z 1,885/1,911/1,937/2,067/2,093/2,119）・
C1d 分解（125,442+9,108）・census幾何（3,920行・429,240/engine・merge
78,750/engine〔z>=45で初非空〕・tail 3,920/engine）・C11r 433,160・
12チェック電池 5,664,680（小計 6,388,610）・総点 6,956,320・merge帰結
887,200・tail帰結 191,158・C4t違反（>0・最初違反 (60,108,108)）・C11r
tail反転probe 3,920を事前機械算出し、同一算術関数が出版y19/y20/y21 auditの
全点数（各14点数・totals 6,941,913 / 6,947,960 / 6,952,761）を完全一致で
再現することを宣言時に確認済みだった。**実測は全項目で宣言予想と完全一致**
（amendmentなし。宣言数値は predict_y22_counts.py の stdout から機械転写
されたため、y=21 宣言で起きた散文内数字転置〔86,436 vs 86,469〕の再発は
無い）。機体の組み立てはビルド段階のローカル作業で完成・出版bytesは最終版のみ。

## 出版の記録（publish-then-execute・単一出版・単一ホストの正直記録）

commit A（実験dir正本12ファイル・6360bb32・census.txt は同梱せず生成器+
SHA pin 3275cc74… で再現する体裁・push直前の観測HEAD f687fa73・
fetch-back byte検証実施）が機体の単一出版正本である。commit B（run log +
K1256 proved 昇格編集 + 本 K1257 item）・commit C（knowledge README
bullet 2件追記）が知識側の反映である。**y=21 editionと異なり、出版時点で
兄弟実行による独立再現は存在しない**: 昇格判定の根拠は単一ホストでの
4実行 byte-identical（3同一cwd+1隔離full-pipeline完全ゼロ再生成）と
fail-closed 電池12種全捕捉・宣言の事前登録昇格条件（overall PASS・bad 0・
byte-identical 決定性・fail-closed 電池合格）の完全充足である。
宣言レシピからの独立ビルド・全数値再現・出版bytesの第二ホスト再現を
次回実行の最優先裏付け課題として明記する。

## 昇格判定（2026-11-23・K1256 observed→proved）

フル14チェック監査 PASS・fail-closed事前検証済みC1dアンカー・census第三
実装のC11r消費・4回byte-identical決定性（うち1回は隔離側での全pipeline
完全ゼロ再生成）・fail-closed電池12種全捕捉により、**K1256 を
observed→proved に昇格した**（同一K項目・宣言で事前登録された昇格条件・
K1141/K1152/K1231/K1233/K1236/K1239/K1241/K1242/K1243/K1245/K1246/K1249/
K1255 前例）。マージ命題は y=1..22 で全称、tail R>=x+z+23 => (x+22)
mod 2、clip 2y+2=46 tight は18族連続（y=5..22）。B子逐語連鎖は
cand9..cand21 に拡大（証明済みB子使用は cand10/cand12..cand21・
**cand21 が系列初の全称確定済み B-child として使用された最初の機体**）。
2トークン族の全称は y=1..22 で完結（**y=22 は全称確定済み範囲 y<=21 の
外の最初の族**）。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 はすべてUNKNOWNのまま。3トークン以上・y>=23族・固定幅・q点版
安定化長は範囲外。
