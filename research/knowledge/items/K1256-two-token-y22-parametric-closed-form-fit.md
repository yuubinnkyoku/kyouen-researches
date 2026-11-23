---
id: K1256
title: "2トークン残余ゲーム y=22族のパラメトリック閉形式の全称証明（全z>=0・全x>=22・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=22 parametric closed-form fit, P22-fit"
  - "cand22 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 119,567 probe points; even-y mechanical translation from the published FINAL cand20, the universally proved y=20 table (K1246 promoted, K1249 machine), Y=20->22; reverse rename verified byte-identical to the published cand20 code in both directions)"
  - "seed law 10th consecutive one-shot test passed (even-y pair series 12->14->16->18->20->22, 6-for-6; FOURTH consecutive proved-seed extrapolation after cand11->13 via K1143, cand18->20 via K1242, cand19->21 via K1243/K1248, cand20->22 via K1246); FIRST family with 11 pin rows on BOTH parities simultaneously (z-odd d==2 mod 4 {-18..22}, z-even d==0 mod 4 {-20..20}); MOST out-of-box pin rows in the series (3+3 = 6, series-first on EACH parity, raw-verified by spot deep rows (41,23)/(37,23)/(33,23)/(42,22)/(38,22)/(34,22)); FIRST 23-row consecutive-integer th sweep 23..45; 8th consecutive family with zero in-box merge rows (out-of-box merge regression 123 rows / 19,449 comparisons bad 0); K0915 z=6,y=22 PROVED-slice three-way cross-check: raw probe vs proved T_22/P_22 boxes vs cand22 on ALL 2,450 in-box slice points bad 0; total 182,042 comparison points bad 0"
  - "universal proof completed (2026-11-23, single-edition 14-check machine under single-owner declaration e1e60cd4): observed -> proved via the 14-check canonical audit at 6,956,320 comparison points bad 0, C1d published-slice anchors preflighted 4-way (12,012+9,108 pts), census_rows.py third implementation consumed by C11r (433,160 pts over 3,920 rows); clip window 2y+2=46 tight (18-family streak y=5..22, 10th walking first-violation (60,108,108)); merge proposition now universal through y=1..22; two-token universal complete through y=1..22; first family beyond the previously proved range y=1..21"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰123行19,449比較・境界行(45,22)/(46,23)のspot照合に使用。y=22ではマージ領域x<=z-23の成立にz>=46を必要としbox z<=30内のマージ行は0行・8族連続のbox内マージ0行〔マージ領域はcensus幾何でも z>=46 が初非空〕）
- type: extends
  target: K1246
  note: seed。cand22初稿は出版cand20（K1246 promoted・K1249機体で全称確定・2トークン族の全称はy=1..20完結）のY=20→22機械翻訳（Y定数・in_T22/in_P22/cand22/b22 rename・docstring・行内コメント値5件の再計算のみでコード本体は全式Y式で1行も変わらず・逆renameが出版cand20コード本体とbyte同一になることを両方向で機械検証）で生成し、probe 119,567点に一発一致。証明済みseed外挿は4連続目（cand11→13〔K1143 proved当时〕・cand18→20〔K1242〕・cand19→21〔K1243〕・cand20→22）。偶数y機械翻訳連鎖12→14→16→18→20→22の第6リンク
- type: extends
  target: K1248
  note: 隣接奇数y族（y=21・K1255機体でobserved→proved済み・2トークン族の全称y=1..21完結）の次の族（第22族・偶数y型）。**全称証明済み範囲（y<=21）の外の最初の族**。対比データ点としてpin mod-4クラス交代（y=20: 0/2・y=21: 1/3・y=22: 2/0）・box外pin個数系列（y=21の3+2→y=22の3+3）・k=Y census偶奇形状分離（y=21の3行→y=22の4行偶数族形状{20,22}/{21}/{22}・y=16/18/20と同型の4データ点目）・band下端系列44→46・掃引長21行→23行。y=22全称段階のB子は出版cand21の逐語転写（x=22合流子{21,22}≡{22,21}でy=21族x=22行と同一状態）で**系列初の全称確定済みB-child**
