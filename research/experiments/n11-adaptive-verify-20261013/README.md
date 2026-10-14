# n11 adaptive verify: next10m solver-trusted 2件の独立終局検証

対象: `n11-conflict-closure-20261013/output/next10m-manifest.json` の rows のうち
solver-trusted止まりだった2件。

| S5 index | raw label (solver) | 独立証明 (terminal-only) |
|---|---|---|
| 126899 | SOLVED verdict=2 (元先手 LOSS, K0371極性) | receipt verdict=2, trusted_leaves=0 |
| 144095 | SOLVED verdict=1 (元先手 WIN) | receipt verdict=1, trusted_leaves=0 |

信頼区分: rawはsolverのcompleted labelでありsolver-trustedのまま。
証拠への昇格は `check_trace` の terminal-only receipt (trusted_leaves=0,
pruned roundtrip, 全件再生成) が成功した場合のみ。UNKNOWNは昇格しない。

手法は `n11-native-terminal-checker-20261013` の focus検証済み3件
(115540 / 144193 / 144311) と同一: checker source はバイト同一
(SHA256 `0f890cb4…`), 同一の root/verdict/trace SHA256 実装結合,
pruned roundtrip, trusted_leaves=0 強制。

## 再現 (repo root, WSL Linux Python)

```sh
g++ -O3 -std=c++20 -DNDEBUG cpp/solvers/kyouen_dfpn_root.cpp -o build/kyouen-dfpn-root-adaptive
python3 research/experiments/n11-adaptive-verify-20261013/scripts/probe_next10m.py --solver build/kyouen-dfpn-root-adaptive
g++ -O3 -std=c++20 -DNDEBUG research/experiments/n11-adaptive-verify-20261013/scripts/check_trace.cpp -o research/experiments/n11-adaptive-verify-20261013/output/check_trace -lz
python3 research/experiments/n11-adaptive-verify-20261013/scripts/test_checker.py
python3 research/experiments/n11-adaptive-verify-20261013/scripts/verify_terminal.py 126899 --manifest research/experiments/n11-conflict-closure-20261013/output/next10m-manifest.json --probe-manifest research/experiments/n11-adaptive-verify-20261013/output/adaptive10m-manifest.json --trace build/n11-adaptive-native-traces/adaptive10m-126899.csv --checker research/experiments/n11-adaptive-verify-20261013/output/check_trace
python3 research/experiments/n11-adaptive-verify-20261013/scripts/verify_terminal.py 144095 --manifest research/experiments/n11-conflict-closure-20261013/output/next10m-manifest.json --probe-manifest research/experiments/n11-adaptive-verify-20261013/output/adaptive10m-manifest.json --trace build/n11-adaptive-native-traces/adaptive10m-144095.csv --checker research/experiments/n11-adaptive-verify-20261013/output/check_trace
python3 research/experiments/n11-adaptive-verify-20261013/scripts/compare_dag.py 126899 --rerun-python
python3 research/experiments/n11-adaptive-verify-20261013/scripts/compare_dag.py 144095 --rerun-python
```

再生成trace (`build/n11-adaptive-native-traces/`, 使い捨て) は
frozen next10m-manifest の trace_sha256 とバイト一致
(126899: `1597e9c7…`, 144095: `4f68c579…`) し、探索節点数も
3,184,967 / 4,152,553 で raw run と一致した。
既存の next10m/focus/pilot 成果物は上書きしていない。
具体DAGのLean内形式検査を意味しない。
