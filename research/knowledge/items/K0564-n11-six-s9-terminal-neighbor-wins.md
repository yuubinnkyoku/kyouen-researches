---
id: K0564
title: 11×11の9石近傍6根を106個の終局10石子で独立検証
kind: verification
status: verified
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の奇数AND・偶数OR伝播
- type: depends_on
  target: K0560
  note: 一石交換近傍を作った先行9石WIN根
- type: depends_on
  target: K0562
  note: 一石交換近傍を作った第二の9石WIN根
- type: depends_on
  target: K0105
  note: 局所終局証明は空盤勝敗を確定しない
artifacts:
- path: research/experiments/n11-batch-s9-terminal-20261025/s9-roots.keys
  role: certificate
  note: 9石AND根6件のD4正準形
- path: research/experiments/n11-batch-s9-terminal-20261025/s10-win.keys
  role: certificate
  note: 6根の全合法10石子106件のD4正準形
- path: research/experiments/n11-batch-s9-terminal-20261025/s8-win.keys
  role: certificate
  note: 逆向きに得た8石WIN親54類
- path: research/experiments/n11-batch-s9-terminal-20261025/verify.py
  role: verifier
  note: 独立4×4整数行列式Bareiss法と終局再帰
- path: research/experiments/n11-batch-s9-terminal-20261025/verify_3x3.py
  role: verifier
  note: 別実装3×3差分行列式との照合
- path: research/experiments/n11-batch-s9-terminal-20261025/reproduce.sh
  role: verifier
  note: 既存C++4×4整数幾何との106葉照合手順
scope: 標準11×11、q=4、完全指摘、通常プレイ。指定9石根6件と8石親54類のみ。元先手固定視点。
evidence: 9石根6件の全合法10石子は相異なる106類。独立4×4 Bareiss整数幾何と別実装3×3差分行列式の終局再帰で106件すべて元先手WIN、葉別探索状態数合計12604が一致。9石奇数ANDの全子WINから6根WIN、8石偶数ORの9石WIN証人から54親WIN。凍結9石WIN1611件・凍結8石WIN13501件に未収録、凍結8石LOSS294件との衝突0。先行2根との局所8石親純増48件、研究全体の純増は未集計。空盤UNKNOWN。
---

# 9石6根と8石親54類の終局まで閉じたWIN証明

9石6根の全合法10石子106件を独立整数幾何で再列挙し、全106件を終局まで再帰検証した。元先手固定視点で10石子はすべてWINなので、9石6根は元先手WIN（手番側LOSS）。その9石根へ合法着手できる8石親54類も元先手WIN。

4×4整数行列式（Bareiss法）と3×3差分行列式の別実装で葉の勝敗と状態数合計12,604が一致した。C++4×4整数行列式との再現スクリプトは保存済みだが、初回作業時点では未実行。凍結WIN/LOSS表は重複・衝突比較のみに用い、勝敗証明に使用していない。

二石rootの新規閉鎖は0件。標準11×11空盤の勝敗はUNKNOWN。
