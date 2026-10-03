---
id: K0165
title: n≥4の最小勝敗保持禁止族に共通必須D4型があるというB258は偽
kind: proposition
status: refuted
topics:
- variants
aliases:
- B258
relations: []
artifacts:
- path: research/verification/round23-b256-symmetric-minimum.md
  role: source
  note: n≥4で共通必須D4型が存在しない一般構成
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/round23_minimum_family_verified.json
  role: data
  note: n=2..20の補助検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/verification/scripts/round23_minimum_family.py
  role: verifier
  note: D4型と商ゲームの検算
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/hypothesis-bank-2026-09-27.md
  role: source
  note: B258の原文
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# n≥4の最小勝敗保持禁止族に共通必須D4型があるというB258は偽

盤点を固定し、禁止四点族だけを部分族へ減らすゲームを考える。標準版と同じ空盤勝者を与える最小非空部分族について、n≥4で全ての最小族に共通するD4四点型は存在しない。

自由盤と標準版の勝者が異なる場合、任意の一四点組だけを禁止した族が最小であり、D4非同値な四点型を選べる。勝者が同じ場合、非空最小族のサイズは2で、1×1正方形型二組だけからなる族と2×1長方形型二組だけからなる族を構成でき、両者に共通するD4型はない。これは勝者の具体値に依存しない一般証明である。

n=2では唯一の四点組しかなく「共通必須型」が自明に存在するが、これは小盤の退化例であり、n≥4の一般主張を救わない。B258の研究上意味のある全n≥4読みは反証済みとする。
