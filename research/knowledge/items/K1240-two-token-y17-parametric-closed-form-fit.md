---
id: K1240
title: "2トークン残余ゲーム y=17族のパラメトリック閉形式の全称証明（全z>=0・全x>=17・全R>=0）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "two-token y=17 parametric closed-form fit, P17-fit"
  - "cand17 fitting and out-of-box spot verification (fitting stage, pre-universal; first-draft ZERO-correction agreement on all 86,552 probe points; odd-y template mechanical translation from the published FINAL cand15, the promoted-universal y=15 table with Y=15->17)"
  - "seed law 5th consecutive one-shot test passed (cand11->13 / cand12->14 / cand13->15 / cand14->16 / cand15->17, odd-y series 11->13->15->17); FIRST 9-pin-row family (y-odd count law (y+1)/2 reaches 9); third consecutive family with zero in-box merge rows"
  - "universal proof completed (2026-11-23, part1+part2 under single-owner declaration b099a974 + geometry amendment 03ca97ad): observed -> proved via the 14-check canonical audit at 6,926,065 comparison points bad 0, C1d published-slice anchors preflighted 4-way (12,789+9,438 pts), census_rows.py third implementation consumed by C11r (444,960 pts); clip window 2y+2=36 tight, 13-family streak y=5..17; merge proposition now universal through y=1..17"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式（box外マージ回帰15,495比較・境界行(35,17)/(36,18)のspot照合に使用。y=17ではbox内マージ行0行・z>=35が必要）
- type: extends
  target: K1235
  note: y=15族全称閉形式（K1235・昇格済み）の次の奇数y族。cand17初稿はy=15出版最終構造cand15（全称証明済み）のY+2機械翻訳（Y定数15→17・関数名変更のみ・コード本体は全式Y式で1行も変わらず）で生成し、probe 86,552点に一発一致（cand13→cand15に続き奇数y seed法則3連続目・全体で5連続一発一致）
- type: extends
  target: K1237
  note: y=16族全称閉形式（K1237・昇格済み）の次族。全称検証器のB子は出版cand16の逐語転写（x=17合流子{16,17}≡{17,16}・B子逐語連鎖はcand9..cand16に拡大・証明済みB子はcand10/cand12..cand16）。マージ命題は本項でy=1..17に全称拡大
- type: extends
  target: K1143
  note: y=11族の奇数y型比較対象（th=2k+1ペア反復型・x偶行のtail・pin行数(y±1)/2系列の基点）。y=17でpin行数は奇z 9行・偶z 8行に到達（4点目）
- type: depends_on
  target: K1238
  note: 偶数y統一テンプレート機械検証の陰性対照知見（テンプレートは偶y特化・y=17は非適用）と整合: 本fitのseedは奇数y系列（cand13/cand15系列テンプレート）で、単一Yパラメトリック奇数yコードがy=13/15/17で再生するかは本fitの一致が新データ点
- type: depends_on
  target: K1241
  note: 全称証明part1（正本検証器12チェック・overall PASS 6,343,825点・3回byte-identical・転写二重正本検証・fail-closed）とpart2（昇格段階・C1d事前検証+census第三実装C11r・14チェック6,926,065点）の機関記録。同一単一オーナー宣言 b099a974（+幾何訂正amendment 03ca97ad）配下の工程
- type: generalizes
  target: K0999
  note: z=8・y>=9一様全Grundy分類のy=17行は本項の特殊例（転写アンカーA8uとしてC1d照合）
- type: generalizes
  target: K1001
  note: z=9・y>=9一様分類のy=17行は本項の特殊例（A9u）
- type: generalizes
  target: K1011
  note: z=10・K1011 scopeのy=17行は本項の特殊例（A10u）
- type: generalizes
  target: K1065
  note: z=15・y>=6一様族のy=17行は本項の特殊例（A15u）
- type: generalizes
  target: K1077
  note: z=16・y>=6一様族のy=17行は本項の特殊例（A16u）
- type: generalizes
  target: K1087
  note: z=17・y>=6一様族のy=17行は本項の特殊例（A17u）
