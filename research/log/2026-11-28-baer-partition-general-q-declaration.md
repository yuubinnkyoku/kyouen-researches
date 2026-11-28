# 宣言: Baer partition (Bruck) の独立機械検証 q=2..9 と disjoint Baer 対 witness による新上界

- 日時: 2026-11-28
- 種別: 高速レーン (publish-then-execute・単一オーナー)
- 宣言時 HEAD: d2d3c398028f8de35d29bff2ea24165a2a97b847
- 目的: K1373 の「次の接続」(一般 q での disjoint Baer 対存在・Baer partition 文献との接続) を実行する。

## 背景

- K1373 (status: proved): disjoint Baer 対が存在する PG(2,q^2) では t=2 最小2重ブロッキング
  min <= 2(q^2+q+1) < 3q^2 (q>=3) は数学的証明済み。存在は q=2 (2,880対)・q=3 (3,265,920対)
  全数機械検証・q=4 サンプリングのみで、「全ての q>=3 で存在」は未証明の条件だった。
- 文献: Bruck による古典的結果 (Singer cycle を用いる Baer subplane decomposition)。
  Nagy et al. 2024 (arXiv:2403.13734v2 / J. Combin. Des. 2024, DOI 10.1002/jcd.21956)
  Lemma 2.4: PG(2,q^2) の Singer group <g> に対し、<g^(q^2-q+1)> の点軌道は
  q^2-q+1 個の disjoint Baer 部分平面 (各 PG(2,q)) の分割をなす。

## 本実行の計画 (all finite, q in {2,3,4,5,7,8,9})

1. 純 Python で GF(q^2) (:= GF(p^{2m}))・GF(q^6) (:= GF(p^{6m}) = GF((q^2)^3)) を独立構成し、
   GF(q^2)^3 ≅ GF(q^6) (3次拡大) を用いて Singer 群 (商群 GF(q^6)*/GF(q^2)*) を実装。
   点 = GF(q^2)* の剰余類、μ-代表 x -> x^(q^4+q^2+1) で正規化。
2. 部分群 <s^(q^2-q+1)> (位数 q^2+q+1) の点軌道分割を計算し、各軌道について
   (a) |軌道| = q^2+q+1、(b) 全直線との交差が 1 または q+1 点 (Baer 性の十分判定)、
   (c) (q+1)-secant 直線がちょうど q^2+q+1 本、を機械検証。
   軌道は group action の軌道なので disjoint 性は自動 (サイズ総和 = q^4+q^2+1 も検証)。
3. 2つの軌道の union (size 2(q^2+q+1)) が全直線と >=2 点で交わることを定義直接機械検証し、
   q=4,5,7,8,9 の新 witness として記録: PG(2,25) <= 62, PG(2,49) <= 114,
   PG(2,64) <= 134, PG(2,81) <= 166 (いずれも < 3q^2)。
   k 個の軌道の union は k-重ブロッキング (k <= q^2-q+1) となる系も q=4, k=3 で機械検証。
4. 較正: q=2 (PG(2,4)) の各軌道は Fano 型 Baer (直線プロファイル {1:14, 3:7}・K1372 census の
   360 Fano Baer と整合)、q=3 (PG(2,9)) は K1373 の 26 点 witness 構成 (disjoint Baer 対 union)
   と同型のものが得られること・直線プロファイル {1:78, 4:13} を確認。
   q=2,3 では K1373 の全数census (disjoint 対 2,880 / 3,265,920) と矛盾しないことを確認
   (partition から得られる disjoint 対は全体の部分集合)。
5. 独立実装での再検証: GF(q^6) を GF(p^{6m}) として再構成する第2実装 (拡大順・基底違い)
   で q=2..9 の軌道分割・Baer 検査を再実行し一致を確認。

## 主張の区別

- 一般定理「すべての素体冪 q で PG(2,q^2) は q^2-q+1 枚の disjoint Baer 部分平面に分割される」は
  Bruck の結果の引用として提示する (自前の全称証明としては扱わない)。
  本実行の寄与は (i) q<=9 での完全機械検証 (有限・定義直接)、(ii) 新 witness による
  t=2 上界の改善 (PG(2,25)/(2,49)/(2,64)/(2,81))、(iii) K1373 の条件付き補題の
  「存在条件」がすべての q>=3 で充足されることの文献接続。
- min の下界は主張しない (counting bound のみ)。PG(2,9) min は [19,26] のまま。
- 標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費。

## 出版計画

- research/experiments/baer-partition-general-q-20261128/ (scripts + out + MANIFEST)
- research/knowledge/items/K1374-baer-partition-disjoint-pairs-general-q.md (仮番号・統合時再採番判定)
- research/log/2026-11-28-baer-partition-general-q.md (完了log)
