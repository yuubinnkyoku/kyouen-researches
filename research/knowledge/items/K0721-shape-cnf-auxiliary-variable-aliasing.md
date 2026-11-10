---
id: K0721
title: 一般形状CNFの補助変数割当は選択変数と衝突し、実現可能な形状をUNSATへ誤符号化した
kind: proposition
status: computed
topics: [geometry, search-methods, verification, provenance]
aliases: []
relations: []
artifacts:
- path: research/experiments/parabola-size1323-drat-20261109/encoding_snapshot.py
  role: source
  note: 修正前search_shape_class.pyの凍結コード
- path: research/experiments/parabola-size1323-drat-20261109/input/legacy-p5-000.cnf
  role: data
  note: 禁止辺なしのp=5・2点形状なのにUNSATとなる30節の旧CNF
- path: research/experiments/parabola-size1323-drat-20261109/input/legacy-p5-000.drat
  role: certificate
  note: 旧CNF自体のUNSAT証明。幾何形状の不存在を証明するものではない
- path: research/experiments/parabola-size1323-drat-20261109/input/fixed-p5-000.cnf
  role: data
  note: 変数範囲を保持した修正版のSAT入力
- path: research/experiments/parabola-size1323-drat-20261109/counterexample.json
  role: data
  note: 重複ID、旧CNFのDRAT受理、修正版モデルと2点のパラメータ、各hash
- path: research/experiments/parabola-size1323-drat-20261109/encoding_fixed.py
  role: source
  note: 修正後共有builderとbyte一致する凍結スナップショット
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/search_shape_class.py
  role: solver
  note: 各counter後にそれまでの予約範囲とnvのmaxを保持する修正版
- path: research/experiments/parabola-size1323-drat-20261109/regression.py
  role: verifier
  note: 反例の再現、修正版11896配置の整数幾何照合とp=2647の旧新CNF比較
- path: research/experiments/parabola-size1323-drat-20261109/regression.json
  role: data
  note: 小例の全照合、000/101の入力差分と011/112のbyte一致
- path: research/experiments/parabola-size1323-drat-20261109/README.md
  role: source
  note: 反例、修正、旧証拠への制限、保存証明と監査再開の手順
scope: 修正前のsearch_shape_class.pyの変数予約不具合とp=5の具体的反例。p=2647の旧000/101形状入力の忠実性を否定するが、上界1322そのものの数学的反証ではない。修正後の一般健全性は有限回帰だけからは主張しない。
evidence: 禁止四点を与えないp=5の2点形状が旧CNFでUNSAT、修正版でSAT。旧CNFのUNSATはDRAT検査でも確認した。修正版11896配置は整数幾何と一致。
---

## 具体的な反例

p=5、h=2、(x,c,e)=(0,0,0)では原点なしで各対から一側を選ぶ2点集合が4通り存在する。
2点に禁止四点は含まれないので、禁止辺を空にした形状CNFはSATでなければならない。
ところが旧builderの10変数・30節はUNSATであり、そのDRATも修正版検査器で受理された。
これはソルバ・DRAT検査器の誤判定ではなく、形状からCNFへの誤符号化である。

## 原因

4値の選択変数は1..8までを予約し、最後の対のLOW/HIGHは7,8。
CardEnc.equalsのtrivialなbound=0では、返るnvが予約したtop_idより小さく、入力literalの最大IDまでとなり得る。
旧コードはBOTHのnvだけをNONEのtop_idへ渡し、最後はNONEのnvだけを点変数の開始位置にした。
この例ではpoint_base=6となり、点1/2の補助変数も7,8になってLOW/HIGHと衝突した。
点2の補助変数H_2はL_2と同値にされる一方、one-hotはL_2とH_2の排他的選択を要求するので矛盾する。

修正は、初期の4hと各段階までに使ったIDの最大値を保持し、
`top=max(top,card_b.nv)`、`point_base=max(top,card_n.nv)` とすること。
修正版は12変数・30節で、保存したモデルが全節を満たし、実際に2点を選ぶ。

## 既存結果への影響と限界

p=2647、サイズ1323の旧入力では000/101が修正版と異なり、旧UNSATを幾何上界の根拠へ採用できない。
011/112は修正版とbyte単位で一致するため、この問題による失効はない。
前回のh+1=1324点の3形状監査は当初から予約範囲をmaxで保持しており、監査済み上界1323は影響を受けない。
上界1322という命題自体を反証したわけではない。現在は[K0711](K0711-p2647-safe-lower-bound-1292.md)で
修正後入力の全4形状のRUP/LRAT監査が完了し、上界1322を採用した。旧000/101の入力は引き続き根拠に使わない。

p=3,5,7,11,13,17の修正版11896配置で、各形状と独立整数幾何の安全性が一致した。
これは実装回帰であり、CardEncやsolver、検証器全体の形式的健全性証明ではない。
