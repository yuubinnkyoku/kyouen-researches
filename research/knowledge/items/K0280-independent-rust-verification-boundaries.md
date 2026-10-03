---
id: K0280
title: 独立Rust実装の検査は参照探索・CSV監査・証明書局所検査を分ける
kind: verification
status: verified
topics:
- verification
- certificates
aliases: []
relations:
- type: verifies
  target: K0010
  note: 形式実装と選択局面の検査。全十盤根ではない
- type: verifies
  target: K0022
  note: 100初手CSVの構造のみ。勝敗ラベルの全独立再求解ではない
artifacts:
- path: rust/independent-verifier/VALIDATION.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: rust/independent-verifier/src/parts/board.rs
  role: verifier
  note: 独立幾何・合法手
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: rust/independent-verifier/src/parts/certificate.rs
  role: verifier
  note: rankとWIN/LOSS局所義務
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: rust/independent-verifier/KYOENC4_VALIDATION.md
  role: log
  note: high-word実証と旧版互換
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: rust/independent-verifier/CROSS_CHECK.md
  role: source
  note: 小盤cross check範囲
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 独立Rust実装の検査は参照探索・CSV監査・証明書局所検査を分ける

Rustは平行移動後の三×三整数行列式から10×10禁止54441を再生成し、C++と照合。参照全探索はn1..4、CIのKYOENC3生成証明書再検査はn1..6。CSVは100初手の重複欠落・D4応答・98子と53代表の構造を検査する。CSVが通るだけで全大根の独立再求解をしたことにはならない。

KYOENC4 high-word smokeは14石WIN→15石終端LOSS・二ノードでbit64..99と任意非空根の局所条件を確認。その後の大型選択根検査は別manifestを参照する。空盤十盤全体の単一証明書完了とは異なる。
