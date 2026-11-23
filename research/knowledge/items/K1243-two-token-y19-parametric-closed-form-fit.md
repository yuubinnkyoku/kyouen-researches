---
id: K1243
title: "2トークン残余ゲーム y=19族のパラメトリック閉形式の全称証明（全z>=0・全x>=19・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=19 parametric closed-form fit, P19-fit"
  - "cand19 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 99,107 probe points; odd-y mechanical translation from the published FINAL cand17, the promoted-universal y=17 table with Y=17->19)"
  - "seed law 7th consecutive one-shot test passed (cand11->13 / cand12->14 / cand13->15 / cand14->16 / cand15->17 / cand16->18 / cand17->19, odd-y pair series 11->13->15->17->19 all 4); FIRST family with 10 pin rows (odd z, (y+1)/2=10); most out-of-box pin rows in the series (3 rows, first family with 2 on a single parity side); 5th consecutive family with zero in-box merge rows; declaration z-even base row-range bookkeeping corrected by the fit census (actual: 19 rows d in [-17,19] with the top d=19 saturating k=Y, same three-k=Y-row pattern as y=17) -- amendment published, formulas unchanged (zero corrections)"
  - "universal proof completed (2026-11-23, single-edition 14-check machine under single-owner declaration da6c1f5f): observed -> proved via the 14-check canonical audit at 6,941,913 comparison points bad 0, C1d published-slice anchors preflighted 4-way (12,069+9,306 pts), census_rows.py third implementation consumed by C11r (440,960 pts); clip window 2y+2=40 tight (15-family streak y=5..19, 7th walking first-violation (60,102,102)); merge proposition now universal through y=1..19"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰16,665比較・境界行(41,21)/(40,20)のspot照合に使用。y=19ではbox内マージ行0行・z>=39が必要）
- type: extends
  target: K1240
  note: y=17族閉形式（K1240・part2昇格によりobserved→proved済み）の次の奇数y族。cand19初稿はy=17出版最終構造cand17（全称証明済み）のY+2機械翻訳（Y定数17→19・関数名変更のみ・コード本体は全式Y式で1行も変わらず）で生成し、probe 99,107点に一発一致（cand15→17に続き奇数y seed法則4連続目・全体で7連続一発一致）
- type: extends
  target: K1242
  note: 隣接偶数y族（y=18 fit・K1242は全称証明済み）。y=19全称検証器のB子は出版cand17→cand18の逐語転写連鎖の続きとして出版cand18（K1242 proved）の逐語転写（x=19合流子{18,19}≡{19,18}）。B子逐語連鎖は本項の昇格でcand9..cand18に拡大・証明済みB子使用はcand10/cand12..cand18。マージ命題は本項でy=1..19に全称拡大
- type: extends
  target: K1241
  note: y=17全称検証part1（型機械・census・二重正本転写検査の枠組み）のy=19版の前段fit。y=19全称段階は宣言da6c1f5fで事前登録された単一機体14チェック版変形（part1/part2分割でなく、機体を最初から14チェック版として構築し段階実行）として実行・出版済み（正本監査はK1245）
- type: extends
  target: K1143
  note: y=11族の行型比較基点（「pinスロット=th-1」と偶z 2k+1 slot則がy=11..19の9族連続候補として確定・y=19は奇z pin行が10行に達する初の族で両偶奇とも最大行数の判定点）
- type: depends_on
  target: K1245
  note: y=19全称検証機械（K1245・単一機体14チェック・総6,941,913照合点・全bad 0・4実行byte-identical・fail-closed 12種全捕捉）が本項observed→proved昇格の全称証拠の正本
- type: generalizes
  target: K0999
  note: C1dアンカーA8u..A17uが固定z切片の出版一様閉形式をy=19行で4方照合（anchor×H_ordered×H_canonical×cand19）。z=8: K0999、preflight・機内掃引ともbad 0。y=19全称はz=8則のy>=19行側を含む
- type: generalizes
  target: K1001
  note: C1dアンカーのz=9一様閉形式K1001のy=19行4方照合 bad 0
- type: generalizes
  target: K1011
  note: C1dアンカーのz=10一様閉形式K1011のy=19行4方照合 bad 0
