---
id: K0560
title: 11×11の9石WIN一局面を18個の終局10石WIN子で独立検証
kind: verification
status: verified
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の奇数AND・偶数ORの勝敗伝播
- type: depends_on
  target: K0531
  note: 既存9石WINの一石交換近傍を探索した背景
- type: depends_on
  target: K0105
  note: 局所証明は空盤の未解決性を変えない
artifacts:
- path: research/experiments/n11-s9-terminal-neighbor-20261025/s10-win18.keys
  role: certificate
  note: 全18合法10石WIN子の固定一覧
- path: research/experiments/n11-s9-terminal-neighbor-20261025/s8-win9.keys
  role: certificate
  note: 9個の合法8石WIN親
- path: research/experiments/n11-s9-terminal-neighbor-20261025/verify.py
  role: verifier
  note: 3×3整数幾何と終局までの独立再帰
- path: research/experiments/n11-s9-terminal-neighbor-20261025/reproduce.sh
  role: verifier
  note: 既存4×4整数幾何C++との18葉の勝敗・合法手数照合
scope: 標準11×11、q=4、完全指摘、通常プレイ。9石根00000000040c00011000010a00001000とその8石親9件のみ。元先手固定視点。
evidence: 9石根からの全合法10石子18件を独立整数幾何で再列挙し、18件すべて元先手WINと終局まで再帰検証。独立Pythonの子別探索状態数合計1082（18葉ごとの再検証と4×4整数行列式による独立照合済み）。旧記載1192は誤記で、勝敗証明には使用しない。9石奇数ANDの全子WINから9石WIN、8石偶数ORの9石WIN証人から9個の8石WIN親。凍結8石LOSS294件との衝突0、凍結8石WIN13501件との重複0。保存cacheの勝敗を証明に使わない。空盤UNKNOWN。
---

# 9石局面の終局まで閉じたWIN証明

9石局面 `00000000040c00011000010a00001000` は元先手固定視点でWIN。9石は後手の手番なので手番側LOSSに相当する。

全18個の合法10石子の独立終局再帰により18個すべてが元先手WIN。3×3差分行列式のPython実装と4×4整数行列式のC++検証器を組み合わせて照合する再現手順を保存した。固定9石局面から一石除去した9個の8石親は、それぞれ合法な9石WIN子を持つため元先手WIN。

この局所的な証明は二石root・一石root・空盤の閉鎖を含まない。標準11×11空盤の勝敗はUNKNOWN。


## 2026-10-25 状態数の訂正

初版の探索状態数1192は、現行検証器の再現値と一致せずCIを停止させた。
18葉の手番側WIN判定と合法着手数を別の4×4整数行列式で照合し、
3×3版・4×4版とも探索状態数合計1082（同じ着手順）を確認した。
CIで用いるC++実装は1083状態で、探索順の違いによるもの。
探索状態数は証明の長さでも勝敗値でもない。
葉ごとの18個の探索状態数を検証器の回帰指紋に固定した。
元先手WIN・8石親のWIN・空盤UNKNOWNという結論は変更しない。
