---
id: K1083
title: 2トークン残余ゲーム z=18・y=4境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: []
relations:
  - type: depends_on
    target: K0832
    note: 残余ゲームHの再帰、単一トークン閉形式、一般tailを使用する
  - type: depends_on
    target: K1078
    note: B子 H(R-1;(x,3);18) の全x閉形式を使用する
  - type: depends_on
    target: K1076
    note: C子 1 xor H(R-1;(x,4);17) の全x閉形式を使用する
artifacts:
  - path: research/experiments/vertical-fiber-two-token-z18-y4-boundary-20261120/report.md
    role: proof
    note: 全x・全RのGrundy値0/1/2分類、偶奇別署名帯表、低R縮約の鋭い境界
  - path: research/experiments/vertical-fiber-two-token-z18-y4-boundary-20261120/verify_z18_y4.py
    role: verifier
    note: 一般多重集合再帰との子アンカー・親照合、署名帯、帰納閉包、低R、tail監査
  - path: research/experiments/vertical-fiber-two-token-z18-y4-boundary-20261120/output/audit.json
    role: data
    note: 1,415,309照合、不一致0、二回実行byte-identicalの有限監査
  - path: research/log/2026-11-20-two-token-z18-y4-single-owner.md
    role: log
    note: 単一オーナー宣言、着手時の既存成果確認、証明・監査・未実施事項
scope: z=18、二トークン(x,4)、x>=4、R>=0
evidence: x外帰納と全Rを覆う偶奇別署名帯表による全称証明。値2の定常pinは27=2y+z+1、値1基底点はx>=22で{19,21,23,25}のちょうど4点。x=23は掃引行O[27,45]。高さのみ縮約はx>=22でR<=26=z+2yが一様に成立し、各xでR=27が反例となる。有限監査は全称性の根拠ではなく独立照合である。
---
全ての \(x\ge4,R\ge0\) に対し \(H(R;(x,4);18)\) のGrundy値0/1/2を完全分類する。値2の定常pinは \(27=2y+z+1\)、値1基底点は \(x\ge22\) で \(\{19,21,23,25\}=\{z+1,z+3,z+5,z+7\}\) のちょうど4点である。\(x=23\) は値2が \(O[27,45]\) に広がる掃引行で、\(x\ge24\) では一点27へ戻る。

さらに全 \(x\ge22\) で
\[
R\le26=z+2y\Longrightarrow H(R;(x,4);18)=H(R;(x+4);18)
\]
が成立し、この一様境界は各xで鋭い。\(R=27\) では \(x=22\) の親値が0、\(x\ge23\) の親値が2で、単一トークン値1と異なる。

完全な値集合・署名帯表・mex証明は[証明報告](../../experiments/vertical-fiber-two-token-z18-y4-boundary-20261120/report.md)、独立検証器は[verify_z18_y4.py](../../experiments/vertical-fiber-two-token-z18-y4-boundary-20261120/verify_z18_y4.py)、監査結果は[audit.json](../../experiments/vertical-fiber-two-token-z18-y4-boundary-20261120/output/audit.json)。
