# N11 第19回: 固定12候補の終局証明

入力は `../n11-s9-post-round18-replan-20261029/next-plan.json`（12候補、合法10石子329本・329類、SHA-256 `564a47bb41339d9fb665536faccd697ed7ce7fac6ec83b3ccbe5e616f3dace2c`）。

- `prove.js`: この12局面に限定した終局探索。WIN9には全合法10石子、LOSS9には合法なLOSS10証人を要求する。初回探索結果を `certificate.json` に固定。
- `verify_compact.js`: 証明書を再読込し、独立整数幾何で全WIN子とLOSS証人を再帰検査する。偽のWIN/LOSS証人と不正な番号を拒否する。
- `verify_python.py`: Nodeや共有solverに依存せず、4×4整数行列式と終局再帰を独立実装。66個の必要な終局局面を再検証。
- `lift.js`: 既存の証明限定8石WINを再構成し、新たなWIN9からの親伝播を検査する。固定結果は成功した実行後の `lift.json` に置く。

[探索CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40810196930)、[独立Node検証CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40810302248)、[独立Python検証CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40810437527) は成功。結果は **2 WIN9 / 10 LOSS9**、LOSS9親閉包100類。初回探索の121終局局面、Python独立検証の66終局局面を混同しない。

8石への伝播は独立に固定されるまで未加算。二石rootの新規閉鎖は0、11×11空盤の勝敗は**UNKNOWN**。
