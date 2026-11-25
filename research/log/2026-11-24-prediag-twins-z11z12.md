# run log: pre-diag 双生児 z11/z12 (K1301) — publish-then-execute 全工程記録

2 つの hourly 実行にまたがる chain の honest 全記録。宣言・キット出版は
先行実行、残工程（fetch-back 再検証・公式 4 走・変異電池・成果物出版・
K item・README bullet・本 log）は continuation 実行が完遂した。
chain の分割は continuation 記録
（`research/log/2026-11-24-prediag-twins-z11z12-continuation-takeover.md`・commit `391cf512`）
に先行出版・中止規約つき。

## 1. 前半（先行 hourly 実行）

1. 宣言ノート出版 `6f4c524d` (2026-11-24T17:19:17Z) — 単一オーナー宣言。
   主張 T-PDT11/T-BDT11/T-PDT12/T-BDT12・L-BU11G/L-BU12G・C1–C3、
   手証明全文 §2（typed 子 mex・単一 R 強帰納・層域横断 2 行と横断ゼロ)、
   宣言前探索 X1–X8/Y1–Y8 (typed self-check 3,878+228 bad 0)、
   機体宣言 counts `[8928,360,8928,360,1939,114,1939,114,58911,1516,18394]`
   総計 101,503 期待 bad 0・変異電池期待値・predry sha
   `70206d62b8a8e91d97bed7403dfaf6d970db47b4c32de4cecc98e7358a5d562c`
   を事前宣言。着手時観測 HEAD `90732788`（Part DQ kit wave C・直交）。
   K1300 は s-parameter レーンが取得済み (`a20b5e25`)・直接 path probe で
   K1301 = max+1 を確保（対抗宣言なし）。
