# 2026-11-11 p2539の116点除外と空対26点gate

開始HEADは4130158feeb32bd857e3cf161e43b417e77ff53e、main。
AGENTS.md、knowledge README、現行K0693/K0702/K0706/K0727、最新logとexperimentを読んだ。
git -c maintenance.auto=false fetch origin main、status、実行中プロセスを確認。研究計算やremote追加はなかった。
前回fetch由来のGit repackは完了していた。他者の未コミットequality_screen_200k.jsonは保持した。

全体UNKNOWNの再実行でなく、保存された一点追加障害に元の完全対保持を組み込んだ。
以前の非自明辺は二つの完全対の四点を省いていた。
uの鏡像がS内なら{6,2533,u,2539−u}から鏡像の削除が必要であり、単点障害を追加できる。
1255四点を加えた全7769四点をgeneric整数4×4行列式0と実検査した。
bounded hitting証明木で116点を独立排除し、既存60点に56点を追加した。
負証明木はpacking248・branch99 node、残る1165点は必要障害族だけの削除証人。
元の60点のnative RUPと新規56点の幾何hitting根拠を混同しない。

追加・削除の鏡像単射から、厳密改善はSの元の空対13個に属する26点の少なくとも一点を追加する必要があると分かった。
その正26-literal ORを一行RUPとして親の保持側CNFだけで-f -U検査し、DERIVATIONを受理した。
空節ではなく、全体UNSATではない。Eの26点は今回除外した116点と交わらない。
回帰は272小seed・528完全対四点・6084削除例と5不正入力、加えて20880 seed/target組・2920厳密改善のgate確認。
有限回帰、具体的証明の受理、全称的なhitting・数え上げの論証を区別した。

同じ五点削除改善の必要条件の強化としてK0727を更新した。新しいKや全体探索は起動していない。
現在の1258..1271と全体UNKNOWNは不変。
次回はEの26点を親へ個別に仮定する異なる部分問題を検討できる。
全26仮定が独立排除できれば、正ORと負単位節を結んで完結証明にできるが、その探索は今回行っていない。
複数のE点を含む候補は複数仮定に属するので、これは互いに素な分割ではなく被覆である。
新規E仮定でSATならsigned modelを保持し、全CNFとgeneric整数全四点検査を経て安全証人を採否する。

最初の通常unittestは完了前に終了値1073807364で中断し、成功扱いにはしていない。
再開時のfetchでremote mainが213a7898へ進み、K0723〜K0727に別の公開済み項目が追加されていた。
未pushローカルの剰余放物線K0723〜K0727をK0730〜K0734へ再採番し、現行正本の参照を更新した。
今回の結論の現行正本はK0734。凍結した実験README・source・証明・receiptは保持し、番号対応は独立した統合logへ保存した。
統合後の検査をやり直す。既存の探索や証明生成を重複起動していない。

統合途中の通常33テストは旧リンクによるcanonical検査1件のfailureだった。
YAMLと参照の統合修正後、uv sync --locked、knowledge check（716項目、error/warningとも0）、通常36 unittest（458.110秒）、buildが成功した。
凍結参照用の専用7テストも成功し、生成物をstage後に再buildしてgit diff --exit-code -- README.md research/knowledge/generatedが終了値0。
6個の凍結READMEのhash、7本の現行移動先、現行ID参照、116/56/26点の正本と証明書のbindingを確認した。
scope指定のindexは42 pathで、実験17ファイルのindex blobは作業中raw bytesと一致。他者screenは取り込まない。
番号統合・incoming metadataの最小修正・必要な参照検査対応と今回の研究結果だけをmainへ直接commitする。
branch/PR、push、長時間探索workflowの自動起動設定は追加していない。