- type: extends
  target: K1238
  note: even-y統一テンプレートの第7データ点（偶数y族式〔z-odd I行k=floor((d+3y+2)/4)の連続整数th掃引23..45・base行同式floor((d+3y+1)/4)・偶z I行k=floor((d+3y-1)/4)・pin格子統一式o_pin=(d+3y)/2・pin行数(y+2)/2とy/2の同時11・単一band則2y+2..x+22・偶z対角値1欠如・tail x奇行〕のy=22でのfit level継続観測）。20→22は宣言c0baada6配下の事前登録どおり
- type: extends
  target: K1143
  note: 「pinスロット=th-1」（奇z I行）と偶z base行2k+1 slot則（y=11..21の11族連続に続き12族目として奇z 11 pin行・偶z 11 pin行すべてで算術的に成立〔2k(d)=o_pin(d)と2k(d)+1=o_pin(d)が全pin行で恒等的に成立〕）
- type: related
  target: K0915
  note: z=6,y=22証明済み切片（全称証明）との交差検証。宣言で補助的と事前登録し、実行では出版T_22(x)/P_22(x)表を監査生成器へ転写してprobe box内z=6切片（x=22..49・R<=x+52）全2,450点の三点照合（生probe値vs証明済み分類・cand22 vs証明済み分類）をfail-closed gateで実施しbad 0。ラダー{1,3,5}・pin(22,6)@47〔d=16〕・(26,6)@49〔d=20〕・掃引x=29の{51,53,55,57}・定常R=51〔=z+2y+1〕・tail R>=x+29→(x+22) mod 2が宣言予想・K0915出版表・生値で完全一致。転写トラップ（tail下端O[x+30,∞)を一時x+31と誤転写→境界点11点のみを検出）はfail-closed設計の作動実例として帳簿に記録（独立裏付け・fit当時はobserved・2レーンの相互補強の記録）
- type: depends_on
  target: K1257
  note: y=22全称検証機械（K1257・単一機体14チェック・総6,956,320照合点・全bad 0・4実行byte-identical〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種全捕捉・単一ホスト出版）が本項observed→proved昇格の全称証拠の正本
- type: generalizes
  target: K0999
  note: C1dアンカーA8uがz=8の出版一様閉形式（K0999）のy=22行で4方照合（anchor×H_ordered×H_canonical×cand22）bad 0（preflight 1,885点+機内掃引）。y=22全称はz=8則のy>=22行側を含む
- type: generalizes
  target: K1001
  note: C1dアンカーのz=9一様閉形式K1001のy=22行4方照合 bad 0（preflight 1,911点+当該分）
- type: generalizes
  target: K1011
  note: C1dアンカーのz=10一様閉形式K1011のy=22行4方照合 bad 0（preflight 1,937点+当該分）
- type: generalizes
  target: K1065
  note: C1dアンカーのz=15一様閉形式K1065のy=22行4方照合+低R単一トークン縮約 bad 0（preflight 2,067点+低R縮約のうち当該分）
- type: generalizes
  target: K1077
  note: C1dアンカーのz=16一様閉形式K1077のy=22行4方照合+低R縮約 bad 0（preflight 2,093点+当該分）
