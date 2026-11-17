# 2026-11-17 n11 class2-lane: cost73lバンド fixB修正battery（K0907の第2バンド拡張）

## Context

K0907（log `2026-11-17-n11-class2-lane-extractor-memo-sign-bug-and-fixed-battery-73k.md`・
commit `b119a433`）は証明書extractorの2欠陥（bug A符号付きmemoキー・bug B死んだ
sentinel 255負境界・ともに性能のみでサウンド性無影響）を特定し、cost-73k帯
22 bitで修正batteryを測定した: fixA −30.8%・fixB −73.9%（出版ms18 baseline比
−81.9%）・22/22証明書byte同一・fixA==fixB occupancy。ただし測定は73k 1バンド
に限定されていた。本実行でfixBのbyte同一gateを第2の完全出版バンドcost-73l
（32 sweep WIN7-D10 root・manifest git blob `6e0a94ab`・出版抽出
424,657,112 nodes）に拡張し、修正採用判断（別レーン判断）の根拠を強化した。

## What was done

1. **script** `measure_fresh_battery_fixed_memo_73l_20261117.py`
   （stdlib Python + Node・決定的・resumable）:
   - pin 4件をgit blob shaで検証: repo-verbatim extractor_exact
     `52bcaf50…`・driver `cert_driver73l.ts` `f997a7cf…`・
     `legal_candidates.py` `8e97082c…`・73l manifest `6e0a94ab…`。
   - fixB変種は73k batteryと同一の行レベル手術: MS=1<<23（出版処方）・
     `mK0..mK3`のInt32Array化（bug A・正確1行）・sentinel対応負境界更新
     （bug B・nowin/nolose正確2行）。各パターンがverbatimにちょうど1回
     存在することと手術後に固定形だけが存在することをassert。
   - manifest 32 bitを対象にper-bit fresh processで抽出し、出版証明書
     （分割ファイルはpart1of2+part2of2連結）とbyte比較。全bitで
     fbt_drops 0・fatal 0・nRows==manifest rowsのgate。

2. **測定結果（2回のフル実行で完全一致）**:
   - **fixB総計 52,079,030 nodes = 出版verbatim ms23 424,657,112の
     0.1226（−87.7%・8.2倍）**。73k帯の0.2607より更に低く、**削減率は
     バンド依存**。
   - per-bit比: 最小 bit25 0.0981（1,804,772 / 18,394,863）〜
     最大 bit119 0.1587（1,820,603 / 11,473,533）。
   - **32/32証明書byte同一**（出版bytesと完全一致）。byte同一累計は
     73k 22 + 73l 32 = **2バンド54証明書**。
   - 決定性gate: bit1を同一スクリプト内で2回fresh抽出し、nodes
     1,456,164両回一致・bytes md5 `114b255f…` 両回一致
     （=73l出版時のbit1既知決定性md5と同一）。
   - 出力JSONは2回のフル実行（別work dir・全bit再抽出）でbyte同一
     （md5 `c4b085eb…`・8,584B）。

3. **K0907 item更新**: artifacts 2件追記（battery script + 出版JSON）・
   evidenceに73l拡張を追記・scopeの測定範囲を73k+73lの2バンドに更新・
   bodyのbattery節に73l拡張行追記・限界節の測定範囲記述を更新。
   README bullet（K0907）にも73l拡張の数値を追記。

## Interpretation guard

- 測定のみ。新規WIN/LOSS verdictなし・manifest行は1行も閉じず・証明書
  bytesは不変（byte同一は再出版ではなくgate）。
- fixB変種は出版決定性連鎖のためのrepo-verbatim extractorの置換では
  ない。将来バンドの抽出への修正採用は別レーン判断のまま。
- 削減率のバンド依存（0.2607 vs 0.1226）は2バンドの有限観察であり、
  他バンドへの外挿は主張しない。
- **11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4は
  いずれもUNKNOWNのまま**。WIN7-D10は個別7石rootのdepth-10内先手勝ち
  のみ・REFUTED-D10はLOSS証明ではない。

## Artifacts

- script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_fresh_battery_fixed_memo_73l_20261117.py`
- data: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-fixed-memo-battery-73l-20261117.json`
- knowledge item: `research/knowledge/items/K0907-extractor-memo-sign-bug-and-dead-negative-bounds.md`（更新）
- README bullet: `research/knowledge/README.md` K0907 bullet に追記
