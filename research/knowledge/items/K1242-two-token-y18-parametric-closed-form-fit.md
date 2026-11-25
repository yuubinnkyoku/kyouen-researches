---
id: K1242
title: "2トークン残余ゲーム y=18族のパラメトリック閉形式の全称証明（全z>=0・全x>=18・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=18 parametric closed-form fit, P18-fit"
  - "cand18 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 92,721 probe points; even-y template mechanical translation from the published FINAL cand16, the promoted-universal y=16 table with Y=16->18)"
  - "seed law 6th consecutive one-shot test passed (cand11->13 / cand12->14 / cand13->15 / cand14->16 / cand15->17 / cand16->18, even-y pair series 12->14->16->18 all 3); FIRST family with 9 pin rows on BOTH parities together and the FIRST with out-of-box lowest pin rows on both parities; FIRST 19-row consecutive-integer th sweep; 4th consecutive family with zero in-box merge rows; K1238 even-y unified template's 5th even-y regeneration data point"
  - "universal proof completed (2026-11-23, part1+part2 under single-owner declaration 1d46f883): observed -> proved via the 14-check canonical audit at 6,934,616 comparison points bad 0, C1d published-slice anchors preflighted 4-way (12,432+9,372 pts), census_rows.py third implementation consumed by C11r (443,080 pts); clip window 2y+2=38 tight, 14-family streak y=5..18; merge proposition now universal through y=1..18"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰16,989比較・境界行(39,20)/(38,19)のspot照合に使用。y=18ではbox内マージ行0行・z>=38が必要）
- type: extends
  target: K1237
  note: y=16族全称閉形式（K1237・昇格済み）の次の偶数y族。cand18初稿はy=16出版最終構造cand16（全称証明済み）のY+2機械翻訳（Y定数16→18・関数名変更のみ・コード本体は全式Y式で1行も変わらず）で生成し、probe 92,721点に一発一致（cand14→cand16に続き偶数y seed法則3連続目・全体で6連続一発一致）
- type: extends
  target: K1238
  note: 偶数y統一テンプレートの第5 even-yデータ点（テンプレートはy=10/12/14/16の4族出版表再生を機械検証済み・y=18は本fitによりその外挿がfit levelで追認。単一Yパラメトリック偶数yコードの5データ点目）
- type: extends
  target: K1240
  note: y=17族閉形式（K1240・part2昇格によりobserved→proved済み）の次族。y=18全称検証器のB子は出版cand17の逐語転写（x=18合流子{17,18}≡{18,17}）。B子逐語連鎖はcand9..cand17に拡大・証明済みB子はcand10/cand12..cand17。マージ命題は本項でy=1..18に全称拡大
- type: extends
  target: K1241
  note: y=17全称検証part1（型機械・census・二重正本転写検査の枠組み）のy=18版の前段fit。y=18全称段階はpart1/part2同型手続きでpart2まで実行・出版済み（単一オーナー宣言 1d46f883・正本監査はK1244）
- type: extends
  target: K1143
  note: y=11族の行型比較基点（「pinスロット=th-1」と偶z 2k+1 slot則がy=11..18の8族連続候補として確定・y=18で両偶奇9 pin行の初の同時到達）
- type: depends_on
  target: K1244
  note: y=18全称検証part1/part2機械（K1244・12+2チェック・総6,934,616照合点・全bad 0・3回実行byte-identical・fail-closed 9+8種）が本項observed→proved昇格の全称証拠の正本
- type: generalizes
  target: K0999
  note: C1dアンカーA8u..A17uが固定z切片の出版一様閉形式をy=18行で4方照合（anchor×H_ordered×H_canonical×cand18）。z=8: K0999、12,432点中 当該掃引 bad 0。y=18全称はz=8則のy>=18行側を含む
- type: generalizes
  target: K1001
  note: C1dアンカーのz=9一様閉形式K1001のy=18行4方照合 bad 0（同上掃引・1,974点）
- type: generalizes
  target: K1011
  note: C1dアンカーのz=10一様閉形式K1011のy=18行4方照合 bad 0（同上掃引・2,002点）
