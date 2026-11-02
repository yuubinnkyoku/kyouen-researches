---
id: K0659
title: 11×11中央49の終局WIN6除外後の46六石被覆は七石2,096類
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0658
  note: 旧2,090類計画を失効させた1984終局WIN6と除外漏れ
- type: depends_on
  target: K0644
  note: 独立終局証明済みLOSS7六類の再利用
- type: depends_on
  target: K0646
  note: 失効した2094段階より前の有効な2154幾何被覆
- type: supersedes
  target: K0654
  note: 失効した2,090類計画を146既知WIN6除外の2,096類へ修復
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_2096_exclude_missed_win6.json
  role: certificate
  note: 除去2・追加2六石、46証人・94五石被覆・2,989合法七石辺・2,096類を固定
- path: research/experiments/n11-central-19-cover-20261031/repair_2090_win6_two_swap.py
  role: solver
  note: 失効WIN6を必ず除去する45除去組・151候補を全数検査
- path: research/experiments/n11-central-19-cover-20261031/verify_2096_win6_repair.py
  role: verifier
  note: WIN6終局戦略・K0637終局戦略・交換全候補・追加六石4×4整数幾何・改変負例8件を独立監査
- path: research/experiments/n11-central-19-cover-20261031/focus_s7_worker_2096.py
  role: source
  note: 修復済み証人から最少未証明七石子を選び、4作業者へ重複なく配布・安全統合
- path: .github/workflows/n11-central49-2096-repair.yml
  role: source
  note: 2096証明書独立検証CI 41544501946成功
- path: .github/workflows/n11-central49-2096-focus.yml
  role: source
  note: 修復済み集中配布の検証
- path: research/log/2026-11-03-n11-central49-2096-certified-win6-exclusion-repair.md
  role: log
  note: 失効の起点、交換全数、独立検証、証拠境界
scope: 標準11×11完全指摘・通常プレイ。中央49の94五石正準類を46六石LOSS候補で被覆する条件付き計画。少なくとも146類の既知WIN6と23類の既知WIN7を除外。六石LOSS・二石root・空盤勝敗は対象外。
evidence: 旧2090証人集合に混入した終局WIN6を独立再検証し、その六石を必ず除去する45除去対・151交換候補を全数検査。幾何的に可能103、既知WIN6除外35、既知WIN7除外0、終局LOSS7六類を維持する有効候補63。最良は二証人交換による2,096七石類。新46六石証人は94/94五石を被覆し、2,989合法七石辺・相異七石2,096類・K0644終局証明済み6類・未証明2,090類。146既知WIN6と23既知WIN7の衝突0。追加六石は独立4×4整数Bareissと3×3差分整数幾何で一致。独立検証CI 41544501946成功、改変負例8件拒否。いずれも条件付き幾何計画であり、六石LOSSは未証明。
---

# 終局WIN6を除外して、2,096類の有効な条件付き計画へ修復

旧2,090類計画は、既に元先手WINと終局証明された六石 `00000000000000603800000000008000` をLOSS証人に含むため失効した。最初に混入したのはK0650の2,154→2,094類への第2回三証人交換である。

失効六石を必ず除去する二証人交換を全数調べた。除去対45組、候補151組のうち、幾何的に可能103組、146類の既知WIN6との衝突35組、既存の終局証明済みLOSS7六類を保持する有効候補**63組**。最小の相異七石義務は**2,096類**だった。既存六類の保持条件を外しても最小値は同じである。

| 指標 | 旧2,090類（失効） | 修復2,096類 |
| --- | ---: | ---: |
| 六石証人 | 46 | 46 |
| 五石被覆 | 94/94 | 94/94 |
| 合法七石辺 | 2,983 | **2,989** |
| 相異なる七石証明義務 | 2,090 | **2,096** |
| K0644終局証明済みLOSS7 | 6 | **6** |
| 未証明七石類 | 2,084 | **2,090** |
| 1984終局WIN6との衝突 | **1** | **0** |

除去六石は `00000000000000603800000000008000` と `00000000000002083800000008000000`。追加六石は `0000000000000000380c200000000000` と `00000000000000203800000008008000`。独立4×4整数Bareissによる追加六石の合法子再計算と、交換全数探索を含む専用CI [41544501946](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/41544501946) が成功し、改変証明書8件も拒否した。

**2,096類は証明計画の幾何的な大きさであり、2,090類のLOSSが証明されたわけではない。** 同じ二証人交換近傍における最良値であって、大域最小性も未証明。四石LOSS・二石局面{49,60}・標準11×11空盤の勝敗は**UNKNOWN**。
