# N11 第27回・9石1局面の限定終局証明

[第26回後の証明限定再計画](../n11-s9-post-round26-replan-20261029/next-plan.json)で選んだ9石1類 `00042010004000821080000000000020` のみを対象とした。[独立事前検証](../n11-s9-post-round26-replan-20261029/preflight.json)では合法10石子29本・29類、整数行列式9,534件の一致を確認。

[限定探索CI 40889593385](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40889593385) 成功。WIN9 0類、LOSS9 1類。辞書順10石子の添字1がLOSS10証人で、初回探索は2終局葉・233再帰状態。証人から合法な9石親10類を導出した。探索結果は [certificate.json](certificate.json) に固定。

[独立終局検証CI 40889814358](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40889814358) はNodeとPythonの双方で成功。Nodeは2種の整数幾何と終局再帰を検査し、偽のWIN証人・範囲外添字を拒否。Pythonは独立したBareiss整数行列式と再帰で**LOSS9 1類、終局証明義務1類、163再帰状態**を再計算。過去のWIN9証明との極性衝突0件。

今回WIN9は増えないため証明限定8石WINは**5,859類**、固定14根計画の未証明辺は**37本**。新規二石root閉鎖0件。未完探索数を勝敗や距離として扱わない。**標準11×11空盤はUNKNOWN**。
