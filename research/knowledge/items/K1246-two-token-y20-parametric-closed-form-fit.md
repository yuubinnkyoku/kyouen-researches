---
id: K1246
title: "2トークン残余ゲーム y=20族のパラメトリック閉形式の全称証明（全z>=0・全x>=20・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=20 parametric closed-form fit, P20-fit"
  - "cand20 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 105,710 probe points; even-y mechanical translation from the published FINAL cand18, the promoted-universal y=18 table with Y=18->20; reverse rename verified byte-identical to the published cand18 code in both directions)"
  - "seed law 8th consecutive one-shot test passed (cand11->13 / cand12->14 / cand13->15 / cand14->16 / cand15->17 / cand16->18 / cand17->19 / cand18->20, even-y pair series 12->14->16->18->20 proven-seed translation no.2 since cand11->13); FIRST family reaching 10 pin rows on BOTH parities (odd z d≡0 mod 4 {-16..20}, even z d≡2 mod 4 {-18..18}); most out-of-box pin rows in the series (4 rows, first family with 2 on EACH parity side, covered by spot deep raw-value checks (37,21)/(33,21)/(38,20)/(34,20)); FIRST 21-row th sweep 21..41; 4-row k=Y census {Y-2,Y}/{Y-1}/{Y} same shape as y=16/18; 6th consecutive family with zero in-box merge rows (full out-of-box merge regression 18,219 bad 0); K0913 z=6,y=20 proven-slice cross-check bad 0; total 165,061 comparison points bad 0"
  - "universal proof completed (2026-11-23, single-edition 14-check machine under single-owner declaration c1987caa): observed -> proved via the 14-check canonical audit at 6,947,960 comparison points bad 0, C1d published-slice anchors preflighted 4-way (11,700+9,240 pts), census_rows.py third implementation consumed by C11r (438,600 pts); clip window 2y+2=42 tight (16-family streak y=5..20, 8th walking first-violation (60,104,104)); merge proposition now universal through y=1..20"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰18,219比較・境界行(43,22)/(42,21)のspot照合に使用。y=20ではbox z<=30内にマージ行は存在せずz>=42が必要）
- type: extends
  target: K1242
  note: seed。cand20初稿は出版cand18（K1242 promoted・全称確定）のY=18→20機械翻訳（Y定数・in_T20/in_P20/cand20/b20 rename・docstring・行内コメント値の再計算のみでコード本体は全式Y式で1行も変わらず・逆renameが出版cand18コード本体とbyte同一になることを両方向で機械検証）で生成し、probe 105,710点に一発一致。seedが全称証明済み族なのはcand11→13（K1143 proved当时）以来2度目
- type: extends
  target: K1243
  note: 隣接奇数y族（y=19・observed→proved済み・2トークン族の全称y=1..19完結）の次の族（第20族）。y=20全称検証器のB子は出版cand19（K1243 proved）の逐語転写（x=20合流子{19,20}≡{20,19}でy=19族x=20行と同一状態）。B子逐語連鎖は本項の昇格でcand9..cand19に拡大・証明済みB子使用はcand10/cand12..cand19。マージ命題は本項でy=1..20に全称拡大
- type: extends
  target: K1238
  note: even-y統一テンプレートの第6データ点（偶数y族式〔z-odd I行k=floor((d+3y+2)/4)連続掃引・base行同式floor((d+3y+1)/4)・偶z I行k=floor((d+3y-1)/4)・pin格子統一式・pin行数y/2両偶奇・単一band則・tail x奇行〕のy=20でのfit level継続観測）
- type: extends
  target: K1143
  note: 「pinスロット=th-1」（奇z）と偶z 2k+1 slot則の行型比較基点（y=11..19の9族連続に続き10族目として両偶奇10 pin行すべてで算術的に成立）
- type: related
  target: K0913
  note: z=6,y=20証明済み切片（全称証明）との交差検証。probe生値のz=6行26行（x=20..45・R<=x+48）をK0913出版署名（ラダー{1,3,5}・pin(20,6)@43・pin(24,6)@45・掃引x=27でR∈{47,49,51,53}・定常R=47）とtail族式のz=6適用に対して機械再検査してbad 0。cand20は証明済み境界z=6とfit levelで完全一致（独立裏付け・全称ではない・2レーンの相互補強の記録）
