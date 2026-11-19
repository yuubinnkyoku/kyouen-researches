---
id: K0865
title: "head-1410 receipt-unclosability census — 174 個の open S5 parent 全数の STERILE 被覆分類（3 parent が残行すべて STERILE で D10 receipt 閉鎖不能・57 partial・orbit-level join）"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases: [head1410 sterile-coverage census, receipt-unclosability census]
relations:
- type: depends_on
  target: K0863
  note: 閉鎖不能分類は K0863（STERILE 行は自前行からの depth-10 WIN7 receipt を持たない）の適用
- type: depends_on
  target: K0783
  note: manifest・receipt の簿記規約
artifacts:
- path: research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json
  role: data
  note: 174 parent 全数の census。コントロール CA〜CI と sha256 入力 pin を含む
- path: research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/cover-precheck-70j-vs-62b-20261116.json
  role: data
  note: 完了済み 62b child からの 70j 行 cover set {21,109} の独立再導出
- path: research/experiments/n11-head1410-receipt-unclosability-census-20261116/report.md
  role: log
  note: census の方法・結果・検証境界

- path: research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_49_root_cache_exclusion_and_mobility_20261119.mjs
  role: verifier
  note: K0863の全133 child universeに49 rootの全削除子D4 orbitを照合し、BigInt Bareiss/Leibnizで次手数を独立計算する再現器
- path: research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-cache-exclusion-mobility-20261119.json
  role: data
  note: 49 rootのcache非所属、唯一のopen bit74照合、合法次手数47〜77、determinant二方式一致
- path: research/log/2026-11-19-n11-49-root-cache-exclusion-and-mobility.md
  role: log
  note: 完全child-universe非所属証明、分岐数の意味と次の探索判断
- path: research/log/2026-11-19-n11-audit-runner-reproduction-and-ci-repair.md
  role: log
  note: 49-root監査の別環境再現、cost63f証明書監査とCI出力差分の再検査

- path: research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_49_root_two_ply_frontier_20261119.mjs
  role: verifier
  note: 49候補rootの二手先frontierをBigInt二方式のdet4とD4正準化で全数集計する再現器
- path: research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-two-ply-frontier-20261119.json
  role: data
  note: 2,985子・146,118順序付き二手目・73,059局面・72,756 D4類・303 root間重複
- path: research/log/2026-11-19-n11-49-root-two-ply-frontier.md
  role: log
  note: 二手先frontier、D4共有cache、coordinator候補順位と証明境界

- path: research/log/2026-11-19-n11-49-root-two-ply-reproduction-repair.md
  role: log
  note: 二手先frontier再現器の構文・出力先・JSON schema不整合を修正し、固定入力の全数再計算で旧結果を照合

- path: research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_49_root_three_ply_frontier_20261119.mjs
  role: verifier
  note: 49候補rootの三手先（10石）frontierをBigInt det4二方式とD4正準化で全数集計する再現器
- path: research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-three-ply-frontier-20261119.json.gz
  role: data
  note: 923,696 raw 10石局面、923,586 root別D4類、10,653 root間重複membershipの圧縮結果
- path: research/log/2026-11-19-n11-49-root-three-ply-frontier.md
  role: log
  note: 三手先のD4共有率・root pair重複・探索候補順への含意と検証境界

scope: "2026-11-16に算出した n11 class-lane の post-cost-60c 正準 head 1410 に対する履歴スナップショット（174 open S5 parent、MS5 S6 manifest 7867 行・orbit 重複なし、35 STERILE 行）。cost-65j fold は後続作業として head 1410 から 1419 へ適用済みであり、本 census の基準 head は 1410 のまま。"
evidence: "orbit-level census: 全 174×7867 ペアで ∃σ∈D4: σ(P) ⊂ R を判定。コントロール: CA manifest 7867 行・cost 総和 615497・orbit 重複なし、CB 174 S5 canon 重複なし、CC cost-60c fold の parent-row 6 ペア全件 orbit-related、CD 62b 行の出版 claim 記載 parent が census の open parents に全件含まれ demand {c1:1,c2:1,c4:0} も完全一致、CE 既知 anchor 3 件（rem 3/209・10/698・18/1460）が出版値と精密一致、CF 違反 0、CG pending-65j 34 orbit が STERILE と非交差、CI cover precheck bits {21,109}・62 合法手 bit 集合・両 cover root hex が出版 claim v2 と一致"
---

