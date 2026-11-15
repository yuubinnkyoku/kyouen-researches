# 2026-11-15：cost-78a WIN7証明書5/5出版とreceipt fold — chain head 1216→1222

開始時main: `f0db5bb28`（cost-67c第三独立監査着地直後。canonical chain head 1216/6631/523382/4901/387105）。AGENTS.md、`research/knowledge/README.md`、K0783、直近のn11 log・experimentを確認した。規約どおりmainを直接更新し、branch / PRは作らない。

## 対象

第3 coverable class-2 target S5 `00000000000000809102000000000000` のcost-78 child `00000000000000809102000000400000`（stones [9,59,60,61,89,93]・edge cost 78・需要 c1=0,c2=2,c4=0）。head-1216でS5は3行/221（69/74/78）を持ち、78行がこのchild。並走レーンがsweep（78候補・5 WIN7-D10 bits 8,20,29,36,109・73 REFUTED-D10・0 capped・184,253,822 nodes）と証明書2件（bit36/bit20）を公開済みで、残り3件（bit29/bit8/bit109）が未出版だった。

## 証明書3件の抽出

`cert_driver78a.ts`（repo-verbatim抽出器 `class4_child1_cert_extractor_exact_v16.ts` をimport・空kill table `pref=null`・chunk rows-only）で、rootの全loser初手を1プロセスでblind抽出した。

| bit | root | mobility | rows | extraction nodes | 時間 |
|---|---|---:|---:|---:|---:|
| 29 | `00000000000000809102000020400000` | 58 | 56,463 | 16,395,724 | 158 s |
| 8 | `00000000000000809102000000400100` | 62 | 75,033 | 25,476,207 | 228 s |
| 109 | `00002000000000809102000000400000` | 68 | 88,039 | 27,863,969 | 240 s |

全move `ok:true`・`capped:false`・`fbt_drops:0`・terminal range [13,17]。`assemble_cost78a_certificate_20261115.py` で行をsort -uし、header 2行を付与。1.75 MiB超のため `split_certificate_at_line_boundary_20261115.py` で行境界2分割した（bit29: 2,040,418 B→1,020,232+1,018,186、bit8: 2,715,416 B→1,357,711+1,357,705、bit109: 3,178,041 B→1,589,023+1,589,018）。

## 二重独立検証（5/5 PASS）

- **BigInt 3x3余因子**（`verify_win7_certificate_bigint_independent.mjs`・solver/verdict cache/repo検証器importなし）: 5/5 PASS。sub-roots 59/64/58/62/68、union missing/extra 0/0、terminal [13,17]。
- **Number Bareiss 4x4**（`verify_bit7_win7_cert.ts --root-check --subroots <全合法手> --consumed-out`）: 5/5 PASS。consumed union == 証明書行集合（missing/extra 0/0）、root mobility == sweep の opponent_legal_replies。
- 既公開bit36/bit20はworking treeのCRLFをLFへ正規化したgit blob内容で再検証した（TS検証器は`\n`のみでsplitするため、CRLFのままではheader検査に落ちる）。bit20は2 partのLF連結が公開whole md5 `348871fd605dedeb34b5a4c4ad6f518c`・whole blob `379a49fc8daaee024547d2beb356618299101d7c` と一致。

`build_cost78a_certificate_manifest_20261115.py` がmanifest `class2-lane-cost78a-win7-certificates-20261115.json`（blob `b07370843588d42a04ffca6252dac87d23fc1cb9`・15,366 B）を生成: **5/5 certificates・326,698 rows・11,806,510 bytes・97,619,220 extraction nodes・311 sub-roots・31 distinct parent-lift orbits**。全証明書のD4親orbitはcanon不変でchildを含む。

## receipt fold（head 1216 → 1222）

`recompute_frontier_cost78a_receipts_20261115.py` はcost-63g fold scriptをrunpyで再実行してhead 1216/6631/523382/4901/387105をbyte-identicalに再現し、cost-78aの25入力ファイル+claimをgit blob shaで照合した後、公開順 [36,20,29,8,109] で5 receiptをfoldする。