- type: generalizes
  target: K1065
  note: C1dアンカーのz=15一様閉形式K1065のy=19行4方照合+低R単一トークン縮約 bad 0（preflight 2,079点+低R縮約のうち当該分）
- type: generalizes
  target: K1077
  note: C1dアンカーのz=16一様閉形式K1077のy=19行4方照合+低R縮約 bad 0（preflight 2,106点+当該分）
- type: generalizes
  target: K1087
  note: C1dアンカーのz=17一様閉形式K1087のy=19行4方照合+低R縮約 bad 0（preflight 2,133点+当該分・y=10段階でK1087初稿の評価順序バグ170点を捕捉した事前検証段階のy=19版は初回から全一致）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（99,107 probe点一発一致・box内tail assertion 22,134点・box外spot 44,597点（全選択行にx>=19機械preflight assert・3 box外pin行(37,20)/(33,20)/(34,19)の生値照合）・merge回帰16,665比較・tail raw 78点・事前予想の判定表・y=12..19横断則・fail-closed 10種10/10（キャッシュ衛生を最初から適用））
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-fit-20261123/cand19.py
  role: verifier
  note: 閉形式の正本cand19（in_T19値2表・in_P19値1表・Y=19・Y==19ハードassert）とprobe全点照合（99,107点・mismatch 0・overlap 0・初稿一発一致）。全称検証器は本ファイルを逐語転写
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-fit-20261123/probe_y19.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=19..z+37・R<=x+z+40=2y+2・1,054行99,107点を書き出す決定論的生成器・約9.6秒）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-fit-20261123/spot_y19.py
  role: verifier
  note: box外spot（全10奇z pin行・全9偶z pin行を個別行選択したdeep rows R<=130・bigz z=31..40・x=y=19 edge・far d∈{38,49,60}・tail raw・merge回帰16,665・LRU cap 1.5M決定的退避・230.0秒〔正本docstring修正後の再実行・bad 0〕）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-fit-20261123/make_audit_y19.py
  role: verifier
  note: 監査生成器（pin格子観測ゲート〔box内可観測8+8行〕・box幾何独立再計算ゲート・逐行整合性ゲート〔x>=19・d再計算・merge flag・RLE長x+z+40〕・in-box tail assertion・in-box merge 0行ゲート・偶z対角値1 census・fail-closed・3実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 a1ddd7f1…65b14・自己文書化・probe/spot/merge/tail数値・sha256ピン〔probe_rows 2a57d075…〕・宣言commit c15b1c3f記録・3 box外pin行と1側2行の族初の誠実記録）