- type: generalizes
  target: K1087
  note: C1dアンカーのz=17一様閉形式K1087のy=22行4方照合+低R縮約 bad 0（preflight 2,119点+当該分）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（119,567 probe点一発一致・box内tail assertion 27,528点・box外spot 43,026点（全11奇z pin行・全11偶z pin行の個別行選択・6 box外pin行(41,23)/(37,23)/(33,23)/(42,22)/(38,22)/(34,22)のR<=130生値照合・全選択行にx>=22機械preflight assert）・merge回帰123行/19,449比較・tail raw 78点・K0915三点交差検証2,450点bad 0・事前横断予想の判定表（全18行一致・amendment不要）・誠実記録5点（宣言前deep smoke開示・sandboxリセットからの再構成・K0915転写トラップ・pinned秒数337.0・対抗宣言確認手段の限界）・y=12..y=22横断判定・宣言値のsha256ピン）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/cand22.py
  role: verifier
  note: 閉形式の正本cand22（in_T22値2表・in_P22値1表・Y=22・偶数y型で値1無限帯・tailはx奇行）とprobe全点照合（119,567点・mismatch 0・overlap 0・初稿一発一致）。出版cand20のY=20→22機械翻訳でコード本体は1行も変わっていない（逆rename byte同一を両方向で機械検証・translate_y22.py・結果docstring確定版に対しても本体検証再実行PASS）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/probe_y22.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=22..z+43・R<=x+z+46=2y+2拡張cap・1,147行119,567点を書き出す決定論的生成器・6回再生成byte-identical incl. 隔離tree+env -i+PYTHONHASHSEED=random・probe_rows.txt SHA-256 2380c951…）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/spot_y22.py
  role: verifier
  note: box外spot（全11奇z pin行・全11偶z pin行を個別行選択したdeep rows R<=130 46行・bigz z=31..40・x=y=22 edge・far d∈{44,55,66}・tail raw・merge回帰123行/19,449・LRU cap 1.5M決定的退避・3バッテリーで全ブロック集計とCacheInfo完全一致）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/make_audit_y22.py
  role: verifier
  note: 監査生成器（box幾何独立再計算ゲート（宣言機械事前算出1,147行/119,567点と厳密照合）・値ヒストグラム事前予想等価ゲート{0:58950,1:49478,2:11139}・逐行整合性ゲート・in-box tail depth 24点/行27,528点ゲート・in-box merge 0行ゲート・in-box pin格子観測ゲート〔8+8行・R=z+(d+66)/2〕・K0915出版T_22/P_22表転写によるz=6切片全2,450点三点照合fail-closedゲート・fail-closed・最終版3回実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/spot_chunk_rerun_y22.py
  role: verifier
  note: spot決定性再実行driver（sandboxの単一実行300秒上限と環境リセット下で、出版spot_y22.pyのmain()を一意マーカーでバイトスライスしdeep/bigz/edge/far/tailmergeの各ブロックをexec再実行。3バッテリーで全ブロック集計・LRU CacheInfo行が完全一致・pinned合計337.0秒）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/translate_y22.py
  role: verifier
  note: Y=20→22機械翻両方向検証器（翻訳生成と逆renameの出版cand20コード本体byte同一検証・docstring確定版に対する再検証含む）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/tamper_battery_y22.py
  role: verifier
  note: fail-closed改ざんバッテリ（20変種すべてcaught・leak 0・no-op 0・ANCHOR EFFECTIVENESS事前assert・復元byte検証・battery終了後のrestore再実行がaudit.json確定shaを再現）
