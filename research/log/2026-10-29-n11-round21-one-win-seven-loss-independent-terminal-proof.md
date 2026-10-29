# 2026-10-29: N11第21回の9石1 WIN / 7 LOSSを独立終局検証

第20回後の固定再計画で選んだ9石8類を対象とする限定終局探索 [CI 40834910872](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40834910872) が2026-10-29 07:22 UTCに成功した。成果物 `n11-round21-discovery`（ID 12880232996、ZIP digest `sha256:3f075a75855edd7bb70f30722648622d6bb3e9387a80bcf8cd7366ccb3e66dde`）を回収し、`research/experiments/n11-s9-post-round20-round21-20261029/certificate.json` に固定した。証人SHA-256は `687e1f0b4168ade29960a354679c89bf8aa3e557ac44068a92bfb45faa66724c`。

探索初回 [CI 40834794955](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40834794955) は、8候補に対し `new Set(keys).size===9` という移植時の誤った検査条件で即時失敗した。これは勝敗計算に入る前の実装上の失敗であり、[修正 e451866a](https://github.com/yuubinnkyoku/kyouen-researches/commit/e451866a57eb8fc0411604ef76a530765c030591) 後の限定探索が成功した。

独立Node・Python検証 [CI 40835119813](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40835119813) は両方**成功**。共有Node探索cacheを使わないPythonの独立した整数幾何・終局再帰を含み、Node側は偽WIN/LOSS証人と範囲外番号の拒否も検査する。

- **9石WIN 1類 / LOSS 7類**。WIN9の全合法10石子28本はWIN、LOSS9は各1つの合法LOSS10証人を持つ。
- 選定8類の合法10石着手226本・226類（独立事前照合 [CI 40834731332](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40834731332) 成功）。
- 初回探索の終局10石局面89類、再帰状態22,672（各独立幾何）。LOSS10証人からのLOSS9親閉包70類。WIN9/LOSS9衝突なし。
- 新規8石WIN純増数、固定14根計画の未証明辺減少は、[独立伝播計算](https://github.com/yuubinnkyoku/kyouen-researches/tree/main/research/experiments/n11-s9-post-round20-round21-20261029) を検証して固定するまで未確定。

この証明は8つの9石局面についてのみ有効で、二石rootの新規閉鎖は0件。現時点の確定8石WINは5,827類、固定14根の未証明辺は41本。**標準11×11空盤の勝敗はUNKNOWN。**
