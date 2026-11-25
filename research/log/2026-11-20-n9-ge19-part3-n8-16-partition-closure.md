# n9-ge19 lane part3: n8-16 (8×8・16石) 完全分割探索閉鎖 — 宣言較正条件 3 の n8 段完了 (2026-11-20)

単一オーナー宣言: `research/log/2026-11-20-n9-ge19-k9-upper-decision-single-owner-note.md`
(commit `21f8610464d2711f768b5764d23b21a40295dee5`) の手法 (a) に基づく成果。
part1 (`0afda0e6`/`9a1c7a98`)・part2 (`906b893f`) に続く。**判定対象 n9-ge19 は依然
INDET のままで、本 part は K_9 への一切の主張をしない。**

## 結論（有限盤面の完全計算として）

**n8-ge16（8×8盤・少なくとも16石の安全配置の存在）= UNSAT** を、ksearch v3d
(ksearchp.js) + chunker.js による完全分割探索で確定した。

- 記録: `results/n8t16-partition-records.jsonl`（280 records）。全 275 葉 chunk が
  uncapped かつ UNSAT。SAT レコード 0。
- capped は計 5 件（[0]/[1]/[2]/[5]/[5,7]）で、いずれも子展開で空間を完全被覆し、
  capped verdict は一切採用していない。
- audit（chunker.js --mode=audit）: **complete=true / all_unsat=true / open_leaves=0 /
  nodes_total=604,101,900**。同じ state への audit を 2 回実行し ts を除く全フィールド一致
  （決定性）。
- 葉 chunk [0,1]（22,365,212 nodes）と中位 chunk [8]（18,012,396 nodes）の fresh 再実行が
  記録と sat/nodes/boundChecks/boundPrunes 全フィールド一致（再現性の直接検証）。
- ネガティブ制御: レコードを [8] の直後で打ち切り [8] を capped 化した改竄 state で
  audit は complete=false / open_leaves=269 で捕捉（fail-closed 実証）。

part1 の較正と一貫: 全体探索 probe は 220s/518M nodes で未完だったが、分割の葉総数
604,101,900 > 518M と整合する。part1 の addendum probe（v3c --min=0 で 140s/70.8M nodes
capped）とも整合（[0] は cap 内に閉じず、本 part は [0,d] 展開で閉じた）。

## 宣言受入条件 3 の位置づけ

宣言の較正必須条件「n=7/8 での既知値（K_7=14・K_8=15）の再現」のうち:

- K_7=14: part1 で n7-15 UNSAT fresh 再現（nodes 11,880,598）＋ part2 で完全分割閉鎖
  （35 chunk、audit PASS、11,880,562 nodes）＋ W7 14石 witness（part1 naive、第三系検証済み）。
- K_8=15: **本 part で n8-16 UNSAT fresh 完全分割閉鎖**（604,101,900 nodes）＋ W8 15石
  witness（part1 naive fresh、n8_ge15_strong 全節充足・det4 forbidden 0、第三系検証済み）。

よって **ksearch 系（探索系）の較正ラダー n7・n8 段は完了**。K_8=15 は既知値
（CYCLE5 完全最大探索、K0029 表）であり、本成果は同値の lane 内 fresh での独立再検証
であって新的数学主張ではない。範囲は有限盤 8×8（q=4 完全指摘・安全配置）のみ。

## 実行の実録（honest bookkeeping）

- 実行環境: 1.0 CPU / 約1GiB / Node 22、bash cap 300s（driver は wall 260s・chunk cap
  110s で小刻み実行）。marathon 本体は 2026-11-20T21:23:32Z〜21:47:29Z、6 driver 呼び出し
  （約1,437s）で queue exhausted。
- **環境リセット 1 回（~21:10Z・2 driver 呼び出しを1つの bash で連結して 300s cap 超過）**。
  消失したのは cap 済みの3レコード（[0]/[1]/[2]、いずれも inconclusive・capped）のみで、
  確定成果の消失はなし。part2（scripts・chunker・n7 記録）が出版済みだったため、出版byte
  からの再取得のみで復旧した（knowledge の「重い計算は小刻み実行＋早期 push」規約の実証例）。
- partition 統計: L1 chunk 49 件（4 capped・内 [3] 47,454,388 / [4] 47,396,393 /
  [6] 45,664,189 / [7] 45,067,790 nodes が最大級）→ L2 188 件（1 capped）→ L3 43 件（全完走）。
  最大葉は [0,2] 28,144,079 / [0,1] 22,365,212 nodes 等、すべて indexer 順（決定的）。
- 全感受性について: chunker の子列挙は計数上界 d ≤ NCELL+m−target で根から完全
  （c=49..63 は 16 石が入らない不能枝として列挙外、ksearch の aliveFuture bound と同一規則）。

## 次段（判定 n9-ge19 への残り）

1. fastsat 系の較正ゲート（n7_ge15_strong / n8_ge16_strong の UNSAT を fastsat で閉じる）
   は未達のまま。衝突率 約700/s の改善（minimization既定ON化・イベント間隔・LBD系
   再開戦略）か、長期連続実行か、plain CNF での交差かのいずれかで lab-side 検討が要る。
2. ksearch 系 n9-19: 本 part の chunk 統計（n8-16 で 604M nodes / 24 分）からの
   規模外挿は広い（[0] のみで n8 全体の 1/4 強を占める heavy-tail 構造）ため、
   n9-19 chunk landscape の probe（chunks c=0..48 の小 cap survey）を先に取る方針。
3. 両系の n9-ge19 判定一致まで、K_9 に関する主張は一切行わない（INDET 継続）。
