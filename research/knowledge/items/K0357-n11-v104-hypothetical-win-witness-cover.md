---
id: K0357
title: "11×11の{60,27}後の第三手104に対する仮想WIN witness cover"
kind: computation
status: computed
topics: [search-methods, square-outcomes, verification, provenance]
aliases: []
relations:
  - type: depends_on
    target: K0002
    note: 先手視点WIN/LOSSと石数 parity によるAND/OR規約
  - type: depends_on
    target: K0007
    note: exact勝敗値の順位付きAND/OR解釈
  - type: depends_on
    target: K0355
    note: 11×11 reply27保存済みcache frontierと有限検査の範囲
artifacts:
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-s3-boundary-diagnostic.json
    role: data
    note: 4,270-entry cache上の残余第三手ごとのcanonical s4 boundary診断
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-s3-v104-win-witness-cover.json
    role: data
    note: v=104の36 UNKNOWN s4 classに対するhypothetical共有s5 witness set coverとrational dual
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-s3-v104-win-cover-independent-audit.json
    role: manifest
    note: geometryを使った独立算術検査。全2401候補のload制約と18件cover/dualを確認
  - path: research/experiments/n11-boundary-recovery-20261006/output/post-next14-expanded-s5.cache
    role: data
    note: 固定snapshot input。canonical exact s5 cache 4,270件
  - path: research/experiments/n11-frontier-selection-20261005/scripts/reply27_geometry_cache.py
    role: verifier
    note: validated geometry index loaderとcanonical s4/s5 boundary data API
scope: "固定したpost-next14 4,270-entry s5 cache上で、{60,27}後の第三手v=104の55 canonical s4 classをfiniteに解析する。未解決exact verdictの探索はしない。"
evidence: "v=104のs4は19 WIN、0 LOSS、36 UNKNOWN。36 UNKNOWN s4 OR classを全てWINにするhypothetical candidate集合をvalidated s5 child geometry上の共有witness set coverとして計算したところ、2401個の現在UNKNOWN s5候補から18件で全36 classを被覆できた。独立検査で整数cover 18と有理dual下界18、全候補のdual load<=1を確認した。"
---

位置`{60,27,104}`は3石のAND位置で、その合法な第4手から生じる55 canonical s4 classは19 WIN、0 LOSS、36 UNKNOWNだった。s4は4石OR位置なので各UNKNOWN classに少なくとも一つexact s5 WINがあればそのclassはWINになる。ただし同じcanonical s5 keyが複数のs4 classを覆うため、36 UNKNOWN classは36個の異なるcandidate数を意味しない。

snapshot cacheで未解決だったs5候補2401個と36 classのincidenceからhypothetical minimum set coverを計算した結果、18 candidate s5 keysで全36 classを覆える。最大multiplicityは2 class/candidate。独立算術監査はこの18件coverの完全性と、有理dual総和18・全候補dual load上限1を確認している。したがって18は固定されたcacheとgeometryでの候補 verdict 数の組合せ最小値であり、solver実行数、探索時間、あるいは勝敗結果ではない。選択された18候補のどの結果もまだWINと判定していない。

仮にこの18候補が全てexact WINなら、v=104の36 s4 classを全てWINにでき、ANDであるs3もWINとなる。その場合、偶数石ORの`{60,27}`から第三手104を選ぶ条件付きWIN経路になる。これは候補選択の条件文であり、候補結果の実現可能性や`{60,27}`、空盤面の実際の勝敗を主張しない。既存の4-class universal LOSS coverとは目的と単位が異なるため、18と4の大小から実solver workを比較できない。
