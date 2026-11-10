---
id: K0722
title: 剰余放物線Q_2207の独立監査済み範囲は1104以上1105以下
kind: proposition
status: computed
topics: [maximum-safe, geometry, verification]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共線または共円四点を含まない標準q=4の安全性
- type: depends_on
  target: K0097
  note: 一般上界A(p)<=(p+3)/2からA(2207)<=1105
- type: depends_on
  target: K0334
  note: 整数共円行列式0なら四パラメータの和が0 mod pとなる必要条件
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/shape_c_2207.json
  role: data
  commit: eece6d3cf909f97cc2edfaa5cd85fd0701b50bc1
  note: 保存されたshape cのSAT候補。safe_against_edgesの自己判定だけでは採用しない
- path: research/experiments/parabola-p2207-1104-witness-20261110/audit.py
  role: verifier
  note: 候補抽出・点集合と対構造の照合・generic整数幾何の独立実行・5制御例
- path: research/experiments/parabola-p2207-1104-witness-20261110/output/candidate.txt
  role: certificate
  note: SHA-256 ce97d4a9447fd32cd67e3cfad59151774fa45cf90c8985287abb1a45480e2347の1104パラメータ
- path: research/experiments/parabola-p2207-1104-witness-20261110/output/extraction.json
  role: manifest
  note: 元JSON・抽出入力・driver・幾何検査器のhashと完全対・空対の対応
- path: research/experiments/parabola-p2207-1104-witness-20261110/output/geometry.json
  role: data
  note: 全61560516876四点の被覆と27941252整数行列式の非零を確認した実検査
- path: research/experiments/parabola-p2207-1104-witness-20261110/output/controls.json
  role: data
  note: 安全三点の受理、二完全対の禁止四点・重複・入力打切り・合成数の拒否
- path: research/experiments/parabola-local-repair-20261109/verify_subset.cpp
  role: verifier
  note: CNFや探索辺を読み込まないgeneric 4x4 Leibniz整数行列式と完全合同式フィルタ
- path: research/experiments/parabola-p2207-1104-witness-20261110/README.md
  role: source
  note: 固定点集合の出所・独立幾何検査・再現手順と最大値の信頼境界
scope: Q_2207={(t,t² mod 2207):0<=t<2207}の標準q=4安全最大サイズ。指定1104点集合による有限検算の下界と一般定理の上界。正確値1104や他素数への一般化は主張しない。
evidence: 保存1104パラメータを整数幾何検査し、合同式で全61560516876四点を被覆して残る27941252行列式すべて非零。一般上界1105と合わせて1104<=A(2207)<=1105。CNFのSAT判定やcached edge listへ依存しない。
---

## 命題と固定証人

**1104 <= A(2207) <= 1105**。
下界の証人は指定candidate.txtの1104点で、点は(t,t² mod 2207)とする。
パラメータは相異なり0..2206に属し、原点0を含む。
完全対は{307,1900}の一つ、空対は{1078,1129}の一つであり、他の対は片側を含む。

元の走査はshape cでSATと報告したが、採用する根拠はそのモデルやsafe_against_edgesフィールドではない。
点集合を固定して、別のgeneric整数4x4行列式検査器で安全性を実検査した。

## 幾何の被覆

K0334の合同式により、相異なる四パラメータの整数共円行列式が0なら、その和は0 mod 2207である。
選択された昇順三点ごとに唯一の第四候補を求め、三点より大きく選択集合に属するものを全て検査した。
この列挙は合同式を満たす各四点をちょうど一度含み、それ以外の四点は合同式だけで排除できる。

したがって全61560516876四点を被覆し、残った27941252四点のgeneric整数4x4行列式を計算した。
すべて非零であり、共円・共線四点は存在しなかった。検査時間は約10.66秒の経過時間。
一般上界K0097の1105と合わせ、主張の範囲が得られる。

## 限界

下界の有限検査はC++検査器とコンパイラに依存し、検査器全体の形式的健全性証明ではない。
5制御例は有限の回帰である。
[K0693](K0693-p2207-no-parabola-equality-witness.md)の全1103 dのUNSAT主張は全数独立監査が未完了であり、
その候補上界1104をここで独立監査済み上界として採用しない。
本項は包含極大性、全1104点集合の分類、正確値A(2207)=1104を証明していない。
