# 2026-10-29: N11第19回、2 WIN9 / 10 LOSS9を独立終局証明

第18回後の固定再計画で選ばれた12類だけを探索した。入力 `research/experiments/n11-s9-post-round18-replan-20261029/next-plan.json` のSHA-256（選択鍵列）は `564a47bb41339d9fb665536faccd697ed7ce7fac6ec83b3ccbe5e616f3dace2c`。独立事前監査は329本の合法10石子を329類と確認済み。

[探索CI 40810196930](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40810196930) は成功し、成果物12869383857（ZIP SHA-256 `a5091601d40d14450d98fff3045703d10dbf0cb682aa4ac02e7b596fba04b65f`）の `certificate.json` をmainへ固定した。9石局面は**2 WIN / 10 LOSS**。WINの全10石子56本を検査し、LOSS10証人を含む初回探索の義務121件、異なる終局局面121類、幾何実装あたり再帰状態21,348。LOSS10証人から導出したLOSS9親閉包100類、WIN9との衝突0。

[独立終局検証CI 40810302248](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40810302248) が成功。WIN9は全合法10石子を、LOSS9は合法なLOSS10証人を、異なる整数幾何実装で再検査し、偽証人・範囲外番号の拒否試験を通した。さらに[独立Python再帰検証CI 40810437527](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40810437527) が成功。共有Node実装・探索cache・df-pnを使わず、10石終局局面66類、再帰状態11,350、WIN8親18類、LOSS9親100類を再現した。初回探索の121終局局面と独立検証の66終局局面は検査義務の違いであり、勝敗数ではない。

上位8石WINへの伝播は別の `lift.js` に分離しており、成功・固定までは証明限定WIN8 **5,803類**、固定14根計画の未証明辺**44本**を維持する。今回の新規二石root閉鎖0。**標準11×11空盤の勝敗はUNKNOWN。**
