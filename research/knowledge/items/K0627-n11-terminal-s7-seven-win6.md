---
id: K0627
title: 11×11の新規共有七石終局戦略から七類の六石元先手WINを証明
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
  note: 局所WIN証明と空盤勝敗の区別
- type: depends_on
  target: K0626
  note: 固定終局戦略の証明書と独立検証
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/terminal_s6_55_strategy.b64
  role: certificate
  note: 七石へ着手した後の全終局戦略を含む固定証明書、復号SHA-256 83bdd3c89555bd80eadae802d47a8dc8289f0aee1a935440fb325f7f9ce25b2b
- path: research/experiments/n11-central-19-cover-20261031/terminal_s7_seven_s6_parents.json
  role: manifest
  note: 七石から一点除去した七つの六石親とD4正準鍵
- path: research/experiments/n11-central-19-cover-20261031/verify_terminal_s7_seven_win6.py
  role: verifier
  note: 七つの六石親で4×4整数行列式による全相手応手・終局の独立再生
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_after_terminal_s6_55_repair_2097.json
  role: manifest
  note: 確定WIN6を除外した66組の固定44条件付き修復から得た2,097七石類
- path: research/experiments/n11-central-19-cover-20261031/verify_terminal_s6_55_repair_2097.py
  role: verifier
  note: 幾何的二対二修復68組のうち確定WIN6で2組を反証し66組を独立監査
- path: research/log/2026-11-02-n11-central49-seven-win6-66-repair.md
  role: log
  note: 七親の終局証明・修復計画の証明境界
scope: 標準11×11完全指摘・通常プレイ。共有七石00000000000200801002080081000000から一点を除いた七つの相異なるD4正準六石局面の元先手視点。二石root・空盤は対象外。
evidence: 固定終局戦略の独立4×4整数行列式による七親の全相手応手再生。各親18,649到達局面、2,554終局、元先手敗北終局0。ローカルで七親すべて検査済み。専用CIの完了は別途確認。
---

# 共有七石から七つの六石元先手WINを証明

共有七石 `00000000000200801002080081000000` で元先手が勝つことはK0626の固定終局戦略により証明できる。七石を構成する7点のうちどの一点を除いても、その点へ合法に着手すれば同じ七石戦略に合流する。

| 六石正準鍵 | 除去点（共有七石の向き） |
| --- | ---: |
| `00000000000000203800000000080080` | 24 |
| `00000000000000801002000240800000` | 81 |
| `00000000000200001002080081000000` | 71 |
| `00000000000200800002080081000000` | 60 |
| `00000000000200801000080081000000` | 49 |
| `00000000000200801002000081000000` | 43 |
| `00000000000200801002080001000000` | 31 |

七類はD4で同一視しても相異なり、既存117類の比較用WIN6・K0624の七類・旧独立WIN6一類とは重複しない。**K0626の一類を含めて七類の新規WIN6**であり、この項目で新たに加わるのは六類。

独立検証器は七つの親をそれぞれ元先手手番として開始し、4×4整数行列式によって相手の全合法応手を展開する。各親について18,649局面・2,554終局、元先手敗北終局0。過去の勝敗cacheには依存しない。

この七類の確定WIN6を除外すると、K0626の条件付き二対二修復68組のうち2組が失効し、当時の残り66組の最小七石証明対象は2,097類となった。しかし、後続の[K0628](K0628-n11-second-terminal-s7-seven-win6-refutes-2097.md)が選択六石二類を新たにWINと証明したため、**この2,097類計画も失効した**。現在の有効な条件付き六石LOSS被覆は再構築が必要である。**選択六石のLOSSは依然として未証明**であり、四石LOSS・二石root・空盤勝敗は導かれない。

**標準11×11空盤の勝敗はUNKNOWN。**
