# n11 長期レーン: depth-11 probeコスト伸び測定パイロット: 単一オーナー宣言ノート（2026-11-20）

残余72行36-root depth-10 sweep本体は別レーンの単一オーナー作業（宣言済み）で結果はまだmainに
出版されていない。K1046レジューム以来「depth>10コスト測定」が未着手課候補のまま残っており、
log・knowledgeを検索しても他レーンの着手・宣言はない（22:39の三手先D4重複監査 c74dfd0c は
幾何測定でありdepth>10には触れていない）。

掃引結果を問わず、**出版済みdepth-10判定rootをdepth-11へ1手だけ延長したときのnodeコストが
depth-10の何倍になるか**は、次の供給判断（depth-11掃引の実行可能性・cap設定・280s timeout
の妥当性）に必要な測定であり、いかなるrootの判定も変えない。本レーンが以下を単一オーナー
として実行することを宣言する。

## 実行するもの

1. 対象rootは出版済みdepth-10判定に限定する:
   - K1069 39-live掃引の最大probe root `00000000010000809002000040000080`
     （bit 7・andclose 0・nodes 14,249,420・REFUTED-D10・出版正本のmax_probe）
   - K1069/K1070 第17証明書WIN root `00004000000000821082000000000100`
     （bit 8・両順序loss=true・nodes andclose1 1,576,372 / andclose0 2,544,178）
2. runner v17はrepo原本（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）の
   byte検証済み固定コピーを用い、cap 30M・timeout 280s・掃引と同一の引数形式・pilot_d6
   制御付きで、同一rootをdepth 10とdepth 11の両方で実行する（両AND順序・計8 probe・逐次）。
3. 深度10側は出版済みnodes値との一致をgateとする（不一致はfail-closed）。
   環境の遅さによるtimeoutは「当該環境で未検証」として記録し、不一致とは区別する。
4. depth-11側はnodes比・capped・wallを記録する。capped/timeout probeはコスト下界の
   実験事実であって、いかなる方向の証拠にもしない（interpretation guard）。
5. 出力は `research/experiments/n11-depth11-cost-scaling-pilot-20261120/` に置く。

## 実行しないもの

- 36-root sweep本体・その分類・証明書抽出・fold・行の閉鎖は掃引オーナーレーンの管轄。
- **本測定はdepth-11掃引の着手宣言ではない。** どのroot族をdepth-11で掃引するかは
  掃引結果出版後のcoordinator判断であって、本測定は供給情報を与えるだけである。
  depth-11での大規模走査は行わない。

## 解釈規約

node数はcap内で決定的（機種非依存の費用単位）。sandboxのwall時間は参考値。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
REFUTED-D10 は LOSS 証明ではない。**

（確認時HEAD: 95312bd26c）