- type: depends_on
  target: K1249
  note: y=20全称検証機械（K1249・単一機体14チェック・総6,947,960照合点・全bad 0・4実行byte-identical・fail-closed 12種全捕捉）が本項observed→proved昇格の全称証拠の正本
- type: generalizes
  target: K0999
  note: C1dアンカーA8u..A17uが固定z切片の出版一様閉形式をy=20行で4方照合（anchor×H_ordered×H_canonical×cand20）。z=8: K0999、preflight・機内掃引ともbad 0。y=20全称はz=8則のy>=20行側を含む
- type: generalizes
  target: K1001
  note: C1dアンカーのz=9一様閉形式K1001のy=20行4方照合 bad 0
- type: generalizes
  target: K1011
  note: C1dアンカーのz=10一様閉形式K1011のy=20行4方照合 bad 0
- type: generalizes
  target: K1065
  note: C1dアンカーのz=15一様閉形式K1065のy=20行4方照合+低R単一トークン縮約 bad 0（preflight 2,015点+低R縮約のうち当該分）
- type: generalizes
  target: K1077
  note: C1dアンカーのz=16一様閉形式K1077のy=20行4方照合+低R縮約 bad 0（preflight 2,041点+当該分）
- type: generalizes
  target: K1087
  note: C1dアンカーのz=17一様閉形式K1087のy=20行4方照合+低R縮約 bad 0（preflight 2,067点+当該分・y=10段階でK1087初稿の評価順序バグ170点を捕捉した事前検証段階のy=20版は初回から全一致）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（105,710 probe点一発一致・box内tail assertion 23,870点・box外spot 41,054点（全10奇z pin行・全10偶z pin行の個別行選択・4 box外pin行(37,21)/(33,21)/(38,20)/(34,20)のR<=130生値照合・全選択行にx>=20機械preflight assert）・merge回帰18,219比較・tail raw 78点・K0913交差検証・事前予想の判定表・y=12..19横断則・fail-closed 15変種（有効改ざん12種全検出・no-op 3種の正直記録）・誠実記録2点（飽和連続数ラベル・deep 44行のハンドオフ再構成）・実行環境フルリセット1回の記録）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/cand20.py
  role: verifier
  note: 閉形式の正本cand20（in_T20値2表・in_P20値1表・Y=20・Y==20ハードassert）とprobe全点照合（105,710点・mismatch 0・overlap 0・初稿一発一致）。出版cand18のY=18→20機械翻訳でコード本体は1行も変わっていない（逆rename byte同一を両方向機械検証）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/probe_y20.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=20..z+39・R<=x+z+40を超えるx+z+42=2y+2拡張cap・1,085行105,710点を書き出す決定論的生成器・約13秒）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/spot_y20.py
  role: verifier
  note: box外spot（全10奇z pin行・全10偶z pin行を個別行選択したdeep rows R<=130・bigz z=31..40・x=y=20 edge・far d∈{40,51,62}・tail raw・merge回帰18,219・LRU cap 1.5M決定的退避・264.6秒〔3全実行264.6/270.6/262.2で全ブロック数値一致〕）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/make_audit_y20.py
  role: verifier
  note: 監査生成器（pin格子観測ゲート〔box内可観測8+8行〕・box幾何独立再計算ゲート（宣言機械事前算出1,085行/105,710点と厳密照合）・逐行整合性ゲート〔x>=20・d再計算・merge flag・RLE長x+z+42〕・in-box tail assertion・in-box merge 0行ゲート・偶z対角値1 census・fail-closed・4実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 63f0fad3…71ddd・自己文書化・probe/spot/merge/tail数値・sha256ピン〔probe_rows 88981b77…62262〕・宣言commit cc20473c記録・K0913交差検証bad 0・4 box外pin行〔2+2〕の族初と誠実記録2点の記録）
