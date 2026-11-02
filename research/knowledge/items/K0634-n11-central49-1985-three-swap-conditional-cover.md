---
id: K0634
title: 11×11中央49の条件付き六石被覆は七石1,985類、固定集合からの三証人交換では改善不能
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共円禁止と合法手の定義
- type: depends_on
  target: K0003
  note: 条件付き証明計画と勝敗証明の区別
- type: depends_on
  target: K0023
  note: 11×11空盤勝敗は未確定
- type: depends_on
  target: K0624
  note: 終局証明済み六石WINを除外する根拠
- type: depends_on
  target: K0626
  note: 第一の六石終局WIN証明
- type: depends_on
  target: K0628
  note: 第二の六石終局WIN証明
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_three_swap_chain.json
  role: certificate
  note: 三段階の六石証人交換、各段階の七石辺数・類数、選択集合のSHA-256
- path: research/experiments/n11-central-19-cover-20261031/audit_central49_2092_three_swap.py
  role: verifier
  note: 3×3整数差分行列式と六頂点完全マッチングによる三証人交換全数監査
- path: research/experiments/n11-central-19-cover-20261031/search_central49_1994_three_swap_descent.py
  role: solver
  note: 有限の全数探索を繰り返し1,985類まで縮小、局所改善不能を確認
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_three_swap_chain.py
  role: verifier
  note: 別方式の4×4整数Bareissによる三段階の幾何・被覆・既知WIN非衝突の独立再計算
- path: research/log/2026-11-02-n11-central49-three-swaps-1985-exact-neighborhood.md
  role: log
  note: 探索経過、件数、信頼境界、独立CI
scope: 標準11×11・二石{49,60}・中央49の優先四石から得る94五石正準類を46六石証人で被覆する条件付きLOSS計画。固定した最終46証人のちょうど三証人交換近傍。
evidence: 2,092→2,049→1,994→1,985の3回の交換を3×3整数幾何で発見し、4×4整数Bareissで独立再計算。最終局面の三証人交換153,183有効候補に改善0件。専用CI 41416165633と41415515661で成功。
---

# 中央49の条件付き六石証人から生じる七石義務は1,985類

11×11の二石局面 `{49,60}` の証明計画で、優先四石から生じる94五石正準類を46六石証人で完全被覆する幾何学的な条件付き構成を改良した。七石子の相異なる正準類数は**2,092→2,049→1,994→1,985類**、計107類（5.11%）減少。合法な六石→七石辺は最終2,989本で、既知WIN6・WIN7との衝突は0件だった。

例外2類を除く92五石頂点の完全マッチング構造を利用し、除去する六石証人3類が開放する6頂点の全15再組合せを検査した。固定した最終46証人からの**ちょうど三証人交換**については、除去三組15,180通り、再組合せ227,700通り、非自明交換166,377件、有効153,183件を全数検査し、改善0件・同数4件。したがってこの近傍では最小だが、全46証人の大域最適性は未証明である。一・二証人交換の最適性もこの結果だけからは導けない。

独立検証器は探索器と異なる4×4整数行列式で全合法七石子を再計算し、D4正準化、五石94/94被覆、三段階の辺数・類数、最終選択集合のSHA-256 `f72c587537cbe2239b0f077545dfd14628298d2fe6d7c6b80ac7345ff46b6026` を確認した。独立CI [41416165633](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/41416165633) は成功。

**1,985は未証明の条件付き七石証明義務の数であって、確定勝敗数ではない。** 選択六石LOSS・四石LOSS・二石root閉鎖はいずれも新規0件。標準11×11空盤の勝敗は**UNKNOWN**。
