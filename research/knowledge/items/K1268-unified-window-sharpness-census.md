---
id: K1268
title: "統合窓 max(z+min(X),2) のセル別鋭さ census: 2トークン前線法則 z*(m)=2m−2+(m mod 2)（250+16セル・例外0・observed）・陰性バンド94セル open・L1/L2 偶奇分離・K1264 C4 再集計完全一致"
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases:
  - "unified-window cell-sharpness census: for cell (z,m) (z=0..24, m=1..10) sharp means some X with min(X)=m separates at R*=W(z,m)+1 with W:=max(z+m,2); two-token scan X=(m+d,m) d<=60 (E3) plus z=25,26 x m<=8 d<=24 completion slice (E3b) gives ZERO exceptions over 266 cells to the frontier law: sharp iff m=1 or z >= z*(m) := 2m-2+(m mod 2); at every frontier cell the separating d in d<=60 is UNIQUE with witness X=(m,m) (even m) / X=(m+1,m) (odd m), parent 2 vs single (5m-3) mod 2 / (5m-1) mod 2 (=1/0 alternating)"
  - "the frontier law unifies published observations: K1264 C4's y>=9 sparsification (needs z>=2y-1, only z=17..26 inside the published z<=26 sweep), K1259-K1262's R=z+7 break-height commonality on the y=6 row (z*(6)=10), and the z-slice witnesses (12,6)@z=17..20/(14,6)@19/(16,6)@20 all sitting at z>=z*(m); E6 extends L1 m=11..20 / L2 m=11..22: L1 separates ONLY odd m (11,13,15,17,19 parent 2 vs single 0), L2 separates ONLY even m (12,14,16,18,20,22 parent 2 vs single 1); cross-parity lines collapse (parent 1=single 1 / parent 0=single 0); the single-value parity formulas (5m−1)/(5m−3) mod 2 held 22/22; the declaration's pre-registered both-parents-2 prediction was thus PARTIALLY REFUTED exactly along the parity split (falsifiable pre-registration functioning as designed, recorded non-fail)"
  - "negative band (m>=2, z < z*(m); 94 cells): after d-extension to 200 (13,160 points) and an arity>=3 battery ({m}^3,{m}^4,{m}^5,(m,m,m+1),(m,m,m+2),(m,m,2m),(m,m,m,m+1); 658 points) ZERO cells resolved: no two-token witness, no arity witness in the battery; two-token all-d non-separation inside the band is a citation-level consequence of the published universally proved y<=22 family closed forms (K1248 y<=21, K1256/K1257 y=22); arity>=3 beyond the battery is UNEXPLORED -> open problem C1 (cell-level banded window extension: does R=z+m+1 also collapse for ALL X with min(X)=m when z < z*(m)?)"
  - "min=1 arity map (E5): {1}^t t=3..8 rows separate at R*=W(z,1)+1 for z=0 and z=1 for ALL swept t (T1/T2 corroboration); deeper z sparse and t-dependent (t=3: z<=3; t=5: {0,1,3,4,5}; t=7: {0,1,3,5,6,7}; etc.); m=1 cells are all sharp via two tokens, so the {1}^t rows are an arity-structure observation (K1264 open item 4) not needed for cell sharpness; cell (0,1) is the unified-window-only cell (W=2 > z+m=1) and is sharp with witness (2,1)@(0,3) parent 2 vs single 1"
  - "fail-closed anchor: K1264 C4 published-domain boundary-census recount (y 1..8, d 0..24, z 0..26, Rb=z+y+1) recomputed independently equals the published per-y break counts 180/37/32/31/26/25/20/19 exactly; 17 published witness anchors (K1264 C5 x11 + K1265 D5 x6) reproduce exactly; audit 273,209 comparisons bad 0, tamper battery 8/8 caught, 4 runs byte-identical (audit SHA-256 b74551b7…)"
relations:
- type: extends
  target: K1264
  note: 未解決3「max(z+min(X),2) 統合窓の行ごとの鋭さの全称特徴付け」への初のセル完備 census 供給。前線法則が C4 の「y>=9 希薄化（19/675）」の統一説明（前線 z>=2y−1/(2y−2) が掃引域に対して高く付くため）。E3/E3b/E4/E5/E6 の全窓端等式照合（fail-closed bad 0）は階段定理の大規模独立再検証でもある（15,650+13,818 点・出版域の C4 再集計も完全一致）。
