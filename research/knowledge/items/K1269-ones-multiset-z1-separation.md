---
id: K1269
title: "{1}^t z=1 分離定理 (t>=3): H(3;{1}^t;1)=2 vs v(t,1,3)=0（T2 の独立昇格・専用機体による機械照合と K item 化・t=2 は崩壊）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "ones-multiset z=1 separation theorem: for every t>=3, {1}^t separates at (z,R)=(1,3) with parent H(3;{1}^t;1)=2 vs single v(t,1,3)=0; t=2 collapses (0=0); this is the T2 companion of K1267 (T1, z=0), whose proof (uniform mex chain, paragraphs (a)-(f)) was published in the unified-window report and is now promoted to its own K item with a dedicated machine and battery (t=2..24; t=17..24 machine-checked here for the first time)"
  - "K1267 flagged T2's promotion as the next-lane task because the unified-window declaration's scope item 6 kept min=1 arity>=3 universal proofs out of that declaration's holdings; the present single-owner declaration (9ceb96d0, publish-then-execute) claimed it with no competing declaration observed at HEAD"
relations:
- type: extends
  target: K1267
  note: "K1267 の同伴定理（T2）の独立的昇格。K1267 が z=0 行 ((z,R)=(0,3)・親0 vs 単一1) を全称確定し、本項目は z=1 行 ((1,3)・親2 vs 単一0) を全称確定する。{1}^t の全 t>=3 に対する z=0,1 両行の分離が確定した。t=2 の崩壊は K1265 {1,1} 全R崩壊と整合。"
- type: depends_on
  target: K1264
  note: 残余ゲーム再帰の定義と階段定理窓 R<=z+min(X)（本定理の位置は窓 z+min=2 を超えた R=3 での分離である点）・出版 witness {1}^3@z=1,R=3（D0b アンカーで照合）。エンジンは出版 verifier 鎖（K1264→統合窓 0ab66665…→本機体 dda422f2…）から sha-gate 機械抽出。
- type: depends_on
  target: K0832
  note: 単一トークン閉形式 v（特に v(t,1,3)=0 の機械アンカー・証明連鎖アンカーの各種窓端・LW 分類の底）として使用。
- type: related
  target: K1265
  note: "{1,1}（t=2）の全R崩壊との対比でアリティ2の特異性を確定（K1267 と同じ位置づけ）。"
- type: related
  target: K1270
  note: "K1270 の境界の鋭さを与える: min=1 では z=1 の窓+1（R=3）が本定理により分離するため、K1270 の min>=2 仮定は鋭い。"
artifacts:
- path: research/experiments/ones-multiset-t2-lowz-banded-20261123/report.md
  role: proof
  note: M1（本項目）の電池構成・監査結果の正本記録。証明そのもの（段(a)-(f)）は出版統合窓 report にあり、本 report が参照する。
- path: research/experiments/ones-multiset-t2-lowz-banded-20261123/verify_ones_multiset_t2_lowz_banded.py
  role: verifier
  note: "専用機体（SHA-256 dda422f28f646821b4ec1529cac45837d5b4694246bb465f081a7beba1be9bdd）。D1 電池: {1}^t@(z=1,R=3) t=2..24・K1267 側 t=2..24 交差照合・証明連鎖アンカー (a)-(e)。"
- path: research/experiments/ones-multiset-t2-lowz-banded-20261123/output/audit.json
  role: data
  note: "監査正本（SHA-256 ea5467c3198931e16691efccf4eeeb118de50aed96845cb6870250550b5e0a27・総照合 64,200 比較 bad 0・4実行 byte-identical）。D1 が本項目の機械照合分。"
- path: research/log/2026-11-23-ones-multiset-t2-lowz-banded-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 9ceb96d0・機械実行に先行出版）。
- path: research/log/2026-11-23-ones-multiset-t2-lowz-banded.md
  role: log
  note: run log（宣言・実行・訂正記録・K番号確認）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰）の全1トークン多重集合 {1}^t について、
  t>=3 すべてで (z,R)=(1,3) における分離 H(3;{1}^t;1)=2 vs v(t,1,3)=0 が成立する
  という全称命題（proved・出版済み証明の昇格+専用機体による t=2..24 独立照合。
  t=17..24 は本機が初めて機械照合した帯）。t=2 の崩壊は K1265 の {1,1} 全R崩壊の
  帰結。z>=2 側の {1}^t 分離構造（E5 疎パターン）は本 item の範囲外。
  標準11×11の空盤・二石root・S2 {59,60}・class 1/2/4 は範囲外かつUNKNOWNのまま。
