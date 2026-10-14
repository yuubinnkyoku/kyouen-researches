# 11×11 S8 LOSS の独立終局検査（2026-10-14）

標準 q=4・完全指摘・通常プレイ・元先手固定視点。11×11空盤勝敗は **UNKNOWN**。

## 範囲と出典

配布物 `n11-lane14-20261014.zip`（SHA-256 `ec08806a42813d98923147569ea68203973ee64299d5e815ad878a6b74fb8db4`）に含まれる8件のS8 LOSS証明書のうち、まず一件をGit管理する。別実装による終局検査を通し、単なるsolver/cache verdictから独立した検証可能な証拠を残す。元の8件の検査は配布物 `n11-lane15-independent-verifier-20261014.zip` にあるが、リポジトリに存在するファイルだけを検査可能な範囲として扱う。

## 検査

```sh
python research/experiments/n11-s8-independent-terminal-20261014/verify_s8_independent.py research/experiments/n11-s8-independent-terminal-20261014/certs/*.cert
python research/experiments/n11-s8-independent-terminal-20261014/test_verifier.py
python -O research/experiments/n11-s8-independent-terminal-20261014/test_verifier.py
```

検査器はPython標準ライブラリのみ。共円性は整数連立方程式で判定し、10石局面から終局までをキャッシュ非依存で再帰計算する。各S8の全合法S9子を網羅し、それぞれに合法なS10 LOSS証人を要求する。出力の`total_states`は各証人の終局再帰状態数の和で、相異なる局面数や計算量の下界ではない。

配布物8件の独立再検査では236本のS9遷移と終局再帰累計141,949状態を確認した。ただしこのリポジトリの検査済み範囲は、収載した証明書だけである。これは新たな二石rootの閉鎖でも、条件付き987候補全体の検証でもない。
