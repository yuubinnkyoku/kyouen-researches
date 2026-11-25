# 2026-10-29: N11第22回・9石5類のLOSSを独立終局検証

第21回までの独立証明と[固定再計画](../experiments/n11-s9-post-round21-replan-20261029/next-plan.json)を入力に、支配縮約後の5類だけを終局まで検査した。標準11×11空盤の勝敗は **UNKNOWN**。

最初の[探索CI 40841234946](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40841234946) は、8類版からの移植時に `new Set(keys).size===8` を残したため、勝敗計算前の入力検査で失敗した。[修正 bce7e745](https://github.com/yuubinnkyoku/kyouen-researches/commit/bce7e7454d59507567a4d6a82b7462c4d862ce75) 後の[限定探索CI 40841361442](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40841361442) は**成功**。成果物 `n11-round22-discovery`（ID 12882419177、ZIP SHA-256 `004034fda1f6f5721e6afa2a6965d994825ad195f88274f3524edc9f6989c9d8`）を回収し、展開した `round22-discovery.json`（SHA-256 `d8304ebecce625b743d6e5a51f87da25b81e2a0a307a9ddb2d60a55f0431f622`）を `certificate.json` に固定した。

**独立Node・Python検証 [CI 40841553819](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40841553819) は両方成功**。Nodeは2種類の整数幾何による終局再帰と、偽WIN証人・範囲外証人の拒否を検査。PythonはNode実装・共有探索cacheを使用せず、独立したD4正準化・4×4 Bareiss整数行列式・終局再帰で5件のLOSS10証人を再計算した。双方で終局10石葉5類、再帰状態1,300、9石LOSS 5類、LOSS9親閉包50類が一致した。

| 指標 | 確定値 |
|---|---:|
| 第22回の選択9石根 | 5類 |
| 独立検証済みWIN9 / LOSS9 | **0 / 5類** |
| 全合法10石着手 | 138本・138類 |
| LOSS10証人の終局義務 | **5類** |
| LOSS10証人から導出したLOSS9親閉包 | **50類** |
| 初回探索の10石終局葉 | 30類 |
| 独立検証の10石終局葉 | **5類** |
| 初回探索の再帰状態 | 5,182 |
| 独立検証の再帰状態 | **1,300** |
| WIN/LOSS衝突（選択根と親閉包） | 0 |
| 新規二石root閉鎖 | 0 |

証人限定の独立検証は初回探索と比べ終局葉83.3%、再帰状態74.9%減。ただし同じ探索義務を処理した速度比較ではない。親閉包50類は今回の5類を含み、過去の証明済みLOSS9との重複を除いた**純増数は未集計**。

今回WIN9が無いため、証明限定8石WINは**5,835類のまま**、固定14根計画の未証明辺は**40本のまま**。次は既存LOSS9親閉包と統合し、候補から除外して第23回の探索対象を選ぶ。**空盤UNKNOWN。**
