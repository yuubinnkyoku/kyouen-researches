---
id: K1270
title: "低z banded window extension (z∈{0,1}・min(X)>=2): H(m+1;X;0)=v(ΣX,0,m+1) かつ H(m+2;X;1)=v(ΣX,1,m+2)（選択肢集合一致による全称証明・K1268 予想C1 の z=0/z=1 行の解決）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "low-z banded window extension: for every m>=2 and every nonempty finite multiset X with min(X)=m, the unified-window collapse extends exactly one step past W(z,m)=max(z+m,2) on BOTH low-z rows: H(m+1;X;0)=v(sumX,0,m+1) and H(m+2;X;1)=v(sumX,1,m+2), for all shapes and all arities; resolves Conjecture C1 of K1268 on the z=0 and z=1 rows (band condition z<z*(m) holds automatically there since z*(m)>=2>1)"
  - "proof technique: option-set matching. On the z=0 slice every A-move child collapses to the single value v(sum-1,0,m) (K1264 window edge for untouched-min children; induction on m with the K0832 R<=2 base for decremented-min children), so parent options form a singleton identical to the single-token side's options and both mexes coincide ((m+1) mod 2). On z=1, m>=3, the child values {v(sum-1,1,m+1)} plus the C-child 1 XOR v(sum,0,m+1) (via the z=0 slice) match the single-token side's option set exactly; the m=2 base is closed by lemma LW (min-1, exactly one 1, budget 3 at z=1 classification: {1}->1, sum>=3->2)"
  - "boundary sharpness: min=1 is necessary (T1/K1267 at z=0, T2/K1269 at z=1 separate at R=3); z<=1 is optimal (z=2, m=2 is the frontier z*(2)=2 with published witness (2,2)@R*=5, parent 2 vs single 1, re-checked in D0b)"
relations:
- type: extends
  target: K1268
  note: "K1268 が open problem として登録した予想 C1（m>=2・z<z*(m) で R=z+m+1 の全 X 崩壊＝階段定理窓の banded 拡張）のうち z=0 行・z=1 行を全称証明で解決。残る z>=2 帯（クリティカルストリップ z*(m−1)<=z<z*(m)）は open のまま。"
- type: depends_on
  target: K1264
  note: "階段定理窓 R<=z+min(X)（z=0/z=1 の窓端等式が本証明の A手子評価に直接使用）・残余ゲーム再帰の定義。エンジンは出版 verifier 鎖（K1264→統合窓 0ab66665…→本機体 dda422f2…）から sha-gate 機械抽出。"
- type: depends_on
  target: K0832
  note: "R<=2 全z 条款（z=0 slice の帰納底 m=2 と LW 分類・窓端アンカー）と単一トークン閉形式 v。"
- type: related
  target: K1267
  note: "境界の鋭さ: min=1 では窓+1 の z=0 が T1 で分離するため min>=2 仮定は鋭い。"
- type: related
  target: K1269
  note: "境界の鋭さ: min=1 では窓+1 の z=1 が T2（K1269）で分離するため min>=2 仮定は鋭い。LW 分類は T2 の {1}^t（全トークン1）と対比される（LW は「ちょうど1個の1」帯・値の一様性の源）。"
- type: related
  target: K1265
  note: "{1,1} 全R崩壊定理（min=1 アリティ2 の特異性）と本項目の min>=2 banded 拡張は残余ゲームの窓構造の相補的な面を与える。"
artifacts:
- path: research/experiments/ones-multiset-t2-lowz-banded-20261123/report.md
  role: proof
  note: M2（本項目）・LW の機械照合構成と監査結果・境界の鋭さ・beyond census の正本記録。証明は宣言ノート（単一オーナー・publish-then-execute）に機械実行前に全文開示。
- path: research/experiments/ones-multiset-t2-lowz-banded-20261123/verify_ones_multiset_t2_lowz_banded.py
  role: verifier
  note: "専用機体（SHA-256 dda422f28f646821b4ec1529cac45837d5b4694246bb465f081a7beba1be9bdd）。D2/D3/D3b/D4 電池: m=2..14 形状電池+乱数・深部 m=15..25・LW 分類・固定 seed 300 deep probe。"
- path: research/experiments/ones-multiset-t2-lowz-banded-20261123/output/audit.json
  role: data
  note: "監査正本（SHA-256 ea5467c3198931e16691efccf4eeeb118de50aed96845cb6870250550b5e0a27・総照合 64,200 比較 bad 0・4実行 byte-identical）。"
- path: research/log/2026-11-23-ones-multiset-t2-lowz-banded-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 9ceb96d0・M2/LW 証明全文の先行開示を含む・publish-then-execute）。
- path: research/log/2026-11-23-ones-multiset-t2-lowz-banded.md
  role: log
  note: run log（宣言・実行・D0c 事前登録値訂正の誠実記録・census 観測・K番号確認）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰）について、全ての m>=2 と min(X)=m を
  持つ空でない任意の有限多重集合 X（全形状・全アリティ）に対して
  (z=0) H(m+1;X;0)=v(ΣX,0,m+1) と (z=1) H(m+2;X;1)=v(ΣX,1,m+2) が成立する
  という全称命題（proved・選択肢集合一致による強帰納・機械照合 64,200 比較 bad 0）。
  z>=2 帯・窓+2 以上の一般保証・min=1 行は範囲外（min=1 は T1/T2 により窓+1 で
  分離）。beyond（窓+2）census の z=0 全陰性・z=1 m=2 の親2 一様帯は観測記録で
  あり本 item の主張ではない。標準11×11の空盤・二石root・S2 {59,60}・class 1/2/4
  は範囲外かつUNKNOWNのまま。
