# N11 第26回・9石1局面の限定終局証明

[第25回後の固定再計画](../n11-s9-post-round25-replan-20261029/next-plan.json)と[独立事前検証](../n11-s9-post-round25-replan-20261029/preflight.json)に基づき、9石1類 `00042010000100821080000000000020` の合法10石子29本のみを調べた。

[限定探索CI 40880675504](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40880675504) 成功。証人を[certificate.json](certificate.json)に固定。初回探索ではLOSS9 1類（WIN9 0類）、LOSS10証人の辞書順添字8、最初の証人まで9終局葉・1,472再帰状態。証人から合法な9石親10類を導出した。探索成果物ZIP SHA-256 `47762a22e9c0a11d57e863899565bdc51baa88fa2f1f2f6de3b3163476598923`。

[独立終局検証CI 40880965070](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40880965070) はNode・Pythonの双方で成功。Nodeは別々の3×3・4×4整数幾何と終局再帰、PythonはBareiss整数行列式と独立再帰を用い、**LOSS9 1類、最小終局証明義務1類、439再帰状態**で一致した。偽WIN証人・範囲外番号の拒否、過去のWIN9との極性衝突検査も成功。独立検証成果物ZIP SHA-256 `f68381de7ec0cb13749bb255f141e0ff3ace108490ef1e85277bb3defc1116e0`。

今回の証明はWIN9を増やさないため、証明限定WIN8は**5,859類**、固定14根計画の未証明辺は**37本**のまま。新規二石root閉鎖0件、標準11×11空盤は **UNKNOWN**。