## 主張

head-1410 の 174 個の open S5 parent のうち、

- 00000000000000801202000000200000（class 2, rem 3, cost 209; 残行 = 65k/70j/74h 行）
- 00000000000000809082000000000000（class 3, rem 10, cost 698）
- 00000000020000003800000080000000（class 4, rem 18, cost 1460）

の 3 parent は、残存するすべての S6 行が STERILE である。よって K0863 により、これらの parent は自前行のどの D10 WIN7 receipt によっても閉じられない（receipt-unclosable）。さらに 57 parent が部分 STERILE（effRem = rem − STERILE refs > 0）で、残存行参照 12274 個のうち 91 個（0.74%）が実効的に閉鎖不能、effRem 合計は 12183 である。

## 補足

- S5 parent と S6 行の関連は D4 orbit レベルで判定する必要がある（raw hex subset join では 65k/74h 行の class-1 demand が出版値と不一致になる）。cost-60c fold の parent-row 6 ペア全件が orbit-related であることで検証した。
- 完了済み cost-62b child（STERILE, 62/62 REFUTED-D10）からの 70j 行の cover set は bit 21 と bit 109 のみで、両方 REFUTED-D10。出版 claim v2 の記述（合法手 bit 集合・cover root hex・demand）と独立に完全一致する。
- head 1410 時点の pending 65j fold は 54 個の行参照に効くが、単独で閉じる parent は存在しない。後続の cost-65j fold は head 1419 へ9行を閉じた。

## 境界

STERILE は「その行自身からの D10 WIN7 receipt では閉じられない」ことであり、その局面の LOSS 証明ではない。receipt-unclosable も勝敗の判定ではなく、cross-cover（隣接 child 経由）や depth 10 を超える証拠の可能性は残る。solved head 1410 は manifest 被覆の簿記である。11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。


## 2026-11-19 追記: head-1608後の5親joint targetをreceipt-awareに再被覆

head-1410の5親joint target 112行を後続receiptに照合すると、head-1589 global foldが13行、cost78c/79c foldが追加2行を閉じており、未閉鎖は97行だった。候補rootの最大被覆数は2行なので下界は49本。31個の公開subset witnessから得た117候補を既知verdictに照合し、既知REFUTED 5本を除外した残余グラフで最大マッチング48、singleton 1本を構成。これにより残97行の最小候補root coverは**49本（48 pair + 1 singleton）**と確定した。49本すべて7石・D4正準・det4非零を独立再検査し、97行を重複なく被覆する。

この照合で利用した既知verdictはREFUTED-D10 236 root、WIN7-D10 156 root（head1476 cost71e、cost73j、cost78c/79cおよびreceipt foldの明示資料）。候補poolとの交差はREFUTED 5、WIN 0。この時点では8,964件のper-root cache全体とのjoinは未完了だったが、後続の候補側非所属監査で49本すべてが公開engine verdict/115 transferに未該当と確認した（48本は全7削除子のD4 orbitが133 child universeに存在せず、残る1本はbit74がopen）。これはraw 1,064ファイルの再走査ではなく、K0863 scanの完全child universeを使う非所属証明である。49本はなお探索候補でありWIN証明書ではない。詳細は[監査ログ](../../log/2026-11-19-n11-five-parent-residual-49-root-cover.md)、[再現スクリプト](../../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_five_parent_residual_49_cover_20261119.mjs)、[結果JSON](../../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/five-parent-residual-49-cover-20261119.json)。標準11×11空盤・二石root・S2・class 1/2/4は引き続き **UNKNOWN**。


## 2026-11-19 追記: 49-root候補の既存verdict非所属と次手分岐数

