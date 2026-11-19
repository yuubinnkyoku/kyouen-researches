# 残余78行の39-root掃引が消費した候補範囲の再監査

2026-11-20。開始時の `main` は `b7e6d2d016acc231cbd9628a5b307fed1a40902b`。AGENTS.md、knowledge README、K1057/K1059、resolve5正本・実装、39-root入力・掃引結果を再確認した。

## 観察された食い違い

K1059の39-root sweepは、resolve5が選んだ39本を全てREFUTED-D10とした。しかし、resolve5正本の**事前候補集合**はfresh-safe 4,728本であり、今回のsweep入力はそのうち39本だけである。したがって、今回の掃引が直接消費したのは選択済み39-root計画であって、4,728本全体ではない。

さらにresolve5の候補グラフには706個の異なる行ペア辺と78行のsingleton候補が記録されている。今回の39本は各2行を覆う互いに素なmatchingであり、singleton候補ではない。ゆえに事前グラフ上では、今回選ばれなかった667個の行ペア辺と、78行のsingleton候補群がこのsweep入力には含まれていない。

## 独立再監査

新しいスクリプトはresolve5出力・resolve5ソース・roots.json・sweep JSONの4 Git blob SHA-1を固定し、以下を再検査した。

- 39 rootの一致（resolve5 witness / runner input / sweep record）
- 39 rootが7石・D4正準・整数行列式で安全
- D4の8像から1石削除したときの残余行被覆が記録2行と一致
- 39組が互いに素で、残余78行をちょうど一度ずつ覆う
- 両AND順序の78 probeが未打切りREFUTED-D10、pilot_d6全件合格

全9 gateが通過した。出力は `output/candidate-supply-scope-audit-20261120.json`。

## 判断

「この39-root計画は消費済み」は正しい。一方「add-one-stone depth-10のfresh候補集合全体が枯渇した」と読むのは誤りである。4,689本はこの39-root sweepの外にある。ただしresolve5のverdict結合は明示pin 379 REFUTED / 168 WINに限られ、K0863の8,964-root全体キャッシュとの結合ではない。したがって4,689本が現在も全て未判定だとは主張しない。

次の優先作業は、K0863の全体cacheを個別root単位で再構成し、4,728候補へ結合したうえで、39本のREFUTEDを除外して候補被覆を再解決すること。これを済ませる前にadd-two-stonesへ移るのは早い。なお、この監査は最大matchingを再計算しておらず、行閉鎖・receipt・勝敗の進展はない。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は引き続きUNKNOWN。
