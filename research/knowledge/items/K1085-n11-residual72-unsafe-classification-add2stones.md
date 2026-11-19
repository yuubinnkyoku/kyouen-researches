---
id: K1085
title: 残余72行 fresh-unsafe 2,871本の構造分類と add-two-stones 拡張census: corpus era drift下のpool identity gate・8石候補宇宙380,098根・greedy 23根完全被覆とplan arithmetic
kind: computation
status: computed
topics: [search-methods, geometry, certificates]
aliases:
  - structural classification of the 2,871 fresh-unsafe add-one candidates of the residual 72 rows
  - add-two-stones expansion census for the residual 72 rows (universe82 = 380,098 eight-stone roots, safe8 120,474)
  - greedy set cover of size 23 roots covers all 72 rows with zero leftover; information-theoretic lower bound 18 roots
  - add-one fresh-safe pool erosion on the current corpus leaves one row stranded, motivating the add-two expansion
relations:
- type: depends_on
  target: K1075
  note: 候補供給正本（SHA-256 49b6f85f…）のfresh-unsafe 2,871本とresidual72 base stateを引き継ぎ、pool identity gateでmembershipを固定
- type: depends_on
  target: K1072
  note: resolve7正本（207f4094…）。72行の出自・割当表の読み出しとlive39-supply status gate
- type: depends_on
  target: K1063
  note: resolve6機械のcorpus/engine map/join構造を再利用（現corpusではera driftを記録しverbatim一致は不要）
- type: depends_on
  target: K1069
  note: sweep39 live掃引正本（22953ae1…）をcost referenceとして読み出し
- type: depends_on
  target: K1059
  note: sweep39 dead掃引正本（f8608d0a…）をcost referenceとして読み出し
- type: depends_on
  target: K1057
  note: sweep43掃引正本（7940638f…）をcost referenceとして読み出し
artifacts:
- path: research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/README.md
  role: document
  note: 実験README（入力正本のSHA pin・要約・解釈・再現方法）
- path: research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/unsafe_classification_add2stones_20261120.py
  role: verifier
  note: corpus収集・両join再構築・era drift記録・fresh-unsafe pool identity gate・Stage A幾何分類・Stage B 8石census・Stage C plan arithmeticの全39 gate fail-closed機械（stdlibのみ・3回実行byte-identical）
- path: research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/output/residual72-unsafe-classification-add2stones-20261120.json
  role: data
  note: 機械可読正本（SHA-256 5fdd342d…・全39 checks PASS・interpretation_guard 5文言同梱）
- path: research/log/2026-11-20-n11-residual72-unsafe-classification-add2stones.md
  role: log
  note: 宣言文言との差分（stage-1 verbatimからera-drift記録+pool identity gateへの置換）の経緯とStage A/B/Cの全数値の記録
- path: research/log/2026-11-20-n11-residual72-unsafe-classification-add2stones-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（先行出版済み）
scope: >-
  K1075が確定した残余72行のadd-one候補のうち未判定かつunsafeな2,871本
  （fresh-unsafe）の構造分類と、残余72行への2石追加（add-two-stones）拡張の
  候補宇宙census・コスト見積り。対象は候補供給の幾何・組合せ観察のみで、
  新規掃引・新規判定・証明書抽出・receipt fold・行の閉鎖は一切行わない。
  fresh-unsafe membershipはpublished K1075正本に SHA-256 pinで固定し、
  現corpusのera drift（post-K1075正当追加によるengine bits 10,261・追加
  judged 179根）は単調性とpool identity gateで吸収する。行のゲーム理論的値
  には一切言及しない。
