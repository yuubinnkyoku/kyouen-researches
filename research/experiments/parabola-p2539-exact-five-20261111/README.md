# p2539: 正確に五点を失う改善の形状制約（2026-11-11）

この実験の採用時点の結論はK0727。現在の正本はknowledge itemを参照する。
種SはK0723の1258点安全集合で、入力は
`../parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt`、
SHA-256は`454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb`。
Sは原点0と完全対{6,2533}を含む。K0726で四点以下の削除は排除済みなので、
今回は**正確に五点を失う層**を探索した。1259点への改善なら六点追加に相当する。

## 凍結入力と結果

xは原点有無、Bは完全対数。安全集合の完全対数は高々一つ（K0097）。
点数は全てexact1259、各探索のconflict budgetは100000。

| case | 変数 | 節 | 初回ソルバ結果 | 初回秒 | 採用DRAT行 | 抽出LRAT行 |
|---|---:|---:|---|---:|---:|---:|
| x0-B0 | 42818 | 127040 | SOLVER_UNSAT | 15.33 | 318386 | 30890 |
| x0-B1 | 46582 | 134567 | SOLVER_UNSAT | 36.26 | 312040 | 53298 |
| x1-B0 | 47810 | 137026 | SOLVER_UNSAT | 74.08 | 486382 | 103010 |
| x1-B1 | 51570 | 144545 | UNKNOWN | 110.07 | — | — |

初回はproof-disabledで、四子プロセスは終了値0。`output/*/launch.json`に実終了値を保存した。
負の三入力だけから`produce.py`で証明を生成した。UNKNOWNは再実行していない。
生成時間は19.48秒、46.86秒、81.14秒。証明生成と独立受理は別段階である。
`input-audit/`は四入力のbyte完全再構築であり、それ自体は負結果の独立証明ではない。

## 独立解釈と受理

`schema.py`はSATライブラリも探索builderもimportしない。各対のBOTH/NONE/LOW/HIGH
one-hot、BOTH数、NONE数の両側制約、point変数の定義、幾何節、損失の両側counterを全照合する。
四状態のpoint定義から集合サイズは1269+x+B−NONE数となる。
seed非原点1257点に対する損失literalは`-a_t`。
原点なしでは既に0を一つ失うため非原点損失はexact4、原点ありではexact5。
exact損失はAtMost(損失,k)とAtMost(非損失,1257−k)の双方からなる。
counterは既存独立prefix検査器のhashで固定し、補助変数を「入力prefix中で少なくともj個真」に解釈する。
領域・符号・全節の照合により、条件を満たす点集合からCNFモデルへ拡張できる。

幾何節は四つの負point変数（原点ありの三literal節は0を補う）へ戻す。
x0二例は各38866四点、x1-B0は38868四点の整数4×4行列式0を既存generic verifierで実確認した。
したがって安全集合は全幾何節を満たす。辺cacheの完全性を排除の前提にしない。
三DRAT全てを固定DRAT-trimのRUP限定モードで受理し、抽出LRATを空節修正版checkerで受理した。
検査器ソース・入力・証明・出力のhashと終了値は`audit-output/*/`にある。
採用圧縮DRATは合計11882701 bytes。大きいLRAT raw/gzipと生成元DRAT gzipはローカル保持・Git除外し、
採用DRAT gzipをGit管理する。`replay.py`はSATライブラリやローカルLRATを使わず、
採用CNF/DRATから独立schema・整数幾何・RUPを別処理で再検査する。

## 全改善集合への部分集合論証

安全集合Tが|T|≥1259、r=|S∖T|≤5を満たすとする。K0726によりr=5である。
S∩Tは1253点。完全対があればその二点も加えた集合Rを取り、なければR=S∩Tとする。
|R|≤1255≤1259なので、Rを含むTの1259点部分集合T'を選べる。
T'は安全性を継承し、S∩Tを全て含むから|S∖T'|=5を保つ。
Sは0を含むので、Tに0があればS∩Tに0が含まれ、なければT'にも0はない。
完全対の二点を保ち、部分集合は新しい完全対を作らないので、完全対数も同じである。
従ってT'は同じx/B形状のexact1259入力にモデルを与える。
独立排除した三形状では矛盾するため、**改善にはr=5、0∈T、完全対数1が必要**となる。

これは有限CNFの独立受理と上記の数学的縮小論証を組み合わせた固定seedの必要条件である。
x1-B1に解があるとは示さず、五点削除近傍全体の局所最適性も示さない。
全体範囲1258≤A(2539)≤1271、等号達成問題は変わらない。検査器・コンパイラ一般の健全性やLean形式証明は主張しない。

## 回帰と再現

`regression.json`は小素数5/7/17の131940割当てによるexact点数・損失・原点会計の回帰。
`schema-regression.json`は実CNFの27改変拒否、point定義192割当て、部分集合縮小例342件。
有限回帰は上の全称論証と区別する。実行はrepo root、各出力先は新しいpathを使う。

```powershell
$exp='research/experiments/parabola-p2539-exact-five-20261111'
uv run --locked --with python-sat==1.9.dev21 python "$exp/audit.py" --saved "$exp/output" --edges research/experiments/parabola-p2539-pair-pilot-20261110/output/edges.txt.gz --output "$exp/input-audit-fresh"
uv run --locked python "$exp/schema_regression.py" --output "$exp/schema-regression-fresh.json"
uv run --locked python "$exp/replay.py" --saved "$exp/audit-output" --output "$exp/replay-fresh.json"
```

独立RUP/LRAT再検査は`verify.py --output <fresh-directory>`。ローカル生成元DRATが必要。
不足時は`produce.py --case x0-B0|x0-B1|x1-B0 --output <fresh-directory>`で対応CNFから再生成し、
その出力を別experimentで検査する。UNKNOWN探索を文書再現のために再実行する必要はない。
探索再現は`search.py --seed <上記seed> --edges <上記edges> --origin 0|1 --complete-pairs 0|1 --removed 5 --target 1259 --budget 100000 --output <fresh-directory>`。

次回はx1-B1を完全対{6,2533}保持と他の完全対に分けるなど、未被覆部分を構造化できる。
既排除三形状や四点以下を同じ条件で再探索しない。
