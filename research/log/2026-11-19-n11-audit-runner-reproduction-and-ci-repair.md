# 2026-11-19 n11: 49-root監査の別環境再現と証明書CI差分の確認

## 基準

作業前に最新main `a4bef2aaf318a64a9eea03f572b2f7225c612650`、root `AGENTS.md`、`research/knowledge/README.md`、K0863/K0865/K0868、および直近の49-root監査ログを確認した。branchやPRは作成していない。

## 1. 5親97行・49-root監査の再実行

mainの再現スクリプトと4入力を固定blobから取得し、隔離した作業用ディレクトリで実行した。実行環境はDebian 13 x86_64、Node.js v22.23.5、1 vCPU・4 GiB RAM。並列実行はしていない。

- スクリプトblob: `337b12ac086ddafaca262f12c14a375591c7c799`
- K0863 scan: `24f214e6a9dd721ef95ac97d6b84cf34af33b14b`
- 49-root residual witness: `a8eaf00bd6494eda50a68e7d06498bed833a7688`
- scan generator: `44f188fbff846754de0ea4fe4da1c5f771a6805d`
- K0868 convention: `b097210d0b49d7cf014cc6a554298b1e49e83384`

結果は **16/16 checks PASS**。49本のうち48本は全7削除子のD4 orbitが133 child universeに存在せず、残る1本だけがchild `00000000000000801222000000800000` のbit 74に対応したが、そのbitはopen。従って公開済み8,964 engine verdictと115 transferに対して49本すべて未判定、という従来結果を再現した。

合法次手数も47〜77、平均60.918367、中央値62。最小47手のrootは `00000000000000821082000010800000`。出力はmainの公開JSONとbyte-identicalで、SHA-256は `e73828856761300fe7167b0c36766c090f247b54c1783d1a9a174721bcf47b23`。

これは同じ公開スクリプトを別環境で再実行した再現確認であり、第二の独立実装による監査ではない。作業用の隔離ディレクトリを使い、リポジトリcheckoutや既存のdirty checkoutは変更していない。

## 2. cost63f第三独立証明書監査のCI差分

main `a84969a6b537a4108c181bce59726db485d0d0dc` のCIで、cost63fの第三独立証明書監査はJSON比較がbyte 2020 / line 59で失敗していた。再実行するとbit 85/91の両証明書、manifestのbytes・MD5・SHA-256・Git blob SHA、戦略行、合法応手、終局、D4親liftはすべて通過した。

- bit 85: 40,154 rows、root mobility 51、visited 87,882
- bit 91: 29,305 rows、root mobility 49、visited 64,688
- 合計: 69,459 rows、visited 152,570、loser reply edges 144,626、terminal 20,962
- D4 parent orbit: 13（14 deletion edgesのうち共通childを1軌道に統合）

旧JSONとの差は `baseline_closed_parent_orbits` のオブジェクト内キー順だけで、キー順を正準化したJSONは完全一致した。再実行2回の出力もbyte-identicalで、生成JSONのSHA-256は `e355824620747f5a29a0b757db6ecde401e0917759f9856ca1593dc31a37e10b`。

この出力はコミット `c59d428c5e7ff2679d4e3be11e360e3e303dd86a` で同期済み。現在のmain上のJSONは再生成結果とbyte-identicalである。証明書本体・verdict・receiptは変更していない。

## 3. knowledge workflowのK0947出力差分

同じmainのknowledge workflowはK0947で停止していた。検証器をPython 3.13.5で再実行すると6,382,085 checks、failures 0、2回のbyte-identicalを再現した。旧audit JSONとの違いは配列の整形と末尾改行だけで、JSON値は完全一致。検証器の正規出力はコミット `38829177fc8c544c3f00cdd86d1dbce07b8186c6` で同期済みで、現在のmain上のJSONは再生成結果とbyte-identicalである。

## 4. 解釈と未解決性

今回の実行は監査の再現性とCI出力の同期を確認したもので、新しいWIN/LOSS verdict、WIN7-D10証明書、receipt、S6 manifest閉鎖は作っていない。49本は引き続き探索候補であり、47手という値は合法次手数であってDFPNの探索費用ではない。

REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。
