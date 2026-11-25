# 2026-11-17：cost66i bit19 WIN7証明書のBigInt独立再検証

## 開始時点

開始時のmainは `41544af1b2126fe7098f86fb399e60214040ef09`。`AGENTS.md`、`research/knowledge/README.md`、K0023、K0863、K0865、K0868、cost66iの証明書manifest・完了記録、およびcost76c bit61の証明書・head1472 fold記録を確認した。

cost76c bit61のfoldは既にmainへ反映され、現在の基準headは

`1473/174/6375/504596/4648/368510`

である。これはS6 manifest被覆の簿記であり、S5 parentはまだ閉じていない。

cost66iは6石child `00000000000000801226000000000000` の66候補sweepで9 WIN7-D10・57 REFUTED-D10・capped 0。9本の証明書も既に出版・Bareiss検証済みで、bit19はhead1452時点の候補marginalが最大（manifest 4行、64h pending foldとの重複1行）だった。ただし、このmarginalはhead1452基準なので、head1473のfold判断には再利用しない。

## bit19公開バイト列の再構成

対象rootは `00000000000000801226000000080000`。公開済みpart1/part2をmainのcommit pinから取得し、README-splitとmanifestを照合した。

| 対象 | bytes | Git blob SHA-1 |
|---|---:|---|
| part1 | 739,395 | `e8f083cd357ce03aaf177f8ee40c868450e11a37` |
| part2 | 739,348 | `53efcd57fbda21c8f5976987a23f55dbd4cad993` |
| 結合後 | 1,478,743 | manifest SHA-256と一致 |

結合後SHA-256は `f87df551ab38f73fb34d756fc4be287de42f1538735e7daf6006deb05749b0ac`。manifest記載値と一致し、part1は行境界で終わる。README-splitの分割サイズとも一致した。

## BigIntによる独立検証

浮動小数点を使わず、持ち上げ座標 `[x²+y²,x,y,1]` の3×3余因子展開をBigIntで評価し、証明書の戦略木を再走査した。既存のBareiss検証器・探索器・verdict cacheは参照していない。

| 検査 | 結果 |
|---|---:|
| rootの石数・安全性 | 7石・安全 |
| rootの合法防御手 | 52 |
| 戦略行 | 40,935 |
| 検証済みsubroot | 52/52 |
| 訪問状態（subroot合計） | 89,700 |
| winner状態 / loser状態 | 58,420 / 18,401 |
| loser応手辺 | 84,973 |
| 終端状態 | 12,879 |
| 終端石数範囲 | [13,17] |
| 証明書行と消費行の差 | missing 0 / extra 0 |

既存のBareiss記録とも、root mobility 52、戦略行40,935、subroot 52/52、終端範囲[13,17]、行集合差0/0で一致した。

## 再現用runner

`scripts/reverify_cost66i_bit19_bigint_20261117.mjs` を追加した。manifest・README・分割part・既存BigInt検証器のGit blob SHAを固定し、結合後MD5/SHA-256を検査してから、既存の独立BigInt検証器を一時ファイルに対して起動する構成である。

このrunnerはNode.jsの構文検査を通過した。今回の数値は、公開partを再構成して隔離JavaScript実行環境でBigInt走査した結果であり、追加したNode runner自体の完全な再実行はまだ行っていない。runnerはその再現経路として公開した。

## 解釈と次の作業

今回確かめたのは**7石root bit19のWIN7-D10証明書**だけである。新しい探索verdictは作っておらず、receipt foldも行っていない。S6 manifest行・S5 parentを閉じた数は今回0。

次は9本のcost66i証明書すべてについて、D4正準形・既存receiptとの重複・WIN/LOSS conflictを再確認し、**head1473に対するmarginalを再計算**する。bit19を最優先にするかどうかも、その再計算結果で決める。head1452の順位をそのまま引き継がない。

WIN7-D10は個別7石rootの深さ10以内の先手勝ちであり、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続きUNKNOWN。