- path: research/log/2026-11-23-y19-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit c15b1c3f・probe実行前に出版・事前横断予想の全記録・対抗宣言チェック・box内マージ行0行と3 box外pin行の事前明記・宣言点数99,107は出版前に機械算出）
- path: research/log/2026-11-23-two-token-y19-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・宣言・経緯・出版記録・次段階）
- path: research/log/2026-11-23-y19-decl-z-even-base-bookkeeping-amendment.md
  role: log
  note: 宣言ノート（c15b1c3f）の偶z base 行域記述（17行・[-17,17]・上端非飽和・2箇所k=Y族初）を行域算術の誤りとして訂正するamendmentノート（実態: 19行・[-17,19]・上端 d=Y 飽和・3行 k=Y は y=17 と同型。族式・閉形式は影響なし・probe 修正0のまま）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/README.md
  role: proof
  note: 全称検証実験README（単一機体14チェック版・C1d事前検証12,069+9,306点・census_rows.py 4,160行/440,960点・C11r 440,960点・フル14チェック監査総6,941,913点bad 0・決定性4実行・fail-closed 12種全捕捉・宣言予想との完全一致の記録・昇格判定）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/verify_y19_universal.py
  role: verifier
  note: 全称検証器正本（単一機体14チェック版・52,631 bytes・SHA-256 76525717…・@@TRANSCRIPTION marker 3ブロック〔engine出版y18機part2 d29acbd8/8ddd0c2f…から逐語・cand18二ソースY→Y18改名・cand19出版cand19.py eaea0f6aから逐語〕）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/audit.json
  role: data
  note: フル14チェック監査正本（SHA-256 59b6fded…・total_points 6,941,913・total_bad 0・type_count 590,877・4実行byte-identical・corollaries merge 1,062,109 / tail 192,520 全bad 0）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/audit-part1-12checks.json
  role: data
  note: 段階実行12チェック電池の監査退避正本（SHA-256 63617241…・total_points 5,627,353・total_bad 0・宣言の段階実行プロトコルの記録）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/census_rows.py
  role: verifier
  note: census第三実装（SHA-256 e4eed396…・XMIN=19・XMAX=70・RBUF=21・ZHI=80・440,960点・zero_points 219,556・misses 9,806,027・約21秒・census.txt 4,160行を生成）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/census.txt
  role: data
  note: census行台帳正本（809,842 bytes・SHA-256 07213ab1…・C11rが全行をcand19から再導出し440,960点bad 0）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/scripts/preflight_c1d_y19.py
  role: verifier
  note: C1d事前検証（SHA-256 9bc154ee…・出版6切片アンカー4方照合12,069点+低R単一トークン縮約9,306点・bad 0・組み込み前fail-closedゲート・anchor blockは出版y18 preflightからbyte-verbatim・JSON SHA-256 1cfabdcf…）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/scripts/check_transcriptions_y19.py
  role: verifier
  note: 転写二重正本検証（engine 1,957 bytes出版y18機から逐語・cand18 3,307 bytes二ソース一致〔出版y18機ブロックと出版cand18.pyの両方とY→Y18改名差分のみで一致〕・cand19 3,411 bytes出版cand19.py逐語・repo rootはAGENTS.md探索・SHA-256 56a999bd…）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/census-ordered.json
  role: data
  note: census ordered部（SHA-256 df767357…・436,800点・bad 0・merge 102,459・tail 4,160）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/census-canonical.json
  role: data
  note: census canonical部（SHA-256 afdf9e60…・436,800点・bad 0・merge 102,459・tail 4,160）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/preflight-c1d-y19.json
  role: data
  note: C1d preflight結果正本（SHA-256 1cfabdcf…・12,069+9,306点bad 0・per z 1,890/1,917/1,944/2,079/2,106/2,133）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/transcriptions-check-y19.json
  role: data
  note: 転写検査結果（engine/cand18二ソース/cand19 全equal・overall PASS・隔離側でも再実行PASS・SHA-256 8a68ecb4…）
- path: research/experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/output/published_run.txt
  role: log
  note: 正典run transcript（段階実行の全記録・転写検査→preflight→census→12チェック→14チェック・決定性4実行・fail-closed 12種・rc=0）
- path: research/log/2026-11-23-y19-universal-verifier-single-owner-note.md
  role: log
  note: 全称段階の単一オーナー宣言ノート（commit da6c1f5f・観測HEAD 6f5419b5・機体実行前に出版・単一機体14チェック版の事前登録・全照合点数の機械算出予想〔出版y18 audit 14/14でcross-validated〕・対抗宣言なしの確認記録・K1245仮採番）
- path: research/log/2026-11-23-two-token-y19-universal-verifier.md
  role: log
  note: 全称段階の実行記録（機体ビルド・段階実行・宣言予想との完全一致・決定性・fail-closed 12種・K1243昇格判定・出版記録・次のレジューム）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,19)、全z>=0・全x>=19・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand19）で
  分類する命題。全称は正本検証器（K1245・単一機体14チェック版・
  フル14チェック監査・総6,941,913照合点・全bad 0・4実行byte-identical・
  fail-closed 12種全捕捉）で検証済み（2026-11-23出版・単一オーナー宣言
  da6c1f5f 配下でobserved→proved昇格）。系としてx<=z-20の単一トークン
  一致マージ命題y=19版とtail R>=x+z+20の(x+19) mod 2を含み、
  マージ命題はy=1..19で全称確定。標準11×11の空盤・二石root・
  S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNのまま。3トークン以上・
  y>=20族・固定幅・q点版も範囲外。
