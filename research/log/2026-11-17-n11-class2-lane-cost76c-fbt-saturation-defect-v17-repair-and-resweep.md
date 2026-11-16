# 2026-11-17：cost76c raw sweep完全独立再実行で発覚したfbtORキャッシュ飽和欠陥、v17修復、76候補再スイープ

開始時の最新mainは `1de5c46a1c1abbb6603a63709fa3f0c30a449fb9`（76c raw sweep監査ピン確定後）。作業前に `AGENTS.md`、`research/knowledge/README.md`、cost76c claim v3、head-1452 presweep、76c raw sweep監査ログを確認した。cost64h fold receiptは未着地・並走claim済みのため着手していない。

## 出発点：三重の独立検証

76c（child `00000000010000809002000001000000`・76候補・head 1452基底）の並走sweep完走に対し、この環境で確立済みのレーン手順を3つ実施した。

1. **出版Python監査器の初実行**: `audit_cost76c_raw_batches_20261117.py` は出版ログで「Python実行環境を確保できず未実行」と記録されていた。本環境で初めて実行し **18/18 PASS・nodes 141,221,576再現**。再生成JSONは出版監査JSONと意味的に完全一致（`blob_sha1`/`raw_blob_sha1` 鍵名差・role/note文言差・鍵順序差のみで、全数値・全check値が同一）。出版監査の結論はそのまま確定した。
2. **v16完全独立再実行**: repo-verbatim v16 runner（blob `0a4a86f6`）を新規環境で同じbatch分割・depth 10・cap 1e9・andclose 1で76 bit全部再実行。**76/76 node-exact**（msのみ相違）・pilot 10/10（3402）・nodes総和141,221,576。出版raw batchの忠実性は完全に確認された。
3. **v15 cross-engine全bit照合**: v15 runner（blob `8744fc65`）で76 bit全部を再実行（nodes総和444,779,818・pilot 5/5 at 5949）。**75/76一致、bit 113のみ不一致**（v16出版 WIN7-D10 vs v15 REFUTED-D10 @16,811,999 nodes・非capped）。

## verdict順序依存の発見（engine不健全性の実証）

bit 113の不一致を調査するため、move orderingのみを変えて（`--andclose 0`）再実行したところ、**完全探索であるはずのverdictが順序で反転**した。

| bit | v16 c1（出版） | v16 c0 | v15 c1 | v15 c0 | v17 c1 | v17 c0 |
|---:|---|---|---|---|---|---|
| 61 | WIN 752,696 | WIN 982,127 | WIN 4,301,193 | WIN 4,587,846 | WIN 752,696 | WIN 982,127 |
| 99 | WIN 4,168,961 | **REFUTED** 4,738,822 | WIN 10,649,504 | **REFUTED** 9,265,533 | WIN 4,140,409 | WIN 8,231,656 |
| 113 | WIN 8,174,662 | **REFUTED** 9,875,922 | **REFUTED** 16,811,999 | REFUTED 16,445,119 | **REFUTED** 7,893,054 | REFUTED 14,700,323 |

- v16: bits 99/113 が順序で反転（c1=WIN / c0=REFUTED）。bit 61は不変。
- v15: bit 99 が順序で反転。**両engineに共通の欠陥**。
- AND-OR完全探索（非capped）はmove orderingでverdictが変わるはずがなく、少なくとも一方のverdictが誤りであることが実証された。

## 根本原因：fbtOR fb cacheのprobe打ち切り黙落とし

v15/v16共通コード `fbtOR` のfb cache（FBS=2^17 slot・probe上限48）は、**probe chainが48を超えると当該三重項の円遮断mask更新を黙って捨てる**（ループ打ち切り後にmask適用なしでreturn）。fb表が約1.16e5 unique triple で飽和すると以降の三重項が黙落としとなり、遮断済みセルが合法手に現れる。つまり**探索するゲーム自体が変質**し、黙落としの位置・個数がtraversal順序依存になる。

計測（v16にcounterのみ追加したprobe版・node数は無計測版と完全一致）:

| bit | andclose | fbtDrops | fbtInserts | verdict |
|---:|---|---:|---:|---|
| 61 | 1 / 0 | **0** / **0** | 70,209 / 70,569 | WIN / WIN |
| 99 | 1 / 0 | 37,236 / 71,808 | 115,827 / 115,165 | WIN / REFUTED |
| 113 | 1 / 0 | 396,102 / 534,900 | 122,449 / 122,278 | WIN / REFUTED |

**verdict反転はdrops>0の構成でのみ発生、drops=0のbit 61は全構成で順序不変**。相関は完全。

## v17修復と全76候補再スイープ

`class4_child1_runner_v17.ts`（blob `c132cc64`）: probe打ち切り時に**cacheせず直接計算してmask適用**するfallbackを追加しただけの最小修復。検証:

- pilot d6 = 3402（不変）。非飽和探索はv16とbyte-identical（bit 61 c1 752,696 / c0 982,127）。
- bits 99/113 は両順序で同一verdictに安定（99: WIN、113: REFUTED）。

v17で全76候補を同じbatch分割で再スイープ（pilot 10/10・nodes総和144,218,750）:

- **verdict反転はbit 113の1件のみ**: WIN7-D10 → **REFUTED-D10**（7,893,054 nodes）。v16出版のbit 113 WINは**偽陽性**と確定。
- 27 bitはnode数のみ変化（飽和していたがverdictは不変）。48 bitはv16と完全一致（非飽和）。
- **訂正された76c行のverdict: WIN7-D10 bits {61, 99}・bit 113 REFUTED-D10**。

## 含意（次回以降への必須事項）

