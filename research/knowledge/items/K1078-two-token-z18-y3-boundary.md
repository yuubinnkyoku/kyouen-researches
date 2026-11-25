---
id: K1078
title: 2トークン残余ゲーム z=18・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: []
relations:
  - type: depends_on
    target: K0832
    note: 残余ゲームHの定義、A/B/C再帰、単一トークン閉形式と一般tail定理を使用する
  - type: depends_on
    target: K1051
    note: B子 H(R-1;(x,2);18) の全x閉形式を使用する
  - type: depends_on
    target: K1067
    note: C子 1 xor H(R-1;(x,3);17) の全x閉形式を使用する
artifacts:
  - path: research/experiments/vertical-fiber-two-token-z18-y3-boundary-20261120/report.md
    role: proof
    note: 全称定理、Grundy値0/1/2の閉形式、R強帰納と完全署名帯表
  - path: research/experiments/vertical-fiber-two-token-z18-y3-boundary-20261120/verify_z18_y3.py
    role: verifier
    note: 二直接再帰、子アンカー、署名帯、低R縮約、tailの独立監査
  - path: research/experiments/vertical-fiber-two-token-z18-y3-boundary-20261120/output/audit.json
    role: data
    note: 6,877,653照合の決定的監査結果
  - path: research/log/2026-11-20-two-token-z18-y3-boundary.md
    role: log
    note: 着手時の既存成果確認、発見、証明判断、未実施検査と次候補
scope: z=18、二トークン(x,3)、x>=3、R>=0
evidence: R強帰納法と全Rを覆う偶奇別署名帯表。K1051とK1067を子アンカーに使う。有限監査は独立照合であり、全称性の根拠は記号的証明。
---
全ての \(x\ge3,R\ge0\) に対し \(H(R;(x,3);18)\) のGrundy値0/1/2を完全分類する。値2の定常pinは25、値1の基底点は \(x\ge20\) で \(\{19,21,23\}=\{z+1,z+3,z+5\}\) のちょうど3点。\(x=22\) は掃引行で、値2が \(O[25,43]\) に広がり、\(x\ge23\) で一点25に戻る。

さらに \(R\le21=z+3\) では単一トークン \(x+3\) への縮約が全称成立し、この一様境界は \(x=16,R=22\) の反例で鋭い。tailは \(R\ge x+22\) で \((x+3)\bmod2\)。

完全な値集合・署名帯表・mex証明は[証明報告](../../experiments/vertical-fiber-two-token-z18-y3-boundary-20261120/report.md)、独立検証器は[verify_z18_y3.py](../../experiments/vertical-fiber-two-token-z18-y3-boundary-20261120/verify_z18_y3.py)、監査結果は[audit.json](../../experiments/vertical-fiber-two-token-z18-y3-boundary-20261120/output/audit.json)。
