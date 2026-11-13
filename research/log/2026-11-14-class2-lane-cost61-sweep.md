# 2026-11-14 長期レーン: class2-lane cost-61 S6 child sweep 完結（4 WIN7-D10 + 57 REFUTED・証明書4件・frontier再計算・11×11はUNKNOWNのまま）

## 何をしたか

cost-60 frontier再計算で新たに最良となった class-2 blocker S5 `00000000000000003802000008000000`
（17 orbit / 1168）の最安未sweep S6 child **cost-61 `00000000000000801a02000000080000`（c2=2,c4=2・双需要）**
の7石目sweepを、main 8055d4be（cost-61関連の並走pushなし）を確認してから実施した。

1. **sweep**: v15 engine verbatim（repo runner・2a1af3a7修復版）・native Node v22・
   2並列worker（控えめ並列）・close-first AND（depth>=8）・cap 50M・depth 10単発で
   **61非退化候補（=全合法7石目）を完走**:
   **4 WIN7-D10（bit 14, 18, 108, 116）+ 57 REFUTED-D10 + 0 capped・総 87,905,423 nodes**。
   pilot d6 制御 5,949 × 5回全PASS。最重量3候補（116/91/22）の独立再実行で **node-exact**
 （5,070,265 / 5,021,989 / 4,168,884）。terminal range は全候補 [13,17]。
2. **WIN7証明書4件**: kill-table-first抽出（exportパッチのみ・各候補1プロセス・pilot制御内蔵）で
   **rows 27,442 / 30,413 / 39,483 / 56,810（合計 154,148 行・抽出 9,772,848 nodes）**。
   repo verifier（Bareiss・engine不使用・ESMパッチのみ）で全件
   **root-check PASS・全合法sub-root PASS（48/48/53/53）・双方向union 0/0・terminal [13,17]**。
3. **frontier再計算（cost61）**: recompute_frontier_cost61.py（recompute_frontier_full.py 論理の
   段階制御付き拡張）で **全段階制御が公表値と完全一致**:
   baseline 638/7208/565500 → batch1 657/7189 → batch2 665/7181/5398/423516 →
   batch3 690/7156/561764/5373/421771 → **cost60 724/7122/559294/5339/419301（assert再現）**。
   cost61の4証明書のcoversは25軌道・marginal 23（manifest内 11）。
   **after cost61: solved_s6_in_manifest 735・unique remaining 7111・sum cost 558,480・
   open 5328 / 418,487**。
4. **class-2 blockerのさらなる低下**: S5 `00000000000000003802000008000000` は
   **17/1168 → 13 orbit / 883**。best class-4 は 24/1934 不変。
   **次の最安未sweep S6 child: cost-61 `00000000000000801a02020000000000`（c2=2・同一S5）**。

## 実装メモ

- 61候補のsweepは2並列で約4分（130M級のcost-60 sweepより軽い）。決定制御・pilot・
  証明書化まで含めても1セッション内で完走した（sweep→抽出→検証→再計算→反映の
  フルサイクル）。
- run_one.sh の CHILD を書換えてcost-61でも同一プロトコルを再利用。
  sub-root列挙は「rootの合法初手」から（前回ログの教訓どおり）。

## 反映

1コミット1ファイルで11件（sweep record・証明書4件・証明書record・recompute script・
recompute JSON・ranking CSV・top-candidates CSV・log）。反映前にmain再取得で
並走のcost-61作業がないことを確認済み。

## 解釈ガード

- WIN7証明書は「対応する7石rootから深さ10以内の勝ち」の証明のみ。
- REFUTED-D10 は「深さ10以内のWIN7の否定」のみ（より深い勝ちは排除しない）。
- **11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN。**
