---
id: K0461
title: 異方格子の水平間隔に余分な奇素因子があれば円は幅以下の点しか持たない
kind: proposition
status: needs-review
topics:
- geometry
- rectangles
- variants
- grundy
aliases: []
relations:
- type: depends_on
  target: K0001
  note: q点禁止と安全局面の定義
artifacts:
- path: research/experiments/fixed-width/reports/prime-spacing-row-sparsity-20261016.md
  role: proof
  note: 奇素数の二段階剰余制限による全称証明
- path: research/experiments/fixed-width/scripts/verify_prime_spacing_20261016.py
  role: verifier
  note: 56有限盤の独立整数円生成と行剰余監査
solution:
  board: 異方格子のw×m・q点版
  level: strong
  outcome: conditional
  classification:
  - root
  - first-moves
  - all-safe-win-loss
  - all-safe-grundy
  coverage: 全m≥1・全安全局面
  conditions: w≥4、q≥w+1、ある奇素数pでv_p(h)>v_p(d)
  verification:
  - mathematical-proof
  - independent-enumeration
  certificate: 二点行の中心整数性と法p²への単根持上げによる全称証明
  independent_check: 非共線三点から円を整数係数で独立生成した56有限盤
  note: g(S)=(w min(m,q-1)-|S|) mod2、M=q-1
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 異方格子の奇素数間隔による全長強解決

水平間隔h、垂直間隔dの格子について、ある奇素数pでv_p(h)>v_p(d)なら、連続w≥4行の無限格子上の任意の円は高々w格子点しか持たない。

証明：円が二点を持つ行があると横中心は格子間隔の半整数倍となる。円上の行番号iはp進二次式f(i)=i²+ai+b≡0(mod p²)を満たす。占有行は法pで一剰余類に限られるか、異なる二根が単根なので法p²で高々二剰余類に限られる。いずれもw≥4では占有行数がw/2以下となる。各行高々2点なので円上点数はw以下。二点行がなければ自明にw以下。

従ってq≥w+1では行間の禁止集合がなく、全m≥1でg(S)=(w min(m,q-1)-|S|) mod2、真の満容量安定化長M=q-1。詳しい補間と整数性の扱い、有限監査の範囲は証明記録を参照。

限界：h=dの標準格子や全奇素数でv_p(h)≤v_p(d)の場合には適用できない。有限監査を全称証明と混同しない。
