# 2026-11-20 n11 K1075（残余72行候補供給）whole-record独立第二検証

対象: K1075正本 `research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json`
SHA-256 `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa`（25 check）。

単一オーナー宣言: `2026-11-20-n11-candidate-supply-whole-record-second-verification-single-owner-note.md`
（先行出版・commit `387e40860b`）。

## まとめ

出版済み正本のみから、87 gateすべてPASSで K1075 正本の全リスト・全数値を再現した。
幾何レーン（D4/Bareiss・44 gate・並走が同時出版）とは役割分担し、本レーンは記録同一性の
独立経路（生probe corpus再構成・dead sweep再構成・resolve6値同一性・fold鎖数値・
row_demand再集計・matching=36の上限下限証明・クロスレーン整合）を担った。

主要な再現結果:

- K1069 live sweep: 生probe 98行（一意78対・重複20行は計時値以外node-exact一致）から
  分類39/39再構成（WIN=第17root 1根、REFUTED 38、CAPPED 0）。nodes総計・最大・平均一致。
- K1059 dead sweep: witness_records.probe_runsからREFUTED-D10 39/39再構成、
  resolve6.base_state.dead_roots_39 と一致。
- fold鎖: 78→(−4)→(−2)→72の集合算術、frontier数値（491,497/6,206/1,642・40/112）、
  resolve6 WIN被覆4行==fold9 target 4行、frontier鎖結合を検証。
- 統計: stage-1==resolve6 verdict_join（stats全6項目・universe_hits 5項目・
  win_cover_hits 4）、7,493+39=7,532・6,707+38=6,745・786+1=787・conflict 0、
  universe 7,969/7,448 の恒等式。
- 供給: row_demand再集計（52/76/4,678・4/13/638・judged_win全0・deficit 0）、
  witness 36根の72行ちょうど1回被覆、matching上限36との一致で maximum_matching=36 を
  記録のみから証明、witness根は全判定済み集合と互いに素。
- クロスレーン: resolve7正本（27 gate）・76-gate resolve7第二検証正本と整合。

信頼境界（正直な再現不能領域）: universe全世界の根リストは出版されておらず、
pair_edges=536・greedy=40・universe交差数（dead37/live38）はK1075内部主張として
記録に留めた。行グラフ再構築・depth-10判定の健全性・引조corpus探索は対象外。

出力: `research/experiments/n11-residual72-candidate-supply-whole-record-second-verification-20261120/output/candidate-supply-whole-record-second-verification-20261120.json`
SHA-256 `753f9a07599525ae17eb66cb1a72f59164d995190d50b182bf26a6e7f07f9de9`（2回+別cwd byte-identical）。

## 解釈規約

REFUTED-D10 は LOSS 証明ではない。matching・被覆は条件付き探索計画の簿記で証明書では
ない。標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて **UNKNOWN のまま**。

## 次の一手

1. 36-root fresh-witness掃引（別レーン宣言済み・着手不可）の成否を回収判断。
   WINが出れば証明書抽出とその第二検証が次の自然な作業。
2. fresh-unsafe 2,871 の構造分類（幾何レーンの C(4,p,q) 結果との突合せ有望）。
3. add-two-stones候補拡張・depth>10コスト測定は未着手。
