# class2-lane cost-63b sweep + 証明書3件 + 正式frontier再計算（2026-11-14）

## 背景

前回までに cost-58 / cost-61-c / cost-63 の3 child を掃討し、after-cost63 正式frontier
（solved 841・unique remaining 7006・sum 550,810・open 5236/411,675）まで反映済み。
best class-2 target S5 `00000000000000809082000000000000` は残28 orbit/1926。
今回はその3番目の最安未sweep child（cost 63 `00000000000000809082000000001000`）を閉じた。

## ① cost-63b sweep（主成果）

- 63候補（独立再列挙: occupied=6・blocked=58（occupied込み）・legal=63 = 公表edge costと一致。
  **列挙器 `scripts/legal_candidates.py`（Bareiss 4x4整数行列式）を新規作成し、
  公表のcost-58(58)/cost-61-c(61)/cost-63(63)候補リストとbit-exact一致で検証済み**）。
- v15 engine verbatim・per-candidate freshEngine・close-first AND（depth≥8）・cap 50M・depth 10単発。
- **3 WIN7-D10（bits 48, 108, 118）+ 60 REFUTED・0 capped・総362,180,924 nodes・terminal [13,17]**。
- 制御: pilot d6 5,949 が63/63プロセスで完全一致・重量5候補（48/108/118/34/32）の独立再実行が
  node-exact（4,052,500 / 6,203,863 / 14,236,510 / 24,243,319 / 15,359,133）。
- raw JSONL（pilot 63行+候補63行）はバッチごとにmainへpush（後述の環境リセット対策）。

## ② WIN7証明書3件（全検証PASS）

抽出は **fbt飽和サイレントドロップ修正版 `class4_child1_cert_extractor_exact.ts`**
（FBS=1<<20・probe 96・drop counter・fbt_drops=0を確認）のblind抽出・1 root 1プロセス。

| bit | root | rows | 抽出nodes | sub-roots | union | terminal |
|-----|------|------|-----------|-----------|-------|----------|
| 48 | 00000000000000809083000000001000 | 31,162 | 6,071,352 | 48/48 | 0/0 | [13,17] |
| 108 | 00001000000000809082000000001000 | 27,510 | 7,679,448 | 47/47 | 0/0 | [13,17] |
| 118 | 00400000000000809082000000001000 | 49,594 | 19,727,646 | 50/50 | 0/0 | [13,17] |

検証はrepo版 `verify_bit7_win7_cert.ts`（engine不使用・Bareiss det4）で全loser初手sub-root分解・
消費行集合=証明書行集合（双方向0/0）・root-check（7石・4点共円なし・loserMobility 48/47/50 =
独立モビリティ列挙と一致）。push後のraw md5 3件ともローカルと一致。

## ③ 正式frontier再計算（after cost-63b）

`scripts/recompute_frontier_cost63b.py`（cost63版の直接拡張・全段階制御assert再現:
baseline 638→…→cost58 814→cost75 831→cost61c 833→cost63 841 まで完全一致してから測定）:

- **after cost-63b: solved 849・unique remaining 6998・sum 550,269・open 5233/411,475**。
- cost-63b効果: covers 19 / marginal 17 / **manifest内 +8**。
- best class-2 target S5 は **28 orbit/1926 → 26 orbit/1798**。best class-4 24/1934不変。
- 出力は2回実行でbyte-identical、repo相対パス版の再実行でもbyte-identical。

## ④ 運用の記録

- **バッチ実行中に300秒timeoutで実行環境ごとリセット**され、最初の15候補分（68.9M nodes）の
  ローカル成果が喪失（公開済みだったfrontier再計算分は無事）。再実行で完全再構成した上、
  以後は**1候補1プロセス×4並列・バッチ完了ごとにraw JSONLをmainへpush**する耐性プロトコルに切替。
- /home/user配下のスナップショット上限（8MiB）に触れたため、証明書など大きい中間成果は
  一時領域で作業し、push直前一時コピーのみcurrent-chatに置く方式に変更。

## 解釈上の注意

REFUTED-D10は深さ10以内のWIN7の否定のみ。WIN7証明書は7石root個別の深さ10以内のWINのみ。
**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN のまま。**

## レジューム

1. best class-2 S5 の残26 orbit の次の最安未sweep child
 （cost 63 帯 `000000000000008090a2000000000000`・`00000000000000809082000000080000` は未解決のまま）。
2. best class-4 `00000000020000003800000080000000` の最安 child（cost 74 `00000000020000003800000080000020`）。
3. fbt飽和修正（extractor_exact）の上流（runner/engine側fbtOR）へのパッチ提案がまだ。
