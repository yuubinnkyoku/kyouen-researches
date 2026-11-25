# 2026-11-14 class4-batch3 child#7 sweep (session 20, long lane)

## Context

- 開始時に最新 main を確認（HEAD 20d8ed1f、第19セッション終了時点と同一）。
- レジューム通り class-4 lane target `00000000020000003800000080000000` の残 S6 child のうち
  次の最安 `00000000020000003800000080001000`（cost 72）の 7 石目 sweep から着手した。
- 作業中に並走レーンが同じ child#5 を sweep・証明書化・反映済みであることが判明
 （21:38-21:50Z、child#5: 68 REFUTED + 4 WIN7 bit108/95/99/17、child#6 `...c0000000`
  cost 73: 73候補全 REFUTED・WIN7-D10-sterile）。

## 本セッションの成果

1. **child#5 の再導出による相互検証（重複回避のため証明書は再pushせず）**:
   独立に構築した native Node harness（close-first AND d>=8 変種）で同 child を全走査し、
   72候補の verdict・候補集合・pilot 5,949・4証明書の行数（16,700/24,611/50,090/46,051）
   がすべて並走レーンの公表値と完全一致することを確認。node 総数 300,572,910
  （公表 256,648,013 と異なるが ordering 依存で非比較対象）。
   記録: output/class4-batch3-child5-sweep-independent-reproduction.json。
2. **child#7 sweep（新規・本セッションの主成果）**: S6 child
   `00000000020000003800010080000000`（cost 72・c4=3・after-batch2 CSV で次点の
   cost-72 orbit）の72非退化候補を全走査 —
   **WIN7-D10 5件（bit80/94/50/39/117）+ REFUTED-D10 67件**、
   総 300,096,377 nodes、capped 0、pilot d6 5,949 PASS、
   決定制御 7 bit（WIN7全5+重いREFUTED 2）独立再実行 node-exact。
   bit30 に11石 terminal（range [11,17]）を観測（child#4 bit77 に次ぐ2例目）。
   記録: output/class4-batch3-child7-sweep.json。
3. **WIN7 証明書 5件の抽出・独立検証**: bit80（17,347行）/bit94（20,555行）/
   bit50（46,206行）/bit39（48,636行）/bit117（47,555行）、合計 180,299 行。
   抽出総 52,978,900 nodes。独立検証（Bareiss 4x4 整数行列式・engine不使用）で
   sub-roots 42/47/52/53/61 全 PASS・union 完全一致（0/0）・terminal range [13,17]。
   記録: output/class4-batch3-win7-certificates-child7-20261114.json。

## Frontier（局所・保守的）

- after-batch2 CSV の class-4 target 32 orbit のうち既に child#3/4/5/6 で消化された
  4 orbit（68/69/72/73）を除いた残りの中で、本 sweep は2番目の cost-72 orbit を閉じる
  （証明書 covers の S6 orbit 追加閉鎖は manifest 再計算待ち・次回課題）。
- child#5 の4証明書の covers が同 orbit を二重カバーする可能性は child#4 記録の
  `in_class4_target_remaining` から未確定のまま（manifest-level 完全再計算が保留中）。

## 解釈ガード

- WIN7 証明書は「7石rootから深さ10以内の勝ち」の証明のみ。REFUTED は
  「深さ10以内の WIN7 の否定」のみ。
- **class 4・S2 {59,60}・二石 root {49,60}・11×11 空盤はいずれも UNKNOWN**。

## レジューム

1. 次の最安未sweep orbit は cost 74 帯 3件（`...80000020` c1=2 / `...88000000` c2=1 /
   `...3801000080000000`）。並走レーンの最新 main を必ず取り直してから選定。
2. manifest-level frontier 完全再計算（child#5/#6/#7 の証明書 covers を含む）
   が依然未実施で優先。milestone5 manifest CSV（テキスト）との部分再計算が可能性。
3. c1=2 の `...80000020` は class-1 blocker にも需要を持つ初の候補で、
   閉じた場合の条件付き class-1 状態への影響を要確認。