# 2026-11-16 n11 class2-lane: cost-65j fold v2 application audit (third implementation, remote-only)

## 目的

fold v2 (class-frontier-cost65j-receipts-recompute-20261116.json, head 1410 -> 1419, 17 WIN7-D10 receipts, 9 rows closed) を、公開成果物のみから第三実装（遠隔のみ・TypeScript・BigInt/D4正準化・整数精度）で独立検証する。特に前回未解決だった demand histogram (s6_needed_by_open_classes / cost_needed_by_open_classes) の定義を解明する。

## 方法

- worklist-1410 CSV (6,438行) と s5-closability CSV (174 parents) を取得
- parent incidence は行から各石を1つ除いてD4正準化する方法で独立導出（合計 12,274 incidences、open_parents 6,438/6438 一致）
- 合法手判定は det3 整数精度の外接円判定

## 結果 — 全チェック PASS

- C1 baseline: 174/6438/509109/505675 再現
- C2 receipt roots: 17/17（root=child|1<<bit、合法手、D4 canon、7行orbit、marginal総和61、mim総和9、zero-mim一致）
- C3 閉鎖9行: worklist上すべて win_receipt_scheduled、所有者は独立incidenceと一致、cost総和635
- C4 parent after算術: 9/9（18 incidences）
- C5 frontier総計: 6429 = 6438-9、508474 = 509109-635
- C6 child既解決前提: child 00000000000000809102000080000000 は worklist に不在、4 cover root の orbit がすべて child を含む
- C7 scheduled孤児: なし（9行すべて fold v2 で閉鎖）
- C8 次ターゲット P (24/1704)・Q (18/1238) は fold v2 の影響なし

## C9 demand histogram 定義の解明（今回の主要な新成果）

- 定義: **c1 == 0 かつ c2 + c4 >= 1**（c1/c2/c4 = 当該行を所有する class 1/2/4 の open S5 parent 数、classes は bitmask {1,2,4}）
- 証拠: cost-60c fold script の docstring「all three closed rows have c1>0, so s6_needed_by_open_classes ... are invariant」、chain の demand レコードが c1/c2/c4 を持つ（例: cost-60c child は c1=1,c2=1,c4=0）
- 第三実装で完全再現: pre 4711行/373023、post 4702行/372388、全9 bucket 一致（c2=2,c4=0: 826→817、閉鎖9行はすべてこの bucket）
- 従来の「class-2/4 owner がいれば数える」解釈 (4898/387133) との差は、c1>0 を持つ187行/14110 が open-only 定義で除外されることで厳密に説明できる
- 実務的意味: 4702行 (372388) は class-2/4 専属の残 sweep demand。c1>0 の187行は class-1 レーンとの共有行

## 次の一手

- cost-65f 残11 bits (4,15,18,23,25,28,66,79,91,101,109) の証明書抽出（実行環境復旧後、driver + repo-verbatim v16 engine）
- 次ターゲット P 00000000000000403800000008000000 (24/1704)、Q 00000000000000821082000000000000 (18/1238) の orbit sweep

## UNKNOWN 宣言

11x11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/class 2/class 4 はすべて UNKNOWN のまま。solved 1419 は manifest 被覆の簿記であり勝敗判定ではない。