evidence: >-
  fit段階の証拠（2026-11-23出版・単一オーナー宣言 c15b1c3f 配下）:
  (1) 初稿一発一致: cand19初稿は出版cand17（K1240全称・Y=17）のY+2機械翻訳で、
  probe box全点に修正0（mismatch 0・overlap 0・値頻度 0:48,800 / 1:39,981 /
  2:10,326・値3なし）。seed法則7連続目（奇数y系列4連続目）。
  (2) 構造則の確定: 基底点19点{z+1,..,z+37}・奇z I帯k=floor((d+3y+1)/4)
  th=2k+1ペア反復19,21,21,...,39・同式base行奇z/偶z共通・偶z I帯
  k=floor((d+3y-1)/4)（8族目候補）・pin格子統一式pin=z+(d+57)/2
  （奇z 10行d≡3 (mod 4) {-17,...,19}・**pin行が10行に達する初の族**・
  偶z 9行d≡1 (mod 4) {-15,...,17}・「pinスロット=th-1」/偶z 2k+1 slotが
  9族連続候補・最終pin行d=19=yのI[2y+z+1)=I[39)型14族目候補・
  **box外pin行3行は系列最多で奇z d=-17/d=-13の同一偶奇側2行は族初**
  〔spot deep row (37,20)/(33,20)/(34,19)生値照合に事前委任〕）・
  **k=Y は 3 行で到達**（奇z base d=18・奇z 最終 I 行 d=19・偶z base 上端 d=19。
  出版 y=17 の 3 行〔d=16/d=17/d=17〕と同型・奇z base 上端飽和は 6 族連続候補）・
  偶z base 行は **d 奇 19 行・d∈[-17,19]** で上端 d=19=Y が k=Y 飽和
  （y=17 の d=17・y=18 の d=18 と同型の族式どおり。d=17 の k=18 非飽和は行域途中の正しい観察。
  **宣言ノートの偶z base 行域記述〔17行・[-17,17]・上端非飽和〕は行域算術の誤りで fit の機械 census が訂正**
  〔amendment 出版・行クラス z偶 d=19 は probe box 内と spot bigz d=19 行で生値検証済み〕。
  宣言の族式そのものは修正 0 で正しかった）・対角cap z+18(奇z)/z+19(偶z)・
  偶z対角値1全欠如12族目候補・掃引d=20・定常pin z+38/z+39・band下端
  2y+2=40・**奇数y族band_base/band_int分離則**（base行[40,x+19]/I行
  [40,x+18]）・tail開始x+z+20値(x+19) mod 2。
  (3) 回帰: マージ命題y=19版（K0832単一トークン）16,665比較不一致0・境界行
  (41,21)/(40,20)の生値一致・tail raw 78点一致。合計160,447点比較・不一致0。
  (4) 決定性・fail-closed: probe_rows.txt 4回再生成（同一cwd3回+隔離
  tree/cwd/HOME+env -i+PYTHONHASHSEED=random1回）byte-identical
  （SHA-256 2a57d075…855a8）・audit.json 4実行byte-identical
  （a1ddd7f1…65b14・4実行: 同一cwd 3回+隔離env -i 1回）・fail-closed 10種全捕捉（probe値改ざん・pin値改ざん・
  Y定数改ざん19→18〔Y==19ハードassert〕・pin mod4クラス改ざん〔監査が
  欠落7行を列挙〕・probe行欠落（幾何ゲート）・重複行注入（幾何ゲート）・
  meta d改ざん・merge flag改ざん・band下端改ざん〔band_base 2*Y+2→2*Y+4・mm=264〕・RLE長改ざん
  〔逐行整合性ゲート〕・復元byte-identical・clean control rc=0・
  **キャッシュ衛生（__pycache__ purge+-B+PYTHONDONTWRITEBYTECODE）を
  最初から適用**してy18のstale-pyc検出漏れ事故は不発生・10/10確定）。
  全称段階の証拠（2026-11-23出版・単一オーナー宣言 da6c1f5f 配下・単一機体14チェック版で
  observed→proved昇格）:
  転写二重正本検証（engine 1,957 bytes出版y18機part2〔d29acbd8・8ddd0c2f…〕
  から逐語・cand18 3,307 bytes二ソース一致〔出版y18機ブロックと出版
  cand18.pyの両方とY→Y18改名差分のみで一致・sources_agree〕・cand19
  3,411 bytes出版cand19.py逐語・overall PASS・隔離側再生成一致）・
  C1d事前検証（出版6切片アンカー4方照合12,069点+低R縮約9,306点
  bad 0・anchor blockは出版y18 preflightからbyte-verbatim・組み込み前
  fail-closedゲート）・census第三実装（rows 4,160・points 440,960・
  zero_points 219,556・misses 9,806,027・約21秒・tail assert全行成立）を
  C11r（rows==80*52=4,160・values range(0,x+z+21)・tail (x+19)%2）で消費し
  フル14チェック監査 total 6,941,913点 bad 0（型590,877・merge帰結
  1,062,109点・tail帰結 192,520点・run1/run2同一cwd
  +隔離側2回〔うち1回は全pipelineゼロ再生成〕で全出力byte-identical・
  audit.json SHA-256 59b6fded…）・段階12チェック電池の監査も別正本
  （total 5,627,353・bad 0・audit-part1-12checks.json 63617241…）で保存・
  fail-closed 12種全捕捉（census.txt欠落/行削除/重複行のFAIL-CLOSED・
  P-set/T-set改ざん→C11r bad 1・C11r tail反転→bad 4,160・アンカー誤結合
  →C1d bad 1,743・lowR参照ずれR+1→bad 9,306・merge境界z-19→merge bad>0・
  clip窓38,39→C4 bad 2,520・in_P19 tail偶奇→C1 bad 2,449・band_base偶奇
  →C1 bad 935）。C4t clip 39違反は770点 (60,102,102) で全bad 0かつ
  tail/merge検査で裏付けられtight判定確定（15族連続 y=5..19・最初違反は
  band下端と歩む系列の7観測目）。宣言の事前機械算出予想（出版y18 audit
  14/14でcross-validated）は全項目で実測と完全一致・amendment不用。
