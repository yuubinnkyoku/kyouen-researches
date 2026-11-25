# 2026-11-15 n11 class2-lane cost-75d WIN7 certificates second verification (all 4 receipts, third geometry system)

第二独立検証セッション。並走sweepレーンが着地した cost-75d（child `00000000000040801202000000200000`, cost 75, 第二coverable class-2 target S5 `00000000000000801202000000200000` 17行/1325 の最安未sweep行）の WIN7-D10 証明書4枚〔bits 12, 40, 92, 111〕を、main公開成果物のみから再構築したmirrorで第三の幾何系統を含む3系統で検証した。

## 実施内容

1. **第三幾何系統の新規実装** `verify_cost75d_win7_rational_independent.py`（本セッション書き下ろし・純stdlib）:
   公開2系統（BigInt 3x3余因子展開・Bareiss 4x4掃き出し）がともに行列式に基づくのに対し、石3組の禁止セルを「共線3組なら直線上の盤面点（整数外積）」「非共線なら有理数の外心（fractions.Fraction による垂直二等分線2x2連立）と等距離判定」で特徴づけ、リプレイも再帰なしの明示的worklistで独立に書いた。**幾何交叉管理**: ランダム5000石3組の禁止maskがBareiss系とbit-exact一致（不一致0）。
   開発中に外心求解式の座標オフセット過剰バグを1件検出・修正（修正後に交叉管理で確認。検出はroot安全アサートの失敗による。最終版 sha256 a225dfdf...）。
2. **全4証明書が3系統PASS**: bit12（31,181 rows / mobility 55 / extraction 1,115,331 nodes）・bit40（52,198 / 60 / 6,007,621）・bit92（75,290 / 66 / 15,330,145）・bit111（81,199 / 61 / 16,145,165）。合計 **239,868 strategy rows / 38,598,262 extraction nodes**。全系統で consumed == rows（union 0/0・証明書は行過剰なし）・terminal stone range [13,15,17]・root safe。BigIntの再実行は公開 bigint JSON 4件すべてと完全一致。
3. **consumed集合の三重一致**: 自レーンBareiss再実行のconsumed出力・有理系のconsumed出力・並走が着地したfold入力consumed dump 4件（bit12 1,028,973B 単発・bit40 1,722,534B 単発・bit92 2×1,242,285B・bit111 893,211+893,211+893,145B parts）がすべて byte-identical。
4. **ハッシュ・簿記**: 4証明書とも md5/sha256/git blob sha が receipt と一致（bit92/bit111 は行境界part結合→whole再現、part md5もmanifestと全件一致）。root == child XOR (1<<bit) 4件すべて成立。rows.summary は per-move すべて ok・terminalRange は13..17内・nMoves は root mobility と一致。決定性: bit12でBareiss・有理系の再実行がbyte-identical。
5. **root新規性**: 4新rootは相互に raw・D4-canon ともdistinct、head 1277 にfoldされた16 receipt roots（65l+74g+69i）とも raw・D4 ともdistinct。548-root全体とのdisjointnessは並走の cost-75d fold script がassertする予定で、fold着地後の次回第二独立検証対象。
6. **輸送上の観察**: bit111 の cert/consumed split manifest は着地途中に2分割→3分割へ改訂された。raw CDN は改訂後数分間旧2分割manifestを返したため、manifest読み取りはGitHub API（blob権威）で行った。

## 解釈境界

WIN7-D10証明書は「個々の7石rootから深さ10以内の先手勝ち」のみを証明する。REFUTED-D10はWIN7-D10不在のみを意味しLOSS証明ではない。solved数はmanifest被覆の簿記であり勝敗ではない。**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4はいずれもUNKNOWN**。

## 機械可読記録

`research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost75d-certificates-second-verification-20261115.json`

## レジューム

- cost-75d fold（4 receipts）は並走のto-follow。着地後に fold script の全統制（baseline 1277 assert・548-root disjointness・marginals・set等式）を第二独立検証する。
- cost-76b sweep着地済み（76候補・WIN7-D10 bits 72/96・74 REFUTED・107,961,863 nodes・commit 5ef0d819）+ blind抽出2件IN FLIGHT。並走のaudit着地後に `audit_cost75d_raw_sweep_independent_20261115.py` 雛形で第二独立監査を行い、証明書着地後に本セッションの3系統検証を適用する。
