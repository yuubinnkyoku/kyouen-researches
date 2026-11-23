---
id: K1248
title: "2トークン残余ゲーム y=21族のパラメトリック閉形式の全称証明（全z>=0・全x>=21・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=21 parametric closed-form fit, P21-fit"
  - "cand21 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 112,530 probe points; odd-y mechanical translation from the published FINAL cand19, the universally proved y=19 table (K1243), Y=19->21; reverse rename verified byte-identical to the published cand19 code in both directions)"
  - "seed law 9th consecutive one-shot test passed (odd-y pair series 11->13->15->17->19->21 5-for-5; THIRD consecutive proved-seed extrapolation after cand11->13 via K1143 and cand18->20 via K1242); z-odd pin rows reach 11 in a single parity for the first time ((y+1)/2=11, d==1 mod 4 {-19..21}); FIVE out-of-box pin rows (3 z-odd + 2 z-even, both series-firsts; raw-verified by spot deep rows (41,22)/(37,22)/(33,22)/(38,21)/(34,21)); 7th consecutive family with zero in-box merge rows (out-of-box merge regression 117 rows / 17,835 comparisons bad 0); 3-row k=Y census {20,21,21} odd-family shape (y=17 {16,17,17}, y=19 {18,19,19}); K0914 z=6,y=21 PROVED-slice three-way cross-check: raw probe vs proved T_21/P_21 boxes vs cand21 on ALL 2,268 in-box slice points bad 0; total 177,304 comparison points bad 0"
  - "universal proof completed (2026-11-23, single-edition 14-check machine under single-owner declaration a0519efe): observed -> proved via the 14-check canonical audit at 6,952,761 comparison points bad 0, C1d published-slice anchors preflighted 4-way (11,856+9,174 pts), census_rows.py third implementation consumed by C11r (436,000 pts); clip window 2y+2=44 tight (17-family streak y=5..21, 9th walking first-violation (60,106,106)); merge proposition now universal through y=1..21"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰117行17,835比較・境界行(43,21)/(44,22)のspot照合に使用。y=21ではbox z<=30内にマージ行は存在せずz>=43が必要・8族連続のbox内マージ0行〔マージ領域はcensus幾何でz>=43が初非空〕）
- type: extends
  target: K1243
  note: seed。cand21初稿は出版cand19（K1243 proved・全称確定）のY=19→21機械翻訳（Y定数・in_T21/in_P21/cand21/b21 rename・docstring・行内コメント値の再計算のみでコード本体は全式Y式で1行も変わらず・逆renameが出版cand19コード本体とbyte同一になることを両方向で機械検証）で生成し、probe 112,530点に一発一致。証明済みseed外挿は3連続目（cand11→13〔K1143 proved当时〕・cand18→20〔K1242 proved〕・cand19→21）
- type: extends
  target: K1246
  note: 隣接偶数y族（y=20・observed→proved済み・2トークン族の全称y=1..20完結）の次の族（第21族・奇数y型）。対比データ点としてpin mod-4クラス交代（y=19: 3/1・y=20: 0/2・y=21: 1/3）・box外pin個数系列（y=20の2+2→y=21の3+2）・k=Y census偶奇形状分離（y=20の4行→y=21の3行）・band下端系列42→44。y=21全称段階のB子は出版cand20の逐語転写（x=21合流子{20,21}≡{21,20}でy=20族x=21行と同一状態）であり、本項の昇格でB子逐語連鎖はcand9..cand20に拡大・証明済みB子使用はcand10/cand12..cand20。マージ命題は本項でy=1..21に全称拡大
- type: extends
  target: K1240
  note: 奇数y族3行k=Y census形状の第3データ点（y=17 {16,17,17}・y=19 {18,19,19}・y=21 {20,21,21}・奇数y族式z-odd I行k=floor((d+3y+1)/4)のペア反復th・z-odd base同式・偶z I行k=floor((d+3y-1)/4)・band_base/band_int分離・tail x偶行のy=21 fit level継続観測）
- type: extends
  target: K1143
  note: 「pinスロット=th-1」（奇z I行）と偶z base行2k+1 slot則（y=11..20の10族連続に続き11族目として奇z 11 pin行・偶z 10 pin行すべてで算術的に成立）