- type: extends
  target: K1265
  note: {1}^t census t=2..6 の延長上の min=1 アリティ地図（E5・t=3..8 × z=0..24・初掃引）と witness アンカー6件の再現。z=0・z=1 の分離は K1267 の T1 と report 開示の T2 に全 t で昇格。{1,1} 行の境界+1 崩壊対照点も再現。
- type: depends_on
  target: K0832
  note: 単一トークン閉形式および R<=2 全z 条款（セル (0,1) の窓端 R=2 の補償）。E0 アンカーグリッド 77,252 点 bad 0。
- type: related
  target: K1248
  note: 陰性バンドの2トークン非分離（全 d）は出版 y<=21 全称閉形式の引用レベル帰結として指摘（本実験は d<=200 を機械確認・E4）。m<=10 セルの2トークン決定は同族閉形式から原理的に導出可能だが、本 census は生エンジンによる独立再採引として供給。
- type: related
  target: K1257
  note: 同上（y=22 族・2トークン族全称は y<=22 で完結）。本 census の m<=10 はその内部領域であり、census は前線法則という横断指数として再編したもの。m>=23 の走査は y>=23 族レーン（仮採番 K1266・宣言 474ec50b 所有）の保持域のため意図的に避けた（L2 採引上限 m=22 は y=22 全称の内側）。
artifacts:
- path: research/experiments/generalx-unified-window-sharpness-20261123/report.md
  role: proof
  note: census 正本記録（前線法則・前線 witness 表・L1/L2 偶奇判定と宣言予想反証記録・陰性バンド94セルの open 化と予想 C1・{1}^t 行地図・K1264 C4 再集計一致・誠実記録5点）。
- path: research/experiments/generalx-unified-window-sharpness-20261123/verify_unified_window_sharpness.py
  role: verifier
  note: census 監査機体（SHA-256 0ab66665…・E3/E3b/E4/E5/E6 fail-closed+census・窓端等式・エンジン一致・出版アンカー17件・C4 再集計 fail-closed ゲート）。エンジンは出版 K1264 検証器から sha-gate 機械抽出（build_unified_verifier.py・PROVENANCE PASS・engine block sha bd5f22e4…）。
- path: research/experiments/generalx-unified-window-sharpness-20261123/output/audit.json
  role: data
  note: census 正本（SHA-256 b74551b7…・266 セルの分離集計・最小 witness・値・E5 行24分離・E6 22点・総照合 273,209 bad 0・4実行 byte-identical・変異電池 8/8）。
- path: research/log/2026-11-23-unified-window-sharpness-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit cf299bdd・先行出版・census 設計と事前横断予想の全記録）。
- path: research/log/2026-11-23-unified-window-sharpness-census.md
  role: log
  note: run log（実行経過・宣言点数ドリフト訂正・E3b 追加の理由・変異電池⑦差し替えの開示・K番号確認・fetch-back 記録・次課題）。
scope: >-
  統合窓 W(z,m)=max(z+m,2)（K1264 系3 の出版帰結）に対するセル別鋭さの
  census 観測（observed・有限掃引 z<=24, m<=10, d<=60（陰性は d<=200 拡張）+
  E3b z=25,26 補完 + E6 L1/L2 採引 m<=22・{1}^t 行 t<=8・アリティ電池）。
  主張は「掃引域で例外0の前線法則 z*(m)=2m−2+(m mod 2)」「前線 witness の
  一意性と値」「L1/L2 の偶奇分離」「K1264 C4 出版再集計一致」までであり、
  掃引域外の全 z,m への拡張は未証明（m<=22 の2トークン分は出版 y 族閉形式
  からの引用レベル帰結として指摘）。陰性バンド94セルは「バッテリー+d<=200
  で witness 未発見（open）」であり、予想 C1（全 X 崩壊による banded 窓拡張）
  は open problem として明記。標準11×11の空盤・二石root・S2 {59,60}・
  class 1/2/4は範囲外かつUNKNOWNのまま。
