# 2026-11-12 11×11 S2 {59,60}: 修正版milestone-4所属多重度の独立集計

基準main: e3e4ebbe095b7cbe5aab9e3247eca60bd25a274f。K0757修正版manifest（3分割、合計1,782,603 bytes、記録上のMD5 452b4336edbe272a49dcd76c4a7764af）をGitHubから取得・結合・JSON解析した。旧manifestは使わない。

各S6行 [hex,cost,certs] について、certStatsの30個のbitマスクを用いて `(BigInt(certs) & BigInt(bit)) === BigInt(bit)` の成立数を数えた。**S6所属証明書数の分布**は1件: 1 orbit、2件: 2,375 orbit、3件: 40,999 orbit（合計43,375）。4件以上は0。1件だけの局面は {73} 証明書に所属し、その他の29証明書には単独専有のS6 orbitがない。

30証明書を別々に処理した場合のS6→S7合法辺数（各証明書所属局面のcostを足した値）は10,242,168本。S6を一度ずつ処理した場合は3,477,178本。差は6,764,990本、重複分の割合は約66.05%。これは**辺の静的重複**であって実測時間短縮ではない。共有cache・同一局面一度の処理の重要性を示すが、全S6のWIN/LOSS認定が必要な点は変わらない。

再現手順（Python 3、標準ライブラリ）: 修正版part1/part2/part3を順にバイト結合しJSONを読み、`masks=[int(x["bit"]) for x in j["certStats"]]`、各 `r in j["s6All"]` で `n=sum((int(r[2])&b)==b for b in masks)` を集計する。各証明書の所属行数は `certStats[].s6OrbitsSingle` と照合すること。値が0のマスクがないこと、マスク同士のビット重複がないことも事前条件。

本集計は証明書所属の構造分析のみ。S6 verdict・S2・11×11空盤は **UNKNOWN**。
