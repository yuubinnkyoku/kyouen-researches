---
id: K1041
title: "第5・第6 WIN7-D10 receiptのbase鎖fold・5親target 25/112更新とK1039/K1040 sweep join後の候補被覆再解決（stranded 57・旧plan-dependent行の3行復帰と1行再stranded化）"
kind: computation
status: computed
topics: [certificates, verification, search-methods]
aliases:
  - n11 fifth/sixth WIN7 receipt fold into the base fold chain
  - five-parent target 25/112 after the fifth/sixth receipts
  - K1039/K1040-aware cover re-solve over the 87 residual rows
  - recovery of three of the four K1038 plan-dependent stranded rows
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
  note: base→first→second/third fold連鎖・117root候補プール
- type: depends_on
  target: K1035
  note: 第4 WIN7-D10証明書・28-root witnessのcompanion REFUTED 2
- type: depends_on
  target: K1036
  note: 第5・第6 WIN7-D10証明書（.n11正本・per-root双検証・bareiss audit・summary・legal move lists）
- type: depends_on
  target: K1038
  note: 第4fold後のfrontier・残余89行refold・stranded 40行分類
- type: depends_on
  target: K1039
  note: K1033 28-root witness全面sweep（WIN 3・REFUTED-D10 25・CAPPED 0）
- type: depends_on
  target: K1040
  note: 残り3未試験witness rootのdepth-10 sweep（全root REFUTED・K1038 26-root witness全root判定完了）
- type: supports
  target: K0865
  note: 5親target 23/112→25/112行の被覆簿記更新（行のLOSS証明ではない）
artifacts:
- path: research/experiments/n11-head1410-fifth-sixth-win7-receipt-fold-20261119/scripts/fold_fifth_sixth_win7_receipts_20261119.mjs
  role: source
  note: fold機械。両証明書をピンBigInt/Bareiss検証器で本環境ライブ再検証し、verdict全域join（284/160）でWIN/LOSS衝突0を確認してから2 receiptを鎖にfoldする
- path: research/experiments/n11-head1410-fifth-sixth-win7-receipt-fold-20261119/scripts/refold_cover_after_fifth_sixth_receipts_20261119.mjs
  role: source
  note: 両receipt fold後の残余87行の候補被覆再解決機。K1036 fold verdictとK1039 sweep（25 REFUTED）・K1040 sweep（3 REFUTED）をjoinし、stranded構造分類と旧stranded行の行き先照合を含む
- path: research/experiments/n11-head1410-fifth-sixth-win7-receipt-fold-20261119/output/fifth-sixth-win7-root-receipt-fold-20261119.json
  role: data
  note: fold実行の機械可読結果。frontier 6,226→6,224行・492,970→492,830・solved 1,622→1,624・parent incidence 11,855→11,852
- path: research/experiments/n11-head1410-fifth-sixth-win7-receipt-fold-20261119/output/fifth-win7-independent-verification-rerun-20261119.json
  role: data
  note: 第5rootの本環境ライブ再検証。54/54 subroots・127,080 states・16,170 terminals・124,176 edges・K1036出版値完全一致
- path: research/experiments/n11-head1410-fifth-sixth-win7-receipt-fold-20261119/output/sixth-win7-independent-verification-rerun-20261119.json
  role: data
  note: 第6rootの本環境ライブ再検証。55/55 subroots・66,292 states・10,905 terminals・59,089 edges・K1036出版値完全一致
- path: research/experiments/n11-head1410-fifth-sixth-win7-receipt-fold-20261119/output/refuted-excluded-cover-refold-after-fifth-sixth-receipt-20261119.json
  role: data
  note: K1039/K1040 join後の残余87行再解決。eligible 32候補・witness 18 root・stranded 57行（53 structural・4 plan-dependent）・旧40行の照合（37維持・3 matched復帰）
- path: research/log/2026-11-19-n11-fifth-sixth-win7-receipt-fold-cover-refold-witness-sweep-join.md
  role: log
  note: 両receipt fold・再解決・K1039/K1040並走検出とjoinの全経過
scope: >-
  標準11×11 head-1410の5親target 112行のうち第5・第6 WIN7-D10
  receipt（K1036証明書のroot 00000000000000805202080001000000・
  00000000040000801202000080100000）による各1行閉鎖の簿記反映と、
  K1039全面sweep・K1040残り3-root sweepのverdictをjoinした残余87行の
  候補被覆再解決・stranded行の再分類。二石root・空盤・クラス全体の
  勝敗は対象外。
