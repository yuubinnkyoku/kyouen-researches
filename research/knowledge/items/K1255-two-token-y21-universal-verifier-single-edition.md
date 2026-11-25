---
id: K1255
title: "2トークン残余ゲーム y=21族の全称検証: 正本検証器 verify_y21_universal.py 単一機体14チェック全 PASS（K1248 を observed→proved へ昇格）"
kind: computation
status: computed
topics: [grundy, residual-games]
aliases:
  - "universal verifier for the two-token y=21 residual family H(R;(x,21);z), single-edition 14-check machine: overall PASS with 6,952,761 comparison points and bad 0, promoting K1248 observed -> proved; two-token universal now complete through y=1..21"
  - "closed-form identity grid, deep-tail rows, option decomposition raw anchor, C1d published-slice anchors pre-flighted fail-closed 4-way (11,856+9,174 pts bad 0), type machine with clip window 2y+2=44 sentinel 45 and 727,229 types (series: y=17: 457,645 -> y=18: 523,398 -> y=19: 590,877 -> y=20: 658,978 -> y=21: 727,229), tightness probe showing clip 43 has 408 confluence violations (first (60,106,106)) so 44 is tight (17-family streak y=5..21: 12/14/16/18/20/22/24/26/28/30/32/34/36/38/40/42/44)"
  - "census anchor z=0..79, x=21..70, R<=x+z+22 over both raw engines via bounded-memoization twins (LRU cap 1,600,000) run as separate commands C11ordered/C11canonical (432,000 points each engine, 50 x-rows per z, ~21-29 s each) and fail-closed merged in the C11 mode with recomputed expected counts (points 432,000 / merge 86,469 / tail 4,000 per engine); independent census ledger consumer C11r over census_rows.py's census.txt (4,000 rows, 80*50, 436,000 points) bad 0"
  - "merge corollary x<=z-22 implies single_token(x+21,z,R) verified at 944,052 points (merge rows first non-empty at z=43, 8th consecutive family whose probe box contained zero merge rows) and tail corollary R>=x+z+22 implies (x+21) mod 2 verified at 192,053 points, both with 0 mismatches; staged 12-check battery kept as a separate audit (5,652,761 pts bad 0, audit-part1-12checks.json)"
  - "single-owner declaration a0519efe published before execution; every declaration pre-computation matched the machine measurements exactly (cross-validated against the published y=19 and y=20 audits 14/14 each), no amendment needed except one prose digit transposition recorded honestly (86,436 vs machine-computed 86,469 per-engine merge count, the declared total 944,052 self-consistent with 86,469); B-child verbatim chain extended to cand9..cand20 (proved B-child usage cand10/cand12..cand20)"
  - "two sibling hourly executions of the declaring lane both built the declared machine independently and both verified it end-to-end: the published build (commit 8960e633, verifier SHA-256 0ab841d9..., 53,269 bytes) ran the published staged pipeline (published_run.txt), and a second AST-identical build (docstrings stripped; SHA-256 fb84f369..., 53,197 bytes, comment-level bytes differ) reproduced every number, then re-fetched the published corpus from main and reproduced all published output bytes on a second host (census.txt d63141b7..., audit.json c039ca73... with the published self-hash, both engines' census parts, preflight and transcription JSONs)"
relations:
  - type: extends
    target: "K1248"
    note: "K1248（y=21族 fit・cand21・出版時 observed）の正本監査段階。A子=x==21 なら cand20(z,21,R-1)（合流子 {20,21}≡{21,20} の多重集合同値・x>=22 は cand20(z,x-1,R-1)）・B子=出版 cand20（K1246 全称・y=20 機 K1249 で proved 昇格済み）・C子=1 xor cand21(z-1,x,R-1) の14チェック。overall PASS + 4回 byte-identical（第1実行・出版run log記録）+ 第2実行での独立再現 + fail-closed 12種全捕捉（両実行それぞれ）で K1248 を observed→proved に昇格した"
  - type: depends_on
    target: "K1246"
    note: "B子の逐語転写元・K1246 の全称証明（y=20族）。cand20 ブロック（3,308 bytes）は出版 cand20.py（git blob a54cfb40）と出版 y20 機ブロックの二系統 byte一致（Y→Y20 改名を除き・両ソース byte一致・sources_agree）。y=21 における使用範囲は B子 x>=21 行と A子 x=21 合流で K1246 の定義域 x>=20 の内側。deep-tail 窓検査は証明済み cand20 tail主張 R>=x+z+21 => (x+20)%2 を x>=20 で使用"
  - type: depends_on
    target: "K1249"
    note: "機体構成の手続き的正本（y=20 単一機体14チェック版を y=21 定数に適合・C1d preflight anchor block は出版 y20 preflight から byte-verbatim で連鎖継続・段階実行プロトコル・C4t 歩み予想・fail-closed 電池の構成を同一適用）"
  - type: depends_on
    target: "K0832"
    note: "残余ゲームHの定義と単一トークン閉形式のraw anchor（C1b・merge corollary・low-R reduction）"