1. **76c claim「3 WIN bits 61/99/113」は「2 WIN bits 61/99」へ訂正が必要**。bit 113は証明書抽出・fold対象から外すこと。並走のcandidate manifest marginals（3 WIN前提）はbits 61/99について再導出が必要。
2. bit 99のWINはv17両順序+v15(c1)で支持。bit 61は無影響（drops 0・byte-identical）。両bitの証明書抽出は継続して妥当。ただし抽出器もfbt影響を受ける可能性があり、**証明書は既存どおり独立検証器（BigInt余因子・Bareiss・円方程式）合格をもって唯一の証明とすること**（この仕組みが本欠陥に対する最終防壁として機能した）。
3. **飽和探索のv16/v15 verdictは両方向に信用できない**。過去laneのREFUTED-D10 verdict（特にnode数が大きいbit）は証拠として使う前にv17再スイープが必要。ただし**fold済みWIN receiptは証明書が独立検証済みであり証明として有効のまま**。REFUTED-D10はもともとLOSS証明ではない。
4. v17は未飽和領域でv16とbyte-identicalのため、既存のdeterminism pin（pilot 3402・小規模bit）と矛盾しない。

## 保存物

- 修復engine: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts`（blob `c132cc64`）
- 監査JSON: `output/class2-lane-cost76c-v17-sweep-and-fbt-saturation-audit-20261117.json`（全入力blob pin・18構成order matrix・per-bit飽和表、2回実行byte-identical）
- 検証器: `scripts/verify_cost76c_v17_fbt_audit_20261117.py`（55 checks・Python標準ライブラリのみ）
- raw証拠: v16独立再実行batch1-10・v17再スイープbatch1-10・v15 crosscheck 5本・order matrix 7本・fbt probe 6本（いずれもJSONL）
- 本ログ

## 追試：cost64h全64候補のv17再検査（in-flight fold基盤の無影響確認）

同じ欠陥が過去laneに影響したかを確定するため、in-flightのcost64h fold（並走実行中・prereg済み）の基盤となった64h sweep（child `00000000000000403800000008100000`・64候補・23 WIN7-D10 + 41 REFUTED-D10）をv17で全bit再実行した。

- **64/64 bitがv16出版記録と完全一致**（verdict・nodes・capped・terminalStoneRange・andclose全項目・nodes総和47,017,565も同一）。pilot 5/5。
- つまり64h行は全体として**fb非飽和**で、fbt欠陥の影響を受けない。23 WIN receipt（証明書二重検証済み）と41 REFUTED簿記のいずれもv17で正確に再現された。**in-flightの64h fold（head 1452→投影1472）の基盤に欠陥の影響はない。**
- 保存物: `output/class2-lane-cost64h-v17-full-row-recheck-20261117.json`（全入出力blob pin付き）+ v17 chunk 5本（win 2 + refuted 3）。

76cと64hの対比から、飽和の実務的しきい値は「そのbit探索のfb unique triple が約1.16e5を超えるか」であり、76cの大規模bit（4-17M nodes）では発生し、64h（最大3.5M nodes/bit・行全体47M nodes）では発生しなかった。node数のみでは判定できず、v17でのnode数不一致（またはprobe計測）が飽和の検出器になる。過去の他lane（65n/66c等、bitあたりnode数が大きいもの）のREFUTED verdictを planning入力に使う前のv17再検査を次回以降の課題とする。

## 追試2: cost64e STERILE行のv17再検査（STERILE判定基盤の無影響確認）

STERILE判定はK0863の深さ10非閉鎖性定理を通じて共有class-2 parentの実効closable需要に影響するため、fbt欠陥がSTERILE判自体を覆す可能性を閉じる必要がある。共有parentの最安行cost64e（child `0000000000000000380000000a002000`・64候補中60候補をv16掃引・全REFUTED-D10・4候補はD4転写）をv17で全bit再実行した。

- **60/60 bitがv16出版記録と全フィールド一致**（verdict・nodes・capped・terminalStoneRange・andclose、nodes総和39,961,790も同一。異なるのは実時間msのみ）。pilot 3/3（3402）。
- 最重bit 32（3,279,693 nodes）・bit 21（3,270,894）・bit 118（2,185,077）を含む全bitがv17で正確に再現され、**64e掃引分行全体がfb非飽和**。なおv17再実行は出版v16と異なるバッチ分割（20bit×3 vs 8bit×7+4）でもnode-exactであり、この行についての順序不変性も同時に観察された。
- よって**STERILE判定とK0863帰結は掃引基盤上で変わらず有効**。ただし4つの転写bit（70/104/115/119）は他行の出版verdictのD4正準同一性転写であり本再検査の対象外で、それらの源流行のv17再検査は既存の過去lane再検査キューに含まれる。
- 保存物: `output/class2-lane-cost64e-v17-full-row-recheck-20261117.json`（全入出力blob pin付き）+ v17 chunk 3本（refuted）。

76c（飽和あり・反転1件）、64h（最大3.5M nodes/bit・無影響）、64e（最大3.3M nodes/bit・無影響）の3行の再検査が揃い、**node数がbitあたり3.5M以下の行はこの2例ではいずれも非飽和**という経験則が得られた。ただし飽和はfb unique triple数に依存しnode数からは判定できないため、検出器は引き続きv17でのnode数不一致（またはprobe計測）とする。

## 信頼境界

v17自体の健全性は「両順序でverdict不変・非飽和領域でv16一致・pilot不変」による強い証拠だが、形式的検証ではない。bits 61/99の最終確定は証明書の独立検証合格による。bit 113のREFUTED-D10もLOSS証明ではない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
