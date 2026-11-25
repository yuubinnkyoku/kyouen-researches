# 研究log: fold14 WIN8-D10 receipt fold root 9090022（2026-11-20）

単一オーナー宣言（commit `48ad9c7d60…`・先行出版）に基づく実行記録。
前段: 同一実行で K1108・K1109 証明書抽出と fold13（K1110・root 9840004・9 行閉鎖）を出版済み。

## 事前検証

1. **fold13 の着地確認**: `13f6cf39`（fold13 本体 5 ファイル）と `f7c2bd29`（README 弾丸・K1110 bullet）の
   SHA pin raw fetch + `cmp` で全ファイル byte-identical 着地を確認（README 389,449 bytes・K1110 bullet 1 箇所）。
2. **K 番号の採番**: README grep（K1110 まで）・items リンク・`list_commits`（K1110 まで）で K1111 の空きを確認。
3. **W14 構成**: W13（fold13 の W root）のコピー + K1109 正本・証明書。fold13 正本（SHA-256 `c2bf8051…`）を
   `fold13/output/` に pin 置きし、fold14 機の rerun gate 用に `fold_win8_root9840004.py` を格納。
   K1097 footprint の root 9090022 エントリは `intrinsic == claimed` == 4 行であることを事前確認。

## 本体実装

`fold_win8_root9090022.py`（fold13 機械の移行型・752 行・約 11.2 秒）:

- フォールド連鎖: fold11 chaining（fold11 機 rerun gate 継続）→ fold12 chaining（隔離 W 複写 rerun gate）→
  **fold13 chaining: 9 行 open 性・cost 照合・frontier_after 出版値（6,184/489,813・solved 1,664・incidence 11,775・
  s6_needed 4,492・cost_needed 356,261）・residual62 == residual65 − fold13 主張 3 行・closed target 50 を全 gate 一致**。
- **fold13 機械 byte-identical rerun gate**: W 隔離複写（shutil.copytree）+ FOLD13_W env で fold13 出版機械を再実行し、
  出力 SHA-256 が出版正本 `c2bf8051…` と一致。fold13 機内の fold12 rerun gate も再帰的に走る（計 3 段再帰 rerun）。
- K1109: 19 gate 全再検証。**g07 は gate 名ごと差し替え**（`g07_k1086_root_claimed_coverage_4rows`・`== 4` 定数・
  K1109 監査時の fail-closed 教訓を引継ぎ、4 行であることを二重に固定）。g05 mobility 50・g06 uncapped probes
  512,590/614,246・g13 nodes 6,102,650/6,102,650・g19 footprint（claimed 4 行）照合・
  証明書 byte 検証（1,082,873 bytes・29,942 行・sorted unique・header）・
  root 幾何（8石・quadruples 0・D4 正準・合法手 50 を独立再導出）。
- K1097: 27 gate・footprint partition（49 行 exactly-once・root 9090022 は intrinsic == claimed == 4 行）・
  主張 4 行が residual62 内・residual23 と不交差。
- **被覆幾何 2 方法**: (A) 8 D4像 × C(8,2) 2石除去 = 224 操作 (B) C(8,6)=28 部分集合直列挙。canonical 行集合 28 行が完全一致。
- 分類: open-frontier 5（本 receipt で閉鎖）・not-in-worklist 22・**closed-before-this-receipt 1**
  （`00000000000000003800000008003000`・過去 receipt 閉鎖済み。root 幾何に閉済み行が現れた初例）。

## 結果

- receipt は **open 5 行**を閉じた（初の 4 主張行候補 fold）:
  K1109/K1097 主張 4 行 `00000000000000801222000000001000`（cost 76）・`00000000000000801222000000800000`（cost 69・
  transfer_partial）・`00000000000000909002000000100000`（cost 79）・`00000000000000909002000080000000`（cost 69）+
  **target 外 open 行 1 行** `00000000000000889002400000000000`（cost 80）。閉鎖行 5 行すべて c2 需要行。
- closed edge cost 373・frontier 6,184/489,813 → **6,179/489,440**・solved S6 1,664 → 1,669・incidence 11,775 → 11,765
  （影響 4 parent: c2 4〔22→20・23→21・67→64・63→60〕・完全閉鎖 0）・
  5親 target 50 → 54/112・残余 62 → 58。s6_needed 4,492 → 4,487・cost_needed 356,261 → 355,888。
- win16 候補は 13 → 12 根（主張 35 行）。残余23行掃引計画（並走宣言済み）は不変。
- 出力 SHA-256 `ed3159fdb8cf2dd8884beb845cd4ef776cbc8b4b7b442d568d895cd930a13f71`。
  同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写（FOLD14_W env）1 回の 3 実行で byte-identical。

## 実装上の注記

- fold13 → fold14 の移行定数: g07 の gate 名差し替え（`3rows` → `4rows`）と `len(CLAIM) == 4`・g19 の
  `len(claimed) == 4` を、K1109 監査の fail-closed 教訓に従い二重に固定した。移行ミスは gate が即座に fail する構造。
- fold13 機の rerun gate の「隔離 W 複写」形式をそのまま継承。3 段再帰 rerun（fold14 機 → fold13 機 → fold12 機 → fold11 機）
  でも 11.2 秒に収まった。

## 解釈規約（不変）

WIN8-D10 はこの 8 石 root のゲーム木のみを証明する。fold は行の閉鎖簿記であり、閉じた行のゲーム理論的値を主張しない。
REFUTED-D10 は LOSS 証明ではない。node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
残り 12 WIN8 候補の抽出・残余 58 行の refsolve は着手時に単一オーナー宣言を要する未着手領域。
