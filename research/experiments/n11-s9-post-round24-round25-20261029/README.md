# N11 第25回・9石1局面の限定終局証明

[第24回後の固定再計画](../n11-s9-post-round24-replan-20261029/next-plan.json)と[独立事前検証](../n11-s9-post-round24-replan-20261029/preflight.json)に基づき、9石1類 `000420100000008210a0000000000020` の合法10石子29本のみを調べた。

[限定探索CI 40872665397](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40872665397) 成功。証人を[certificate.json](certificate.json)に固定。初回探索ではLOSS9 1類（WIN9 0類）、LOSS10証人の辞書順添字1、最初の証人まで2終局葉・840再帰状態。証人から合法な9石親10類を導出した。探索成果物ZIP SHA-256 `081a598d01b163ae6320776c441f7d17f86259d04ebb967bc383844412ec91b0`。

[独立終局検証CI 40872891045](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40872891045) はNode・Pythonの双方で成功。Nodeは別々の3×3・4×4整数幾何と終局再帰、PythonはBareiss整数行列式と独立再帰を用い、**LOSS9 1類、最小終局証明義務1類、499再帰状態**で一致した。偽WIN証人・範囲外番号の拒否、過去のWIN9との極性衝突検査も成功。独立検証成果物ZIP SHA-256 `2d51d9c2691561cb2f8c899e17f18f228ef9a513d0241fd7573b468f7c51777b`。

今回の証明はWIN9を増やさないため、証明限定WIN8は5,859類、固定14根計画の未証明辺は37本のまま。新規二石root閉鎖0件、標準11×11空盤は **UNKNOWN**。
