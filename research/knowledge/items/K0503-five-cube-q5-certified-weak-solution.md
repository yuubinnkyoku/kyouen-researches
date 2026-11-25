---
id: K0503
title: 5×5×5の3次元5点禁止版は全125初手を覆う独立検査済み証明書で後手必勝
kind: proposition
status: computed
topics: [variants, first-moves, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常プレイのP/N再帰と有限局面のAND/OR帰納法
- type: generalizes
  target: K0435
  note: 同じ共平面・共球面5点禁止版の有限弱解決を5×5×5へ拡張。Lean形式検査ではない
artifacts:
- path: research/experiments/cube-q5-weak-20261022/README.md
  role: proof
  note: 5×5×5のルール・座標・証明書形式・全初手被覆・再現手順
- path: research/experiments/cube-q5-weak-20261022/solve.cpp
  role: solver
  note: 128bit・48対称性・exact P/N探索と証明書抽出・空盤への統合
- path: research/experiments/cube-q5-weak-20261022/verify_certificate.cpp
  role: verifier
  note: 探索器を呼ばずBareiss 5×5整数行列式で証明書の全AND/OR境界を独立検査
- path: research/experiments/cube-q5-weak-20261022/empty-5.cert.gz
  role: certificate
  note: 空盤Pの1368687局面証明書。gzip展開後に独立検査する
- path: research/experiments/cube-q5-weak-20261022/verified-5.json
  role: data
  note: 空盤P・1655414辺・443783終端・全局面到達性の独立検査結果
- path: research/experiments/cube-q5-weak-20261022/manifest-5.json
  role: manifest
  note: ソース・実行結果・圧縮証明書・展開後証明書のSHA-256
- path: research/experiments/cube-q5-weak-20261022/search-5.jsonl
  role: data
  note: 6個の2石P根・合計13325226展開・19777673確定memo
- path: research/experiments/cube-q5-weak-20261022/play.py
  role: source
  note: 圧縮証明書に収録された局面から実盤上の必勝応手を取り出す
- path: research/experiments/cube-q5-weak-20261022/regression.json
  role: data
  note: 既知3×3×3の全20二石軌道・空盤・偽証明書拒否・予算0のUNKNOWNを検査
scope: 5×5×5整数格子・共平面または共球面5点禁止・完全指摘・通常プレイ、空盤および全125初手
evidence: 48対称性で圧縮した1368687局面のAND/OR証明書を独立整数幾何で検査
solution:
  board: 5×5×5・3次元q=5
  level: weak
  outcome: second-player-win
  classification: [root, first-moves]
  coverage: 空盤・125/125初手（10軌道）への必勝応手
  conditions: 5点共平面または共球面禁止・完全指摘・通常プレイ
  verification: [exact-search, ranked-and-or-certificate, independent-cpp-check]
  certificate: empty-5.cert.gz・1368687局面・1655414関係・最大12石
  independent_check: Bareiss 5×5整数行列式で合法手・全P境界・N証人・全収録局面の到達性を確認
  note: 全初手後は次手番側N。任意の非収録局面・全Grundy・7以上の奇数辺長は対象外
---

5×5×5の3次元5点禁止ゲームの空盤はP、すなわち後手必勝である。
点 `(x,y,z)` の番号を `(x*5+y)*5+z` とする。次の6個の2石根がPであることを
厳密探索し、立方体の48対称性で全初手10軌道を覆った。

`{0,3}`, `{2,17}`, `{6,7}`, `{31,32}`, `{62,37}`, `{12,112}`。

各P根のAND/OR証明書を統合し、初手後の10個のN局面と空盤Pを加えた。
重複を統合して根から到達不能な記録を落とした結果は1,368,687局面、
1,655,414関係、443,783終局。石数は0〜12。P局面の全合法子はN、
N局面の少なくとも一つの合法子はPであり、石数の単調増加から帰納的に正しい。

探索器は4点の持ち上げ差分行列から余因子で禁止追加点を計算する。
独立検査器は5×5整数行列式をBareiss法で再生成し、6億792万2,271回の
行列式評価で全合法境界と応手を再検査した。全収録局面が根から合法辺で
到達することも検査した。証明書を盲信する外部葉やUNKNOWNの採用はない。

3×3×3の既知全20二石軌道のP判定と空盤を回帰確認し、欠損・重複・誤ラベル・
不完全行・盤外点などの不正証明書を拒否することも確認した。
予算切れはUNKNOWNとして扱う。

限界: これは有限盤の弱解決と全初手の判定であり、全安全局面の強解決や
Grundy値の計算ではない。証明書の最大12石は戦略内の上限であり、盤全体の
最大安全石数ではない。Leanによる形式化はしていない。7×7×7以降の奇数辺長の
結論は含まない。共円だけを禁止する別ルールとも区別する。
