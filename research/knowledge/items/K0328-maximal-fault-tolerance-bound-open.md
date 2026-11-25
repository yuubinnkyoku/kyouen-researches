---
id: K0328
title: n≥2の標準盤の全極大配置で故障耐性ρは一様有界か
kind: question
status: open
topics: [maximal-safe, geometry]
aliases: [B363]
relations:
- type: depends_on
  target: K0026
  note: 標準盤の安全極大配置
artifacts:
- path: research/experiments/original-claims/reports/round29-fault-witness-audit.md
  role: source
  note: 正確なρ2の5×5証人
- path: research/experiments/original-claims/reports/round70-b301-b400-original-scope-audit.md
  role: source
  note: 無界族・上界3候補・n1端点と有限カタログの区別
---

# n≥2の標準盤の全極大配置で故障耐性ρは一様有界か

ρ(S)は安全極大Sから石を除き、元から空だった点を一つでも合法に戻す最小除去数。削除場所への再着手を数えない。n≥2の標準n×nで全安全極大Sにρ(S)≤Cを保証する絶対定数Cがあるか。ρは有限整数なので、否定は任意rのρ≥r構成となる。

n1は元の空点がなくρ未定義なので対象から明示的に除外する。n≥2では全盤占有は安全でなく、安全極大には空点がある。全石除去で空点を合法に戻せるのでρは定義される。

現在の正確な5×5証人はρ2。小盤の全極大、n7の最大16、n8の八石極大408でρ≥3の証人はない。n7/n8のこれら有限族は全極大族ではない。上界3候補B364に一般証明はなく、一様上界も無界構成も未解決。全最小極大だけのρ1問題K0298とは別問題である。

## 2026-10-17 bounded advance

New finite evidence: exact fault-tolerance rho computed for all maximal sets n=2..6 (4,56,928,16860,349596 sets), 16 maximum 14-stone sets n=7, 408 eight-stone maximal sets n=8, and selected saturation witnesses (11x11 10-stone rho=1, 10x10 19-stone T rho=2, U\{25} rho=1). No rho>=3 in any tested family; max observed rho=2.

Scope clarification: 7x7 covers only maximum-size maximals; 8x8 covers only 8-stone family; 9x9+ not exhaustively enumerated. Arbitrary integer boards can have unbounded rho (K0346/K0348) but use selected point sets, not full grids.

Next steps: exhaustive enumeration for 7x7+ all maximals and 9x9+; prove or refute uniform bound on square boards. Status remains open.

## 2026-10-17 bounded advance (round 2)

New finite evidence: rho (minimum removals to make an originally empty point legal) computed for 155,167 maximal safe sets. 7x7: 16 max 14-stone (all rho=2), 1,952 13-stone (1,384 rho=1, 568 rho=2), 152,776 12-stone (149,008 rho=1, 3,768 rho=2); total 154,744, rho>=3: 0. 8x8: 408 complete 8-stone minimum maximals (all rho=1), 15 15-stone witnesses (10 rho=1, 5 rho=2); total 423, rho>=3: 0. Combined: rho=1 150,810, rho=2 4,357, rho>=3 0; max observed rho=2.

Scope clarification: evidence consistent with C=2 on tested families only. Coverage gaps: 7x7 maximals of sizes 7-11 not enumerated; 8x8 maximals of sizes 9-14 not enumerated. Arbitrary integer boards can have unbounded rho (K0346/K0348); full square boards only.

Next steps: enumerate missing maximal sizes or find general proof. Status remains open.

統合監査（2026-10-20）: 上記2026-10-17の追記はローカル研究時点の報告であり、今回すべての探索・測定を再実行したものではない。再検証の範囲は `research/experiments/local-main-integration-20261020/README.md` に記す。既存の未解決性・量化の限界を維持する。
