---
id: K0433
title: 初手49の閉鎖不能8応手は保存pool制約の産物であり、証明書の逆向き再利用は新規S5 WINを与えない
kind: computation
status: computed
topics: [square-outcomes, search-methods, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0420
  note: 初手49 WIN側frontier（pool 1,928・closable 57・unclosable 8軌道）
- type: depends_on
  target: K0371
  note: 元先手固定のAND/OR極性（S5 WINは全S6子WIN、単一S6 WINから結論しない）
- type: depends_on
  target: K0426
  note: S6終局LOSS証明の逆向き全子完成伝播の入力
- type: supports
  target: K0417
  note: 候補効果測定が第8次計画の層別・上界判断に資する
artifacts:
- path: research/experiments/n11-night-plan-update8-20261016/scripts/analyze_unclosable.py
  role: source
  note: 閉鎖不能応手の制約なし再解析と新規証人候補列挙
- path: research/experiments/n11-night-plan-update8-20261016/output/unclosable-reanalysis8.json
  role: data
  note: 8応手のpool-shortage判定・greedy証人数・pool外候補227
- path: research/experiments/n11-night-plan-update8-20261016/scripts/reuse_certificates.py
  role: source
  note: S6/S7/S8終局証明の逆向き全子完成伝播と再利用の算定
- path: research/experiments/n11-night-plan-update8-20261016/output/certificate-reuse8.json
  role: data
  note: 追加S5 LOSS indexed 2＋index外1、新規S5 WIN 0、計画効果0
- path: research/experiments/n11-night-plan-update8-20261016/output/candidate-branch-ranking.json
  role: data
  note: pool未カバー分岐9件を単独解消する候補9件の列挙
- path: research/experiments/n11-night-plan-update8-20261016/output/candidate-effects.json
  role: data
  note: 候補別に分岐解消数・WIN/LOSS時の上界差分を測定
scope: 標準11×11・q=4・通常プレイ。元先手固定視点。初手49の全65応手軌道（D4縮約）と保存WIN証人pool 1,928、およびS6/S7/S8終局証明。solver探索なし（候補効果は計画再計算のみ）。
evidence: 第8次再被覆で閉鎖不能な応手軌道は `[0,1,2,4,15,46,79,101]` の8件。保存pool制約を外して各応手のthirdsを再解析すると65/65が閉鎖可能で、8件はいずれも pool-shortage（幾何的・数学的障害ではない）。群の最小証人数は greedy で30（r=46）〜32、exact探索はnode cap 400,000到達で未確定（greedyは上界）。pool外の新規証人候補は227件（全て used_in_replies=1）。S6/S7/S8終局証明を逆向きに全子完成伝播させると、追加でLOSSと確定するS5は indexed 2件（381858 / 382619、既に第8次層別済）＋index外1件のみで、新規S5 WINは0（S7根の7つのS6 WIN親はどのS5の6子も完成させない）、新規S7 LOSS 0、楽観的共同計画の和集合は不変（効果0）。pool未カバー分岐は第7次12・第8次9で、単独で解消できる候補は9件（143718 / 144019 / 196002 / 221294 / 103564 / 211133 / 144774 / 193768 / 144692）。各候補は分岐1つを解消しLOSS時Δ−1、WIN時Δは0（150871）〜+111（221294）。実測最良は150871（WINΔ0→新規LOSSとして層別）で、次は144774（WINΔ+1・10M NODE_LIMIT）。
---

初手49のWIN側frontierが示す未閉鎖8応手は、応手側の構造的障害ではなく、保存WIN証人poolという有限資産の枯渇（pool-shortage）である。したがって救済は当該応手分岐を閉じる未知S5 WINの獲得であり、pool外の新規証人候補227件の終局閉包が必要になる。

証明書の逆向き再利用は、既に独立証明済みのS6/S7/S8終局構造を全子完成規則で伝播させるもので、第8次ラウンドでは計画を広げる新規WINを生まなかった（新規S5 WIN 0）。これはK0371極性（S5 WINは全S6子WINを要し、単一S6 WINからは結論しない）を保った帰結である。

限界: 群のexact最小証人数は未確定（greedy上界のみ、node cap到達）。pool外証人候補227件は列挙までで、被覆成立・正準性・未cacheの検証と、証人1個あたりの全S6先手WIN閉包費は未測定。
