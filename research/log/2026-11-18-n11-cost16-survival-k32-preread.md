# 2026-11-18 N11 cost-16 生存曲線 rank-32構造preread — rank-32 (15,23) mid-hub root・行23が二重行族に初参加（triple 9・quad 12・quint 0）・新pair 7 shared/24 disjoint・全C(32,6)=906,192 sextet zero（I-E quint打ち切り7度目の安全確認）

k=31本計算（script+log `cf8d7dcc`・result JSON `5da4cc6c`〔blob `0d9f67ee69ad4fb8aa37904ddbf6666745786807`〕・record JSONL `a4bef2aa`〔blob `d308b6d537e8606dadef33c52cdade6cda109320`〕・log `bb0d6e3b`）とcrosscheck k=31拡張（`d994e371`・112 checks 0 failures）を受けて、**k=32本計算に必要な構造事実の事前確定（preread）**を実施・出版した。 deterministicな純Python script（`cost16_survival_k32_preread_20261118.py`・25,163B・blob `26d4edead26631644c4f4be9ac7150c7fa263bff`）が、pinned aggregate（blob `31bdefdb2e2cc90b706cbb8090e98eb5eece4d87`）とpinned出版k30/k31 result JSON（blob `9c24e7a30ad213d3b7675e620ec606b00f73a330` / `0d9f67ee69ad4fb8aa37904ddbf6666745786807`）から、独立2分類器（dict蓄積型とCounter派生型の併用、全列挙一致・不一致0）で全censusを再導出する。31 checks all PASS・二重実行byte-identical（sha256 `8ad1344779e34f5be3e4413db5f007c87dc33407d4f63a83c5c40e0c8ce2ba73`・14,947B）・network/local両モード同一出力。**生存曲線はban回避代替最小cover計画の組合せ数であってverdictではない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。**

## Node整数丸めerratumの再発防止（本prereadの設計意図）

k=31 preread JSON（commit `188106bb`）はNodeのdouble丸め表示で membership/a_part/b_part の3大整数を近似値で印字し、k=31 result JSONの `preread_erratum` blockでの訂正を必要とした（誤: membership 120,181,378,067,473,630 → 正: 120,181,378,067,473,629）。本prereadは**Python（正確な任意精度整数）で書き直し**、最終check `rank32_exact_integer_json_serialization` で出力JSONを書き出した後のparse-back照合（membership/a_part/b_partの3点がaggregateの正確整数と一致）を毎実行時に課した。

## rank-32確定事実（全てaggregateから機械導出）

1. **rank-32 root = (15,23)**（hex `00000000000000801222000000081000`）。**m32 = 120,146,272,057,315,812**（A = 92,121,445,452,103,947 / B = 28,024,826,605,211,865・A+B==M32厳密成立）。行15は6 prior roots（indices 0,13,14,16,17,22）に被覆される中位ハブ帯行。**行23はprior sharerがindex 11の1本のみ**で、rank-32は行23が二重行になる最初のrank。
2. **行23の二重行族への参加はtriple層とquad層のみ（9 + 12 records）、quint層では0**: 行23のdoubled quintは{11, 31}に加えて行15/16/17体系（既存二重行族）を回避する3根が必要だが、そのような組合せがtop-32に存在しない。構造的に閉じている（上位root集合が変わらない限り）。
3. **新pair census = 7 shared / 24 disjoint**（31本・disjoint多数派はk26型の急落パターン。marginal予測はdisjoint-partner法則で Σ新j2 ≈ disjoint 24本 × 約5.3e15 ≈ 127e15 帯〔m32比約106%〕だが24本中の行15共有の重み次第でやや下振れし、marginal比はk29/k26型の低位20%台の可能性）。
4. **新census**: triple C(31,2)=465 = b_only 275 / zero 50 / disjoint 140。quad C(31,3)=4,495 = b_only 1,878 / zero 2,459 / **disjoint 158**（全て|union|=8・disjoint quad累積662+158=**820**）。quint C(31,4)=31,465 = **b_only 2,010** / zero 29,455 / disjoint 0・b_only累積6,787+2,010=**8,797**・二重行hist {15:613, 16:65, 18:962, 19:370}・全2,010本が3/2/0の4-subset profileを維持。
5. **全census C(32,3)=4,960 = {2,992/980/988}・C(32,5)=201,376 = {8,797/192,579/0}**（二重行hist {15:1,616, 16:304, 18:5,111, 19:1,766}・行23はquint二重行族に不参加のまま）。**C(32,6)=906,192 sextet全zero**で、quint次I-E打ち切りの安全性はk=26から7連続で機械保証された。
6. 層接続: full(32) − rank-32新層 = full(31)（8,797−2,010=6,787・192,579−29,455=163,124）は出版k31 censusと厳密一致。rank-31回帰は942,617組合せの2分類器一致・出版structure fields（root/membership/m30正確整数/pair 15/15・quad 986/3,025/49・quint 819/26,586/0・full censuses・sextet 736,281 zero）と全面一致。rank-30回帰も同様に全面一致（pair 8/21・quad 1,302/2,241/111・quint 1,328/22,423/0・sextet 593,775 zero）。

## 実行記録

- 入力pin: agg `31bdefdb…` + k30 JSON `9c24e7a3…`（commit `f6a08dc5`）+ k31 JSON `0d9f67ee…`（commit `5da4cc6c`）。network mode（jsdelivr/raw fallback・sha1照合）とlocal modeが同一出力（byte-identical）。
- 31 checks構成: 2（aggregate/chain）+ 30回帰 4 + 31回帰 5（層接続込み）+ 32事実 18 + 正確整数serialization 1 + 期待総数 1。実行時間約13.5秒/回。

k=32本計算（script変換・joint pm計算・finalize）はこのprereadのcensus・正確整数をassert直用いて次回レーンで実施する。生存曲線はcover-plan組合せ数の確定のみで、勝敗に関するいかなるverdictも生成しない。**標準11×11空盤はUNKNOWNのまま。**
