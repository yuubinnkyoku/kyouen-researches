---
id: K0638
title: 11×11中央49の1,985七石条件付き計画は選択六石WINの終局証明で失効
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共円禁止と合法手の定義
- type: depends_on
  target: K0023
  note: 11×11空盤の勝敗は未確定
- type: depends_on
  target: K0634
  note: 失効する1,985七石条件付き計画と選択六石の同一性
- type: depends_on
  target: K0637
  note: 同じ旧計画内の別の七石LOSS終局証明は有効
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/generate_five_terminal_loss7.cpp
  role: solver
  note: 元先手WIN7極性でも戦略を決定的に生成できる整数3×3探索器
- path: research/experiments/n11-central-19-cover-20261031/verify_focus_s6_win_refutation.py
  role: verifier
  note: 元後手の全合法応手を別方式4×4整数Bareissで検査し六石の勝ち手を確認
- path: .github/workflows/n11-central49-five-loss7-terminal.yml
  role: source
  note: 五つのLOSS7と一つの反証WIN7を再生成・独立検証するCI
- path: research/log/2026-11-02-n11-central49-focus-s6-win-refutes-1985.md
  role: log
  note: 反証戦略の統計、SHA-256、旧証人計画への影響と再計画条件
scope: 標準11×11、中央49の二石{49,60}から導いた旧1,985七石条件付き計画で選択されていた六石局面 0000000000000020380a000000000000。元先手番のWIN6。
evidence: 六石で元先手が点44に置いた七石局面 0000000000000020380a100000000000 は元後手番のLOSS（元先手WIN7）。元先手の固定終局戦略7,182局面を別実装4×4整数Bareissで独立検証し、到達10,762局面・終局1,255局面で元先手敗北終局0。証明書SHA-256 072454b7a4c72ebf68095d0b90a6c7665a9cef521325435012ac2341a32b9635。旧計画のこの六石をLOSS証人として採用できない。
---

# 六石局面の確定WINが旧1,985類計画を反証

中央49の旧条件付き六石証人46類に含まれる局面

0000000000000020380a000000000000

は**元先手WIN6**である。元先手が点44（座標0,4）に置くと、七石

0000000000000020380a100000000000

へ移る。この七石では元後手の手番だが、**元後手LOSS（元先手WIN7）**を終局まで独立検証した。

証明書は元先手の番に7,182局面で合法な応手を指定し、元後手の番では全合法手を列挙する。到達生局面10,762、終局1,255、元先手が敗北する終局0、終局石数13〜17。探索器は3×3整数差分行列式、独立監査器は4×4整数Bareissを使用。証明書はSHA-256固定で、改変負例4件を拒否する。これは未完探索のpn/dnやsolver-trusted判定ではなく、固定戦略の終局までの検査である。

従って、**六石局面を元先手LOSSと仮定して五石LOSSを導く旧1,985類の計画は失効**。46六石証人による94/94五石の幾何被覆、七石1,985正準類という計数、および旧集合に関する最大三証人交換の局所最適性は、歴史的な幾何計算として残る。しかし、この六石が確定WINなので、46類を全てLOSSとして閉じることは不可能。少なくとも当該証人を交換し、既知WIN6・WIN7との衝突を再検査する必要がある。

K0637の旧集合内五つの七石LOSS証明自体は有効であり、削除しない。ただし旧計画の残り1,980類や集中六石の残り58類を、現行の有効なLOSS計画の義務として追跡してはならない。

**新規確定WIN6は1類。新規六石LOSS・四石LOSS・二石root閉鎖は0件。標準11×11空盤はUNKNOWN。**