2. キット出版 `eb045ea2` (17:19:58Z) — 15 files。
   `verify_k1301.py` (sha256 `6026e07f8f61f4434c5a23738d5471bdcf871b4c91fa8aac4286a15667ff5b05`・
   engine pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`
   startup ゲート内蔵・embed は K1138/K1282..K1299 と同一 bytes)・
   `engine_block.py` (`582c93c1…`・K1282–K1299 kit と byte-identical)・
   `explore_k1301.py+.out`・`explore2_k1301.py+.out`・`predry/` 4 走
   (byte-identical sha `70206d62…` = 宣言値)。
3. （停滞）公式監査成果物・K item・README bullet の出版が
   2026-11-24T18:58Z 時点で 1 時間 39 分なし。

## 2. 後半（continuation 実行・本 log の執筆実行）

1. **着手時確認**: 最新 main 取り直し (HEAD `9bd5d9ca` 18:42:49Z・
   W-spectrum レーン)・K1300 実在 (s-parameter)・K1301 は宣言+kit のみで
   audit 成果物なし（search_code/search_commits/直接 path probe・
   items 1,272 件の 1000 件 cap 回避のため path 直撃）。
2. **fetch-back 再検証**: kit commit `eb045ea2` から 15 file raw fetch・
   sha256/size 全件一致（15/15）。verify `6026e07f…`・engine_block
   `582c93c1…`・predry 4 走同一 sha `70206d62…` は宣言値どおり。
3. **continuation 記録出版 `391cf512`** (18:59Z 前後): 競合時中止規約つき
   先行記録。
4. **公式 4 走**（fetch-back bytes から）: rc=0 全走・stdout byte-identical
   sha256 `70206d62…` = 宣言 = predry。
   - run1 同一 cwd PYTHONHASHSEED 未設定 (random)・15.7s
   - run2 同一 cwd PYTHONHASHSEED=1・16.0s
   - run3 隔離 tree isoA env -i PYTHONHASHSEED=99・16.7s
   - run4 隔離 tree isoB env -i PYTHONHASHSEED=7・15.7s
   counts `[8928,360,8928,360,1939,114,1939,114,58911,1516,18394]`
   総計 **101,503 bad 0**（`overall_bad: 0`・engine_gate PASS）。
5. **変異電池 5/5 fail-closed 宣言一致**:
   - `--tamper-engine`: rc=2・mutated sha
     `0ea47a80761d2b20bf414cd52b1535fba56829c3a4c232d1b2f5da3f81441882` ≠ pin
     （K1282–K1299 と同一変異）・`tamper_engine.info` size 0 (設計どおり)。
   - `--tamper=z11s`: rc=1・D1 bad 8,928。`--tamper=z11b`: rc=1・D2 bad 360。
   - `--tamper=z12s`: rc=1・D3 bad 8,928。`--tamper=z12b`: rc=1・D4 bad 360。
   （bad は counts テーブル D1–D4 の該当列のみ・他列 0・D5–D11 無影響＝
   宣言 §4 どおり）
6. **成果物出版 `eef36f40`**: audit_run1-4.out+.info・tamper 5 種×2・
   `detcheck.json` (status OFFICIAL-PASS)・`MANIFEST-sha256` (34 entries)。
   fetch-back 20/20 sha256 byte 一致・`tamper_engine.info` 遠隔 size 0 照合。
   push 直前の main 再取得で K1301 競合出版なしを確認（中止規約不発動）。

## 3. 受入判定

- 公式 4 走 stdout が宣言 sha・predry sha と完全一致・rc 全 0。
- 変異電池が宣言どおり fail-closed（rc・bad 個数の両方で一致）。
- 成果物 20 file の fetch-back byte 一致。kit bytes は一切変更していない
  （verify・engine_block・宣言ノートの sha は出版時から不変）。
- より K1301 package は machine-audit 完了・定理（手証明は宣言ノート §2）
  として受入。計算結果 (census 101,503 点) は定理の実機照合であって
  証明の代替ではない。標準 11×11 空盤・二石 root・S2・class 1/2/4 は
  全時点で UNKNOWN のまま・verdict 不消費。

## 4. 運用知見（今回）

- **同一 lane の hourly 実行間で chain を分割した初の事例**:
  宣言+kit 出版が先行実行の時間切れ/$reset で止まった場合、残工程は
  fetch-back bytes から機械的に継続できる。継続前に
  (i) 競合出版の機械チェック (ii) fetch-back sha 全件一致 (iii) 中止規約
  つき continuation 記録の先行出版、の 3 点を必須とする手順は
  長期レーンの takeover 規律と整合し機能した。
  （宣言ノート自体に takeover 条項が書かれていない場合も、
  「bytes 不変・中止規約・先行記録」の 3 点lesら停止可能な設計にすれば
  安全に継続できる。）

## 5. 次課題（高速レーン）

1. **K1302採番チェックを最初に必ず**（直接 path probe・最新 items 上の
   max 確認）。moment/W-spectrum/K1300 s-parameter 等の並走レーンに注意。
2. **K1302 本命: O9⁗ — T-PDT13/T-BDT13・T-PDT14/T-BDT14（z13/z14 typed
   全称・層厚 L(13)=L(14)=14）**: C 子は本項 z11/z12 定理を全 R 参照
   （同構文で証明可能な見通し）・z13 は層域横断 2 行（budget 12,13 が
   z12 主則域 R≥12 を読む）・z14 は横断ゼロ ((14,14))・完了で
   sharpened C-PSF′ が w=14 まで全称化。入力 OBS は本項 D11/Y3–Y5/Y8
   （z13/z14 band 4,500×2・beds 120×2・far-row R≥14・L-BU13G/L-BU14G
   w≤30/40 発現・dedup z=0..16）に揃っている。
3. O10⁗（L-BUzG 一般 w 全称形・境界一致 3 型の一般命題化）・
   O11（横断 2 行 / 横断ゼロの (w mod 2) 2 型による O9 一般 w 帰納の
   定式化）・O12（giant 枝刈り格子の境界側拡張 z∈{0..12} の接続記録）。
4. publish 手順は今回の 3 点必須手順（競合チェック・fetch-back sha
   全件一致・中止規約つき先行記録）を維持する。
