# run log: pre-diag 双生児 z13/z14 (K1302) — publish-then-execute 全工程記録

単一の hourly 実行内で完結した chain の記録 (K1301 と異なり分割なし・takeover なし)。
同一実行内で 宣言前探索 (X1–X8/Y1–Y8) → 検証機体構築 → 宣言前修正 → predry →
宣言出版 → kit 出版 → fetch-back → 公式 4 走 → 変異電池 → 成果物出版 → K item →
README bullet までを完走した。

## 1. 着手時確認

1. 最新 main 取り直し: HEAD `1f08b0bc` (2026-11-24T19:19:40Z・PG(2,8)/AG(2,8)
   cap games レーン・直交)。K1301 は本レーンの先行実行が出版済み
   (`84ee5369`・README bullet `dd9e85f7`)。intervening commits (`ff3e99c1`
   W_24 s-spectrum・`1f08b0bc` cap games) は全て領域直交。
2. K1302 採番確認: search_commits "K1302" = 0 件・K1302 = max+1 として確保
   (push 直前にも再確認)。

## 2. 宣言前工程 (同一実行内)

1. **探索**: `explore_k1302.py` (X1–X8) — z13/z14 band/beds の (R,δ) 表
   (mixed 0・層厚 14 の直接観測・R=14 seam 行 z13 全 1 / z14 全 0)・
   L-BU13G/L-BU14G 発現 1,972 checks bad 0・sharpened C-PSF′ probe z=0..16
   bad 0・typed 子 self-check 3,878+228 bad 0。
   `explore2_k1302.py` (Y1–Y8) — z13/z14 wide census 8,928/360 × 2 bad 0・
   z15/z16 OBS (band 4,500×2・beds 120×2・far-row m=12 R≥16 210×2・low-R
   hist {0:637,2:616}×2)・ordered engine 交差 z=13..16 mismatch 0・
   L-BU15G/L-BU16G 発現 probe (z=16,17, w≤40) bad 0・dedup z=0..18 全 19 面
   mixed 0 (C-PSF′ 観測が plane 18 まで拡張)。
2. **検証機体**: K1301 kit `verify_k1301.py` からの機械的 surgery (55 edits)
   で `verify_k1302.py` を生成。
3. **宣言前修正 (honest・ノート §2.7)**: 初回ローカル実行が bad 2,376
   (D1–D8 の engine plane 実引数が古い 11/12 のまま残留) を指摘。
   主張テーブル側は正しく engine が誤りだった。plane 引数 4 箇所×2 を
   13/14 に修正 + docstring/stale comment 全面書き換え → bad 0
   (修正後 sha256 `336aaf7a80f518a56e5dee70307ffe6bfedc96d24b0420819fec0815e5fafb16`)。
   far-row 電池は K1301 §2.7 の教訓を事前適用し R≥16 guard + low-R 分離
   (設計修正不要)。
4. **変異電池の宣言前確認**: `--tamper-engine` rc 2 (mutated sha
   `0ea47a80761d2b20bf414cd52b1535fba56829c3a4c232d1b2f5da3f81441882`)・
   z13s/z13b/z14s/z14b rc 1 (D1–D4 bad 8,928/360/8,928/360)。
5. **predry 4 走**: 同一 cwd PYTHONHASHSEED random/1 ×2 + 隔離 tree
   env -i PYTHONHASHSEED 99/7 ×2。stdout 全走 byte-identical
   sha256 `f6f26e095f1cb44b597fd2a3b7043c170e111f99119524c3099ac34630b43b0e`
   (約 19–20s/走)。counts
   `[8928,360,8928,360,1939,114,1939,114,68531,1516,19232]` 総計 111,961 bad 0。

## 3. publish-then-execute

1. **宣言ノート出版 `4905228a`**: 主張 T-PDT13/T-BDT13/T-PDT14/T-BDT14・
   L-BU13G/L-BU14G・C1–C3、手証明全文 (typed 子 mex・単一 R 強帰納・
   z13 層域横断 2 行 (budget 12,13 が z12 主則域 R≥12 を読む) と
   z14 横断ゼロ ((14,14))・mex 場合表)、機体宣言 (counts・変異電池期待値・
   predry sha・verify sha 336aaf7a… の事前宣言)。fetch-back byte 一致。
2. **kit 出版 `3f436333`** (15 files): verify_k1302.py・engine_block.py
   (`582c93c1…`・K1282–K1301 kit と byte-identical)・explore×2 py+out・
   predry_run1-4.out+info。**fetch-back 15/15 byte 一致**
   (verify sha `336aaf7a…`・predry sha `f6f26e09…` は宣言値どおり)。