K0863の8,964 engine verdict（REFUTED-D10 8,305・WIN7-D10 659）と115 transfer（全てREFUTED-D10）を含む133個の6石child universeに対し、49本それぞれの7削除子をD4正準形で照合した。48本は該当child orbitなし。残る1本 `00000000000000909002200080000000` はchild `00000000000000801222000000800000` のbit74に対応するが、engine verdictは0件、transfer bitsは55/65/109のみで、bit74はopen。よって49本すべてがこの公開indexでは未判定である。これはraw 1,064ファイルを再走査した結果ではなく、scan生成器が全claims/sweeps/auditsから構成する133 child universeを使った候補側の完全非所属証明である。

同じ49 rootの合法次手数をdet4で再計算した。BigInt BareissとLeibnizの2方式はroot安全性1,715四点組と候補次手153,988判定で完全一致。次手数は47〜77（平均60.918367・中央値62）。最小47のrootは `00000000000000821082000010800000` で2行を被覆する。49本すべてD4 orbit size 8で、root自身の対称性による枝の併合はない。これは分岐構造の測定であって探索node数・費用ではない。再現資料は[監査ログ](../../log/2026-11-19-n11-49-root-cache-exclusion-and-mobility.md)、[スクリプト](../../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_49_root_cache_exclusion_and_mobility_20261119.mjs)、[結果JSON](../../experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-cache-exclusion-mobility-20261119.json)。標準11×11空盤・二石root・S2・class 1/2/4は引き続き **UNKNOWN**。


## 2026-11-19 追記: 49-rootの二手先frontierとroot間D4共有

K0001/K0868の整数det4規約で49本を二手先まで展開した。BigIntの三項余因子展開と六項Leibniz展開を28,553個の3点組×121点（3,454,913件/方式）で照合し、全49本の一手候補集合も既存mobility censusと一致した。対象rootは2行被覆48本と1行singleton 1本。2,985個の8石子は全て28〜73手を持ち、終局子は0。順序付き二手目146,118件は、順序交換を除いた9石局面73,059個に対応する。

各root内では9石frontierのD4重複は0。49本横断では73,059 membershipが72,756正準類にまとまり、303類だけが別rootと共有された（0.4147%、全て2 root共有、213 root pair）。最大共有はroot 00000000000000801202020001001000 と 00000000010000809002000040100000 の47類で、各frontier 1,061/1,707類・和集合2,721類。共有hex一覧は結果JSONに保存。最小一手分岐47のroot 00000000000000821082000010800000 は二手先でも最小881局面で、最初の小probe候補を維持する。ただしこれは実DFPN費用ではない。

浅い9石層での共有cache利得は限定的（重複0.415%）。最大共有pairを同じworker/cache shardに寄せる余地はあるが、深い層の共有率は未測定。8石子に終局がないことは即時勝ち手がないというだけで、rootのLOSSを意味しない。新しいverdict/certificate/receiptはなく、11×11空盤・二石root・S2・class 1/2/4はUNKNOWNのまま。詳細は研究ログ、再現スクリプト、結果JSONを参照。


## 2026-11-19 追記: 49-root二手先frontier再現器の修復とNode実行確認

再現スクリプトには検査配列の構文誤り、未定義の出力変数、JSON schema不一致があり、そのままでは実行不能だった。さらにGit blob SHA-1のheader区切りが二重エスケープされ、NUL byteではなく文字列 `\0` を渡していた。これらを修正し、検査名・分析基準headも出力JSONと一致させた。

接続Proxmox runner `kyouen-80f-runner`（1 vCPU、4 GiB RAM、Node v22.23.5）で、固定commitからスクリプトと入力6ファイルを取得。6/6のGit blob SHA-1 pin、`node --check`、Node実行2回、15/15 checks、既存JSONとのbyte-identicalを確認した。2回目の実行時間は7.297秒。修正版スクリプトblobは `1ac095ee7e6378d6520cb360a58a1797ea86b90a`、結果JSON blobは `f631574b5701bd8f441d2c552ba001814246ef69`、結果JSON SHA-256は `2e50e310936ba4ac5aa0adc9a11f4fbc579b8ce4828e79ead649348cff7ad646`。詳細は[修復・実行ログ](../../log/2026-11-19-n11-49-root-two-ply-reproduction-repair.md)。