- path: research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 fecfc248…15b905b・自己文書化・probe/spot/merge/tail数値・sha256ピン〔probe_rows 2380c951…・cand22 7a62577b…・probe_y22 b525e64b…・spot_y22 d176336b…・spot_chunk_rerun f697a1d6…〕・宣言commit c0baada6記録・K0915三点照合2,450点bad 0・両偶奇11 pin行とbox外pin 3+3の族初の記録）
- path: research/log/2026-11-23-y22-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit c0baada6・probe実行前に出版・事前横断予想の全記録・対抗宣言チェック・box幾何1,147行/119,567点・総比較点182,042の出版前機械算出・逆rename両方向検証の事前登録・宣言前deep smoke 1回の誠実開示・fetch-back byte検証 SHA-256 b552094d…d6cce）
- path: research/log/2026-11-23-two-token-y22-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・宣言・経緯・系列初一斉達成3件・誠実記録5点・出版記録〔Commit A 3b69574e・fetch-back byte検証〕・次段階〔y=22全称はB子cand21逐語＝系列初の全称確定済みB-child〕）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/README.md
  role: proof
  note: 全称段階の正本README（単一機体14チェック版の機械構成・転写marker検査・段階実行結果表・C4t tight（18族連続・歩み10観測目）・決定性4実行〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種全捕捉・宣言予想と実測の完全一致〔amendment不要〕・再現コマンド・昇格判定・解釈規約・単一ホスト出版の正直記録）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/verify_y22_universal.py
  role: verifier
  note: 正本検証器（単一機体14チェック版・53,422 bytes・SHA-256 96d9787fae441a39c1cf0475e446b9dfef9bcc8297818afc1bd82a9f3c19ec6b・@@TRANSCRIPTION marker 3ブロック〔engine 1,957 bytes・cand21 3,502 bytes二ソース・cand22 3,212 bytes〕・C1dアンカー前のpreflight fail-closedゲート設計）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/census_rows.py
  role: verifier
  note: census第三実装（XMIN=22・XMAX=70・ZHI=80・RBUF=24・LRU cap 1,600,000・433,160点・zero_points 216,626・misses 11,469,227・census.txt〔3,920行+80空行区切り・791,080 bytes・SHA-256 3275cc74…〕を生成。台帳bytesは本editionでは実験dirに同梱せず生成器+SHA pinで再現する体裁〔y=21 editionと同一〕）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/scripts/check_transcriptions_y22.py
  role: verifier
  note: 転写二重正本検証（engine 出版y21機〔blob ca5e8284〕から逐語・cand21 出版cand21.py〔git blob 38613e92〕と出版y21機ブロックの両方とY→Y21改名差分のみで一致・sources_agree・cand22 出版cand22.py〔git blob fd50358e〕逐語・repo rootはAGENTS.md探索）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/scripts/preflight_c1d_y22.py
  role: verifier
  note: C1d事前検証（出版6切片アンカー4方照合 12,012点+低R単一トークン縮約 9,108点・bad 0・anchor blockは出版y21 preflightからbyte-verbatim・JSON SHA-256 a65b967d…）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/audit.json
  role: data
  note: フル14チェック監査正本（SHA-256 41813df3…・total_points 6,956,320・total_bad 0・type_count 797,559・corollaries merge 887,200 / tail 191,158 全bad 0・verifier self-hash 96d9787f…）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/audit-part1-12checks.json
  role: data
  note: 段階実行12チェック電池の監査退避正本（SHA-256 1d434dbd…・total_points 5,664,680・total_bad 0・宣言の段階実行プロトコルの記録・型797,559）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/census-ordered.json
  role: data
  note: census ordered部（SHA-256 246506b2…・429,240点・bad 0・merge 78,750・tail 3,920）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/census-canonical.json
  role: data
  note: census canonical部（SHA-256 da0c20fc…・429,240点・bad 0・merge 78,750・tail 3,920）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/preflight-c1d-y22.json
  role: data
  note: C1d preflight結果正本（SHA-256 a65b967d…・12,012+9,108点bad 0・per z 1,885/1,911/1,937/2,067/2,093/2,119）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/transcriptions-check-y22.json
  role: data
  note: 転写検査結果（engine/cand21二ソース/cand22 全equal・overall PASS・SHA-256 7767d14c…）
- path: research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/output/published_run.txt
  role: log
  note: 正典run transcript（段階実行の全記録〔転写検査→preflight→census→12チェック→14チェック〕・rc=0・4回決定性〔3同一cwd+1隔離full-pipeline再生成〕・fail-closed 12種〔探針(9)初回no-opの正直記録を含む〕・宣言の事前予想と全照合点数の一致・出版SHA-256 pin一式）
- path: research/log/2026-11-23-y22-universal-verifier-single-owner-note.md
  role: log
  note: 全称段階の単一オーナー宣言ノート（commit e1e60cd4・機体実行前に出版・観測HEAD-before-push db195667・対抗宣言なしの確認記録・単一機体14チェック版の事前登録〔publish-then-execute〕・事前横断予想の機械算出〔出版y19/y20/y21の3audit 14点数ずつでcross-validated〕・K1257仮採番）
- path: research/log/2026-11-23-two-token-y22-universal-verifier.md
  role: log
  note: 全称段階の実行記録（単一実行の出版・宣言予想との完全一致・決定性・fail-closed 12種・K1256昇格判定・出版記録・単一ホスト出版の正直記録・次のレジューム）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,22)、全z>=0・全x>=22・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand22）で
  分類する命題。全称は正本検証器（K1257・単一機体14チェック版・
  フル14チェック監査・総6,956,320照合点・全bad 0・4実行byte-identical
  〔3同一cwd+1隔離のfull-pipeline完全再生成〕・fail-closed 12種全捕捉）
  で検証済み（2026-11-23出版・単一オーナー宣言e1e60cd4配下で
  observed→proved昇格）。系としてx<=z-23の単一トークン一致マージ命題
  y=22版とtail R>=x+z+23の(x+22) mod 2を含み、マージ命題はy=1..22で
  全称確定。2トークン族の全称はy=1..22で完結（y=22は全称確定済み範囲
  y<=21の外の最初の族）。標準11×11の空盤・二石root・S2 {59,60}・
  class 1/2/4は範囲外かつUNKNOWNのまま。3トークン以上・y>=23族・
  固定幅・q点版も範囲外。