artifacts:
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/README.md
  role: document
  note: "実験README（単一機体14チェック版の機械構成・転写marker検査・段階実行結果表・C4t tight（17族連続・歩み9観測目）・決定性4実行〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種全捕捉・宣言予想と実測の完全一致の記録〔86,436→86,469 の宣言散文内転置のみ誠実記録〕・再現コマンド・昇格判定・解釈規約）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/verify_y21_universal.py
  role: verifier
  note: "正本検証器（単一機体14チェック版・53,269 bytes・SHA-256 0ab841d9dd3d445fbde1c8142383d365048d7e3ca79fcd22ec6230c5bcec4c5a・@@TRANSCRIPTION marker 3ブロック〔engine 1,957 bytes・cand20 3,308 bytes二ソース・cand21 3,412 bytes〕・C1dアンカー前のpreflight fail-closedゲート設計・census.txtが無い場合はC11rがFAIL-CLOSED）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/scripts/check_transcriptions_y21.py
  role: verifier
  note: "転写二重正本検証（engine 出版y20機〔blob 170f3346〕から逐語・cand20 出版cand20.py〔git blob a54cfb40〕と出版y20機ブロックの両方とY→Y20改名差分のみで一致・sources_agree・cand21 出版cand21.py〔git blob 38613e92〕逐語・構造アンカー抽出・repo root は AGENTS.md 探索・SHA-256 c4d7cc4e…）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/scripts/preflight_c1d_y21.py
  role: verifier
  note: "C1d事前検証（出版6切片アンカー4方照合 11,856点+低R単一トークン縮約 9,174点・bad 0・anchor block は出版y20 preflightからbyte-verbatim・JSON SHA-256 57897cfd…）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/census_rows.py
  role: verifier
  note: "census第三実装（XMIN=21・XMAX=70・ZHI=80・RBUF=23・LRU cap 1,600,000・436,000点・zero_points 217,061・misses 10,909,227・約21-26秒・census.txt〔4,000行+80空行区切り・800,318 bytes・SHA-256 d63141b7…〕を生成。台帳bytesは本editionでは実験dirに同梱せず生成器+SHA pinで再現する体裁〔y=20 editionは同梱〕）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/audit.json
  role: audit-output
  note: "フル14チェック監査正本（SHA-256 c039ca73…・total_points 6,952,761・total_bad 0・type_count 727,229・corollaries merge 944,052 / tail 192,053 全bad 0・verifier self-hash 0ab841d9…・第2実行がmainから再取得した出版bytesで第二ホスト上の段階再実行により全出力をbyte再現）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/audit-part1-12checks.json
  role: audit-output
  note: "段階実行12チェック電池の監査退避正本（SHA-256 dab3dc53…・total_points 5,652,761・total_bad 0・宣言の段階実行プロトコルの記録・型727,229）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/census-ordered.json
  role: audit-output
  note: "census ordered部（SHA-256 30279436…・432,000点・bad 0・merge 86,469・tail 4,000）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/census-canonical.json
  role: audit-output
  note: "census canonical部（SHA-256 b88e3ddc…・432,000点・bad 0・merge 86,469・tail 4,000）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/preflight-c1d-y21.json
  role: audit-output
  note: "C1d preflight結果正本（SHA-256 57897cfd…・11,856+9,174点bad 0・per z 1,859/1,885/1,911/2,041/2,067/2,093）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/transcriptions-check-y21.json
  role: audit-output
  note: "転写検査結果（engine/cand20二ソース/cand21 全equal・overall PASS・SHA-256 79007127…）"
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/published_run.txt
  role: log
  note: "正典run transcript（第1実行・段階実行の全記録〔転写検査→preflight→census→12チェック→14チェック〕・rc=0・4回決定性〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種・宣言の事前予想と全照合点数の一致・出版SHA-256 pin一式）"