---

## 命題・範囲

すべての z>=0・x>=19・R>=0 に対して H(R;(x,19);z) = cand19(z,x,R) が成り立つ
（**status: proved・2026-11-23 単一機体14チェック全称検証の出版で
observed→proved 昇格**）。全称段階の正本は
[全称検証実験dir](../../experiments/vertical-fiber-two-token-y19-parametric-allz-proof-20261123/README.md)。
fit段階の正本は
[fit実験dir](../../experiments/vertical-fiber-two-token-y19-parametric-allz-fit-20261123/report.md)
で、cand19.py が閉形式の正本実装である。fit段階の証拠は
(1) probe box（z=0..30・x=19..z+37・R<=x+z+40）生二重再帰 1,054 行 99,107 点の
全点一致（初稿一発・修正 0・T/P 重複 0）、(2) box 内 tail assertion
R>=x+z+20 → (x+19) mod 2 の 22,134 点一致、(3) box 外 spot 44,597 点
（全 10 奇z pin 行・全 9 偶z pin 行を個別行として選択した deep rows・
bigz z=31..40・x=y=19 edge・far d∈{38,49,60}）、(4) merge 回帰 16,665 比較
（K0832 単一トークン閉形式）+ 境界行 (41,21)/(40,20) の生値一致、
(5) tail raw 78 点、の計 160,447 点比較不一致 0 である。

## 主要構造（fit で確定した構造則・有限範囲）

