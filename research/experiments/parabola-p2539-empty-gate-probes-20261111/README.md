# p2539: 空対26仮定の8点を閉じ、124点除外・18点gateへ（2026-11-11）

採用時点の必要条件はK0734へ追加する。現在の正本はknowledge itemを参照する。
対象は同じ1258点seed S（SHA-256 `454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb`）の五点削除による改善。
**26個の空対点仮定のうち8個を独立に排除し、残る18個はUNKNOWN**。
全体の非存在や新しい上下界は主張しない。

## 共通入力と一回のprobe

原点と完全対{6,2533}を保つexact1259点・exact五点損失の凍結親CNF（51570変数144546節）に、
前回の116個の負point単位節を追加した。共通baseは51570変数144662節で`output/base.cnf.gz`へ一つだけ保存する。
これら116節は幾何hitting証明を根拠に採用する。元の60点にnative RUPもあることと、新規56点の幾何根拠は区別する。
case uは共通baseへ[a_u]（a_u=36512+u）を一つ加えた144663節。子CNFはbaseとこの一節からbyte再構築できる。
26点の正ORは前回の親だけのRUPと数え上げで正当化され、この26仮定は互いに重なり得る被覆である。

PySAT 1.9.dev21/Cadical195、proof-disabled、budget10000で26個を一回ずつ実行した。
全子は終了値0、18ケースがUNKNOWN、8ケースがSOLVER_UNSAT。SATモデルはなかった。
同じ全体UNKNOWN・同じpoint入力の再実行ではない。各子は120秒に制限し、存在する出力directoryは再起動しない。

SOLVER_UNSATとなった点は
`612, 1367, 1518, 1547, 1623, 1892, 2277, 2479`。
これだけを新しい`proof-output/`でproof-enabled再生成し、全て終了値0・完結DRATを保存した。
UNKNOWNの18個はproof生成も再実行もしていない。

## 入力・証明の独立検査

`audit.py`は探索コードやencoding.pyをimportせず、元の保持側の全構造・point・exact損失・幾何と末尾116節を確認する。
116点の負hitting証明木を再生し、親38868四点と除外木が参照する四点をgeneric整数4×4行列式で実検査した。
26個全ての正point仮定と子入力SHA、source SHA、実終了値も照合した。
`input-audit/`の初回SOLVER_UNSATは、この段階では独立負証明として扱わない。

`verify_cases.py`は8子のDRATを固定DRAT-trimの-Uで独立に受理し、-lで核DRATを抽出した。
核の追加節へ¬a_uを付けて仮定を除去し、共通baseだけで-f -U検査した。
8個全ての子反証と負単位節導出が受理された。
raw核DRATはローカル保持・Git除外し、圧縮核と導出・receiptはGit管理する。

8負単位節をbaseへ加えたreduced baseは51570変数144670節。
残る18点の正ORをこのreduced baseで一行RUPとして受理した。
さらに8負単位節の導出と正18点ORを結合し、`replay.py`で共通baseだけから別処理再生した。
`replay-output/coverage.rup.gz`はソルバや子DRATを使わず再生できる採用証明である。
成功は-f -Uのs DERIVATIONとc VERIFIED derivationで判定し、終了値1を通常のUNSAT受理（終了値0）と区別する。
**空節のない導出であり、共通baseや元の親の全体UNSATではない。**

今回のnative導出は、116個の幾何除外節を含むbaseからのもの。
新規8点を元の親だけからnative RUPで導いたとは主張しない。
独立入力監査と既存の幾何hitting根拠を合わせ、実際の安全改善候補への排除として使う。

## 数学的な接続

K0734の既存根拠から、改善Tは|S∖T|=5、{0,6,2533}⊆T、既存116除外点を含まず、元の空対26点を少なくとも一つ含む。
新規排除点uをTが含むなら、(S∩T)∪{u}の1254点を含むTの1259点部分集合T'を取れる。
T'は安全で、元の1253共通種点、原点・完全対、u、既存116除外を保つ。
従って共通baseへa_uを真とするモデル拡張ができ、今回の¬a_u導出に反する。
新規8点は大きなTでも使えず、総除外は116+8=124点となる。

元の26点のORから新規8点を除き、残る必要追加集合は次の18点。

```
60 106 262 269 647 692 916 992 1021
1027 1172 1197 1342 1512 1847 1927 2270 2433
```

この18ケースは各budget10000でUNKNOWN。全体の改善不能、五点削除局所最適性、A(2539)=1258は示していない。
現在の全体範囲1258≤A(2539)≤1271は不変。残るモデルが見つかれば全CNFとgeneric整数幾何の検査が必要。
検査器・コンパイラ一般の形式的健全性やLean形式証明は主張しない。

## 回帰・再現・引継ぎ

実baseの6改変を拒否し、26個の正point仮定の52真理値割当てを確認した。
親・幾何hitting・仮定除去の回帰は凍結source SHAで固定して引き継ぐ。全体未知探索の再実行はしていない。
repo rootで新しい出力pathを使う。

```powershell
$exp='research/experiments/parabola-p2539-empty-gate-probes-20261111'
uv run --locked python "$exp/audit.py" --saved "$exp/output" --output "$exp/input-audit-fresh"
uv run --locked python "$exp/regression.py" --output "$exp/regression-fresh.json"
uv run --locked python "$exp/replay.py" --output "$exp/replay-fresh"
```

全初回probeの再現は`uv run --locked --with python-sat==1.9.dev21 python <exp>/run.py --output <fresh-directory> --budget 10000`。
新しい実行はsourceで固定した26仮定だけを対象とし、既存directoryを発見したら保持する。
8負証明の再検査は`verify_cases.py --output <fresh-directory>`。
次回は残る18点の二点同時追加障害（最大153組）や、追加点数を固定した支持構造を評価できる。
同じ18仮定・同じ予算を理由なく再実行しない。今回の8負単位節を加えてもbaseと全モデルは一致し、単に新しい問題になったとは扱わない。