- type: related
  target: K0914
  note: z=6,y=21証明済み切片（全称証明・A/B/C選択肢署名表＋Theorem T＋一般tail定理）との交差検証。宣言で補助的と事前登録し、実行では出版T_21(x)/P_21(x)表を監査生成器へ転写してprobe box内z=6切片（x=21..47・R<=x+50）全2,268点の三点照合（生probe値vs証明済み分類・cand21 vs証明済み分類）をfail-closed gateで実施しbad 0。ラダー{1,3,5}・pin(21,6)@45・(25,6)@47・掃引x=28の{49,51,53,55}・定常R=49・tail R>=x+28→(x+21) mod 2が宣言予想・K0914出版表・生値で完全一致（独立裏付け・全称ではない・2レーンの相互補強の記録）
- type: depends_on
  target: K1255
  note: y=21全称検証機械（K1255・単一機体14チェック・総6,952,761照合点・全bad 0・4実行byte-identical・fail-closed 12種全捕捉・第2実行による独立再現と出版bytes第二ホストbyte再現）が本項observed→proved昇格の全称証拠の正本
- type: generalizes
  target: K0999
  note: C1dアンカーA8u..A17uが固定z切片の出版一様閉形式をy=21行で4方照合（anchor×H_ordered×H_canonical×cand21）。z=8: K0999、preflight・機内掃引ともbad 0。y=21全称はz=8則のy>=21行側を含む
- type: generalizes
  target: K1001
  note: C1dアンカーのz=9一様閉形式K1001のy=21行4方照合 bad 0
- type: generalizes
  target: K1011
  note: C1dアンカーのz=10一様閉形式K1011のy=21行4方照合 bad 0
- type: generalizes
  target: K1065
  note: C1dアンカーのz=15一様閉形式K1065のy=21行4方照合+低R単一トークン縮約 bad 0（preflight 2,041点+低R縮約のうち当該分）
- type: generalizes
  target: K1077
  note: C1dアンカーのz=16一様閉形式K1077のy=21行4方照合+低R縮約 bad 0（preflight 2,067点+当該分）
- type: generalizes
  target: K1087
  note: C1dアンカーのz=17一様閉形式K1087のy=21行4方照合+低R縮約 bad 0（preflight 2,093点+当該分）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（112,530 probe点一発一致・box内tail assertion 25,668点・box外spot 46,861点（全11奇z pin行・全10偶z pin行の個別行選択・5 box外pin行(41,22)/(37,22)/(33,22)/(38,21)/(34,21)のR<=130生値照合・全選択行にx>=21機械preflight assert）・merge回帰117行/17,835比較・tail raw 78点・K0914三点交差検証2,268点bad 0・事前横断予想の判定表（全項目一致・amendment不要）・誠実記録4点（probe docstring点数訂正110,148→112,530・sandbox制約下のspotブロック別再実行・改ざんバッテリno-op 2種の正直記録・pinned秒数）・y=12..21横断判定）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/cand21.py
  role: verifier
  note: 閉形式の正本cand21（in_T21値2表・in_P21値1表・Y=21）とprobe全点照合（112,530点・mismatch 0・overlap 0・初稿一発一致）。出版cand19のY=19→21機械翻訳でコード本体は1行も変わっていない（逆rename byte同一を両方向で機械検証・結果docstring差し替え後に再検証PASS）。全称段階で機体K1255の転写検査がこのbytesに対してblocks一致を機械検証
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/probe_y21.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=21..z+41・R<=x+z+44=2y+2拡張cap・1,116行112,530点を書き出す決定論的生成器・3回再生成byte-identical incl. 隔離tree+env -i+PYTHONHASHSEED=random）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/spot_y21.py
  role: verifier
  note: box外spot（全11奇z pin行・全10偶z pin行を個別行選択したdeep rows R<=130・bigz z=31..40・x=y=21 edge・far d∈{42,53,64}・tail raw・merge回帰117行/17,835・LRU cap 1.5M決定的退避・run1全実行302.5秒）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/make_audit_y21.py
  role: verifier
  note: 監査生成器（pin格子観測ゲート〔box内可観測8+8行〕・box幾何独立再計算ゲート（宣言機械事前算出1,116行/112,530点と厳密照合）・値ヒストグラム事前予想等価ゲート{0:55466,1:46196,2:10868}・逐行整合性ゲート〔x>=21・d再計算・merge flag・RLE長x+z+44〕・in-box tail depth 23点/行25,668点ゲート・in-box merge 0行ゲート・偶z対角値1 census（box内幾何学的vacuityを明記）・K0914出版T_21/P_21表転写によるz=6切片全2,268点三点照合fail-closedゲート・fail-closed・最終版4回実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/spot_chunk_rerun.py
  role: verifier
  note: spot決定性再実行driver（sandboxの単一実行300秒上限と環境リセット下で、出版spot_y21.pyのmain()を一意マーカーでバイトスライスしdeep/bigz/edge/far/tailmergeの各ブロックをexec再実行。run2/run3で全ブロック集計・LRU CacheInfo行がrun1と完全一致）
