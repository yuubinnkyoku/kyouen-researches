# 2026-10-29: N11第22回証明を再利用し第23回の5根・140子を固定

第22回の9石LOSS 5類・LOSS9親閉包50類を入力とする[証明限定再計画CI 40847747047](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40847747047)が成功。成果物ZIP SHA-256 `b2b57b43e272862b0b1a00ebd2b44e22fa40c77c3b6ff6c531b13d146626e383`、内部JSON SHA-256 `562a9bf3e3f0ad9fdf4a5bf401a3b923dde26884fe527ee0299b13f67e22b14c` を確認し、[next-plan.json](../experiments/n11-s9-post-round22-replan-20261029/next-plan.json) に固定。

第9〜22回の固定証明書を再利用し、WIN/LOSS衝突0件を確認。候補は32→27類（第22回で探索済みの5類を除外）、支配削減後5類。前回の5類138本に対して今回の選定5類は合法10石子140本。潜在被覆5辺は前回と同数であり、証明済み被覆ではない。LOSS9親閉包50類は既存候補から追加除外0類で、純増50類と解釈しない。

独立Python整数幾何で3×3差分行列式と4×4行列式の47,670件の一致を検査。5根の合法子数は [26,28,28,29,29]、計140本すべて異なる10石類。独立照合結果を[preflight.json](../experiments/n11-s9-post-round22-replan-20261029/preflight.json)に固定し、再実行用スクリプトを保存。

第23回の5類のみを終局探索する専用の[限定探索コード](../experiments/n11-s9-post-round22-round23-20261029/prove.js)とCIを追加。CI実行だけでは新たなWIN/LOSS証明とはしない。現時点の証明限定8石WINは5,835類、固定14根計画の未証明辺40本、新規二石root閉鎖0件。**標準11×11空盤はUNKNOWN。**
