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