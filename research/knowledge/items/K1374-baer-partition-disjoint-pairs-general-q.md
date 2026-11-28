---
id: K1374
title: Bruck の Baer 分割による PG(2,q^2) の disjoint Baer 対の一般存在と t=2 上界 2(q^2+q+1) の全域化・PG(2,25)/(2,49)/(2,64)/(2,81) の新上界
kind: proposition
status: proved
topics: [blocking-sets, finite-geometry, baer-subplanes, singer-groups]
aliases: [Baer partition general q, disjoint Baer pairs all q, PG2q2 upper bound 2(q2+q1)]
relations:
- type: depends_on
  target: K1373
  note: 条件付き補題「disjoint Baer 対が存在すれば min <= 2(q^2+q+1) < 3q^2」の
    存在条件を Bruck の Baer 分割定理で全域化し、PG(2,25)/(2,49)/(2,64)/(2,81)
    に新 witness を与える。K1373 の「一般 q での存在は未証明」は本項目で解消。
- type: depends_on
  target: K1372
  note: q=2 軌道 (Fano 型 Baer) の直線プロファイル {1:14, 3:7} の較正。
artifacts:
- path: research/experiments/baer-partition-general-q-20261128/scripts/baer_partition_impl1.py
  role: verifier
  note: GF(p^{2m})+3次拡大の塔による構成・design/Baer/witness 全数判定
- path: research/experiments/baer-partition-general-q-20261128/scripts/baer_partition_impl2.py
  role: verifier
  note: GF(p^{6m}) 直接構成+部分体内部列挙+GF(p) 線形代数の独立実装
- path: research/experiments/baer-partition-general-q-20261128/out/impl1_all.json
  role: data
  note: q=2,3,4,5,7,8,9 の検証結果・witness 点座標
- path: research/experiments/baer-partition-general-q-20261128/out/impl2_all.json
  role: data
  note: 独立実装の結果 (不変量は impl1 と完全一致)
- path: research/log/2026-11-28-baer-partition-general-q.md
  role: log
  note: 宣言・amendment・実行・バグ開示・出版の一次記録
scope: >-
  (a) 引用定理: Bruck — PG(2,q^2) の Singer 群 <g> に対し <g^(q^2-q+1)> の
  点軌道は q^2-q+1 枚の disjoint Baer 部分平面の分割をなす
  (arXiv:2403.13734v2 Lemma 2.4 / J. Combin. Des. 2024, DOI 10.1002/jcd.21956)。
  (b) 有限機械検証: q = 2,3,4,5,7,8,9 で (a) の分割を2つの独立実装で
  定義直接・全数検証 (design・生成元位数・軌道分割・Baer 基準・witness)。
  (c) 上界: PG(2,q^2) の t=2 最小2重ブロッキング min <= 2(q^2+q+1)。
evidence: >-
  (c) は (a)+K1373 で q>=3 の全素体冪に対して成立 (2(q^2+q+1) < 3q^2)。
  新規有限上界: PG(2,25) <= 62, PG(2,49) <= 114, PG(2,64) <= 146,
  PG(2,81) <= 182 (witness = Singer 分割の軌道 2 枚の union・
  全直線との交差 >=2 を機械検証)。PG(2,9) <= 26・PG(2,16) <= 42 は
  K1373 と同一値を独立 witness で再現。系 (証明つき): 分割の
  k (<= q^2-q+1) クラスの union は k 重ブロッキング
  (k=2 全 q・k=3 は q=4 で機械検証)。較正: q=3 の 26 点 witness の
  直線プロファイル {2:65, 5:26} は K1373 の witness と完全一致、
  q=2 軌道プロファイル {1:14, 3:7} は K1372 の Fano census と一致。
  独立2実装 (塔構成 vs GF(p^{6m}) 直接+部分体内部列挙) の全不変量一致。
  主張の限界: (a) は Bruck の引用定理であり自前の全称証明ではない。
  min の下界は主張しない (PG(2,9) は [19,26] のまま)。
---

## 命題・範囲

1. **一般存在 (引用定理による)**: すべての素体冪 q で PG(2,q^2) は
   q^2-q+1 枚の pairwise disjoint な Baer 部分平面に分割される
   (Singer 部分群 <g^(q^2-q+1)> の点軌道)。よって **すべての q >= 3 で
   PG(2,q^2) の t=2 min <= 2(q^2+q+1) < 3q^2** が無条件で成立し、
   K1373 の条件付き補題の存在条件は全域で充足される。
   「PG(2,n) t=2 min = 3n」パターンは平方位数 n = q^2 >= 9 では
   すべて不成立。
2. **有限機械検証 (自前・定義直接・全数)**: q = 2,3,4,5,7,8,9 の各 q で、
   2つの独立実装 (GF(p^{2m}) 塔構成 / GF(p^{6m}) 直接構成+部分体内部列挙) が
   ともに、(i) design 検査 (点=直線=q^4+q^2+1・各直線 q^2+1 点・
   各点 q^2+1 直線・2直線の交差はちょうど1点)、(ii) 生成元の位数完全検証、
   (iii) 軌道分割 (q^2-q+1 軌道 × q^2+q+1 点・disjoint・総和 N)、
   (iv) 各軌道の Baer 基準 (全直線との交差 1 または q+1 点・
   (q+1)-secant ちょうど q^2+q+1 本)、(v) 軌道対 union の
   全直線交差 >=2、を検証し、全不変量が一致。
3. **新規有限上界 (witness つき)**: PG(2,25) <= 62、PG(2,49) <= 114、
   PG(2,64) <= 146、PG(2,81) <= 182。いずれも 3q^2 未満。
   PG(2,9) <= 26・PG(2,16) <= 42 は K1373 と同一値 (独立 witness)。
4. **系 (証明つき)**: 分割の任意の k クラス (k <= q^2-q+1) の union は
   サイズ k(q^2+q+1) の k 重ブロッキング。k=2 全 q・k=3 (q=4) は機械検証。

## 現在の根拠と限界

- 一般定理 (1) は Bruck の結果の引用 (Nagy et al. 2024 Lemma 2.4 経由)。
  自前の寄与は q <= 9 の完全機械検証と witness による上界の拡大。
- 下界は counting bound のみで本項目では改良しない。
- PG(2,9) k=25 SAT (min = 26 確定)・PG(2,16) disjoint 対全数 census は
  引き続き open (長期レーン向け)。

## 次の接続

- PG(2,q^2) の t 重ブロッキング min <= t(q^2+q+1) と既知下界のギャップ。
- AG(2,q^2) 制限 (Baer 導入直線の除去) での同種の分割構造。
- 標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費。

## Addendum (2026-11-28): q=11, 13 への拡張 (宣言 `709c8515`)

- 実験 dir: research/experiments/baer-partition-q11-q13-20261128/
- **PG(2,121) <= 266 < 363** (111 軌道 × 133 点・per-orbit プロファイル
  {1:14630, 12:133}・witness プロファイル {2:14497, 13:266})・
  **PG(2,169) <= 366 < 507** (157 軌道 × 183 点・{1:28548, 14:183}・
  witness {2:28365, 15:366}) を全数機械検証 (impl1)。
- 有限検証範囲は q = 2,3,4,5,7,8,9,11,13 (impl1)。
  q=11,13 は単一実装 (impl2 の gamma 探索は p^{6m} 走査で q>=11 は
  スケール外)。design・Baer・Singer 商位数の fail-closed 検査は全数実施。
- 生成元位数の O(ordE) 追加ループは ordE > 600,000 で skip
  (factor test gamma^{ordE/f} != 1 (all prime f) が位数の完全検証として十分)。
