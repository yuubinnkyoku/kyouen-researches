# 2026-10-29: N11第25回・9石LOSS1類を独立終局証明

[第24回後の証明限定再計画](../experiments/n11-s9-post-round24-replan-20261029/next-plan.json)が選んだ9石1類のみを探索。[独立事前検証](../experiments/n11-s9-post-round24-replan-20261029/preflight.json)で合法10石子29本・29類、3×3差分行列式と4×4整数行列式9,534件の一致を確認した。

[限定探索CI 40872665397](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40872665397) が成功。9石 `000420100000008210a0000000000020` はLOSSで、証人は辞書順10石子の添字1。初回は2終局葉・840再帰状態、LOSS10証人の9石親閉包10類。証人は[固定証明書](../experiments/n11-s9-post-round24-round25-20261029/certificate.json)に保存。探索成果物ZIP SHA-256 `081a598d01b163ae6320776c441f7d17f86259d04ebb967bc383844412ec91b0`。

[独立検証CI 40872891045](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40872891045) がNode・Pythonとも成功。双方で**LOSS9 1類、最小終局証明義務1類、499再帰状態**を再計算。Nodeは2種類の整数幾何を照合し、Pythonは独立したBareiss行列式と再帰を用いる。偽のWIN証人と範囲外番号を拒否し、過去のWIN9証明との極性衝突0件。独立検証成果物ZIP SHA-256 `2d51d9c2691561cb2f8c899e17f18f228ef9a513d0241fd7573b468f7c51777b`。

WIN9は増えていないため証明限定WIN8は5,859類、固定14根計画の未証明辺は37本。新規二石root閉鎖0件。第26回の再計画ではLOSS9親閉包10類を除外集合に反映する。**標準11×11空盤はUNKNOWN**。