- path: research/log/2026-11-23-y20-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit cc20473c・probe実行前に出版・事前横断予想の全記録・対抗宣言チェック・box幾何1,085行/105,710点・総比較点165,061の出版前機械算出・逆rename両方向検証の事前登録）
- path: research/log/2026-11-23-two-token-y20-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・宣言・経緯・誠実記録3点・出版記録・次段階）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/README.md
  role: proof
  note: 全称段階の正本README（単一機体14チェック版の機械構成・転写marker検査・段階実行結果表・C4t tight（16族連続・歩み8観測目）・決定性4実行〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種全捕捉・宣言予想と実測の完全一致の記録〔amendment不用〕・再現コマンド・昇格判定・解釈規約）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/verify_y20_universal.py
  role: verifier
  note: 正本検証器（単一機体14チェック版・53,146 bytes・SHA-256 1e2a519f0bf81c401a3d18e0183a24d333ffd5eafabcd4b37032b0ed41a96bc9・@@TRANSCRIPTION marker 3ブロック〔engine 1,957 bytes・cand19 3,501 bytes二ソース・cand20 3,212 bytes〕・C1dアンカー前のpreflight fail-closedゲート設計）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/census_rows.py
  role: verifier
  note: census第三実装（SHA-256 af93fcc7…・XMIN=20・XMAX=70・ZHI=80・LRU cap 1,600,000・rows 4,080・points 438,600・zero_points 219,325・misses 10,354,827・約20秒・census.txt 4,080行を生成）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/scripts/check_transcriptions_y20.py
  role: verifier
  note: 転写二重正本検証（engine 出版y19機〔blob c0cec1d5〕から逐語・cand19 出版cand19.py〔fit eaea0f6a blob cb05633f〕と出版y19機ブロックの両方とY→Y19改名差分のみで一致・sources_agree・cand20 出版cand20.py〔7a2d3f9a blob a54cfb40〕逐語・repo rootはAGENTS.md探索・SHA-256 82420958…）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/scripts/preflight_c1d_y20.py
  role: verifier
  note: C1d事前検証（SHA-256 3e9932d7…・出版6切片アンカー4方照合 11,700点+低R単一トークン縮約 9,240点・bad 0・anchor blockは出版y19 preflightからbyte-verbatim・JSON SHA-256 d2aabc6e…）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/audit.json
  role: data
  note: フル14チェック監査正本（SHA-256 a09cad0e…・total_points 6,947,960・total_bad 0・type_count 658,978・corollaries merge 1,003,367 / tail 192,254 全bad 0・stageはsingle-edition 14-check machine）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/audit-part1-12checks.json
  role: data
  note: 段階実行12チェック電池の監査退避正本（SHA-256 ff347b9c…・total_points 5,640,320・total_bad 0・宣言の段階実行プロトコルの記録・型658,978）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/census.txt
  role: data
  note: census行台帳正本（801,508 bytes・SHA-256 b858c496…・C11rが全行をcand20から再導出し438,600点bad 0）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/census-ordered.json
  role: data
  note: census ordered部（SHA-256 ed073fa8…・434,520点・bad 0・merge 94,380・tail 4,080）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/census-canonical.json
  role: data
  note: census canonical部（SHA-256 1f420269…・434,520点・bad 0・merge 94,380・tail 4,080）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/preflight-c1d-y20.json
  role: data
  note: C1d preflight結果正本（SHA-256 d2aabc6e…・11,700+9,240点bad 0・per z 1,833/1,859/1,885/2,015/2,041/2,067）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/transcriptions-check-y20.json
  role: data
  note: 転写検査結果（engine/cand19二ソース/cand20 全equal・overall PASS・隔離側でも再生成一致・SHA-256 db16070a…）
- path: research/experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/output/published_run.txt
  role: log
  note: 正典run transcript（段階実行の全記録〔転写検査→preflight→census→12チェック→14チェック〕・rc=0・4回決定性〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種・宣言の事前予想と全照合点数の一致）
- path: research/log/2026-11-23-y20-universal-verifier-single-owner-note.md
  role: log
  note: 全称段階の単一オーナー宣言ノート（commit c1987caa・機体実行前に出版・観測HEAD-before-push 69f76309・対抗宣言なしの確認記録・単一機体14チェック版の事前登録〔publish-then-execute〕・事前横断予想の機械算出〔出版y19 audit 14/14でcross-validated〕・K1249仮採番）
