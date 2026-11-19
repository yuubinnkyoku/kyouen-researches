---
id: K1046
title: "117-root候補プールのdepth-10完全判定（109 REFUTED + 8 WIN + 0未検証）・第7・第8 WIN7-D10証明書と第7/第8レシートフォールド（frontier 6,222行/492,688・solved S6 1,626・5親target 26/112・残余86行の全プール内stranded）"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - 117-root candidate pool fully depth-10 judged (109 REFUTED + 8 WIN + 0 untested)
  - seventh and eighth WIN7-D10 strategy certificates (roots 00000000040080801202000000100000 / 00000000040000801202000000100001)
  - fifth-sixth to seventh to eighth receipt fold chain
  - K1041 witness 18-root sweep fully subsumed
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
  target: K1033
  note: base→first→second/third fold連鎖・117root候補プールの設定
- type: depends_on
  target: K1035
  note: 第4 WIN7-D10証明書
- type: depends_on
  target: K1036
  note: 第5・第6 WIN7-D10証明書
- type: depends_on
  target: K1038
  note: 第4fold後のfrontier・残余89行refold・stranded分類
- type: depends_on
  target: K1039
  note: 28-root witness全面sweepの出版記録（本項はその全面再現を実施）
- type: depends_on
  target: K1040
  note: 残り3 root sweep・node数照合の基準値
- type: depends_on
  target: K1041
  note: 第5・第6fold+K1039/K1040 join後のrefold・残余87行・witness 18 root
- type: supports
  target: K0865
  note: 5親target 25/112→26/112行の被覆簿記更新（行のLOSS証明ではない）
artifacts:
- path: research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/cert-7th/win7-root-00000000040080801202000000100000-20261119.n11
  role: data
  note: 第7 WIN7-D10証明書正本（.n11テキスト・21,829行・SHA-256 7049f7cb54163ce49d640e86d079fb47ad0a3adf9aa3d2a8e40bbe4b7a85ecb3）
- path: research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/cert-8th/win7-root-00000000040000801202000000100001-20261119.n11
  role: data
  note: 第8 WIN7-D10証明書正本（.n11テキスト・39,163行・SHA-256 7e0599f7fa177a1667fc63b1c81ad1114aeca7a5bc2102c7caed81986aa04d03）
- path: research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/sweep35/eligible-29-candidate-root-depth10-sweep-20261119.json
  role: data
  note: 残余87行を覆う29候補の両AND順序depth-10掃引記録（WIN 1・REFUTED 28・CAPPED 0・nodes 28,064,341/40,873,195・canon_hex事故とK1040修復照合込み）
- path: research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/sweep6/output/probe-records-w0.jsonl
  role: data
  note: 6 zero-cover候補の掃引記録（WIN 1=第8root・REFUTED 5・CAPPED 0）w1と対
- path: research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/fourth-fifth-sixth-win7-receipt-fold-20261119.json
  role: data
  note: 第4・第5・第6foldのPython再実装記録（frontier 6,229→6,224/492,830・solved 1,624・K1041出版値と完全一致）
- path: research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/seventh-win7-receipt-fold-20261119.json
  role: data
  note: 第7fold記録（S6行 0000000000000000380000000b000000 閉鎖・frontier 6,223/492,762・solved 1,625・5親target 26/112）
- path: research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/eighth-win7-receipt-fold-20261119.json
  role: data
  note: 第8fold記録（class-2 S6行 00000000000000801202000000100001 閉鎖・frontier 6,222/492,688・solved 1,626・5親target不変）
- path: research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/post-seventh-receipt-cover-resolve3-20261119.json
  role: data
  note: 第7fold直後の残余86行再解決（witness 0・matching 0・lower bound 43・残余86行全行stranded）
- path: research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/post-eighth-receipt-cover-resolve4-20261119.json
  role: data
  note: sweep6勝敗join後の117-rootプール完全判定（pool_refuted 109・pool_win 8・pool_fully_depth10_judged true・eligible 0）
- path: research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/sweep28-repro/output/residual-28-root-witness-depth10-sweep-20261119.json
  role: data
  note: K1039 28-root witness sweepの完全再現（56 probe全件pilot合格・WIN 3=出版C/D/E receipt・C-root node数出版値一致）
scope: >-
  標準11×11 head-1410系の117-root候補プールのdepth-10完全判定と、そこから得た第7・第8
  WIN7-D10証明書の抽出・二重独立検証・fold連鎖への反映。二石root・空盤・クラス全体の
  勝敗の確定は対象外。