y=19 は奇数 y 族（y=9..17 と同型）で、値1無限帯・tail は x 偶の行。
基底点 19 点 {z+1,...,z+37}・マージ行 x<=z-20（box 内 0 行・5 族連続）・
奇z I 帯行 k(d)=floor((d+58)/4)・th=2k+1 ペア反復 19,21,21,...,39
（奇数 y 族型・偶数 y 族の連続整数掃引との偶奇分離の継続）・
偶z I 帯行 k=floor((d+56)/4)（8 族目候補）・base 行 k=floor((d+58)/4)
（奇z/偶z 共通・奇数 y 族式）・pin 格子統一式 pin=z+(d+57)/2
（o_pin∈[20,38]・奇z 10 行 d≡3 (mod 4) {-17,...,19}・**pin 行が 10 行に
達する初の族**・偶z 9 行 d≡1 (mod 4) {-15,...,17}・
「pin スロット = th-1」/偶z 2k+1 slot 9 族目・最終 pin 行 d=19=y の
I[2y+z+1)=I[39) 型 14 族目候補・**box 外 pin 行 3 行は系列最多で奇z
d=-17/d=-13 の同一偶奇側 2 行は族初**）・掃引行 d=20・定常 pin z+38（奇z）/
z+39（偶z）・band 下端 2y+2=40・**奇数 y 族 band_base/band_int 分離則**
（定常 base 行 [40,x+19]・定常 I 行 [40,x+18]・偶数 y 単一 band 則との
偶奇分離）・tail 開始 x+z+20・tail 値 (x+19) mod 2・偶z 対角行 d=-19 の
値 1 全欠如（12 族目候補）・対角 cap z+18(奇z)/z+19(偶z)（奇 y 族式の向き・
偶 y 族と逆向き）。**k=Y は 3 行で到達**（奇z base d=18・奇z 最終 I 行 d=19・
偶z base 上端 d=19 = Y の飽和・偶z base 行は d 奇 19 行 d∈[-17,19]・
出版 y=17 の 3 行 k=Y と同型の族パターン。奇z base 上端飽和は y=14..19 の
6 族連続候補）。d=17（偶z base・k=18）は行域途中の非飽和行。
標準の信頼境界（選択肢分解・mex 恒等式・有限型空間）は y=5..17 出版系列と
同一の機械分類に依存し、全称段階で初めて検証される。

## fit の工芸的観察（fitting なしの一発一致）

**初稿一発一致（修正 0）**: cand19 初稿は y=17 の出版最終構造（cand17・K1240
全称昇格済み）を seed とした Y+2 機械翻訳（Y 定数の差し替えと関数名変更のみ・
コード本体は全式 Y 式で 1 行も不変）で、probe 99,107 点に修正 0 で一致。
「直前の出版最終構造 seed による外挿が一発一致する」は **7 連続**
（cand11→13・cand13→15・cand15→17・cand17→19〔奇・奇数 y 系列 4 連続〕・
cand12→14・cand14→16・cand16→18〔偶〕）となり、横断法則一般補題化レーンの
主要リスク（族式の y 依存跳躍）をさらに低減した。y=16/17/18 に続き
5 族連続の「box 内マージ行 0 行」族でもあり、事前宣言どおりマージ回帰は
全面 box 外。宣言ノートの点数 99,107 は出版前に機械算出して記載したため
amendment 不用（y=17 の点数算術誤り訂正 82653b6f の教訓を適用）。
R cap は x+z+40 = 2y+2 に拡張した（band 下端 2y+2 の直接 box 内観測・
7 データ点目）。

## 誠実記録（3 box 外 pin 行と検証インフラ）

(0) **宣言の偶z base 行域記述の訂正（amendment 出版）**: 出版済み宣言ノート
（commit c15b1c3f）は偶z base 行を「17 行・d∈[-17,17]・上端 d=17 非飽和」と
記述していたが、fit の機械 census は偶z 生残 d 域が [-18,19] で偶z base 行が
**d 奇 19 行・d∈[-17,19]・上端 d=19=Y が k=Y 飽和**（y=17 の d=17・y=18 の
d=18 と同型）を示し、宣言の「2 箇所 k=Y は族初」も 3 行 k=Y（y=17 と同型）
への訂正となった。行クラス z 偶 d=19 は probe box 内（z=0..30 全偶z 行）と
spot bigz d=19 行（z=31..40）で生値検証済み。**宣言の実効的内容（事前登録
された族式とその機械翻訳コード）は影響を受けず probe 99,107 点に修正 0**で、
ずれたのは行域の帳簿づけのみ。訂正は amendment ノート
（research/log/2026-11-23-y19-decl-z-even-base-bookkeeping-amendment.md）
として出版し、cand19.py の docstring・コメント（行域記述・k=Y 主張・pin 節の
o_pin 偶奇ラベル）も訂正の上でコード本体不改変を selfcheck 再確認・spot 再
実行（bad 0）・監査再生成（4 実行 byte-identical）・電池再適用（10/10）まで
取り直した（y17 の点数算術誤り訂正 82653b6f と同じ運用手順・出版前捕捉）。
(1) y=19 は**box 外 pin 行が 3 行（奇z d=-17・d=-13・偶z d=-15）で系列最多**、
かつ**1 つの偶奇側に box 外 pin 行が 2 行生じる初の族**（y=17 は奇z d=-15 の
み・y=18 は奇z d=-14・偶z d=-16 の 1+1）。宣言で事前に明記し、監査の pin
ゲートは box 内可観測 8+8 行に設計、box 外 3 行は spot deep row
(37,20)/(33,20)/(34,19) の生値全点照合（R<=130 bad 0・pin R 値 2 込み）に
明示委任して全 19 pin 行を検証した。(2) 全選択行に x>=19 の機械 preflight
assert を実装（y17/y18 と同じ gate）し spot 全行の domain を機械保証。
(3) fail-closed 改ざん電池は**キャッシュ衛生（`__pycache__` purge・`-B`・
`PYTHONDONTWRITEBYTECODE`・各変種は正本から新規 copy した隔離 dir で実施）を
最初から適用**して最終正本に対して 10/10 を確定した（y18 で暴露された
stale-pyc 検出漏れ事故の運用正則を事前適用・今回は事故不発生・
検出条件は「非零 exit + FAIL-CLOSED 報告 + output/audit.json 未書き出し」）。
経緯は output/audit.json と report が正本。