- path: research/log/2026-11-23-y21-universal-verifier-single-owner-note.md
  role: log
  note: "単一オーナー宣言ノート（commit a0519efe・機体run前に出版・観測HEAD-before-push 77d3cadf・対抗宣言なしの確認記録・単一機体14チェック版の事前登録〔publish-then-execute〕・事前横断予想の機械算出〔出版y19とy20の両audit 14/14でcross-validated〕・K1255仮採番）"
- path: research/log/2026-11-23-two-token-y21-universal-verifier.md
  role: log
  note: "全称段階の実行記録（第1実行の出版と第2実行の独立再現の両方を記録・宣言予想との完全一致・決定性・fail-closed 12種×2実行・K1248昇格判定・出版記録・コメントレベル差異の誠実記録・次のレジューム）"
scope: >-
  κ=1残余ゲームHの2トークン族X=(x,21)、全z>=0・全x>=21・全R>=0 の全称命題
  （K1248）に対する正本検証として、実行・出版された単一機体14チェック
  （C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12・総6,952,761照合点・
  全bad 0・第1実行で4回実行byte-identical〔うち1回は隔離側での完全ゼロ再
  生成〕・fail-closed 12種全捕捉・宣言の事前登録昇格条件を満たし K1248 は
  observed→proved 昇格〔昇格はK1248側に記録〕）。宣言で事前登録された段階
  実行の12チェック電池の監査もaudit-part1-12checks.json（総5,652,761点・
  bad 0）として別正本で保存。系のマージ命題y=21版（x<=z-22）とtail
  （R>=x+z+22→(x+21) mod 2）はcorollary掃引で944,052 / 192,053点 bad 0
  でマージ命題はy=1..21で全称確定。並走する毎時実行の第2実行が独立ビルド
  （AST同一・docstring/comment差）で全数値を再現し、mainから再取得した
  出版corpusを第二ホストで段階再実行して全出版出力bytes（census.txt
  d63141b7…・audit.json c039ca73…含む）を再現した。標準11×11の空盤・二石
  root・S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNのまま。3トークン以上・
  y>=22族・固定幅・q点版も範囲外。
