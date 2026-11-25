# 2026-11-11 p2539の空対26被覆から8仮定を独立排除

開始HEADはb6680dc25e1593866d31d82c076142f079f94db5、main。
AGENTS.md、knowledge README、現行K0693/K0702/K0706/K0734、最新logとexperimentを読んだ。
fetch・status・実行中プロセスを確認し、研究計算はなかった。他者の未コミットequality_screen_200k.jsonは保持した。
remoteに5×19の独立log更新2 commitがあり、競合なくmergeした。作業開始時統合HEADは71eb7387eb13f93ca995c474d762eae540257408。

前回の正26点gateを使い、保持側親に116個の独立幾何除外節を加えた共通baseを作った。
元の全体UNKNOWNの再実行ではなく、26個の異なる正point仮定を初めてbudget10000・proof-disabledで各一回探索した。
全子終了値0、18 UNKNOWN、8 SOLVER_UNSAT、SATモデルなし。既存出力を上書き・重複起動していない。
8点は612,1367,1518,1547,1623,1892,2277,2479。
入力schemaは探索encodingをimportせず、親全節・116負単位節・26正point仮定・hashを確認した。
116点のhitting-treeと実四点の整数幾何も検査し、6不正base・52仮定真理値割当ての回帰が成功した。

負の8点だけproof-enabledで再生成。全子終了値0で完結DRATを得た。
固定DRAT-trimの-Uで全8子を独立反証し、核DRATを抽出して¬a_uでliftした。
共通baseだけからの8負単位節を-f -Uで受理した。これは116幾何除外節を仮定するbaseからの導出で、元の保持側親単独とは区別する。
reduced baseで正18点ORを一行RUP受理し、8負導出と18点ORを結合したcoverage証明を別処理再生した。
ソルバ・子DRATなしの再生がDERIVATIONとして受理され、空節や全体UNSATと混同していない。
核DRAT rawはローカル保持・Git除外、圧縮核・lift導出・結合証明・全receiptは保存した。

共通種点1253点と仮定点uを保つ1259点部分集合を取る論証で、大きな安全改善Tにも新規8点の排除が必要となる。
合計124点を避け、元の空対の残る18点から少なくとも一つを加える必要がある。
同じ必要条件の更新としてK0734へ保存する。全体範囲1258..1271と五点削除改善の未解決状態は不変。
18 UNKNOWNは再探索もproof生成もしていない。

次回は残る18点の二点同時追加障害（153組）や、追加点数を固定したクラスを評価できる。
入力に導出済み8単位節を加えても全モデルは元の共通baseと一致するため、同じ仮定・同じ予算の再実行を新規問題と扱わない。

統合前検査はuv sync --locked成功、knowledge check 716項目・0 errors・0 warnings、
unittest 36件成功（511.507秒）。build.pyを二回実行し、生成物をstageした後の再生成差分は0件だった。
実験source・圧縮証明・receiptのhash結合も一致し、結合RUPの実ファイルは20491行。
checker内部の表示20492 lemmasとファイル行数を区別した。
実験201ファイルについてindex blobと作業中bytesの一致を確認し、raw核8本はローカルに保持・Git除外した。
commit対象はこの実験、K0734、生成物4ファイル、このlogの207ファイルだけ。
他者のequality_screen_200k.jsonは未stageのまま保持し、branch・PR・workflow変更・pushは行っていない。
