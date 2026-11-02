---
id: K0628
title: 11×11の二つ目の共有七石終局戦略から六石七類を証明し2,097類計画を反証
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
  note: 六石局所証明と空盤弱解決の区別
- type: depends_on
  target: K0627
  note: 一つの終局WIN7戦略を七つの六石親に持ち上げる方法
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/terminal_s6_60_strategy.b64
  role: certificate
  note: 二つ目の終局戦略14,440バイトをzlib/base64圧縮、復号SHA-256 debb5464282eb28e6a30496f8728515433d6f9507ffdeeda1eeaf04e3c5d7de4
- path: research/experiments/n11-central-19-cover-20261031/verify_terminal_s6_60_compact.py
  role: verifier
  note: 4×4整数行列式による全相手応手・終局の独立検証
- path: research/experiments/n11-central-19-cover-20261031/terminal_s7_second_seven_s6_parents.json
  role: manifest
  note: 二つ目の共有七石から一点を除いた七つの六石正準類
- path: research/experiments/n11-central-19-cover-20261031/verify_terminal_s7_second_seven_win6.py
  role: verifier
  note: 七親の全終局再生と既存WIN6との重複排除
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_2097_refuted_by_second_s7.json
  role: manifest
  note: 旧2,097類計画の六石証人二類が元先手WINと判明、再計画必須
- path: research/experiments/n11-central-19-cover-20261031/verify_second_s7_refutes_2097.py
  role: verifier
  note: 旧46証人と七親の交差を独立4×4整数幾何で検査
- path: research/log/2026-11-02-n11-central49-second-terminal-win7-seven-win6-refutes-2097.md
  role: log
  note: 終局戦略・七親・条件付き被覆反証の研究記録
scope: 標準11×11完全指摘・通常プレイ。共有七石00000000000200821002008000800000から一点を除いた七つの相異なるD4正準六石局面の元先手視点。空盤・二石rootの勝敗は対象外。
evidence: 固定終局戦略を独立4×4整数行列式で各六石親22,364到達局面・2,942終局まで再生し、元先手敗北終局0。ローカル独立C++・Python検査済み、専用CIの完了は別途確認。
---

# 二つ目の共有七石終局戦略から七つの六石WIN

六石 `00000000000000203808000000000020` で点107に着手すると、共有七石 `00000000000200821002008000800000`（D4正準）へ進める。元先手の必勝戦略を14,440バイトの固定証明書として構成し、探索器とは別の4×4整数行列式で全相手応手・終局を再計算した。到達22,364局面、終局2,942局面、元先手敗北終局0。

七石から一点を取り除いた六石親はD4正準化後もすべて異なる。

| 六石正準鍵 | 除去点（共有七石の元の向き） |
| --- | ---: |
| `00000000000000203808000000000020` | 107 |
| `00000000000000203808000000002000` | 5 |
| `00000000000000801082002080000000` | 69 |
| `00000000000200021002008000800000` | 59 |
| `00000000000200820002008000800000` | 60 |
| `00000000000200821000008000800000` | 61 |
| `00000000000200821002000000800000` | 51 |

各親では取り除いた点へ合法に置き、同じ七石の終局戦略を使える。既存117類・K0624の七類・K0627の七類との重複はない。**この項目の新規元先手WIN6は七類**。

ただし、七親のうち二類（`00000000000000203808000000000020` と `00000000000000203808000000002000`）が、K0626/K0627で修復した条件付き46六石証人に含まれている。よって**2,097七石類の条件付きLOSS証明計画は失効**した。修復用の幾何的被覆が成立することと、六石証人がLOSSであることは別である。

新しい有効な六石LOSS被覆は未構成。六石LOSS・四石LOSS・二石root閉鎖は新規0件。**標準11×11空盤の勝敗はUNKNOWN**。