- path: research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 b61e6581…e2982・自己文書化・probe/spot/merge/tail数値・sha256ピン〔probe_rows bd9482c7…1c6cbf0・cand21 10d8e495…・probe_y21 8f79a9ef…・spot_y21 04440247…〕・宣言commit 2d3aeac2記録・K0914三点照合2,268点bad 0・5 box外pin行〔3+2〕の族初と誠実記録の記録）
- path: research/log/2026-11-23-y21-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit 2d3aeac2・probe実行前に出版・事前横断予想の全記録・対抗宣言チェック・box幾何1,116行/112,530点・総比較点177,304の出版前機械算出・逆rename両方向検証の事前登録）
- path: research/log/2026-11-23-two-token-y21-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・宣言・経緯・誠実記録4点・出版記録・次段階）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/README.md
  role: proof
  note: 全称段階の正本README（単一機体14チェック版の機械構成・転写marker検査・段階実行結果表・C4t tight（17族連続・歩み9観測目）・決定性4実行〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種全捕捉・宣言予想と実測の完全一致の記録〔86,436→86,469の宣言散文内転置のみ誠実記録〕・再現コマンド・昇格判定・解釈規約）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/verify_y21_universal.py
  role: verifier
  note: 正本検証器（単一機体14チェック版・53,269 bytes・SHA-256 0ab841d9dd3d445fbde1c8142383d365048d7e3ca79fcd22ec6230c5bcec4c5a・@@TRANSCRIPTION marker 3ブロック〔engine 1,957 bytes・cand20 3,308 bytes二ソース・cand21 3,412 bytes〕・C1dアンカー前のpreflight fail-closedゲート設計）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/census_rows.py
  role: verifier
  note: census第三実装（XMIN=21・XMAX=70・ZHI=80・RBUF=23・LRU cap 1,600,000・436,000点・zero_points 217,061・misses 10,909,227・census.txt〔4,000行+80空行区切り・800,318 bytes・SHA-256 d63141b7…〕を生成。台帳bytesは本editionでは実験dirに同梱せず生成器+SHA pinで再現する体裁〔y=20 editionは同梱〕・第2実行が出版bytesを第二ホストで再生成してbyte一致を確認）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/scripts/check_transcriptions_y21.py
  role: verifier
  note: 転写二重正本検証（engine 出版y20機〔blob 170f3346〕から逐語・cand20 出版cand20.py〔git blob a54cfb40〕と出版y20機ブロックの両方とY→Y20改名差分のみで一致・sources_agree・cand21 出版cand21.py〔git blob 38613e92〕逐語・repo rootはAGENTS.md探索）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/scripts/preflight_c1d_y21.py
  role: verifier
  note: C1d事前検証（出版6切片アンカー4方照合 11,856点+低R単一トークン縮約 9,174点・bad 0・anchor blockは出版y20 preflightからbyte-verbatim・JSON SHA-256 57897cfd…）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/audit.json
  role: data
  note: フル14チェック監査正本（SHA-256 c039ca73…・total_points 6,952,761・total_bad 0・type_count 727,229・corollaries merge 944,052 / tail 192,053 全bad 0・verifier self-hash 0ab841d9…）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/audit-part1-12checks.json
  role: data
  note: 段階実行12チェック電池の監査退避正本（SHA-256 dab3dc53…・total_points 5,652,761・total_bad 0・宣言の段階実行プロトコルの記録・型727,229）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/census-ordered.json
  role: data
  note: census ordered部（SHA-256 30279436…・432,000点・bad 0・merge 86,469・tail 4,000）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/census-canonical.json
  role: data
  note: census canonical部（SHA-256 b88e3ddc…・432,000点・bad 0・merge 86,469・tail 4,000）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/preflight-c1d-y21.json
  role: data
  note: C1d preflight結果正本（SHA-256 57897cfd…・11,856+9,174点bad 0・per z 1,859/1,885/1,911/2,041/2,067/2,093）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/transcriptions-check-y21.json
  role: data
  note: 転写検査結果（engine/cand20二ソース/cand21 全equal・overall PASS・SHA-256 79007127…）
