# 2026-11-24 Part CU 完了: batch-29 (class 2251) 16-LOSS canonical adoption + reaudit — publish-then-execute 全工程完了・出版 A-E

## 結論 (このレーンで確定したこと)

batch-29 (class 2251) takeover drive-1 checkpoint 1/3 の採用可能証拠のうち、2-pass node-exact に解決済みの16キー ab001..ab016 (全て result 2 = LOSS, budget 15M, nodes合計 57,463,971/pass) を **canonical exact-S5 chain cache に正式採用した**。BASE = Part CO merged cache `854800f3...` (6,301行, 158 WIN / 6,143 LOSS) + 16行 = **6,317行 (158 WIN / 6,159 LOSS)**, merged cache sha256 `30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4`。

- **class 2251 は解放されない** (unknown children 54 -> 38, closure rank 35 -> 4)。38 filelessキー (ab017..ab054) は UNPROBED。
- batch-29 は PARTIALLY probed: 採用パケットは probed集合上で loss-only (WIN行・EXHAUSTED行は1行も未観測)。batch全体の完全性は主張しない。
- verdict不消費 (WIN行採用はscrutiny owner C++ pin `9193f5b6...` 専権のまま)。
- **11×11 空盤の勝敗は UNKNOWN のまま。**

## ラベル経緯 (誠実記録)

前sessionで「Part CT」ラベルの空きを機械確認して予約していたが、並走sessionが 2026-11-24T00:02:51Z に別レーン (batch-28 aa050 30M reprobe) で Part CT を宣言したため、混同回避で **Part CU** に変更して着手した (observed HEAD `d06c4d92` で CU未使用・レーン本体への対抗宣言なしを機械確認済み)。

## 実行記録 (全て宣言ノート publish-then-execute の下で実施)

1. **宣言ノート出版** (`research/log/2026-11-24-part-cu-b29loss16-adoption-single-owner-note.md`, commit `d8276573`, 10,020B): push後 git blob sha1 `d274d5fc159919c7f6b5af418cfaecb2477da38a` でローカル正本とbyte一致を機械確認 (fetch-back検証。raw fetchの折返しartifact 3改行はfetchパイプライン由来と切り分け)。
2. **宣言pinの機械照合**: 宣言ノートからpin 11本を正規表現で機械抽出し、実行成果物と全一致 (ALL-PIN-MATCH)。
3. **公式rerun D1-D5** (scratch tree `cp -a` 2面 = 通常 + 隔離):
   - D1 maker ×4: increment `bab011e3...` / manifest `f9f58ee1...` 全回byte一致 (PASS ×4)。
   - D2 merger: selftest PASS + merge ×3: merged `30ddad9d...` / audit `8f611fe1...` ×3 同一 (PASS)。
   - D3 refresh ×3: summary `b60d71a2...` / closure `3019d37f...` / prc `61dbd39a...` / worklist `0d7474e1...` 全回byte一致 (PASS ×3, ~59s/run)。
   - D4 extractor ×4: 全gate PASS, decomp-deltas `3274a297...` byte一致 (PASS ×4)。
   - D5 隔離実行 (別tree, `env -i`, `PYTHONHASHSEED=random`): refresh + extractor byte一致 (PASS)。
4. **tamper battery プロトコル5 a-n**: **14/14 fail-closed捕捉**。捕捉gate: raw 2-pass mismatch (a: verdict flip / b: nodes drift / c: 単一pass budget改変), kit MANIFEST sha drift (d), merger WIN/LOSS conflict (e: BASEへの偽WIN重複行 / h: incrementへの偽WIN複製行), extractor increment sha drift (f: nodes改変 / i: filelessキー注入), manifest sha drift (g: loss_idsからab016を削除するverdict主張偽造), status.log sha drift (j), val-gate takeover-host sha drift (k), scenario cache sha drift (l: filelessキー偽装行), scenario summary sha drift (m), scenario closure sha drift (n: rank改変)。各probe後に正本復元・sha確認、最終clean pass (extractor + maker) 再確認。
   - honest注記: 1回目のbatteryで3probe (d/g/n) は**改変スクリプト側の形式勘違い** (MANIFEST行書式, manifest のキー名, closure CSVのカラム順) で改変が適用されず assertion で検出された。偽の捕捉主張はしていない。修正したprobeで再実行し3捕捉を確定した。
5. **出版 A-E (5 commit, main直接)**:
   - A `b8ece461`: scripts 4本 (maker / merger / refresh fork / extractor)
   - B `24111596`: increment + manifest + merge-audit ×3
   - C `2c2487f7`: merged chain cache (260,590B)
   - D `f6635144`: reaudit outputs 3つ + decomp-deltas (probe-worklistは体積のためsha宣言のみ)
   - E `5b2ad169`: README + MANIFEST-sha256 (14ファイル機械sha列入れ)
   - **各commit fetch-back検証**: GitHub上の各file blob sha1 (計15 file) とローカル公式rerun tree の blob sha1 が全件一致。

## 採用効果 (機械観察・勝敗と誤読なし)

- class_status_counts 両側不変 (excluded 390 / excluded_now 23 / free_now 38 / unknown 34,498; flip・newly free なし)。
- closure: class 2251 unknown_now 54→38 (rank 35→4)。holderのみの変化: 1181 (102→101), 1182 (104→103), 11426 (60→59)。rank churn 125 (tie-swap left {1945,19645} / entered {386,1044})。行数 808→808。anchors 23101/1849/16757 完全安定。
- metrics: joint greedy 38,310→35,691; worklist 64,828→64,809 (class 2251 serving rows 54→38; 採用16キーはworklistから消滅); update8 不変 (141/31,718; 採用16 s5 index はupdate8 baseline requirementと交差なし — 機械観察); PRG movers root 16 (2,971→2,970), root 37 (4,001→3,852); holder union 48。
- このadoptionは19 central-reply root のどれも解決しない。

## 並走レーンの観察 (非接触)

- **Part CV** (`a8592d9c`, 00:17:04Z): 同じ16キー ab001..ab016 の row-audit + pinned-replica + 第三実装交叉検証を宣言・着手 (scrutiny lane) 。adoption chain への対抗宣言・本実験dirへの接触なし。成果は本adoptionの16行をさらにcorroborate/挑戦する。
- **Part CW** (`ba08e1cf`, 00:24:49Z): batch-28 (class 5343) Part CQ 20M再probeの新解決WIN 2行 (aa004/aa035) の第三実装交叉検証を宣言。非接触。
- **Part CT** 完了 (`30af9f49`): batch-28 最終残aa050 が **WIN** 解決 (25,541,199 nodes, 2-pass)。WIN行採用は本レーンの管轄外 (scrutiny owner C++ pin専権)。
- K1275 (z=7 スライス), Part CS/CR (完了) も非接触。

## honest 事項

- 前sessionで extractor雛形の jsreplay pin を手転写した際に無効文字を混入し maker が fail-closed ABORT したことがある。修正は機械抽出・機械置換で行い、本Part成果物に手転写pinは残っていない (全pinは filler script `sup/fill_extractor_b29loss16.py` 系の機械抽出による; filler自体はsession産物で実験ではない)。
- batch-29 残38キー (ab017..ab054) の解決は別drive・別宣言が必須 (class 2251解放の必要条件)。
- 今回の出版では push_files の chunked read (file_system.read_file offset/limit) を使い、手転写を全工程で排除した (計 260KB超のファイルも含む15ファイル全てbyte一致検証済み)。

**11×11 空盤の勝敗は UNKNOWN のままである。**