## 解釈規約・全称段階

有限 fit は有限観測の機械的証拠であり全称主張ではない。全称段階
（verify_y19_universal.py・A子 H(R-1;(x-1,19);z)〔x=19 行は合流子{18,19}≡
{19,18} で cand18(z,19,R-1)〕・B子 出版 cand18 逐語転写・C子 1 xor
cand19(z-1,x,R-1)・型機械 clip 窓 2y+2=40 の tight 判定〔tight 14 族連続の
15 族目候補〕・census）は単一オーナー宣言 da6c1f5f 配下で 2026-11-23 に
実行・出版され、**本項は単一機体14チェック監査の出版で proved に昇格した**
（詳細は下記「全称段階の記録」）。
標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。3トークン以上・y>=20 族・固定幅・q 点版安定化長は範囲外。

## 全称段階の記録（単一機体14チェック版・observed→proved・2026-11-23）

単一オーナー宣言 da6c1f5f（検証器実行前に出版・観測 HEAD 6f5419b5・対抗宣言
なしを確認）配下で、y=13..y=18 出版手続き（part1 12チェック→part2 C1d+C11r）
を**単一機体単一出版**に一体化した変形（宣言で事前登録）として実施した
（evidence 内容は part1/part2 二段階と同一・12チェック電池の audit は
audit-part1-12checks.json として別正本保存）:

- **機体**: 単一機体14チェック版 verify_y19_universal.py（52,631 bytes・
  SHA-256 76525717…・C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12）。
  転写3ブロック（engine 1,957 bytes〔出版y18機part2 d29acbd8・8ddd0c2f…から
  逐語〕・cand18 3,307 bytes〔出版y18機ブロックと出版cand18.pyの二系統
  byte-equality・Y→Y18改名〕・cand19 3,411 bytes〔出版cand19.py・fit実験
  eaea0f6aから逐語〕）を check_transcriptions_y19.py が検証 PASS
  （cand18は二ソース一致・sources_agree・隔離側でも一致）。
- **C1d 事前検証**: preflight_c1d_y19.py（SHA-256 9bc154ee…・anchor block は
  出版 y18 preflight から byte-verbatim〔y=10/y=12 連鎖〕）が出版6切片
  アンカー（K0999/K1000/K1001/K1011/K1065/K1077/K1087・z0∈{8,9,10,15,16,17}）
  を y=19 行で4方照合: **12,069点 bad 0**（per z 1,890/1,917/1,944/2,079/
  2,106/2,133）+ 低R単一トークン縮約 R<=z+6: **9,306点 bad 0**・
  3.1秒・3要素は JSON 正本 1cfabdcf…。機内 C1d 掃引（x=19..159・R<=x+61）は
  **136,206点 bad 0**。