- path: research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/output/published_run.txt
  role: log
  note: 正典run transcript（段階実行の全記録〔転写検査→preflight→census→12チェック→14チェック〕・rc=0・4回決定性〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種〔探針(4)(5)の初回no-opの正直記録含む〕・宣言の事前予想と全照合点数の一致・出版SHA-256 pin一式）
- path: research/log/2026-11-23-y21-universal-verifier-single-owner-note.md
  role: log
  note: 全称段階の単一オーナー宣言ノート（commit a0519efe・機体実行前に出版・観測HEAD-before-push 77d3cadf・対抗宣言なしの確認記録・単一機体14チェック版の事前登録〔publish-then-execute〕・事前横断予想の機械算出〔出版y19とy20の両audit 14/14でcross-validated〕・K1255仮採番）
- path: research/log/2026-11-23-two-token-y21-universal-verifier.md
  role: log
  note: 全称段階の実行記録（第1実行の出版と第2実行の独立再現・宣言予想との完全一致・決定性・fail-closed 12種×2実行・K1248昇格判定・出版記録・次のレジューム）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,21)、全z>=0・全x>=21・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand21）で
  分類する命題。全称は正本検証器（K1255・単一機体14チェック版・
  フル14チェック監査・総6,952,761照合点・全bad 0・4実行byte-identical
  〔3同一cwd+1隔離のfull-pipeline完全再生成〕・fail-closed 12種全捕捉・
  並走第2実行による独立再現と出版bytesの第二ホストbyte再現）で検証済み
  （2026-11-23出版・単一オーナー宣言a0519efe配下でobserved→proved昇格）。
  系としてx<=z-22の単一トークン一致マージ命題y=21版とtail
  R>=x+z+22の(x+21) mod 2を含み、マージ命題はy=1..21で全称確定。
  標準11×11の空盤・二石root・S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNの
  まま。3トークン以上・y>=22族・固定幅・q点版も範囲外。
