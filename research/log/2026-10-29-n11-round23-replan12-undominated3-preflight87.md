# 2026-10-29: N11第23回証明後の再計画で第24回候補を3類に限定

[証明限定再計画CI 40862891827](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40862891827) が成功。第9〜23回の証明書を再検査し、第23回のWIN9 2類・LOSS9 3類、LOSS9親閉包30類、証明限定8石WIN 5,851類、固定14根計画の未証明38辺を再確認。WIN/LOSS衝突0件。

第23回以前の未証明9石候補27類のうち、今回の証明で6類を除外（探索済み5類＋追加LOSS9親1類）。残り21類のうち9類は未証明38辺に寄与しない。対象12類を支配削減し、3類を選定。選択根の潜在被覆は3辺、合法10石着手は87本で、前回の140本から**37.9%削減**。これは計算量の事前見積りであり、WIN/LOSS証明数ではない。

再計画成果物ZIP SHA-256 `9539ad66344c90463c2670eda440ab13003fa69f17382f9dbea8a28cc87646e4`、内部JSON SHA-256 `591ff88ba64825662b96af7314b4435945b0c9810b7da249a2a90dcf05ed7386`。選択結果は[固定計画](../experiments/n11-s9-post-round23-replan-20261029/next-plan.json)に保存。

[独立事前検証CI 40864080949](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40864080949) は3×3差分行列式と4×4整数行列式の28,602件を照合し成功。3根の合法子数は [29,29,29]、合計87本・87類、重複0。成果物ZIP SHA-256 `d8f166f96bc59b22ed9870aeec9e0ccb3c5936388b0eb3ad87e2547f382f61e8`、内部JSON SHA-256 `94dcbfe757ba743e29b4c595096df828fd85bc61bea479b3c5d89de97fb72689`。結果を[preflight.json](../experiments/n11-s9-post-round23-replan-20261029/preflight.json)に固定。

第24回の限定終局探索は証明書回収・独立検証まで未確定。二石root閉鎖0件、**標準11×11空盤はUNKNOWN**。
