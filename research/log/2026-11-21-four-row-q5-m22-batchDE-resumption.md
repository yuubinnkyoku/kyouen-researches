# 単一オーナー宣言: (4,22,5) class-split 掃引 batchD/batchE 再開（2026-11-21・高速レーン）

- **宣言時刻**: 2026-11-21T07:10Z（実行環境時刻・HEAD d6858a93 時点で再確認: 他レーンの同一 (4,22,5) 着手なし）。
- **レーン**: 既存実験 research/experiments/four-row-q5-m22-class-split-20261115 の掃引完結
  （前セッションの RESETUP-20261120.md が「次回実行」へ明示的に引き継いだ batchD/batchE）。
  同一レーンの続行であり、新規 (w,m,q) の取得ではない。
- **現状確認**: m22 records は 68行（HEAD 58c8d129 以降増分なし・13:04Z 2026-11-20 が最終）。
  2026-11-20T13:05Z 以降のコミットは m22 の batchD/batchE handoff 2件のみで、
  他レーンの同一 (4,22,5) 着手なしを list_commits で確認済み。
  進捗: 陽性対照 SAT + multi 7クラス UNSAT + k2/k1/k0 46枚 UNSAT + c1k3p0..p10 11枚 UNSAT
  + c0k3p0/p1/p2 の 600s INDET（既記録）。
- **作業内容**:
  1. batchD: c0k3p3..p10 直接 8枚（sat3.js、CAP=900s 壁時計）。
  2. batchE: c0k3p0 b1..20・c0k3p1 b2..20・c0k3p2 b3..20 の x2 分割 57枚
  （k-aware sat4 = repo scripts/sat4.js・CAP=900s）。
  INDET サブバケットは第3石 x3 分割で追分解する予定。SAT が出た場合は js+py
  2系統 witness 検証をして batchD/batchE を打ち切り witness band 拡大として記録する。
- **較正（本環境・実施済み）**: ctrl_4x20_c0k3p1 CNF md5 362034b2… byte-exact・
  kissat SAT 375,415 conflicts bit-exact。既出版 c1k3p3 CNF 再生 md5 25bccf63… byte-exact。
  (4,21,5) c0k3p0 --x2=1 で新旧 sat4 CNF byte-identical（13749780…）。
  c1k3p10 再実行 UNSAT 1,146,769 conflicts bit-exact。kissat 4.0.4 は md5 3a5eba83… 出版pin 一致。
- **出版予定**: records.jsonl は append-only・決着単位のこまめな増分push。
  全 UNSAT 完了なら 4×22 witness-free → witness-free幅集合 {21,22}・
  **M_{4,5} = 21 or ≥24**（K0821 監査規約）を K item（採番はpush直前3点確認）+
  実験 README 更新 + 研究log + knowledge README bullet で昇格。上界 U_{4,5}=140（K0318）は引用値。
- **衝突プロトコル**: push前に必ず最新 main を再取得。同一 (4,22,5) への先行宣言・records 増分を
  検出した場合は即時停止・記録して次回へ回す。push競合時も同様（07:02Z の d6858a93 競合は
  無関係レーンの宣言ノートであったため本レーンの内容を変えずに再pushした）。
- 標準11×11空盤には影響しない（w=4 固定幅レーン・UNKNOWN のまま）。
