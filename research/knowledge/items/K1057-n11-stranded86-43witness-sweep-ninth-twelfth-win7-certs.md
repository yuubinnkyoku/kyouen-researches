---
id: K1057
title: "残余86行のadd-one-stone候補拡張censusと43-root witness掃引（WIN 4・REFUTED 39・CAPPED 0）・第9〜第12 WIN7-D10証明書と4-receipt fold（frontier 6,222→6,213行/492,688→492,021・solved S6 1,635・5親target 34/112）・resolve5は残余78行を39 pair witnessで完全被覆（stranded 0）"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - add-one-stone expansion census over the 86 stranded five-parent target rows (universe 8,663, fresh-safe 5,142)
  - 43 witness-root depth-10 sweep (4 WIN7-D10 / 39 REFUTED-D10 / 0 capped / 0 ordering conflict, 173,165,148 nodes)
  - ninth to twelfth WIN7-D10 strategy certificates (roots 00000000000000801202000001040200 / 00000000000000821082040200000000 / 00000000000000821092200000000000 / 00000000001020003800000048000000)
  - ninth-twelfth receipt fold and post-twelfth cover resolve5 (39 fresh pair witnesses, 0 stranded)
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定規約
- type: depends_on
  target: K0007
  note: ranked AND/OR certificateの構造と検証境界
- type: depends_on
  target: K0865
  note: head-1410の5親targetとS6 receipt簿記
- type: depends_on
  target: K1046
  note: 117-rootプールdepth-10完全判定・残余86行strandedの設定（本項はその候補拡張）
- type: depends_on
  target: K1033
  note: base→first→second/third fold連鎖とReceipt/Cover機構
- type: supports
  target: K0865
  note: 5親target 26/112→34/112行の被覆簿記更新（行のLOSS証明ではない）
artifacts:
- path: research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/census/output/add-one-stone-expansion-86-rows-20261119.json
  role: data
  note: 86行census正本（universe 8,663・fresh-safe 5,142・pair完全被覆43・二回実行byte-identical・SHA-256 6fe87d61ebf9676d3847c85b16982566a7d0c867e8746dbe6a87871cca153897）
- path: research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/sweep43/output/witness-43-root-depth10-sweep-20261119.json
  role: data
  note: 43-witness掃引分類正本（WIN 4・REFUTED 39・CAPPED 0・conflict 0・nodes総計173,165,148・pilot_d6 86/86合格）
- path: research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/cert-9th/win7-root-00000000000000801202000001040200-20261119.n11.gz.b64
  role: data
  note: 第9 WIN7-D10証明書正本（84,928行・3,069,801 bytes。正本テキストのSHA-256 503ff9dadc7a0d52cba8d75fa185273c798811e2ca1a897eee98cbd2b6cce631。3.0MBを超えるためgzip+base64の561,188 bytesとして出版。`base64 -d <…>.gz.b64 | gunzip` で復元するとSHA-256が上記pinと一致）
- path: research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/cert-10th/win7-root-00000000000000821082040200000000-20261119.n11
  role: data
  note: 第10 WIN7-D10証明書正本（45,450行・SHA-256 6ba50576f3f9500d0b11ffa4a47231255e9968af40e6dcb0330c09a58fc6d426）
- path: research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/cert-11th/win7-root-00000000000000821092200000000000-20261119.n11
  role: data
  note: 第11 WIN7-D10証明書正本（24,375行・SHA-256 c68e63752392d17002e4d2447b23f0f98da55348400b952c0f8dbff269a6b566）
- path: research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/cert-12th/win7-root-00000000001020003800000048000000-20261119.n11
  role: data
  note: 第12 WIN7-D10証明書正本（26,756行・SHA-256 6513b7d57ace489764b7c863025487b2d14313e134153a1460a039578287e37a）
- path: research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/ninth-twelfth-win7-receipt-fold-20261119.json
  role: data
  note: 4-receipt fold正本（frontier 6,222→6,213/492,021・solved S6 1,635・5親target 26→34/112・verdict universe 379/168）
- path: research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/post-twelfth-receipt-cover-resolve5-20261119.json
  role: data
  note: 残余78行カバー再解決正本（matching 39・witness 39・stranded 0・次回掃引の条件付き計画）
scope: >-
  標準11×11 head-1410系の残余86行（five-parent target 26/112時点）に対する
  add-one-stone候補拡張census、43-witness掃引、そこから得た第9〜第12 WIN7-D10
  証明書の抽出・二重独立検証、4-receipt foldへの反映、残余78行の再解決まで。
  二石root・空盤・クラス全体の勝敗の確定は対象外。
