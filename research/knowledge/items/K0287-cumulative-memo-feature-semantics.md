---
id: K0287
title: multi-state probeの累積memoは候補独立特徴でない
kind: method
status: active
topics:
- search-methods
- provenance
aliases: []
relations:
- type: verifies
  target: K0086
  note: 元改善主張の撤回を要する測定欠陥を監査
artifacts:
- path: docs/MOVE_ORDERING_AUDIT.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/audit_blind_probe.py
  role: verifier
  note: 累積値と入力順の照合
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/10x10/blind-probe-audit.json
  role: data
  note: 160行の順位決定性
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# multi-state probeの累積memoは候補独立特徴でない

旧multi-state経路はbatch20候補につき一Solverを保持し、候補ごとのvisitedは再初期化するがmemoは消去しない。memo_usedとsecondsは累積、visited・maxdepth・depth visitedは候補単位。全batch0八親160行でmemo-desc順位が入力順の完全逆になった。

候補ごとfresh processのLOPO特徴はこのバグの対象外。visited−memoもhit数ではない（hitはvisitedを増やさず、memoized depthが限定される）。測定counterの意味を費用・予測説明と混同しない。
