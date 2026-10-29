# N11 第23回・選定5局面の限定終局探索

[固定再計画](../n11-s9-post-round22-replan-20261029/next-plan.json)と独立した[合法着手監査](../n11-s9-post-round22-replan-20261029/preflight.json)で選定した9石5類のみを調べる。合法10石子は140本・140類。WIN9には全合法10石子のWIN証明、LOSS9には少なくとも1つのLOSS10証人を要求する。独立した2種類の整数幾何と終局再帰で照合し、偽証人や衝突は拒否する。

`node research/experiments/n11-s9-post-round22-round23-20261029/prove.js` で限定探索を実行し、専用CIは `n11-round23-discovery` を生成する。**結果を回収し独立検証するまでは勝敗の新規確定値に算入しない。** 二石root閉鎖0件、標準11×11空盤 **UNKNOWN**。
