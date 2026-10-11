---
id: K0389
title: 長方形盤の共円・共線点組数の鏡映公式（法2・法4）
kind: proposition
status: proved
topics:
- geometry
- rectangles
- statistics
aliases: []
relations: []
artifacts:
- path: research/experiments/rectangle-reflection-parity-20261011/proof.md
  role: proof
  note: 二軸鏡映による全称母関数公式と四点版閉公式
- path: research/experiments/rectangle-reflection-parity-20261011/verify.py
  role: verifier
  note: 整数円方程式と独立四点行列式による有限監査
- path: research/experiments/rectangle-reflection-parity-20261011/audit.json
  role: data
  note: 49盤245条件の偶奇照合と25盤の四点完全列挙
- path: research/experiments/geometry/reports/rectangle-v4-mod4-20261011.md
  role: proof
  note: 全w,hの共円・共線四点組V4法4公式
- path: research/experiments/geometry/reports/rectangle-v4-mod4-source-proof-20261011.md
  role: proof
  note: 原ZIP内の独立導出
- path: research/experiments/geometry/scripts/rectangle_v4_mod4_audit_20261011.py
  role: verifier
  note: 整数行列式の有限盤監査
- path: research/experiments/geometry/output/rectangle_v4_mod4_audit_source_20261011.txt
  role: data
  note: 原ZIPの監査記録
scope: 全正整数w,h、q≥4の標準整数長方形盤
evidence: 位数4の鏡映群の軌道と円・直線の一意性による全称数学的証明、独立整数計数による有限監査
---

# 長方形盤の全q点共円・共線組数の偶奇公式

長方形 P(w,h) の共円q点組数 C_q、共線q点組数 H_q の偶奇を、二軸鏡映の不変点組だけで正確に求められる。中心からの倍座標で半径Rごとの4点軌道数u_R、2点軌道数v_Rを数えると

```text
C_q ≡ Σ_R [t^q](1+t^4)^{u_R}(1+t²)^{v_R} (mod 2).
```

特に奇数qでは共円q点組数は偶数。a=⌊w/2⌋, b=⌊h/2⌋ とすると、共線について

```text
q=2k:   H_q ≡ [h奇数]binom(a,k)+[w奇数]binom(b,k)
q=2k+1: H_q ≡ [w,h奇数](binom(a,k)+binom(b,k))
```

四点版は次の閉公式になる。

```text
C_4 ≡ ab+[w,h奇数]min(a,b),
H_4 ≡ [h奇数]binom(a,2)+[w奇数]binom(b,2) (mod 2).
```

正方形 n×n では禁止四点組総数が奇数となるのは n≡2 (mod 4) の場合に限る。長方形への拡張と全qの母関数が本項の新しい範囲である。

証明・適用条件・独立検証の詳細: [proof](../../experiments/rectangle-reflection-parity-20261011/proof.md)。有限検算は無界証明の代わりではない。Grundy数や勝敗の定理ではない。
