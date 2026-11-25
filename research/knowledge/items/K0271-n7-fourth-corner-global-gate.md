---
id: K0271
title: 代表最大A–B間の十二石経路は第四の角を大域的に必ず通る
kind: proposition
status: proved
topics:
- reconfiguration
- maximum-safe
aliases:
- Discovery:fourth-corner-gate
relations:
- type: depends_on
  target: K0001
  note: 代表ゲートと閉包検査は全最大センサスの完全性に依存しない
artifacts:
- path: research/log/discovery-cycles/DISCOVERY_CORNER_GATE_AND_COMPONENTS.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/discovery_full_board_forbid_48.json
  role: certificate
  note: 角禁止の250局面成分
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: results/discovery_corridor_auxiliary.json
  role: data
  note: 全30補助点と鋭い経路
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/structural-discovery/scripts/verify_corridor_discovery.py
  role: verifier
  note: 独立閉包と安全性検査
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 代表最大A–B間の十二石経路は第四の角を大域的に必ず通る

最小交換A–B対の和集合Uは19点で三つの角を含む。残る第四の角vは初期にも終期にもないが、全49点を許したG12経路でも必ず一度占有する。代表v=48=(6,6)、v禁止48点盤のA成分は250局面でBを含まない。

U外30点を一つずつ許す全検査でG12接続に成功するのはv一つだけ。U∪{v}に十二石を保つ十四操作の経路があり補助点数最小1・選択一意。盤面全体の幅は正確に12。角禁止成分の閉包と全域木で不可能性を独立検査。