evidence: >-
  fit段階の証拠（2026-11-23出版・単一オーナー宣言2d3aeac2配下）:
  probe box全点一発一致（112,530点・mismatch 0）・box内tail assertion
  25,668点・box外spot 46,861点・merge回帰117行/17,835比較・tail raw 78点・
  K0914交差検査2,268点・合計177,304点比較不一致0・seed法則9連続一発一致・
  probe_rows 3回再生成byte-identical・audit 4実行byte-identical・
  fail-closed電池20変種で有効改ざん16種全検出
  （本文「対象範囲」「現在の根拠」が詳細の正本）。
  全称段階の証拠（2026-11-23出版・単一オーナー宣言a0519efe配下・単一機体
  14チェック版でobserved→proved昇格）:
  転写二重正本検査（engine 1,957 bytes出版y20機〔blob 170f3346〕から逐語・
  cand20 3,308 bytes 出版cand20.py〔git blob a54cfb40〕と出版y20機ブロックの
  二系統byte一致・Y→Y20改名・両ソースbyte一致・cand21 3,412 bytes 出版
  cand21.py〔git blob 38613e92〕逐語・overall PASS・隔離側再生成一致）・
  C1d事前検証（出版6切片アンカー4方照合11,856点+低R縮約9,174点bad 0・
  anchor blockは出版y20 preflightからbyte-verbatim・組み込み前fail-closed
  ゲート・機内掃引135,108点bad 0）・census第三実装（rows 4,000=80*50・
  points 436,000・zero_points 217,061・misses 10,909,227）をC11r（全行を
  cand21から再導出・行数斉一性・行重複/欠損FAIL-CLOSED）で消費しフル14
  チェック監査total 6,952,761点 bad 0（型727,229・merge帰結944,052点・
  tail帰結192,053点・3同一cwd+隔離full-pipeline再生成1回で全出力
  byte-identical・audit.json SHA-256 c039ca73…・census.txt d63141b7…は
  本editionでは生成器+pinで再現〔第2実行が出版bytesから第二ホストで再生成
  byte一致〕）・段階12チェック電池の監査も別正本（total 5,652,761・bad 0・
  audit-part1-12checks.json dab3dc53…）で保存・fail-closed 12種全捕捉が
  両実行で実施（census欠落/行削除3999!=4000/重複行(0,21)のFAIL-CLOSED・
  P-set/T-set改ざん→C11r bad 1・C11r tail反転→bad 4,000〔全行・宣言予想
  どおり〕・アンカー誤結合→C1d bad 14,769・lowR参照ずれR+1→bad 9,174〔全
  lowR点が独立に識別〕・merge境界z-22→z-21→merge bad>0・clip窓44,45→42,43
  →C4 bad 1,360・in_P21 tail偶奇→C1 bad 2,449/C2 bad 23,478・in_P21 band
  偶奇→C1/C2 bad>0〔第1実行は両band行C1 1,692/C2 24,431・第2実行は
  band_baseのみC1 935/C2 23,211〕。探針の初回no-op〔第1実行(4)(5): 正規
  表現が括弧集合構文に不 matchで中断・第2実行(2): 台帳末尾の空行区切り削除
  をデータ行削除と取り違え〕はprobe harness自体の誤りとして正直記録し有効
  版で再検出）・並走第2実行がAST同一の自前ビルドで全数値再現（自ビルド
  audit a0b23fb3…・検証台帳は出版census.txtとbyte同一）した上でmainから
  の出版bytes（commit 8960e633）を第二ホストで段階再実行し全7出版出力byte
  再現。C4t clip 43違反408点・最初(60,106,106)で clip 2y+2=44 はtight
  （17族連続y=5..21・最初違反はband下端と歩む系列の9観測目）。宣言の事前
  機械算出予想は散文内転置1件（86,436→機械算出86,469・宣言合計944,052は
  86,469と自己整合）を除き全項目で実測と完全一致（宣言noteは日付付き一次
  資料として改稿せず実験README/run transcript/K1255 itemに訂正記録）。
---

## 命題・範囲

すべての z>=0・x>=21・R>=0 に対して H(R;(x,21);z) = cand21 が成り立つ
（**status: proved・2026-11-23 単一機体14チェック全称検証の出版で
observed→proved 昇格**・全称段階の正本は
[全称検証実験dir](../../experiments/vertical-fiber-two-token-y21-universal-proof-20261123/README.md)）。
ここで cand21 は
z 偶奇別のパラメトリック T/P 集合表（fit実験dirの `cand21.py` が正本・Y=21・**奇数 y 型で値1無限帯・tail は x 偶行**・
d = x-z・off = R-z）であり、出版 cand19（K1243 proved）の Y=19→21 機械翻訳に等しい
（コード本体 1 行も変わらず・逆 rename byte 同一を両方向で機械検証済み）。

fit段階の正本は
[fit実験dir](../../experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/report.md)
で、
fit段階の証拠は下記「対象範囲」の合計 177,304 点比較・不一致 0 である。

## 対象範囲（fit 段階の有限証拠）

- probe box: z=0..30・x=21..z+41・R<=x+z+44（=2y+2）の生二重再帰 1,116 行・112,530 点
  （cand21 全点一致・mismatch 0・T/P 重複 0・値頻度 0:55,466/1:46,196/2:10,868・値 3 なし）
- box 内 tail assertion R>=x+z+22→(x+21) mod 2: 25,668 点 bad 0
- box 内マージ行 0 行（y=21 では x<=z-22 に z>=43 が必要・7 族連続）
- box 外 spot 46,861 点 bad 0（deep 44 行/5,720 点〔全 21 pin 行の個別行選択・5 box 外 pin 行
  (41,22)/(37,22)/(33,22)/(38,21)/(34,21) の R<=130 生値照合〕・bigz 280 行/34,510 点・edge 25 行/4,075 点・
  far 18 行/2,556 点・全選択行 x>=21 機械 assert）