evidence: >-
  2026-11-23出版・単一オーナー宣言 a0519efe 配下:
  (1) 転写の二重正本検証: engine/cand20/cand21 の3ブロックが出版bytesと
  byte一致（cand20は出版cand20.py〔git blob a54cfb40〕と出版y20機ブロック
  の2ソースで一致・sources_agree・隔離側の再生成でもPASS）。
  (2) 段階実行12チェック PASS: 総5,652,761点・bad 0（C1 25,650 / C1b
  45,489 / C1d 135,108 / C2 238,091 / C2b 19,756 / C3 1,395 / C4 568,340 /
  C4t 568,340〔probe〕 / C7 200,000 / C8 1,100,592 / C9 892,650 /
  C12 1,857,350）・audit-part1-12checks.jsonに退避。
  (3) フル14チェック PASS: 総6,952,761点・bad 0・型727,229
  （12チェック電池 5,652,761 + C11 864,000 + C11r 436,000。宣言noteの
  事前機械算出と全照合点数で完全一致〔出版y19とy20の両audit 14点数ずつを
  完全一致で再現してcross-validated〕・amendmentは散文内転置1件のみ誠実記録
  〔86,436→機械算出86,469・宣言合計944,052は86,469と自己整合〕）。
  (4) clip窓2y+2=44 は tight: C4tで clip 43 が 408違反・最初 (60,106,106)
  で band bottom とともに歩く最初違反の系列が9観測目
  （y=13..20の8観測に (60,106,106) を追加・y=5..21の17族tight連続確定）
  （宣言の事前横断予想〔違反>0・最初違反(60,106,106)〕と完全一致）。
  (5) census: z=0..79・x=21..70・R<=x+z+22・両エンジン各432,000点 bad 0
  （bounded-memoization twin・LRU 1.6M・分離コマンド
  C11ordered/C11canonical・C11 modeでFAIL-CLOSED検証の上 merge）。
  merge帰結はcensus幾何では z>=43 で初めて非空（merge 86,469/engine）。
  C11rはcensus_rows.py（第三実装・4,000行=80*50・436,000点・zero_points
  217,061・misses 10,909,227 / hits 21,370,154）の台帳をcand21から行単位
  再導出してbad 0（rows==4000の斉一性はFAIL-CLOSED・行重複/欠損も
  FAIL-CLOSED）。
  (6) C1d: 出版固定z切片アンカー（z0∈{8,9,10,15,16,17}・出版y20 preflight
  からanchor block逐語）をpreflight（4方照合 11,856点+低R縮約 9,174点
  bad 0・組み込み前fail-closedゲート）を経て機内掃引は135,108点 bad 0
  （アンカー掃引 125,934+lowR 9,174）。
  (7) 決定性: audit/census台帳/census部品/preflight/転写検査出力・
  第1実行で4実行byte-identical（同一cwd 3回 + 隔離tree/cwd/HOME+env -i+
  PYTHONHASHSEED=random 1回・隔離側は全pipelineをゼロ再生成・census
  engine statesまで同一）。
  (8) fail-closed 12種全捕捉が第1実行と第2実行のそれぞれで実施され双方
  全捕捉: census.txt欠落/行削除（3999 != 4000）/重複行(0,21)の
  FAIL-CLOSED・P-set/T-set改ざん→C11r bad 1・C11r tail反転→bad 4,000
  （全行・宣言予想どおりrows数）・アンカー誤結合(17,A17u)→(17,A10u)→
  C1d bad 14,769・lowR参照ずれR+1→bad 9,174（全lowR点が独立に識別・
  両実行で一致）・merge境界 z-22→z-21→merge corollary bad>0・clip窓
  44,45→42,43→C4 bad 1,360（両実行で一致）・in_P21 tail偶奇反転→
  C1 bad 2,449/C2 bad 23,478（両実行で一致）・in_P21 band偶奇改ざん→
  C1/C2 bad>0（第1実行は両band行改ざんC1 1,692/C2 24,431・第2実行は
  band_baseのみC1 935/C2 23,211。探針の初回no-op〔第1実行: 探針(4)(5)の
  正規表現が括弧集合構文にマッチせず改ざん前に中断・第2実行: 探針(2)が
  台帳末尾の空行区切りを削りデータ行無傷のまま〕はprobe harness自体の
  誤りとして正直記録し有効版で即再検出）。
  (9) 第2実行の独立再現: 同じ宣言・同じ機械翻訳レシピから独自ビルドした
  機体（SHA-256 fb84f369…・53,197 bytes）が実行可能コードについて出版
  機体とAST同一（docstring定数を除去した構文木が一致・コメント等效差は
  両機体に存在し全て非実行）であることを確認した上で、自前の段階
  パイプライン（転写→preflight→census→両census部→12チェック→14チェック）・
  4回byte-identical決定性〔3同一cwd+1隔離full-pipeline、隔離側はenv -i+
  PYTHONHASHSEED=random〕・fail-closed 12種全捕捉を実施し全数値が出版
  runと一致（自ビルドaudit a0b23fb3…・検証台帳も出版census.txtとbyte同一）、
  さらにmainからの出版bytes再取得（commit 8960e633）を第二ホストで段階
  再実行し出版7出力（transcriptions/preflight/census両部/census.txt/
  audit-part1/audit.json〔出版self-hash 0ab841d9…を含む〕）すべてbyte再現。
---

## 14チェックの構成と実績値（単一機体版）

y=20 機（K1249）と同一構成のチェック群を y=21 定数へ適合:
A子は x==21 の合流子 {20,21}≡{21,20} で cand20(z,21,R-1)、
B子は出版 cand20（K1246 全称・x>=21 行は定義域 x>=20 の内側）、
C子は 1 xor cand21(z-1,x,R-1)、型機械 clip 2y+2=44・番兵 45、
census z=0..79・x=21..70（80*50=4,000行）・R<=x+z+22、
C7 seed 20261212（y=16 20261162 / y=17 20261172 / y=18 20261182 /
y=19 20261192 / y=20 20261202 系列）、C8 の x=20 行は拡張整合行としてのみ
（x<21 のraw主張はしない・deep-tail窓は出版 cand20 のtail主張
R>=x+z+21 => (x+20)%2 を x>=20 で使用）。

**実績値: overall PASS・総6,952,761照合点・全bad 0・型727,229**
（系列: y=17 457,645 → y=18 523,398 → y=19 590,877 → y=20 658,978 →
y=21 727,229。C4 in-box登録型数は clip 44/番兵 45 で 429,397
〔y=20 機の clip 42 での 408,708 に対応・宣言はここを事前予想していない〕）。
段階実行12チェック電池（part1相当）の監査は audit-part1-12checks.json
（総5,652,761点・bad 0）としても保存。merge帰結 944,052点・tail帰結
192,053点 bad 0。

## C4t tight と最初違反の歩み（17族連続）

