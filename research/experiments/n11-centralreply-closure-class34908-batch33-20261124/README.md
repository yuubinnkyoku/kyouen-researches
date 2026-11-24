# batch-33 (closure class 34908) 54-key probe drive-1 (Part DQ) — 完了 (2026-11-24)

Part DQ (宣言: `research/log/2026-11-24-part-dq-batch33-class34908-drive1-declaration.md`
commit `c8388b719e`・observed HEAD `fb88a6a`・publish-then-execute・単一オーナー・
verdict不消費)。closure class 34908 (rank 36・closure table 807行・unknown_now 54)
の cost 54子 (既知 {955954: LOSS, 958114: LOSS} 以外の全unknown子) を
2-pass fresh-cold budget 15M で probe した。**事前登録済み drive-1 WIN-HALT
設計どおり、distinct WIN 2行 (af029, af047) の観測で wave halt (rc=45)**・
残り af048..af054 の7キーは fileless UNPROBED のまま (af048 のみ p1 完走
ファイルのみ存在・p2 truncated・verdictなし・UNPROBED扱い)。**閉鎖・被覆・
secured・root勝敗の主張は一切しない**。nodes数は bookkeeping であり勝敗でも
距離でもない。

## kit (出版済み・sha pin)

- 宣言: `c8388b719e` / kit (scripts+README類): `dfdae79e` / inputs
  (batch-keys.json + af001..af054 CSV 67ファイル): `f57f406f` /
  val-gate 4ファイル: `90732788`。
- maker `make_batch33_keys.py` `5d65addd…`・runner `runbatch.sh` `f591f8c2…`
  (byte-clone)・solver `jsreplay.js` `84585617…` (byte-clone)・
  session script `drive1_local_step_b33.sh` `ef44a49e…` (published
  batch-32 drive-1 `e43f5f83…` からの最小delta: key-id正規 ae→af のみ)。
- batch-keys.json pin `8a863381…` (宣言§3どおり)。
- val-gate (本host fresh): 4/4 node-exact PASS (2M at2m 2キー exhaustion・
  first-15m result 2 nodes 3,651,923・second-15m result 2 nodes 5,040,200・
  published baseline比較 field 1-8,10-11 全一致・wall_s 許容差)。
  `.b33-host.out` 4ファイルを val-gate/ に出版 (commit `90732788`)。

## 実行経緯 (正直開示)

1. drive-1 wave 1..12 (resolved 47キー): 各wave最大2キー・2 worker・
   inner `timeout 260` / outer 290s cap。
2. **worker timeout 2件 (af008 p2, af039 p2)**: truncated pass は verdict
   でないため pinned runner の guard が自動再実行し PASS (af008
   PASS nodes 14,364,852・af039 EXHAUSTED)。truncated 生ファイルは
   `af008.p2.truncated.171704.out` / `af039.p2.truncated.180716.out`
   として保管・出版。
3. **環境reset事故 1件**: af031 完了直後に実行環境が reset されローカル
   作業dirが消失。**increment出版 (main) から kit・status.log・raw を
   byte復元** (fetch-back全件一致・runbatch/batch-keys/makerのsha pin再照合)。
   af030/af031 は fresh-cold 再実行で **result・nodes 完全再現**
   (af030 result 2 nodes 4,462,892・af031 result 2 nodes 4,161,701・
   reset前後で同一)。同時多発他レーンとの接触なし。
4. **WIN-HALT**: af029 (wave 8) で WIN 1件目・af047 (wave 12) で WIN 2件目
   → 事前登録どおり wave halt (rc=45)。af048 は同 wave 内 p1 完走後に
   p2 truncated (worker timeout)・verdict なし・**UNPROBED**。
   af049..af054 は一度も未実行 (fileless UNPROBED)。
5. MISMATCH 0・WIN-HALT 2 (distinct)。EXHAUSTED は same-condition
   再probeなし (honest UNKNOWN)。

## 増分出版 (reset耐性・commit列)

inc1 `7324bb17` (af001-af009) / inc2 `77c4f245` (af010-af017) /
inc3 `25522df3` (af018-af029・af029 WIN は即時出版) /
inc4 `bd013154` (af030-af038・reset事故と af030/af031 再現を記録) /
inc5 `e39c5ff4` (af039-af048・WAVE-HALT)。すべて投稿後に fetch-back
byte一致を機械検証 (本 README/MANIFEST 作成時に全ファイル diff 0)。

## 結果集計 (54キー・status.log正本から機械導出)

- **LOSS (result 2)**: 41キー
- **WIN (result 1)**: 2キー — **af029 (s5 900646)** nodes 4,862,485・
  **af047 (s5 961976)** nodes 9,841,975 (2-pass fresh-cold node-exact)
- **EXHAUSTED (result 0 = honest UNKNOWN)**: 4キー — af003 (s5 153030)・
  af023 (s5 810351)・af034 (s5 93060)・af039 (s5 950512) (各 nodes
  15,000,000 = Budget上限)
- **UNPROBED**: 7キー — af048..af054 (宣言§4どおり wave halt 時点の
  残キー維持)
- probe実行 nodes 総和 (47キー): 337,933,140 (参考値・bookkeeping)。
  最大 LOSS nodes: af008 14,364,852。
- membership内訳 (54キー全体): {2: 7, 3: 9, 4: 38} (宣言・batch-keys
  どおり)。s5 範囲 1176..962471 昇順。