- type: generalizes
  target: K1065
  note: C1dアンカーのz=15一様閉形式K1065のy=18行4方照合+低R単一トークン縮約 bad 0（2,142点+低R縮約のうち当該分）
- type: generalizes
  target: K1077
  note: C1dアンカーのz=16一様閉形式K1077のy=18行4方照合+低R縮約 bad 0（2,170点+当該分）
- type: generalizes
  target: K1087
  note: C1dアンカーのz=17一様閉形式K1087のy=18行4方照合+低R縮約 bad 0（2,198点+当該分・y=10段階でK1087初稿の評価順序バグ170点を捕捉した事前検証段階のy=18版は初回から全一致）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（92,721 probe点一発一致・box内tail assertion 20,460点・box外spot 40,383点（全選択行にx>=18機械preflight assert・両box外最低pin行(33,19)/(36,20)の生値照合）・merge回帰16,989比較・tail raw 84点・事前予想の判定表・y=12..18横断則・fail-closed 10種と誠実記録〔bigz domain-guard live捕捉・pin_counts同一クラッシュ暴露・stale __pycache__検出漏れ→キャッシュ衛生で10/10確定〕）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-fit-20261123/cand18.py
  role: verifier
  note: 閉形式の正本cand18（in_T18値2表・in_P18値1表・Y=18・Y==18ハードassert）とprobe全点照合（92,721点・mismatch 0・overlap 0・初稿一発一致）。全称検証器は本ファイルを逐語転写
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-fit-20261123/probe_y18.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=18..z+35・R<=x+z+38=2y+2・1,023行92,721点を書き出す決定論的生成器・約10秒）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-fit-20261123/spot_y18.py
  role: verifier
  note: box外spot（全18 pin行を個別行選択したdeep rows R<=130・bigz z=31..40・x=y=18 edge・far d∈{36,47,58}・tail raw・merge回帰16,989・LRU cap 1.5M決定的退避・190.9秒・bad 0）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-fit-20261123/make_audit_y18.py
  role: verifier
  note: 監査生成器（pin格子観測ゲート〔box内可観測8+8行〕・box幾何独立再計算ゲート・本族新設の逐行整合性ゲート〔x>=18・d再計算・merge flag・RLE長x+z+38〕・in-box tail assertion・in-box merge 0行ゲート・偶z対角値1 census・fail-closed・3実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 b0d9c4be…7468・自己文書化・probe/spot/merge/tail数値・sha256ピン〔probe_rows e80ca337…〕・宣言commit 738ab049記録・両偶奇box外最低pin行の初の族の誠実記録）
- path: research/log/2026-11-23-y18-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit 738ab049・probe実行前に出版・事前横断予想の全記録・対抗宣言チェック・box内マージ行0行と両最低pin行box外到達不能の事前明記・宣言点数92,721は出版前に機械算出）
- path: research/log/2026-11-23-two-token-y18-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・経緯・出版記録・次段階）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/README.md
  role: proof
  note: 全称検証実験README（part1+part2・C1d事前検証12,432+9,372点・C11r 443,080点・フル14チェック監査総6,934,616点bad 0・決定性3回・fail-closed 9+8種・昇格判定の記録）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/verify_y18_universal.py
  role: verifier
  note: 全称検証器part2正本（52,177 bytes・SHA-256 8ddd0c2f…・14チェック。part1出版の12チェック本体はbyte不変・diffはanchor block/check_C1d/check_C11r/docstring/main()登録のみ）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/output/audit.json
  role: data
  note: part2フル14チェック監査正本（SHA-256 a636c187…・total_points 6,934,616・total_bad 0・type_count 523,398・3回実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/census_rows.py
  role: verifier
  note: census第三実装（SHA-256 1cd71004…・XMIN=18・XMAX=70・RBUF=20・ZHI=80・443,080点・zero_points 221,548・misses 9,262,827・約18秒・census.txt 4,240行を生成）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/output/census.txt
  role: data
  note: census行台帳正本（810,453 bytes・SHA-256 8e239f52…・C11rが全行をcand18から再導出し443,080点bad 0）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/scripts/preflight_c1d_y18.py
  role: verifier
  note: C1d事前検証（SHA-256 1d21c6ab…・出版6切片アンカー4方照合12,432点+低R単一トークン縮約9,372点・bad 0・組み込み前fail-closedゲート・JSON SHA-256 89cb9541…）
