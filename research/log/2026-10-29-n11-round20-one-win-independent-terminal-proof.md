# 2026-10-29: N11第20回9石1 WIN / 8 LOSSを独立終局検証

第19回の固定14根計画（未証明42辺）から選定した9石9類について、[限定終局探索CI 40821512573](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40821512573) が成功した。成果物12874377901を回収し、`research/experiments/n11-s9-post-round19-round20-20261029/certificate.json` に固定した。証人SHA-256 `c9f0f248820a46c919240144e267206effaba58ed2c6d59e13a40931c6aaadca`。

独立Node検証 [CI 40821636470](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40821636470) と、共有Node実装・探索キャッシュに依存しないPython検証 [CI 40821639618](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40821639618) は両方成功。

- **WIN9 1類 / LOSS9 8類**。WIN9は合法な10石子28本すべてがWIN、LOSS9は合法なLOSS10証人を持つ。
- 合法10石着手251本（異なる10石局面250類）。第20回の初回探索は終局局面127類・再帰状態25,114。証明書を使う独立検証は**36終局局面・10,692再帰状態**。検証の終局局面数は初回より71.7%少なく、状態数は57.4%少ない。
- 8石WIN親は9類、LOSS10証人からのLOSS9親閉包は80類。WIN9/LOSS9衝突なし。偽WIN/LOSS証人と不正番号を拒否する試験に成功。
- 3×3差分行列式と独立4×4整数行列式による境界照合も[CI 40821434669](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40821434669) で成功済み。

証明済みWIN8の純増数、固定14根計画の未証明辺の減少数は、上位伝播の独立検査と固定結果が出るまで未確定。二石root閉鎖は0件。**標準11×11空盤の勝敗はUNKNOWN。**