- path: research/log/2026-11-23-two-token-y20-universal-verifier.md
  role: log
  note: 全称段階の実行記録（選定・機体ビルド・段階実行・宣言予想との完全一致・決定性・fail-closed 12種・K1246昇格判定・出版記録・次のレジューム）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,20)、全z>=0・全x>=20・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand20）で
  分類する命題。全称は正本検証器（K1249・単一機体14チェック版・
  フル14チェック監査・総6,947,960照合点・全bad 0・4実行byte-identical
  〔3同一cwd+1隔離のfull-pipeline完全再生成〕・fail-closed 12種全捕捉）で
  検証済み（2026-11-23出版・単一オーナー宣言c1987caa配下でobserved→proved
  昇格）。系としてx<=z-21の単一トークン一致マージ命題y=20版とtail
  R>=x+z+21の(x+20) mod 2を含み、マージ命題はy=1..20で全称確定。
  標準11×11の空盤・二石root・S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNの
  まま。3トークン以上・y>=21族・固定幅・q点版も範囲外。
evidence: >-
  fit段階の証拠（2026-11-23出版・単一オーナー宣言cc20473c配下）:
  probe box全点一発一致（105,710点・mismatch 0）・box内tail assertion
  23,870点・box外spot 41,054点・merge回帰18,219比較・tail raw 78点・
  K0913交差検証26行・合計165,061点比較不一致0・seed法則8連続一発一致・
  4実行byte-identical・fail-closed電池15変種で有効改ざん12種全検出
  （本文「対象範囲」「現在の根拠」が詳細の正本）。
  全称段階の証拠（2026-11-23出版・単一オーナー宣言c1987caa配下・単一機体
  14チェック版でobserved→proved昇格）:
  転写二重正本検査（engine 1,957 bytes出版y19機から逐語〔blob c0cec1d5〕・
  cand19 3,501 bytes出版cand19.py〔blob cb05633f〕と出版y19機ブロックの
  二系統byte一致・Y→Y19改名・cand20 3,212 bytes出版cand20.py
  〔7a2d3f9a blob a54cfb40〕逐語・overall PASS・隔離側再生成一致）・
  C1d事前検証（出版6切片アンカー4方照合11,700点+低R縮約9,240点bad 0・
  anchor blockは出版y19 preflightからbyte-verbatim・組み込み前fail-closed
  ゲート・機内掃引135,660点bad 0）・census第三実装（rows 4,080・points
  438,600・zero_points 219,325・misses 10,354,827）をC11r（rows==80*51・
  全行をcand20から再導出）で消費しフル14チェック監査total 6,947,960点
  bad 0（型658,978・merge帰結1,003,367点・tail帰結192,254点・3同一cwd+
  隔離full-pipeline再生成1回で全出力byte-identical・audit.json SHA-256
  a09cad0e…）・段階12チェック電池の監査も別正本（total 5,640,320・bad 0・
  audit-part1-12checks.json ff347b9c…）で保存・fail-closed 12種全捕捉
  （census欠落/行削除4079!=4080/重複行(0,20)のFAIL-CLOSED・P-set/T-set
  改ざん→C11r bad 1・C11r tail反転→bad 4,080〔全行・宣言予想どおり〕・
  アンカー誤結合→C1d bad 14,666・lowR参照ずれR+1→bad 9,240・merge境界
  z-21→z-20→bad 7,528・clip窓42,43→40,41→C4 bad 1,881・in_P20 tail
  偶奇→C1 bad 4,898/C2 bad 24,024・band偶奇→C1 bad 1,763/C2 bad 24,451。
  探針(4)(8)の初回はprobe harness自体のno-opとして正直記録し有効版で
  再検出）。C4t clip 41違反570点 (60,104,104) で全bad 0かつtail/merge検査
  で裏付けられtight判定確定（16族連続y=5..20・最初違反はband下端と歩む
  系列の8観測目）。宣言の事前機械算出予想は全項目で実測と完全一致・
  amendment不用。
---

## 命題・範囲