3. **公式 4 走** (fetch-back bytes から): rc=0 全走・stdout byte-identical
   sha256 `f6f26e09…` = 宣言 = predry。
   - run1 同一 cwd PYTHONHASHSEED 未設定 (random)・19.3s
   - run2 同一 cwd PYTHONHASHSEED=1・19.0s
   - run3 隔離 tree isoC env -i PYTHONHASHSEED=99・19.4s
   - run4 隔離 tree isoD env -i PYTHONHASHSEED=7・19.4s
   counts `[8928,360,8928,360,1939,114,1939,114,68531,1516,19232]`
   総計 **111,961 bad 0** (`overall_bad: 0`・engine_gate PASS)。
4. **変異電池 5/5 fail-closed 宣言一致**:
   - `--tamper-engine`: rc=2・mutated sha `0ea47a80…` ≠ pin
     (K1282–K1301 と同一変異)・`tamper_engine.info` size 0 (設計どおり)。
   - `--tamper=z13s`: rc=1・D1 bad 8,928。`--tamper=z13b`: rc=1・D2 bad 360。
   - `--tamper=z14s`: rc=1・D3 bad 8,928。`--tamper=z14b`: rc=1・D4 bad 360。
   (bad は counts テーブル D1–D4 の該当列のみ・他列 0・D5–D11 無影響 =
   宣言 §4 どおり)
5. **成果物出版 `021236fc`**: audit_run1-4.out+.info・tamper 5 種×2・
   `detcheck.json` (status OFFICIAL-PASS)・`MANIFEST-sha256` (34 entries)。
   **fetch-back 20/20 sha256 byte 一致**・`tamper_engine.info` 遠隔 size 0 照合。
   push 直前の main 再取得で isolated lane の Part DT log (`305d1590`・
   直交・経路無衝突) のみを確認 (K1302 競合出版なし・中止規約不発動)。

## 4. 受入判定

- 公式 4 走 stdout が宣言 sha・predry sha と完全一致・rc 全 0。
- 変異電池が宣言どおり fail-closed (rc・bad 個数の両方で一致)。
- 成果物 20 file の fetch-back byte 一致。kit bytes は一切変更していない。
- より K1302 package は machine-audit 完了・定理 (手証明は宣言ノート §2)
  として受入。計算結果 (census 111,961 点) は定理の実機照合であって
  証明の代替ではない。標準 11×11 空盤・二石 root・S2・class 1/2/4 は
  全時点で UNKNOWN のまま・verdict 不消費。

## 5. 運用知見 (今回)

- **surgery 生成機体の痕跡検査**: K1301 verify からの機械的平行移動生成は
  docstring・comment だけでなく engine 呼び出しの引数埋め込み箇所も取り残す
  ことがある。宣言 predry の前に (a) 全 battery の初回ローカル実行 bad 0 確認
  (b) grep による引数・文言の stale 検査、を手順に含めるべき (今回は (a) が
  捕まえた)。悪いまま出版すれば「主張対 engine」の大量 bad として
  fail-closed に終わるだけで定理嘘証明にはならないが、宣言前発見が望ましい。
- **単一実行完走**: 1 実行で探索→宣言→公式監査まで積むには predry 段階で
  口を揃えておく (counts 実測・sha 確定・byte-identity 3 環境) のが効率的。

## 6. 次課題 (高速レーン)

1. **K1303 採番チェックを最初に必ず** (直接 path probe・最新 items 上の
   max 確認)。並走レーン (moment/W-spectrum/s-parameter/Part D/DT 等) に注意。
2. **K1303 本命: O9(5) — T-PDT15/T-BDT15・T-PDT16/T-BDT16 (z15/z16 typed
   全称・層厚 L(15)=L(16)=16)**: C 子は本項 z13/z14 定理を全 R 参照・
   z15 は層域横断 2 行 (budget 14,15 が z14 主則域 R≥14 を読む)・
   z16 は横断ゼロ ((16,16))。完了で sharpened C-PSF′ が w=16 まで全称化。
   入力 OBS は本項 D11/Y3–Y5/Y8 (z15/z16 band 4,500×2・beds 120×2・
   far-row R≥16・L-BU15G/L-BU16G w≤30/40 発現 (g1(t−14)/f0(t−16))・
   dedup z=0..18) に揃っている。typed self-check・宣言前構文検証は
   X8 方式をそのまま平行移動できる。
3. O10(5) (L-BUzG 一般 w 全称形・境界一致 3 型の一般命題化)・
   O11 (横断 2 行 / 横断ゼロの (w mod 2) 2 型による O9 一般 w 帰納の
   定式化)・O12 (giant 枝刈り格子の境界側拡張 z∈{0..14} の接続記録)。
4. 手数が続くなら z15/z16 packet を本項同様に一気通貫で実行する
   (探索スクリプトの平行移動・verify surgery の stale 引数検査を
   必須ステップとして)。