## キー別行 (正本: status.log + output/raw/*.out)

| key | s5 | legal | member | verdict | nodes |
|-----|----|----|----|----|----|
| af001 | 1176 | 91 | 2 | LOSS | 2952432 |
| af002 | 38614 | 93 | 3 | LOSS | 10550283 |
| af003 | 153030 | 93 | 3 | EXHAUSTED | 15000000 |
| af004 | 225112 | 96 | 4 | LOSS | 3318813 |
| af005 | 259539 | 98 | 4 | LOSS | 5078821 |
| af006 | 325164 | 98 | 3 | LOSS | 5970933 |
| af007 | 356884 | 99 | 3 | LOSS | 7700082 |
| af008 | 415399 | 91 | 4 | LOSS | 14364852 |
| af009 | 442092 | 93 | 4 | LOSS | 3618250 |
| af010 | 494504 | 84 | 2 | LOSS | 5558617 |
| af011 | 544291 | 84 | 2 | LOSS | 9514618 |
| af012 | 564062 | 91 | 4 | LOSS | 9240870 |
| af013 | 597227 | 94 | 4 | LOSS | 6573273 |
| af014 | 605532 | 98 | 4 | LOSS | 9869039 |
| af015 | 625618 | 96 | 4 | LOSS | 5884486 |
| af016 | 682541 | 97 | 4 | LOSS | 5920144 |
| af017 | 709725 | 93 | 4 | LOSS | 6520712 |
| af018 | 716543 | 93 | 4 | LOSS | 4504991 |
| af019 | 732262 | 100 | 4 | LOSS | 4140443 |
| af020 | 772553 | 96 | 4 | LOSS | 6989622 |
| af021 | 794839 | 96 | 4 | LOSS | 5619693 |
| af022 | 800281 | 95 | 4 | LOSS | 4329388 |
| af023 | 810351 | 94 | 4 | EXHAUSTED | 15000000 |
| af024 | 839602 | 87 | 4 | LOSS | 6089162 |
| af025 | 854635 | 97 | 4 | LOSS | 2894174 |
| af026 | 858969 | 100 | 4 | LOSS | 4299814 |
| af027 | 866321 | 90 | 4 | LOSS | 2601444 |
| af028 | 887040 | 86 | 2 | LOSS | 3569293 |
| af029 | 900646 | 86 | 2 | **WIN (WIN-HALT)** | 4862485 |
| af030 | 904339 | 101 | 4 | LOSS | 4462892 |
| af031 | 913616 | 97 | 4 | LOSS | 4165016 |
| af032 | 916477 | 97 | 4 | LOSS | 5132691 |
| af033 | 921203 | 101 | 4 | LOSS | 11737990 |
| af034 | 930660 | 95 | 4 | EXHAUSTED | 15000000 |
| af035 | 937328 | 97 | 4 | LOSS | 6690990 |
| af036 | 939215 | 93 | 4 | LOSS | 3982739 |
| af037 | 941383 | 97 | 4 | LOSS | 10047387 |
| af038 | 946835 | 98 | 4 | LOSS | 8731665 |
| af039 | 950512 | 89 | 4 | EXHAUSTED | 15000000 |
| af040 | 951758 | 94 | 4 | LOSS | 5576569 |
| af041 | 953035 | 101 | 4 | LOSS | 7100779 |
| af042 | 958529 | 86 | 3 | LOSS | 10487546 |
| af043 | 960072 | 97 | 4 | LOSS | 6467873 |
| af044 | 960568 | 95 | 4 | LOSS | 11691718 |
| af045 | 960786 | 91 | 3 | LOSS | 3895802 |
| af046 | 961459 | 99 | 4 | LOSS | 5382774 |
| af047 | 961976 | 84 | 3 | **WIN (WIN-HALT)** | 9841975 |
| af048 | 962172 | 87 | 3 | UNPROBED (p1完走のみ) | — |
| af049 | 962233 | 99 | 4 | UNPROBED | — |
| af050 | 962386 | 94 | 3 | UNPROBED | — |
| af051 | 962410 | 96 | 4 | UNPROBED | — |
| af052 | 962450 | 90 | 4 | UNPROBED | — |
| af053 | 962470 | 90 | 2 | UNPROBED | — |
| af054 | 962471 | 88 | 2 | UNPROBED | — |

(verdict 文言は honest label。result 1 = df-pn proof値 WIN・2 = LOSS・
0 = EXHAUSTED。**本Partはいかなる verdict も消費・採用しない**。)

## 取り扱い規約 (宣言§5・§6の再掲)

- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
  {59,60}・class 1/2/4・class 8730 / 5804 / 34269・class 34908 (54キー
  WIN/LOSS/EXHAUSTED行を含む) は全時点で UNKNOWN**。本実験の出版は
  これらの勝敗を一切定めない。
- canonical cache への書き込みなし (Part DP 6,502行 chain はread-only)。
  adoption は pinned fail-closed merger `90711961…` を経由する別
  adoption Part のみ。WIN行の scrutiny (C++ `9193f5b6…`) は専権者のまま。
- closure table membership 変動 (flips/newly_free) は probe 完了後の
  reaudit が機械導出する (本READMEはderiveしない)。
- EXHAUSTED 4行の高budget再probe・残7キー (af048..af054) の継続probeは
  別宣言 (batch-33 drive-2 或いは再投入。いずれも新declaration必須)。