evidence: >-
  fit段階の証拠（2026-11-23出版・単一オーナー宣言c0baada6配下）:
  probe box全点一発一致（119,567点・mismatch 0）・box内tail assertion
  27,528点・box外spot 43,026点・merge回帰123行/19,449比較・tail raw 78点・
  K0915交差検査2,450点・合計182,042点比較不一致0・seed法則10連続一発一致・
  probe 6回再生成byte-identical・audit 3回byte-identical・fail-closed電池
  20変種すべてcaught（本文「検証規模」「主結果」が詳細の正本）。
  全称段階の証拠（2026-11-23出版・単一オーナー宣言e1e60cd4配下・単一機体
  14チェック版でobserved→proved昇格）:
  転写二重正本検査（engine 1,957 bytes出版y21機〔blob ca5e8284〕から逐語・
  cand21 3,502 bytes 出版cand21.py〔git blob 38613e92〕と出版y21機ブロックの
  二系統byte一致・Y→Y21改名・両ソースbyte一致・cand22 3,212 bytes 出版
  cand22.py〔git blob fd50358e〕逐語・overall PASS・隔離側再生成一致）・
  C1d事前検証（出版6切片アンカー4方照合12,012点+低R縮約9,108点bad 0・
  anchor blockは出版y21 preflightからbyte-verbatim・組み込み前fail-closed
  ゲート・機内掃引134,550点〔125,442+9,108〕bad 0）・census第三実装
  （rows 3,920=80*49・points 433,160・zero_points 216,626・misses
  11,469,227・hits 22,466,349）をC11r（全行をcand22から再導出・行数斉一性・
  行重複/欠損FAIL-CLOSED）で消費しフル14チェック監査total 6,956,320点
  bad 0（型797,559・merge帰結887,200点〔729,700+2×78,750〕・tail帰結
  191,158点〔183,318+2×3,920〕・3同一cwd+隔離full-pipeline再生成1回で全出力
  byte-identical・audit.json SHA-256 41813df3…・census.txt 3275cc74…は
  本editionでは生成器+pinで再現）・段階12チェック電池の監査も別正本
  （total 5,664,680・bad 0・audit-part1-12checks.json 1d434dbd…）で保存・
  fail-closed 12種全捕捉（census欠落/行削除3,919!=3,920/重複行(0,22)の
  FAIL-CLOSED・P-set/T-set改ざん→C11r bad 1・C11r tail反転→bad 3,920〔全行・
  宣言予想どおりrows数〕・アンカー誤結合→C1d bad 14,869・lowR参照ずれR+1→
  bad 9,108〔全lowR点が独立に識別〕・merge境界z-23→z-22→merge bad 59〔初回
  探針はharnessのno-opとして正直記録し有効版で再検出〕・clip窓46,47→44,45→
  C4 bad 945・in_P22 tail偶奇反転→C1 bad 4,898/C2 bad 24,024・in_P22 band
  偶奇改ざん→C1 bad 1,763/C2 bad 24,451・12種すべてrc=1・スクラッチtreeで実施
  ・正典treeは無傷）・C4t clip 45違反280点・最初(60,108,108)で clip 2y+2=46
  はtight（18族連続y=5..22・最初違反はband下端と歩む系列の10観測目）。
  宣言の事前機械算出予想（predict_y22_counts.py・出版y19/y20/y21の3audit
  の14点数ずつを完全一致で再現してcross-validated・数値はstdoutから機械
  転写）は全項目で実測と完全一致（amendmentなし・散文内転置なし）。
  誠実記録: 本全称段階は単一ホストでの出版であり（4実行byte-identical・
  隔離ゼロ再生成込み）、y=21 editionのような兄弟実行による独立ビルド・
  第二ホスト再現は出版時点でまだ存在しない。独立再現は次回実行の裏付け
  課題として本itemとrun logに明記する。
---

