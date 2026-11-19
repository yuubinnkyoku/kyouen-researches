# 2026-11-19 n11: 第4 WIN7-D10証明書のreceipt fold・5親target再解決・stranded構造分類

## 開始時点

開始時の最新mainは `cc8be6d6dc1df9ef87dd10aae4b9103035e82754`（K1021 z=12 y=3 verify backfill、11:31:42Z）。その直前の出版は K1035（`aa69a48723`、head-1410残余28-root witnessからの第4 WIN7-D10証明書・root `00000000000000801202060001000000`・「receipt foldは未実施」と明記）、K1034 z=15 y=3完成（`e9b7882444`）。AGENTS.md、`research/knowledge/README.md`、K0863・K0865・K1029・K1033・K1035、およびbase/global/cost fold群・49-cover・48-root sweep・28-root再解決の記録を確認した。branch / PRは作らず、mainへ直接反映する。

本レーンの今回の対象は、K1035が未実施と明記した「第4証明書のreceipt fold」。fold機械（`fold_second_third_win7_receipts_20261119.mjs`・blob `7923a0fe`）の構造をそのまま踏襲し、base→first→second/thirdのfold連鎖に第4receiptを接続した。

## 入力pinの取得と照合

Gitバイナリはこの実行環境にないため、raw GitHubからcommit `cc8be6d6` をピンしてbytesを取得し、Node `crypto` でGit blob SHA-1を計算して全て照合した。全pin一致。

- worklist `2fee1d07`・ledger `e8785d50`・census `9c251da3`・globalFold `753a4bf4`・previousCostFold `7e6144cc`
- firstFoldTarball `fa5f26a9`・49-cover `a8eaf00b`・head1476 verdict join `65d0c7ce`
- cost78c `626409d5`・cost79c `054923a4`・cost73j `74fc3417`
- 48-root sweep `37aba599`・fold23 `7923a0fe`・coverResolve `600b23d3`・witnessProbes `9cfb5c9c`
- runner v17 `c132cc64`・extractor v16 `5518d37`・BigInt verifier `62b5d941`・Bareiss verifier `2960afab`
- 第4証明書gzip `a9030a51`（gzip SHA-256 `f9bf9b2489f6bf656837579490d4b67956290132741ebae0f3d3ebe472ee7f91`・展開後1,843,284 bytes・SHA-256 `f3fcf274ee72d98f4501d104f694d679cd3301e0e161a06a22c191c89ad94bae`）

## 第4証明書の本環境での独立再検証

foldの入力とする前に、証明書をライブで再検証した。

- BigInt 3×3余因子展開: 53/53 subroots PASS・`union_missing=0`・`union_extra=0`・visited states 101,663・terminal 16,052・loser reply edges 91,807・終局石数13〜17
- 4×4 Bareiss: 53 subroots PASS・consumed records 65,610・unique 50,941・差分0・状態流量101,663/16,052/91,807でBigInt方式と一致

いずれもK1035の出版値と完全一致。この再検証はfold機械の内部ゲートとしても同じ工程を実行する（`controls.live_bigint_verification_rerun` 等）。

## receipt foldの実行

`research/experiments/n11-head1410-fourth-win7-receipt-fold-20261119/scripts/fold_fourth_win7_receipt_20261119.mjs` を作成した。構成は以下の通り。

1. 全pin入力をGit blob SHA-1照合で読む
2. base frontier（worklist/ledger/census）を再構成し、global fold・cost78c/79c receipts・first fold（tarballからJSON展開）・second/third foldを連鎖させてfold前状態を再計算
3. 出版verdict全域（head1476/cost73j transfers/sweep/global fold/first/second/third receipts、K1035分は除く）をjoinし、第4rootのWIN/LOSS衝突を検出（衝突0を確認）
4. 証明書を両検証器でライブ再検証し、K1035出版値と照合
5. 第4receiptのS6行被覆を8つのD4像すべてから再導出し、fold前に行が開いていたことを確認
6. receiptをfold

結果（3回実行・別cwd含め出力byte-identical）:

- S6行3行閉鎖: `00000000000000801202020001000000`・`00000000000000801202040001000000`（この2行が5親target行）＋非target行 `00000000000000801202060000000000`
- closed edge cost 214（各行68・77・69）
- frontier: unique remaining S6 6,229→6,226行・sum remaining cost 493,184→492,970・solved S6 in manifest 1,619→1,622・parent行incidence 11,859→11,855
- 影響parent 2: `00000000000000003800000009000000`（残行25→23）、`00000000000000801202020000000000`（残行44→42）
- 5親target簿記: 21/112→23/112行（累計閉鎖15+2+4+2=23）。これはVERIFIED-D10の被覆冊記更新であり、行のLOSS証明ではない

## REFUTED除外後の5親target再々解決

