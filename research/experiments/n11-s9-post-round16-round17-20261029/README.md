# N11 第17回：9石20局面の独立終局証明

第16回後の[再計画CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40798702949)から、未証明9石候補158類のうち支配関係による削減後の20類を選択。独立した[境界検証CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40805015035)が合法10石子526本、異なる10石局面526類、重複0類を確認した。

[限定終局探索CI 40805114064](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40805114064) は成功。**4 WIN9 / 16 LOSS9**、WIN9の全合法10石子103本、初回の終局局面196類・各幾何の再帰状態34,943を確認した。証人列のSHA-256は `008aeae9ac329092d3357132a90944f8303574bcb7964b4d0ec305a3335941fa`。成果物12867363876のZIP SHA-256は `2919df7bb486ada4c9e23ecee5d76a67c5eadea69de4770ebc5d15ebcb7a0d61`。

[独立証明書検証CI 40805214915](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40805214915) は成功。3×3差分行列式と独立4×4整数行列式を用い、WINの全子とLOSSの証人を再帰的に再計算。偽のWIN/LOSS証人と範囲外の番号も拒否した。独立検証に必要な終局局面は**119類**、再帰状態は**21,900**（それぞれ初回から39.3%、37.3%削減）。成果物12867897228のZIP SHA-256は `a5f575bfd0b12f135e888e17d87d0acbde8dac2c9c921417faf1258e91a998e3`。

[WIN8伝播CI 40805303167](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40805303167) も成功。4類のWIN9から36類の8石親を導出し、既存証明との重複4類を除いた**32類**が新規WIN8。証明限定WIN8は**5,763→5,795類**。固定14根計画の証明済み辺は**499/548→503/548**、未証明辺は**49→45本**。WIN8/LOSS8衝突0件。成果物12867888316のZIP SHA-256は `9637539a1b41dce3f6d270bc963fca08753bd688ef08d07e8969d2c3975e4e67`。

再現:
```sh
node research/experiments/n11-s9-post-round16-round17-20261029/prove.js
node research/experiments/n11-s9-post-round16-round17-20261029/verify_compact.js --negative
node research/experiments/n11-s9-post-round16-round17-20261029/lift.js
```

固定証明書 `certificate.json` と固定伝播結果 `lift.json` は各検証器が照合する。今回の結果から新しい7石・5石・二石rootの勝敗は導出されていない。45本は固定14根計画の残りであり、空盤までの残証明数ではない。**標準11×11空盤の勝敗はUNKNOWN。**
