# 2026-11-09 固定dの距離測定はUNKNOWN、モデル符号を修正

K0709/K0710の抽象反例からQ_pの相関を否定せず、実際のp=2647,d=1323の
元CNF節削除距離を測るため、RC2(g3)による全節重み1のcore-guided MaxSATを試した。
既存のprobe/auditプロセスと出力先が異なることを確認して一度だけ実行。
53,886節の正規化入力を保存したが、60秒の壁時計上限でUNKNOWNとなった。
モデルなし、終了後の当該worker残存なし。距離にも最大安全サイズにも新しい数値境界はない。

一次資料と再現コードは `research/experiments/parabola-cnf-deletion-distance-20261109/`。
当初workerを別名で保持し、後から保存CNF入力と直接base interpreterによるsupervisorを加えた。
同じp,d,方式,予算のUNKNOWNを繰り返さない。

実装照合中、既存maxsat_probe.pyのSAT後処理に3つの符号誤りを確認した:
負リテラルをabs変数で評価していない、True変数を低側の点にしている、
負リテラルの除去点がp-litとなり範囲外になる。
正しい符号化はTrueが高側p-iで、違反節の支持点は正ならlit、負ならp+lit。
helperを切り出して修正した。既存UNSAT/UNKNOWNのソルバ返値を変更するものではない。
歴史的な出力はそのまま保持する。

投影、違反節の支持、修復後の安全性を、小素数の全テンプレートと独立な整数行列式で照合する。
p<=13だけでは全テンプレートが安全で修復分岐の検証にならなかったため、
違反テンプレートのあるp=17を追加した。全1312テンプレート（うち違反192）で一致し、
両helperの修復後は全て安全だった。負リテラル例・保存CNF一致・supervisor玩具例も通過した。
回帰の出力はexperimentに保存する。
単独UNKNOWNのため新しいK項目は作らない。

次は、保存CNFに対して別の具体的な構成法または測定法ができた時に再開する。
モデルが得られてもソルバ最適性と直接検査の上界を区別する。
1324点候補まで進めた場合は、cached edgesだけでなく独立整数幾何検査が必要。
他のchatによる監査・走査とその出力は保持し、この作業に取り込まない。

## 統合確認

`uv sync --locked`、knowledge check（692項目、エラー0・警告0）、
knowledge unittest（33件、331.564秒、全件OK）、build（6ビューとREADME）、
generated差分検査が正常終了した。既存の歴史スクリプトのSyntaxWarningのみ。
新規回帰は全1312テンプレート、負リテラル単位例、入力CNF一致とsupervisor玩具例で通過。
core.autocrlf=trueのcheckoutでも入力CNFの記録hashを保てるよう、experiment内の
`.gitattributes`でそのCNFを変換対象から外した。
