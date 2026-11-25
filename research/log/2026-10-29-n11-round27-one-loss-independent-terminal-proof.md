# 2026-10-29: N11第27回・9石LOSS1類を独立終局証明

最新mainとAGENTS.md、knowledge正本、過去の第9〜26回証明を確認して再開。第26回のLOSS10証人からの9石親閉包10類を再導出し、全回のWIN9とLOSS9親閉包を照合。矛盾0件。[再計画CI 40888329887](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40888329887) 成功。未証明9石候補は7→6類、支配削減後は1類。潜在被覆は固定14根計画の未証明辺1本、合法10石子29本。結果は[固定計画](../experiments/n11-s9-post-round26-replan-20261029/next-plan.json)に保存。

[独立事前検証CI 40889400749](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40889400749) で3×3差分行列式と4×4整数行列式の9,534件を照合。候補 `00042010004000821080000000000020` の合法10石子29本・29類、重複0件。

[限定探索CI 40889593385](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40889593385) 成功。9石1類はLOSSで、辞書順10石子添字1が証人。初回探索は2終局葉・233再帰状態、LOSS9親閉包10類。証人を[固定証明書](../experiments/n11-s9-post-round26-round27-20261029/certificate.json)に保存。

[独立検証CI 40889814358](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40889814358) はNode・Pythonとも成功。Nodeは2種の整数幾何と終局再帰、偽証人・範囲外添字の拒否を検査。PythonはBareiss整数行列式と独立再帰で最小終局1類・163再帰状態を再計算。過去のWIN9証明との衝突0件。

証明限定8石WINは5,859類、固定14根計画の未証明辺37本、新規二石root閉鎖0件。第28回は今回のLOSS9親閉包10類を除外して候補を再計画する。ただし残候補は6類に縮小しており、候補が尽きる前に未証明8石局面の全合法9石子を精査し、WIN8証明不能な辺を識別する構造監査が重要。固定14根計画の残辺を空盤全体の残義務と混同しない。**標準11×11空盤はUNKNOWN**。