evidence: >-
  （1）era driftとpool identity: 現main corpusのengine bitsはresolve6-era
  再構築の8,960を超える10,261（unresolved raw 10除外・manifest 1,279中
  1,272 sha verified・post-scan changed 7ファイル除外）で、published
  resolve6-era stage-1 verbatim一致は原理的に成立しないことを確定し、
  代わりにera-drift単調性gate（追加judged根のみ・WIN/REFUTED衝突0・
  universe再構築7,969はpublishedと厳密一致）とfresh-unsafe pool
  identity gate（部分集合かつcount 2,871一致が集合同一を強制・追加179
  judgedは全てfresh-safe側でfresh-safe 4,109→3,930・3,930+179==4,109を
  別gate検証）を課した。これによりStage A/B/C全統計はpublished K1075
  membership上の計算として厳密に有効。eroded fresh-safe poolでは行
  0000…380000000a002000がadd-one fresh-safe候補を使い果たしたstranded行
  となり（matching 35・greedy 39・witness 36で71/72行被覆）、add-one
  単独の計画では72行の完全被覆は不可能。（2）Stage A: 2,871根の禁止四つ組3,279個
  （per-root {1:2,482, 2:370, 3:19}）を分類し、collinear 670・axis_rect
  189・axis_square 20・other_circle 2,400、other_circle外心の28 type
  class（half/half 1,774・int/int 340支配）、circle/line support全4
  （延長rootゼロ）、covered row events 2,964、全四つ組が追加石を含む
  （pair_quad_incidence 3,372==with_added 3,372）、inside_row_image 0、
  残余72行は全行 quadruple-freeを確定。（3）Stage B: 72行×C(121,2)の
  generation witness（471,960 events）をcanon正準dedupした8石候補宇宙
  universe82 380,098根（safe8 120,474・unsafe8 259,624・7石judgedとの
  交差0）を、幾何定義との一致を39,255根の独立再計算（mismatch 0）で
  検証。safe8のcoverage hist {1:82,602, 2:33,104, 3:4,718, 4:50}、
  per-row demand 1,714〜2,944（zero-demand行0）、greedy set cover
  23根が72行をleftover 0で完全被覆（gains {4:7,3:13,2:2,1:1}）、
  情報論的下界ceil(72/4)=18根。（4）Stage C: 出版3掃引正本
  （sweep43 173,165,148 nodes・sweep39dead 115,940,695・sweep39live
  169,615,508）をsha pinで読み、plan arithmetic add-one 36根→72
  probes、add-two greedy 23根→46 probes、下界18根→36 probes、
  breakeven Fraction(36,23)を確定（add-two greedyはadd-one witness
  の23/36のprobes）。caveat: node costは7石計測ベースで8石probeは
  より高価になりうる、greedy/witness listは証明書ではなく計画、
  REFUTED-D10はLOSS証明でない。（5）決定論: stdlibのみ、3回実行
  （2回repo実験dir＋1回別cwd別プロセス）byte-identical（正本SHA-256
  5fdd342d…）、全39 gate PASS・fail-closed。本項はどの行も閉じない:
  残余72行は全行openのままである。REFUTED-D10はLOSS証明ではなく、
  分類・census・被覆は候補供給の簿記である。標準11×11空盤・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
  再採番備考: 実験着手時の仮番号K1080はpush前チェックで併走レーンの
  z=17・y=5境界切片（[K1080](K1080-two-token-z17-y5-boundary.md)）との
  重複を検出したため、AGENTS.md規約に従いK1085へ再採番した（K1080〜K1084は
  いずれも併走レーンの正当な出版items）。実験dir機械・output正本・
  単一オーナー宣言ノート・研究ログにK番号の依存はなく、正本SHA-256
  5fdd342d…は番号非依存ですべてそのまま有効である。
---

## 詳細

本レーンはK1075「次の一手」第2項（fresh-unsafe 2,871本の構造分類・
add-two-stones拡張census・コスト見積り）の単一オーナー宣言ノートを先行出版
のうえ実行した。era driftによりpublished stage-1 verbatim一致が現corpusで
原理的に成立しないことを確定し、fresh-unsafe pool identity gate（2,871本の
集合同一）で代替して全統計の正当性を担保した。残72行のadd-one fresh-safe
計画は現corpusで1行strandedとなり、add-two 8石候補（universe82 380,098根・
safe8 120,474）のgreedy 23根が72行をleftover 0で完全被覆すること、下界
18根、plan arithmetic breakeven Fraction(36,23)を確定した。どの行も閉じて
いない。実験着手時の仮番号K1080は併走レーンのz=17・y=5境界切片に先行取得
されていたため、AGENTS.md規約に従いK1085へ再採番した。
詳細は[実験](../../experiments/n11-residual72-unsafe-classification-add2stones-20261120/README.md)・
[分類・census正本](../../experiments/n11-residual72-unsafe-classification-add2stones-20261120/output/residual72-unsafe-classification-add2stones-20261120.json)・
[研究ログ](../../log/2026-11-20-n11-residual72-unsafe-classification-add2stones.md)。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
