---
id: K0009
title: Lean形式化の範囲と具体証明書の信頼境界
kind: verification
status: verified
topics:
- formalization
- certificates
aliases: []
relations:
- type: verifies
  target: K0007
  note: 抽象局所条件から勝敗への一般健全性
- type: verifies
  target: K0337
  note: 固定点なし対合とブロック条件による抽象十分条件のみ
- type: verifies
  target: K0434
  note: 整数座標の円・直線方程式とForbiddenFourの同値
artifacts:
- path: Kyouen/OddInvolution.lean
  role: lean
  note: 抽象鏡映定理と有限盤上のLosingへの接続
- path: Kyouen/IntegerGeometry.lean
  role: lean
  note: 行列式と分母を払った円・直線方程式の同値
- path: Kyouen/FormalizationChecks.lean
  role: lean
  note: 仮定の境界例、盤面ルールへの接続例、主要定理の公理一覧
- path: Kyouen/Rules.lean
  role: lean
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: Kyouen/CertificateSoundness.lean
  role: lean
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: docs/PROOF_STATUS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# Lean形式化の範囲と具体証明書の信頼境界

Kyouen/Rules.leanは一般n×n盤の整数行列式、相異なる禁止四点、LegalMove、movesを定義する。CertificateSoundness.leanはLocallyValidからWinning/Losingを導く一般健全性をrank帰納で証明する。

`Kyouen/MaximalParity.lean` はK0305の一般ゲーム論部分、`Kyouen/OddInvolution.lean` はK0337の抽象ブロック十分条件を形式化する。
後者は未使用点への合法な鏡像応手と有限性から同じ `Losing` を導く。幾何学的な鏡映がブロック条件を満たすことは未接続。

`Kyouen/IntegerGeometry.lean` は、相異なる最初の二点を持つ整数座標四点について、行列式0と分母を払った円または直線の方程式の同値を証明し、既存の `ForbiddenFour` に接続する（K0434）。
実数型上のユークリッド円や距離・平方根の定義との同値はまだ形式化していない。
これらの追加定理はLean 4.35.0でコンパイルし、公理一覧は `propext`, `Classical.choice`, `Quot.sound` のみであることを確認した。

具体的な巨大バイナリ証明書の読み込みと局所条件の全件検査はC++またはRust側。具体証明書をLean核のみで検査する実装はない。一般定理の形式化を9×9や10×10の具体的な核検査済み勝敗定理と表現しない。