- path: research/experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/scripts/check_transcriptions_y18.py
  role: verifier
  note: 転写二重正本検証（engine/cand17二ソース/cand18の出版bytes一致・part2検証器bytesでもPASS・隔離側で再生成し一致）
- path: research/log/2026-11-23-y18-universal-verifier-single-owner-note.md
  role: log
  note: 全称段階の単一オーナー宣言ノート（commit 1d46f883・part1+part2単一オーナー継続保持・対向宣言はy=19 fitのみ）
- path: research/log/2026-11-23-y18-universal-verifier-part1.md
  role: log
  note: part1実行記録（region-splice欠陥のlive捕捉の誠実記録・出版記録）
- path: research/log/2026-11-23-y18-universal-verifier-part2.md
  role: log
  note: part2実行記録（C1d事前検証・census_rows.py・C11r・フル14チェック監査・決定性・fail-closed 8種・昇格判定）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,18)、全z>=0・全x>=18・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand18）で
  分類する命題。全称は正本検証器part1+part2（K1244・フル14チェック監査・
  総6,934,616照合点・全bad 0・3回実行byte-identical・fail-closed 9+8種）で
  検証済み（2026-11-23出版・単一オーナー宣言 1d46f883 配下でobserved→proved
  昇格）。系としてx<=z-19の単一トークン一致マージ命題y=18版とtail
  R>=x+z+19の(x+18) mod 2を含み、マージ命題はy=1..18で全称確定。標準11×11の空盤・二石root・
  S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNのまま。3トークン以上・
  y>=19族・固定幅・q点版も範囲外。
