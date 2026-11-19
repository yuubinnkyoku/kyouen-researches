# n11-residual72-candidate-supply-whole-record-second-verification-20261120

K1075（残余72行のfull cache-join候補供給再構築）出版正本の独立第二検証、
**whole-record経路**。単一オーナー宣言ノート
`research/log/2026-11-20-n11-candidate-supply-whole-record-second-verification-single-owner-note.md`
を先行出版した同一レーンの実行。branch/PRは作らずmainに直接出版。
resolve7第二検証・fold10第二検証と同じ「出版済み正本のみからの独立再現」枠組み。

## 検証対象

- K1075正本: `n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json`
  SHA-256 `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa`（25 check・全PASS）

## 幾何レーンとの役割分担

並走レーンが同正本の幾何経路（D4変換・厳密整数Bareiss・witness 36根/retired 38根の
被覆幾何再導出・44 gate）を出版済み
（`research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/candidate-supply-second-verification-20261120.json`）。
本レーンは幾何の再導出を行わず、出版記録の同一性のみを独立経路で検査する。両レーンの
一致（36根×2行の1回被覆・matching=36・row_demand集計値・live38の割当）は、
独立実装2系統による再現の追加証拠になる。

## 何をしたか（4独立経路 + 正本全フィールド照合）

- **route A（K1069 live sweep の生probe corpus再構成）**: 4-worker生probe記録
  （`probes-w{0..3}.jsonl`・98行・一意(root,ordering)78対・重複20行）から自前
  dedup/agreement実装で分類を再構成し、39/39で正本classificationと完全一致。
  重複20行は loss/nodes/capped/bit/child/covered_rows/control すべて一致、
  差異は wall_s と result.ms の計時値のみ。nodes総計169,615,508・最大probe
  （`00000000010000809002000040000080`・14,249,420）・平均（2,174,557）も再計算一致。
  WINは`00004000000000821082000000000100`（第17receipt root）両順序loss=trueのみ1根、
  REFUTED 38・CAPPED 0・order conflict 0。
- **route A2（K1059 dead sweep のREFUTED-D10再構成）**: sweep39dead正本の
  witness_records 39件それぞれの probe_runs（両順序・loss=false・uncapped・
  nodes_total==run合計）からREFUTED-D10を再構成。39根集合==
  classification.refuted_d10.roots==resolve6.base_state.dead_roots_39。
- **route B（fold鎖・frontier数値）**: resolve5/resolve6の残余78行同一性、両正本の
  witness_full 39根がそれぞれ78行をちょうど1回被覆（2レコードはwitness選択が
  異なるが被覆不変量は同一）を機械照合。fold9 target 4行⊆78・fold10 target 2行⊆(78−4)、
  78−4−2=72を集合算術で再導出し、K1075 base rows・fold10 residual_row_hex_after・
  resolve7 residual_72_after rows の4経路と一致。fold9.frontier_after ==
  fold10.frontier_before、published_base（cost 491,497・s6 6,206・solved 1,642）==
  fold10.frontier_after、閉鎖40/112。resolve6のWIN 4根の被覆行がfold9 target 4行に
  ちょうど一致する証拠照合。sv17（第17証明書三重検証・38 gate）のrootがretired root
  と一致。
- **route C（join統計の値同一性）**: K1075 stage-1複製detailの join_stats ==
  resolve6 verdict_join.stats 全6項目、universe_hits 5項目一致、win_cover_hits=4。
  判定済みdelta算術 7,493+39=7,532・6,707+38=6,745・786+1=787・conflict 0。
  universe恒等式 4,417+3,102=7,519、7,519+446+4=7,969、4,109+2,871=6,980、
  6,980+468+0=7,448==universe72_roots、fresh_safe_pool==4,109。
- **route D（phase-2供給解剖・クロスレーン整合）**: 72行row_demand再集計
  （fresh-safe min52/max76/sum4,678・judged_refuted 4/13/638・judged_win全0・
  deficit全false）、fresh_safe_72row_coverage==残余72行、uncover 0行。
  witness 36根の解剖（covered==rows==2行・safe・popcount 7・36根で72行を重複なく
  ちょうど1回被覆）から、matching上限 ⌊72/2⌋=36 と36本達成で maximum_matching=36 を
  記録のみから証明。witness根は live39・dead39・retired root のいずれとも交差しない。
  live38記録==live sweep 39根−WIN==resolve7 rows_per_root鍵。resolve7正本
  （27 gate全PASS・SHA-256 `207f4094…`一致）と76-gate resolve7第二検証正本
  （resolve7 pin一致）のクロスレーン整合。