evidence: >-
  開始時main d3a6e69fee8ce7873e21499e0dac999313b97b1e（K1038の
  出版commit）。実行中に並走のK1039（51f474141ac7・28-root全面sweep）と
  K1040（e3cd0499af91・残り3 root sweep）の出版を順次検出したため、
  refoldは両sweep JSONをpinしてjoin対象に組み入れた（K1039のsweep
  JSONはgit blob SHA-1 a4e5d6f8…3134、K1040のsweep JSONは
  82adcae0…535d）。全入力をGit blob SHA-1で照合: fold4記録
  38715413…・refold4記録 791e6be7…・K1036の.n11正本
  b072170a…/02ea43b3…（展開後SHA-256 69589e76…/5289f152…）・
  per-root検証JSON 433e59f1…/f9819aa3…・bareiss union audit
  3e5bcc80…/564e8201…・summary 9e71ab4e…・legal move lists
  b5b8fb2d…・両pin検証器 62b5d941…/2960afab…。fold機械は
  base→first→second/third→fourthの既存fold鎖を全ピン再計算で再構成し
  （frontier 6,226行・492,970でK1038記録と一致）、出版verdict全域を
  joinして第4receipt WIN 1＋companion REFUTED 2を加えた284/160を
  K1038 refoldのverdict_poolと crosscheckした上で、第5・第6rootが
  REFUTED証拠・既foldのいずれにもないことを確認して両receiptをfold
  した。fold前後で両証明書を本環境で独立再検証: BigInt 3×3余因子と
  4×4 Bareissの両方式で第5root 54/54 subroots（55,857行・127,080
  states・16,170 terminals・124,176 loser edges・消費union差分0）、
  第6root 55/55 subroots（30,984行・66,292 states・10,905 terminals・
  59,089 edges・union差分0）、両方式の状態流量完全一致、K1033の
  cover-resolve witness plan行との独立一致、K1036のper-root検証・
  bareiss audit・summaryの全出版値と完全一致。fold結果: 第5rootは
  S6行1行 00000000000000805202000001000000（5親target 1行）、第6rootは
  00000000020000809002000040000000（同1行）を各閉鎖、combined closed
  edge cost 140、5親target 23/112→25/112（残余89→87行）、frontier
  6,226→6,224行・492,970→492,830、solved S6 1,622→1,624、parent行
  incidence 11,855→11,852。foldは3回実行（別cwd含む）・refoldは
  2回実行し、いずれも出力byte-identical（fold記録 SHA-256
  6ecdfdcc…・refold記録 bfa76a33…）。K1039/K1040 join後の再解決:
  verdict全域は310 REFUTED/162 WIN（K1039の25 REFUTEDは既知companion
  2の再現＋新規23、K1040の3 REFUTEDは残り未試験root全部で新規3。
  WIN 3はK1035/K1036証明書rootと完全一致）。117root poolはrefuted
  79・WIN receipt 6を除きeligible 32候補。残余87行: pair edge
  17・singleton行 8・最大マッチング12（24行）＋singleton witness 6の
  witness 18 root計30行被覆（lower bound 44）・未試験witness 18
  root。stranded 57行の再分類: 53行structural（残余32候補に被覆
  providerなし。候補拡張・depth>10・他の閉鎖機構が必要。数学的閉鎖
  不能証明ではない）＋4行plan-dependent（matchable 0。任意の最大
  基数マッチングで被覆されないが、eligible候補が被覆し
  残るためdepth-10 WIN7 receiptで閉じ得る）。K1038のstranded 40行と
  の照合: 37行stranded維持、旧plan-dependent 4行のうち3行
  （00000000000000043800000008080000・
  00000000000000801202000001000200・00000000020003800000048000000）
  は本再解決の計画でmatchedに復帰、残る1行
  00000000000040809002000000100000 は再びstranded化（plan-dependent。
  唯一のeligible provider 00000010000000801202040000000400 は未試験の
  まま本計画にも採用されず、行を除去した部分グラフの最大マッチング
  ＋1が全体最大と一致しないことから、いかなる最大基数計画でもこの
  行は被覆されないと実測）。57−37=20行は本鎖で初めてstrandedと
  なった行（K1038計画では被覆providerを持ち、K1039/K1040のjoinで
  24 rootがREFUTED確定したことにより主としてproviderを失い、残余
  32候補内の再編成でも被覆されなかった）。これはK1040が予告した
  「K1038 26-root witnessプール内のdepth-10 receiptでは残47行は
  閉じ不可」の行別実測と整合する。REFUTED-D10は7石rootの
  depth-10内先手勝ちなし判定でありLOSS証明ではない。receipt foldは
  行被覆の簿記であり、二石root・クラス全体の勝敗を確定しない。
  標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4
  はUNKNOWN。
---
