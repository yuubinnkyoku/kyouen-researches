# N11 第21回・選定8局面の限定終局探索

第20回までの独立検証済み証明書と、[第21回の固定再計画](../n11-s9-post-round20-replan-20261029/next-plan.json)だけを入力とする。8類の9石局面について合法な10石子を調べ、WIN9なら全合法子のWIN、LOSS9なら1つのLOSS10証人を必要とする。9石局面を勝敗未確定のまま打切り判定しない。

入力計画は証明限定8石WIN 5,827類、固定14根計画の未証明41辺、候補47類から支配削減8類、潜在被覆8辺、合法10石着手226本。独立したPythonの3×3/4×4整数幾何による[事前照合](../n11-s9-post-round20-replan-20261029/preflight_independent.py)を前提とする。

`node research/experiments/n11-s9-post-round20-round21-20261029/prove.js` で限定探索し、CI成果物 `n11-round21-discovery` を得る。結果は独立した終局検証器で再検査し、`certificate.json` に固定するまで勝敗証明として数えない。共有cacheの推測値、探索途中のpn/dn、候補の潜在被覆を勝敗として扱わない。二石rootの閉鎖は未確認で、**11×11空盤UNKNOWN**。
