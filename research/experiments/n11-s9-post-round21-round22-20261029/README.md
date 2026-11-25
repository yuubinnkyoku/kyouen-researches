# N11 第22回・選定5局面の限定終局探索

第21回までの独立検証済み証明書と、[第22回の固定再計画](../n11-s9-post-round21-replan-20261029/next-plan.json)のみを入力とする。5類の9石局面について合法な10石子138本を調べ、WIN9なら全合法子のWIN、LOSS9なら合法なLOSS10証人を要求する。途中探索や未完局面を勝敗に読み替えない。

入力計画は証明限定8石WIN 5,835類、固定14根計画の未証明40辺、候補32類から支配削減5類、潜在被覆5辺、合法10石着手138本。独立Pythonによる3×3/4×4整数幾何の[事前照合](../n11-s9-post-round21-replan-20261029/preflight_independent.py)は成功済み。

`node research/experiments/n11-s9-post-round21-round22-20261029/prove.js` で限定探索し、CI成果物 `n11-round22-discovery` を得る。**独立終局検証と証明書の固定が完了するまで新規WIN/LOSSに数えない。** 二石rootの閉鎖は未確認で、標準11×11空盤は **UNKNOWN**。