- **正本自体の監査**: schema/date/status、interpretation_guard のLOSS非証明・
  証明書非該当文言、trust_boundary の conflict-fail-closed・stage-1 abort文言、
  25 check全PASS・check名リスト完全一致。

## 結果

- **87 gate すべてPASS**（pin 16 + route A/A2/B/C/D再導出・照合71）。
- 出力正本 `output/candidate-supply-whole-record-second-verification-20261120.json`
  SHA-256 `753f9a07599525ae17eb66cb1a72f59164d995190d50b182bf26a6e7f07f9de9`、
  2回実行+別cwd別プロセスで byte-identical。
- 幾何レーン（44 gate・D4/Bareiss再導出）と本レーン（87 gate・記録同一性経路）の
  互補検査で、K1075正本の内容は2系統の独立実装で追試済み。

## 信頼境界（本検証が再現しないもの）

- 根レベルのuniverseリスト（7,969/7,448根・fresh pool 4,109根）と根ごとの被覆行
  対应は正本に全世界リストとして出版されておらず、記録だけからの再列挙は不可能。
  `pair_edges=536`・`greedy_set_cover_size=40`・`singleton_eligible_rows=72`・
  universe交差数（dead39_in_universe72=37・live38_in_universe72=38）は K1075 内部の
  主張として記録に留め、本検証のgate対象外。幾何レーンがBareiss再導出で
  safe universe 4,577/unsafe 2,871・被覆ヒストグラム(1:6616, 2:832)を独立再構築済み。
- maximum_matching=36 の上限は「72行のマッチングは36対を超えない」の全称命題、
  下限はwitness 36ペアの1回被覆。行グラフ自体の再構築は含まない。
- ランナー（runner v16/v17）のdepth-10判定の健全性・D4不変性は上流の前提であり、
  本検証はいかなる局面も判定しない。K0863 corpus 1,272/1,279 fileの
  SHA検証・実機探索の再実行は対象外（正本の corpus_verification/trust_boundary の
  記述に依拠し、その文言の存在をgateで確認）。

## 実行方法

- stdlibのみ。`python3 scripts/k1075_second_verification.py <input_dir> <out>`。
- input/ は正規名（k1075.json, resolve5.json, resolve6.json, fold9.json, fold10.json,
  sv17.json, sweep39.json, sweep39dead.json, resolve7.json, r7second.json,
  probes-w{0..3}.jsonl, roots.json）。pinsは機械内にSHA-256固定（fail-closed）。
- 公開パスからの取得元:
  K1075正本（本README冒頭）、resolve5（.../n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/post-twelfth-receipt-cover-resolve5-20261119.json）、
  resolve6（.../n11-residual78-cache-join-resolve6-20261120/output/post-saturation-full-cache-join-resolve6-20261120.json）、
  fold9（.../n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json）、
  fold10（.../n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json）、
  sv17（.../n11-residual78-seventeenth-win7-cert-extract-20261120/output/seventeenth-cert-triple-verification-20261120.json）、
  sweep39 live（.../n11-residual78-39livewitness-depth10-sweep-20261120/output/witness-39live-root-depth10-sweep-20261120.json）、
  sweep39 dead（.../n11-residual78-39witness-depth10-sweep-20261119/output/witness-39-root-depth10-sweep-20261119.json）、
  resolve7（.../n11-residual72-postfold-witness-recheck-20261120/output/residual72-postfold-witness-recheck-20261120.json）、
  r7second（.../n11-residual72-resolve7-second-verification-20261120/output/resolve7-second-verification-20261120.json）、
  probes・roots.json（.../n11-residual78-39livewitness-depth10-sweep-20261120/ 直下・output/）。

## 解釈規約（他のn11項目と同一）

- REFUTED-D10 は LOSS 証明ではなく、fold・被覆は行の簿記。本第二検証は探索ゼロ・
  根の新規判定ゼロ・行の閉鎖ゼロ。witness根・候補供給は条件付きdepth-10掃引計画で
  証明書ではない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。**

## 次の一手

1. 36-root fresh-witness掃引は別レーンの宣言済み（着手不可）。成否の出版を回収して
   次回判断する。WINが出れば証明書第二検証が次の自然な作業。
2. fresh-unsafe 2,871の構造分類（幾何レーンのC(4,p,q)再導出結果との突合せ有望）。
3. add-two-stones候補拡張・depth>10コスト測定（K1038 strandedの後続）は未着手。
