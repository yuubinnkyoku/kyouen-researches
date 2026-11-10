# 2026-11-11 p2539の五点削除改善に残る形状を限定

開始HEADは9df4e44f01c53dcecb93b56d1a7308551ffa59ff、main。
AGENTS.md、knowledge README、現行K0693/K0702/K0706/K0726と最新log・experimentを確認した。
git fetch origin main、status、実行中プロセスを確認。研究計算はなく、remote追加もなかった。
他者の未コミットequality_screen_200k.jsonは保持した。

K0726で削除四点以下は全形状排除済みなので、既知層を除くexact五点削除を選んだ。
原点有無と完全対数0/1の四形状をproof-disabled、100000 conflictsで実行。
原点なし二形状と原点あり・完全対なしはSOLVER_UNSAT、残る原点あり・完全対一つはUNKNOWN。
四つとも子終了値0。入力・source・seed・辺のhashとlaunchを保存した。
小素数5/7/17のexact点数・損失・原点会計131940割当ての回帰も成功した。

凍結した三負入力だけからproof-enabledでDRATを生成し、UNKNOWNを再実行しなかった。
生成された318386/312040/486382行DRATはソルバの主張として保存し、独立検査を別に行った。
独立schemaはSATライブラリや探索builderをimportせず全節を確認。
exact損失を上下両counterで解釈し、原点なしでは非原点損失4、原点ありでは5と確認した。
各38866/38866/38868幾何四点の整数行列式を検査した。
三証明ともRUP限定検査と空節修正版LRAT検査を受理、抽出LRATは30890/53298/103010行。
実入力27改変を拒否し、point定義192割当て、部分集合縮小例342件の回帰も成功した。
採用圧縮CNF/DRATからschema・幾何・RUPを別処理再生し、三例を受理した。
採用DRAT gzip約11.88MBをGit管理、大きいLRAT raw/gzipと生成元DRAT gzipはmanifest付きでローカル保持・Git除外。

S∩Tの1253点と必要なら完全対二点を保つ1259点部分集合を選ぶと、削除数・原点有無・完全対数が保たれる。
K0726と三形状排除を結合し、五点以下の削除による改善には正確な五点損失・原点・完全対一つが必要とK0727へ記録した。
残る形状はUNKNOWNであり、五点削除局所最適性も全体最大性も示さない。1258..1271は不変。

次回は残るx1-B1を元の完全対{6,2533}を保つ場合と他の対へ変える場合へ分けるなど、未被覆層を構造化できる。
同じ100000 conflictsのUNKNOWNや既排除三形状・削除四点以下を理由なく再実行しない。
元のraw evidenceと凍結sourceは更新せず、新出力先で継続する。

uv sync --locked、knowledge check（709項目、error/warningとも0）、33 unittest（339.059秒）、buildが成功した。
生成物をstageして再度buildし、git diff --exit-code -- README.md research/knowledge/generatedが終了値0。
ソース・seed・生成元/採用DRAT・保持LRAT・初回子終了値・部分集合論証hashを照合した。
scope指定のindexは74ファイルで、採用証明は三つ、experimentのindex blobは作業中raw bytesと一致。
大きいraw/gzip LRAT、生成元DRAT gzip、他者screen、__pycache__は含めていない。
branch/PRは作らず、自分の検証済み変更だけmainへ直接commitする。pushやworkflow設定変更は行わない。
