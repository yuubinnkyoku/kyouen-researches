---
id: K0326
title: 故障耐性ρが2以上の極大安全配置には一石交換がない
kind: proposition
status: proved
topics: [maximal-safe, reconfiguration]
aliases: []
relations:
- type: depends_on
  target: K0026
  note: 安全性の遺伝性と極大性
artifacts:
- path: research/experiments/original-claims/reports/round70-b301-b400-original-scope-audit.md
  role: proof
  note: ρの原文定義からの直接論証とB365の条件付き有限統計
- path: research/experiments/original-claims/output/round70_scope_catalogue_check.json
  role: data
  note: n6全最大の同被覆和内でρ2は交換次数0
---

# 故障耐性ρが2以上の極大安全配置には一石交換がない

有限盤の安全極大Sで、元の空点を一つでも合法に戻す最小石除去数ρ(S)が定義され、ρ(S)≥2なら、Sから石aを一つ除いて元の空点pを一つ追加する安全配置は存在しない。最大性は不要である。

ρ≥2の定義から、任意a∈Sに対してS\{a}でも全ての元の空点は使用不能である。従ってpを追加するS\{a}∪{p}は安全でない。削除点a自身が合法になることは交換先の存在ではない。

特に同サイズ安全族内で一石交換次数は0。逆のρ1なら交換次数が正という命題は含めない。B365のn6全464最大では被覆和を合わせた七セルでρ2の平均次数0、ρ1は1..3だが、この有限の厳密差を全盤の統計関係としない。

