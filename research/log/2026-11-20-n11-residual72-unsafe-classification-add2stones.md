# n11 残余72行 fresh-unsafe 2,871本の構造分類と add-two-stones 拡張census（2026-11-20）

単一オーナー宣言ノート
[2026-11-20-n11-residual72-unsafe-classification-add2stones-single-owner-note.md](2026-11-20-n11-residual72-unsafe-classification-add2stones-single-owner-note.md)
に従い、K1075（残余72行のfull cache-join候補供給再構築）README「次の一手」第2項
（fresh-unsafe 2,871本の構造分類 + 残余72行への add-two-stones 拡張census・コスト見積り）
を実行した。**一切の新規掃引・新規判定・証明書抽出・receipt fold・行の閉鎖は行っていない。**
追加した計算はすべて幾何・組合せ・出版記録の集計である。

- 機械: `research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/unsafe_classification_add2stones_20261120.py`
  （SHA-256 `f5ef884622d64d981aa90b869790db4ef3143b23c5d1dc78d4fb663b65df275e`・89,094 bytes・stdlibのみ・コンパイルOK）
- 正本: `research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/output/residual72-unsafe-classification-add2stones-20261120.json`
  （39,221 bytes・SHA-256 `5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e`）
- 決定論: 3回実行（repo実験dir 2回＋別cwd別プロセス `/tmp/cwdtest` 1回）すべて同一SHA-256でbyte-identical。
  実行時間は約2分/回（_production corpus収集込み）。
- checks: 全39 gate PASS（failed_checks空）。

## 入力と信頼境界

出版済み正本のみをSHA-256 pinで入力: K1075候補供給正本（`49b6f85f…`）・resolve6正本
（`e85d4bfb…`）・resolve5正本（`5a2f4815…`）・fold9正本（`24db2352…`）・fold10正本
（`bed7d331…`）・sv17 38gate正本（`c1073bae…`）・39 live掃引正本（`22953ae1…`）・
resolve7正本（`207f4094…`）・sweep43掃引正本（`7940638f…`）・sweep39 dead掃引正本
（`f8608d0a…`）に加え、K0863 scan corpus（manifest 1,279 entries・1,272 sha256 verified・
post-scan changed 7ファイル除外・unresolved raw 10 entries除外はK0863収集契約通り）。
残余72行のbase stateはresolve5 78行−fold9 4行−fold10 2行のK1075と同一 derivationで
全数値gate再現。幾何はすべて厳密整数演算（行列式）またはexact Fractions（外心）。
corpus追加は単調でengine mapと両joinで衝突gate fail-closed。

## 宣言文言との差分: stage-1 verbatim一致からera-drift記録+pool identity gateへ

宣言ノートは「K1075機械のstage-1〜3をverbatim再実行し、出力が出版正本SHA-256と
一致することをfail-closedで要求する」と書いた。これは当時の想定では正しかったが、
実行時に**現mainのcorpusにはK1075出版後に併走レーンが追加した正当なファイルがある**
ことが判明した: engine bitsはresolve6-era再構築の8,960に対して現corpusでは10,261
（K0863出版scanの8,964も超える）、unresolved raw entries 10個、per-target-child
engine分布は2 childでpublished scanと不一致である。corpusへの追加は判定の追加のみを
もたらす単調変化なので、**resolve6-era verbatim一致は現corpusでは原理的に成立しない**
ため、stage-1 gateを以下の等価なfail-closed構成に置換した。

1. **era-drift記録**（gate `era-drift-recorded`）: 再構築phase-1 joinのjudged
   canonical roots 8,511（REFUTED 7,655・WIN 856・WIN/REFUTED衝突0・cache engine
   8,325）をrecord。published resolve6-era値（7,493 judged・6,707/786）との差分は
   追加judged根のみ（単調性gate）。universe再構築7,969はpublishedと完全一致。
2. **fresh-unsafe pool identity gate**（`fresh-unsafe-pool-identity-stable`）:
   corpus追加は判定を追加するだけなので、再構築fresh-unsafe poolはpublished K1075
   の2,871本の部分集合にしかなりえない。実際の再構築数がちょうど2,871と一致する
   ため、**部分集合かつ同数は集合としての同一を強制する**。併せて追加judged 179根
   がすべてfresh-safe側に落ちたこと（fresh-safe 4,109→3,930・3,930+179==4,109・
   judged REFUTED 468→647・WIN 0で不変）を別gateで検証した。

