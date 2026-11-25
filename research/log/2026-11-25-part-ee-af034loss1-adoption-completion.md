# Part EE 完了: af034loss1 (af034 60M解決 1 LOSS行) canonical adoption 接続core 完了・reaudit (wave F) は pending (2026-11-25)

単一オーナー Part EE・publish-then-execute。接続core (宣言〜README/MANIFEST
まで) の全 wave が完了した。wave 毎の publish + fetch-back git blob sha1
照合は以下のとおり全て一致した (wave C の初回 push は後述のとおり
truncate 事故が発生し、同一 commit 内で全 6 ファイルを再 push して修正
している・事故と修正の両方を正直に記録する)。

| wave | 内容 | commit |
|---|---|---|
| A | 宣言log (observed HEAD `67b87d26`。blob sha1 一致) | `27517867` |
| B | kit 2 scripts (maker fork `772c3c45…` + merger byte-clone `90711961…`)・blob sha1 2/2 一致 | `efbbc8be` |
| C | outputs 6 files (初回 push は merged cache が 63,971B で truncate 事故) | `7c34e893` |
| C-fix | outputs 6 files 再 push (merged cache は read_file 行chunk 連結で全 277,578B・blob sha1 6/6 一致。C-fix 後の 6 ファイルの sha が正本) | `bb7cd3ac` |
| D | README.md (blob `22838a23…` 4,837B) + MANIFEST-sha256.txt (blob `228502b5…` 1,965B) | `45f5ac02` |
| E | 本完了log | (本 commit) |
| F | **reaudit (refresh fork + delta extractor + reaudit outputs)・Part EE 宣言で事前登録済み・未実行** | (次回以降の実行) |

## 採用結果 (honest label・verdict は af034 1行のみを接続coreで消費)

- 採用行: af034 = (1152921504607911937, 68719476736) (stones=5・
  legal=95・s5 index 930660・class 34908 境界子) = Part ED 60M 条件の
  fresh exact LOSS (result=2・nodes 32,012,059・two-pass fresh-cold
  node-exact)。予算条件 ladder は 15M (b33) EXHAUSTED → 30M (Part EA)
  EXHAUSTED → 60M (Part ED) resolved exact LOSS (各 rung は個別宣言済み
  Part・同一条件の再 re-probe は行っていない)。
- increment `output/increment-af034loss1-20261125.cache` (1,597B) sha256
  `cc9c474627ec8f6fc98c0ebeb7600707021e8cd598b3be6799d39c104289e162`
  (1行: `s5verdict,1152921504607911937,68719476736,5,2,32012059`)
- merged canonical `output/merged-exact-s5-chain-plus-af034loss1-20261125.cache`
  (277,578B) sha256
  `fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f`
  = **BASE (Part EC `cecc1a0f…` 6,665行・WIN 158 / LOSS 6,507) + fresh 1行
  = 6,666行・WIN 158 / LOSS 6,508** (unique・dup_elided 0・実測検証:
  s5verdict 行 6,666・採用 lo/hi は 1行のみ)
- merge-audit ×3 同一 sha256
  `05381cea4c65fcbcaf46d77fbdf3b1d307c41f6abeef0cc9636954e29f5cbcfd`
  (各 1,658B)。manifest `output/increments-manifest.json` (5,290B)
  sha256 `0ad3469ede4bfbddaee21d12dbab97f7e0babdbe5cbaba8cc7a6f2f41d0d22c9`
  (schema af034loss1-increments-manifest-v1・full_packet_eq_loss_only=true・
  win_scenario_exists=false・adopted_table_digest `aab6262a…`)。
- merged cache名は短縮形式 (従来の BASE名+`-plus-…` 命名は 260B超で
  merger `.tmp` 書き出しパスが filesystem 255B 制限に抵触・実測 Errno 36)。
  完全な BASE (EC) cache名と sha `cecc1a0f…` は maker・merge-audit・
  宣言が保持する。検証性は sha 照合で完全に保たれる。