# K1256: 2トークン残余ゲーム y=22族のパラメトリック閉形式の全称証明（observed→proved・2026-11-23）

## 命題・範囲

すべての z>=0・x>=22・R>=0 に対して H(R;(x,22);z) = cand22 が成り立つ
（**status: proved・2026-11-23 単一機体14チェック全称検証の出版で
observed→proved 昇格**・全称段階の正本は
[全称検証実験dir](../../experiments/vertical-fiber-two-token-y22-universal-proof-20261123/README.md)）。
ここで cand22 は z 偶奇別のパラメトリック T/P 集合表（fit実験dirの
`cand22.py` が正本・Y=22・偶数 y 型で値1無限帯・tail は x 奇行・
d = x-z・off = R-z）であり、出版 cand20（K1246 proved）の Y=20→22
機械翻訳に等しい（コード本体 1 行も変わらず・逆 rename byte 同一を
両方向で機械検証済み・translate_y22.py）。

fit段階の正本は
[fit実験dir](../../experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/report.md)
で、fit段階の証拠は下記「検証規模」の合計 182,042 点比較・不一致 0 である。

## fit段階の記録（宣言 c0baada6 配下・publish-then-execute）

- **初稿一発一致**: probe 119,567 点 mismatch 0・T/P overlap 0・値ヒストグラム
  0:58,950/1:49,478/2:11,139 が宣言の事前機械予想と厳密一致・値 3 なし。
  seed 法則 10 連続（偶数 y 6 連続）・証明済み seed 外挿 4 連続。
- **系列初一斉達成 3 件**: ①両偶奇同時 11 pin 行（初）②box 外 pin 各偶奇 3 行・
  合計 6 行（系列最多）③23 行 th 連続整数掃引 23..45（初）。
  いずれも偶数 y 族式（y=10,12,…,22）からの外挿どおりで、宣言で事前登録された。
- **K0915 証明済み z=6,y=22 切片との三点照合**（補助・宣言電池外）: 全 2,450 点 bad 0。
  指摘対象となる転写ミス（tail 下端 x+30→x+31）は境界点 11 点のみで fail-close 検出。
- **マージ回帰**: cand22 == single_token(x+22,R)（K0832）を box 外 123 行 19,449 比較 bad 0。
  y=22 は box 内マージ行 0 行（z>=46 必要）が 8 族連続。
- **決定性・fail-closed**: probe 6 回再生 byte 同一・audit 3 回 byte 同一・
  spot 3 バッテリー全統計一致・改ざん 20 変種すべて caught（no-op 0・leak 0・
  anchor 実効性事前 assert・復元 byte 検証）。

## 検証規模（宣言電池合計 182,042 点・bad 0）

| 検査 | 規模 | bad |
|---|---:|---:|
| probe box（1,147 行）全点照合 | 119,567 点 | 0 |
| box 内 tail assertion（24 点深/行） | 27,528 点 | 0 |
| spot deep 46 行 R<=130 | 5,980 点 | 0 |
| spot bigz 240 行 | 30,240 点 | 0 |
| spot x=y=22 edge 25 行 | 4,100 点 | 0 |
| spot far 18 行 | 2,628 点 | 0 |
| tail raw | 78 点 | 0 |
| merge 回帰 vs K0832 | 19,449 比較 | 0 |
| K0915 z=6 三点照合（補助・電池外） | 2,450 点 | 0 |

## 誠実記録

帳簿づけ 5 点（宣言前 deep smoke 1 回の開示・sandbox リセットからの出版参照による再構成
〔再生成 probe の byte 同一再現で検証〕・K0915 転写トラップ・pinned 秒数 337.0・
対抗宣言確認手段の限界）の正本は report.md・fit log に同じ。

## 範囲外の維持

標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は UNKNOWN のまま。
3 トークン以上・y>=23 族・固定幅・q点版は範囲外。 y=22 の全称（A子/B子cand21逐語
〔系列初の全称確定済み B-child〕/C子・clip 窓 2y+2=46 tight 判定）は本項の昇格条件であり
別宣言とされた。**2026-11-23、その別宣言（単一オーナー宣言 e1e60cd4）配下で
単一機体14チェック検証器（K1257）が実行・出版され、全条件を満たして本項は
observed→proved に昇格した**（詳細は下記「全称段階の記録」）。
y=23 fit の seed は cand21（K1248 proved）。

