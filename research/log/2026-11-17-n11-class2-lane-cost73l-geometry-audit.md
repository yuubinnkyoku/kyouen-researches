# 2026-11-17：cost73l の32 WIN7 rootを独立幾何監査・D4重複監査

## 開始時点と参照した正本

開始時に確認した main は \`a1e1590b43077cacf7cb829aa5f223476c7314ca\`。作業中に別レーンの更新（\`0fa02b7b\`、\`f8381a68\`）が fast-forward で入り、今回の成果を含む main は \`550f1b0e85abc903c5ac9bb8dfdd9af81652b35b\`。

\`AGENTS.md\`、\`research/knowledge/README.md\`、K0023・K0863・K0865・K0868・K0907、実験README、cost73l sweep-complete log、cost73l certificates log、claim v3、raw sweep audit、manifest、stats、det-reextraction を確認した。

K0868の候補規約は、6石 child の3点組に対する整数 \`det4\` が0となる空セルを除外するもの。共線の退化円も除外対象に含む。K0907は証明書extractorのmemo符号キー・負境界の欠陥を性能のみの問題とし、誤ったhitは生じないと検証している。ただしfixBの大幅な節点削減とbyte同一batteryはcost73kの22本に対する結果であり、cost73lの32本へそのまま外挿しない。

## 独立幾何・D4監査

対象は child \`00000000000000c09002000000400000\`、cost 73。manifestにある32個のWIN7-D10 rootを、既存の \`legal_candidates.py\` やcensus実装をimportせず、BigInt整数演算で再導出した。

- 全32 rootで \`root = child | (1 << bit)\` が一致。
- 全32 rootが7石で、全4点組の \`det4 != 0\`。安全性を再確認。
- 全32 rootの生残手数を独立再計算し、manifestの \`loser_mobility\` と32/32一致。
- D4の8対称変換を独立実装し、\`d4_canon_root\` と32/32一致。\`raw_is_canon\` も全件一致。
- 32 root間のD4正準形重複は0。
- 既存cost73j（16本）・cost73k（22本）の計38 rootとのD4重複も0。
- transfer bit106はcost73j bit118、bit110はcost73k bit98とそれぞれD4正準形が一致。claim v3のtransfer canonとも一致。

claimの候補分割は73候補 = 66 open + 7 confirmation。結果は34 WIN7-D10 / 39 REFUTED-D10 / capped 0。manifestの32本は新規sweep WINの32本で、残り2 WINは上記transfer証明書で被覆される。

statsの32行を合計し、manifestと再照合した。

| 指標 | 再計算値 | manifest |
|---|---:|---:|
| 証明書 | 32 | 32 |
| 戦略行 | 1,693,203 | 1,693,203 |
| 抽出節点 | 424,657,112 | 424,657,112 |
| 証明書bytes | 61,171,191 | 61,171,191 |
| FBT drops | 0 | 0 |

決定論性の公開サンプル6 bit [1, 9, 47, 61, 64, 116] は、manifest・stats・det-reextraction間でmd5、行数、sizeがすべて一致した。これは公開済みの再抽出記録との照合であり、今回6本を再抽出した意味ではない。

## 再現用成果物と境界

- \`scripts/audit_cost73l_manifest_geometry_20261117.mjs\`：BigInt det4・D4・mobility・claim/manifest/stat・transfer重複を再監査するNodeスクリプト。blob \`8a32f40f23dacd6a5948e19e12f776edb37e496a\`。
- \`output/class2-lane-cost73l-publication-geometry-audit-20261117.json\`：今回実行した監査結果。blob \`e544fb1af1c442b6d707d66ace0b8be775adad0d\`。
- \`output/class2-lane-cost73l-pins-20261117.txt\`：GitHub directory listingから取得した証明書出力ディレクトリ159ファイルの \`name|blob_sha|size\` pin表。blob \`f36f9a57790a476f552f42c1924ba25b8615a4b3\`。

監査スクリプトの幾何計算はこの実行内で同じBigInt式を用いて再実行したが、公開スクリプト自体をローカルrepo checkout上で実行したとは主張しない。pin表は159件の名前・blob SHA・sizeを固定したもので、今回その159ファイルのbytesを再取得・再hashしたわけではない。

**重要な未完了点:** GitHub connectorは1MB超のcertificate partを本文取得できず、raw certificate bodyを読み込めなかった。そのため、今回の監査では32本の戦略行をBigInt verifierで探索していない。公開logのBareiss engine-free verifier 32/32 PASSを今回再実行したわけでもない。第三実装BigIntによるbytes-level再検証は依然pending。

Proxmoxの利用可能資源も確認した。pve-hp-aioはメモリ91%使用、pveは4 core・メモリ43%使用だが、負荷を隔離して回せる適切な実行guestは確認できなかった。共有ホストを圧迫する長時間ジョブは起動していない。

## 次の作業

1. pin表159件とclaim pinを使い、32 certificateのsplit/whole bytes、Git blob SHA、md5/sha256、header/root/row countを照合。
2. \`verify_win7_certificate_bigint_independent.mjs\` を32本に実行し、root mobility・全subroot・strategy row union・terminal range・sidecarのseen/terminals/opponentEdges総和を突き合わせる。並列は2 workerから始める。
3. 既存のBigInt検証済み151 root（cost73kの前段129 + cost73k 22）とのD4重複を確認。
4. その後もcoordinatorの順序を守り、receipt foldは別レーンのfold chain完了後に行う。

## 解釈境界

- WIN7-D10は個別7石rootの深さ10以内の先手勝ちのみ。
- REFUTED-D10はLOSS証明ではない。
- 今回はreceiptをfoldしておらず、manifest行は1つも閉じていない。
- **標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はすべてUNKNOWN。**
