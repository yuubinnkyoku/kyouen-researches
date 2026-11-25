# 2026-11-11 p2539の原点保持・四点削除近傍を独立排除

開始HEADはd476cbdc6331330cecfa5170e02d76b45d083fc4、main。
AGENTS.md、knowledge README、現行K0693/K0702/K0706/K0723/K0724、最新logとexperimentを読んだ。
git fetch origin mainとstatus・実行中プロセスを確認し、研究計算は動いていなかった。
途中の再fetchでも追加remote commitはなかった。他者の未コミットscreenは保持した。

前回の完全対変更・完全対なしの負結果はproof-disabledだった。
未知探索を繰り返すのでなく、この二つの凍結CNFからproof-enabledで証明を生成した。
changed-pairは254562行・25.23秒、no-pairは298208行・18.62秒でソルバUNSAT証明を保存、両実行は終了値0。
この段階を独立証明とは扱わず、別schema・整数幾何・RUP/LRATで検査した。

独立schemaは既存prefix解釈をhashで固定し、4値one-hot、BOTH数、NONEの両側上限、point定義、削除counterを全照合。
二入力の各38868幾何節は負のpoint変数から実四点へ戻して整数行列式0を確認した。
初版auditはproduce.py経由でSATライブラリをimportしてしまい、root locked環境で前処理前に停止した。
定数を分離し、独立auditがSATライブラリや探索builderをimportしない形で再実行した。既存出力は上書きしていない。

両DRATのRUP限定検査と、抽出42292行・33132行LRATの空節修正版による検査が成功した。
新しい14改変を拒否し、実point定義の128真理値割当てと部分集合選択の縮小例356件も確認。
採用圧縮DRATを別処理で再生し、schema・幾何・seedのbindingを再検査した。
採用DRAT gzipは計約4.57MBをGit管理し、大きなLRAT raw/gzipはhash・所在付きでローカル保持・Git除外とした。
RUPとLRAT双方で検査した事実はreceiptに残し、portable replayは採用DRATを使う。

元の完全対を保つK0724の場合と合わせると、原点を保つ三場合を被覆する。
exact1259点だけでなく大きいTにも適用するため、S∩Tと必要な新完全対を保つ1259点部分集合を取る論証を追加した。
新完全対の場合は元の対の片側を失うのでr>=1となり、必要集合の大きさは1258-r+2<=1259。
この全称論証と有限独立証明を組み合わせた原点保持の局所排除をK0725へ記録し、K0724から参照する。
原点を除く交換や全体の最大値へは拡張しない。

通常のuv sync、knowledge check（707項目、error/warningとも0）、33 unittest、buildが成功した。
新しい全source・部分集合論証・採用DRAT・ローカル保持LRATと三場合のseed bindingも照合した。
生成物の再生成byte一致とstage後のgit diff --exit-code -- README.md research/knowledge/generatedも成功した。
次回の改善探索は原点を除く形状、または5点以上の削除を優先できる。
原点なし・target1259なら、(原点有無,完全対数,空対数)は(0,1,11)または(0,0,10)。
種の原点を必ず失うので、総削除上限4に対応する非原点1257点の削除counter上限は3となる。
既に独立排除した原点保持・4点以下の領域の同条件探索を再実行しない。
