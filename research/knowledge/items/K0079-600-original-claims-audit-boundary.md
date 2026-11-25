---
id: K0079
title: 600原文の監査状態と弱化版作業ラベルは別の量
kind: verification
status: verified
topics:
- migration
- provenance
aliases: []
relations: []
artifacts:
- path: research/experiments/original-claims/reports/round26-original-scope-index.md
  role: source
  note: 命題・対象範囲・根拠を記した出典
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/experiments/original-claims/output/round26_original_scope_index.json
  role: manifest
  note: 全600原文と採用範囲・根拠ポインタ
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
- path: research/archive/claim-audit-history/HANDOFF-2026-10-01-round61.md
  role: source
  note: 最終原文状態と残件
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
---

# 600原文の監査状態と弱化版作業ラベルは別の量

原文監査索引は600原文を保持する。現在の件数はartifactの生成索引・JSONを正本とし、165件時点の移行件数を現状として使わない。NOT_AUDITEDは内容監査が未実施という状態で、数学的未解決の件数ではない。旧「600/600決着」には有限・弱化版の昇格が含まれ原文全量化の決着を意味しない。

古いSUPPORTEDを無界定理へ機械昇格しない。原文・前提・採用範囲・preferred reportと個別理由を既存生成器のREVIEWEDと索引に保持する。監査済みでも重複・途中メモ・弱い有限傍証だけなら独立Kやaliasは不要。INCONCLUSIVEとSCOPE_UNCLEARも内容を確認した監査済み状態であり、一般命題が解けたこととは区別する。

2026-10-04に全600件の内容監査を完了し、NOT_AUDITED=0となった。全量化が真偽決着したという旧600/600の意味ではなく、各原文がSUPPORTED/REFUTED/PARTIAL/INCONCLUSIVE/SCOPE_UNCLEARの監査済み状態になったという意味である。生きた集計と個別根拠は生成索引を参照する。
