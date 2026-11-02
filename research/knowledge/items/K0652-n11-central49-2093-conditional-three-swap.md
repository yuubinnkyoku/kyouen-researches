---
id: K0652
title: 11×11中央49の条件付き七石義務を三証人交換で2,094類から2,093類へ削減
kind: computation
status: superseded
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0650
  note: 46証人・2,094類の出発点と二度の三証人交換
- type: depends_on
  target: K0651
  note: 二証人以下では改善できないという厳密な局所最適性
- type: depends_on
  target: K0644
  note: 終局証明済みLOSS7の23類と現行被覆との交差6類
- type: supersedes
  target: K0650
  note: 同じ94五石被覆を維持し、三証人交換を一回追加して七石義務を一類削減
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_post_seven_win6_2093_three_swap.json
  role: certificate
  note: 交換前後の三つの六石正準鍵と現行被覆の数値・勝敗UNKNOWNを固定
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_2093_three_swap.py
  role: verifier
  note: 五終局戦略再生、4×4 Bareissと3×3差分幾何による独立検証、改変負例6件
- path: research/experiments/n11-central-19-cover-20261031/audit_central49_2094_three_swap_neighborhood.py
  role: verifier
  note: 現行2094類からの三証人交換全近傍を厳密列挙し、2093類候補と照合
- path: .github/workflows/n11-central49-2093-three-swap.yml
  role: source
  note: 新2093類証明書の独立検証CI
- path: .github/workflows/n11-central49-2094-three-swap-exhaustive.yml
  role: source
  note: 2094類からの全三証人交換近傍の再現CI
- path: research/experiments/n11-central-19-cover-20261031/focus_s7_worker_2093.py
  role: source
  note: 現行2093類の優先六石64子を終局証明で2類確保し、残り62類を安全に四分配
- path: .github/workflows/n11-central49-2093-focus.yml
  role: source
  note: 現行2093類の集中配布・改変負例・安全統合の専用CI
- path: research/log/2026-11-03-n11-central49-2094-two-swap-local-and-2093-three-swap.md
  role: log
  note: 計算過程、再現方法、CI状態と証拠境界
scope: 標準11×11完全指摘・通常プレイ。中央49の94五石類を46六石LOSS候補で被覆する条件付き計画。六石LOSS・四石LOSS・二石root・空盤勝敗は対象外。
evidence: K0650の2,094類計画から六石証人三類を三類へ交換。4×4整数Bareissと別実装3×3整数差分行列式が追加三証人の全合法七石子で一致。46証人・94/94五石被覆・2,986合法七石辺・2,093正準七石類・K0644由来の終局証明済みLOSS7六類を確認。既知WIN6 145類・WIN7 23類との衝突0。固定交換と独立検証器をmainに記録。2093証明書の独立監査CI 41499925282成功、改変負例6件拒否。全三証人交換313,629候補（幾何的に有効283,361、確定WIN6除外1,455、有効281,906）を全数監査し、改善候補がこの一組だけであることをCI 41498886102で確認。優先六石の子64類・終局証明済み2類・未検証62類の配布器を2093類へ再固定し、CI 41499951578成功。
---

> **2026-11-03・終局WIN6反証（K0658）：この段階以降のLOSS証人計画は失効。**
> 2,154→2,094類の第2回三証人交換で、既に終局WINと独立証明済みの六石
> `00000000000000603800000000008000` が追加された。以後の2,093・2,091・2,090類計画も
> 同じ六石を保持した。幾何的な局所交換計数は歴史的結果として残るが、
> **全46六石をLOSSとして閉じる作業一覧には使えない**。
> 2096類への修復はK0659を参照。二石rootと空盤はUNKNOWN。

# 中央49の条件付き証明義務を2,093類へ縮小

**2026-11-03更新：この計画はK0653の2,091類計画に置き換えられた。** 本項は2,094→2,093類の交換と検証の履歴として保持する。

二証人以下の交換では改善不能だった2,094類の条件付き被覆を、**三証人の交換一回で2,093類に削減**した。選択六石証人46類、94五石類の完全被覆、既存の終局証明済みLOSS7六類を維持する。

| 指標 | K0650 | 今回 |
| --- | ---: | ---: |
| 六石証人 | 46 | 46 |
| 五石被覆 | 94/94 | 94/94 |
| 合法七石辺 | 2,987 | 2,986 |
| 相異なる七石証明義務 | 2,094 | **2,093** |
| 終局証明済みLOSS7との交差 | 6 | **6** |
| この証明系列で未確保 | 2,088 | **2,087** |

三証人交換の正準鍵は機械可読証明書に固定した。新しい三証人の合法七石子はそれぞれ59・60・65類で、4×4整数Bareissと3×3整数差分行列式で全件一致する。既知WIN6とWIN7を条件付きLOSS証人に採用しない。

全三証人交換近傍の再現用監査器と、現行2093類に固定した四作業者用配布器も追加した。**固定2,094類計画からの最大三証人交換313,629候補を全数検査し、勝敗証明済みWIN6・WIN7を除外した有効281,906候補のうち、改善する交換は今回の一組だけ**だった。ただし、**2,093類の大域的最小性や三証人交換後の局所最適性は主張しない**。再現用検証器で元の2,094類の共有済み局面集合を破壊する副作用を発見し、局面集合を複製してから交換するよう修正した。修正後の独立監査と集中配布器のCIは成功している。この計画に選んだ六石のLOSSは依然として未証明で、二石局面 {49,60} と標準11×11空盤の勝敗は **UNKNOWN**。
