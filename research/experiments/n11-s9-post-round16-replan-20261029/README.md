# N11 第16回後の証明限定再計画（第17回入力）

第16回までの独立検証済み9石証明書と8石WIN伝播結果を用い、固定14根計画の残る49本の未証明辺に関係する9石候補だけを選び直した。

[再計画CI 40798702949](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40798702949) は成功。成果物12864739126のZIP SHA-256は `600849017cbf0e06586b86b5beb84953fcc641b2db6aece1798d390d3f4800b3`。出力を `next-plan.json` に固定した。未証明候補は215→**158類**（選択済み28、追加のLOSS親5、残る未証明辺に接続しない24を除外）。支配関係による削減後は28→**20類**。第17回の選択は20類、潜在的な8石被覆は20類、合法10石子の予定数は526本。

別実装のPythonで各局面の安全性、D4正規形、3×3差分行列式、4×4整数行列式を検査し、**526本すべてが異なる10石局面**であることを再現した。[独立検証CI 40805015035](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40805015035) も成功。結果は `preflight.json` に固定し、`preflight.js` が再検査する。

`replan.js` は第9〜16回の証明書、10石LOSS証人からの9石LOSS親、SHA-256、回をまたぐWIN/LOSS矛盾、8石への伝播を検査する。結果の「潜在被覆」は勝敗証明ではない。

実行: `node research/experiments/n11-s9-post-round16-replan-20261029/replan.js`、独立検査: `node research/experiments/n11-s9-post-round16-replan-20261029/preflight.js`。

**標準11×11空盤の勝敗はUNKNOWN。**
