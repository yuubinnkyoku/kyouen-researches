---
id: K0624
title: 11×11の共有七石終局戦略から七つの六石元先手WINを独立証明
kind: proposition
status: proved
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 完全指摘・通常プレイの合法手と終局規則
- type: depends_on
  target: K0003
  note: 局面証明と空盤弱解決の区別
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/shared58_s6_win_strategy.cert
  role: certificate
  note: 共有七石へ進んだ後の全相手応手を含む元先手戦略、SHA-256 10e816538fbe6cc0062e2d0dd0fe96930ef294101812701305e1595b531b21da
- path: research/experiments/n11-central-19-cover-20261031/verify_shared_s7_seven_win6.py
  role: verifier
  note: D4変換で七六石親に戦略を移し、4×4整数行列式で全応手と終局を再検査
- path: research/experiments/n11-central-19-cover-20261031/verify_shared58_win6_repair_2089.py
  role: verifier
  note: 終局WIN6を除外した94五石被覆の二類置換と2,089七石類の独立監査
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_after_shared58_win6_repair_2089.json
  role: manifest
  note: 当時の固定44六石の条件付き修復被覆。後続K0626で選択六石のWINが終局証明され、LOSS証人計画として失効
- path: research/log/2026-11-02-n11-shared-terminal-s7-seven-certified-win6.md
  role: log
  note: 新規五六石WINの証明・独立CI成功・残る未解決事項
scope: 標準11×11の完全指摘・通常プレイ、七石00000000000000603808200000000000から一点を取り除いた七つの相異なるD4正準六石局面の元先手視点。二石root・空盤勝敗は対象外。
evidence: 固定終局戦略証明書のSHA-256照合と4×4整数Bareiss行列式による七つの六石局面それぞれの全合法応手・終局の独立再生。GitHub Actions 41370901856 成功。
---

# 一つの共有七石戦略から七つの六石WINを証明

七石局面 `00000000000000603808200000000000` は元先手WINと終局まで証明済みである。この七点のうち任意の一点を取り除いた六石局面では、その点へ合法に置いて同じ七石に戻せる。七つの六石親はD4対称性で同一視してもすべて異なるため、**七類の六石局面すべてが元先手WIN**。

| 六石正準鍵 | 勝ち手 | 証明の新旧 |
| --- | ---: | --- |
| `00000000000000083801800000000000` | 73 | 新規 |
| `00000000000000203808200000000000` | 70 | 既証明の再検査 |
| `0000000000000020380c000000000000` | 75 | 既証明の再検査 |
| `00000000000000403808200000000000` | 69 | 新規 |
| `00000000000000601808200000000000` | 61 | 新規 |
| `00000000000000602808200000000000` | 60 | 新規 |
| `00000000000000603008200000000000` | 59 | 新規 |

検証器は、探索器とは異なる4×4整数行列式で各親の全応手を再生成し、各局面について戦略10,881局面、全到達16,980局面、終局2,237局面を確認。元先手が敗北する終局は0件、終局石数は13〜17の奇数のみ。証明書は旧solverのWIN/LOSS cacheに依存しない。専用CIは成功（実行ID 41370901856）。

この七類は、既存19類の比較用WIN7から逆伝播された117類のWIN6と重複しない。前回終局証明済み二類を除いた**五類が新規の独立終局証明**である。

一方、二石 `{49,60}` の四石LOSS候補に使うための修復済み46六石被覆は、全94五石親を幾何学的に覆うだけであり、選択六石がLOSSであるとは証明していない。二類置換の幾何的な候補は三組だが、一組はこの共有七石WINに反するため失効。残る二組のうち最少の証明対象は相異なる七石2,089類である。後続の[K0626](K0626-n11-central49-terminal-s6-win55.md)により、この2,089類の条件付き被覆に含まれる別の六石局面も元先手WINと終局証明された。したがって、**この2,089類をLOSS証人として使う計画は失効**しており、現行の修復候補は2,097類（いずれもLOSS未証明）である。
\n**11×11空盤の勝敗はUNKNOWN**。
