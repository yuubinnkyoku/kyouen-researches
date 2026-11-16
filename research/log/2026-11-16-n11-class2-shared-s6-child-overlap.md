# 2026-11-16：第二coverable class-2 S5のS7重複と第一応手共有を独立再監査

開始時mainは \`1dde798765b4b63c9e225cfd7599c68322b4c595\`。\`AGENTS.md\`、knowledge README、K0023/K0105/K0783、S2 milestone-5実験README、v12 published-chain監査、cost70g reconciliation、cost76d/77e第二独立検証を確認した。11×11の現行canonical frontierは \`1405/6443/509457/4713/373180\`。

対象は第二coverable class-2 S5 \`00000000000000801202000040000000\` と、残る6 S6行（cost64a/71d/75e/76c/76d/77e）。各S6子をD4で共通五石親へ整列した。親S5の安定化群は恒等変換のみで、各子の削除・変換対応は一意。合法手数は64/71/75/76/76/77で、既存edge costと一致した。

## 構造上の重複

- 439個のS7候補出現は、raw bitboardで **424個の異なるS7 root** にまとまる。
- **15個のS7 rootが2つのS6親から重複到達**する。全15 rootは安全で、D4軌道数も424。root hexと両出所、各rootの合法応手数は \`research/experiments/n11-class2-shared-s6-child-overlap-20261116/output/audit.json\` に全件保存した。
- 15重複rootを一度だけ探索すれば、S7 root検索を15件、第一応手辺を978件省ける。重複rootの証明書がWIN7なら、その一枚を両S6親への被覆として使える。

## 8石第一応手の重複

| S6行 | 合法手 | 無順序2手組 | 安全な8石組 |
|---|---:|---:|---:|
| cost64a | 64 | 2,016 | 1,736 |
| cost71d | 71 | 2,485 | 2,126 |
| cost75e | 75 | 2,775 | 2,319 |
| cost76c | 76 | 2,850 | 2,406 |
| cost76d | 76 | 2,850 | 2,355 |
| cost77e | 77 | 2,926 | 2,464 |
| **合計** | **439** | **15,902** | **13,406** |

各安全な無順序組 \`{p,q}\` は \`S6+p\` からの応手qと \`S6+q\` からの応手pの両方を持つ。合法応手を別途再列挙し、重複root込みで26,812本、root重複除去後で25,834本の有向第一応手辺を確認した。8石raw bitboardは12,448種類。

- 15個の重複S7 rootを除く前：\`26,812 - 12,448 = 14,364\` 回の潜在再訪（53.573%）。
- 重複rootを除いた後：\`25,834 - 12,448 = 13,386\` 回の潜在再訪（51.815%）。
- root dedup後、11,510局面は2個の異なるS7 rootから、938局面は3個から到達する。938の内訳は**2群918・3群20**。

## 独立検査

同じ列挙手順を、(1) lifted 3×3差分行列式、(2) full 4×4 Bareiss行列式の別実装で実行し、D4整列、各合法手数、各群の安全ペア数、15群間交差、15重複S7 root一覧、root重複前後の辺数、頻度分布、集計値が一致した。12,448個の異なる安全な8石局面は各70部分集合すべてを検査（871,360件）。全15,902候補ペアは零判定で早期終了しながら検査し、行列式評価は合計1,030,080回。スクリプトを2回実行し、出力JSONはbyte-identical。

## 現在の6行の確定境界

- cost64a / cost71dはWIN7-D10候補としてSTERILE。これはLOSS証明ではない。
- cost75eはローカル調整メモのみで、raw artifacts未公開。
- cost76cのin-flight claimはsuperseded head 1403を参照し、着地時に1405へre-baseが必要。
- cost76d / cost77eは4件のWIN7-D10証明書が第二独立検証済み。両receipt foldはcanonical 1405へ別レーンでin-flight。

## 探索器への含意と限界

現行 \`class4_child1_runner_v16.ts\`（blob \`0a4a86f...\`）は候補ごとにfreshEngine()を作り、raw四語占有キーのTT（2^18枠・probe 64）と禁止三点cache（2^17枠・probe 48）を候補間で共有しない。したがって、共通S5座標へ整列した424個のS7 rootを一度ずつ処理し、engineを保持すれば、理論上13,386件の第一応手再訪を再利用できる可能性がある。

これは全合法応手が探索された場合の組合せ上限であり、実測TT hit・節点削減ではない。早期打切り、深さ境界、候補順、表飽和で実際の再利用は減り得る。今回は探索・certificate foldを起動していない。cost76d/77eのreceipt foldは別レーンでin-flightのため触れていない。

## 次

15 rootを除いた424件の決定的worklistを作り、共有engine版を小さな固定部分集合で現行per-candidate版と比較する。memo hit・占有率・挿入失敗・root別節点数を記録し、WIN/LOSS一致と決定性を確認してから全件へ広げる。

**標準11×11空盤、二石root \`{49,60}\` / \`{59,60}\`、S2 \`{59,60}\`、このS5親の勝敗はすべてUNKNOWN。** この幾何監査は勝敗を決めていない。

Artifacts: \`research/experiments/n11-class2-shared-s6-child-overlap-20261116/audit.py\` と \`output/audit.json\`。

- \`audit.py\` SHA-256: \`1fff311e714e78fbb2b8e85fd2af50e31b31ed9a316fd877715d859f91eb522a\`
- \`audit.json\` SHA-256: \`9059d3ef77632f1ed8c9d5395eb431a5755949f2426c582e733b0d0851725169\`
