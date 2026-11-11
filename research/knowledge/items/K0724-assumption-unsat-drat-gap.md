---
id: K0724
title: 候補B の assumption-UNSAT を単体の DRAT 証明へ落とす手続きは未取得である
kind: question
status: open
topics: [maximum-safe, search-methods, certificates]
aliases: []
relations:
- type: depends_on
  target: K0718
  note: 前提(4) の所在
- type: depends_on
  target: K0706
  note: DRAT 監査の実施例
artifacts:
- path: research/log/2026-11-10-a2647-113-candidate-b-proof-omp.md
  role: log
  note: 第2部の証明書計画（候補A、d 固定 CNF + DRAT）
- path: research/log/2026-11-10-a2647-113-hardcore-attack-plan-omp.md
  role: log
  note: 候補A 予算ラダーの計画
scope: 候補B（assumption 掃引）の UNSAT 主張の監査可能性に関する未解決の問い。
evidence: W10 §1.7 前提(4)・§2.1 が「未取得」と明記。2026-11-10 時点で新しい計算は無い。
---

## 問い

`solve_limited(assumptions=[B_d])` の UNSAT は `CNF ∧ B_d` の UNSAT を意味するが、
現行の掃引記録は assumption を単位節として書き出していないため、
単体の DRAT 証明に対応しない。

d 固定 CNF（または B_d を加えた CNF）を書き出して DRAT を取り、独立チェッカで
検査する手続きを、クラス (1,1,3) の未決着範囲を増やさずに適用できるか。
候補A 方式（三値・固定 d、K0712/K0723）と候補B 方式の費用対効果は未測定である。

## 現状

- 前提(1)(2) は証明で閉じ（K0720/K0719）、前提(3) は範囲限定で検証済み（K0721）。
  符号化側で残る外挿は (3) の一般 n のみ。
- ソルバ側の前提(4) は本項のみが未解決で、候補B の UNSAT 主張
  （K0717 の掃引 67 件を含む）を DRAT 監査済みに引き上げる唯一の経路が候補A 化である。
