# 研究log: fold13 WIN8-D10 receipt fold root 9840004（2026-11-20）

単一オーナー宣言（commit `d2521aa462cd…`・先行出版）に基づく実行記録。
前段: 同一実行で K1108（root 9840004 証明書抽出・45,286 行）・K1109（root 9090022 証明書抽出・29,942 行）を出版済み。

## 事前検証

1. **K1109 README 弾丸の着地確認**: 前段の実行末尾で実行した README 弾丸 push（commit `c955976291`）の
   `list_commits` での着地確認（HEAD == `c955976291・index K1109 WIN8 cert extract`）。
2. **K 番号の採番 3 点確認**: README grep（tool 結果全文 grep・K1109 まで）・items リンク grep（K1109-まで）・
   `list_commits`（K1109 まで）で K1110 の空きを確認。
3. **fold12 正本・fold12 機械・K1108 正本の取得**: 手元の抽出器材（`/home/user/work/w9840004`・K1108 の監査正本・証明書）と
   fold12 出版 W root（fold12 record `0f73795c…`）から W13 を構成。K1097 footprint の root 9840004 エントリは
   `intrinsic == claimed` == 3 行・residual65 内であることを事前確認。

## 本体実装

`fold_win8_root9840004.py`（fold12 機械の移行型・701 行）:

- チェーン全段 frontier 再計算 6,259/495,507 → … → fold10 6,206/491,497 → fold11 chaining 6,201/491,110
  （fold11 機械 byte-identical rerun gate 継続）→
  **fold12 chaining: 8 行 open 性・cost 照合・frontier_after 出版値（6,193/490,526・solved 1,655・incidence 11,790・s6_needed 4,501・cost_needed 356,974）・residual65 == residual68 − fold12 主張 3 行・closed target 47 を全 gate 一致**。
- **fold12 機械 byte-identical rerun gate（新形式）**: fold12 機械の出力先が published record と同パス
  （`fold12/output/…`）のため、W 全体の隔離複写（shutil.copytree）を作り FOLD12_W で再実行して出力 SHA-256 が
  出版正本 `0f73795c…` と一致しなければ fail-close する形に移行した（fold11 の `fold/output/` 分離慣行との違いを
  解消）。rerun 後 5.6 秒で全 gate PASS。
- K1108: 19 gate 全再検証（g05 mobility 57・g06 uncapped probes 1,143,198/1,528,656・g07 主張 3 行・g08 pilot_d6 4・
  g13 nodes 4,109,768/3,075,922・g19 footprint 照合）・証明書 byte 検証（1,640,220 bytes・45,286 行・sorted unique・header）・
  root 幾何（8石・quadruples 0・D4 正準・合法手 57 を独立再導出）。
- K1097: 27 gate・footprint partition（49 行 exactly-once・root 9840004 は intrinsic == claimed == 3 行）・
  主張 3 行が residual65 内・residual23 と不交差。
- **被覆幾何 2 方法**: (A) 8 D4像 × C(8,2) 2石除去 = 224 操作 (B) C(8,6)=28 部分集合直列挙。canonical 行集合 28 行が完全一致。
- 分類: open-frontier 9（本 receipt で閉鎖）・not-in-worklist 19。closed-before-this-receipt 0
  （worklist-but-not-open gate で chain 不整合 0）。

## 結果

- receipt は **open 9 行**を閉じた（単一 WIN8 receipt として最多を更新・fold12 の 8 行を上回る）:
  K1108/K1097 主張 3 行 `00000000000000003800000009000004`（cost 82）・`…09040000`（cost 76）・`…09800000`（cost 69・5親 target 内）+
  **target 外 open 行 6 行** `…00840004`（cost 92）・`…01800004`（cost 77）・`…01840000`（cost 78）・`…08004100`（cost 82）・
  `…08800004`（cost 79）・`…08840000`（cost 78）。余剰 6 行は単一 receipt として最多。
- closed edge cost 713・frontier 6,193/490,526 → **6,184/489,813**・solved S6 1,655 → 1,664・incidence 11,790 → 11,775
  （影響 5 parent: c4 3〔87→84・90→87・75→72〕・c2 2〔61→58・16→13〕・完全閉鎖 0）・
  5親 target 47 → 50/112・残余 65 → 62。s6_needed 4,501 → 4,492・cost_needed 356,974 → 356,261。
- win16 候補は 14 → 13 根（主張 39 行）。残余23行掃引計画（並走宣言済み）は不変。
- 出力 SHA-256 `c2bf80511e816306bbb8dcf4efb450214234f020c513386c3b3a82045f71e9ae`。
  同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写（/tmp・FOLD13_W env）1 回の 3 実行で byte-identical。

## 実装上の注記

- fold12 機械への移行は「旧変数の残置」による fail を最初の実行前に排除するため、.edit 差し替え箇所を
  open68→open65・residualSet72→residualSet65・K1106→K1108・fold 実行順序で段階確認した。
  今回は初回実行から全 gate PASS（移行定数の fail-closed 検査は g07 が 3 行定数・g05 が 57・g06 が 1,143,198/1,528,656・
  g13 が 4,109,768/3,075,922 と K1108 出版値に固定されているため、root 定数の未置換は直ちに fail する）。
- fold12 rerun gate は W 隔離複写（shutil.copytree）で published record の上書きを回避する新形式とした。
  fold14 以降の移行も同形式で継承する。

## 解釈規約（不変）

WIN8-D10 はこの 8 石 root のゲーム木のみを証明する。fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。
REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
残り 13 WIN8 候補の抽出・root 9090022 の fold14・残余 62 行の refsolve は着手時に単一オーナー宣言を要する未着手領域。
