---
id: K0109
title: 7〜9×9公開証明書のLOSS比34〜35%は三サイズの観測
kind: proposition
status: observed
topics:
- certificates
- statistics
aliases:
- F-C
- H5
relations: []
artifacts:
- path: research/archive/hypothesis-ledgers/findings.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: scripts/analysis/cert_loss_ratio.py
  role: verifier
  note: 公開証明書のノード比計数
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 7〜9×9公開証明書のLOSS比34〜35%は三サイズの観測

指定KYOENC3証明書でLOSS比は7×7=35.4%、8×8=34.2%、9×9=34.4%。DAGの選択戦略・対称性合流に依存するノード統計で、全安全局面のP比でも全nに不変な定理でもない。

F-Cの見出しの「盤面サイズに依存しない」はこの有限範囲に限定する。層別WIN/LOSS奇偶分離は保存構造の性質。

旧H5はこれを「比率一定なので非単調説を反証」としたが、三値は一致せず実際に非単調。一般のサイズ非依存も非単調性も三標本だけでは決着しない。
