# 2026-11-19 n11: 第5・第6 WIN7-D10 receiptのfold・K1039/K1040 sweep join後の5親target再解決

## 開始時点

開始時の最新mainは `d3a6e69fee8ce7873e21499e0dac999313b97b1e`（本レーンによるK1038出版: 第4 WIN7 receipt fold・5親target再解決・stranded 40行分類、12:13Z）。AGENTS.md・knowledge README（出版版）およびK1035・K1036・K1038・K1038 refoldの記録を確認した上で、K1036が「foldは未実施」と明記していた第5・第6 WIN7-D10証明書のreceipt foldを今回の対象に選んだ。branch / PRは作らず、mainへ直接反映する。

## 入力pinの取得と照合

raw GitHubのcommitピンからbytesを取得し、Node `crypto` でGit blob SHA-1を計算して全照合した。

- 第4fold記録 `38715413`・K1038 refold記録 `791e6be7`（残余89行・stranded 40の直前状態）
- K1036出版の両証明書 .n11正本: 第5root `b072170a`（2,017,673 bytes・SHA-256 `69589e76e5d2e5f22e6992929f38d9fd67f07ce1bd9fe9e3f971d32bdd635a49`）・第6root `02ea43b3`（1,117,575 bytes・SHA-256 `5289f152e88072d716f22d42414222162facb7486d07fd024b61fdc50ddef885`）
- per-root検証JSON `433e59f1`/`f9819aa3`・bareiss union audit `3e5bcc80`/`564e8201`・summary `9e71ab4e`・legal move lists `b5b8fb2d`
- 両pin検証器 BigInt `62b5d941`・Bareiss `2960afab`（fold鎖の既存pinと同一）
- それ以前のfold鎖全pin（worklist・ledger・census・global/cost fold群・first fold tarball・49-cover・head1476・cost78c/79c/73j・48-root sweep・fold23・coverResolve・witnessProbes）はK1038で照合済みのものを再照合
- 実行中に検出した並走出版物のsweep JSON: K1039の28-root全面sweep `a4e5d6f8ef180b0b7910ea90bf240c1a3a773134`（commit 51f474141ac7）・K1040の残り3-root sweep `82adcae089ceb88241cd3ec96d98cf2c9800535d`（commit e3cd0499af91）

## 両証明書のfold機械とライブ再検証

`fold_fifth_sixth_win7_receipts_20261119.mjs` を作成し、fold4機械の構造をそのまま踏襲してbase→first→second/third→fourthのfold鎖（frontier 6,226行・492,970・solved 1,622・parent incidence 11,855をK1038記録と全一致で再構成）に第5・第6receiptを接続した。fold前にverdict全域をjoinして衝突scan: 282/159（pre-K1035）→ 第4receipt WIN＋companion REFUTED 2で284/160（K1038 refoldのverdict_poolと数字一致）、第5・第6rootがいずれの既知verdictにも現れないことを確認。

本環境でのライブ再検証（fold機械の内部ゲートとして実行）:

- 第5root: BigInt 54/54 subroots PASS・55,857行・visited 127,080・terminal 16,170・loser edges 124,176・消費union差分0・終局石数13〜17。Bareiss 54 subroots・consumed 82,983/unique 55,857・状態流量がBigInt方式と完全一致。K1036のper-root検証JSON・bareiss audit・summary56.verification.fifth の全出版値と完全一致。
- 第6root: BigInt 55/55 subroots PASS・30,984行・visited 66,292・terminal 10,905・loser edges 59,089・union差分0。Bareiss 55 subroots・consumed 42,537/unique 30,984・状態流量一致・K1036出版値完全一致。
- 両rootとも coverResolve（K1033）の28-root witness plan該当行・root_checks・legal move lists 54/55も独立照合。第4rootのlegal bits 53もリスト内で再照合された。両rootの covered target rows が plan行とbyte一致（1行ずつ）。

## receipt foldの実行

fold-complete一発通過。第5root（root `00000000000000805202080001000000`・added bit 71・54合法手・総nodes 5,121,073）はS6行 `00000000000000805202000001000000` を、第6root（`00000000040000801202000080100000`・added bit 90・55合法手・931,581 nodes）は `00000000020000809002000040000000` を各1行閉鎖（いずれもK1033 plan行どおり、非target行の追加閉鎖なし）。combined closed edge cost 140。

frontier: 6,226→6,225→6,224行・残cost 492,970→492,908→492,830・solved S6 1,622→1,623→1,624・parent行incidence 11,855→11,854→11,852。5親target簿記は23/112→25/112（13+2+2+4+2+1+1）、残余89→87行。witness plan（K1033框架）の未試験rootは25→23。3回実行（別cwd含む）でfold記録はbyte-identical（SHA-256 `6ecdfdcc5ea96f4c80d6500bdc82cc26905f02b5f9b7d028e9b64d1b42f13964`）。

## 実行中の並走出版（K1039・K1040）の検出とjoin

fold実行後のmain再確認で、並走レーンが2件を順次出版した。

1. **K1039**（`51f474141ac7`・12:17Z）: K1033 28-root witnessの全面depth-10 sweep。WIN 3＝第4/第5/第6rootとK1035/K1036証明書root完全一致・REFUTED-D10 25（内新規23）・CAPPED 0・順序矛盾0。
2. **K1040**（`e3cd0499af91`・12:22Z）: K1038の26-root witnessのうちK1039で未判定だった残り3 root（`00000000000000403800000008100020`・`00000000020000801202000100100000`・`00000000000000889002000080100000`）を同protocolで判定し、3 rootすべてREFUTED-D10。これでK1038 witness 26 rootの全root判定が完了（WIN 2＝第5/第6root・REFUTED 24・CAPPED 0）。

