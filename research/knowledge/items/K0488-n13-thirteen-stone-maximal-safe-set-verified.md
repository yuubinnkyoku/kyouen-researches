---
id: K0488
title: 13×13に13石の極大安全集合が存在する（検証済みwitness）
kind: proposition
status: computed
topics:
- maximal-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0026
  note: 極大安全集合の定義（包含極大）
artifacts:
- path: research/experiments/local-main-integration-20261020/source/NEW13-r4-report.md
  role: source
  note: 探索条件・witness・比較・限界
- path: research/experiments/local-main-integration-20261020/source/verify_new13.py
  role: verifier
  note: 独立整数行列式検証。forbidden quads 0、未阻害空点 0
- path: research/experiments/local-main-integration-20261020/verify_witnesses.py
  role: verifier
  note: 今回の独立した差分3×3整数行列式・全空点阻害検査
- path: research/experiments/local-main-integration-20261020/witness-validation.json
  role: data
  note: 今回の安全性・極大性と阻害三つ組分布
scope: 13×13標準ルール（4共円または共線の禁止）における13石極大安全集合の存在。単一witnessの存在のみを主張し、最小・最大・完全列挙は主張しない。
evidence: "heuristic search (90.0s, seed 20261017) found witness_ids [25, 28, 35, 55, 84, 85, 90, 99, 107, 108, 119, 130, 140]; independent Python verifier (research/experiments/local-main-integration-20261020/source/verify_new13.py): 0 forbidden quads among C(13,4)=715 subsets; 0 unblocked among 156 empty points; block-count distribution {1:38, 2:51, 3:32, 4:23, 5:8, 6:3, 7:1}."
---

# 13×13に13石の極大安全集合が存在する

13×13盤に安全な13石の極大集合が存在する。行優先 index `p = x + 13*y` による witness:

`25, 28, 35, 55, 84, 85, 90, 99, 107, 108, 119, 130, 140`

座標 `(x,y)`:

`(12,1), (2,2), (9,2), (3,4), (6,6), (7,6), (12,6), (8,7), (3,8), (4,8), (2,9), (0,10), (10,10)`。

独立検証結果:

- 安全性: 全 `C(13,4)=715` 個の4部分集合について、4×4行列式（行 `[x^2+y^2, x, y, 1]`）が非零 → forbidden quadruple 0個。
- 極大性: 156個の空点すべてが、少なくとも1つの石の三つ組と組み合わせて forbidden quadruple を作る → 未阻害空点 0個。
- 阻害三つ組数の分布: 1:38, 2:51, 3:32, 4:23, 5:8, 6:3, 7:1（最小1、最大7）。
- 密度: `13/169 = 7.69%`。

限界:

- 単一 witness の存在のみを示す。完全列挙や非存在証明ではない。
- `s_13`（最小極大サイズ）の既知上界 `≤12` を更新しない。13石極大の存在は最小値を決めない。
- `K_13`（最大安全サイズ）を更新しない。本 witness は小さい極大例である。
- 13石が最小でも最大でもない。探索は有界ヒューリスティック成功であり、非存在や最小性の証明ではない。

## 2026-10-17 bounded advance (round 4)

New finite evidence: 13-stone maximal safe set on 13x13 verified. Indices 25,28,35,55,84,85,90,99,107,108,119,130,140; Python verifier: 0 forbidden quads among 715 subsets; 0 unblocked among 156 empty points; block-count distribution {1:38,2:51,3:32,4:23,5:8,6:3,7:1}; density 13/169=7.69%. Search: 90.0 s bound, terminated at 0.1054 s, 23,519 steps, 2 restarts. Compared with known 12-stone set (only index 84 shared).

Scope clarification: existence of one verified witness only; does not update s_13 <= 12 or K_13. K0488 status remains computed.

Next steps: none beyond existing scope; no complete enumeration or minimum/maximum claim. Status remains computed.
