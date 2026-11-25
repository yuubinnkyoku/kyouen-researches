# N11 第23回後の証明限定再計画（第24回候補）

[再計画CI 40862891827](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40862891827) 成功。成果物ZIP SHA-256 `9539ad66344c90463c2670eda440ab13003fa69f17382f9dbea8a28cc87646e4`、内部JSON SHA-256 `591ff88ba64825662b96af7314b4435945b0c9810b7da249a2a90dcf05ed7386`。固定結果は [next-plan.json](next-plan.json)。

第9〜23回の証明書を再検査。第23回WIN9 2類からWIN8 16類を純増し、証明限定8石WINは5,835→**5,851類**。固定14根計画の未証明辺は40→**38本**。第23回のLOSS9証人からの親閉包は30類で、既存WIN9と衝突0件。

第23回以前の未証明9石候補27類から、今回の証明で6類を除外（選択済み5類＋新規LOSS親1類）。残り21類のうち9類は残存38辺に触れず、対象12類を支配削減して3類を選定。潜在被覆3辺、合法10石子87本。**潜在被覆は勝敗証明ではない。**

[独立事前検証CI 40864080949](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40864080949) 成功。3×3差分行列式と4×4整数行列式の28,602件を照合し、3局面の合法10石子数は [29,29,29]、計87本・87類（重複0）。成果物ZIP SHA-256 `d8f166f96bc59b22ed9870aeec9e0ccb3c5936388b0eb3ad87e2547f382f61e8`、内部JSON SHA-256 `94dcbfe757ba743e29b4c595096df828fd85bc61bea479b3c5d89de97fb72689`。固定結果は [preflight.json](preflight.json)。

次の探索は選定3局面のみ。証明書を独立検証するまではWIN/LOSSを確定扱いしない。新規二石root閉鎖0件、標準11×11空盤は **UNKNOWN**。
