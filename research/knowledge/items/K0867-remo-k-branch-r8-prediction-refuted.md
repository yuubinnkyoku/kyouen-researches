---
id: K0867
title: r=8 REMO 3枝の4/10族非坍縮予想を対象族の完全検査で反証
kind: proposition
status: refuted
topics: [variants, multiplayer, maximal-safe, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0866
  note: K0866からのr=8外挿予想だけを対象にする。r=7定理Iは維持される
- type: depends_on
  target: K0861
  note: 定理E′の領域ゲーム正確性により、プロファイル結果は全ての実現盤面に及ぶ
artifacts:
- path: research/experiments/remo-k-branch-r8-target-refutation-20261116/report.md
  role: proof
  note: r=8の対象2族・γ=0..3の有限完全反証、範囲と限界
- path: research/experiments/remo-k-branch-r8-target-refutation-20261116/verify_r8_target.py
  role: verifier
  note: K0866領域エンジンをGit blob SHAで固定し、独立生存者ビット集合再帰と全照合
- path: research/experiments/remo-k-branch-r8-target-refutation-20261116/output/audit.json
  role: data
  note: 140プロファイル・8鎖・r=7陽性対照127プロファイルの決定論的監査
scope: >-
  3枝REMO領域ゲーム、枝サイズ上限10、r=8における枝サイズ(4,4,10)と
  (4,10,10)、共通核γ=0..2の非坍縮族予想を対象とする。γ=3も対照として
  検査する。各対象キーの全正準原子プロファイルを含むが、r=8の全715キー
  や枝サイズ11以上は含まない。
evidence: >-
  固定枝サイズと共通核を保つ二枝専用原子(a12,a13,a23)を全列挙し、
  単独原子を差分で一意に決定してS3正準化する。対象140プロファイルと
  8鎖プロファイルを、K0866領域ゲーム再帰と独立した生存者ビット集合再帰で
  照合し、不一致・予算打切り0。全プロファイルと鎖の可能生存者集合は{P_3,P_7}（検証器の0始まり番号3,7）、
  決定プロファイルは0。r=7陽性対照127プロファイルでは既知の決定数
  (16/20,7/10,2/4; 39/45,22/28,7/13)を再現した。従ってK0866の
  r=8対象族予想は有限完全範囲で反証されるが、r=8全境界は未決定。
---
# r=8の4/10族非坍縮予想の反証

K0866はr=6の4/8族、r=7の4/9族から、r=8では4/10族
(4,4,10),(4,10,10)×γ=0..2が非坍縮になると予想した。
しかし対象キーの全プロファイルでチェーンと同じ非決定状態になった。
この有限予想は反証された。

詳細な数値・二方式の検証・適用範囲は
[実験報告](../../experiments/remo-k-branch-r8-target-refutation-20261116/report.md)、
[検証器](../../experiments/remo-k-branch-r8-target-refutation-20261116/verify_r8_target.py)、
[監査JSON](../../experiments/remo-k-branch-r8-target-refutation-20261116/output/audit.json)
を参照。
