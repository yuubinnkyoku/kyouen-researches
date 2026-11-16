# 2026-11-16：cost-64g 並走sweep・証明書成果の独立再実行検証 — 59/59 node-exact・bit89証明書byte-identical・BigInt/Bareiss両再検証PASS・census v3 transfer効果一致・VERIFICATION PASSED

開始時main: `4ecadd43`（cost-64g win1 certificate commit 07:56Z）。対象は、並走レーンが07:49〜07:56Zに着地させた**cost-64g（cheapest open class-2 candidate S5行 `00000000000100003800000008080000`・child `00000000000100003800000008080000`・stones [19,27,59,60,61,80]・cost 64・59 open candidates・5転送済みREFUTED [5,29,104,111,119]）のsweep成果** — census v3（blob `47174799`）→ claim v1（blob `895b0cfc`）→ claim v2 completed NOT-STERILE（blob `c899b52d`・WIN bit 89のみ・58 REFUTED swept・nodes 33,505,865）→ raw batch 8本 → win1 certificate（git blob `1d2cc167`・win1 manifest blob `e30be681`）。64g foldは本log時点で未着地（claim v2上でdeferred per protocol）。本レーンはfoldに着手せず、**並走と完全に独立に同一行を再実行し、全数値を照合する第二独立検証**を実施した。claim v2の `chain_head_at_claim` はhead **1438/174/6410/507143/4683/371057**（blob `e11f31f3`・commit `2d3052df`）を正しくpinしておりstale-baselineなし。

## 検証内容（出力 `output/class2-lane-cost64g-independent-parallel-rerun-verification-20261116.json`・schema `-v1`・blob `2a54e087`・全チェックPASS）

### 独立並行sweep（repo-verbatim runner v16・8バッチ7×8+3・4並列2ウェーブ）
- 並走の成果公開後、本セッションが同じhead-1438 rankingから同一59 open bit集合を導出し、raw CDNから取得した**main収載のrunner v16そのまま**（depth 10・cap 10⁹・pilot_d6 3402を全バッチ冒頭で実行・全PASS）で独立sweep。engine状態は候補ごとに完全リセット。
- 結果: **WIN7-D10 = bit 89のみ**（690,457 nodes）・REFUTED 58・capped 0・総nodes 33,505,865・全bit terminal [13,17]・andclose全true — claim v2と完全一致。
- 並走出版raw batch 8本との照合: **59/59 bitがbit/loss/nodes/capped/terminalStoneRange全項目で完全一致**（過不足・不一致0件・総nodes同一・pilot全3402）。
- determinism rerun（batch 3 = 最重bit 43含む8 bits）: ローカル第2実行で8/8 node-exact。
- v15 cross-engine: pilot 5949 PASS・bit 89 WIN両方向一致（v15 1,760,287 nodes vs v16 690,457 — node比はengine版特性・verdictが比較対象）+ REFUTED anchors bits 1/43/118 verdict一致。

### bit 89証明書の独立盲抽出とbyte-identical照合
- published generic blind driver `cert_driver65j.ts`（45手・`legal_candidates.py`の再列挙とbit-exact一致）+ repo-verbatim `class4_child1_cert_extractor_exact_v16.ts`（empty kill table）で**証明書を一切参照せずに盲抽出**: 30,373 rows・1,278,418 extraction nodes・fbt_drops 0。
- 組立whole証明書が**並走出版証明書（git blob `1d2cc167b2212c2df6cb85c99f91d244cba4be55`）とbyte-identical**（1,096,891B・md5 `8845801d6b5ad57df9de0a29cd0066f1`）。
- 独立検証器2種を本セッション環境で再実行: **BigInt検証器（3×3余因子展開・repo importなし）PASS**（union 0/0・45 sub-roots・winner 44,932・loser 14,916・terminals 9,172 [13,17]・visited 69,020）と **Bareiss検証器（`verify_bit7_win7_cert.ts --cert --root-check --subroots`・exit 0・root mobility 45）** — 両verifierの全統計量が一致。

### census・parents・64f harvest転送の独立再計算
- head-1435 v2 presweepの64bit表を**独立D4 canon実装**（8変換辞書順最小・audit64f_cache.cjs d4CanonHex由来のPython移植）で64/64再検証PASS。legal_candidates.py再列挙も64/64 bit-exact。
- 64g行の親をD4-canonicalized one-stone-removal joinで特定: `00000000000000003800000008002000`（class-2・rows 30・edge cost 2081）と `00000000000000801202010000000000`（class-2・rows 50・3631）— 並走census v3と一致。
- 64f harvest（3 WIN7 + 61 REFUTED）の転送効果を独立計算: **64g行への追加転送0（59 openは不変）**・runner-up cost-65行 `00000000000000801202010000800000` にbit 51（canon `0000000000000080120a010000800000` REFUTED）の1件 — **並走census v3（blob `47174799`）と完全一致**。

## 意義

1. cost-64g行の全確定（64/64候補: WIN7-D10 bit 89 + REFUTED 63 = swept 58 + transferred 5）が**並走と独立の第二環境で全数値レベルで再現可能**であることを確定。以後の64g fold着地と監査は本verification record（blob `2a54e087`）をpinできる。
2. WIN7-D10証明書bit89について、**盲抽出→byte-identical→BigInt/Bareiss二重独立検証**という完全な再生成チェーンが第三者環境で成立。foldの入力となる証明書はrepo公開物のみから独立検証可能。
3. census v3の転送簿記（64g行0件・cost-65行bit 51の1件）が独立実装で一致 — 64f fold harvestの正確性を副次確認。
4. WIN7-D10 nodesのv15/v16比率（bit 89: 1,760,287/690,457 ≈ 2.55×）はv16枝刈り改善の実測例として記録に値する。

## 解釈境界（重要）

- WIN7-D10証明書は7石root `00000000020100003800000008080000` から深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。NOT-STERILEは当該行の閉鎖不能表明であり勝敗決着ではない。
- solved 1438はmanifest被覆の簿記であり、64g fold着地までchain bookkeepingは不変。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4は引き続きUNKNOWN**。

## 今後

- 64g fold onto head 1438は並走のin-flight作業（着手禁止）。着地検知→census・claim・raw・証明書・本verification recordをpinした監査へ。
- 次target選定（cost-65行 `00000000000000801202010000800000` 等）は並走census v3依存。重複回避のため本レーンは新規claimを作らない。
