# p2207の単一CNF上界を独立監査する

現在の上界は[K0693](../../knowledge/items/K0693-p2207-no-parabola-equality-witness.md)、下界と正確値は[K0722](../../knowledge/items/K0722-p2207-safe-lower-bound-1104.md)を参照する。
元CNFとDRATはea4ab649に保存されたものを保持し、SAT探索を再実行しない。

```sh
uv run --locked python research/experiments/parabola-p2207-single-cnf-audit-20261110/audit.py --output FRESH-output --timeout 180
uv run --locked python research/experiments/parabola-p2207-single-cnf-audit-20261110/regression.py --output FRESH-regression.json
uv run --locked python research/experiments/parabola-p2207-single-cnf-audit-20261110/replay.py --saved research/experiments/parabola-p2207-single-cnf-audit-20261110/output --output FRESH-replay.json
```

いずれも既存出力を上書きしない。新しいCNF・DRATを生成せず、採用CNF gzipとLRAT gzipをGit管理する。
raw core.lratはローカル保持してGit除外し、元DRAT gzipも元artifactに保持する。

## 形状からCNFへの論理

安全1105点集合は、原点を含み、完全対一つ、空対なしに限られる（K0097）。
各対にBOTH/NONE/LOW/HIGHのone-hotを与え、BOTHはちょうど一つ、NONEは全て偽、点選択はBOTHまたは対応する側と同値とする。
schema.pyはCardEncや探索builderをimportせず、これらを明示節として再構成する。

構造節はone-hot 7721、BOTHのat-least-oneとSinz counter 3306、NONE単位節1103、点定義6618の計18748。
変数領域は選択子1..4412、counter 4413..5514、点5515..7720で、交差しない。
保存CNFの構造節は全てこれと一致し、残る31868節は全て負の点literalからなる幾何節だった。
原点は必ず選択されるため、三literalの節には0を戻して四点を復元する。
全提供辺を探索と独立なgeneric整数4x4行列式で禁止四点と確認した。

任意の安全1105点集合Sを仮定する。対状態と点選択をSから割り当て、counterにはBOTHのprefix ORを割り当てれば構造節を全て満たす。
Sinzの単調prefix節と各BOTHの阻止節は、二つ目のBOTHを排除し、ちょうど一つのBOTHに対するprefix割当を許す。
各幾何節は真の禁止四点なので、Sの安全性から全て満たされる。したがってSがあればCNFモデルがある。
この方向の論理に辺集合の完全性は不要である。独立検査したCNFのUNSATにより安全1105点集合を排除できる。

## 証拠と制御

7720変数・50616節、元DRAT 497179行。元DRATのSHA-256はf0ce140db899e4c9009fced1bc38aa753315d71bd8eb9f1498db0c74ad77a7ea。
固定DRAT-trim -U（RUP限定）が32.22秒で受理した。
抽出LRATは187955行・100042045 bytesで、空節処理修正版C検査器が16.73秒で受理した。
圧縮CNF・LRATからの別処理による実再生、全source・schema・幾何・証拠hashと既存下界receiptの照合も成功した。

p=5,7,11の全1104対状態について全counter補助割当の存在射影を検査し、独立な形状条件と一致した。
構造節欠落・余分な正単位節・選択子を使う幾何節・重複点・入力打切り・点と選択子のaliasの6改変を拒否した。
構文だけでは通る非辺を幾何検査で拒否し、真の辺を受理する2制御も実行した。
有限の回帰であり、検査器全体の形式的健全性証明ではない。

単一CNF経路で上界1104が独立監査済みになった。旧d別の21/1103という被覆数は変更せず、全dを個別再生したとは扱わない。
既存の独立1104点下界と合わせてA(2207)=1104という有限計算の結論を採用する。Lean形式証明や他素数への一般化ではない。
