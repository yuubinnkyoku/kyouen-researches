# 2026-11-14 長期レーン: class2-lane cost-61(b) S6 child sweep 完結（12 WIN7-D10・証明書12件・frontier再計算・11×11はUNKNOWNのまま）

## 何をしたか

同一セッション内で、cost-61(a)フルサイクルに続いて同一 class-2 blocker S5
`00000000000000003802000008000000` の**2番目に安い未sweep S6 child
cost-61 `00000000000000801a02020000000000`（c2=2・class-2専用需要）**の
7石目sweep→証明書化→frontier再計算→反映まで完走した。

1. **sweep**: 同一プロトコル（v15 engine verbatim・native Node v22・2並列worker・
   close-first AND depth>=8・cap 50M・depth 10単発）で**61非退化候補を完走**:
   **12 WIN7-D10（bit 0,1,6,28,32,33,50,84,90,99,105,110）+ 49 REFUTED-D10 +
   0 capped・総 122,567,571 nodes**。pilot d6 5,949 ×2 PASS。
   最重量3候補（102/1/84）の独立再実行で node-exact
 （6,396,662 / 5,724,997 / 5,092,913）。terminal [13,17] 全候補。
2. **WIN7証明書12件**: kill-table-first抽出（exportパッチのみ・各候補1プロセス・
   pilot制御内蔵）で **合計 454,421 行・抽出 34,172,217 nodes**
 （rows 20,295〜50,398）。repo verifier（Bareiss・engine不使用）で全件
   **root-check PASS・全合法sub-root PASS（42〜52）・双方向union 0/0・terminal [13,17]**。
3. **frontier再計算（cost61b）**: 全段階制御が公表値と完全一致:
   baseline 638 → batch1 657 → batch2 665 → batch3 690 → cost60 724 →
   **cost61 735/7111/558480/5328/418487（assert再現）**。
   cost61bの12証明書のcoversは72軌道・marginal 62（manifest内 14）。
   **after cost61b: solved_s6_in_manifest 749・unique remaining 7097・
   sum cost 557,548・open 5314 / 417,555**。
4. **class-2 blockerの継続低下**: S5 `00000000000000003802000008000000` は
   **13/883 → 10 orbit / 688**（今日一日で 32/2206 → 17/1168 → 13/883 → 10/688）。
   best class-4 は 24/1934 不変。**次の最安未sweep S6 child: cost-64
   `00000000000000801a0a000000000000`（c2=2・同一S5）**。

## 実装メモ

- 61候補×2回（cost-61 a/b）のsweepはいずれも2並列で4〜6分。1セッションで
  sweep2件＋証明書16件＋frontier再計算2回まで完走できることを実証。
- run_one.sh の CHILD 書換えのみで同一プロトコルを再利用。

## 反映

1コミット1ファイルで17件（sweep record・証明書12件・証明書record・recompute script・
recompute JSON・ranking CSV・top-candidates CSV・log）。反映前にmain再取得で
並走の同child作業がないことを確認。

## 解釈ガード

- WIN7証明書は「対応する7石rootから深さ10以内の勝ち」の証明のみ。
- REFUTED-D10 は「深さ10以内のWIN7の否定」のみ（より深い勝ちは排除しない）。
- **11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN。**
