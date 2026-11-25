# 保存されたp2207の1104点候補の独立幾何監査

eece6d3cでコミットされたshape_c_2207.jsonから1104パラメータを抽出した。
元JSONのSATとsafe_against_edgesの自己判定を安全性の根拠にせず、別実装のgeneric整数4x4行列式で検査する。
現在の主張は[K0722](../../knowledge/items/K0722-p2207-safe-lower-bound-1104.md)を参照する。

```sh
uv run --locked python research/experiments/parabola-p2207-1104-witness-20261110/audit.py --output FRESH-output
```

outputは既存ディレクトリを上書きしない。sourceのpoint listから作る固定入力のSHA-256は
ce97d4a9447fd32cd67e3cfad59151774fa45cf90c8985287abb1a45480e2347。
原点を含み、完全対は307、空対は1078であることも点集合から再計算した。
元JSONとcandidate、driver、C++検査器のhashはextraction.jsonとgeometry.jsonへ保存した。

全61560516876四点を完全な合同式フィルタで被覆し、残る27941252四点の整数行列式は全て非零だった。
安全三点は受理し、既知の禁止四点・重複・入力打切り・合成数は拒否する5制御も確認した。
geometry.jsonのstdoutは`2207 1104 61560516876 27941252`、終了コード0、経過時間約10.66秒。

これは1104点の安全性による下界である。一般定理の上界1105と合わせて1104<=A(2207)<=1105。
K0693の未完了の全数UNSAT監査を完了したとは扱わず、正確値1104は採用しない。
元の走査結果・既存source・receiptは変更していない。新しいSAT探索は起動していない。
既存outputを再指定するとFileExistsErrorで拒否され、元の4ファイルのhashが変わらないことも確認した（output/overwrite-control.json）。