## 全称段階の記録（単一機体14チェック版・observed→proved・2026-11-23）

単一オーナー宣言 e1e60cd4（検証器実行前に出版・観測 HEAD-before-push db195667・
対抗宣言なしを確認）配下で、y=21 出版手続き（K1255・単一機体単一出版）を y=22
定数に適合した単一機体14チェック版として実施した（宣言で事前登録・段階実行:
転写検査→preflight→census→12チェック電池→フル14チェック・12チェック電池の
監査は audit-part1-12checks.json として別正本保存）:

- **機体**: 単一機体14チェック版 verify_y22_universal.py（53,422 bytes・
  SHA-256 96d9787f…・C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12）。
  転写3ブロック（engine 1,957 bytes〔出版y21機 blob ca5e8284 から逐語〕・
  cand21 3,502 bytes〔出版cand21.py〔git blob 38613e92〕と出版y21機ブロックの
  二系統 byte-equality・Y→Y21 改名・sources_agree〕・cand22 3,212 bytes〔出版
  cand22.py〔git blob fd50358e〕から逐語〕）を check_transcriptions_y22.py
  が検査 PASS（cand21 は二ソース一致・隔離側でも再生成一致）。
  A子 x==22 行は合流子 {21,22}≡{22,21} で cand21(z,22,R-1)〔y=21族x=22行と
  同一状態〕・B子 出版 cand21 逐語転写〔x>=22 行は定義域 x>=21 の内側・
  **系列初の全称確定済み B-child**〕・C子 1 xor cand22(z-1,x,R-1)・
  型機械 clip 2y+2=46・番兵 47。
- **C1d 事前検証**: preflight_c1d_y22.py（anchor block は出版 y21 preflight
  から byte-verbatim）が出版6切片アンカー（K0999/K1001/K1011/K1065/
  K1077/K1087・z0∈{8,9,10,15,16,17}）を y=22 行で4方照合:
  **12,012点 bad 0**（per z 1,885/1,911/1,937/2,067/2,093/2,119）+
  低R単一トークン縮約 R<=z+6: **9,108点 bad 0**・JSON 正本 a65b967d…。
  機内 C1d 掃引（アンカー掃引 125,442 + lowR 9,108）は **134,550点 bad 0**。
- **census第三実装**: census_rows.py（XMIN=22・XMAX=70・ZHI=80・RBUF=24・
  LRU cap 1,600,000・約65秒）が census.txt（791,080 bytes・3,920行+80空行
  区切り・SHA-256 3275cc74…・台帳は生成器+SHA pinで再現〔実験dirに同梱せず・
  y21 edition体裁〕）を生成し、C11r（rows==80*49=3,920・全行を cand22 の
  T/P集合・Thue-Morse index・tail から再導出）が **433,160点 bad 0**
  （zero_points 216,626・misses 11,469,227・hits 22,466,349）。
  census部品（C11ordered/C11canonical・bounded-memoization twin・LRU 1.6M）は
  各engine **429,240点 bad 0**・merge帰結各 78,750・tail各 3,920 bad 0
  （census幾何では z>=45 で初めて非空）。
- **段階12チェック電池**（part1相当）: **overall PASS・総5,664,680点・全bad 0・
  型797,559**（C1 26,220 / C1b 46,220 / C1d 134,550 / C2 242,305 / C2b 19,844 /
  C3 1,425 / C4 562,559 / C4t 562,559〔probe〕 / C7 200,000 / C8 1,122,279 /
  C9 889,974 / C12 1,856,745）・audit-part1-12checks.json（SHA-256 1d434dbd…）
  に退避。
- **フル14チェック監査**: **overall PASS・総照合点 6,956,320**（12チェック電池
  5,664,680 + C11 858,480 + C11r 433,160）・**全bad 0・型797,559**（系列:
  y=17 457,645 → y=18 523,398 → y=19 590,877 → y=20 658,978 → y=21 727,229 →
  y=22 797,559）・audit.json（SHA-256 41813df3…・verifier self-hash
  96d9787f…）が正本。merge帰結 **887,200点 bad 0**
  （x<=z-23 => H == single_token(x+22,z,R)・呼び出し点 729,700 +
  両census engine 2×78,750）・tail帰結 **191,158点 bad 0**
  （R>=x+z+23 => (x+22) mod 2）。
