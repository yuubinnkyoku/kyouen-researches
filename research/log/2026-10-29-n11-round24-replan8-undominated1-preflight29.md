# 2026-10-29: N11第24回証明後の再計画で第25回候補を1類に限定

[証明限定再計画CI 40871756803](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40871756803) が成功。第9〜24回の証明書を再照合し、第24回WIN9 1類・LOSS9 2類、LOSS9親閉包20類、証明限定8石WIN 5,859類、固定14根計画の未証明37辺を確認。WIN/LOSS衝突0件。成果物ZIP SHA-256 `665572aa3e62ce39b86c21123c8a9e493360fd3299f8d141cdb7f61c6e0d9a8a`、選定結果は[固定計画](../experiments/n11-s9-post-round24-replan-20261029/next-plan.json)。

第24回以前の未証明9石候補12類から、今回の証明で選択済み3類を除外。LOSS9親閉包による追加除外0類。残る9類のうち1類は未証明37辺に触れず、8類を支配削減して**1類**を選定。潜在被覆1辺、合法10石子29本で、前回87本から**66.7%削減**。候補削減は勝敗証明ではない。

[独立事前検証CI 40872478425](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40872478425) は3×3差分行列式と4×4整数行列式の9,534件を照合し成功。1局面の合法子29本・29類（重複0）。成果物ZIP SHA-256 `32faa407474bddd266c3e4a9bf03364c796d5d568b4cda8b93b0caf2eb906bb9`、結果は[独立事前検証](../experiments/n11-s9-post-round24-replan-20261029/preflight.json)に固定。

二石root閉鎖0件。第25回の証明書が独立検証されるまでは新しい勝敗を計上しない。**標準11×11空盤はUNKNOWN**。
