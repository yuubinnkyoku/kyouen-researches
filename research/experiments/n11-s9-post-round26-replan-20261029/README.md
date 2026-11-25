# N11 第26回後の証明限定再計画（第27回候補）

第26回の独立検証済み9石LOSS1類（最小終局証明義務1類、439再帰状態）を再検査し、第9〜26回の固定証明書を照合した。異なる回のWIN9と、LOSS10証人から導出したLOSS9親閉包の極性衝突は0件。

[再計画CI 40888329887](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40888329887) 成功。再現コードは [replan.js](replan.js)、確定出力は [next-plan.json](next-plan.json)。

第26回前の未証明9石候補7類から、独立証明済みの選定1類を除外。LOSS9親閉包10類による追加除外は0類。残り**6類**は未証明37辺に触れ、支配削減後の候補は**1類**。第27回の候補 `00042010004000821080000000000020` は潜在被覆1辺、合法10石子29本。潜在被覆はWIN8証明ではない。

[独立事前検証CI 40889400749](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40889400749) 成功。[preflight_independent.py](preflight_independent.py) は独立した3×3差分行列式と4×4整数行列式を9,534回照合し、合法10石子29本・29類、重複0件を確認。結果は [preflight.json](preflight.json) に固定。

この再計画は固定14根計画に限定され、未証明37辺が空盤全体の残義務を意味するわけではない。証明限定8石WINは5,859類、新規二石root閉鎖0件。**標準11×11空盤はUNKNOWN**。
