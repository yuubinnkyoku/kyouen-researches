# 2026-11-16：cost-64h の K0863 out-of-sample 監査

開始時 main: `11077dcb52d191d2c0597cf14fdc96cea0df3db5`。cost-64h の64候補 sweep は完了していたが、23本のWIN7-D10証明書抽出とhead 1452へのreceipt foldは未完了だった。

## 独立再計算

新規のNode.js標準ライブラリのみの監査器 `audit_cost64h_k0863_out_of_sample_20261116.mjs` を追加した。既存Python監査器とは別に、BigInt Bareiss 4x4行列式・合法手列挙・D4正準化を再実装し、入力11ファイルをGit blob SHAで固定した。

- 6石child `00000000000000403800000008100000` の安全性を再確認。
- 合法候補64個を独立列挙し、claimの候補集合と完全一致。
- v16 raw batch 8本を再結合し、64候補を重複・欠落なく確認。
- v16結果は23 WIN7-D10 / 41 REFUTED-D10 / 0 capped、節点合計47,017,565、終端石数範囲[13,17]。
- 8個のpilotはすべてloss=false・3,402節点。
- 独立v15 engineは23/23のWIN7-D10を再確認。節点合計55,171,821。
- 64個の7石rootは64個のD4正準形に分かれ、WIN/REFUTED衝突0。23 WIN rootも全てD4相異なるため、今回の23証明書候補は対称性だけでは重複排除できない。

## K0863の新規行への適用確認

既存のK0863 theorem-applicability scanが列挙した35 STERILE行を、同じ独立幾何実装で再列挙した。

- 35行すべてで合法候補数が出版されたengine_refuted数と一致。
- 合法候補の合計は2,628。
- cost-64hの23 WIN rootと35 STERILE行の候補正準形集合の交差は0行。

これはK0863の新しい数学的証明ではなく、cost-64hという後続sweepが既存定理・既存STERILE censusと矛盾しないことの有限な追加確認である。D10 engine verdictの健全性そのものは独立証明していない。

## 公開物

- 監査器: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost64h_k0863_out_of_sample_20261116.mjs`
- 結果: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64h-k0863-out-of-sample-audit-20261116.json`
- 監査器の中核処理はCode Mode上で実行し、10項目すべてのassert相当検査が通過した。リポジトリ全体のknowledge check / unittest / buildは、この実行環境に完全なcloneがないため未実施。

## 次の作業と境界

23 WIN rootは全てD4相異なる。次はv16 extractorで個別証明書を抽出し、BareissとBigIntの独立検証、byte/hash固定、receipt marginalの再計算を経てhead 1452へfoldする。今回の監査自体は証明書を生成せず、manifest行も閉じていない。

Proxmox状態は確認したが、pve-hp-aioはメモリ91.5%、nixos-aio VMはIO-ERROR。pveノードには4 CPU coreと稼働中サービスがあるため、この回は長時間探索・証明書抽出を投入していない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はUNKNOWNのまま。** WIN7-D10は個別7石rootの深さ10以内の先手勝利だけを示し、REFUTED-D10はLOSS証明ではない。
