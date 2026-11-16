# 2026-11-16 n11 class2-lane: cost-65j stale-claim takeover・sweep完走（65/65）と17 WIN7-D10 receiptsのfold前cover map

## やったこと

1. **重複stale claimの発見とtakeover**。cost-65f claim（2026-11-14・batch 1-7/9で放置・56/65候補・13 WIN7-D10既出版）とcost-65j claim（2026-11-15・batch出版ゼロで1日停滞）が同一child `00000000000000809102000080000000`（第三class-2 target S5 `00000000000000809102000000000000`の最安child・cost 65・65合法候補）の重複claimであることを特定。最新main（commit `7c99621f`）で他のtakeoverがないことを確認し、claim v2 takeoverを出版（`7f2d1bd9`）してからsweepを開始した。
2. **残候補の事前解決の再利用**。bit 113はtheorem-applicability scan（`2d090b49`・第二独立検証 `7c99621f`）のcanonical identity transfer（via child `00000000000000809102000000000008` bit 97）でREFUTED-D10事前確定済みのため再実行せず、残りは8 bit（111,112,114,116,117,118,119,120）。8 bitすべて合法候補であることを独立Bareiss実装で再検証してから実行した。
3. **sweep完走**（v16 `class4_child1_runner_v16.ts`・depth 10・cap 1e9・andclose=1・pilot d6 3,402 nodes両バッチPASS）。
   - batch8（bits 111,112,114,116,117,118,119）: **4 WIN7-D10**（bit 112: 3,673,038 nodes・bit 116: 1,235,013・bit 118: 7,987,181・bit 119: 1,788,624）+ 3 REFUTED-D10（111: 22,542・114: 651,409・117: 436,186）
   - batch9（bit 120）: REFUTED-D10（1,929,932）
   - raw batch出版 `738e33e3`・claim v3 completed `0d6be9d5`・**v4 erratum**（v3のrefuted_bitsリストがbit 92抜け〔65f batch6・loss=false nodes 1,228,321〕・total 48は正しくlist 47件→48件訂正）`614d0ac2`。
   - これでchildは**65/65確定: 17 WIN7-D10（65f 13 + 65j 4）・48 REFUTED-D10（65f 43 + 転送1 + 65j 4）・0 capped**。
4. **fold前cover map**（`analyze_cost65j_win_marginals_20261116.py`〔`1f3960ab`〕 + `class2-lane-cost65j-win-marginals-20261116.json`〔`6d46cb72`〕・stdlib・Bareiss・独立D4・engine不使用・再実行byte-identical md5 `65f77eb0…`）。17 WIN receiptsの全7削除canonをMS5 S6 manifest（7,867行）と照合:
   - **34行がcover対象**（union）。65j自身の行（cost 65）は全17 receiptがcover。他33行はcost 61-77（大半class-2、bit 101はclass-6の2行とclass-4の1行もcover）。
   - 2行は複数receiptでcover（`…809102000000200000` bits [21,109]・`…809102000002000000` bits [25,91]）。
   - 最安のcover行はcost 61 `00000000000080003800000008080000`（bit 91）とcost 62 `00000000020000003800000008080000`（bit 101）。
   - **セッション観察の再導出**: 未sweep cost-64行 `00000000000000003800000008002002` と `00000000000000003800000008003000` は65f bit-21 / bit-20 receiptにcoverされることを同スクリプトがassert付きで再現（theorem-applicability scanの133 targetsに未収録の行）。
   - 34行のうちいくつがhead 1410でまだopenかはfoldが決める（本mapはopen/closedを主張しない）。

## セッション中の補助的観察（環境リセットでローカル成果喪失・結論のみ記録）

- 全lane raw batch（903件・claim経由child逆引き・Bareiss合法性再検証・D4正準形集約）の**canonical root verdict転送cache**を第三の独立実装として構築・実行した: 95 sweep・5,570 distinct canonical root・verdict **conflict 0**（corpus全体で初の一貫性監査）・K0863正の対照（70f bit84 == 70g bit29・WIN-WIN）再現・同一canon複数出处一致1,058組・legality fail 4件は並走第二検証が特定した69h batch2の非合法bitsと一致。tool本体は以下の環境リセットで喪失したが、同役割は並走のscan（`2d090b49`）+第二独立検証（`7c99621f`）がmain出版済みであり再構築不要。
- 上記cache構築時に、WIN転送（canon一致で未sweep候補が既出版WIN receiptと同じ位置になること）が2件見つかり、65f/65j sweepの価値判断の根拠となった（65f bit-20/21のcover行）。

## 環境リセット事故（実験事実）

sweep起動直後のbash呼び出しがKoyeb 503 upstream resetで失敗した時点で実行環境が全体初期化された（前セッション構築のlane作業コピー1.4GB・git smart-HTTP client・fold chain再構築鎖の進捗〔62aまで完了〕を喪失）。**raw CDN単ファイル取得+v16 runnerのpilot gate（3,402 nodes）で最小再構築すればsweepは即座に再開できる**ことを確認し、実際にtakeoverから完走までを完了した。重要成果はすべてpush済み（claim v2-v4・raw batch8/9）のため証拠喪失なし。

## レジューム

- canonical head **1410不変**（65jはsweep完了のみ・foldで進む）。
- **次回の65j fold**: (1) fold chain再構築（lane dir+MS5 dir取得→reconstruct scripts依存順84a→83d→83c→83a→69i→62a→58c→63h→63i→63j→65m→67d→70g→`recompute_frontier_cost60c_receipts_20261116.py`でhead 1410再現） (2) `recompute_frontier_cost65j_receipts_20261116.py`新規作成（17 WIN receiptsを1410にfold・閉鎖候補はcover mapの34行とhead 1410 remaining setの交差・65j自身の行と65f bit-20/21の2行は確度高い） (3) 証明書要件の確認（60c foldのreceiptはcertified:true・4新規WIN rootのcert extractionが必要か・65f 13 WINの証明書不在も確認） (4) 17 receipts vs 1410時点713 folded rootsのroot disjointness assert。
- **69h batch2/3 raw再出版**が未対応の残課題（`7c99621f`のデータ品質観察: batch2はbits [12,15,18,23]の再実行が必要・batch3はbits [24,25,26,28,29,30,32,33]・audit aggregateとnodes一致確認）。
- 69a（並走in-flight）は着手禁止。着地時にK0863予測（bit 109 REFUTED-D10）を確認。76d/77e fold着地時は1410 headとのreconciliation必須。
- **solved 1410はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4はいずれもUNKNOWN**。