artifacts:
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/report.md
  role: proof
  note: fit段階の正本記録（86,552 probe点一発一致・box内tail assertion 18,848点・box外spot 41,465点（全選択行にx>=17機械assert・cand17.py selfcheckにも全行assert）・merge回帰15,495比較・tail raw 84点・事前予想の判定表・y=6..17横断則・fail-closed 8種と誠実記録〔z-odd pin d=-15のbox内到達不可能性を監査生成器自体のFAIL-CLOSEDで捕捉しゲート修正+spot生値照合に委任〕）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/cand17.py
  role: verifier
  note: 閉形式の正本cand17（in_T17値2表・in_P17値1表・Y=17・全行x>=17 assert）とprobe全点照合（86,552点・mismatch 0・overlap 0・初稿一発一致）。全称検証器は本ファイルを逐語転写
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/probe_y17.py
  role: verifier
  note: 生二重再帰probe（正準降順multiset memoization・z=0..30・x=17..z+33・R<=x+z+36=2y+2・992行86,552点を書き出す決定論的生成器・約8秒）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/spot_y17.py
  role: verifier
  note: box外spot（deep rows・bigz・edge・far d・tail raw・merge回帰・LRU cap 1.5M決定的退避・177秒・bad 0）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/make_audit_y17.py
  role: verifier
  note: 監査生成器（pin格子観測ゲート・box幾何独立再計算ゲート〔行欠落・注入・重複を含む改ざんを捕捉〕・in-box tail assertion・in-box merge 0行ゲート・fail-closed・3実行byte-identical）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/output/audit.json
  role: data
  note: fit監査正本（SHA-256 c5593987…・自己文書化・probe/spot/merge/tail数値・sha256ピン・宣言commit eeeb1a8e+訂正amendment 82653b6f記録・z-odd pin d=-15 box内到達不可能性の誠実記録）
- path: research/log/2026-11-23-y17-two-token-skeleton-single-owner-note.md
  role: log
  note: fit段階の単一オーナー宣言ノート（commit eeeb1a8e・probe実行前に出版・事前横断予想12項目の全記録・対抗宣言チェック・box内マージ行0行とd>=18 tail 19点深の事前明記・点数算術訂正amendment 82653b6f）
- path: research/log/2026-11-23-two-token-y17-parametric-fit.md
  role: log
  note: fit段階の実行記録（選定・経緯・出版記録・次段階）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/README.md
  role: proof
  note: 全称検証実験の正本記録（転写二重正本検証・part1 12チェック+part2 C1d/C11r 14チェック結果表・bounded-memoization twin設計・3回決定性・fail-closed part1 6種+part2 6種・T5初案bad 0の誠実記録〔拡張整合性観察〕・observed→proved昇格判定・再現コマンド・解釈規約）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/verify_y17_universal.py
  role: verifier
  note: 正本検証器（part2正本・SHA-256 4253cf29…・14チェック構成。part1出版正本はcommit 33e0a062・SHA 2110ecbb…・12チェック・part2はpart1 byteのin-place拡張〔y=13..y=16 part2手続き〕でpart1 12チェック本体はbyte不変）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/output/audit.json
  role: audit-output
  note: part2フル14チェック監査正本（SHA-256 fd4b7d8c…・total_points 6,926,065・total_bad 0・型457,645・3実行byte-identical〔2同一cwd+1隔離再生成〕。part1 12チェック正本はSHA 301f7690…・commit 33e0a062）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/census_rows.py
  role: verifier
  note: census第三実装 y=17版（SHA-256 1188bcd1…・census.txt 817,882 bytes 4,320行+空行80・SHA-256 597370b4…）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/scripts/preflight_c1d_y17.py
  role: verifier
  note: C1d事前検証（出版6切片アンカーの4方照合12,789点+低R縮約9,438点・bad 0・組み込み前fail-closedゲート・SHA-256 fc1d4ec0…・output/preflight-c1d-y17.json c8e0e0a9…）
- path: research/experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/scripts/check_transcriptions_y17.py
  role: verifier
  note: 転写二重正本検証（@@TRANSCRIPTION marker 3ブロックの出版bytes一致・part2版でもPASS・SHA-256 ac40c03c…）
- path: research/log/2026-11-23-y17-universal-verifier-single-owner-note.md
  role: log
  note: 全称段階の単一オーナー宣言ノート（commit b099a974・検証器実行前に出版・対抗宣言grep clean・part1+part2継続保持の宣言・幾何訂正amendment 03ca97ad〔C2b掃引行x∈{17,22,…,67}〕）