evidence: >-
  当初のK番号はK1045を予定していたが、出版直前の最新main再取得で並走two-tokenレーンがK1045（z=13 y=5資料群・コミット39502245f4ほか）を先に出版したためK1046に繰り下げた。前回のこのレーン実行（2026-11-19・GitHub push手段のない実行）ですべての計算を終えて
  いた未出版成果の出版。開始時main HEAD 15d54369f6e3（2026-11-19 13:10Z・n11並走レーンが
  probe_driver18.pyをmainに置いた2コミット直後）。
  （1）掃引: 第5・第6fold後の残余87行に対する117-rootプール内の被覆候補はeligible
  35（残余を覆う29＋zero-cover 6）。29候補をrunner v17（git blob
  c132cc6425eee3feaeef1d697dd74f968cfedb59・depth 10・cap 30M・両AND順序・pilot_d6
  3,402 nodes全件合格）で掃引し WIN 1（G=00000000040080801202000000100000）・
  REFUTED 28・CAPPED 0・順序矛盾0（nodes総計 28,064,341/40,873,195）。
  （2）実装事故と修復: round-1の29候補中5件でrunner生成時に child にcanon_hex
  （D4正準化）を被せたため別局面をprobeしていた。K1040出版値（root
  00000000000000403800000008100020 の 254,303/565,069 nodes）との不一致で検出し、
  生のmaxbit childで再probeしてEXACT一致を確認。5件のround-1記録はround1-quarantine/
  に隔離し判定には使用していない。K1040の3 rootはchild分解修復後に出版probe-recordsと
  nodes/loss/cappedで完全一致。教訓: probe driverは(child,bit)分解に生整数hexのみを
  通しcanon_hex(child)を禁止する。なおround-1有効24件+再probe 5件のper-root生記録は
  実行環境の消滅で失われたが、判定は組立済み分類JSON・3 rootのK1040 byte照合・
  node総計で裏付けられ、resolve3/resolve4がその結合の正本である。
  （3）zero-cover 6候補の掃引: WIN 1（H=00000000040000801202000000100001・両順序
  1,207,782/1,893,198 nodes）・REFUTED 5・CAPPED 0。よって117-rootプールはdepth-10で
  完全判定: 109 REFUTED-D10 + 8 WIN + 0未検証（resolve4 checks pass・
  pool_fully_depth10_judged true・eligible_candidates 0・明示ソース結合による全体既知
  verdictはrefuted 340/win 164）。
  （4）第7証明書（G）: 51/51合法手・抽出 552,457 nodes・21,829行・終局石数[13,17]・
  fbt_drops 0・証明書SHA-256 7049f7cb54163ce49d640e86d079fb47ad0a3adf9aa3d2a8e40bbe4b7a85ecb3
  （.n11正本で出版）。BigInt 3×3余因子展開独立検証は51/51 subroots・訪問状態 49,378
  （winning 31,910/losing 10,166）・loser応手edge 44,902・terminal 7,302・4×4 Bareiss
  union 差分 0/0・消費31,910行→unique 21,829行。
  （5）第8証明書（H）: 58/58合法手・抽出 2,655,359 nodes・39,163行・SHA-256
  7e0599f7fa177a1667fc63b1c81ad1114aeca7a5bc2102c7caed81986aa04d03。BigInt検証は
  58/58 subroots・状態 85,802（winning 55,034/losing 16,271）・edge 74,770・
  terminal 14,497・Bareiss union 差分 0/0。
  （6）fold連鎖（Python再実装・既存fold鎖を全pin再計算で検証: 6,259/495,507 →
  6,240/493,965 → 6,236/493,703 → 6,229/493,184）: 第4・第5・第6foldで
  6,224/492,830・solved 1,624・parent incidence 11,852・5親target 25/112に到達し、
  K1041の出版fold記録（mjs実装・別実行・別lane）と全数値で一致（fold実装の二重独立
  確定）。第7fold（G）はS6行 0000000000000000380000000b000000（cost 68・c2需要2）を
  閉鎖し frontier 6,223/492,762・solved 1,625・incidence 11,850・5親target 26/112・
  残余86行。第8fold（H）はHが残余86行を0行覆ったままclass-2フロンティアS6行
  00000000000000801202000000100001（cost 74・両故3402pilot合格の掃引でWINと確定済みの
  root由来）を閉鎖し frontier 6,222/492,688・solved 1,626・incidence 11,848・
  5親targetは不変。
  （7）再解決: resolve3（第7fold後・掃引45rootの結合）で残余86行はpair edge 0・
  matching 0・witness 0・lower bound 43、すなわち117-rootプールというスコープでは
  86行全行がdepth-10でstranded（候補不足情報であり数学的閉鎖不能証明ではない）。
  resolve4（第8fold+sweep6結合）がプール完全判定を正式記録化した。
  （8）K1039完全再現: 同一プロトコル（cap 30M・両順序・pilot_d6）で28-root witness
  sweepを再実行し、56 probe全件のpilot合格・3 WIN（出版C/D/E receipt rootと同一）・
  25 REFUTED・0 CAPPED・C-rootのWIN node数 3,294,339/3,953,563が出版probesC値と
  一致。
  （9）K1041 witness18の全件包含: K1041のrefoldが挙げた未試験witness 18 root
  （0000000000000004380000000a080000・00000000000000801202000001081000・
  00000000000000801202000001101000・00000000000000801202000001140000・
  00000000000000801202010001100000・00000000000000801202060000001000・
  00000000000000801212080000001000・00000000000000801222000000900000・
  00000000000000909002200000100000・00000000000000989002000080000000・
  00000000010000809002000080100000・00000000010000809003000040000000・
  00000000020000801202080000100000・00000000020080003800000048000000・
  00000000040004801202000000000080・00000000040080801202000000100000・
  00000000240000003820000000000800・00000010000000801222000000000400）は
  本掃引の29候補に全件含まれ、17 REFUTED-D10＋G（WIN7-D10・本項が証明書を出版済み）で
  ある。したがって並走レーンがmainに置いた18-root sweep driver（commits bf65d8c2・
  15d54369）の掃引対象は本項で完全に判定済みであり、その実行結果の期待値は
  上述の通りで、Gの抽出も不要である。
  （10）解釈規約: REFUTED-D10はその7石rootのdepth-10内の先手勝ちなし完全探索証明で
  あって、より早い局面のLOSS証明ではない。foldは行被覆の簿記であり行のLOSS証明では
  ない。残余86行のstrandedは117-rootプールというスコープでのdepth-10候補不足を
  意味するだけで、数学的閉鎖不能証明ではない（プール外候補・depth>10・他の閉鎖機構
  が残る）。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。
