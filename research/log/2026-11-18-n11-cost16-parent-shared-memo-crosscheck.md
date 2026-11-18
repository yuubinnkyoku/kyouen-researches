# 2026-11-18 N11 cost-16 parent の B 型総数・共有memo独立照合

## 背景

開始時のmainは `e5f2fab7b7004a79d6352e087c02230c5b5baf9e`。AGENTS.md、research/knowledge/README.md、K0863/K0865/K0868、head-1476のparent census・class-2 cover、rank-1再照合、cost-16 phase-B group設計logを確認した。

checkpoint commit `d2901d15a6bd23bb2d4096322c237c002f684bca` は、31行parent `00000000000000003800000008001000` の phase B を31個の独立fresh-memo sliceで計算し、B16 = 660,663,050,386,546,968 と記録していた。ただしそのcommitはscriptのみで、最終JSONとlogは未出版だった。従来のgroup runnerは47/425 pair typeまで進んだ後、作業環境のfilesystem rollbackで中間JSONLを失っている。

## 独立再計算

入力5件をGit blob SHAで固定し、全てmain上のpinと一致することを確認した。

- worklist-1410: `2fee1d0718547a62e346d35f5858d7913e37c097`
- K0865 census: `9c251da3138c5cb0516e097be5e5d35ab4f26a5d`
- fold ledger 1410→1476: `e8785d509e8a11a37c0d03cc450455a14708c34d`
- parent cover table: `4e4a911d0e05779437d4a8e97685a8feb66c0d25`
- phase-A output: `fe4b4b559fd8c3fdc9bc9b9f40a048fc3217c55b`

worklistからD4 parent包含で31行を再抽出し、66 fold-closed行と35 STERILE行を除外した。各行の合法候補を整数det4で再列挙し、edge costと31/31一致した。

| 構造 | 再計算値 |
|---|---:|
| 対象S6行 | 31 |
| 候補出現数 | 2,333 |
| D4正準root | 1,908 |
| 1行を覆うroot | 1,483 |
| 2行を覆うroot | 425 |
| pair typeの重複度 | 全て1 |

B型を、二重被覆される行dごとに
`B_d = Σ_{a<b in N(d)} w(d,a)w(d,b) pm(V minus {d,a,b})`
と分解した。checkpointの31 fresh-memo sliceとは異なり、今回は**31個のd slice間で1つのmemoを共有**した。これにより同じ部分マッチング状態を繰り返し計算せず、B全体を9,226,801状態で計算できた。Aの31行pmも同じmemoから再計算した。

## 結果

**18/18 checks PASS**

- A16 = **2,305,787,291,293,934,388**。既刊phase-Aの31行全pm値と31/31一致。
- B16 = **660,663,050,386,546,968**。checkpointの値と完全一致。
- 最小cover総数 A16+B16 = **2,966,450,341,680,481,356**。
- 31個のB_dは276〜435 anchor、合計11,267 anchor。
- 共有memoはB終了時9,226,801状態、A終了時9,226,842状態。上限12,000,000以内。
- fresh memoを2個作った再計算で、31個のB_d・anchor数・memo状態数が全て一致した（同一Python実行環境内の独立memo再計算。別プロセス実行とは主張しない）。

checkpointのB16総数を、異なるmemo共有方式で再現できた。31個の独立sliceがそれぞれ約352万状態を要するという既存測定と比べ、共有memoでは重複する部分状態の再計算を避け、全体の状態挿入を約923万に抑えた。

## 成果物・再現境界

- verifier: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/crosscheck_cost16_parent_shared_memo_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost16-shared-memo-crosscheck-20261118.json`
- output Git blob SHA-1: `b70689ea6b2177b2a86909939737f57c5ed637c9`

実計算は、GitHubから取得した上記pin一致入力から抽出した31行を使い、利用可能なPython実行環境で2回実施した。公開verifierはrepo checkout上で5入力pinから行集合を再抽出し、候補列挙・共有memo計算・二重再計算を行う標準ライブラリのみの再現用scriptである。今回の実計算をrepo checkout上でこのscript自体から実行したとは主張しない。

## 解釈境界・次の作業

これは**最小cover計画の組合せ数**の確定であり、探索費用・engine verdict・WIN7-D10証明書ではない。S5 parentは閉じておらず、新しいWIN/REFUTED verdictも発生していない。REFUTED-D10とSTERILEはLOSS証明ではない。

次の実探索優先は、head-1476で11行/806候補・757 D4 root・最小6 root cover 337,020通りと判明したbest own-closable class-2 parent `00000000000000403800000008000000`。このcover集合から既存coordinatorの実測費用で6本を選び、選ばれたrootだけを探索する。今回のcost-16 parentを次のengine targetへ繰り上げない。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべて**UNKNOWN**のまま。