evidence: >-
  fit段階の証拠（2026-11-23出版・単一オーナー宣言 738ab049 配下）:
  (1) 初稿一発一致: cand18初稿は出版cand16（K1237全称・Y=16）のY+2機械翻訳で、
  probe box全点に修正0（mismatch 0・overlap 0・値頻度 0:45,620 / 1:37,046 /
  2:10,055・値3なし）。seed法則6連続目（偶数y系列3連続目）・K1238偶数y
  統一テンプレートの第5 even-yデータ点。
  (2) 構造則の確定: 基底点18点{z+1,..,z+35}・z-odd I帯k=floor((d+3y+2)/4)
  th連続整数19..37の初の19行掃引・同式base行k=floor((d+3y+1)/4)・z-even I帯
  k=floor((d+3y-1)/4) th=2k+1・z-even base行同式・pin格子統一式
  pin=z+(d+54)/2（奇z 9行d≡2 (mod 4)・偶z 9行d≡0 (mod 4)・**両偶奇とも
  9行に揃う初の族**・「pinスロット=th-1」/偶z 2k+1 slotが8族連続候補・
  最終pin行d=18=yのI[37)型13族目候補・**両最低pin行d=-14/d=-16がともに
  box内到達不能は系列初**〔spot deep row (33,19)/(36,20)生値照合に事前委任〕）・
  対角cap z+18/z+17・偶z対角値1全欠如11族目候補・掃引d=19・定常pin
  z+36/z+37・band下端2y+2=38・偶y単一band則・tail開始x+z+19値(x+18) mod 2・
  d=18飽和k=Y 5族連続候補。
  (3) 回帰: マージ命題y=18版（K0832単一トークン）16,989比較不一致0・境界行
  (39,20)/(38,19)の生値一致・tail raw 84点一致。合計150,177点比較・不一致0。
  (4) 決定性・fail-closed: probe_rows.txt 3回再生成（同一cwd2回+隔離
  tree/cwd/HOME+env -i+PYTHONHASHSEED=random1回）byte-identical
  （SHA-256 e80ca337…4429）・audit.json 3実行byte-identical（b0d9c4be…7468）・
  fail-closed 10種全捕捉（probe値改ざん・pin値改ざん・Y定数改ざん18→17〔Y==18
  ハードassert〕・pin mod4クラス改ざん〔監査が欠落7行を列挙〕・probe行欠落
  （幾何ゲート）・重複行注入（幾何ゲート）・meta d改ざん・merge flag改ざん・
  RLE長改ざん〔本族新設の逐行整合性ゲート〕・band下端改ざん〔mm=511〕・復元
  byte-identical・clean control rc=0・**キャッシュ衛生込み**〔同一秒内・同一
  サイズ改ざんがstale __pycache__の秒粒度mtime照合で握り潰される現象を暴露し、
  purge+-B+PYTHONDONTWRITEBYTECODEで10/10確定。「byte-identical N回」型
  検証にはバイトコードキャッシュ衛生が必須という運用正則〕）。
  全称段階の証拠（2026-11-23出版・単一オーナー宣言 1d46f883 配下・part1+part2でobserved→proved昇格）:
  part1（commit 9f3d5764）: 転写二重正本検証（@@TRANSCRIPTION 3ブロックの
  出版bytes一致）・正本検証器12チェック overall PASS（総6,354,790点・bad 0・
  型523,398・clip 38 tight〔14族連続 y=5..18〕・merge 1,121,822比較 bad 0・
  tail 192,210点 bad 0）・3回決定性（同一cwd2回+隔離run3で全出力byte-identical）・
  fail-closed 9種（T1-T8改ざん全捕捉・T9深部tail窓のbad 0は出版cand17
  〔K1240 proved〕tail主張の内部点の拡張整合性観察で真の境界(17)シフトは
  C8で40 bad捕捉）。
  part2: C1d事前検証（出版6切片アンカー4方照合12,432点+低R縮約9,372点
  bad 0・PASS・組み込み前ゲート）・census_rows.py（第三実装・rows 4,240・
  points 443,080・zero_points 221,548・misses 9,262,827・約18秒）を
  C11r（rows==4,240==80*53・values range(0,x+z+21)・tail (x+18)%2）で消費し
  フル14チェック監査 total 6,934,616点 bad 0（run1/run2同一cwd+run3隔離で
  byte-identical・audit.json SHA-256 a636c187…）・fail-closed 8種全捕捉
  （census.txt欠落/行削除/重複行のFAIL-CLOSED・P-set/T-set改ざん→C11r bad 1・
  C11r tail反転→bad 4,240・アンカー誤結合→C1d bad 1,756・lowR参照ずれR+1→
  bad 9,372）。C4t clip 37違反は1,012点 (60,100,100) で全bad 0かつ
  tail/merge検査で裏付けられtight判定維持。
---

## 命題・範囲

すべての z>=0・x>=18・R>=0 に対して H(R;(x,18);z) = cand18(z,x,R) が成り立つ
（**status: proved・2026-11-23 全称検証 part1+part2 出版で observed→proved 昇格**）。
全称段階の正本は
[全称検証実験dir](../../experiments/vertical-fiber-two-token-y18-parametric-allz-proof-20261123/README.md)。
fit段階の正本は
[fit実験dir](../../experiments/vertical-fiber-two-token-y18-parametric-allz-fit-20261123/report.md)
で、cand18.py が閉形式の正本実装である。fit段階の証拠は
(1) probe box（z=0..30・x=18..z+35・R<=x+z+38）生二重再帰 1,023 行 92,721 点の
全点一致（初稿一発・修正 0・T/P 重複 0）、(2) box 内 tail assertion
R>=x+z+19 → (x+18) mod 2 の 20,460 点一致、(3) box 外 spot 40,383 点
（全 18 pin 行を個別行として選択した deep rows・bigz z=31..40・x=y=18
edge・far d∈{36,47,58}）、(4) merge 回帰 16,989 比較（K0832 単一トークン
閉形式）+ 境界行 (39,20)/(38,19) の生値一致、(5) tail raw 84 点、
の計 150,177 点比較不一致 0 である。

