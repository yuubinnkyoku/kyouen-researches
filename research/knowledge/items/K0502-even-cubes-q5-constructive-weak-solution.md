---
id: K0502
title: 3次元5点禁止版の全偶数辺立方盤は鏡映応手で後手必勝
kind: proposition
status: proved
topics: [variants, grundy, first-moves]
aliases: []
relations:
- type: generalizes
  target: K0304
  note: 円・直線の鏡映証明を3次元の平面・球面へ適用
- type: depends_on
  target: K0337
  note: 鏡像二点を含む禁止ブロックの鏡映不変性という十分条件
artifacts:
- path: research/experiments/cube-q5-weak-20261022/README.md
  role: proof
  note: 全偶数辺長と偶数辺を持つ直方格子の構成的鏡映証明
- path: research/experiments/cube-q5-weak-20261022/reflection.py
  role: source
  note: 任意の正の辺長に対応する鏡映応手関数
- path: research/experiments/cube-q5-weak-20261022/audit_reflection.cpp
  role: verifier
  note: 64点までの全対称安全局面と全合法鏡映応手の整数検査
- path: research/experiments/cube-q5-weak-20261022/verify_reflection.py
  role: verifier
  note: 別方式の直接4×4行列式による独立対称局面・応手検査
- path: research/experiments/cube-q5-weak-20261022/reflection-4.json
  role: data
  note: 4×4×4の529対称安全局面・2048合法応手・496終端
- path: research/experiments/cube-q5-weak-20261022/reflection-4-independent.json
  role: data
  note: 独立Python行列式検査による全局面・応手・終端頻度の一致
scope: 共平面または共球面5点禁止・通常プレイ、全偶数n≥2のn×n×nと少なくとも一辺が偶数の直方格子
evidence: 幾何学的な鏡映応手の合法性と有限性による全称証明
solution:
  board: n×n×n・3次元q=5・偶数n≥4
  level: weak
  outcome: second-player-win
  classification: [root, first-moves]
  coverage: 全偶数n≥4・全初手n³個への合法な必勝応手
  conditions: 5点共平面または共球面禁止・完全指摘・通常プレイ
  verification: [mathematical-proof, independent-enumeration]
  certificate: τ(x,y,z)=(n−1−x,y,z)による構成的戦略証明
  independent_check: 4×4×4の529対称安全局面と2048合法応手を余因子法と直接行列式の別実装で照合
  note: 4×4×4、6×6×6以降の全偶数辺長。奇数辺長はこの定理の対象外
---

全偶数nについて、相手の着手 `(x,y,z)` に `(n−1−x,y,z)` を返す後手戦略が
必ず合法で勝つ。特に4×4×4は後手必勝であり、6×6×6、8×8×8以降も同様。
同じ座標鏡映が使える全直方格子（少なくとも一辺が偶数）にも成立する。

鏡像二点を含む平面・球面は鏡映不変である。直前の対称安全局面とその曲面の
交わりは偶数個なので、相手の合法手に鏡像応手を追加して初めて5点に達する
ことはない。応手後も安全・対称であり、有限性から後手必勝になる。
証明全文と実行可能な戦略はartifactを参照。

この戦略は必ず合計4手で終局する。二つの鏡像対の4点は同一円または同一直線に
乗り、どの5点目も共球面または共平面5点を作るからである。
4×4×4では529対称安全局面（0石1、2石32、4石496）、全2,048応手を
独立整数実装で照合済みであり、全496終局は4石である。

既存2026-10-16実験の高次元鏡映定理の帰結を明示的な弱解決として登録した。
新しい全局面Grundy列挙ではなく、奇数辺立方盤、非対称局面の強解決、
または円だけを禁止する別ルールには結論を拡張しない。5×5×5以降の奇数辺は
別途の証明・探索を必要とする。
