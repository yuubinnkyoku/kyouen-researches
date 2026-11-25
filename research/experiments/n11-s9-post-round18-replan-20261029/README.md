# N11 第18回後の証明限定再計画（第19回入力）

第9〜18回の固定9石証明書を読み直し、第18回の終局証人を独立検証してから、WIN9→WIN8の伝播と10石LOSS証人→LOSS9親の導出を行う。異なる回のWIN9/LOSS9衝突、WIN8/LOSS8衝突、SHA-256の不一致、上位証明の既存固定結果との不一致を即時検出する。

固定14根計画の未証明8石辺だけを対象とし、既に選んだ9石局面と証明済みLOSS9親を除外する。残りの9石候補から支配関係を削除し、最大32候補を選択する。再計画は**探索対象の選定**であり、潜在被覆や未完探索をWIN/LOSSに読み替えない。

実行: `node research/experiments/n11-s9-post-round18-replan-20261029/replan.js`。実行結果はCI成果物 `n11-round18-replan` に保存し、検証後に `next-plan.json` へ固定する。前回の `lift.json` がまだ固定されていない場合も、第18回の独立検証器と `lift.js` を再実行して導出する。結果を固定した後は再実行結果と厳密一致させる。


## 固定結果（2026-10-29）

再計画CI [40807697423](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40807697423)は成功し、成果物12869540624（ZIP SHA-256 `1ff023be55065ca65cf17345225dd610d7db293de484a92dfe0613092d53e420`）を `next-plan.json` に固定した。未証明9石候補は116→93類、支配関係削減後は12類。第19回はこの12類だけを対象とする。潜在被覆12は勝敗証明ではない。

独立したPython実装 `preflight_independent.py` は、全12局面の安全性・D4正規化と全合法10石子を、3×3差分行列式および4×4整数行列式の置換展開で照合する。結果は `preflight.json` に固定し、`python3 research/experiments/n11-s9-post-round18-replan-20261029/preflight_independent.py` で厳密一致を再検査する。329本の合法子はすべて異なるD4類で、12候補間の共有は0類。

固定14根計画の未証明辺44本、証明限定WIN8 5,803類は不変。新規二石root閉鎖0。空盤UNKNOWN。

**標準11×11空盤の勝敗はUNKNOWN。**