これは49候補rootの二手先構造の再現性検証であり、DFPN探索ではない。303共有類（0.414733%）は9石層だけの重複で、深い探索のcache利得や実測費用を示さない。新しいWIN/LOSS verdict、certificate、receipt、manifest閉鎖は0。49本は候補rootのまま。標準11×11空盤、二石root `{49,60}`/`{59,60}`、S2 `{59,60}`、class 1/2/4は **UNKNOWN**。


## 2026-11-19 追記: 49-root三手先frontierとD4共有

49本の候補rootを7石から三手先の10石層まで正確に展開した。各9石局面の合法三手目を全列挙し、追加3点を座標番号の昇順 \`p<q<r\` で一度だけ数える。安全性は部分集合に遺伝するため、各安全10石集合はこの順序で一意に生成できる。各rootの9石局面数は、既存二手先JSONの49件すべてと一致した。

- 49 rootからの9石局面は73,059個。全て合法な三手目を持ち、各局面の合法三手目数は14〜68。
- 9石局面上の合法三手目は合計2,771,088件。順序を除いたraw 10石集合は923,696個（各10石集合は、その3つの9石部分集合から各1回ずつ数えられるため総数は3倍）。
- root別にD4正準化すると923,586類で、root内のD4重複が110件（rawの0.011909%）。9石層ではroot内重複0だったので、D4による併合は10石層で初めて現れた。
- 49 root横断のD4類は912,933。root間重複membershipは10,653（root別D4類membershipの1.153439%）。9石層の303/73,059（0.414733%）に対して2.78116倍。
- 多重度は1 root共有902,297類、2 root共有10,619類、3 root共有17類。347組のroot pairが重複し、最大は \`00000000000000801202020001001000\` と \`00000000010000809002000040100000\` の851類。9石層での最大47類の18.106倍。
- 2手先frontier順位と3手先D4類数順位のSpearman相関は0.990816。ただし30/49 rootで順位が変化した。最小候補は引き続き \`00000000000000821082000010800000\`（一手47候補・9石881局面・10石D4類8,420）。

最大共有pairを同じworkerの共有表へまとめる価値は、9石層だけの監査より強くなった。ただし、これは10石層までの幾何学的なD4重複であり、実DFPNの探索費用・深い局面での表参照率・証明可能性を示さない。49本は候補rootのままで、WIN7-D10証明書ではない。

検査は13/13 PASS。BigIntの三項余因子展開と六項Leibniz展開を142,059個の3点組×121点（17,189,139点検査）で照合し、49 rootの1,715四点組も全て非零。最小構成の作業木で \`node --check\` と実行2回を行い、gzip結果はbyte-identical。script Git blob SHA-1 \`9967afadca27a9dc02a8dd07364d466f2c23da86\`、script SHA-256 \`4360a8e41f03a6e10ed82c3f3b188916e8611b9a1633e57c1efad4c112494531\`、圧縮JSON Git blob SHA-1 \`f5854dcc74554829525f2d973dceaecf1882bc27\`、圧縮JSON SHA-256 \`5a91e3b95c1a4bb628c47dbf50be280eed3cbda4465a7a0ad811e7a90629f517\`、展開JSON SHA-256 \`b57da15406f29e4059ed42f08486c9966ebfab02d07df08fdbc8f456cb5d2e8f\`。

実行環境は接続runner \`pve:199\`（Debian 13、Node v22.23.5、1 vCPU・4 GiB）。C++ compilerがないため、この回はDFPNを実行していない。新しいWIN/LOSS verdict、certificate、receipt、manifest閉鎖は0。REFUTED-D10はLOSS証明ではなく、標準11×11空盤・二石root・S2・class 1/2/4は **UNKNOWN** のまま。
