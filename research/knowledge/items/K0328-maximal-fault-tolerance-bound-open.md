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