- **C4t**: clip 45（2y+1）違反**280点・最初 (60,108,108)** → clip窓 2y+2=46 は
  **tight・18族連続確定**（y=5..22: 12/14/…/44/46）・最初違反は band下端
  R-z=2y+2=46 とともに歩む系列の**10観測目**
  （(60,90,90)→(60,92,92)→…→(60,106,106)→(60,108,108)・宣言の事前予想
  〔違反>0・(60,108,108)〕と完全一致）。C4 in-box 登録型数は clip 46/番兵 47
  で **448,494**（y=21 機の clip 44 で 429,397 を更新）。
- **決定性・fail-closed**: 4実行 byte-identical（同一cwd 3回 + 隔離
  tree/cwd/HOME+env -i+PYTHONHASHSEED=random 1回〔隔離側は転写検査・preflight・
  census_rows・census両部・12チェック・フル14チェックの完全ゼロ再生成・
  census engine states まで同一: misses 11,469,227 / hits 22,466,349〕）。
  fail-closed 12種全捕捉（census.txt 欠落/行削除 3,919 != 3,920/重複行 (0,22)
  のFAIL-CLOSED・P-set/T-set改ざん→C11r bad 1・C11r tail反転 (x+22)→(x+23)→
  bad 3,920〔全行・宣言の予想どおりrows数〕・アンカー誤結合 (17,A17u)→(17,A10u)
  →C1d bad 14,869・lowR参照ずれ R+1→bad 9,108〔全lowR点が独立に識別〕・merge
  境界 z-23→z-22→merge bad 59〔初回の探針はharnessのno-op（編集不発効）として
  正直記録し有効版で即再検出〕・clip窓 46,47→44,45→C4 bad 945・in_P22 tail
  偶奇反転（x%2==1→==0）→C1 bad 4,898/C2 bad 24,024・in_P22 band偶奇改ざん
  （off%2==0→==1）→C1 bad 1,763/C2 bad 24,451。12種すべてrc=1・スクラッチtree
  で実施・probe後にbaselineをbuild bytesとcmp検証・正典treeは無傷）。
- **宣言予想との完全一致**: 宣言ノートの事前機械算出（出版y19/y20/y21の3機体
  auditの14点数ずつを完全一致で再現して cross-validated・数値は
  predict_y22_counts.py stdoutから機械転写）は、preflight 12,012+9,108・
  C1d 134,550・census幾何全値（3,920行・429,240/engine・merge 78,750・
  tail 3,920）・C11r 433,160・12チェック電池 5,664,680・総点 6,956,320・merge帰結 887,200・tail帰結 191,158・C4t
  （違反>0・最初違反 (60,108,108)）・C11r tail反転 bad 3,920 の**すべてが
  実測と完全一致**（全段階無修正・amendmentなし・散文内転置なし）。
- **系の確定**: 2トークン族の全称は **y=1..22 で完結**（y=1..12 は旧来の単族
  証明・y=13..22 は機械検証の逐語連鎖）。マージ命題
  x<=z-23 => H == single_token(x+22,z,R) は y=1..22 で全称。tail
  R>=x+z+23 => (x+22) mod 2。clip窓 2y+2 は y=5..22 の 18 族連続で tight。
  B子逐語連鎖 cand9..cand21（証明済みB子使用は cand10/cand12..cand21）、
  機体 item は K1257（proposition は本項）。**y=22 は全称確定済み範囲
  （y<=21）の外の最初の族**である。
- **単一ホスト出版の正直記録**: y=21 edition と異なり、出版時点で兄弟実行に
  よる独立ビルド・第二ホスト再現はまだない。単一ホストでの4実行
  byte-identical（隔離ゼロ再生成込み）と fail-closed 電池が昇格の根拠であり、
  独立再現は次回実行の裏付け課題として run log に明記する。
- **範囲外の維持**: 標準 11×11 の空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は UNKNOWN のまま。3トークン以上・y>=23 族・固定幅・q点版は
  範囲外。
