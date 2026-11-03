---
id: K0663
title: 11×11の47終局LOSS7から七石LOSS251類を導き既存23類と合わせ274類を確保
kind: proposition
status: proved
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 完全指摘・通常プレイと合法な一点追加
- type: depends_on
  target: K0003
  note: 局所終局証明と空盤弱解決の区別
- type: depends_on
  target: K0661
  note: 53七石子の独立終局検証と47元先手LOSS7
- type: depends_on
  target: K0644
  note: 既存五根からの23元先手LOSS7の親持ち上げ
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/verify_2096_focus_53_terminal_classes.py
  role: verifier
  note: 53終局戦略の固定総合SHAと4×4整数Bareiss全応手監査、47勝ち初手後の八石と376復帰辺、既存23類との非重複を検査
- path: research/experiments/n11-central-19-cover-20261031/terminal_loss7_parent_lift_274_manifest.json
  role: data
  note: 47根由来251類、K0644由来23類、和集合274類の正準鍵。単体では証明書でなく独立再生検証器との一致が必要
- path: .github/workflows/n11-central49-2096-focus-53-terminal.yml
  role: source
  note: 53戦略と親持ち上げ・固定一覧の独立再生CI
- path: research/log/2026-11-03-n11-47-loss7-parent-lift-274.md
  role: log
  note: 導出、既存証明との交差、条件付き被覆の再計画に向けた境界
scope: 標準11×11・完全指摘・通常プレイ。K0661の元先手LOSS7の47根で元後手の証明済み勝ち初手により到達する八石34正準類と、それらの全合法七石親。K0644の既存23類との和集合。六石LOSS・二石root・空盤勝敗は対象外。
evidence: K0661の53終局戦略を固定総合SHA-256 034bb4b162d67afa559bad0bbe7cff339c120eb35af0a6ff21e2ee914f5f9bd6で再生成し、独立4×4整数Bareissで全応手と終局を検査。47元先手LOSS7の勝ち初手後は元先手番LOSS8であり、八石から一点を除く376本の七石親の復帰手を独立整数幾何で全検査。八石34正準類、七石親251正準類（元の47類を含み新規204類）。K0644の既存五根と固定勝ち初手から再構成した23類とは交差0。両系列の合計274類で、従来の70類から204類増加。CI 41550344718で47根の親持ち上げと全53終局戦略の再生成功。CI 41550890999で固定274類一覧の完全一致・K0644の23類との交差0・全53終局証明の再生に成功。二石root・空盤はUNKNOWN。
---

# 47個の終局LOSS7から251類へ

K0661で独立検証された53個の七石局面のうち、47個は元先手LOSS7であり、七石時点で手番側の元後手が勝つ。各証明書が選ぶ最初の合法手で八石局面へ進むと、元先手の手番で元先手LOSSとなる。

この八石から任意の一点を除いた安全な七石局面では、元後手がその点に戻せば、同じ証明済み八石へ到達できる。従って、その七石局面も元先手LOSSである。これは未完探索の勝敗推定ではなく、終局まで検証済みの戦略を再利用する一手帰納である。

| 量 | 独立監査結果 |
| --- | ---: |
| 元の終局証明済みLOSS7 | 47類 |
| 最初の一手後のLOSS8 | 34正準類 |
| 八石から七石への合法復帰辺 | 376本 |
| 導出したLOSS7 | **251正準類** |
| 元の47類からの増分 | **204類** |
| K0644由来の既存23類との交差 | **0類** |
| 両系列の終局証明由来LOSS7 | **274類** |

47根の戦略生成器は3×3差分整数行列式を使うが、検証器は別の4×4整数Bareissで全合法応手・終局・376復帰辺を再計算する。生成器の勝敗表示や未完の探索表は証拠に採用しない。さらにK0644の五根・固定初手から23類を再構成して集合の交差0を検査する。

正準鍵の一覧は `terminal_loss7_parent_lift_274_manifest.json` に保存し、独立再生の結果と**集合全体の一致**を要求する。一覧だけを根拠に勝敗を確定してはならない。

これら274類は二つの終局証明系列からの和集合であり、全リポジトリのあらゆる既知LOSS7を網羅したという主張ではない。失効した2,096類の六石LOSS証人計画は復活しない。新しい被覆計画では既知WIN6の183類・WIN7の少なくとも29類を除外し、この274類を安全に再利用できる。

**新規六石LOSSは未証明。二石局面{49,60}と標準11×11空盤の勝敗はUNKNOWN。**
