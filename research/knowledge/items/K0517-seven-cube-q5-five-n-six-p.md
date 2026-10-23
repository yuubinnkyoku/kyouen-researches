---
id: K0517
title: 7立方5点禁止版の五石局面{0,2,5,26,69}はN、54着手後はP
kind: verification
status: verified
topics: [variants, certificates, verification, search-methods]
aliases: []
relations:
- type: supports
  target: K0505
  note: 未処理第三手69の下の五石Nを閉じた部分証明。上位根の勝敗証明ではない
artifacts:
- path: research/experiments/cube-q5-seven-balanced-20261023/five-results.md
  role: proof
  note: 五石Nと六石Pの意味・勝ち手・独立検査・再現方法と限界
- path: research/experiments/cube-q5-seven-balanced-20261023/five-n.cert.gz
  role: certificate
  note: 五石Nの431195局面・580676辺証明書
- path: research/experiments/cube-q5-seven-balanced-20261023/six-p.cert.gz
  role: certificate
  note: 六石Pの431194局面・580675辺証明書
- path: research/experiments/cube-q5-seven-balanced-20261023/verify_incremental.cpp
  role: verifier
  note: 探索器とは別実装のBareiss5×5行列式・差分合法子検査器
- path: research/experiments/cube-q5-seven-balanced-20261023/five-n-incremental-verified.json
  role: data
  note: 五石Nの全証明書を325137492回の整数行列式評価で独立検査
- path: research/experiments/cube-q5-seven-balanced-20261023/six-p-incremental-verified.json
  role: data
  note: 六石Pの全証明書の独立検査結果
scope: 7×7×7整数格子、共平面または共球面5点禁止・通常プレイ、明示した五石根と六石根
evidence: private checkpointを既知葉にせず全AND/OR条件・安全性・到達性を独立Bareiss検査
---

番号を`(x*7+y)*7+z`とする。五石局面 `{0,2,5,26,69}` はNであり、手番側は
54（座標(1,0,5)）へ着手してP局面 `{0,2,5,26,54,69}` に進める。
証明書の正規化済み根はそれぞれ `{7,10,28,42,51}` と `{7,10,28,42,51,56}`。

五石証明は431,195局面・580,676辺。六石証明は根1局面・証人辺1本を除いたもの。
最大16石までを含み、97,269終端を使う。探索器の幾何と異なる整数Bareiss検査で、
全Pの全合法子とNのP証人、根の安全性、正規化、全行の到達性を確認した。
再開用の数千万候補ラベルを独立に全検査したという意味ではない。

この五石根はK0505の未処理第三手69の子孫。三石根・二石根・空盤は引き続き
未確定であり、7立方の弱解決や強解決ではない。
