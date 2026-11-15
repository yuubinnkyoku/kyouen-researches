# 2026-11-15：cost67c WIN7証明書の第三独立再生監査

開始時main: `2f05130ff7deb5535ea76366ded18523346e097f`。対象はcost67cで公開済みのbit64・bit96の2証明書。receipt foldは行わず、証明書の戦略木と親liftを別実装で再生した。

| 指標 | bit64 | bit96 |
|---|---:|---:|
| 証明書行 | 34,583 | 35,897 |
| root合法初手 | 53 | 53 |
| 全root合併後の一意DAG局面 | 52,739 | 54,785 |
| 勝ち側局面 | 34,583 | 35,897 |
| 負け側局面 | 10,656 | 10,834 |
| 負け側応手辺 | 50,810 | 51,438 |
| 終局 | 7,500 | 8,054 |
| 終局石数 | 13〜17 | 13〜17 |
| missing / extra | 0 / 0 | 0 / 0 |

BigInt有理中心分子と共線外積の整数判定を用い、浮動小数点・repo solver/cache・既存のBigInt verifier・perm-det4 verifierは使用していない。両証明書とも全戦略木を再走査し、戦略行と実際に消費した勝ち局面が完全一致。証明書全体のMD5・SHA-256・Git blob SHA、分割片のGit blob SHAも照合した。

2 rootから得る親liftは14 incidence、異なるD4軌道は13。共通親S6 `00000000000000801202000000202000` はbit64・bit96の2つの合法手で別々の第二手番LOSS rootへ進めるため、**この六石局面はWINと証明された**。13親軌道中7軌道が7,867行のS6 manifestに存在するが、worklist所属は未解決を意味しない。

共通子S6はhead 1216のtop-candidates CSVでclass2親の残り行として直接確認できる。D4削除から得るclass4親もopen S5だが、その子行はtop-candidatesの掲載範囲外であり、この監査では残りincidenceを独立再生成していない。claim側は両親に残り行があると記録している。

receipt foldは未実施。親lift全体と未解決S6集合の交差を確定していないため公式frontierは更新しない。headは `1216/6631/523382/4901/387105`、残りS5は175軌道のまま。公式solved数の増分は0（fold未実施）。

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は **UNKNOWN**。

再現: `node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost67c_certificates_third_independent_20261115.mjs`
