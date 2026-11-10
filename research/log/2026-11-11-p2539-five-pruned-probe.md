# 2026-11-11 p2539の60点除外単位節を採用したprobeはUNKNOWN

開始HEADはd62e39f32f0958f8fcea3319dcbd7331ddb58850、main。
AGENTS.md、knowledge README、現行K0693/K0702/K0706/K0727、最新logとexperimentを読んだ。
git fetch origin main、status、実行中プロセスを確認し、研究計算や新しいremote commitはなかった。
他者の未コミットequality_screen_200k.jsonは保持した。

前回独立排除した60点を採用し、保持側の凍結UNKNOWN CNFに60個の負point単位節を加えた。
親CNFをbyte保存したまま51570変数144606節とし、追加節と元の幾何・hitting-tree証明のhashを保存した。
元のUNKNOWNと同じ入力ではなく、新しい独立必要条件を採用した入力である。
PySAT 1.9.dev21/Cadical195、proof-disabled、budget100000で一回だけ実行。
85.197秒・100000 conflictsでUNKNOWN。子終了値0であり、失敗やUNSATとして扱わない。
正モデルも負の完結証明も得られず、同入力・同予算の再実行はしていない。

新しいschemaは探索コードやSATライブラリをimportせず、親全節と末尾60節を全照合した。
採用60点の負hitting-treeを独立再生し、親38868四点と証明参照2507四点の整数行列式0を実確認した。
実入力10改変を拒否し、60負point単位節の120真理値割当ても確認した。
これは入力の意味・根拠の監査であり、UNKNOWNを独立UNSATへ昇格させない。
必要条件の命題は変わらないのでKを新設せず、K0727に最新のUNKNOWN入力と結果の所在を追加した。

次回は候補二点の同時追加障害など、入力の支持構造を評価できる。
別案として、60除外の根拠を親CNFの実節へ照合し、a_u仮定下のRUP証明を¬a_uでliftして単位節を導く橋渡しを検討できる。
これは未実装で、現在の追加60節が親CNFだけのRUP証明で導かれたとは主張しない。
同じpruned60入力・同じ100000 budgetを再実行しない。全体範囲1258..1271と五点削除の未解決状態は不変。

uv sync --locked、knowledge check（709項目、error/warningとも0）、33 unittest（346.880秒）、buildが成功した。
生成物をstageして再buildし、git diff --exit-code -- README.md research/knowledge/generatedは終了値0。
source・input・60point mapping・監査・実子終了値を照合し、UNKNOWNのまま保存されていることを確認した。
scope指定のindexは19ファイルで、experimentのindex blobは作業中raw bytesと一致し、他者screenや__pycache__を含めていない。
終了前のfetchでもremote追加はなかった。branch/PRを作らず、検証済みの自分の変更だけmainへ直接commitする。
pushや長時間探索workflowの自動起動設定は変更しない。新しい研究上の結論やユーザー対応を要する変化はない。