すべての z>=0・x>=20・R>=0 に対して H(R;(x,20);z) = cand20(z,x,R) が成り立つ
（**status: proved・2026-11-23 単一機体14チェック全称検証の出版で
observed→proved 昇格**・全称段階の正本は
[全称検証実験dir](../../experiments/vertical-fiber-two-token-y20-parametric-allz-proof-20261123/README.md)）。
ここで cand20 は
z 偶奇別のパラメトリック T/P 集合表（fit実験dirの `cand20.py` が正本・Y=20・偶数 y 型で値1無限帯は
x 奇行・d = x-z・off = R-z）であり、出版 cand18（K1242 promoted）の Y=18→20 機械翻訳に等しい
（コード本体 1 行も変わらず・逆 rename byte 同一を両方向で機械検証済み）。

fit段階の正本は
[fit実験dir](../../experiments/vertical-fiber-two-token-y20-parametric-allz-fit-20261123/report.md)
で、
fit段階の証拠は下記「対象範囲」の合計 165,061 点比較・不一致 0 である。

## 対象範囲（fit 段階の有限証拠）

- probe box: z=0..30・x=20..z+39・R<=x+z+42（=2y+2）の生二重再帰 1,085 行・105,710 点
  （cand20 全点一致・mismatch 0・T/P 重複 0・値頻度 0:52,068/1:43,045/2:10,597・値 3 なし）
- box 内 tail assertion R>=x+z+21→(x+20) mod 2: 23,870 点 bad 0
- box 内マージ行 0 行（y=20 では x<=z-21 に z>=42 が必要・6 族連続）
- box 外 spot 41,054 点 bad 0（deep 44 行/5,720 点〔全 20 pin 行の個別行選択・4 box 外 pin 行
  (37,21)/(33,21)/(38,20)/(34,20) の R<=130 生値照合〕・bigz 240 行/28,800 点・edge 25 行/4,050 点・
  far 18 行/2,484 点・全選択行 x>=20 機械 assert）
- tail raw 回帰 6 行 78 点 bad 0・merge 回帰 18,219 比較 bad 0
  （z∈{42,49,56,63,73,86}・x=20..z-22・R<=x+z+41）・マージ境界行 (43,22)/(42,21) 生値一致
- K0913（z=6,y=20 証明済み切片）との交差再検査 26 行 bad 0
- 合計 165,061 点比較・不一致 0

## 現在の根拠

上記有限範囲の全点照合（宣言ノート cc20473c の事前横断予想全項目が fit level で一致・修正 0）、
probe_rows.txt 4 回再生成 byte-identical（SHA-256 88981b77…62262）・
audit.json 4 実行 byte-identical（SHA-256 63f0fad3…71ddd）・spot 3 全実行の数値一致・
fail-closed バッテリ 15 変種で有効改ざん 12 種全検出（no-op 3 種は電池設計の誤りとして
正直記録し有効版で再検出）・出版最終構造 seed 法則 8 連続一発一致
（偶数 y 系列 12→14→16→18→20・証明済み seed 外挿は cand11→13 以来 2 度目）。
決定性の再生成は実行環境フルリセット 1 回をはさんで実施されており、出版数値は
すべてリセット後の再生成正本由来である（report・audit に記録）。

## 構造（y=20 で新たに観測された族初構造・fit level）

- pin 行数 y/2=10 が両偶奇とも 10 行に達する初の族（奇z d≡0 mod 4{-16,...,20}・
  偶z d≡2 mod 4{-18,...,18}・box 外 pin 4 行〔2+2〕は系列最多かつ両側 2 行同時は系列初）
- 奇z I 帯行 th 21..41 の初の 21 行連続掃引（偶数 y 族の掃引長線形則 6 データ点目）
- k=Y=20 飽和 census 4 行 {Y-2,Y}/{Y-1}/{Y}（y=16/18 と同一の偶数族 4 行形状・
  奇数族 3 行形状 y=17/19 との偶奇分離の継続）
- 偶z 対角行の値 1 全欠如 13 族目候補・band 下端 2y+2=42 の 8 データ点目・
  偶数 y 単一 band 則の 6 連続目の観測（y=10/12/14/16/18/20）

## 限界・範囲外の明示

