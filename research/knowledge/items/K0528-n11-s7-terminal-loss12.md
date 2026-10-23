---
id: K0528
title: 標準11×11の未分類7石局面を12個の終局LOSS葉で独立証明
kind: verification
status: verified
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の奇数AND・偶数OR伝播
- type: depends_on
  target: K0371
  note: LOSSからの誤った上位WIN伝播を排除
- type: depends_on
  target: K0516
  note: 既存68個の9石WIN根の終局証明
artifacts:
- path: research/experiments/n11-s7-terminal-loss12-20261024/certificate.json
  role: certificate
  note: 18新規9石WIN・3個の8石LOSS・39葉被覆・12葉最小被覆・双対重み
- path: research/experiments/n11-s7-terminal-loss12-20261024/verify.py
  role: verifier
  note: 全合法境界、固定先手極性、双対下界、C++/Python照合
- path: research/experiments/n11-s7-terminal-loss12-20261024/verify_s10_cpp.cpp
  role: verifier
  note: 独立4×4整数行列式による終局minimax
- path: research/experiments/n11-s7-terminal-loss12-20261024/README.md
  role: source
  note: 再現手順と信頼境界
scope: 標準11×11・q=4・完全指摘・通常プレイ・元先手固定視点。指定7石局面のみ。空盤は含まない。
evidence: 指定7石の全36合法8石子は独立終局証明でWIN33・LOSS3。18個の新規9石WIN根が23個の新規8石WIN子を支え、3個の8石LOSSの全74相異なる9石義務を39個の10石LOSS葉が被覆。1個の8石LOSSは22義務を12葉で被覆し、181候補の終局再計算と半整数双対下界11.5で同形式の最小性を独立検証。C++4×4とPython3点整数円方程式で1,963個の10石葉の勝敗・合法手数・個別状態数が一致（WIN1,887/LOSS76、合計396,636状態）。元先手固定7石ANDはLOSS。6石WINや二石root、空盤勝敗は導出しない。
---

# 7石局面 `00000000100000021081000020000020` はLOSS

全36個の合法8石子の勝敗を、元先手固定視点でWIN33件・LOSS3件と独立終局まで検証した。奇数石AND局面である7石にはLOSS子が存在するため、7石も**LOSS**。

最短の局所証明は、8石LOSS `00000000100000021081004020000020` と、その22個の9石子を覆う12個の10石LOSS葉。全181個の候補を分類し、半整数双対で11葉以下を排除した。最小性はこの局所的な葉形式に限る。

再現は `research/experiments/n11-s7-terminal-loss12-20261024/reproduce.sh`。旧cache勝敗を前提としない。**標準11×11空盤の勝敗はUNKNOWN**。