## 主要構造（fit で確定した構造則・有限範囲）

y=18 は偶数 y 族（y=10/12/14/16 と同型）で、値1無限帯・tail は x 奇の行。
基底点 18 点 {z+1,...,z+35}・マージ行 x<=z-19（box 内 0 行・4 族連続）・
奇z I 帯行 k(d)=floor((d+3y+2)/4)・th 連続整数 19..37（**初の 19 行掃引**）・
偶z I 帯行 k=floor((d+3y-1)/4)（8 族目候補）・base 行 k=floor((d+3y+1)/4)
（9 族目候補・偶z d=18 で k=18=Y 飽和・5 族連続候補）・
pin 格子統一式 pin=z+(d+54)/2（o_pin∈[19,36]・奇z 9 行 d≡2 (mod 4)
{-14,...,18}・偶z 9 行 d≡0 (mod 4) {-16,...,16}・**両偶奇とも 9 行に揃う
初の族・偶z 9 行は y 偶族式 y/2 増加則 6→7→8→9 の到達点**・
「pin スロット = th-1」/偶z 2k+1 slot 8 族目・最終 pin 行 d=18=y の
I[2y+z+1)=I[37) 型 13 族目候補・**両最低 pin 行 d=-14/d=-16 がともに
box 内到達不能は系列初**）・掃引行 d=19・定常 pin z+36（奇z）/z+37（偶z）・
band 下端 2y+2=38・偶y 単一 band 則・tail 開始 x+z+19・tail 値 (x+18) mod 2・
偶z 対角行 d=-18 の値 1 全欠如（11 族目候補）・対角 cap z+18/z+17
（偶 y 族式の向き）。標準の信頼境界（選択肢分解・mex 恒等式・有限型空間）
は y=5..17 出版系列と同一の機械分類に依存し、全称段階で初めて検証される。

## fit の工芸的観察（fitting なしの一発一致）

**初稿一発一致（修正 0）**: cand18 初稿は y=16 の出版最終構造（cand16・K1237
全称昇格済み・K1238 偶数 y 統一テンプレート正本）を seed とした Y+2 機械翻訳
（Y 定数の差し替えと関数名変更のみ）で、probe 92,721 点に修正 0 で一致。
「直前の出版最終構造 seed による外挿が一発一致する」は **6 連続**
（cand11→13・cand13→15・cand15→17〔奇〕・cand12→14・cand14→16・
cand16→18〔偶〕）となり、横断法則一般補題化レーンの主要リスク
（族式の y 依存跳躍）をさらに低減した。y=15/16/17 に続き 4 族連続の
「box 内マージ行 0 行」族でもあり、事前宣言どおりマージ回帰は全面 box 外。
宣言ノートの点数 92,721 は出版前に機械算出して記載したため amendment 不用
（y=17 の点数算術誤り訂正 82653b6f の教訓を適用）。

## 誠実記録（両偶奇 box 外最低 pin 行と検証インフラの live 捕捉）

(1) y=18 は**両偶奇の最低 pin 行（奇z d=-14・偶z d=-16）がともに宣言 box
（z<=30・x>=18）内で幾何学的に到達不可能である系列初の族**（y=17 は奇z
d=-15 のみ）。宣言で事前に明記し、監査の pin ゲートは box 内可観測 8+8 行
に設計、9 行目（両偶奇）は spot deep row (33,19)/(36,20) の生値全点照合
（R<=130 bad 0・pin R 値 2 込み）に明示委任して全 18 pin 行を検証した。
(2) spot 初稿の bigz d 選択（d=-16@z=31 は x=15<18）が spot 自身の preflight
assert に live で拒否され 25 値選択に修正された（domain guard が紙上でなく
機能した実例）。(3) 監査初稿の pin_counts が tuple キーで JSON クラッシュし
「3 実行 byte-identical」が実態は 3 回同一クラッシュだったのを電池の clean
control が暴露、原因を除去して改めて byte-identical 3 実行を確定した。
(4) 改ざん電池初回実行で同一秒内・同一サイズの改ざんが stale `__pycache__`
（秒粒度 mtime+サイズ照合）に握り潰され 2 変種のみ検出を逃した。
`__pycache__` purge・`-B`・`PYTHONDONTWRITEBYTECODE` のキャッシュ衛生で
10/10 検出を確定した（「byte-identical N 回」型検証主張にはバイトコード
キャッシュ衛生が必須という運用正則）。経緯は output/audit.json と report が正本。