- path: research/log/2026-11-23-y17-universal-verifier-part1.md
  role: log
  note: part1記録（12チェック6,343,825点全PASS・3回byte-identical・昇格判定part2留保のまま出版）
- path: research/log/2026-11-23-y17-universal-verifier-part2.md
  role: log
  note: part2記録（C1d事前検証・census第三実装・14チェック監査6,926,065点・3回byte-identical・K1240 observed→proved昇格・出版記録）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,17)、全z>=0・全x>=17・全R>=0。
  HのGrundy値0/1/2をz偶奇別のパラメトリックT/P集合表（閉形式cand17）で
  分類する命題（status proved・2026-11-23 part2出版でobserved→proved昇格。
  正本検証器14チェック体制・型機械・census・C1d publishedアンカー・単一
  オーナー宣言 b099a974 配下のpart1+part2）。系として
  x<=z-18 => H == single_token(x+17,z,R) のマージ命題とtail
  R>=x+z+18 => H == (x+17) mod 2 が全称系として確定（マージ命題は
  y=1..17で全称）。標準11×11の空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNのまま。3トークン以上・
  y>=18族・固定幅・q点版も範囲外。
evidence: >-
  fit段階の証拠（2026-11-23出版・単一オーナー宣言 eeeb1a8e 配下）:
  (1) 初稿一発一致: cand17初稿は出版cand15（K1235全称・Y=15）のY+2機械翻訳で、
  probe box全点に修正0（mismatch 0・overlap 0・値頻度 0:42,568 / 1:34,200 /
  2:9,784・値3なし）。seed法則5連続目（奇数y系列3連続目）。
  (2) 構造則の確定: 基底点17点{z+1,..,z+33}・z-odd I帯k=floor((d+3y+1)/4)
  th=2k+1ペア反復・同式base行・z-even I帯k=floor((d+3y-1)/4)・z-even base行
  同式・pin格子統一式pin=z+(d+51)/2（奇z 9行d≡1 (mod 4)・偶z 8行d≡3 (mod 4)・
  FIRST 9-pin-row family・「pinスロット=th-1」7族連続候補・最終pin行d=17=yの
  I[35)型12族目候補）・対角cap z+16/z+17・偶z対角値1全欠如10族目候補・
  掃引d=18・定常pin z+34/z+35・band下端2y+2=36・tail開始x+z+18値(x+17) mod 2。
  (3) 回帰: マージ命題y=17版（K0832単一トークン）15,495比較不一致0・旧来の
  境界行(35,17)/(36,18)の生値一致・tail raw 84点一致。
  (4) 決定性・fail-closed: probe_rows.txt 3回再生成（同一cwd2回+隔離
  tree/cwd/HOME+env -i+PYTHONHASHSEED=random1回）byte-identical
  （SHA-256 248d5249…）・audit.json 3実行byte-identical（c5593987…）・
  fail-closed 8種全捕捉（probe値改ざん・pin値改ざん・Y定数改ざん17→16
  〔mismatch 3,764〕・pin mod4クラス改ざん・probe行欠落（幾何ゲート）・
  重複行注入（幾何ゲート）・z-odd pin d=-15 box内到達不可能性の監査生成器
  deep row (33,18)生値照合に委任〕・復元byte-identical）。
  全称段階の証拠（2026-11-23出版・単一オーナー宣言 b099a974 + amendment
  03ca97ad 配下・part1+part2でobserved→proved昇格）:
  part1（commit 33e0a062）: 転写二重正本検証（@@TRANSCRIPTION 3ブロックの
  出版bytes一致）・正本検証器12チェック overall PASS（総6,343,825点・bad 0・
  型457,645・clip 36 tight〔13族連続 y=5..17〕・C1z出版切片アンカー・C2a/C2b
  掃引・merge 1,182,632比較 bad 0・tail 193,096点 bad 0）・3回決定性
  （同一cwd2回+隔離run3で全出力byte-identical）・fail-closed 6種全捕捉。
  T5初案のbad 0は拡張整合性観察として誠実記録（引用は監査合格後）。
  part2: C1d事前検証（出版6切片アンカー4方照合12,789点+低R縮約9,438点
  bad 0・PASS・組み込み前ゲート）・census_rows.py（第三実装・rows 4,320・
  points 444,960・zero_points 221,578・misses 8,725,227・約17.5秒）を
  C11r（rows==4,320==80*54機・values range(0,x+z+20)・tail (x+17)%2）で
  消費し フル14チェック監査 total 6,926,065点 bad 0（run1/run2同一cwd+
  run3隔離でbyte-identical・audit.json SHA-256 fd4b7d8c…）・fail-closed
  6種全捕捉（census part改ざん/census.txt欠落/P-set改ざん/merge境界改ざん/
  canonical part欠落/重複行注入）。C4t clip 36違反は1,300点 (60,98,98)
  で全bad 0かつtail/merge検査で裏付けられtight判定維持。