fit 段階の有限証拠に加え、y=20 の全称（A子・B子 出版 cand19 逐語転写・
C子・型機械 clip 窓 2y+2=42 の tight 判定〔16 族目候補→確定〕・census）は
単一オーナー宣言 c1987caa 配下で 2026-11-23 に実行・出版され、**本項は単一機体14チェック
監査の出版で proved に昇格した**（詳細は下記「全称段階の記録」）。
seed 法則・横断族式の全称は一般補題化レーンの対象であり、本項はその偶数 y 系列第 6 データ点
（fit level）として寄与する。
標準 11×11 の空盤勝敗・二石 root・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま一切言及しない。
3 トークン以上・y>=21 族・固定幅・q 点版安定化長・fold 系・n11 batch 系（Part BL 系）・
inversive arc 系（K1250/K1251/K1252/K1253）は対象外。

## 全称段階の記録（単一機体14チェック版・observed→proved・2026-11-23）

単一オーナー宣言 c1987caa（検証器実行前に出版・観測 HEAD-before-push 69f76309・
対抗宣言なしを確認）配下で、y=19 出版手続き（K1245・単一機体単一出版）を y=20
定数に適合した単一機体14チェック版として実施した（宣言で事前登録・段階実行:
転写検査→preflight→census→12チェック電池→フル14チェック・12チェック電池の
監査は audit-part1-12checks.json として別正本保存）:

- **機体**: 単一機体14チェック版 verify_y20_universal.py（53,146 bytes・
  SHA-256 1e2a519f…・C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12）。
  転写3ブロック（engine 1,957 bytes〔出版y19機 blob c0cec1d5 から逐語〕・
  cand19 3,501 bytes〔出版cand19.py〔fit eaea0f6a blob cb05633f〕と出版y19機
  ブロックの二系統 byte-equality・Y→Y19 改名・sources_agree〕・cand20 3,212
  bytes〔出版cand20.py 7a2d3f9a blob a54cfb40 から逐語〕）を
  check_transcriptions_y20.py が検査 PASS（cand19 は二ソース一致・隔離側でも
  再生成一致）。A子 H(R-1;(x-1,20);z)〔x==20 行は合流子 {19,20}≡{20,19} で
  cand19(z,20,R-1)〕・B子 出版 cand19 逐語転写〔x>=20 行は定義域 x>=19 の
  内側〕・C子 1 xor cand20(z-1,x,R-1)・型機械 clip 2y+2=42・番兵 43。
- **C1d 事前検証**: preflight_c1d_y20.py（SHA-256 3e9932d7…・anchor block は
  出版 y19 preflight から byte-verbatim）が出版6切片アンカー
  （K0999/K1001/K1011/K1065/K1077/K1087・z0∈{8,9,10,15,16,17}）を y=20 行で
  4方照合: **11,700点 bad 0**（per z 1,833/1,859/1,885/2,015/2,041/2,067）+
  低R単一トークン縮約 R<=z+6: **9,240点 bad 0**・3.3秒・JSON 正本 d2aabc6e…。
  機内 C1d 掃引（アンカー掃引 126,420 + lowR 9,240）は **135,660点 bad 0**。
- **census第三実装**: census_rows.py（SHA-256 af93fcc7…・XMIN=20・XMAX=70・
  ZHI=80・LRU cap 1,600,000・約20秒）が census.txt（801,508 bytes・4,080行・
  SHA-256 b858c496…）を生成し、C11r（rows==80*51=4,080・全行を cand20 の
  T/P集合・Thue-Morse index・tail から再導出）が **438,600点 bad 0**
  （zero_points 219,325・misses 10,354,827・hits 20,284,849）。
  census部品（C11ordered/C11canonical・bounded-memoization twin・LRU 1.6M）は
  各engine **434,520点 bad 0**・merge帰結各 94,380・tail各 4,080 bad 0。
- **段階12チェック電池**（part1相当）: **overall PASS・総5,640,320点・全bad 0・型658,978**
  （C1 25,080 / C1b 44,758 / C1d 135,660 / C2 233,877 / C2b 19,668 / C3 1,365 /
  C4 574,040 / C4t 574,040〔probe〕 / C7 200,000 / C8 1,078,938 / C9 895,302 /
  C12 1,857,592）・38.9秒・audit-part1-12checks.json（SHA-256 ff347b9c…）に退避。
