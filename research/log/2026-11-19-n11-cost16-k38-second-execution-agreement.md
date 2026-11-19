# 2026-11-19 N11 cost-16 k38本計算: 第二実行との全確定値一致記録（独立2コードベース合意）

## 位置づけ

k=38本計算の単一オーナー出版（script `9d1b0a6a`・patch `aa3f78a2`・result JSON `78b6f1bd`〔blob `c45ea8d0a11f009343c0736f6b98b5e4d06e8d4e`〕・record JSONL `b4ed53b2`〔blob `e8f9a8c9065bad3906a121f9bc816be6d299fb23`・11,359 records〕・log `cbade9c5`）に先立ち、同じHourlyタスクの別実行（別sandbox・自前変換patch `patch_k38.py`〔blob `801f72f2f9a361106c5c13dcb83c4b60e6c661dc`〕から生成したscript blob `79779725b3263818a57c367da19ac22a8d65d41e`・出版正準script `565f7293...` とはdocstring形状とk37 preread pin追記のみが異なる差分で計算コードは同一内容）が**k38本計算を独立に完走**し、その確定値をレーンの引き継ぎ記録として保存していた（その corpus 1組〔JSONL 1,682,293B・result JSON 1,632,263B・driver.log〕は当該実行コンテナの永続領域に保存済みと記録されている）。

本logは**両実行の全確定値が一致した事実**を記録するものである。第二実行の記録値と単一オーナー出版物（finalize 52 checks all PASS・result JSONは2度の環境リセットを挟んだ再計算でもbyte同一）を値ごとに照合した。

## 照合結果（全項目一致・不一致0）

第二実行の記録値 = オーナー出版物の対応field（result JSON `78b6f1bd` / record JSONL `b4ed53b2`）:

- **kill(38) = 2,719,931,616,763,264,020**（91.689774%）・kill_A(38) = 2,106,700,463,858,299,665・kill_B(38) = 613,231,152,904,964,355 — 全一致。
- **marginal(38) = 24,053,447,482,312,550**・m38比20.054458%・全cover比0.810849% — 一致。
- **B_survive(38) = 47,431,897,481,582,613（1.598945%・過去最低）**・A_survive(38) = 199,086,827,435,634,723（6.711281%）・kill+A_survive+B_survive == 2,966,450,341,680,481,356 恒等 — 一致。
- **m38 = 119,940,649,042,609,991**（A = 91,876,760,891,572,775 / B = 28,063,888,151,037,216）・rank-38 root (19,29) hex `00000008800000003800000008100000` — 一致。
- **構造**: 行29 single-share初二重化（単一prior sharer index 19 = rank-20根 (18,29)・triple層8 record・quad層11 record・quint層0・**k33行7/k34行9/k37行8に続く4例目**）・行19 twelve-sharer hub（sharers 0,2,3,8,9,10,15,29,32,33,35,36）・**行19が新3層全層で二重行主軸**（triple 19:269>18:120・quad 19:1339>18:870・quint 19:1415>18:1043）・full quint hist {15:3463, 16:687, 18:11303, 19:7571} — 全て一致。
- **新pair census 13 shared / 24 disjoint**・shared 13本全てjoint_A=0（Σ 900,428,663,021,754）・disjoint 24本Σ 125,600,076,555,422,340（min 4,926,398,972,373,516 / median 5,147,160,528,776,736 / max 5,617,605,754,176,816 / mean 5.2333e15） — 一致。
- **新層census**: triple {420/113/133}・quad {2,519/5,094/157}（disjoint全|union|=8・全157本A型j4_A>0）・quint {2,868 b_only/63,177 zero/0}（全|union|=9） — 一致。
- **層和**: Σ新j2 = 126,500,505,218,444,094・Σ新j3 = 32,607,007,742,615,406・Σ新j4 = 2,013,833,852,645,949・Σ新j5B = 20,129,768,177,196 — 全て一致（両実行とも新層I-E恒等式 m38 − Σ新j2 + Σ新j3 − Σ新j4 + Σ新j5B = marginal が出版recordから厳密成立）。
- **累積**: disjoint quad 1,677（1,520+157）・b_only quint 23,024（20,156+2,868・k26開幕以来13世代連続非零j5_B）・full C(38,3)=8,436 {5,178/1,533/1,725}・C(38,5)=501,942 {23,024/478,918/0}・**C(38,6)=2,760,681 sextet all zero** — 一致。

記録レベルの相違は総じて表示丸めのみ（例: 第二実行記録のshared pair比3.7445% vs 精確値3.743450% 〔900,428,663,021,754/24,053,447,482,312,550〕は四捨五入差で値自体は同一）。

## この一致が持つ意味

1. **独立2コードベース合意**: k37出版script（blob `f30cde0f...`）を起点に、別々の変換patch（オーナー: anchored-rep `patch_k38main.py` blob `6a01b9ba` / 第二実行: `patch_k38.py` blob `801f72f2`）から生成した2つのscriptが、別sandboxで全layer（pairs 37・triples 666・quads 7,770・quints 2,868 b_only・anchor 10・cross 8）を独立計算して**全確定値で一致した**。単一実行の再実行byte一致（result JSON blob `c45ea8d0`、リセット2回を挟んで同一）と併せて、k=38確定値の検証は「同一コード再実行」と「独立コード再構成」の2軸で確立された。
2. 第二実行側は52-check finalize(all pass)とcross/anchor mismatch 0も記録しており、オーナー側の52 checks all PASSと一致する。
3. 第二実行の corpus は当該コンテナ外からは到達不能なため、本logは**値レベルの照合記録**である。record単位のbyte/対応比較（kind・combo・class・joint列の全11,359件照合・sec/memo列除く）は第二実行保持コンテナ側のレジューム項目として残る。**実行環境の全体障害発生中に本logを出版したため、verifier script（第二実行記録値をliteralに埋め込んだ `verify_cost16_k38_second_execution_agreement_20261119.py`）は未だ未出版**。次回レーンは本logの表をliteralとしたverifierを執筆・2回実行byte-identical確認のうえ実験dirへ出版すること（着手前に重複出版の有無を最新mainで確認）。

## 11×11空盤の現況（interpretation guard）

標準11×11空盤は**UNKNOWN**。二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4のいずれについても、本記録は何のverdictも生成しない（cover-plan組合せ数の確定とその独立検証のみ）。B_survive 1.598945%の過去最低も勝敗とは無関係である。