## 解釈規約・次段階

有限 fit は有限観測の機械的証拠であり全称主張ではない。全称段階
（verify_y18_universal.py・A子 H(R-1;(x-1,18);z)〔x=18 行は合流子{17,18}≡
{18,17} で cand17(z,18,R-1)〕・B子 出版 cand17 逐語転写・C子 1 xor
cand18(z-1,x,R-1)・型機械 clip 窓 2y+2=38 の tight 判定〔tight 13 族連続の
14 族目候補〕・census）は単一オーナー宣言 1d46f883 配下で 2026-11-23 に実行・出版され、**本項は part2 出版で proved に昇格した**（詳細は下記「全称段階の記録」）。
標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。3 トークン以上・y>=19 族・固定幅・q 点版安定化長は範囲外。

## 全称段階の記録（part1・part2・observed→proved・2026-11-23）

単一オーナー宣言 1d46f883（検証器実行前に出版・対向宣言はy=19 fitのみで
y=18全称は本レーンが単一オーナー・part1+part2継続保持を宣言）配下で、
y=13..y=17 と同一手続きの part1+part2 を実施した:

- **part1**（commit 9f3d5764・K1244）: 転写二重正本検証 PASS の後、正本検証器
  12チェック overall PASS（総 6,354,790 点・bad 0・型 523,398・clip 38 tight
  で 14 族連続 y=5..18・merge 1,121,822 比較 bad 0・tail 192,210 点 bad 0）。
  3回決定性（run1/run2 同一 cwd + run3 隔離再生成）で全出力 byte-identical。
  fail-closed 9種（改ざん8種全捕捉・T9深部tail窓のbad 0は K1240 tail内部点の
  拡張整合性観察）。組み立て段階のregion-splice欠陥を機のC1が出版前に捕捉
  （1,229 bad・1族シフト署名・出版bytesは修正後のみ）の誠実記録つき。
- **part2**: C1d 事前検証（出版 6 切片アンカーの 4 方照合 12,432 点 + 低 R
  縮約 9,372 点・bad 0・組み込み前 fail-closed ゲート・preflight 3実行
  byte-identical）→ census_rows.py（第三実装・4,240 行 443,080 点・
  zero_points 221,548・misses 9,262,827・tail assert 全行成立）を C11r
  として正本検証器に組み込み、フル 14 チェック監査 total 6,934,616 点
  bad 0（audit.json SHA-256 a636c187…・run1/run2/run3 byte-identical）。
  fail-closed 8種全捕捉。検証器 part2 正本は part1 出版 byte の in-place
  拡張（SHA-256 8ddd0c2f…・part1 12 チェック本体は byte 不変）。
- **系の確定**: 2トークン族の全称は y=1..18 で完結（y=1..12 は旧来の
  単族証明・y=13..18 は B子逐語連鎖 cand9..cand17・証明済み B子は
  cand10/cand12..cand17）。マージ命題 x<=z-19 => H == single_token(x+18,z,R)
  は y=1..18 で全称。clip 窓 2y+2 は y=5..18 の 14 族連続で tight
  （y=18 は 38・最初違反 (60,100,100) はバンド下端と歩む 6 回目の観測）。
- **範囲外の維持**: 標準 11×11 の空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は UNKNOWN のまま。3トークン以上・y>=19 族・固定幅・q点版は
  範囲外（y=19 fit は並走レーンの単一オーナー宣言済み・非接触）。
