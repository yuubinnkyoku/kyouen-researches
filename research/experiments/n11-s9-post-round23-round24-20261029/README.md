# N11 第24回・選定3局面の限定終局探索

[固定再計画](../n11-s9-post-round23-replan-20261029/next-plan.json)と[独立事前検証](../n11-s9-post-round23-replan-20261029/preflight.json)に基づき、9石3類・合法10石子87本のみを探索。

[探索CI 40864388504](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40864388504) の証人を[certificate.json](certificate.json)に固定。[独立検証CI 40864771805](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40864771805) はNode・Pythonとも成功。9石WIN1類、LOSS2類を検証し、最小終局証明義務31類、再帰状態6,847。偽証人・範囲外番号の拒否と過去証明との衝突検査を実施。

WIN9の8石親は9類。既存証明との重複を除いた純増と固定14根計画への寄与は、[lift.js](lift.js) の独立伝播を確定するまで未計上。二石root閉鎖0件、標準11×11空盤 **UNKNOWN**。
