---
id: K0301
title: 安全四石配置対は三石Johnson交換層を経由して接続できる
kind: proposition
status: proved
topics:
- reconfiguration
relations: []
aliases: []
artifacts:
- path: research/verification/round42-exact-residual-family-audit.md
  role: proof
  note: 四石配置間の三石Johnson橋の一般証明
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round42_families_verified.json
  role: data
  note: 明示証人と有限照合結果
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round42_families_audit.py
  role: verifier
  note: 証人の独立検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 安全四石配置対は三石Johnson交換層を経由して接続できる

任意の標準盤で安全な四石配置 (S,T) を取る。Sから一石を除いて三石集合 (S')、Tから一石を除いて三石集合 (T') を作る。

禁止集合は四点なので全ての三石集合は安全であり、三石集合のJohnsonグラフは連結である。従って三石層で一石交換を繰り返せば (S') から (T') へ移れ、最後にTの除いた石を戻せる。

ここで三石層の「交換」は一石除去と一石追加を一つの原子的遷移として扱う。この定理を、追加・削除だけを辺とし常に三石以上を保つ通常の再配置グラフへそのまま読み替えてはいけない。K0226に残る一般kでの橋数・長さ・型の一様分類は未解決である。