- 新canonical head: **`1222/6625/522908/4895/386631`**（solved 1216→1222、in-manifest marginal 6、raw marginal 26）。
- child `00000000000000809102000000400000` は**bit36**で閉鎖（全rootが自身の追加石削除でchildをcover）。
- 第3 target S5 `00000000000000809102000000000000`: **3行/221 → 2行/143**（残り69/74）。
- 第2開親 `00000000000000801202000100000000`: **79行/6539 → 73行/6065**（child+5親orbitを喪失）。
- best class-4 blocker S5 `00000000020000003800000080000000` は **18行/1460不変**。best class-2は第3 target（2行/143）。
- zero-mim receiptなし。set等式 `s_after == s_1216 ∪ covers(5 roots)`、root disjointness（112 folded rootsとraw/D4両方で交差0）、sweep audit再導出（78候補・pilots 3402×10・determinism rerun node-exact・v15 5/5 WIN+3/3 refuted anchors sum 64,742,220・pilots 5949×2）、manifest totals再合計をすべてassert。
- 出力: head JSON（blob `c1c0f0a42f919b63cb33f27736b0a884443413c6`・10,572 B）、ranking CSV（`fac7bd27bfc2aa79f771c6ff4e6e87c14780d1f5`・7,580 B）、top-candidates CSV（`99f9760810551cefc4cb32ecd4c6a24b9c66d5a7`・6,039 B）。claimはcompletedへretireし、fold記録・出力blob・再現コマンドを記載。completed claim後の再実行で3出力のbyte-identityとfold数値を再assertする制御を追加した。

## 実行環境上の注意（再現性）

- このcheckoutはWindows + `core.autocrlf=true` のため、公開chain scriptが前提とするLFと異なる。fold scriptは `Path.write_text` をLF固定にmonkey-patchし、証明書・manifestはCRLF→LF正規化してからhashする。作業前にoutput配下のtext fileをLFへ正規化し、`git add --renormalize` でindex statのみ更新した（内容差分なし）。
- chain scriptの一部はrepo外のローカル作業ディレクトリを前提とする。`output/cost72b-certs/` に `class2-lane-cost72b-certificates/` のpartをコピーし、cost-63g bit113は公開2 partを連結したwhole `bit113-root-00020000080000801202000000200000.cert` をローカルに用意した（いずれも未追跡・公開物はpartのまま）。これらはchainのbyte検証をローカルで通すための再構成であり、公開証明書の内容を変更しない。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書は各7石rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- child orbitの閉鎖は両S5親の残り行からchildを除くが、どちらのS5も未解決のまま。第3 targetは残り2行（69/74）で、両行とも並走レーン（69g/74e）の担当。
- 証明書木そのものの再走査は本foldの範囲外。manifest記載の二重独立検証（BigInt + Number Bareiss）に依拠し、foldはbytes・root同定・sub-roots・終端範囲・親orbit・D4正準性を再検証した。

## 並走・次の一手

- cost-67c（bits 64/96証明書公開済み・fold未）・cost-65l（bits 21/48・証明書本体未公開）・cost-69g/65j/74e/74fは本foldに含めない。次のfoldは新head 1222へのrebaseが必須。
- 第3 target S5の残り2行のうち69はcost-69g、74はcost-74eが担当。両方がWIN7 receiptで閉じれば、第3 target S5が先手WINとなりclass-2 blockerが条件付きで閉鎖される。現時点では未fold。

## 勝敗

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、類2・類4はすべて **UNKNOWN**。今回のfoldは勝敗判定を変更しない。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost78a_receipts_20261115.py
```

runpyチェーン全体（63g→63f→76a→…）を再実行し、head 1216のbyte-identical再現から全制約を再検証した上でfoldする。実行時間は約15分。
