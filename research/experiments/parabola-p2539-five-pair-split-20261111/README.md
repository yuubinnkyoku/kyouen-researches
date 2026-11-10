# p2539: 五点削除改善での元の完全対保持（2026-11-11）

採用時点の結果はK0727へ追加した。現在の正本はknowledge itemを参照する。
対象seed Sは1258点、SHA-256は
`454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb`。
入力は`../parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt`。

## 分割と実行結果

前回K0727で残った原点あり・完全対一つ・exact1259点・exact五点損失の親入力だけを扱う。
親は`../parabola-p2539-exact-five-20261111/output/x1-B1-target1259-remove5/input.cnf.gz`、
非圧縮SHA-256は`d23890f881d73064f41719de379346d80193fea8ec507a9f7fe0050edf73f40a`。
元の完全対{6,2533}を保持する場合と、他の完全対へ変更する場合に分ける。
BOTHの変数番号はB_i=4i−3なので、B6は21。
親の全144545節をそのまま保ち、保持側に[21]、変更側に[-21]を一節だけ追加した。
どの親モデルも正確に片方へ属し、両子は51570変数144546節である。

| case | 単位節 | budget | proof-disabled結果 | 秒 | 実conflicts |
|---|---|---:|---|---:|---:|
| retained | [21] | 100000 | UNKNOWN | 97.85 | 100004 |
| changed | [-21] | 100000 | SOLVER_UNSAT | 127.01 | 99424 |

両子プロセスは終了値0。保持側は再実行していない。
変更側だけproof-enabledで再生成し、終了値0・116.76秒・同じ99424 conflictsで483675行DRATを保存した。
UNKNOWNや初回ソルバUNSATだけでは、幾何学的非存在を結論しない。
`run.py`は実子終了値とtimeoutを保存し、各子300秒に制限する。

## 独立検査

`check_inputs.py`で圧縮CNFを親+単位節へbyte完全照合した。
`schema.py`は探索builderやSATライブラリをimportせず、四状態one-hot・BOTH数1・NONE数12・
全point定義・幾何節・損失counterの上下両側・末尾のsplit一節を全て解釈する。
counter補助変数は既存の独立prefix意味で拡張し、全変数領域を確認する。
正確に五点失う安全集合で0を保ち、完全対一つが{6,2533}と異なればB6は偽となり、
この変更側CNFの全節にモデルを拡張できる。
幾何節の全38868四点を負point変数から復元し、既存generic整数4×4行列式で0と実検査した。
提供辺cacheの完全性はモデル拡張・非存在の前提にしない。

変更側DRATは固定DRAT-trimのRUP限定検査で受理し、抽出147349行LRATは空節修正版checkerで受理した。
`audit-output/changed/`に全receiptとsource・入力・証明のhashを保存した。
採用DRAT gzipは8574253 bytesをGit管理。生成元DRAT gzipと大きいLRAT raw/gzipはローカル保持・Git除外し、
manifestにhashと所在を保存する。`replay.py`は採用圧縮CNF/DRATのみから独立schema・整数幾何・RUPを再検査する。
16不正入力の拒否、実B6とpoint定義の128真理値割当て、共通親の復元も回帰で確認した。
親のexact損失に関する131940割当てと独立prefix回帰は保存済みの根拠を引き継ぎ、同じ計算は再実行していない。

## 全改善集合への部分集合論証

K0727の前回根拠から、|T|≥1259、|S∖T|≤5の安全集合Tがあれば、
r=|S∖T|=5、0∈T、完全対数1である。
その完全対が{d,2539−d}、d≠6と仮定する。
R=(S∩T)∪{d,2539−d}は高々1255点なので、Rを含むTの1259点部分集合T'が選べる。
T'は安全で、種との共通点1253点、原点0、完全対{d,2539−d}を保つ。
部分集合は新しい完全対を作らず、元のTに{6,2533}は完全対として存在しないから、T'もB6を満たさない。
従ってT'は変更側CNFへモデル拡張でき、独立UNSAT受理と矛盾する。
**五点以下の削除による改善は、正確に五点を失い、原点と元の完全対{6,2533}を全て保つ必要がある。**

これは固定Sについての必要条件で、保持側には100000 conflictsでUNKNOWNが残る。
保持側の実在・非存在、五点削除局所最適性、全体の最大性は示さない。
1258≤A(2539)≤1271と等号達成問題は不変。検査器・コンパイラ一般の健全性やLean形式証明は主張しない。
有限回帰と上記全称縮小論証も区別する。

## 再現と継続

repo rootから、出力先を新しいpathにして実行する。

```powershell
$exp='research/experiments/parabola-p2539-five-pair-split-20261111'
uv run --locked python "$exp/check_inputs.py" --saved "$exp/output" --output "$exp/input-audit-fresh"
uv run --locked python "$exp/regression.py" --output "$exp/regression-fresh.json"
uv run --locked python "$exp/replay.py" --saved "$exp/audit-output" --output "$exp/replay-fresh.json"
```

ローカル生成元証明がある場合のRUP/LRAT再検査は`verify.py --output <fresh-directory>`。
探索再現は`uv run --locked --with python-sat==1.9.dev21 python <exp>/run.py --output <fresh-directory> --case retained|changed|both --budget 100000`。
証明生成は同じcommandに`--proof --case changed`を付ける。
独立再生のために保持側UNKNOWNや既排除形状を再探索する必要はない。

次回は保持側の削除候補を幾何的な追加点の障害から絞るなど、残る問題を構造化する。
同じretained入力・同じ予算のUNKNOWN再実行は避ける。変更側の証明から全完全対や全体最大性を推測しない。