`scripts/refold_cover_after_fourth_receipt_20261119.mjs` を作成した。K1035の30-root witness probes（WIN 1＋companion REFUTED-D10 2: `00000000000000003800000008001021`・`00000000020000801222000000100000`）をverdict joinに加え、117root候補プールからREFUTED 53・WIN receipt 4を除いて再解決した（3回実行・別cwd含めbyte-identical）。

- 残余89行・eligible 60候補・pair edge 41・singleton行12
- 最大マッチング23（被覆46行）＋singleton 3行でwitness 26 root・被覆49行・lower bound 45
- 未試験witness 26 root（全witness rootが未probe。次のdepth-10 probe対象。証明ではなく候補計画）
- 旧38 stranded全行はstranded維持（`previous_stranded_held`チェック）。K1035 companion REFUTEDにより、その候補provider経由で覆われていた行のうち2行が新規strandedとなり、stranded計40行
- K1033の旧28-root witnessのうち23 rootを新witness 26 rootで再利用し、REFUTED 2 rootを含む5 rootを除外した（`witness_sweep_plan`）。未試験26 rootは全てprobe対象の候補であり、証明ではない

## stranded 40行の構造分類（本項の新規解析）

stranded 40行の解釈を精密化した。K1033のREADME弾丸は「38行stranded（当該プール内のいかなるdepth-10候補でも閉じ不可）」と書いていたが、これは最大マッチングのplanとeligible被覆の存在性を混同した過大な記述だった。refold機械に分類を実装した結果:

- **structural 36行**: 残余89行上で被覆を与えるeligible候補が存在しない。残余プールのいかなるdepth-10 WIN7 receiptでも閉じられず、候補拡張またはdepth>10探索が必要。数学的閉鎖不能証明ではない
- **plan-dependent 4行**: eligible pair候補が存在して被覆する。この特定の最大マッチング＋singleton fallback計画では外れる
  - `00000000000000043800000008080000`（provider `0000000000000004380000000a080000`）
  - `00000000000000801202000001000200`（provider `00000000240000003820000000000800`）
  - `00000000000020003800000048000000`（provider `00000000040004801202000000000080`）
  - `00000000000040809002000000100000`（provider `00000000000040889002000000100000`・`00000010000000801202040000000400`）

plan-dependent 4行について、頂点除去再計算（当該行の頂点を除いた部分グラフの最大マッチング+1が全体最大と一致するか）による代替計画被覆可能性を判定したところ、**4行すべて代替最大マッチングでも被覆不可**（inessential vertex）。すなわち「どの最大濃度計画でも本計画同様に外れるが、provider候補自体がWIN7-D10になれば閉じ得る」。

この分類は出力JSONの `resolve.stranded_classification` に機械可読で記録した。verdict joinの周辺で分類は変わるため、次回の再解決でも常に再計算される。

実装上の注記: 最初の分類実装で部分グラフを作る際に頂点indexのcompact化が抜けているバグ（`residualRows.indexOf` が除去後でなく元index空間を返す）を出力前reviewで発見し、kept-index写像に修正した。修正後に40/40行の分類と3つの整合チェック（分類の分割・eligible被覆との一致・witnessの非stranded被覆完整性）が全passした。

## 実施しなかったこと・未解決範囲

- K1033旧解釈の修正は本項の側での精密化として明記するのみで、K1033本体のテキストは変更していない（main既存のK番号・本文は変更しない規則）。
- verdict全域joinは明示的ピンsourcesのみを使用しており、8,964-entry cacheの全joinではない（fold出力の `verdict_join_summary.join_limitation` に明記）。
- 未試験witness 26 rootのprobe・stranded 36行（structural）に対する候補拡張（span>2・depth>10・別closure機構）は次回以降の課題。plan-dependent 4行はprovider候補のprobeで閉じ得る。
- 標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれもUNKNOWN。

## 簿記まとめ

| 項目 | 第3証明書fold後（K1033） | 第4証明書fold後（本項） |
|---|---:|---:|
| solved S6 in manifest | 1,619 | 1,622 |
| unique remaining S6 | 6,229 | 6,226 |
| sum remaining cost | 493,184 | 492,970 |
| parent行incidence | 11,859 | 11,855 |
| 5親target閉鎖 | 21/112行 | 23/112行 |
| 残余89行の被覆 / stranded | （残91行: 被覆53/stranded 38） | 被覆49/stranded 40（36 structural・4 plan-dependent） |
| eligible候補 / witness | 63候補/witness 28 root | 60候補/witness 26 root |

## 出版前の並走衝突とK番号の振り直し（11:55–11:57Z）

本項のpush直前のHEAD再確認で、mainが `cc8be6d6` から `970d714f93` へ進んでいたことを検出した。並走レーンが3コミット（`52f5914482`・`f1a8dedbd0`・`970d714f93`）で「K1036 part 1〜3」として第5・第6 witness証明書を出版していた。

