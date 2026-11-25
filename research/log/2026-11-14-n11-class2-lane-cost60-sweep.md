# 2026-11-14 class2-lane cost-60 orbit sweep（第20セッション続き）

- **対象**: S6 `00000000000000801a02000020000000`（cost 60・c2=2・
  batch3 frontier完全再計算で発見した、class-2 lane上の最安未sweep orbit。
  どの既存sweep recordにも未登場）。
- **方法**: class4-batch3 child#5〜#8と同一 — v15 engine verbatim
 （`scripts/class4_child1_sweep_engine.ts` 規則・`class4_child1_runner.ts`）を
  native Node v22で実行、per-candidate freshEngine、close-first AND（depth>=8）、
  cap 50M、depth 10単発。**60非退化候補 = 6石child位置の合法手全て**
 （候補列挙とroot mobility定義はchild#8記録で74/74事前検証済み）、
  mob 40..56の昇順、**4並列worker×15候補**、per-bit増分JSONL。
- **結果**: **19 WIN7-D10 + 41 REFUTED-D10 + 0 capped**・総130,582,358 nodes・
  全候補 terminal range [13,17]。**このorbitは emphatically NOT sterile** —
  class-2 lane初のsweepで、単一orbitとして過去最大のWIN7-D10収穫。
  WIN7: bit 0,1,10,20,25,26,50,52,53,72,76,92,96,98,110,111,112,113,117。
- 制御: pilot d6 control 5,949 nodes PASS・最重量5候補（bit 25/6/52/76/3）の
  独立再実行で node-exact・verdict一致。
- **frontier効果の見積り（未検証・参考値）**: 19 rootのcovers union 111軌道のうち
  **34個がmanifest内かつafter-batch3 solved集合に対してmarginal**
 （batch3全体の25個を上回る）。ただしfrontier数値は検証済み証明書の
  coversのみを数える規約のため、本sweep単体ではbookkeepingを変更しない。
  記録: `output/class2-lane-cost60-sweep-20261114.json`（コミット 4b0a341b）。
- **実装上の重要修正**: repo内 `class4_child1_runner.ts` のコピーがトランスポート
  破損（209-210行目の改行文字列リテラルが実改行にデコードされ、
  strip-typesでコンパイル不能）していたのを `String.fromCharCode(10)` で修復
 （コミット 8744fc65・pilot 5949 PASS + d2 smoke runで検証）。
  usageコメント内の継続バックスラッシュも除去（同種の二重デコード対策）。
- 解釈ガード: WIN7-D10は「対応する7石rootからdepth 10以内のWIN7」のみを
  意味し、証明書抽出・独立検証後に確定する。REFUTEDは深さ10以内のWIN7の
  否定のみで、より深い勝ちは排除しない。
  **class 2・class 4・S2 {59,60}・二石root {49,60}・11×11空盤はいずれも UNKNOWN**。
- レジューム: (1) 19 WIN7候補の証明書抽出・独立検証（class-2 laneの
  secured coverageを一気に伸ばせる。cost順に bit50/117/111/113 が軽い）。
  (2) 検証後、frontier再計算（+34予想）。並走レーンの最新mainを取り直してから。
