# n11 第8次両計画更新: 層別外3件＋S6未反映2件＋新規LOSS 150871 の反映

基準: main `2b762103`（第7次計画 update7、上界31,771・下界6,585・層別17）。
本実験は既存実験・knowledge正本・生成物・共有solver論理・K0423・
既存出力・第1次〜第7次出力・batch1〜5出力・履歴を一切変更せず、
`research/experiments/n11-night-plan-update8-20261016/` に結果を分離保存する。
第7次出力 (`n11-night-plan-update7-20261015/output/`) は読み取り専用の基盤。

極性は [K0371](../../knowledge/items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md)
絶対準拠: S5=AND・後手手番。WIN(verdict=1)=全S6先手WIN、LOSS(verdict=2)=存在S6先手LOSS。
UNKNOWNは証拠ではない。空盤 (11x11) はUNKNOWNのまま、全盤への飛躍は行わない。

## 反映した事実

1. 層別外3件（native focus10m 由来の厳密receipt、checker source `0f890cb4…`・trusted葉0）
   - 115540 **LOSS**（verdict 2）・144193 **LOSS**（verdict 2）・144311 **WIN**（verdict 1）
2. S6終局証明 (`s6-loss-optimized.cert`, sha `cb2e73c2…`) の未反映S5親2件
   - 381858 **LOSS**（mask `00000000000000101001000010010000`）
   - 382619 **LOSS**（mask `00000000040004001000000004010000`）
3. 本ラウンド新規10M探索の **150871 LOSS**（S={12,24,49,59,60}、SOLVED verdict 2、
   3,744,513 nodes・trusted葉0・終局DAG 644,490/971,480/83,851、独立receiptあり）

144774（S={5,49,60,67,75}）は同一10MでNODE_LIMIT（UNKNOWN）。証拠にせず、同条件再探索はしない。

## 結果

### 共同計画 (`output/repaired-joint-plan-update8.json`)

- 上界 **31,859**（baseline 31,771・Δ+88）
- 層別 **18（WIN 7＋LOSS 11）**、resolved verdict 23件
- 除外S4 **23件**・`new_excluded_s4_classes=[3945, 5596, 14102]`・changed_choice_count **6**
  （全てWIN 144311の選択クラス5596失効に伴う再選択）・free_thirds 122
- `known_loss_removed_from_cost=[115540,144193,150871,381858,382619]`
- 一括／段階反映は labels/candidates/obligations/choices/union 全一致（union 31,859）
- 境界再検算: 352選択S4・2261 third・19 third境界、known_loss_in_union 0・known_win_selected 0

### 双対下界 (`output/updated-element-dual-update8.json`, `--verify`通過)

- 厳密総和 `182572529/27720` ≒ 6,586.31057、整数下界 **6,587**、上界31,859
- 869有料群・948群・選択肢34,426・要素962,443・degree sha `08d5a4d1…`

### WIN側 (`output/win-side-reanalysis8.json`)

- 使用可能証人 **1,928**（保存1,945−17）・closable **57/65**・
  unclosable `[0,1,2,4,15,46,79,101]`（8軌道）・AND幅 **6,585**・未閉鎖証人 **1,661**
- update7比: closable 59→57、newly_unclosable `[0,46]`・verification passed（57被覆）

### 証明書再利用 (`output/certificate-reuse8.json`)

- 追加S5 LOSS: indexed 2件（381858/382619、既に層別済）＋index外1件のみ
- **新規S5 WIN 0**・新規S7 LOSS 0・共同計画の和集合は不変（効果0）

### 閉鎖不能応手の再解析 (`output/unclosable-reanalysis8.json`)

- 8応手 `[0,1,2,4,15,46,79,101]` は全て **pool-shortage**（pool制約なしなら65/65閉鎖可能）
- 群最小証人数はgreedy 30〜32（exact探索はnode cap 400,000で未確定）
- pool外の新規証人候補 **227**

### 候補効果 (`output/candidate-branch-ranking.json` / `candidate-effects.json`)

- pool未カバー分岐9件、単独解消候補9件（144019/193768/144692は既に10M済で除外）
- 各候補LOSS Δ−1・WIN Δは0（150871）〜+111（221294）。実測最良150871→新規LOSSとして層別

### 終局検証 (`output/receipt-150871.json` / `terminal-verify-150871.json`)

- 共通検査器 `check_trace`（source sha `0f890cb4…`）で独立検査、trusted葉0・pruned roundtrip
- `compare_terminal_update8.py` のPython独立再導出も同値（nodes 644490・edges 971480・terminal 83851）

## 限界

上界31,859は検証済み事実の反映であり、要求S5和集合が全てLOSSとなることは未証明（楽観的計画）。
exact最小証人数・pool外証人227の被覆成立・証人単位のS6閉包費は未測定。空盤勝敗はUNKNOWN。

## 再現

```sh
uv run --locked python research/experiments/n11-night-plan-update8-20261016/scripts/update_loss_plan.py
uv run --locked python research/experiments/n11-night-plan-update8-20261016/scripts/update_dual.py --verify
uv run --locked python research/experiments/n11-night-plan-update8-20261016/scripts/update_win_side.py
```

10M探索 (`probe_update8_candidates.py`) はWindows上でWSL2 UbuntuのLF ELF `build/kyouen-dfpn-root-adaptive`
（sha `72f1da29…`）を用い、input CSVは `input/s5-<index>.csv`、出力manifestは
`output/update8probe10m-manifest.json`。traceは `build/n11-update8-traces/`（ignored）。
