# p2539・原点を保つ四点削除近傍の独立排除

現在の結論は[K0725](../../knowledge/items/K0725-p2539-origin-retaining-four-deletion-exclusion.md)を参照する。
固定1258点集合Sの完全対6を固定する条件を外し、原点を保つ場合の局所排除を監査する。
先行experimentのソルバ記録や入力は変更しない。

## 再現と保存

rootのuv環境・gcc・g++を使い、出力には未使用のpathを指定する。

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-origin-local-audit-20261111/produce.py --case changed-pair --output FRESH-proof-changed --budget 100000
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-origin-local-audit-20261111/produce.py --case no-pair --output FRESH-proof-none --budget 100000
uv run --locked python research/experiments/parabola-p2539-origin-local-audit-20261111/audit.py --output FRESH-audit --timeout 120
uv run --locked python research/experiments/parabola-p2539-origin-local-audit-20261111/regression.py --output FRESH-regression.json
uv run --locked python research/experiments/parabola-p2539-origin-local-audit-20261111/replay.py --saved research/experiments/parabola-p2539-origin-local-audit-20261111/output --output FRESH-replay.json
uv run --locked python research/experiments/parabola-p2539-origin-local-audit-20261111/qualify.py --output FRESH-qualification.json
```

produceは凍結済みCNFを読み、builderを使わず証明を生成する。独立監査ではない。
auditは保存proof-output/changed-pairとproof-output/no-pairを読み、生成済み証明を独立に検査する。
任意の別出力へ生成したproofを監査する場合は、保存版と同じ配置・hashを復元してから新しいaudit出力先を指定する。
元のソルバ結果はproof-disabledだったので、この実行は証明を得るために行った。
同じUNKNOWN探索の再実行ではない。

採用CNF gzipとverified-proof.drat.gzをGit管理する。
抽出した大きなcore.lrat・core.lrat.gzはローカル保持・Git除外し、所在・hash・行数を各manifestへ記録する。
replayはGit管理されたDRATだけを使い、SATライブラリ・元proof-output・ローカルLRATは不要。
二つの採用DRAT gzipは約2.35MBと2.22MBで、portableな証明再生に使う。

## 独立schema

| クラス | 変数 | 節 | 幾何節 | 元DRAT行 | 検査LRAT行 |
|---|---:|---:|---:|---:|---:|
| 完全対1個、元の対6と異なる | 44062 | 130779 | 38868 | 254562 | 42292 |
| 完全対なし | 40302 | 123259 | 38868 | 298208 | 33132 |

独立schemaはSATライブラリ・探索builderをimportしない。
各対のBOTH/NONE/LOW/HIGHの7節を完全照合し、BOTHのexactly-oneまたは全否定を検査する。
NONE=eとNONE補集合=1269−eの二つのAtMostを、既存の独立prefix意味で解釈する。
eはそれぞれ12,11。各入力counterの全節を導入・持ち越し・増分・上限超過禁止の四型へ照合する。
point変数a_tとBOTH∨sideの三節同値も全点で照合する。
削除counterの入力は種の非原点1257点の不選択literalであり、上限4。
全補助変数領域は互いに素で、宣言変数数の末尾まで覆う。

幾何節は負のpoint変数から直接四点へ戻す。原点を省いた三点節には0を補う。
各38868四点をgeneric整数4x4行列式で実検査し、合同式だけで受理しない。
安全候補Tから状態・point・prefix変数を構成すれば全節を満たすため、提供辺の完全性は不要。
両CNFのDRATを固定RUP限定検査で受理し、抽出LRATを空節処理修正版で受理した。
採用圧縮DRATも別処理で実再生した。

## exact1259から全改善集合へ

Sは1258点、原点と完全対{6,2533}を含む。原点を保つ安全なTで|S∖T|≤4、|T|≥1259を仮定する。
完全対は高々1個なので、次の三場合だけを考えればよい。

1. Tが元の完全対6を含む場合はK0724で既に排除済み。
2. Tが完全対を持たない場合、S∩Tを全て含む1259点部分集合T'を選べる。
   |S∩T|≤1258なので選択可能で、原点を保ち、完全対なし、|S∖T'|=|S∖T|。
   本監査の完全対なしCNFにより排除される。
3. Tが別の完全対{d,2539−d}を持つ場合、元の完全対の少なくとも片側がTにないのでr=|S∖T|≥1。
   必須集合R=(S∩T)∪{d,2539−d}は|R|≤1258−r+2≤1259。
   Rを含む1259点部分集合T'をTから選べ、原点と新完全対を保ち、削除数rも変わらない。
   本監査の完全対変更CNFにより排除される。

いずれの部分集合も安全性を受け継ぐので矛盾する。
従って原点を保つ改善は、少なくとも5点をSから除く必要がある。
原点を除く交換、5点以上の削除、A(2539)の全体上界は結論に含めない。

## 回帰と信頼境界

実入力の14改変を拒否し、二入力のpoint定義の128真理値割当てを検査した。
有限の縮小例356件で、上記部分集合選択の性質も確認したが、一般論証は前節による。
prefix意味は既存2064割当てと不正制御を持つ固定sourceへhashで結び付ける。
RUP/LRAT checkerは既存の固定sourceと空節修正を使い、一般健全性の形式証明は主張しない。
全体の独立範囲1258≤A(2539)≤1271は変わらない。