- tail raw 回帰 6 行 78 点 bad 0・merge 回帰 117 行 17,835 比較 bad 0
  （z∈{43,50,57,64,74,87}・x=21..z-23・R<=x+z+43）・マージ境界行 (43,21)/(44,22) 生値一致
- K0914（z=6,y=21 証明済み切片）との三点交差再検査 2,268 点 bad 0（fail-closed gate）
- 合計 177,304 点比較・不一致 0（宣言ノートの出版前機械算出と全数値一致）

## 現在の根拠

上記有限範囲の全点照合（宣言ノート 2d3aeac2 の事前横断予想全項目が fit level で一致・修正 0・amendment 不要）、
probe_rows.txt 3 回再生成 byte-identical（SHA-256 bd9482c7…1c6cbf0・内1回は隔離tree+env -i+PYTHONHASHSEED=random）、
audit.json 最終版 4 回実行 byte-identical（SHA-256 b61e6581…e2982）、spot は run1 全実行（302.5 秒）+
run2/run3 ブロック別再実行（出版スクリプトの main() バイトスライス・sandbox 制約のため）の 3 実行で
全ブロック集計・LRU CacheInfo 行が完全一致、fail-closed バッテリ 20 変種で有効改ざん 16 種全検出
（no-op 2 種は正直記録し有効版で再設計検出）、出版最終構造 seed 法則 9 連続一発一致
（奇数 y 系列 11→13→15→17→19→21 の 5 連続・証明済み seed 外挿 3 連続目）、
および全称段階の14チェック監査（下記「全称段階の記録」・総 6,952,761 点 bad 0）。

## 構造（y=21 で新たに観測された族初構造・fit level）

- 奇z pin 行数 (y+1)/2 = 11 が単一偶奇側で系列初の到達点（d≡1 (mod 4) {-19,-15,-11,-7,-3,1,5,9,13,17,21}）
- box 外 pin 行 5 行（奇z 3 行 d=-19/-15/-11〔z>=41/37/33〕＋偶z 2 行 d=-17/-13〔z>=38/34〕）は
  合計も単一偶奇側 3 行も系列初（y=17: 1・y=18: 1+1・y=19: 2+1・y=20: 2+2）
- 偶z base 上端 d=21=Y 飽和の 6 族連続（y=16..21）・奇z base d=Y-1=20 飽和の 8 族連続（y=14..21）
- k=Y=21 census 3 行 {20,21,21} の奇数族 3 行形状（y=17/19 と同型・偶数族 4 行形状との偶奇分離継続）
- band 下端 2y+2=44 の 9 データ点目・偶z 対角行の値 1 全欠如 14 族目候補
  （spot deep (42,21) 全行照合が正本証拠・probe box は d>=-9 のみで box 内対角行は幾何学的に存在しない）
- y=21 機体の型登録数 727,229（系列: y=17 457,645 → y=18 523,398 → y=19 590,877 →
  y=20 658,978 → y=21 727,229）・C4 in-box 登録型数は clip 44/番兵 45 で 429,397

## 限界・範囲外の明示

fit 段階の有限証拠に加え、y=21 の全称（A子・B子 出版 cand20 逐語転写〔K1246 proved〕・
C子 1 xor cand21(z-1,x,R-1)・型機械 clip 窓 2y+2=44 の tight 判定〔17 族目候補→確定〕・census）は
単一オーナー宣言 a0519efe 配下で 2026-11-23 に実行・出版され、**本項は単一機体14チェック
監査の出版で proved に昇格した**（詳細は下記「全称段階の記録」）。
seed 法則・横断族式の全称は一般補題化レーンの対象であり、本項はその奇数 y 系列第 6 データ点
（fit level）として寄与する。
標準 11×11 の空盤勝敗・二石 root・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま一切言及しない。
3 トークン系（K1247 仮採番レーン）・y>=22 族・固定幅・q 点版安定化長・fold 系・n11 batch 系（Part BL 系）・
inversive arc 系（K1250/K1251/K1252/K1253）は対象外。

## 全称段階の記録（単一機体14チェック版・observed→proved・2026-11-23）

