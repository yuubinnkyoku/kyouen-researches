# p2531のd=86..100を独立LRAT監査

現在の監査状態は[K0702](../../knowledge/items/K0702-p2531-no-parabola-equality-witness.md)を参照する。
前段147 dとの重複を避けて、未被覆d=86..100の15件を生成・検査した。
旧143件だけを起点にせず、前段のLRAT4件を含むcoverage manifestとそのhashを引き継いだ。

## 入力の縮約

前段の837640辺から、二完全対 `{±a,±b}` の799480辺を除き、38160辺を `input/edges.txt` へ保存した。
固定完全対が1つで他の各対から一側しか選ばないテンプレートは、二完全対を同時に含めない。
従って省いた辺は常に投影でtautologyとなる。
縮約後でも前段4入力のDIMACSがbyte一致し、新15件も元generatorを使わない独立な投影schemaに一致した。
全38160提供辺のgeneric整数4×4検査も成功した。
辺集合の完全性は上界排除に必要とせず、健全な辺の部分集合による緩和を使う。

## 証明と保存

全15件でCaDiCaL UNSAT、DRAT-trim -U VERIFIED、空節処理修正版lrat-check VERIFIEDを確認した。
さらに保存した各CNF・LRAT gzipを展開し、別の再生処理でも全15件を受理した。
各input・source・binary・proof hashと実stdoutはresultとcertificate manifestに保存した。
採用LRAT gzipとCNF gzipはGit管理する。
原DRAT gzipとraw LRATは生成先にローカル保持し、Gitから除外する。
原DRATの所在は `output/batch86-100/d<d>/proof.drat.gz` で、hashと保存範囲は各recordに記した。
別checkoutで原DRATがなくても、Git管理されたCNFと採用LRATだけで独立再生できる。
保存監査は原DRATがローカルにある場合に追加でhashを照合し、不在をUNSATの根拠へ読み替えない。

前段147 dと今回15 dは重複がなく、被覆の和は162/1265、残り1103である。
修正版増分DRAT143 dとLRAT19 dを同じ検証器の履歴へ混ぜず、集合和として扱う。
全数監査、検証器の一般健全性の形式証明、正確な最大サイズを主張しない。

rootのuv環境で、出力先は毎回新しくする:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2531-lrat-20261110/audit.py --edges research/experiments/parabola-p2531-lrat-20261110/input/edges.txt --ds 86,87,88,89,90,91,92,93,94,95,96,97,98,99,100 --output FRESH-batch --budget 100000
uv run --locked python research/experiments/parabola-p2531-lrat-20261110/verify_saved.py --saved research/experiments/parabola-p2531-lrat-20261110/output/batch86-100 --output FRESH-verification.json --manifest FRESH-manifest.json --replay
```

最初は新しいsolver証明を生成する再現、最後は保存証拠の照合・実再生であり、新しいSAT探索を使わない。
同じcaseを研究上の新しい被覆件数に再計上しない。