- 第5root `00000000000000805202080001000000`（55,857行・SHA-256 69589e76…）
- 第6root `00000000040000801202000080100000`（30,984行・SHA-256 5289f152…）

本項は当初K1036として composing していたが、AGENTS.mdのK番号規則（main既存のK番号は変更しない・衝突新規項目を再採番）により **K1037** へ振り直した。並走コミットは本項のピン入力に触れていない（3コミットともaddのみ、既存blobの変更なし）ため、本項のfold/refold出力・検証結果は全てそのまま有効である。

### K1036証明書と本項refoldの合成forecast

第5・第6rootはいずれも本項refold（cc8be6d6時点・残余89行・witness 26 root）のwitnessに含まれる。両rootの残余89行へのD4一行刈り被覆を純幾何で計算した（`forecast56.mjs` 相当の計算。証明ではなくfold forecast）:

- 第5rootは `00000000000000805202000001000000` の1行を被覆（非stranded・本計画witness割り当て済み行）
- 第6rootは `00000000020000809002000040000000` の1行を被覆（同上）

よって両receiptのfold（本項の第4foldに連鎖させる形）が完了すれば、5親targetは本項の23/112から25/112（残余87行）へ進む。stranded 40行の構造分類はverdict変化で再計算されるべきものであり、次回の再々解決で再導出する。

本項のlog内のK1036への言及はコミットSHAでも特定している。push直前のmain照合でn11側K1036 itemの出版（b111557129・items/K1036-n11-witness-fifth-sixth-win7-certificates.md）を確認したため、本項のREADME弾丸・itemは同itemにMarkdown linkする。


## push前の知識README破損の検出・複数レーンでの同時復元・二度目の再採番K1038

push準備中に以下を検出し対応した。

1. **b111557129d による知識READMEの輸送切断事故**: 並走レーンの第5・第6証明書出版コミット `b111557129d` は research/knowledge/README.md を **+2/−128** 変更していた。親コミット `851331ec3d` のREADME（229,729B・git blob SHA-1 `a64c5d8c…`）は本項の開始時snapshotとbyte一致しており、`b111557129d` 後のREADME（63,598B・blob `0ae297ef…`）はK1036弾丸行追加と同時に**末尾128行（94弾丸行の要約ブロック: K0895〜K1034 のREMO r=10..13・定理J・素数二分法・最小周期・P(C)双子素数法則・SIEVE/σ_Z系列・smoothヒット系列・t=2 q-series・z=6..15切片群）を削除**していた。コミットメッセージに削除の記載がなく、削除された要約行の移動先もrepo内に存在しなかったため、全ファイル取得時の約61.5KB切断を「最新main」と誤認してpushした事故と判断した（GitHub Appのget_file_contents系は大きなファイルでMSLResource化・プレビュー切断が発生し得ることを本項の出版作業中に直接確認済み）。
2. **本項側の復元準備**: live@1e2adea1 を基点に「本項弾丸行の挿入＋当該128行ブロックのbyte-exact復元」を含むREADMEを二通りの独立構成（旧snapshot起点・live起点）で作成しbyte一致（234,568B）、挿入分を除けばlive@1e2adea1（blob `0ae297ef…`）とbyte一致することを検証した。
3. **並走z11y5レーンの同時修復**: 本項push直前のHEAD再確認で、`fc93629b3b`（z11y5レーンが誤採番したK1036切片itemの削除）と `61010864ea`（同スライスを**K1037として再出版**＋**README union restore**＋.github/workflows/knowledge.yml修正）を検出した。`61010864ea` のREADME（233,957B・187行）の復元ブロックは本項が独立に復元を準備していたものと**byte一致**していた（同READMEは「本項復元版から本項弾丸行を除き、末尾にz11y5のK1037弾丸行を加えたもの」と正確に一致）。両レーンの独立復元が一致したため、本項のREADME反映は復元を含まず「本項弾丸行の挿入2行のみ」となる。
4. **二度目の再採番**: z11y5レーンのK1037取得（`61010864ea`・items/K1037-two-token-z11-y5-boundary.md）により、AGENTS.mdのK番号規則（main既存のK番号は変更しない・衝突新規項目を再採番）に従い本項は **K1037 → K1038** へ再採番する。K1038は README@61010864ea 全文（byte取得）で被参照ゼロ・直近採番系列（K1026〜K1037が全て判明・連続採番）と整合し空きと確認した。generated/index.md は現時点でK1035以降を含まない（旧い生成物。CI再生成は所管外）。

以上により、本項のREADME弾丸行は K1036-n11 item へのlinkと上記経緯を反映し、idはK1038として出版する。
