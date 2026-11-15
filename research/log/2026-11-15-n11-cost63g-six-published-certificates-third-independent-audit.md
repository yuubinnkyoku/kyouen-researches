# 2026-11-15 n11 cost-63g: six published WIN7 certificates third independent audit

## 対象

cost-63gはhead 1195で始まったcost-63fの兄弟child `00000000080000801202000000200000` の探索。公開sweep auditは63候補、WIN7-D10 14件（bits 0/9/12/50/54/58/62/64/72/94/96/99/105/113）、REFUTED-D10 49件、capped 0、75,637,935節点。

2026-11-15 10:30時点で公開されていた証明書6件（bits 64/96/105/58/62/54）を対象にした。残る8件はまだ公開されていなかったため、対象外。

## 第三独立検査

cost63fで使ったのと同じ独立幾何方式を用いたが、今回の6証明書は別root・別証明書ファイルから再生した。

- 非共線3点: 有理数の外心を分子・分母で表し、整数式で同一円周を判定。
- 共線3点: 整数外積で同一直線上か判定。
- 浮動小数点なし。探索器、判定cache、BigInt検査器、Bareiss検査器をimportしない。
- Git blob SHAとファイル長を照合。
- root == child | (1<<bit)、root安全性、合法な相手初手、勝者の戦略手の合法性、敗者の全合法応手、終局で敗者が手詰まりであることを検査。
- 消費した勝者局面の和集合と証明書行の一致を検査。
- D4正準形をsweep auditの14 root orbit mapと照合。

## 結果

| bit | 証明書行 | root合法応手 | 訪問局面 | 敗者応手辺 | 終局 |
|---:|---:|---:|---:|---:|---:|
| 64 | 14,896 | 40 | 35,677 | 32,571 | 5,532 |
| 96 | 18,463 | 42 | 39,263 | 35,044 | 6,028 |
| 105 | 21,430 | 42 | 47,020 | 42,798 | 7,187 |
| 58 | 24,030 | 46 | 53,818 | 48,635 | 8,354 |
| 62 | 23,905 | 44 | 53,086 | 47,542 | 8,381 |
| 54 | 27,156 | 47 | 60,500 | 54,856 | 9,361 |
| **計** | **129,880** | **261** | **289,364** | **261,446** | **44,843** |

6/6 PASS。全件でmissing/extra=0/0、終局石数13〜17、rootから最大10手。6 rootのD4軌道はすべて異なり、sweep auditのWIN7 bit集合・orbit mapとも一致。

## D4親lift

7石rootから1石ずつ削除する42辺をD4正準化すると、**37個の異なるS6親軌道**になった。共有重複はchild `00000000080000801202000000200000` だけで、6証明書それぞれの追加bit（64/96/105/58/62/54）を削除すると同じchildに戻る。

これは6つのWIN7証明書が同じS6 childの勝ち手を6通り示す一方、残り36親liftは別軌道であることを示す。どの親liftがglobal manifestで未解決かは、receipt foldの再計算でのみ確定する。

## 成果物

- `scripts/audit_cost63g_six_published_certificates_rational_independent_20261115.mjs`
- `output/cost63g-six-published-certificates-rational-independent-audit-20261115.json`
- `.github/workflows/ci.yml` にNode 22での第三検査・JSON再生成比較を追加

CIのstatus APIはこのログ作成時点で空配列を返しており、CI PASSとは扱わない。in-session再生は6件すべて成功した。

## frontierへの影響と次の条件

この監査は証明書の再生確認のみであり、**global frontier寄与は0**。現headはcost63f fold後の **1199/6648/524616/4918/388339**。cost63gのsweep claimはhead 1195を基準に作られているため、14件の証明書出版・独立検証が完了した後のreceipt foldは必ずhead 1199へrebaseし、baselineを再現してから行う。並走laneの作業を重複起動していない。

この6証明書が示すのは各7石rootの深さ10以内の先手勝ちだけである。S6 childやS5親の閉鎖はreceipt fold後に判定する。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class2、class4は引き続き **UNKNOWN**。