---
deep row (33,18)生値照合に委任〕・復元byte-identical）。
---

## 命題・範囲

すべての z>=0・x>=17・R>=0 に対して H(R;(x,17);z) = cand17(z,x,R) が成り立つ
（**status: proved・2026-11-23 全称検証 part1+part2 出版で observed→proved 昇格**）。
全称段階の正本は
[全称検証実験dir](../../experiments/vertical-fiber-two-token-y17-parametric-allz-proof-20261123/README.md)。
fit段階の正本は
[実験dir](../../experiments/vertical-fiber-two-token-y17-parametric-allz-fit-20261123/report.md)
で、cand17.py が閉形式の正本実装である。本項の証拠は
(1) probe box（z=0..30・x=17..z+33・R<=x+z+36）生二重再帰 992 行 86,552 点の
全点一致（初稿一発・修正 0・T/P 重複 0）、(2) box 内 tail assertion
R>=x+z+18 → (x+17) mod 2 の 18,848 点一致、(3) box 外 spot 41,465 点
（全 9 奇z pin 行・全 8 偶z pin 行を個別行として選択した deep rows・bigz
z=31..40・x=y=17 edge・far d∈{34,45,56}）、(4) merge 回帰 15,495 比較
（K0832 単一トークン閉形式）+ 境界行 (35,17)/(36,18) の生値一致、
(5) tail raw 84 点、の計 143,596 点比較不一致 0 である。

## 主要構造（fit で確定した構造則・有限範囲）

y=17 は奇数 y 族（y=9/11/13/15 と同型）で、値1無限帯・tail は x 偶の行。
基底点 17 点 {z+1,...,z+33}・マージ行 x<=z-18（box 内 0 行・3 族連続）・
奇z I 帯行 k(d)=floor((d+3y+1)/4)・th=2k+1 ペア反復型（y 偶族掃引型との
偶奇分離 17 族目）・偶z I 帯行 k=floor((d+3y-1)/4)（7 族目候補）・
base 行 k=floor((d+3y+1)/4)（8 族目候補・偶z d=17 で k=17=Y 飽和）・
pin 格子統一式 pin=z+(d+3y)/2（o_pin∈[18,34]・奇z 9 行 d≡1 (mod 4)
{-15,...,17}・偶z 8 行 d≡3 (mod 4) {-13,...,15}・**初の 9 pin 行族**・
「pin スロット=th-1」7 族目・最終 pin 行 d=17=y の I[2y+z+1)=I[35) 型
12 族目候補）・掃引行 d=18・定常 pin z+34（奇z）/z+35（偶z）・
band 下端 2y+2=36・tail 開始 x+z+18・tail 値 (x+17) mod 2・
偶z 対角行 d=-17 の値 1 全欠如（10 族目候補）・対角 cap z+16/z+17
（奇 y 族式の向き）。標準の信頼境界（選択肢分解・mex 恒等式・有限型空間）
は y=5..16 出版系列と同一の機械分類に依存し、全称段階で初めて検証される。

## fit の工芸的観察（fitting なしの一発一致）

**初稿一発一致（修正 0）**: cand17 初稿は y=15 の出版最終構造（cand15・K1235
全称昇格済み）を seed とした Y+2 機械翻訳（Y 定数の差し替えと関数名変更のみ）で、
probe 86,552 点に修正 0 で一致。「直前の出版最終構造 seed による外挿が一発一致する」
は **5 連続**（cand11→13・cand13→15・cand15→17〔奇〕・cand12→14・cand14→16〔偶〕）
となり、横断法則一般補題化レーンの主要リスク（族式の y 依存跳躍）をさらに低減した。
y=15・y=16 に続き 3 族連続の「box 内マージ行 0 行」族でもあり、事前宣言どおり
マージ回帰は全面 box 外。宣言ノートの点数算術誤り（81,902 → 86,552）は
amendment 82653b6f で訂明記録した。