- **フル14チェック監査**: **overall PASS・総照合点 6,947,960**（12チェック電池
  5,640,320 + C11 869,040 + C11r 438,600）・**全bad 0・型658,978**（系列:
  y=17 457,645 → y=18 523,398 → y=19 590,877 → y=20 658,978）・
  39.5秒/run・audit.json（SHA-256 a09cad0e…）が正本。
  merge帰結 **1,003,367点 bad 0**（x<=z-21 => H == single_token(x+20,z,R)・
  census幾何では z>=41 で初めて非空・6族連続のbox内マージ行0行の族的持続）・
  tail帰結 **192,254点 bad 0**（R>=x+z+21 => (x+20) mod 2）。
- **C4t**: clip 41（2y+1）違反**570点・最初 (60,104,104)** → clip窓 2y+2=42 は
  **tight・16族連続確定**（y=5..20: 12/14/…/40/42）・最初違反は band下端
  R-z=2y+2=42 とともに歩む系列の**8観測目**
  （(60,90,90)→(60,92,92)→…→(60,102,102)→(60,104,104)・宣言の事前予想
  〔違反>0・(60,104,104)〕と完全一致）。
- **決定性・fail-closed**: 4実行 byte-identical（同一cwd 3回 + 隔離
  tree/cwd/HOME+env -i+PYTHONHASHSEED=random 1回〔隔離側は転写検査・preflight・
  census_rows・census両部・フル14チェックの完全ゼロ再生成・census engine
  states まで同一〕）。fail-closed 12種全捕捉（census.txt欠落/行削除
  4079 != 4080/重複行 (0,20) のFAIL-CLOSED・P-set/T-set改ざん→C11r bad 1・
  C11r tail反転→bad 4,080〔全行・宣言の予想どおりrows数〕・アンカー誤結合
  (17,A17u)→(17,A10u)→C1d bad 14,666・lowR参照ずれ R+1→bad 9,240〔全lowR点が
  独立に識別〕・merge境界 z-21→z-20→merge bad 7,528・clip窓 42,43→40,41→
  C4 bad 1,881・in_P20 tail偶奇反転→C1 bad 4,898/C2 bad 24,024・band偶奇
  改ざん→C1 bad 1,763/C2 bad 24,451。探針(4)(8)の初回は probe harness 自体の
  no-op（sed pattern不一致）として正直記録し有効版で即再検出。12種すべて
  rc=1・スクラッチtreeで実施・各probeは正本から新規copy・probe後にbaselineを
  build bytes と cmp 検証・正典treeは無傷）。
- **宣言予想との完全一致**: 宣言ノートの事前機械算出（出版y19 auditの14点数を
  完全一致で再現して cross-validated）は preflight 11,700+9,240・C1d 135,660・
  census幾何全値・C11r 438,600・12チェック小計 6,373,700 + C1d 135,660 +
  C11r 438,600 = 総点 6,947,960・C4t違反>0と最初違反 (60,104,104)・C11r tail
  反転 bad 4,080 の**すべてが実測と完全一致**・amendment不要（全段階無修正）。
- **系の確定**: 2トークン族の全称は **y=1..20 で完結**（y=1..12 は旧来の単族
  証明・y=13..20 は機械検証の逐語連鎖）。マージ命題
  x<=z-21 => H == single_token(x+20,z,R) は y=1..20 で全称。tail
  R>=x+z+21 => (x+20) mod 2。clip窓 2y+2 は y=5..20 の 16 族連続で tight。
  B子逐語連鎖 cand9..cand19（証明済みB子使用は cand10/cand12..cand19）、
  機体 item は K1249（proposition は本項）。
- **誠実記録（帳簿の訂正）**: fit項のK1243関係ノートが「x=20合流子
  {19,20}≡{20,19}でy=19族x=20行」（機体の実装どおり A = cand19(z,20,R-1)・
  C3/C1bのraw照合で検証済み）であるべきところ「y=19族x=19行」と記載していた
  帳簿上の誤記を、本昇格編集で訂正した（実効的内容〔cand19逐語転写・合流子の
  同値〕は影響を受けず・指摘は帳簿づけのみ）。
- **範囲外の維持**: 標準 11×11 の空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は UNKNOWN のまま。3トークン以上・y>=21 族・固定幅・q点版は
  範囲外（y=21 族のfit〔K1248・observed〕は本項の結果を受け取る側にある）。
