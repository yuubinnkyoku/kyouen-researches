# 11盤S5→S6商・訂正済みパイロット・安全局面の子同値定理

基準main: `befb0a916a0e98fa7dc50d708f43814ed4c4e99b`。
入力の完全SHA256は各censusと検査receiptに保存する。
旧log `2026-10-13-n11-pilot-s5-s6-symmetry.md` の26件は極性訂正前の入力であり、
この実験は現在のcheapest10＋polarity_conflicts29件を再計算したもの。
歴史的logを現在の39件の証拠として読み替えない。

- 一般証明：[proof.md](proof.md)。4石以上の安全な親では、子D4同値は親安定化群の着手軌道と一致する。3石反例あり。
- 共同計画の全31,546親：3,191,228合法辺→3,169,651親内正準子incidence→1,564,737相異なるS6。
- 現行39候補：3,273合法辺→2,363親内正準子incidence→2,269相異なるS6。
- 最小義務数17の558600と衝突候補20の209644を冷たい独立root探索でprobe。
  1M nodeでは双方UNKNOWN。10M上限ではそれぞれ1,269,467 nodeで元先手LOSS、
  1,684,694 nodeで元先手WIN。後者は旧LOSS共同計画の要求と逆向き。

censusは未知勝敗を仮定せず、探索もしない。
合法辺数と相異なる子数は厳密だが、LOSS証明は存在子で足りるため、
全和集合を求解することが必須とも、実行時間がこの割合で減るとも主張しない。
WIN側とLOSS側の衝突候補の「共有」は同じ局面を逆の要求で参照するという意味であり、
証拠の両用ではない。

## 再現

repo rootから（環境のツール有効化後）：

```sh
python3 research/experiments/n11-s5-s6-quotient-20261013/scripts/census.py
python3 research/experiments/n11-s5-s6-quotient-20261013/scripts/census.py --scope joint --output research/experiments/n11-s5-s6-quotient-20261013/output/joint.json.gz
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic research/experiments/n11-s5-s6-quotient-20261013/scripts/verify.cpp -o build/n11-s5-s6-quotient-verify
python3 research/experiments/n11-s5-s6-quotient-20261013/scripts/verify.py research/experiments/n11-s5-s6-quotient-20261013/output/pilots.json --binary build/n11-s5-s6-quotient-verify --output /tmp/n11-pilots-check.json
python3 research/experiments/n11-s5-s6-quotient-20261013/scripts/verify.py research/experiments/n11-s5-s6-quotient-20261013/output/joint.json.gz --binary build/n11-s5-s6-quotient-verify --output /tmp/n11-joint-check.json
python3 research/experiments/n11-s5-s6-quotient-20261013/scripts/small_board_audit.py
```

C++はPython Boardを使わず、平行移動3×3行列式で三点曲線の全格子点を生成し、
全親の安全性・合法数・安定化群位数・Burnside数・正準子数、
全親の子和集合と親数分布を独立に照合する。
改変した合法手数が拒否されることも確認する。

実探索は勝敗の追加証拠を必要とする場合だけ実行する。
既存raw/proofを上書きしないようprefixを新しく指定する。

```sh
g++ -std=c++20 -O2 cpp/solvers/kyouen_dfpn_root.cpp -o build/kyouen-dfpn-root
python3 research/experiments/n11-s5-s6-quotient-20261013/scripts/probe_pilots.py --solver build/kyouen-dfpn-root --budget 10000000 --prefix reproduction
```

1M probe出力のlegal欄は初回入力に0を入れたためmetadataが0になっている。
solverはoccupied maskから合法手を再構成しており、UNKNOWN結果はこれによって変わらない。
訂正済み入力と10M probeはlegal=68/80を記録し、runnerが幾何censusと照合する。
探索1回のnode数と秒は測定結果で、他の局面・予算への外挿はしない。

## 独立終局証明と計画修復（完了）

2局面の証明DAGを保存し、独立検査器が全局所条件と幾何終局を検査した。
5石局面の手番は**元後手**であり、勝敗表記は元先手固定である。

| S5 | 元先手結果 | proof節点 | proof辺 | 終局 | trusted葉 |
|---|---|---:|---:|---:|---:|
| 558600: {40,48,60,72,80} | LOSS | 270,545 | 426,376 | 28,813 | 0 |
| 209644: {49,55,60,65,71} | WIN | 349,157 | 518,252 | 50,131 | 0 |

生nativeトレース（192/265MiB）はignored `build/n11-proof-traces/` に移した。
正準の共有終局DAGはgzipで7.7/9.5MiB、trace/certificateのSHA256はreceiptに保存。
具体DAGをLean内で形式検査したという意味ではない。

```sh
python3 research/experiments/n11-proof-dag-engine-20261011/scripts/verify_saved.py research/experiments/n11-s5-s6-quotient-20261013/output/pilot-558600-terminal-dag.json.gz --out /tmp/pilot-558600-check.json
python3 research/experiments/n11-proof-dag-engine-20261011/scripts/verify_saved.py research/experiments/n11-s5-s6-quotient-20261013/output/pilot-209644-terminal-dag.json.gz --out /tmp/pilot-209644-check.json
# trace再変換時は --trace-dir build/n11-proof-traces を指定できる。
python3 research/experiments/n11-s5-s6-quotient-20261013/scripts/repair_plan.py
python3 research/experiments/n11-s5-s6-quotient-20261013/scripts/updated_dual.py
python3 research/experiments/n11-s5-s6-quotient-20261013/scripts/updated_dual.py --verify research/experiments/n11-s5-s6-quotient-20261013/output/updated-element-dual.json
```

WIN子を持つS4クラス5687/5690を旧共同LOSS計画から排除し、5選択を差し替えた。
修復後は19 root・全2,261 third手・無料122手・349選択S4を幾何から再検算し、
既知WIN子なし、全要求境界一致、未確定要求31,636を確認した。
旧31,546計画の原ファイルは変更せず、現行計画を別outputに保存している。
旧solver-trusted葉は引き続きその境界のままで、19 rootの終局証明ではない。

現行インスタンスのelement-only双対を全選択肢について厳密Fractionで評価した。
869有料群・95,225選択肢不等式が通過し、総和91145221/13860から整数下界6,577。
従って現在の楽観的選択問題は `6,577 ≤ OPT ≤ 31,636`。
この境界と勝敗の確定を混同せず、11×11空盤はUNKNOWNを維持する。
