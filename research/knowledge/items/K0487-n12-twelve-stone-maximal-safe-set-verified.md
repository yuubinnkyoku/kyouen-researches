---
id: K0487
title: 12×12に12石の極大安全集合が存在する（検証済みwitness）
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
- path: research/experiments/local-main-integration-20261020/source/NEW12-r3-report.md
  role: source
  note: 探索条件・witness・比較・限界
- path: research/experiments/local-main-integration-20261020/source/verify_new12.py
  role: verifier
  note: 独立整数行列式検証。forbidden quads 0、未阻害空点 0
- path: research/experiments/local-main-integration-20261020/verify_witnesses.py
  role: verifier
  note: 今回の独立した差分3×3整数行列式・全空点阻害検査
- path: research/experiments/local-main-integration-20261020/witness-validation.json
  role: data
  note: 今回の安全性・極大性と阻害三つ組分布
scope: 12×12標準ルール（4共円または共線の禁止）における12石極大安全集合の存在。単一witnessの存在のみを主張し、最小・最大・完全列挙は主張しない。
evidence: "heuristic search (90.0s, seed 20261017) found witness_ids [5, 50, 56, 57, 61, 66, 68, 72, 77, 88, 98, 107]; independent Python verifier (research/experiments/local-main-integration-20261020/source/verify_new12.py): 0 forbidden quads among C(12,4)=495 subsets; 0 unblocked among 132 empty points; block-count distribution {1:34, 2:32, 3:33, 4:16, 5:11, 6:4, 7:2}."
---

# 12×12に12石の極大安全集合が存在する

12×12盤に安全な12石の極大集合が存在する。行優先 index `p = x + 12*y` による witness:

`5, 50, 56, 57, 61, 66, 68, 72, 77, 88, 98, 107`

座標 `(x,y)`:

`(5,0), (2,4), (8,4), (9,4), (1,5), (6,5), (8,5), (0,6), (5,6), (4,7), (2,8), (11,8)`。

独立検証結果:

- 安全性: 全 `C(12,4)=495` 個の4部分集合について、4×4行列式（行 `[x^2+y^2, x, y, 1]`）が非零 → forbidden quadruple 0個。
- 極大性: 132個の空点すべてが、少なくとも1つの石の三つ組と組み合わせて forbidden quadruple を作る → 未阻害空点 0個。
- 阻害三つ組数の分布: 1:34, 2:32, 3:33, 4:16, 5:11, 6:4, 7:2（最小1、最大7）。
- 密度: `12/144 = 8.33%`。

限界:

- 単一 witness の存在のみを示す。完全列挙や非存在証明ではない。
- `s_12`（最小極大サイズ）の既知上界 `≤11` を更新しない。12石極大の存在は最小値を決めない。
- `K_12`（最大安全サイズ）の既知下界 `≥22` を更新しない。本 witness は 22石構成より小さい極大例である。
- 12石が最小でも最大でもない。探索の有界失敗（23石 probe）は上界証明ではない。

## 2026-10-17 bounded advance (round 3)

New finite evidence: 12x12 maximal safe 12-stone set found by heuristic fixed-size walker (90.0 s, seed 20261017; 11,302 steps, 1 restart) and independently verified by Python integer geometry: 0 forbidden quads among C(12,4)=495 subsets; 0 unblocked among 132 empty points; block-count distribution {1:34,2:32,3:33,4:16,5:11,6:4,7:2}; density 12/144=8.33%. Witness indices 5,50,56,57,61,66,68,72,77,88,98,107. Additional bounded 23-stone probe (60 s) did not produce a safe 23-stone set (negative evidence only). Compared with n=11: 10-stone maximal on 11x11 vs new 12-stone on 12x12; density 8.26% vs 8.33%.

Scope clarification: existence of one verified witness only; does not change s_12 <= 11 or K_12 >= 22. K0487 status remains computed.

Next steps: none beyond existing scope; no complete enumeration or upper-bound claim. Status remains computed.

## 2026-10-17 bounded advance (round 4)

New finite evidence: K0487 creation/validation recorded by NEWK-r4. Item validated by check.py (431 items, 0 errors, 0 warnings) and build.py (6 views). Witness: 12-stone maximal safe set on 12x12, indices 5,50,56,57,61,66,68,72,77,88,98,107; independent verifier: 0 forbidden quads among 495 subsets, 0 unblocked among 132 empty points. Report artifact `research/experiments/local-main-integration-20261020/source/NEWK-r4-report.md` and verifier `research/experiments/local-main-integration-20261020/source/verify_new12.py` exist in repo.

Scope clarification: records only existence of one verified witness; does not change s_12 <= 11 or K_12 >= 22. K0487 status remains computed.

Next steps: none beyond existing scope; no complete enumeration or upper bound claimed. Status remains computed.