両sweep JSONをraw CDNのcommitピンから取得してGit blob SHA-1照合の上、refold機械のverdict join対象に組み入れた。K1039で検出した時点でrefoldをK1039 join版に拡張済みだったが、K1040検出により今度はその3 REFUTEDもjoinする3度目の拡張を行った（いずれの版も出版前のため、最終版のみを出版する）。

## 並走sweep join後の候補被覆再解決（resolve3相当）

verdict全域は 284/160 → K1039の25 REFUTED（既知companion 2の再現＋新規23）で 307/162 → K1040の3 REFUTEDで **310 REFUTED/162 WIN**。WIN/LOSS衝突は0（K1040の3 rootはjoin前のeligibleセット内にあり、WIN矛盾なし）。117root poolは refuted 79・WIN receipt 6を除き **eligible 32候補**。残余87行について pair edge 17・singleton行 8・**最大マッチング12（24行）＋singleton witness 6 root 計18 witness root・30行被覆（lower bound 44）**。未試験witness 18 root（K1038計画witness 26 rootとの再利用率は0/26: うち2 rootはfold済みreceipt・24 rootはREFUTEDで使用不可のため、本計画の18 rootは全て旧計画外のeligible候補から再選された）。全15 checks PASS・2回実行でbyte-identical（SHA-256 `bfa76a33bbe3b0656ba41e6e744fa1958ffe138ec24a359ac8de7f9c92deab76`）。

strandedは57行（53 structural・4 plan-dependent・plan-dependent-matchable 0）。これはrefutation joinによる計画縮小の正確な実測であり、K1039が予告した「21 REFUTED rootがK1038計画で被覆予定だった42行は本プール内providerを失う」・K1040が予告した「K1038 witness被覆49行のうち証明書つき2 WIN rootが担う2行を除く残47行は当該プール内のdepth-10 receiptでは閉じ不可」と整合する。旧K1038 stranded 40行の行き先を新規に照合した:

- 37行（旧structural 36行＋旧plan-dependent 1行）: stranded維持
- 3行 `00000000000000043800000008080000`・`00000000000000801202000001000200`・`00000000020003800000048000000`（いずれも旧plan-dependent）: 本再解決の計画でmatchedに復帰
- 57−37=20行は本鎖で初めてstrandedとなった行（K1038計画では被覆providerを持ち、24 rootのREFUTED確定で主としてproviderを失い、残余32候補内の再編成でも被覆されなかった）

旧plan-dependent 4行のうちの残る1行 `00000000000040809002000000100000` は再びstranded化した。この行の唯一のeligible providerは `00000010000000801202040000000400`（K1039が指摘した残存provider・未試験）であり、本再解決ではいずれの最大基数マッチング計画にも採用されず「行を除去した部分グラフの最大マッチング＋1＝全体最大」とならないことが実測された。すなわちK1040のjoin後は、いかなる最大基数マッチング計画もこの行を被覆せず、plan-dependent（非matchable）に再分類された。provider自体はeligible 32候補内に残るため、この行はdepth-10 WIN7 receiptで閉じ得る可能性を保持する。

「plan-dependent分類は計画依存であり、refutationで被覆に復帰し得る」（K1038で導入した解釈）は3行の復帰で実例が得られた一方、「同じjoinの別の側面で逆に再stranded化も起こり得る」ことの実例も同時に得られた。いずれも分類の解釈をさらに正確にする実測である。

## 簿記まとめ

- 5親target: 21/112（K1033時点）→ 23/112（K1038）→ **25/112**（本項）。残余87行。
- S6 frontier: 6,229→6,226（K1038）→ **6,224行**・492,830・solved 1,624・parent incidence 11,852。
- base鎖receipt: first・second・third（K1029系）＋ fourth（K1035証明書）＋ fifth/sixth（K1036証明書）の6 receipt。
- verdict全域（ピンソースjoin）: **310 REFUTED・162 WIN**・衝突0（282/159 → +2companion+4WIN/25sweep+3sweep）。
- 残ると課題: 57 stranded（53 structural）・eligible 32候補・未試験witness 18 root（被覆見込み30行）。53 structural行の閉鎖には117root pool外の候補・depth>10・または他の閉鎖機構が必要（数学的閉鎖不能証明ではない）。

## 未解決範囲・精度管理

- fold 3回・refold 2回実行しbyte-identical。両証明書のライブ再検証は本環境のBigInt/Bareiss両pin検証器で実施し、K1036の全出版値と完全一致。
- REFUTED-D10は7石rootのdepth-10内先手勝ちなし判定でありLOSS証明ではない。receipt foldは行被覆の簿記であり、クラス全体・上流rootの勝敗を確定しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はいずれもUNKNOWNのまま。**
- 次回レーンの自然な対象: (1) 未試験witness 18 rootのdepth-10 probe（K1039/K1040と同protocol・被覆見込み30行）、(2) 53 structural行に対するpool外候補生成（D4 liftの全域再列挙・depth>10把握）、(3) `00000000000040809002000000100000` の唯一provider `00000010000000801202040000000400` を含むplan-dependent 4行の直接probe。

## 採番

本項の作業開始時点でK1039は未採番だったが、fold実行後に並走レーンがK1039（28-root全面sweep、12:17Z）を出版し、refold→K1039 join拡張後にさらにK1040（残り3-root sweep、12:22Z）を出版したため、本項はAGENTS.mdのK番号規則により **K1041** を採番した（README@`e3cd0499af91` 全文照合でK1041被参照ゼロ・K1040は上記の並走sweep項目が使用済み）。
