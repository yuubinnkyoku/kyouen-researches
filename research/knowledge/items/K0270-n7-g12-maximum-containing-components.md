---
id: K0270
title: 7×7のG12で最大配置を含む成分は八個・各903局面
kind: proposition
status: proved
topics:
- maximum-safe
- reconfiguration
aliases:
- Discovery:G12-max-components
relations:
- type: depends_on
  target: K0051
  note: ''
- type: depends_on
  target: K0266
  note: ''
artifacts:
- path: night-research/DISCOVERY_CORNER_GATE_AND_COMPONENTS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/discovery_full_board_forbid_-1.json
  role: certificate
  note: 903局面の全盤成分
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/discovery_corridor_verification.json
  role: log
  note: 閉包・全域木・hash検査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: night-research/verify_corridor_discovery.py
  role: verifier
  note: 探索実装をimportしない独立整数検査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 7×7のG12で最大配置を含む成分は八個・各903局面

全49点上の安全配置を一石追加/削除し石数≥12を保つG12では、全16最大配置は二つずつ八成分。各成分は十二石817・十三石84・十四石2、合計903局面。同じ成分の最大対は最小5点交換のA–Bペア。

Leibniz整数detを別実装で再生成し、集合の隣接閉包と根からの全域木を検査。D4像は互いに交わらず全最大16を覆う。最大配置を含まないG12成分の完全分類は主張しない。
