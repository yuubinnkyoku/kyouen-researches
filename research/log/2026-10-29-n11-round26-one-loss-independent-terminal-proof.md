# 2026-10-29: N11第26回・9石LOSS1類を独立終局証明

[第25回後の証明限定再計画](../experiments/n11-s9-post-round25-replan-20261029/next-plan.json)が選んだ9石1類のみを探索。[独立事前検証](../experiments/n11-s9-post-round25-replan-20261029/preflight.json)で合法10石子29本・29類、3×3差分行列式と4×4整数行列式9,534件の一致を確認した。

[限定探索CI 40880675504](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40880675504) が成功。9石 `00042010000100821080000000000020` はLOSSで、証人は辞書順10石子の添字8。初回は9終局葉・1,472再帰状態、LOSS10証人の9石親閉包10類。証人は[固定証明書](../experiments/n11-s9-post-round25-round26-20261029/certificate.json)に保存。探索成果物ZIP SHA-256 `47762a22e9c0a11d57e863899565bdc51baa88fa2f1f2f6de3b3163476598923`。

[独立検証CI 40880965070](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40880965070) がNode・Pythonとも成功。双方で**LOSS9 1類、最小終局証明義務1類、439再帰状態**を再計算。Nodeは2種類の整数幾何を照合し、Pythonは独立したBareiss行列式と再帰を用いる。偽のWIN証人と範囲外番号を拒否し、過去のWIN9証明との極性衝突0件。独立検証成果物ZIP SHA-256 `f68381de7ec0cb13749bb255f141e0ff3ace108490ef1e85277bb3defc1116e0`。

WIN9は増えていないため証明限定WIN8は5,859類、固定14根計画の未証明辺は37本。新規二石root閉鎖0件。第27回の再計画ではLOSS9親閉包10類を除外集合に反映する。**標準11×11空盤はUNKNOWN**。