## 誠実記録（z-odd pin d=-15 の box 内観測可能性境界）

初回の監査生成は FAIL-CLOSED した: 事前登録した奇z pin 格子 9 行のうち
d=-15 は宣言 box（z<=30・x>=17）では幾何学的に到達不可能（x=z-15>=17 は
z>=32 を要求）であり、in-box 観測は 8 行までしか存在しない。これは fail-closed
設計が想定どおり機能した捕捉であり、ゲートを box 内可観測 8 行に修正し、
9 行目（d=-15）を spot deep row (33,18) の生値全点照合（R<=130 bad 0・
pin R=51 値 2）に明示委任して本 fit で全 9 行を検証した。経緯は
output/audit.json（in_box_observability_note）と report が正本。

## 解釈規約・次段階

有限 fit は有限観測の機械的証拠であり全称主張ではない。全称段階
（verify_y17_universal.py・A子 H(R-1;(x-1,17);z)〔x=17 行は合流子{16,17}≡
{17,16} で cand16(z,17,R-1)〕・B子 出版 cand16 逐語転写・C子 1 xor
cand17(z-1,x,R-1)・型機械 clip 窓 2y+2=36 の tight 判定〔13 族目候補〕・
census）は単一オーナー宣言 b099a974（+幾何訂正 amendment 03ca97ad）配下で
2026-11-23 に実行・出版され、**本項は part2 出版で proved に昇格した**（詳細は
下記「全称段階の記録」）。標準 11×11 空盤・二石 root
{49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
3 トークン以上・y>=18 族・固定幅・q 点版安定化長は範囲外。

## 全称段階の記録（part1・part2・observed→proved・2026-11-23）

単一オーナー宣言 b099a974（検証器実行前に出版・対抗宣言 grep clean・幾何訂正
amendment 03ca97ad は C2b 掃引行 x∈{17,22,…,67} の掃引範囲訂正）配下で、
y=13..y=16 と同一手続きの part1+part2 を実施した:

- **part1**（commit 33e0a062）: 転写二重正本検証 PASS の後、正本検証器
  12チェック overall PASS（総 6,343,825 点・bad 0・型 457,645・clip 36 tight
  で 13 族連続 y=5..17・merge 1,182,632 比較 bad 0・tail 193,096 点 bad 0）。
  3回決定性（run1/run2 同一 cwd + run3 隔離再生成）で全出力 byte-identical。
  fail-closed 6種全捕捉。T5 初案の bad 0 は拡張整合性観察として誠実記録し、
  大域安定化長の引用は 14 チェック監査合格後に解禁した。
- **part2**: C1d 事前検証（出版 6 切片アンカーの 4 方照合 12,789 点 + 低 R
  縮約 9,438 点・bad 0・組み込み前 fail-closed ゲート）→ census_rows.py
  （第三実装・4,320 行 444,960 点・zero_points 221,578・misses 8,725,227）を
  C11r として正本検証器に組み込み、フル 14 チェック監査 total 6,926,065 点
  bad 0（audit.json SHA-256 fd4b7d8c…・run1/run2/run3 byte-identical）。
  fail-closed 6種全捕捉。検証器 part2 正本は part1 出版 byte の in-place
  拡張（SHA-256 4253cf29…）で part1 12 チェック本体は byte 不変。
- **系の確定**: 2トークン族の全称は y=1..17 で完結（y=1..12 は旧来の
  単族証明・y=13..17 は B子逐語連鎖 cand9..cand16・証明済み B子は
  cand10/cand12..cand16）。マージ命題 x<=z-18 => H == single_token(x+y,z,R)
  は y=1..17 で全称。clip 窓 2y+2 は y=5..17 の 13 族連続で tight
  （y=17 は 36・最初違反歩み 5 点）。
- **範囲外の維持**: 標準 11×11 の空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は UNKNOWN のまま。3トークン以上・y>=18 族・固定幅・q点版は
  範囲外（y=18 fit は別の単一オーナー宣言が必要）。
