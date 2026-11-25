# p=2531の未被覆dを独立LRAT検査

現在の命題・監査状態は[K0702](../../knowledge/items/K0702-p2531-no-parabola-equality-witness.md)を参照する。
修正版増分DRATの既存143 dに含まれないd=82,83,84,85を対象にした。
旧raw proofが一時領域に見つからなかったため、この未監査4 dだけ新しい証明を生成した。
実行中の同対象計算はなく、既存143件の監査や既存raw evidenceを上書きしていない。

既存の辺cacheを読み、2531と837640行のheaderを付けて `edges.txt.gz` へ保存した。
全837640四点を、generatorとは別のgeneric整数4×4検査器で真の禁止四点と確認した。
辺集合の完全性は主張せず、UNSATには健全な部分集合で十分であることを使う。
原点と完全対{d,2531-d}を固定し、他の各対は低側または高側を1つ選ぶ。
各禁止四点の全選択を避ける節を投影し、元generatorの節集合と独立な直接投影の一致も確認した。

全4入力は各1265変数・38160節。CaDiCaLは各約5.0〜5.3秒でUNSATを返した。
原DRATを保存し、固定upstream DRAT-trim -Uで各約3.8〜4.1秒で受理・LRAT化した。
さらに空節処理を修正した別実装lrat-checkで各約1.0〜1.2秒、全4 LRATを受理した。
各入力・原DRAT・LRATをgzipでGit管理し、各result.jsonにsource/binary/input/proof hashと実stdoutを保存する。
raw LRATは同じ出力先にローカル保持し、Git対象から除外する。

`verify_saved.py` はSATソルバや元generatorを使わず、保存された全辺から独立な投影節集合を作る。
各入力の全節集合、原DRAT・LRAT・source hash、整数幾何receiptと各受理記録を照合した。
既存修正版143 dと新LRAT4 dは重複がなく、被覆の和は147/1265、未被覆1118である。
異なる検証器を同じsource hashの履歴へ混ぜない。全数監査完了や数学的な一般証明は主張しない。

初回はgeneratorの依存moduleのimportで失敗し、solver開始前に中断した。
その時の `output/batch82-85/edges.txt.gz` は保持し、import経路を直した後は新しい出力先v2を使った。
外側の実行ツールは全記録出力後の終了値を1と報告したが、各独立C検査は終了コード0で受理し、
保存証拠と別コードによる全節schema・hash照合が成功したことを採用根拠にする。
外側の終了値の原因は未確定で、正常終了の推測で採用範囲を広げない。

元cacheがある環境では、新しい出力先へ再現できる:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2531-lrat-20261109/audit.py --edges C:/Users/yuubi/AppData/Local/Temp/kyouen-parabola/edges_2531.txt --ds 82,83,84,85 --output FRESH-batch --budget 100000
uv run --locked python research/experiments/parabola-p2531-lrat-20261109/verify_saved.py --saved research/experiments/parabola-p2531-lrat-20261109/output/batch82-85-v2 --output FRESH-verification.json
```

別checkoutでは保存 `edges.txt.gz` を展開し、先頭のpと辺数の1行を除いた本文を新しいcache fileへ復元し、
そのpathを `--edges` へ渡す。保存証拠の照合には新しいSAT探索は不要である。
既存の固定sourceのDRAT-trim6制御と修正LRAT5制御も新しい出力先で実行し、全て期待通りだった。
