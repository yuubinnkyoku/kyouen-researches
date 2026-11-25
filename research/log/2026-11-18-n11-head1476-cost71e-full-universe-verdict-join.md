# 2026-11-18 n11 head-1476 class-2 cover universe × cost71e verdict join

## 開始時点

開始時のmainは `c56d630bd7e6a7e981de54073a5fd22f79c801cc`。`AGENTS.md`、`research/knowledge/README.md`、K0863/K0865/K0868、head-1476の757-root membership、top15 verdict-aware audit、cost71e claim/raw audit/certificate manifestを確認した。

対象はS5 parent `00000000000000403800000008000000` の11個のS6行。既存membershipは757個のD4正準root、最小6-root coverは359,610通り。既存top15 auditでは13位までの候補のうち10 REFUTED-D10・2 WIN7-D10・3未分類で、未分類はrank 1/3/8だった。

cost71eはS6 child `00000000000000c09002000000002000` の71合法候補を既に全探索し、13 WIN7-D10 / 58 REFUTED-D10 / 0 cappedを出版済みだった。今回はこの既存結果を別の757-root被覆集合へD4正準形で接続した。新しいゲーム探索は行っていない。

## 71候補の全件接続

cost71eのraw batch 1–9を全件読み直し、各 `child | bit` の7石rootをBigIntでD4正準化した。

- raw候補71/71が757-root universeに存在
- D4正準rootの重複0
- raw verdictは13 WIN7-D10 / 58 REFUTED-D10 / 0 capped
- candidate nodes 88,919,559、pilot 9×3,402、合計88,950,177 nodes
- 既存certificate manifestは13本すべてを列挙し、13/13でsubroot PASS、union missing/extra 0/0

top15の未分類3本はすべてcost71e raw結果に一致した。

| top15順位 | D4正準root | cost71e bit | nodes | 接続後 |
|---:|---|---:|---:|---|
| 1 | `00000000200000003801000080000001` | 110 | 1,191,862 | REFUTED-D10 |
| 3 | `00000000000041801202000000080000` | 86 | 658,628 | REFUTED-D10 |
| 8 | `00000000000000c09002000000002200` | 9 | 910,209 | REFUTED-D10 |

既存のtop15 statusとcost71e raw verdictの衝突は0。rank 5/7の既知REFUTED、rank 6の既知WINも同じcost71e sweepで再確認できた。rank 6のWIN rootはcost71e bit94のraw rootをD4正準化したもので、cost73iの既存証明書rootと一致する。

結果、top15全体は **13 REFUTED-D10 / 2 WIN7-D10 / 0 UNKNOWN** になった。top15が359,610通りすべての最小coverをhitする性質も再計算で再現した。

## 最小coverへの影響

既知REFUTEDのtop15 rootを除く最小cover数は次のように減る。

| 状態 | 残る最小6-root cover |
|---|---:|
| 元の候補集合 | 359,610 |
| 既知REFUTED 10本を除外 | 38,265 |
| rank 8もREFUTEDとして除外 | 33,765 |
| 13本すべてを除外 | **14,496** |

最後の14,496通りは、2本の既知WIN7-D10 rootの少なくとも一方を必ず含む。

- rank 6 root `00000000020001003810000008000000` を含む: 9,621通り
- rank 15 root `00000000000000c09002000000001200` を含む: 10,071通り
- 両方を含む: 5,196通り
- rank 6だけを含む: 4,425通り
- rank 15だけを含む: 4,875通り
- どちらも含まない: 0通り

これは「top15の既知REFUTEDを避ける」という条件だけを課した候補計画数であり、残りのrootがすべてWINだという意味ではない。top15外の742 rootはこの監査では全件joinしていない。

cost71eの13 WIN証明書が覆う対象S6行は2行だった。

- `00000000000000c09002000000002000`
- `00000000000000403800400008000000`

このうちbit94 / rank6の1本が2行を同時に覆い、残り12本は前者だけを覆う。したがって既存証明書のreceiptを正しくfoldできれば、対象parentの11行のうち2行を閉じる候補になる。

ただし、**この監査ではreceipt foldを行っていない**。cost71e claimのfold待ちは継続しており、head-1476の台帳にはcost76cとcost66i bit19のfoldまでが入っている。cost66iの残り、cost66j、cost69j等の依存foldは担当レーンの更新を待つ。今回の監査によってmanifest行が新たに閉じた数は0。

## 実行・再現

- 実行環境: dedicated Proxmox CT `pve:199`、1 CPU、`nice 10`。探索エンジンは起動せず、標準ライブラリによるraw/hash/D4/被覆DPの照合のみ。
- 初回実行はraw audit JSONのキー名を `rawPins` と誤認して停止した。正しい `raw_batch_pins` に修正して再実行し、12/12 checks PASS。
- 別実装のV8再計算でも出力JSONがbyte-identical。出力Git blob SHA-1は `65d0c7ce0200638a50db5451b11b8cb88ec64b5d`。
- 再現スクリプト自身のGit blob SHA-1: `1a2b7e35e885a935f1b6fd7dcd6b8813978e8192`

公開物:

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/join_cost71e_verdicts_into_head1476_cover_20261118.py`
- output: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/head1476-cost71e-full-universe-verdict-join-20261118.json`
- source inputs are pinned by Git blob SHA-1 inside the output; all nine cost71e raw batches are pinned individually.

scriptはcommit `801f4a4`で追加し、初回実行で見つかった入力キー名の誤りを `3b0eb6f`で修正。outputは `175bd2c`でmainへ直接反映した。branch/PRは作っていない。

## 解釈上の制限と次の作業

- REFUTED-D10は深さ10以内の先手勝ちが見つからなかったという判定であり、LOSS証明ではない。
- WIN7-D10は個々の7石rootの証明であり、S5 parentや11×11空盤の勝敗を決めない。
- cost71eの13証明書は既存manifestの検査結果を再照合しただけで、今回それらの証明書本体を再検証・再抽出したわけではない。
- 次は担当レーンのcost66i残り / cost66j / cost69j等のfold依存を尊重し、依存解消後にcost71eの13 receiptを現行headへ再基準化してfoldする。その後、対象11行の残り需要と、top15外742 rootの既存verdict/cache joinを再評価する。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。