- **census第三実装**: census_rows.py（SHA-256 e4eed396…・XMIN=19・XMAX=70・
  RBUF=21・ZHI=80・LRU cap 1,600,000・約21秒）が census.txt（809,842 bytes・
  4,160行+空行80・SHA-256 07213ab1…・tail assert R>=x+z+20 全行成立）を生成し、
  C11r（rows==80*52=4,160・values range(0,x+z+21)・tail (x+19)%2）が全行を
  cand19 から再導出（T/P集合・Thue-Morse index・tail）して**440,960点 bad 0**。
  census部品（C11ordered/C11canonical・bounded-memoization twin・LRU 1.6M）は
  各engine **436,800点 bad 0**・merge帰結各102,459・tail各4,160 bad 0。
- **段階12チェック電池**（part1相当）: **overall PASS・総5,627,353点・全bad 0・
  型590,877**（C1 24,510 / C1b 44,027 / C1d 136,206 / C2 229,663 / C2b 19,580 /
  C3 1,335 / C4 579,657 / C4t 579,657〔probe〕 / C7 200,000 / C8 1,057,317 /
  C9 897,930 / C12 1,857,471）・37.4秒・audit-part1-12checks.json
  （SHA-256 63617241…）として退避。
- **フル14チェック監査**: **overall PASS・総照合点 6,941,913**（12チェック小計
  6,364,747 + C1d 136,206 + C11r 440,960）・**全bad 0・型590,877**（系列:
  y=17 457,645 → y=18 523,398 → y=19 590,877）・37.1秒/run・
  audit.json（SHA-256 59b6fded…）が正本。merge帰結 **1,062,109点 bad 0**・
  tail帰結 **192,520点 bad 0**。
- **C4t**: clip 39（2y+1）違反**770点・最初 (60,102,102)** → clip窓 2y+2=40 は
  **tight・15族連続確定**（y=5..19: 12/14/…/38/40）・最初違反は band下端
  R-z=2y+2=40 とともに歩む系列の**7観測目**
  （(60,90,90)→…→(60,100,100)→(60,102,102)・宣言の事前予想と完全一致）。
- **決定性**: 4実行 byte-identical（同一cwd 2回 + 隔離 tree/cwd/HOME+
  env -i+PYTHONHASHSEED=random 2回〔うち1回は転写検査・preflight・
  census_rows・census両部・フル14チェックの完全ゼロ再生成〕）。
  audit.json・census.txt・census両部・preflight JSON・転写検査JSON 全対応。
- **fail-closed 12種全捕捉**: census.txt欠落/行削除/重複行→FAIL-CLOSED・
  P-set/T-set改ざん→C11r bad 1・C11r tail反転→bad 4,160（全行）・アンカー
  誤結合 (16,A16u)→(16,A10u)→C1d bad 1,743・lowR参照ずれR+1→bad 9,306・
  merge境界 z-20→z-19→merge bad>0・clip窓 40,41→38,39→C4 bad 2,520・
  in_P19 tail偶奇反転→C1 bad 2,449・band_base偶奇→C1 bad 935
  （12種すべて rc=1・スクラッチtreeで実施・正典treeは無傷）。
- **宣言予想との完全一致**: 宣言ノートの事前機械算出
  （predict_y19_counts.py・出版y18 auditの14点数を完全一致で再現して
  cross-validated）は preflight 12,069+9,306・C1d 136,206・census幾何全値・
  C11r 440,960・小計 6,364,747・総点 6,941,913・C4t違反>0と最初違反
  (60,102,102)・C11r tail反転4,160 の**すべてが実測と完全一致**・
  amendment不要（y18 part1 のmerge予測スリップと異なり全段階無修正）。
- **系の確定**: 2トークン族の全称は **y=1..19 で完結**（y=1..12 は旧来の
  単族証明・y=13..19 は機械検証の逐語連鎖）。マージ命題
  x<=z-20 => H == single_token(x+19,z,R) は y=1..19 で全称。tail
  R>=x+z+20 => (x+19) mod 2。clip窓 2y+2 は y=5..19 の 15 族連続で tight。
  B子逐語連鎖 cand9..cand18（証明済みB子使用は cand10/cand12..cand18）、
  機体 item は K1245（proposition は本項）。
- **範囲外の維持**: 標準 11×11 の空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は UNKNOWN のまま。3トークン以上・y>=20 族・固定幅・q点版は
  範囲外（y=20 族は本項の結果のみを受け取る側にある）。