単一オーナー宣言 a0519efe（検証器実行前に出版・観測 HEAD-before-push 77d3cadf・
対抗宣言なしを確認）配下で、y=20 出版手続き（K1249・単一機体単一出版）を y=21
定数に適合した単一機体14チェック版として実施した（宣言で事前登録・段階実行:
転写検査→preflight→census→12チェック電池→フル14チェック・12チェック電池の
監査は audit-part1-12checks.json として別正本保存）:

- **機体**: 単一機体14チェック版 verify_y21_universal.py（53,269 bytes・
  SHA-256 0ab841d9…・C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12）。
  転写3ブロック（engine 1,957 bytes〔出版y20機 blob 170f3346 から逐語〕・
  cand20 3,308 bytes〔出版cand20.py〔git blob a54cfb40〕と出版y20機
  ブロックの二系統 byte-equality・Y→Y20 改名・sources_agree〕・cand21 3,412
  bytes〔出版cand21.py〔git blob 38613e92〕から逐語〕）を
  check_transcriptions_y21.py が検査 PASS（cand20 は二ソース一致・隔離側でも
  再生成一致）。A子 H(R-1;(x-1,21);z)〔x==21 行は合流子 {20,21}≡{21,20} で
  cand20(z,21,R-1)〕・B子 出版 cand20 逐語転写〔x>=21 行は定義域 x>=20 の
  内側〕・C子 1 xor cand21(z-1,x,R-1)・型機械 clip 2y+2=44・番兵 45。
- **C1d 事前検証**: preflight_c1d_y21.py（anchor block は出版 y20 preflight
  から byte-verbatim）が出版6切片アンカー（K0999/K1001/K1011/K1065/
  K1077/K1087・z0∈{8,9,10,15,16,17}）を y=21 行で4方照合:
  **11,856点 bad 0**（per z 1,859/1,885/1,911/2,041/2,067/2,093）+
  低R単一トークン縮約 R<=z+6: **9,174点 bad 0**・JSON 正本 57897cfd…。
  機内 C1d 掃引（アンカー掃引 125,934 + lowR 9,174）は **135,108点 bad 0**。
- **census第三実装**: census_rows.py（XMIN=21・XMAX=70・ZHI=80・RBUF=23・
  LRU cap 1,600,000・約21-26秒）が census.txt（800,318 bytes・4,000行+80
  空行区切り・SHA-256 d63141b7…）を生成し、C11r（rows==80*50=4,000・全行を
  cand21 のT/P集合・Thue-Morse index・tail から再導出）が **436,000点 bad 0**
  （zero_points 217,061・misses 10,909,227・hits 21,370,154）。
  census部品（C11ordered/C11canonical・bounded-memoization twin・LRU 1.6M）は
  各engine **432,000点 bad 0**・merge帰結各 86,469・tail各 4,000 bad 0。
- **段階12チェック電池**（part1相当）: **overall PASS・総5,652,761点・全bad 0・型727,229**
  （C1 25,650 / C1b 45,489 / C1d 135,108 / C2 238,091 / C2b 19,756 / C3 1,395 /
  C4 568,340 / C4t 568,340〔probe〕 / C7 200,000 / C8 1,100,592 / C9 892,650 /
  C12 1,857,350）・audit-part1-12checks.json（SHA-256 dab3dc53…）に退避。
- **フル14チェック監査**: **overall PASS・総照合点 6,952,761**（12チェック電池
  5,652,761 + C11 864,000 + C11r 436,000）・**全bad 0・型727,229**（系列:
  y=17 457,645 → y=18 523,398 → y=19 590,877 → y=20 658,978 → y=21 727,229）・
  audit.json（SHA-256 c039ca73…・verifier self-hash 0ab841d9…）が正本。
  merge帰結 **944,052点 bad 0**（x<=z-22 => H == single_token(x+21,z,R)・
  census幾何では z>=43 で初めて非空・**8族連続のbox内マージ0行の族的持続**）・
  tail帰結 **192,053点 bad 0**（R>=x+z+22 => (x+21) mod 2）。
