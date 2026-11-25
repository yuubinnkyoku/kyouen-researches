# p2539: 60個の幾何学的除外単位節を加えた五点削除probe（2026-11-11）

保存実行の結果は**UNKNOWN**。非存在・存在や新しい上下界は得ていない。
現在の必要条件はK0727を参照する。過去のUNKNOWN入力は上書きしていない。

## 入力と結果

親は`../parabola-p2539-five-pair-split-20261111/output/retained/input.cnf.gz`で、非圧縮SHA-256は
`64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b`。
原点と完全対{6,2533}を保ち、exact1259点・種からのexact五点損失を要求する。
種SのSHA-256は`454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb`。

前回独立hitting-tree・整数幾何で排除した60点uについて、point変数a_uの負単位節を追加した。
point baseは36512、追加節は`[-(36512+u)]`。親51570変数144546節を保持し、144606節とした。
新入力の非圧縮SHA-256は`ea0b35e2e934035cea98abc6f491f9312c11830d60347b8097e9eebe62fd8656`。
これらは保存された幾何・hitting-tree根拠を持つ単位節であり、親CNFだけのRUP導出を今回生成したものではない。

PySAT 1.9.dev21のCadical195、proof-disabled、conflict budget100000で一回だけ実行した。
85.197秒・100000 conflictsでUNKNOWN、子プロセスは終了値0。SATモデルも完結した負証明もない。
親は保持側・同予算でUNKNOWNだったが、今回は独立排除済みの新しい60節を採用した異なる入力である。
同じ新入力を同じ予算で再実行していない。`run.py`は一子を300秒に制限し、実終了値・stdout・stderrを保存する。

## 入力・根拠の独立検査

`schema.py`は探索コードやSATライブラリをimportしない。
親の全構造・幾何・exact損失・B6単位節を既存独立schemaで解釈し、byte SHAで同一親を確認する。
末尾60節は独立証明書に記載された除外点への負point単位節と全照合する。
60点の負hitting-treeを既存独立検査器で再生し、親の38868幾何四点と、
今回の60証明で参照する2507四点をそれぞれgeneric整数4×4行列式0と実検査した。
`input-audit/`はこの意味と幾何入力の監査であり、UNKNOWNをUNSATへ昇格させるものではない。

`regression.json`は実入力10改変の拒否と60負point単位節の120真理値割当て。
親のprefix・exact損失・四状態と、hitting-treeの帰納健全性・回帰は以前の凍結根拠を引き継ぐ。
新しい検査器・コンパイラ一般の形式的健全性やLean形式証明は主張しない。

## 再現と継続

repo rootで新しい出力pathを使う。

```powershell
$exp='research/experiments/parabola-p2539-five-pruned-20261111'
uv run --locked python "$exp/check_inputs.py" --saved "$exp/output" --output "$exp/input-audit-fresh"
uv run --locked python "$exp/regression.py" --output "$exp/regression-fresh.json"
```

probeの再現は`uv run --locked --with python-sat==1.9.dev21 python <exp>/run.py --output <fresh-directory> --budget 100000`。
UNKNOWNの再現だけを目的に探索を起動する必要はない。
次回は二点同時追加の障害など、残る候補同士の制約を評価できる。
または、除外単位節の根拠を親CNFの具体節へ照合し、各a_u仮定下のRUP証明を¬a_uでliftして単位節を導く方式を検討できる。
後者は今回未実装・未検証であり、保存証明が親CNFだけのRUPになっているという意味ではない。
全体範囲1258≤A(2539)≤1271、五点削除局所最適性の未解決状態は変わらない。