- full packet == 採用行 (probe-level WIN行ゼロ・still-EXHAUSTED行ゼロ)。
  **verdict は本 Part では af034 の 1行のみを canonical cache へ接続
  (採用) した。** class 34908 の 6不消費WIN子 {af029, af047, af050,
  af053, af023, af048} は引き続き scrutiny owner C++ 第二実装 gate pin
  `9193f5b6…` 専権・全て不消費のまま。それ以外の不消費WINプール
  (d002, d008, d009, d021, d026, d029, e042, e002) も不変。

## wave C truncate 事故 (正直な記録)

wave C の初回 push (`7c34e893`) で merged cache (277,578B) が
63,971B で reader truncate された状態で出版された (read_file 1回の
~64KB 上限にかかった)。fetch-back 照合が即時に検出し、同一 commit の
6 ファイルを read_file 行chunk (1,500行×5) 連結で byte-exact に再構成
して再 push (`bb7cd3ac`) し、git blob sha1 全 6 ファイル一致で正本を
確定した。現行 main 上の 6 ファイルは正本であり、誤った短縮 byte は
main 上に残っていない (同一 path の上書き)。以降 277KB 級の push は
行chunk 連結 + ローカル `cmp`/sha256 検証を push 前に必須とする
(すでに EC 運用知見として記録済みの再発防止策の実効確認)。

## class 境界 (期待値のみ・reaudit で機械導出まで主張しない)

- class 34908: EC 時点 unknown 子 7 → 接続core の時点では予想 6
  (af034 EXH 残が 60M exact-LOSS に解決した分)。残る 6子は全て
  不消費WIN。**class 34908 は free化も excluded化もされず unknown の
  まま** (win行は 1行も消費していない)。
- class 16371 / class 20421: 本 Part の採用行は境界内に存在しない
  予想 (closure行 byte-static)。
- 上記は closure-classes・per-root-coverage・decomp-deltas・worklist
  regen pin の再計算・byte照合を reaudit (wave F) が fail-closed で
  機械導出するまで、予想値としてのみ扱う。

## 解釈ガード

- **標準 11×11 空盤は UNKNOWN。19 central-reply root も全て UNKNOWN。
  二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 も全て UNKNOWN。**
- nodes は bookkeeping であり勝敗・距離の主張ではない。pn/dn ではない。
- 60M 解決は verdict 1行の接続core であって、secured coverage・
  被覆・勝敗の数値更新は reaudit の機械導出を待つ。
- EXHAUSTED は honest UNKNOWN。af034 は 60M で解決済みのため以後同
  キーの再 probe は不要。

## 実験dir・正本

- `research/experiments/n11-centralreply-af034loss1-adoption-reaudit-20261125/`
  (README 4,837B・MANIFEST-sha256.txt 8 entries = scripts 2 +
  outputs 6・README/MANIFEST self-exclusion、reaudit 未実行分は
  MANIFEST rev2 で追加予定)
- 依存 byte (ED): kit MANIFEST rev2 `1dfe02ca…` (36 files)・status 5行
  `26a97e02…`・audit_ed `5473eafb…` (58/58 gates)・60M runner
  `b0c5f714…`・jsreplay `84585617…`・af034 raws `63860f94…`/`eb64725f…`・
  exh30m raws `9ecfdc77…`/`3978990d…`・input csv 4行
  (af034 `a4bff566…`・af001 `b2ef3588…`・af029 `b5500b8d…`・
  af039 `e51a3c9d…`)・b33-status `1f663fc8…` (66行)・ea-status
  `db7c7017…` (13行)・quarantine `81d23160…`。EC BASE cache
  `cecc1a0f…`。
- tamper battery 3/3 ABORT fail-closed (T1 maker pin 改変 / T2 raw
  verdict bit 反転 / T3 status nodes 改変・いずれも出力なし)。改変なし
  再実行は increment・manifest・merged・audit の全 byte を再現
  (double-run determinism)。
- hourly 並走があるため、本 wave E の push 前に最新 main を取り直した
  (observed HEAD 移行 `45f5ac02` → push 時点 HEAD は commit に記録)。
  競合時は無理せず次回へ回す規約どおり。
