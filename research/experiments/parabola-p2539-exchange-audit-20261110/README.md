# p2539の四点削除近傍の独立監査

現在の数学的結論は[K0724](../../knowledge/items/K0724-p2539-fixed-pair-four-deletion-local-exclusion.md)を参照する。
保存1258点集合を固定し、原点・完全対d=6を保ち、4点以下を除いて1259点以上を得る入力を監査した。
SAT探索は起動せず、先行experimentの入力・元DRAT・receiptを保持する。
前回のソルバUNSATという記録自体を独立受理の記録へ書き換えない。

## 再現

rootのlocked uv環境、gcc、g++を使う。出力には未使用のdirectoryまたはreceipt pathを指定する。

```sh
uv run --locked python research/experiments/parabola-p2539-exchange-audit-20261110/audit.py --output FRESH-audit --timeout 120
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2539-exchange-audit-20261110/regression.py --output FRESH-regression.json
uv run --locked python research/experiments/parabola-p2539-exchange-audit-20261110/replay.py --saved research/experiments/parabola-p2539-exchange-audit-20261110/output --output FRESH-replay.json
uv run --locked python research/experiments/parabola-drat-trim-20261109/controls.py --output FRESH-rup-controls.json
uv run --locked python research/experiments/parabola-drat-trim-20261109/lrat_controls.py --output FRESH-lrat-controls.json
```

初回auditには先行experimentでローカル保持したproof.drat.gzが必要。
replayはGit管理したCNF gzip・LRAT gzip・固定種・独立schemaだけを使い、元DRATを読まない。
raw core.lratはローカル保持してGit除外し、採用core.lrat.gzはGit管理する。
hashと行数はoutput/manifest.jsonに保存した。

## 全節の意味

独立schemaは探索器・CardEnc・三値builderをimportしない。
86583節を以下へ分け、全節を検査した。

| 部分 | 節数 | 検査 |
|---|---:|---|
| 幾何 | 38868 | 負の選択変数を要求点に戻し、F={0,6,2533}で四点へ補い、整数行列式0を実検査 |
| one-hot | 5072 | 各自由対の低側・高側・空対の四節と完全一致 |
| 空対counter | 31388 | 1268入力、上限12、prefix意味の四型の節 |
| 削除counter | 11255 | 種の1255非固定点の不選択literal、上限4、同じ四型の節 |

幾何節の四点候補を選ぶ際には和0 mod2539を必要条件として使うが、受理には実整数行列式0を要求する。
提供禁止辺の完全性を仮定しない。安全なTは提供された真の禁止四点を全て避けるからである。

## 安全候補をCNFモデルへ拡張する証明

Fを含む安全なTは二完全対を含めないため、他の各対は低側・高側・空対に一意に対応する。
これを選択変数へ割り当てるとone-hotと全幾何節を満たす。
|T|=1271−空対数なので、1259点以上なら空対入力の真の個数は12以下。
削除入力は種の選択点の否定なので、その真の個数は|S∖T|であり4以下。

各counterの補助変数s(i,j)へ「入力x_0,...,x_iの真がj個以上」の真偽を割り当てる。
schemaは全節を次の四型だけとして解釈する。

1. ¬x_i ∨ s(i,1)
2. ¬s(i,j) ∨ s(i+1,j)
3. ¬x_i ∨ ¬s(i−1,j) ∨ s(i,j+1)
4. ¬x_i ∨ ¬s(i−1,k)（kは上限）

初めの三型はprefix個数の定義で成立する。
最後の型が偽ならx_iとその前の少なくともk真入力があり、全体の上限に反する。
schemaは各補助変数に矛盾のない(i,j)意味を付け、全宣言補助変数がこの解釈を持つことを確認する。
領域3808..18879と18880..23883は互いに素で、選択変数1..3807とも交差しない。
未使用の固定対変数は自由に割り当てられる。
したがって対象の安全なTは全86583節を満たすCNFモデルへ拡張できる。

## 保存証明の受理

元228249行DRATを固定DRAT-trimの-U（RUPのみ）で受理し、64571行LRATを抽出した。
空節処理修正版lrat-checkで受理し、採用圧縮証明を別処理でも再生した。
このCNFがUNSATなので、前節の拡張可能性から対象条件のTは存在しない。
counterに逆方向の意味を証明する必要はなく、安全候補からモデルへの拡張だけで排除には十分である。

小規模の符号付き・符号なし2064 prefix割当てを全数照合し、六つの破損schemaを拒否した。
和0 mod2539を満たす(1,2,4,2532)はschema上の候補にはなるが整数幾何で非禁止として拒否した。
RUP六制御と空節修正版LRAT五制御も再実行した。原版LRATの偽受理は採用しない（K0718）。

これは固定種・固定原点・固定完全対の局所排除であり、条件なしの局所最適性やA(2539)の全体上界ではない。
検査器・コンパイラの一般健全性やLean形式証明を主張しない。
