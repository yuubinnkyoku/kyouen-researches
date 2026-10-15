---
id: K0426
title: 11盤の終局証明追加は3件のS8 LOSSと一件のS6 LOSSを提示
kind: verification
status: needs-review
topics: [square-outcomes, certificates, verification, search-methods, provenance]
aliases: []
relations:
- type: depends_on
  target: K0371
  note: 元先手固定視点の通常プレイにおける偶奇層の勝敗伝播
- type: supports
  target: K0417
  note: 固定された共同S5計画の要求数に対する追加LOSS証拠として提示
artifacts:
- path: research/experiments/n11-targeted-terminal-lift-20261015/README.md
  role: source
  note: 407件のS10追加検査、終局証明、上位への伝播と信頼境界
- path: research/experiments/n11-targeted-terminal-lift-20261015/SHA256SUMS
  role: manifest
  note: パッケージ内50ファイルのSHA-256一覧
- path: research/experiments/n11-targeted-terminal-lift-20261015/certificates/new_s8_loss_three_terminal.cert
  role: certificate
  note: 3個のS8 LOSS、104個のS9義務と63個の終局S10 LOSS葉
- path: research/experiments/n11-targeted-terminal-lift-20261015/certificates/new_s8_171_terminal.cert
  role: certificate
  note: 171個のS8 WIN終局証明
- path: research/experiments/n11-targeted-terminal-lift-20261015/certificates/new_s8_win_sixteen_terminal.cert
  role: certificate
  note: 追加16個のS8 WIN終局証明
- path: research/experiments/n11-targeted-terminal-lift-20261015/scripts/verify_s8_loss_batch_cpp.cpp
  role: verifier
  note: キャッシュなしで終局まで再計算する独立C++検査器
- path: research/experiments/n11-targeted-terminal-lift-20261015/scripts/verify_s8_loss_batch_python.py
  role: verifier
  note: キャッシュなしで終局まで再計算する独立Python検査器
- path: research/experiments/n11-targeted-terminal-lift-20261015/REPRODUCTION_RECEIPT.txt
  role: log
  note: 提供パッケージの再現実行記録。今回の統合時には再実行していない
- path: research/experiments/n11-s6-terminal-loss-20261015/s6-loss-optimized.cert
  role: certificate
  note: 一つのS6 LOSSを29個のS8 LOSS証人と483個の終局S10葉で証明する証明書
- path: research/experiments/n11-s6-terminal-loss-20261015/verify_s6_terminal.py
  role: verifier
  note: S6証明境界と全S10葉をキャッシュなしで検査
- path: research/experiments/n11-s6-terminal-loss-20261015/audit_joint_plan.py
  role: verifier
  note: 六つのS5 LOSS親と固定共同計画の重なりを再計算
scope: 標準11×11・q=4・完全指摘・通常プレイ。勝敗ラベルは元先手固定視点。提供された終局証明と派生するS5親のみに限定し、空盤面や二石rootは対象外。
evidence: 添付パッケージは3 S8 LOSS（104 S9義務、63終局S10葉、85,676メモ化状態）、171+16 S8 WIN、および一つのS6 LOSS（49 S7子、29 S8証人、1,046 S8→S9義務、483終局S10葉、1,028,621状態）を報告する。SHA256一覧と単独S8証明書のハッシュは入力完全性として照合したが、各ゲーム検査器はこの統合では実行していない。
---

証明資料の取り込みを記録する項目であり、添付READMEの再現receiptを独立監査済み結果として扱わない。したがって本項目は `needs-review` とする。

提供内容が正しければ、3つのS8 LOSSから19個の新規S7 LOSS親が導かれ、6石局面 `00000000040004001004000004010000` のS6 LOSS証明は6個の異なるS5 LOSS親を与える。後者のうち3個は固定されたK0417共同計画のS4クラス16397に現れ、添付監査はその計画を保った場合の楽観的未確定S5和集合が31,774から31,771へ減ると報告する。この条件付き更新は未監査のため、K0417の確定済み31,774基準値はこの項目だけでは変更しない。

両パッケージとも新しい二石rootを閉じていない。標準11×11空盤面の勝者は引き続きUNKNOWN。S10既存51,164件の全独立再検査や、C++のみの2,229候補の昇格も主張しない。
