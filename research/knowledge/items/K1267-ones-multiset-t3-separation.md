---
id: K1267
title: "{1}^t 全アリティ分離定理 (t>=3): H(3;{1}^t;0)=0 vs v(t,0,3)=1（一様 mex 連鎖による全称証明・K1265 census の全 t 昇格）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "ones-multiset all-arity separation theorem: for every t>=3, {1}^t separates at (z,R)=(0,3) with parent H=0 vs single v(t,0,3)=1; t=2 collapses ({1,1} is the K1265 total-collapse row); proved by a uniform symbolic mex chain (paper, pre-declared in the single-owner note cf299bdd with the chain disclosed before any engine run in this lane); engine-checked both raw engines for t=3..16 (audit E2 t<=12 bad 0 + post-declaration supplementary check t=13..16, disclosed in the report)"
  - "K1265 D4 census chain extension: K1265 observed t=3..6 (t=3,4 direct-calculation; t=5,6 census-only, initial separation all at (z,R)=(0,3) parent 0 vs single 1); K1267 upgrades the quantifier to ALL t>=3 with a proof; also the two-token side witness (2,1)@(z=0,R=3) parent 2 vs single 1 makes cell (0,1) sharp via two tokens (the unified-window-only cell where W=max(z+m,2) exceeds the K1264 staircase window z+m)"
  - "T2 companion discovered during the run (NOT part of this item per the declaration's scope item 6; deferred to its own future declaration+item): for every t>=3, {1}^t ALSO separates at (z,R)=(1,3) with parent 2 vs single 0; full paper chain in the experiment report (paragraphs (a)-(f), uniform in t); engine-confirmed t=3..16"
relations:
- type: extends
  target: K1265
  note: "{1}^t census (t=2..6, z=0..16) の直接の全称昇格。K1265 は t=3,4 を「本定理・閉形式からの直接計算で確定」・t=5,6 を census 観測と区分していた。K1267 は量化子を全 t>=3 に拡張し証明で閉じた。t=2 の崩壊 ({1,1} 全R崩壊) は K1265 のまま不変・t>=3 との非対称（アリティ2の特異性）を確定した。"
- type: depends_on
  target: K1264
  note: 残余ゲーム再帰の定義・階段定理窓 R<=z+min(X)（本定理の位置は窓 z+min=1 を超えた R=3 での分離である点）・出版 witness {1}^3@z=1,R=3（本 item の (0,3) と対 E1 アンカーで照合）。エンジン・閉形式は K1264 出版検証器（SHA-256 108fdd65…）からの sha-gate 機械抽出。
- type: depends_on
  target: K0832
  note: 単一トークン閉形式 v（特に v(t,0,3)=min(3,t) mod 2 の機械アンカーとして使用）。
artifacts:
- path: research/experiments/generalx-unified-window-sharpness-20261123/report.md
  role: proof
  note: T1 一様 mex 連鎖の証明（宣言前紙面・宣言ノートに先行開示）・2トークン対照点 (2,1)@(0,3)（セル (0,1) の2トークン witness・紙面計算+E2 機械照合）・T2 同伴定理の証明と補足機械照合 t=3..16（宣言後発見・K 昇格は次回に委ねる旨の開示）を含む正本記録。
- path: research/experiments/generalx-unified-window-sharpness-20261123/verify_unified_window_sharpness.py
  role: verifier
  note: E2 T1 アンカー群（t=2..12・(2,1)@(0,3)）を含む監査機体（SHA-256 0ab66665…）。エンジンは出版 K1264 検証器から byte-exact 機械抽出。
- path: research/experiments/generalx-unified-window-sharpness-20261123/output/audit.json
  role: data
  note: 監査正本（SHA-256 b74551b7…・総照合 273,209 比較 bad 0・4実行 byte-identical）。E2 セクションが本 item の機械照合 t=3..12 分。
- path: research/log/2026-11-23-unified-window-sharpness-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit cf299bdd・T1 証明の宣言前開示を含む・先行出版）。
- path: research/log/2026-11-23-unified-window-sharpness-census.md
  role: log
  note: run log（宣言・実行・T2 発見の開示・宣言点数ドリフトの訂正記録・K番号確認）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰）の全1トークン多重集合 {1}^t について、
  t>=3 すべてで (z,R)=(0,3) における分離 H(3;{1}^t;0)=0 vs v(t,0,3)=1 が
  成立するという全称命題（proved・一様記号 mex 連鎖による紙面証明+両 raw
  エンジンによる t=3..16 の照合）。t=2 の崩壊は K1265 の {1,1} 全R崩壊定理の
  帰結。z>=1 側の同伴定理 T2（(z,R)=(1,3)・親2 vs 単一0・∀t>=3）は本 item の
  範囲外（宣言スコープ6により run 中発見のため次回の独立宣言・K item に回す。
  証明と機械照合値は実験 report に開示済み）。標準11×11の空盤・二石root・
  S2 {59,60}・class 1/2/4は範囲外かつUNKNOWNのまま。
