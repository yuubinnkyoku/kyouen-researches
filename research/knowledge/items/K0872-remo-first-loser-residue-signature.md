---
id: K0872
title: 3枝REMOの非坍縮キーはr=3..8で第1敗者剰余がちょうど2種類
kind: computation
status: computed
topics: [multiplayer, variants, strategy-length]
aliases: [three-branch first-loser residue signature]
relations:
- type: depends_on
  target: K0864
  note: 任意枝数・任意rで可能第1敗者集合が {C_i mod r} となる全称補題FL
- type: depends_on
  target: K0862
  note: r=3・cap<=10の非坍縮22キー完全境界
- type: depends_on
  target: K0866
  note: r=7・cap<=10の非坍縮6キー完全境界
- type: depends_on
  target: K0869
  note: r=8・cap<=10の非坍縮10キー完全境界
artifacts:
- path: research/experiments/remo-first-loser-residue-signature-20261116/report.md
  role: data
  note: K0862/K0864/K0866/K0869の完全境界とFLを組み合わせた剰余署名の有限分類
- path: research/experiments/remo-first-loser-residue-signature-20261116/verify_first_loser_residue_signature.py
  role: verifier
  note: 715キー列挙、非坍縮一覧の剰余署名、r=9の事前整理を再現する標準ライブラリ検証器
- path: research/experiments/remo-first-loser-residue-signature-20261116/output/audit.json
  role: data
  note: r=3..9の剰余類計数、r=3..8の非坍縮署名、r=9の715キー事前分類
scope: "3枝REMO、各枝サイズ1..10、0<=gamma<min(C_1,C_2,C_3)、r=3..8の既存完全境界結果に対する有限な剰余署名再分類。r=9については715キーの第1敗者剰余クラス数だけを列挙し、ゲーム結果は計算しない。"
evidence: "各r=3..8の既存非坍縮キー一覧（K0862/K0864/K0866/K0869）を、K0864の全称補題FLに従って {C_1 mod r,C_2 mod r,C_3 mod r} へ写像。全ての非坍縮キーで剰余集合の大きさは2、かつ各r内で同一の剰余対。715キーの直接列挙と最小サイズ別和公式が一致。r=9は単一/二重/三重剰余の件数57/336/322を完全列挙。"
---

## 主張

枝サイズ \(C_1\le C_2\le C_3\le10\)、共通核サイズ \(0\le\gamma<C_1\) の715キーについて、既存の完全境界結果が示すr=3..8の全非坍縮キーを、全称補題FLの第1敗者集合

\[
L_r=\{C_1\bmod r,C_2\bmod r,C_3\bmod r\}
\]

で分類すると、**全ての非坍縮キーで \(|L_r|=2\)** であり、各rの全非坍縮キーは同一の剰余対を持つ。

| r | 非坍縮キー数 | 共通剰余対 |
|---:|---:|---:|
| 3 | 22 | {0,2} |
| 4 | 12 | {0,1} |
| 5 | 12 | {3,4} |
| 6 | 6 | {2,4} |
| 7 | 6 | {2,4} |
| 8 | 10 | {0,6} |

715キー全体の \(|L_r|=1,2,3\) の件数は、r=3..9について監査JSONに記録した。

## r=9の探索順に関する情報

r=9では、715キーは単一剰余57、二重剰余336、三重剰余322に分かれる。既存r=3..8の観察を探索順にだけ反映するなら、336個の二重剰余キーを先に調べるのが自然である。ただし、これは候補の優先順位であり、残り379キーを除外する定理ではない。

## 限界

本項は既存の有限完全スイープを剰余署名で再分類した計算結果である。非坍縮の必要条件 \(|L_r|=2\) を一般のr・枝サイズへ拡張する証明はない。また、r=9のゲーム結果は未計算である。全称証明済みなのは前提として使った補題FLのみであり、本項の有限観察を全称定理へ昇格させない。
