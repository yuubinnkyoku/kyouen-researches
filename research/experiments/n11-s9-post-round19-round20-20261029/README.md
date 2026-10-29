# N11 第20回: 固定9候補の限定終局探索

入力は第19回証明限定再計画 `../n11-s9-post-round19-replan-20261029/next-plan.json`。9石候補9類、合法10石子251本・250類、選定SHA-256 `ab89b6464e23a5d5ef1a1fb59db6126b52693cf89ccff4e503ce00c2862e0b4a`。

`prove.js` はこの9局面に限定して、3×3差分行列式と独立4×4整数幾何の10石終局判定を比較する。WIN9には全合法10石子、LOSS9には合法なLOSS10証人を要求し、10石終局の重複計算を共有する。異なる回の証明と入力SHA-256を照合し、矛盾時には停止する。

計算結果は専用GitHub Actions `n11-s9-post-round19-round20.yml` の成果物 `n11-round20-discovery` に保存する。**探索出力は独立検証済みの証明書ではない**。成功時には固定証明書と独立Node/Python検証を別途実装してから上位WIN8に反映する。実行失敗・時間切れは勝敗の根拠にならない。

現時点の確定値は証明限定WIN8 5,819類、固定14根計画の未証明42辺、新規二石root閉鎖0件。標準11×11空盤の勝敗は**UNKNOWN**。


## 第20回の独立終局検証（2026-10-29）

[探索CI 40821512573](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40821512573) が成功し、成果物12874377901を `certificate.json` に固定した。結果は**WIN9 1類、LOSS9 8類**。WIN9の全合法10石子28本を証明し、LOSS9の各証人を確認した。

[独立Node検証CI 40821636470](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40821636470) と [独立Python検証CI 40821639618](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40821639618) は両方成功。偽のWIN/LOSS証人と不正番号を拒否する試験も通過。初回探索は127終局局面・25,114再帰状態、証明書の独立再検査は36終局局面・10,692再帰状態。WIN9からの8石親9類、LOSS9親閉包80類、WIN/LOSS衝突0件。

上位WIN8への反映は `lift.js` で証明書と旧来のWIN8集合を再構成して検査する。伝播結果が固定されるまで新しいWIN8数・未証明辺数を計上しない。二石root閉鎖0、空盤は**UNKNOWN**。
