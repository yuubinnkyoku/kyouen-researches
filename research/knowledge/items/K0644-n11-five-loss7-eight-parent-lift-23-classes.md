---
id: K0644
title: 11×11の五つの終局LOSS7証明から七石LOSS23類を帰納し現行義務6類を確定
kind: proposition
status: proved
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 合法な一点追加と通常プレイの終局規則
- type: depends_on
  target: K0003
  note: 局所勝敗と11×11空盤弱解決の区別
- type: depends_on
  target: K0637
  note: 五つの固定七石必勝戦略と独立終局検証
- type: depends_on
  target: K0641
  note: 現行46六石証人・2,301七石条件付き証明義務
- type: depends_on
  target: K0642
  note: 既存五根と現行被覆の交差4類
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/verify_five_loss7_eight_parent_lift.py
  role: verifier
  note: 五終局戦略の独立再検証、初手後八石の全七親と現行46証人の4×4整数幾何監査
- path: research/experiments/n11-central-19-cover-20261031/verify_five_terminal_loss7.py
  role: verifier
  note: 五つの固定戦略のSHA-256・全応手・終局の独立検査
- path: .github/workflows/n11-central49-five-loss7-terminal.yml
  role: source
  note: 証明書再生成と七親持ち上げ、CI 41461559484成功
- path: research/log/2026-11-02-n11-five-loss7-eight-parent-lift-23-and-six-current.md
  role: log
  note: 初手後八石の重複構造、23七親と現行被覆の交差
scope: 標準11×11完全指摘・通常プレイ。K0637の五つの元先手LOSS7根から元後手の戦略初手で到達する八石の全七石親。現行K0641の2,301七石義務との交差。六石LOSS・二石root・空盤勝敗は対象外。
evidence: K0637の五つのSHA-256固定戦略を再生成し4×4整数Bareissで全合法応手・終局まで再検証。初手後八石は元先手番LOSSでD4正準3類。八石から一点除去した40七親辺を4×4整数幾何で全検査し23七石正準類（既知5・新規18）の元先手LOSSを構成的に導出。現行46六石証人・2,301七石義務を再監査して交差6類・6辺・3証人（既知4類に新規2類）を確認。CI 41461559484成功。
---

# 五つの終局戦略の初手後八石から七石LOSSを23類に拡張

K0637の五つの七石根は元後手の手番であり、固定終局戦略によって元後手WINと独立検証されている。各戦略の最初の一手で到達する八石では元先手の手番だが元先手LOSSである。八石から任意の一点を除いた七石親では、元後手がその点へ合法に戻せば同じ証明済み八石に到達する。したがって、その七石親も元先手LOSSである。

五つの戦略初手は115・76・114・49・65。初手後八石はD4正準で3類、40本の七石親辺は23正準類となる。元の五根を除く18類は新たな元先手LOSS7の帰結である。

現行K0641の46六石証人から生じる2,301七石義務との交差は6類・6辺・3証人。K0642の4類に加え、次の2類が新たに確定した。

| 新規元先手LOSS7正準鍵 | 現行六石証人正準鍵 |
| --- | --- |
| 0000000000000020380a000000000040 | 00000000000000203808000000000040 |
| 00000000000002043800800000000010 | 00000000000000203808000000000040 |

本証明系列で未被覆の現行七石義務は2,295類。ただし全既存証拠を統合したUNKNOWN数ではない。証明書はCI成果物に保存し、4×4整数Bareissで全応手・終局と40合法復帰手を独立検証した。

**六石LOSS・四石LOSS・二石rootの新規閉鎖はない。標準11×11空盤の勝敗はUNKNOWN。**