- **C4t**: clip 43（2y+1）違反**408点・最初 (60,106,106)** → clip窓 2y+2=44 は
  **tight・17族連続確定**（y=5..21: 12/14/…/42/44）・最初違反は band下端
  R-z=2y+2=44 とともに歩む系列の**9観測目**
  （(60,90,90)→(60,92,92)→…→(60,104,104)→(60,106,106)・宣言の事前予想
  〔違反>0・(60,106,106)〕と完全一致）。
- **決定性・fail-closed**: 4実行 byte-identical（同一cwd 3回 + 隔離
  tree/cwd/HOME+env -i+PYTHONHASHSEED=random 1回〔隔離側は転写検査・preflight・
  census_rows・census両部・12チェック・フル14チェックの完全ゼロ再生成・
  census engine states まで同一〕）。fail-closed 12種全捕捉（census.txt
  欠落/行削除 3999 != 4000/重複行 (0,21) のFAIL-CLOSED・P-set/T-set改ざん→
  C11r bad 1・C11r tail反転→bad 4,000〔全行・宣言の予想どおりrows数〕・
  アンカー誤結合 (17,A17u)→(17,A10u)→C1d bad 14,769・lowR参照ずれ R+1→
  bad 9,174〔全lowR点が独立に識別〕・merge境界 z-22→z-21→merge bad>0・
  clip窓 44,45→42,43→C4 bad 1,360・in_P21 tail偶奇反転→C1 bad 2,449/C2
  bad 23,478・in_P21 band偶奇改ざん→C1/C2 bad>0〔両band行版で C1 1,692/
  C2 24,431〕。12種すべてrc=1・スクラッチtreeで実施・probe後にbaselineを
  build bytes と cmp 検証・正典treeは無傷）。
- **並走第2実行の独立再現**: 同一宣言配下の兄弟実行が同一レシピで独自ビルド
  した第2機体（SHA-256 fb84f369…・53,197 bytes）は実行可能コードについて
  出版機体と AST 同一（docstring定数を除去した構文木一致・差は全て
  docstring/comment）。第2実行は自前で全段階パイプライン（転写→preflight→
  census→両census部→12チェック→14チェック）・4回byte-identical決定性
  〔3同一cwd+1隔離full-pipeline・隔離側はenv -i+PYTHONHASHSEED=random〕・
  fail-closed 12種全捕捉〔探針(2)の初回は台帳末尾の空行区切り削除という
  harness側no-opとして正直記録し有効版で再検出〕を実施し全数値が出版runと
  一致し、さらに main から出版bytes（commit 8960e633）を再取得して第二
  ホストで段階再実行し、出版7出力（transcriptions/preflight/census両部/
  census.txt/audit-part1/audit.json〔出版self-hash 0ab841d9…を含む〕）すべて
  をbyte再現した。両ビルドのコメントレベルの軽微な不整合は機体item
  （K1255）に正直記録した（すべて非実行）。
- **宣言予想との完全一致**: 宣言ノートの事前機械算出（出版y19とy20の両audit
  の14点数を完全一致で再現して cross-validated）は preflight 11,856+9,174・
  C1d 135,108・census幾何全値・C11r 436,000・12チェック小計 6,381,653・
  段階電池 5,652,761・総点 6,952,761・merge帰結 944,052・tail帰結
  192,053・C4t違反>0と最初違反 (60,106,106)・C11r tail反転 bad 4,000 の
  **すべてが実測と完全一致**。唯一の散文内転置（per-engine merge領域の
  86,436 は機械算出 86,469 の転置・同一宣言の合計 944,052 は 86,469 と自己
  整合）は宣言noteを日付付き一次資料として改稿せず実験README・run
  transcript・K1255 itemに訂正記録した。
- **系の確定**: 2トークン族の全称は **y=1..21 で完結**（y=1..12 は旧来の単族
  証明・y=13..21 は機械検証の逐語連鎖）。マージ命題
  x<=z-22 => H == single_token(x+21,z,R) は y=1..21 で全称。tail
  R>=x+z+22 => (x+21) mod 2。clip窓 2y+2 は y=5..21 の 17 族連続で tight。
  B子逐語連鎖 cand9..cand20（証明済みB子使用は cand10/cand12..cand20）、
  機体 item は K1255（proposition は本項）。
- **範囲外の維持**: 標準 11×11 の空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は UNKNOWN のまま。3トークン以上・y>=22 族・固定幅・q点版は
  範囲外。
