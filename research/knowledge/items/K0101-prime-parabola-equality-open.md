---
id: K0101
title: 全奇素数で剰余放物線上界(p+3)/2を達成するという予想は反証された
kind: proposition
status: refuted
topics:
- maximum-safe
- geometry
aliases: []
relations:
- type: depends_on
  target: K0097
  note: 一般上界と等号集合の完全対構造
- type: depends_on
  target: K0334
  note: 等号の存在とある完全対dのCNFのSATが同値
- type: depends_on
  target: K0706
  note: p=2647の全1323 dのUNSAT証明が修正版検証器で検査済み
artifacts:
- path: research/experiments/structural-lemmas-2026-10-02/quadratic-constructions.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/frontier-geometry-2026-10-05/proof.md
  role: proof
  note: 禁止四点の完全対分類とNAE・原点節の厳密な分解。全素数で充足可能という主張は含まない
- path: research/experiments/frontier-geometry-2026-10-05/recovered-witnesses.json
  role: certificate
  note: 131..251拡張の追跡されていなかった証人を回復・保存
- path: research/experiments/frontier-geometry-2026-10-05/density-probe-witnesses.json
  role: certificate
  note: 509,1009の追加有限等号証人
- path: research/experiments/parabola-equality-extension-20261016/README.md
  role: source
  note: 521..2000への有限拡張の当時の記録
- path: research/experiments/parabola-equality-extension-20261016/output/witnesses_521_2000.json
  role: certificate
  note: 521..1999の全206素数の等号証人
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2143_2500.json
  role: certificate
  note: 2003..2477の64素数のうち2207を除く63素数の等号証人
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/parabola-equality-audit.txt
  role: data
  note: generic 4×4 Leibnizによる全63証人の独立検証出力（共円0件）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/p2207_d_verdicts.json
  role: data
  note: p=2207の全1103 dのCNF UNSAT判定（反例候補。DRAT未検査）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/README.md
  role: source
  note: 反例候補の方法・全数照合・信頼境界
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2503_2700.json
  role: certificate
  note: 2503..2700の21素数の等号証人（5素数は浅いdで未発見）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/parabola-equality-audit-2503-2700.txt
  role: data
  note: 新21証人のgeneric 4×4独立検証出力（共円0件）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2701_2900.json
  role: certificate
  note: 2701..2900の20素数の等号証人（6素数は浅いdで未発見）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/parabola-equality-audit-2701-2900.txt
  role: data
  note: 20証人の独立検証出力（共円0件）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/witnesses_2901_3100.json
  role: certificate
  note: 2901..3100の17素数の等号証人（6素数は浅いdで未発見）
- path: research/experiments/parabola-equality-extension-2143-2500-20261107/output/parabola-equality-audit-2901-3100.txt
  role: data
  note: 17証人の独立検証出力（共円0件）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_2647_34249932790a9e9d.json
  role: data
  note: p=2647の全1323 dの修正版DRAT受理記録。K0706の有限計算の根拠
  commit: b52faa12b77ff8bae9cf5343b20f3561917381a6
- path: research/experiments/parabola-equality-refutation-20261109/verify_receipts.py
  role: verifier
  note: コミット済み監査記録の範囲・重複・ソースhashを確認する。DRATの再検査ではない
- path: research/experiments/parabola-equality-refutation-20261109/receipt_coverage.json
  role: manifest
  note: 全dの完全被覆、入力SHA-256、10負例拒否、実測範囲
- path: research/experiments/parabola-equality-refutation-20261109/README.md
  role: source
  note: 全称命題の反証の論理と有限計算の信頼境界
scope: 全奇素数pについてQ_p内の最大安全サイズA(p)が(p+3)/2に等しいという全称命題。反例p=2647の最大値そのものは決定しない。
evidence: K0706の全1323 dの修正版DRAT検査とK0334の等価よりA(2647)<=1324<1325。全称命題は有限計算で監査された反例によって否定される。
---

## 命題・対象範囲

元の全称命題は、全奇素数pに対して、標準q=4の剰余放物線
`Q_p = {(t,t² mod p): 0<=t<p}` 内の最大安全サイズA(p)が
`(p+3)/2` に等しい、という主張である。この命題は反証された。
同じK番号の真偽を更新したもので、別の修正版の予想に置き換えたわけではない。

## 監査済み反例と反証の論理

1. K0097により一般上界は `A(p)<=(p+3)/2`。
2. K0334により、h=(p-1)/2として、等号h+2の達成は、ある完全対dについて
   対応するCNFがSATであることと同値である。
3. K0706ではp=2647の全d=1..1323についてUNSATのDRAT証明を修正版検証器で受理した。
   コミット済み受理記録は1323件、重複・欠落・失敗0で、検証器ソースhashも一致する。
4. 従って `A(2647)<=1324<1325=(2647+3)/2`。一つの奇素数の反例で全称命題は偽となる。

このためstatusは `refuted`。従来のquestionから、否定された同じ全称命題を表すpropositionへ変更した。
これは有限計算に支えられた反例による否定であり、未検査の他素数に同じ不達成を一般化しない。

## 他の証拠と残る問い

5..2203の全奇素数、2213..2477、およびその後の多くの素数には、保存・検査された等号証人がある。
これらの肯定例は反例p=2647と矛盾しない。有限範囲の証人と独立検証の出典はartifactに保持する。
保存証人の完全対は必ずしもd=hではなく、例えばp=1861ではd=864=h-66、
p=2027,2399,2477ではd=h-1の証人が保存されている。
この証人の選び方だけから、同じ素数でd=hの証人が存在しないとは結論しない。
p=2207、2531、3251の等号不達成のソルバ計算はK0693、K0702、K0708を参照し、
それぞれの未完監査をp=2647の結果から完了扱いにはしない。

`A(2647)` の正確値、等号を達成する素数の特徴づけ、不達成素数の分布は未解決である。
例えば `A(2647)=1324` の下界証人は今回得ていない。

## 信頼境界

反証はK0334の幾何からCNFへの還元と、K0706の修正版DRAT検査による有限計算に依存する。
K0707で偽受理が見つかった旧検証器の記録は使わない。
今回追加したverify_receipts.pyはコミット済み受理記録の完全被覆と整合性を検査するもので、
個々のDRAT証明の再実行や、修正版検証器の一般的健全性の形式証明ではない。
検証器・符号化・コンパイラ等への実装上の依存は残る。
