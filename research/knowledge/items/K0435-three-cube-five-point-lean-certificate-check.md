---
id: K0435
title: 3×3×3・5点禁止ゲームの839局面証明書をLeanで具体検査し空盤後手必勝を証明
kind: verification
status: verified
topics:
- formalization
- certificates
- variants
aliases: []
relations:
- type: depends_on
  target: K0009
  note: Lean局所条件とWinning/Losingの健全性を使用
- type: supports
  target: K0102
  note: 3×3×3の具体証明書についてLean核検査を完了。一般巨大証明書は未完了
artifacts:
- path: Kyouen/CubeRules.lean
  role: lean
  note: 3×3×3盤・5点禁止判定・合法手
- path: Kyouen/CubeSymmetry.lean
  role: lean
  note: 48対称変換と正規化
- path: Kyouen/CubeCertificate.lean
  role: lean
  note: 839局面証明書の局所条件検査と空盤後手必勝定理
- path: Kyouen/CubeCertData.lean
  role: lean
  note: certificate.b64から生成した具体データ
- path: research/experiments/highdim-q5-cubes-20261016/verify_certificate.py
  role: verifier
  note: 独立Python検証器
---

# 3×3×3・5点禁止ゲームの839局面証明書をLeanで具体検査

3×3×3の27点を `Fin 27` で表し、5点の禁止を整数座標の5×5行列式（差分4×4行列式）で定義した。48個の立方体対称変換で正規化した839局面のAND/OR証明書をLeanの具体データに変換し、`LocallyValid` を検査した。P局面では全合法子がN、N局面では少なくとも一つの合法子がPであることを、局面ごとの合法手判定とともに確認した。1石4軌道（2石20軌道）の勝ちを経て空盤が後手必勝であることを `empty_board_losing` として証明した。

限界: 一部の有限検査（839局面の局所条件、単石軌道の合法手存在、対称性の全単射性・禁止集合不変性）は `native_decide` によるコンパイル時評価に依存する。証明された `empty_board_losing` は 48 対称性で正規化した圧縮ゲーム上の定理であり、元の `CubeRules.moves` への接続 (`empty_board_losing_raw`) は未完成である。任意辺長の奇数辺立方格子への一般化も未解決。

## 2026-10-17 bounded advance (round 2)

New finite evidence: 3D q=5 cube variant highdim extension. Exact solver + independent Python verifier agree on 2x2x5: forbidden 5-sets 3,464; safe states 32,028; terminal 7,405; root Grundy 0; two-stone g=0 190/190; max Grundy 5. Comparison 2x3x4: forbidden 8,480; safe 107,543; terminal 25,226; root 0; two-stone 160/276; max 4. Recorded 3x3x3: forbidden 16,026; safe 205,506; terminal 57,296; root 0; two-stone 351/351 in 20 orbits; certificate 839 canonical positions, 1,130 edges. Hypotheses: H1 2x2xn all two-stone P for n>=4 (observed n=4,5,6? here n=4,5) with exception n=3 (18/66); H2 nim-values beyond 4 (value 5 occurs). Mirror theorem explains losing empty board for grids with an even side but not two-stone status.

Scope clarification: computational, not proof; enumeration limited to <=27 points; H1 remains hypothesis. Supports K0435 3x3x3 certificate result but does not change its verified status.

Next steps: test 2x2x7 (requires raising limit) or find symmetry/strategy proof; ensure certificate style allows nim-values up to at least 5. Status of K0435 remains verified.

## 2026-10-17 bounded advance (round 3)

New finite evidence: 2x2x6 fully enumerated: forbidden 5-sets 8,696; safe states 111,423; terminal 25,236; root Grundy 0; two-stone g=0 276/276; max Grundy 5. C++ Bareiss and Python independent verifier agree (hash 70f99cad9a01fa754a2616a253d7d0a78607f23760f333b052ccbe7aad59b457). H1 now supported for n=4,5,6; exception n=3 (18/66) remains.

Scope clarification: finite confirmation only; does not prove H1 for all n. Enumeration bounded to 24 points; 2x2x7 not tested. No source files modified.

Next steps: raise state-space limit/mask width or find symmetry/strategy proof; test larger n. K0435 status remains verified.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
