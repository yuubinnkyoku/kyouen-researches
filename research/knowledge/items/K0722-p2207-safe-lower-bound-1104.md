---
id: K0722
title: 剰余放物線Q_2207の最大安全サイズは1104（単一CNFの独立schema・RUP/LRAT監査済み）
kind: proposition
status: computed
topics: [maximum-safe, geometry, verification]
aliases: []
relations:
- type: depends_on
  target: K0693
  note: 全1105点集合を覆う単一CNFの独立schema・幾何・RUP/LRAT監査による上界1104
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
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/output/manifest.json
  role: manifest
  note: 独立schemaと幾何を照合した上界CNF・採用LRAT gzipの所在とhash、二実装の検査記録
- path: research/experiments/parabola-p2207-single-cnf-audit-20261110/output/replay.json
  role: data
  note: 圧縮CNF・LRATの別処理実再生と、既存の1104点下界receipt・入力hashの結び付け
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/shape_c_2207.json
  role: data
  commit: eece6d3cf909f97cc2edfaa5cd85fd0701b50bc1
  note: 保存されたshape cのSAT候補。safe_against_edgesの自己判定だけでは採用しない
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-2207-1105/a2207_1105.cnf
  role: certificate
  note: サイズ1105（クラス(1,1,0)）の単一CNF。7,720変数・50,616節
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/cert-2207-1105/a2207_1105.drat.gz
  role: certificate
  note: 上記CNFのDRAT証明（解凍後497,179行、SHA-256 F0CE140D...D77A7EA）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/shape_class_2207_1105.json
  role: data
  note: 単一CNFの求解記録（UNSAT、19.9秒、検証875秒）
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
scope: Q_2207={(t,t² mod 2207):0<=t<2207}の標準q=4安全最大サイズ。指定1104点集合による有限検算の下界と、全1105点集合を覆う忠実な単一CNFのRUP/LRAT監査による上界。正確値1104を有限計算として主張し、他素数への一般化は主張しない。
evidence: 保存1104パラメータの整数幾何検査を独立下界として採用。上界は7720変数・50616節の単一CNFを18748構造節と31868真の禁止四点へ独立照合し、元DRATのRUP限定検査・修正版LRAT検査・採用圧縮証明の別処理実再生に成功。下界と上界のhash bindingを照合してA(2207)=1104を有限計算として確認。
---

## 命題と固定証人

**A(2207) = 1104**。下界は保存1104点の独立幾何監査、上界はサイズ1105の単一CNFのDRAT証明（2026-11-10）。
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
この下界とK0693の単一CNF監査による上界1104を合わせ、A(2207)=1104となる。

## 上界との結び付け

K0693の独立schemaは、全1105点安全集合を覆うクラス(原点あり、完全対一つ、空対なし)を検査した。
全50616節を構造18748節と幾何31868節に分離し、幾何節は全て整数行列式で検査した。
元DRATを固定RUP限定検査で受理し、187955行LRATを空節処理修正版で受理した。
さらに採用CNF・LRAT gzipの別処理での実再生と、本項の下界入力・receiptとのhash bindingを確認した。

## 限界

下界の有限検査はC++検査器とコンパイラに依存し、検査器全体の形式的健全性証明ではない。
5制御例は有限の回帰である。
K0693の旧d別の修正版被覆は21/1103のままだが、本項の上界はその未完了の全数走査に依存しない。
別経路の単一CNFで全1105点集合の排除を監査した。
本項は有限計算・検査器・コンパイラへの依存を残し、Lean形式化、全1104点集合の分類、他素数の最大値は主張しない。