evidence: >-
  （1）census: K1046のresolve4状態（残余86行・プール完全判定済み）から、各行に
  1石追加したD4正準形7石rootのuniverseを全列挙し安全フィルタ・既知verdict
  （340 REFUTED/164 WINの明示pinned source結合）を適用した。universe 8,663
  （in_pool 98・既知REFUTED 7・既知WIN 0・fresh 8,558 = safe 5,142 + unsafe 3,416）。
  既存8 WIN receiptは86行を0行被覆。multi-cover（≥3行）のfresh-safe rootは
  存在せず、pair候補（835 edge）のみ。maximum matching 43が86/86行を完全pair被覆
  （witness 43 root・各2行。greedyなら46本）。census JSON二回実行はbyte-identical。
  実行はexpand86.py --with-sweep（sweep28 verdictの取り込みにフラグ必須）。
  （2）掃引: 43 witnessをrunner v17（blob c132cc64…）・depth 10・cap 30M・
  両AND順序でprobeし86 probe全件のpilot_d6制御が合格（loss=false・3,402 nodes）。
  分類はWIN 4（第9〜第12）・REFUTED 39・CAPPED 0・順序矛盾0・総nodes 173,165,148。
  生probe記録（probe-records-w0/w1.jsonl）と分類正本を出版。分類は生記録から
  出版後に独立再導出しても完全一致した。probe driverは生maxbit childのみを通す
  （K1046のcanon_hex事故規約の継承）。
  （3）証明書: 第9 root 00000000000000801202000001040200（72合法手・抽出
  3,765,226 nodes・84,928行・終局[13,17]・fbt_drops 0）。第10 root
  00000000000000821082040200000000（56・2,536,415・45,450行）。第11 root
  00000000000000821092200000000000（47・702,661・24,375行）。第12 root
  00000000001020003800000048000000（51・834,730・26,756行・added_bit 84）。
  法定手リストは独立再導出（win_legal_gen.json）。各証明書をBigInt 3×3余因子
  展開（昇格行列式[x²+y²,x,y,1]・浮動小数点なし）と4×4整数Bareissの二重独立検証
  で確定: 第9は72/72 subroot・状態171,066（winning 110,087/losing 33,569）・
  loser応手edge 153,450・terminal 27,410、第10は56/56・96,862（62,415/18,511）・
  86,443・15,936、第11は47/47・56,207（36,361/11,330）・51,440・8,516、第12は
  51/51・61,065（39,578/12,296）・55,923・9,191。4枚ともunion差分0/0・
  cross-method状態流量一致・certificate_union_exact true。抽出は検証二回実行
  （verify-w0/w1.log）で確認。.n11テキスト正本のSHA-256はartifacts欄の通り
  （第9は3,069,801 bytesのためgzip+base64形態 .n11.gz.b64 で出版、復元でSHA一致）。
  （4）fold: 4 receiptで9 S6行（target 8行＋第10のextra 1行
  00000000000000801082080400000000 cost 80）を閉鎖、closed_edge_cost 667
  （第9 163・第10 227・第11 133・第12 144）。9行は全て8-D4像から独立再導出し
  各行が閉鎖前にopen・receipt間で重複なしをgate検証。結果: frontier 6,222行/
  492,688 → 6,213行/492,021・solved S6 1,626→1,635・parent incidence 11,848→
  11,826・s6_needed_by_open_classes 4,517→4,513・5親target 26→34/112（残余78行）・
  fully-closed parent 0。verdict universe（明示pinned source結合）は
  340/164 → 379/168（WIN/LOSS矛盾0。8,964 cache全体との結合ではない）。
  fold実装はbase frontier（6,222/492,688）の再計算からopen連鎖を逐步照合した。
  （5）resolve5: 第12fold後の残余78行について、86行censusと同じ規則（生候補列挙・
  安全フィルタ・既知verdict 379/168除外）で再解決。universe 7,969（in_pool 93・
  既知REFUTED 46・fresh 7,830 = safe 4,728 + unsafe 3,102）。既知168 WIN receiptは
  78行を0行被覆。39本のREFUTED witnessは全て78行universe内に現れ、4本のWIN
  witnessは閉鎖済み8行のみを被覆していたため正しく不在（両gateを明示検証）。
  multi-cover 0本・pair edge 706・maximum matching 39が78/78行を完全被覆、
  stranded 0・witness計画39本（greedyなら42本）。
  この39 witnessは未判定rootの条件付き掃引計画であり証明書ではない。
  （6）構造観察: censusの43 pair witness→4 WIN（8行閉鎖）+39 REFUTEDのdeflation後、
  残余78行はちょうど39 fresh pairで完全被覆された（43→39）。REFUTED witnessの
  担当行はすべてfresh代替pairで再結合可能であり、このスコープの候補供給は
  枯渇していない。
  （7）解釈規約: REFUTED-D10はLOSS証明ではなくdepth-10内の先手勝ちなし完全探索
  のみを意味する。foldは行被覆の簿記であり行のゲーム理論的値には一切言及しない。
  resolve5のwitnessは条件付き計画。stranded 0はこのスコープでの観察であり、
  depth>10や他の閉鎖機構の不存在を意味しない（むしろ本項は行閉鎖の進行を
  記録するもので閉鎖不能性とは無関係）。標準11×11空盤・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。
---