clip 43（2y+1）で 408 型収束違反・最初違反 (60,106,106)。最初違反は
band bottom とともに歩む系列
（(60,90,90)→(60,92,92)→(60,94,94)→(60,96,96)→(60,98,98)→(60,100,100)
→(60,102,102)→(60,104,104)→(60,106,106)）9観測目で、**clip窓 2y+2 tight
判定は17族連続（y=5..21: 12/14/…/42/44）**に伸長した（宣言の事前横断予想
〔違反>0・(60,106,106)〕と完全一致）。

## 宣言予想との完全一致（amendment は散文内転置1件のみ）

宣言note（a0519efe）は全14チェックの照合点数・preflight box（11,856+
9,174）・census幾何（4,000行・432,000/engine・merge 86,469・tail 4,000）・
C11r 436,000・12チェック小計 6,381,653（C1dを除く12チェック+C11）+ C1d
135,108 + C11r 436,000 = 総点 6,952,761・C4t違反（>0・最初違反 (60,106,106)）・
C11r tail反転probe 4,000を事前機械算出し、同一の算術関数が出版y19 auditの
全点数（14点数）と出版y20 auditの全点数（14点数）の両方を完全一致で再現
することを宣言時に確認済みだった。**実測は全項目で宣言予想と完全一致**。
唯一の不一致は宣言散文のcensus幾何行の per-engine merge領域表記 86,436 が
機械算出 86,469 の数字転置であった点（同一宣言のmerge帰結合計 944,052
= 771,114 + 2×86,469 は 86,469 と自己整合であり実測と完全一致・宣言noteは
日付付き一次資料として改稿せず実験READMEとrun transcriptに訂正記録）。
機体の組み立てはビルド段階のローカル作業で完成・出版bytesは最終版のみ。

## 並走実行の記録（publish-then-execute・単一出版・誠実記録）

本項は同一の毎時スケジュールに乗る兄弟実行が同一宣言（a0519efe）配下で
同じ手続きを並走実行した最初の族である。第1実行が機体をビルド・実行し
実験dir正本12ファイルを commit 8960e633 として出版（observed
HEAD-before-push cc233107・output/published_run.txt に段階実行・決定性・
fail-closedの全記録を同梱・K1255はpush直前に空き番号であることを再確認）。
これに対し第2実行は、(a) 自らの機械翻訳ビルド（実行可能コードが出版機体と
AST同一であることを構文木比較で確認）で全段階パイプライン・決定性4回・
fail-closed 12種を独立に実行して全数値一致、(b) mainから出版bytesを再取得
し第二ホストで段階再実行して全7出版出力（census.txt d63141b7…・
audit.json c039ca73…・出版self-hash含む）をbyte再現、を行った。二つの
ビルドの差は docstring・コメント行のみで、両者のコメントレベルの軽微な
不整合（第1実行ビルド: cand21.py の SHA-256 docstring表記が1文字欠落
〔63桁〕・tightness probe コメントが y=20 の「CLIP=41」のまま〔実際の
probeは clip 43 で C4t チェック自体は正常〕・anchor block 由来コメント
が chain-head commit を 99b7e070〔y=19機〕と表記〔機械系列の実際の
chain-head は y=18 part2 commit d29acbd8〕。第2実行ビルド: anchor block
由来コメントが機械翻訳元 y=20 機の head 表記「published y=19 machine's
anchor block」を保持し即時転写元 y=20 機を明示しない）を本記録に正直に
列挙する（すべて非実行・転写検査はマーカー間の実際のbytesを検査するため
検証対象に影響しない）。 Publishers の正本は単一（commit 8960e633）で
あり、昇格判定の根拠は両実行の完全一致する実測値である。

## 昇格判定（2026-11-23・K1248 observed→proved）

フル14チェック監査 PASS・fail-closed事前検証済みC1dアンカー・census第三
実装のC11r消費・4回byte-identical決定性（うち1回は隔離側での全pipeline
完全ゼロ再生成）・fail-closed電池12種全捕捉・第2実行による独立再現と
出版bytesの第二ホストbyte再現により、**K1248 を observed→proved に昇格
した**（同一K項目・宣言で事前登録された昇格条件・
K1141/K1152/K1231/K1233/K1236/K1239/K1241/K1242/K1243/K1245/K1246/K1249
前例）。マージ命題は y=1..21 で全称、tail R>=x+z+22 => (x+21) mod 2、
clip 2y+2=44 tight は17族連続（y=5..21）。B子逐語連鎖は cand9..cand20 に
拡大（証明済みB子使用は cand10/cand12..cand20）。2トークン族の全称は
y=1..21 で完結。
