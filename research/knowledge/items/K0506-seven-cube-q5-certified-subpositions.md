---
id: K0506
title: 7立方5点禁止版の6石N・7石Pと17石極大安全局面を独立証明書で確認
kind: verification
status: verified
topics: [variants, certificates, verification, maximal-safe, maximum-safe]
aliases: []
relations:
- type: supports
  target: K0505
  note: 7立方の有限部分証明と再開可能な探索境界を提供。空盤の勝敗証明ではない
artifacts:
- path: research/experiments/cube-q5-seven-frontier-20261022/README.md
  role: proof
  note: 座標、有限部分証明の意味、独立検査、17石構成、探索の信頼境界
- path: research/experiments/cube-q5-seven-frontier-20261022/verify.cpp
  role: verifier
  note: 6ワードQ5CUBE2・Bareiss整数幾何・全AND/OR条件の独立検査器
- path: research/experiments/cube-q5-seven-frontier-20261022/six-n.cert.gz
  role: certificate
  note: 6石N局面の8314局面・10705辺証明書
- path: research/experiments/cube-q5-seven-frontier-20261022/seven-p.cert.gz
  role: certificate
  note: 7石P局面の8313局面・10704辺証明書
- path: research/experiments/cube-q5-seven-frontier-20261022/terminal17.cert.gz
  role: certificate
  note: 安全かつ合法追加点0の17石局面1件
- path: research/experiments/cube-q5-seven-frontier-20261022/six-n-verified.json
  role: data
  note: 6石Nの独立検査結果
- path: research/experiments/cube-q5-seven-frontier-20261022/seven-p-verified.json
  role: data
  note: 7石Pの独立検査結果
- path: research/experiments/cube-q5-seven-frontier-20261022/terminal17-verified.json
  role: data
  note: 17石極大安全集合の独立検査結果
- path: research/experiments/cube-q5-seven-frontier-20261022/manifest.json
  role: manifest
  note: ソース・結果・圧縮前後の証明書・private checkpointのhashと保存範囲
scope: 7×7×7整数格子、共平面または共球面5点禁止・通常プレイ、明示した3占有集合
evidence: 探索器と別実装の5×5 Bareiss整数行列式による全局所条件と到達性の検査
---

点 `(x,y,z)` の番号を `(x*7+y)*7+z` とする。次の有限3件を独立検査した。

* `{1,4,6,22,55,63}` はN（手番側勝ち）。着手57で次のP局面に移れる。
* `{1,4,6,22,55,57,63}` はP（手番側負け）。証明書8,313局面・10,704関係。
* `{5,7,9,42,56,68,78,169,178,187,196,220,239,243,247,258,275}` は
  17石の極大安全局面であり、P終端である。

最初の6石Nの証明は7石Pの証明に根1局面・証人辺1本を加えた8,314局面。
両証明の最大石数は15。最初の6石根は立方体対称性で
`{0,2,5,26,49,69}` に写せるため、K0505の未処理第三手69の下の部分木に属する。
三石根69、二石根 `{0,5}`、空盤のどれも、この部分証明だけでは判定できない。

17石構成は安全性と全追加候補の違法性を806,820回の整数行列式評価で検査した。
従って7立方の最大安全石数は少なくとも17である。最大値17や全極大集合の分類は
主張しない。奇数石の極大安全局面の存在も確認できる。

独立検査器はcheckpointや探索器の結論を既知葉として使わず、証明書の根の安全性、
全P局面の全合法子、N局面の合法なP証人、正規化、全記録の根からの到達性を確認する。
各6石/7石証明で161,740,290回の5×5 Bareiss行列式評価を行った。
有限性と石数の厳密増加による帰納法で各ラベルが正しい。

限界: 7立方の弱解決・全局面の強解決・全Grundy計算ではない。Lean形式検査も
行っていない。探索中の数百万の確定候補memo全体を独立検査したわけではない。
