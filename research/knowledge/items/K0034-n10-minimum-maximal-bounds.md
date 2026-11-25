---
id: K0034
title: 10×10の最小極大安全サイズはs_10=10
kind: proposition
status: proved
topics:
- maximal-safe
aliases:
- F-AJ
- F-AK
relations:
- type: depends_on
  target: K0033
  note: ''
- type: depends_on
  target: K0038
  note: ''
- type: supersedes
  target: K0145
  note: 九石の有無という問い（K0145）を本命題で解消
artifacts:
- path: research/experiments/original-claims/reports/round56-ten-board-eight-stone-exclusion.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round56_complete_verified.json
  role: data
  note: 接頭部・再開部分・全五分割の接続監査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round59-60-final-ten-board-search.md
  role: source
  note: 九石UNKNOWNと最終境界
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/reports/round49-ten-stone-maximal-counterexample.md
  role: source
  note: 十石極大証人（s_10<=10）
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/n10-nine-stone-sat-20261016/README.md
  role: source
  note: 九石全域排除の完全報告（D4代表15点・95,816,876,802節点・AUDIT PASS）
- path: research/experiments/n10-nine-stone-sat-20261016/output/audit-nine_k9.txt
  role: data
  note: 全487チャンクの連鎖・完全性・found=false の機械監査
- path: research/experiments/n10-nine-stone-sat-20261016/output/manifest_nine_k9.json
  role: manifest
  note: 全チャンクのsha256・ノード数・resume/timeout接頭部
- path: research/experiments/n10-nine-stone-sat-20261016/scripts/nine_stone_exact_search.cpp
  role: solver
  note: 厳密探索（D4第一石還元・辞書式再開・round56共通の枝刈り）
scope: 10×10の極大安全集合の最小サイズ
evidence: complete_enumeration_nine_stone_exclusion_and_ten_stone_witness
---

# 10×10の最小極大安全サイズはs_10=10

**s_10 = 10。** 10×10 の極大安全集合は少なくとも10石必要で、10石で実現する。

- 下限 `s_10 >= 10`: 八石以下の全域排除は round56（初点0..4の五root、D4還元）。九石の全域排除は本実験（research/experiments/n10-nine-stone-sat-20261016）で、D4第一石代表15点 `0 1 2 3 4 11 12 13 14 22 23 24 33 34 44` を完全列挙し **全15代表が `complete:true, found:false`**（487チャンク・95,816,876,802節点・106,626プロセス秒）。チャンク連鎖・resume整合・最終完全性は `output/audit-nine_k9.txt` が機械検査（AUDIT PASS）、全チャンクのハッシュは `output/manifest_nine_k9.json`。
- 上限 `s_10 <= 10`: round49 の十石極大証人。本実験の局所探索が別の十石証人 `13 50 56 59 63 68 77 83 85 98` を再発見し、Python/C++ の独立検証器2本で PASS。

D4 還元: 任意の極大安全集合 S に対し min(S) を代表に写す D4 元が存在し、対称変換は安全性と極大性を保つため、第一石を代表に固定した列挙は各軌道をちょうど1回尽くす。

検証境界:
- 厳密探索は有限完全列挙。round56 k<=8 と同じツールで k=8 を全15代表実行し不在（round56 の別還元と一致）を交差確認した。n=9 k=9 では証人を発見し、両独立検証器で極大安全を確認（葉条件の正例）。
- SAT 符号化（曲線符号化）は n=10 ≤9 で ~8 時間 SAT/UNSAT 未着。結果に影響しない。
- 全 n に対する単調性（K0149）は引き続き未確定。s_1..10 の完全値は 1,3,5,5,5,6,7,8,9,10。
