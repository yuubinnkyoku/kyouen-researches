# 2026-11-19 n11: 49-root残余候補の最小分岐rootからWIN7-D10証明書を取得・独立検査・receipt fold

## 開始時点と入力固定

開始時のmainは f4de1d01844d9af2911fac3151b106b3ba67af9d。AGENTS.md、research/knowledge/README.md、K0863・K0865・K0868と、49-root残余coverの実験・ログを確認した。AGENTS.mdの規約どおりmainへ直接反映し、branch / PRは作らない。

抽出時のsource main 567045d818d1943bfb8b97d74e7f9bc29f9d0acdは現行mainの祖先（277 commits ahead / 0 behind）。receipt foldの元の基準head a84969a6b537a4108c181bce59726db485d0d0dcも現行mainの祖先（270 ahead / 0 behind）。receipt-fold JSONには、公開直前headとしてf4de1d01844d9af2911fac3151b106b3ba67af9dを固定した。

foldが使う11入力のGit blob SHA-1を現行mainから再取得して照合し、11/11一致した。対象はworklist、fold-chain ledger、STERILE census、global receipt fold、cost78c/79c fold、49-root cover、mobility、runner v17、extractor v16、BigInt verifier、Bareiss verifier。sourceや入力が後続commitで差し替わっていないことを確認している。

## 対象rootと探索

対象は7石D4正準root 00000000000000821082000010800000（D4 orbit size 8）。49本の残余候補中、合法次手数が最小の47。bit 71を除いた6石childは 00000000000000021082000010800000。開始時の公開verdict indexにはchild orbitがなく未判定だった。

runner v17、depth 10、cap 950,000で2方式を実行した。

| probe | runner結果 | nodes | 時間 | 打切り |
|---|---|---:|---:|---|
| andclose=1 | loss=true | 392,235 | 1,142 ms | なし |
| andclose=0 | loss=true | 446,745 | 1,337 ms | なし |

pilot_d6 controlは両方式3,402 nodesで一致。runnerのloss=trueは当該6石childの手番側（後手側）の敗北を示し、7石rootの先手WIN候補となる。最終的なWIN7-D10判定は、完全な戦略証明書と独立検査を通してから採用した。

## 証明書抽出と独立検査

既存のclass4_child1_cert_extractor_exact_v16.tsを固定root・bit71・47応手へ適用した。47応手すべて完了、総616,064 extraction nodes、26,708 unique strategy rows、fbt_drops=0、終局石数13〜17。

展開後の証明書は966,579 bytes、SHA-256:
5a32d95d0e1bddfeed9e810db4d372d5a9440cde594b12b3d94ae2dd06c02ab8

Git管理上はgzip 119,778 bytes（SHA-256 b18b5f607f4c6d215f3fb999f102d30e897f99be2e4416ff88f5dfbb89d8e7bd）で保存した。再現用driver・検査結果・receipt fold JSONはevidence bundle（12,524 bytes、SHA-256 3d4e78e1afeb030a86f0ed8acc7dbba5777b80f5c4ea40e1f238c08582f1c048）に格納した。bundle内READMEに展開・再検査手順を記載した。

BigInt 3×3余因子展開（lifted determinant [x²+y²,x,y,1]、浮動小数なし）でroot安全性、mobility 47、47 subrootsを検査。証明書行26,708、消費行26,708、union missing=0 / extra=0。別実装の4×4 Bareiss行列式検査も47/47 subroots PASS。seen 60,884、terminals 9,942、opponent edges 54,552、consumed records 39,307 / unique 26,708、union差分0。二方式は同じ探索器の再実行ではなく、determinant計算と検査実装を分けている。

## receipt foldと残余cover

証明書rootから4つのS6行が新たにreceipt化された。edge cost合計262。うち5親target内は次の2行。

- 00000000000000821082000000800000
- 00000000000000821082000004000000

残り2行は 00000000000000801082000084000000 と 00000000000000103800000000002020。影響を受けたS5 parentは5個で、各parentの行数を2ずつ減らしたが、完全閉鎖されたparentは0。

| frontier項目 | fold前 | fold後 |
|---|---:|---:|
| solved S6 in manifest | 1,608 | 1,612 |
| unique remaining S6 | 6,240 | 6,236 |
| remaining S5 orbit | 173 | 173 |
| remaining cost | 493,965 | 493,703 |
| open-class S6 demand | 4,524 | 4,524 |
| open-class demand cost | 358,685 | 358,685 |

solved S6はmanifestのreceipt bookkeepingであり、ゲーム状態の勝敗確定数ではない。open-class demandは変わっていない。

5親targetは97行から95行へ減少。候補coverは49 rootから48 root（47 pair + 1 singleton）へ縮小した。95行に対する下界ceil(95/2)=48と、各行を重複なく覆う48-root witnessが一致するため、残余coverは厳密に最小。WIN/LOSS conflictは0。

## 再現と実行環境

接続runner pve:199（Debian 13、Node v22.23.5、1 vCPU、4 GiB RAM）で実行。root filesystemは満杯だったため、抽出・検査の再実行は/dev/shm上で行い、巨大な中間ファイルをroot diskへ書かなかった。3 driverすべてnode --check成功。

- extract driver再実行: certificate / summary byte-identical
- BigInt verifier: 47/47、union差分0
- Bareiss verifier: 47/47、union差分0
- receipt fold driver: current main head f4deを固定し、元fold結果とbase head以外のJSON構造・数値が一致
- progress JSONLの時間欄は実行ごとに変化するため、決定性比較の対象外

## 結論と境界

49本の残余候補から、最小分岐の7石rootを1本WIN7-D10で閉じ、5親targetの2行をreceipt化した。残余coverは49→48 rootへ厳密に縮小した。

ただし二石rootを閉じたわけではなく、5親の完全閉鎖も0。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はUNKNOWNのまま。REFUTED-D10をLOSSと読み替えない。
