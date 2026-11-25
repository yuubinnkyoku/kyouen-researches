# 2026-11-17：cost76cのWIN候補をmanifest限界寄与で再順位付け

開始時の最新mainは `48aa2c4d2f71b6ef3fe0408e93fb107bcd2f7c48`。作業前に `AGENTS.md`、`research/knowledge/README.md`、K0023/K0863/K0865/K0868、cost76c raw-audit log・claim、head-1452 presweep、cost64h/76d/77eのfold資料を確認した。知識項目を増やす種類の結果ではなく、cost76c実験の証明書抽出順を決める簿記監査なので、K項目は新設していない。

## 問い

cost76cのraw sweepでは bits 61/99/113 の3候補がWIN7-D10だった。3件すべてをblind extractionする必要があるかは未確認だった。現在のMS5 manifestを閉じる寄与だけで比べる。

## 方法

公開済みの `fold_projection_head1450_tool_20261116.py` をそのまま使用した。ツールはcost66c foldまでの基礎771 receipt roots（764既存roots＋7 cost66c roots）を再構成し、blob pin・head1450要約・需要ヒストグラムを再assertする。そこへ公開済みcost76d/77eの4 receiptを適用した既存4roots projection（head1452）を基準に、cost76cの各候補を1件ずつ、さらにbit昇順で3件まとめて投影した。

- 基準head：`1452/174/6396/506144/4669/370058`
- MS5 S6 manifest：7,867行（6分割CSV）
- cost76c候補：raw auditのWIN7-D10 bits 61/99/113。child `00000000010000809002000001000000` に各bitを追加した7石root
- 各候補の投影は、他の2候補を含めず単独で実施。最後に3件をbit順で連続適用
- 新しいエンジン探索・証明書抽出・証明書検証は行っていない

## 結果

| bit | 7石root | raw探索nodes | 単独の新規D4 S6 orbit | 単独のmanifest新規行 |
|---:|---|---:|---:|---:|
| 61 | `0000000001000080b002000001000000` | 752,696 | 5 | **1** |
| 99 | `00000000040000809002000000400800` | 4,168,961 | 5 | **1** |
| 113 | `00000000040000809002000000400008` | 8,174,662 | 5 | **1** |

3候補の7削除coverの和集合は19個のD4正準S6 orbit。そのうち7個がMS5 manifestに属し、6個はhead1452ですでに被覆済み、**未被覆なのは1個だけ**だった。

`00000000010000809002000001000000`

3候補はそれぞれ単独で、まったく同じこの1行を閉じる。残る4個の単独marginalはmanifest外である。

3件をbit順にまとめて投影すると、marginalは次のようになった。

| bit | marginal D4 orbit | manifest marginal |
|---:|---:|---:|
| 61 | 5 | 1 |
| 99 | 4 | 0 |
| 113 | 4 | 0 |

したがって3件すべてをfoldしても、manifest上の新規閉鎖は1行だけ。headは仮に1件を検証・foldした時点で、

`1453/174/6395/506068/4668/369982`

となり、3件すべてを入れた場合も同じ値である。現行headを1453へ更新したわけではない。

bit61を単独でfoldした場合の親側変化は4 S5 parent・6 parent-row incidence・親辺cost合計458。これは同一S6行が複数親に現れるincidence合計であり、global unique S6 costの減少76とは別の量である。

## 判断

**証明書抽出はbit61だけを最初に試す。** bit99・113は同じ1行を閉じる予備候補として残し、bit61の抽出に失敗した場合にbit99、次いでbit113を試す。探索nodes比ではbit61はbit99の約5.54分の1、bit113の約10.86分の1である。ただしこれはraw探索nodesの比較であり、証明書抽出時間の比ではない。抽出時の実測は別に記録する。

この判断で、現行manifestを進めるために先行して抽出する対象を3件から1件へ絞った。bit99/113のWIN7-D10探索結果そのものを撤回したわけではない。

## 再現・入力固定

再現コマンド：

```sh
python3 research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost76c_candidate_manifest_marginals_20261117.py
```

- 監査器SHA-256：`094047faccd99a459ee6726711b5cd9a2bff74feee1eb099bb1cc7475bcde821`
- 出力SHA-256：`dab6e411c977713496650ac1c65d3d657e509a6908aa8ad8922732a1c3981c8c`
- 最新main（48aa2c4）へ更新した疎cloneでも再実行し、出力SHA-256は同一だった。

主なblob pin：

- projection tool：`49fcd8ae6706c075b39eea5b115b2a045c2950cf`
- cost66c fold script：`898cfa614e63049e52f19f080cdc398a22e0f6c9`
- cost66c fold JSON：`8783993e5c73cc9697c3ca48aef981725f422be8`
- head1452 four-root projection：`005423113c601301e2b5c208d1138e17283cb774`
- cost76d/77e fold JSON：`8d4bc622f9da22b8754f2e398e5481359656d956`
- cost76c claim input snapshot：`8932f2d5e100325549a5f251a1d883558cae0708`
- cost76c raw audit：`7160490ce5d49f732acdecbf629fc0d79e6081ef`
- head1452 presweep：`0d9a94a272de9fe45708757f17bfea60239a3c9b`

保存物：

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost76c_candidate_manifest_marginals_20261117.py`
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost76c-candidate-manifest-marginals-20261117.json`

## 境界と次

これは既存WIN7-D10探索候補のmanifest被覆projectionであり、新しい証明書・verdict・receiptは作っていない。bit61の証明書抽出、独立検証、v15照合、receipt foldはすべて未実施。headは1452のまま。

**標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はUNKNOWN。** REFUTED-D10はLOSS証明ではなく、solved headはゲーム理論的勝敗を意味しない。