この置換により、stage-A/B/Cの全統計は**published K1075のfresh-unsafe membership
（2,871本）の上の計算として厳密に有効**である。era-drift gateのrecord文言通り、
published K1075 stage-1のverbatim一致は現corpusでは要求していない。

## 現corpusでの add-one 計画状態: stranded 1行の発生（K1075からの変化）

eroded fresh-safe pool上でadd-one witness計画を再照合すると、行
`0000000000000000380000000a002000` が**fresh-safe add-one候補を持ち尽くした
stranded行**となる（fresh-safe pool 3,930・pair coverage hist {1: 2,778, 2: 93}・
maximum matching 35・greedy set cover 39・witness 36で72行中71行のみ被覆）。
K1075のresolve6-era corpusではstranded 0（matching 36）だったが、期待ハズレでは
なく宣言文言・正本noteの通りcorpus era driftの帰結である。**よって現corpusでは
add-one witness計画単独で72行を覆う計画はもはや存在せず、これがadd-two-stones
拡張censusの直接の動機になる。**

## Stage A: fresh-unsafe 2,871本の構造分類

2,871根の禁止四つ組は合計3,279個で、per-root分布は {1本: 2,482, 2本: 370, 3本: 19}。
分類は:

- taxonomy: **collinear 670・axis_rect 189・axis_square 20・other_circle 2,400**
- other_circle 2,400の外心（exact Fractions）は**28種類のtype class**で、
  half/half（両座標半整数）1,774・int/int 340が支配的（残余はden4/int型など
  小頻度26種）。外心typeはother_circle限定で数える（axis矩形を含めると1,956種
  側の読みになるため configsとは別管理）。
- circle/line support: other_circle 2,609円すべてsupport 4（5番目の石で禁止円を
  延長するrootはゼロ）、collinear 670線すべてsupport 4。
- 行被覆面: covered row events 2,964・coverage per root hist {1: 2,778, 2: 93}・
  pair_quad_incidence 3,372 == with_added_stone 3,372（**全四つ組が追加石を含む**）・
  inside_row_image 0（単一の行イメージの内部では四つ組は完成しない）・残余72行は
  すべて quadruple-free（`stageA-rows-quad-free`）。

## Stage B: add-two-stones 拡張census

残余72行それぞれに2石追加した8石root宇宙をgeneration witness方式
（72行×C(121,2)ペア、行内既存7石位置はskip → 471,960 events → canon正準化dedup）
で構築すると、幾何定義 {r: ∃t: r_mask ⊆ t の追加2位置を含む} と厳密に一致する
（これは実行で示した: eventsのcoverage記録と幾何再計算が同一になる）。

- **universe82: 380,098根** = safe8 120,474 + unsafe8 259,624
  （`join_judged_cross_roots` 0: 8石rootは7石judged canonicalと構造的に交差しない）
- safe8 coverage hist: {1行のみ: 82,602, 2行: 33,104, 3行: 4,718, 4行: 50}
- per-row safe8 demand: 72行すべて正（1,714〜2,944・**zero-demand行ゼロ**）
  ・demand sum 163,164
- safe8判定は56 triple det3事前計算+70 quad det4差分+early exitで380,098根を
  約9秒で処理（実装メモ: with_added判定は盤面positionでなくbits listのindexで
  quadruple indexと比較する）
- coverage crosscheck: multi-cover（>=2）37,872本を含む39,255根で幾何再計算
  （C(8,6)=28 six-stone subset全件）を独立実行し、**mismatch 0**
- **greedy set cover: 23根で72行を完全被覆**（gains {4: 7, 3: 13, 2: 2, 1: 1}・
  leftover 0）。judged除外変形で同一結果（交差ゼロのため）。
- **情報論的下界: ceil(72/4) = 18根**（1根は最大4行しか覆えない）

## Stage C: コスト参照と計画算術（出版掃引記録に基づく）

出版済み3掃引正本をPINSから読み出し:

| 掃引 | roots | probes | nodes総計 | WIN/REFUTED |
|---|---|---|---|---|
| sweep43（K1057）| 43 | 86 | 173,165,148 | 4 / 39 |
| sweep39 dead（K1059）| 39 | 78 | 115,940,695 | 0 / 39 |
| sweep39 live（K1069）| 39 | 78 | 169,615,508 | 1 / 38 |

plan arithmetic:

- add-one witness: 36根 → 両順序72 probes（ただし現corpusでは1行strandedで
  計画として72行を覆わない）
- **add-two greedy: 23根 → 46 probes で72行を完全被覆（leftover 0）**
- add-two下界: 18根 → 36 probes
- breakeven: Fraction(72,46) == Fraction(36,23)。**add-two greedy掃引は全体被覆
  のためにadd-one witness計画の23/36のprobesで足りる**（下界36 probesとgreedy46
  probesの間に43%の最適化余地が残る）。

caveat 3文言: (1) node costは7石計測ベースで、8石probeはより深い木を探索するため
probeあたりnode数は上昇しうる（plan arithmeticはroot/probe数の比較であって厳密な
node cost予測ではない）、(2) greedy・witness listは条件付き計画で証明書ではない
（行閉鎖には証明書抽出＋独立二重検証が必要）、(3) REFUTED-D10はLOSS証明ではなく、
REFUTEDになった候補根の除去に過ぎない。

## status と解釈

status = `fresh-unsafe-classified-add-two-census-complete`。この記録は
**どの行も閉じない**。残72行は全行openのまま、fresh-unsafe分類・add-two census・
greedy/witness list はすべて候補供給の簿記・条件付き計画である。eroded fresh-safe
poolを考慮すると、add-one計画は72行の完全被覆を達成できず、完全被覆のための確定した
現実的な最小計画は add-two 8石候補となる（下界18根、greedyで23根、best-caseは
18〜23根の間にある）。REFUTED-D10はLOSS証明ではない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。**

## interpretation_guard（正本の文言）

1. REFUTED-D10はLOSS証明ではなく、depth-10飽和ラベルはrunner v16/v17移動モデル
   内の実験的node-identity判定である。
2. fresh-unsafe分類・add-two census・すべてのgreedy/witness listは条件付き掃引計画
   であって証明書ではない。行閉鎖には証明書抽出＋独立二重検証が別途必要である。
3. corpus era drift: 現main corpus上の再構築joinはpublished resolve6-era統計を
   正当なpost-K1075追加分だけ超える。fresh-unsafe pool identityはgate済みだが、
   将来のcorpus追加はfresh-safe側にさらに判定を追加しても本記録を無効化しない。
4. 本記録はどの行も閉じない: 残余72行はすべてopenのままであり、stranded/greedy
   coverage countは候補供給の簿記に過ぎない。
5. 標準11x11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はUNKNOWNのままである。

## 次の一手

- add-two 8石候補の実際のdepth-10掃引着手は宣言外（追加の単一オーナー宣言を要する）。
- greedy 23根計画の46 probesは、12 fresh-safe witness掃引（宣言済み別オーナー）と
  併走する場合も独立に全部件が実行可能な規模である。
- fresh-unsafe 2,871本のうち、add-two universe82の unsafe8 側からどの程度が
  7石unsafe poolの近傍に潜むかの解析は今回対象外。

## 備考: knowledge item番号の再採番

本レーンの実験着手時の仮番号K1080は、push前の最新main確認で併走レーンの
z=17・y=5境界切片（K1080-two-token-z17-y5-boundary.md）に先行取得されていた
ことが判明した（K1081 depthplus cost scaling・K1082 nodecost ledger・
K1083 z18-y4境界切片・K1084 36-root三手先frontier第二検証も同時に出版済み）。
AGENTS.md規約（K1060・K1073と同じ運用）に従い、本レーンのknowledge itemは
K1085へ再採番した。実験dir（K番号を含まない）・機械・正本（schema
`n11-residual72-unsafe-classification-add2stones-20261120-v1`）・単一オーナー
宣言ノート・知識README bulletリンクの実験側パスはすべて番号非依存であり、
正本SHA-256 `5fdd342d…`は変更なく有効である。
