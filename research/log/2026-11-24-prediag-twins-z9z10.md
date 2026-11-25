# run log: 2026-11-24 pre-diag twins z9/z10 (K1299 fast lane)

単一オーナー実行: 共円ペア面 z9/z10 の pre-diag 双生児 typed 全称
（T-PDT9/T-BDT9・T-PDT10/T-BDT10・L-BU9G/L-BU10G・sharpened C-PSF′
w=9,10 実例化）を publish-then-execute 全工程で出版した。

## 実行 chain

1. **着手時観測**: HEAD `4377c987`。K1294 kit（`9421cbc2` pin とおり
   verify_k1294.py sha256 `b3974b63…`・engine_pin `bd5f22e4…`・
   engine_block.py `582c93c1…`）を raw fetch して再利用。最新 K item は
   K1298（parity-graded レーンが colliding K1294 から再採番したもの・
   `74753b66`）。intervening Part DP commits（`8c3b77ae`/`7a5ee133`/
   `4f731fb1`）は adoption lane/log・内容直交。K1295/K1296/K1297 は
   projective-blocking-kyouen / moment レーンが取得済み。
2. **採番**: max+1 = **K1299** を 直接 path probe
   （`research/knowledge/items/K1299-prediag-twins-z9-z10.md` not found）
   で空き確認（宣言 push 直前に再確認・1 回の再実行なし・ race なし）。
3. **宣言前探索**（explore_k1299.py / explore2_k1299.py・K1290/K1294 kit
   構文の踏襲）: X1–X4 z9/z10 band/bed (R,δ) 表 mixed 0・R<10 層が
   2·[R odd]・R=10 seam 全 1（z9）/全 0（z10）・R≥11 主則一致
   （核 z9 δ=9→2・z10 δ=11→2）。X5/X6 L-BU9G/L-BU10G w≤30 bad 0
   （1,972 checks）・w=1 edge {0,2}。X7 cpsf probe z=0..12 全 bad 0。
   **X8 typed 子 self-check: slices 3,878 + beds 228 bad 0**
   （申立テーブル + K1294 既刊 z7/z8 + 閉形式のみで構成した子 mex =
   申立値 = engine・手証明構文の宣言前検証）。Y1/Y2 z9/z10 wide census
   8,928/360 × 2 bad 0。Y3–Y5 **z11/z12 OBS**
   （band 4,500×2・beds 120×2・far-row 216×2・low-R (R<12) hist
   {0:402,2:392}×2・cpsf bad 0・全称主張なし）。Y6 交差 engine
   z=9..12 各 464 mismatch 0。Y7 **L-BU11G/L-BU12G 発現**（w≤40 bad 0・
   plane-11: 2·[t odd] (t<12)/g1(t−10)・plane-12: …/f0(t−12)）。Y8
   T-TWIN bad 0・**dedup z=0..14 全 15 面 mixed 0・cpsf bad 0**
   （C-PSF′ 観測 plane 14 まで拡張）。
4. **機体**: verify_k1299.py（sha256 `0fa53559…`・engine pin
   `bd5f22e4…` startup gate・embed bytes は K1138/K1282..K1294 と同一）。
   バッテリ D1–D4 census・D5–D8 typed 3-way・D9
   （L-BU9G/L-BU10G 493×2・K1294/K1290/K1289/K1288/K1286 アンカー
   4,690×4+2,345・sharpened C-PSF′ identity **w=0..10** 25,795・T-TWIN
   201・閉形式×両 engine z∈2..11 1,200・w=1 edge 4）・D10 交差 engine
   ・D11 OBS（z11/z12・L-BU11G/L-BU12G・dedup z=0..14）。
   **predry 4 走byte-identical sha256 `e9b3784a…`**
   counts [8928,360,8928,360,1939,114,1939,114,49291,1516,17046]
   総計 90,535 bad 0・変異電池 5 モードを local 事前確認
   （engine rc2・z9s 8,928/z9b 360/z10s 8,928/z10b 360 全 rc1）。
5. **出版 chain（main 直接・全 fetch-back byte 一致）**:
   - 宣言ノート **`506a7d18`**
     （`research/log/2026-11-24-prediag-twins-z9z10-single-owner-note.md`・
     証明全文 §2・fetch-back sha256 一致）。
   - キット **`fc3f987f`**（15 files・README/verify/engine_block/explore×2
     +.out/predry×8・fetch-back 15/15 byte 一致）。
   - 公式 4 走（fetch-back bytes・同一 cwd ×2 PYTHONHASHSEED random/1・
     隔離 tree isoA/isoB env -i 99/7）: 全 rc=0・stdout byte-identical
     sha256 **`e9b3784a…`** ＝宣言＝predry（~12.2-12.8s/走）。総計
     90,535 bad 0。
   - 変異電池 5/5 fail-closed 宣言一致（`--tamper-engine` rc2 mutated
     sha `0ea47a80…`≠pin・tamper_engine.info size 0・z9s/z9b/z10s/z10b
     rc1 bad 8,928/360/8,928/360）。
   - 成果物 **`f9afeadd`**（audit_run1-4.out+.info・tamper 5 種×2・
     detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries・
     fetch-back 20/20 byte 一致）。
   - K item + 本 run log + knowledge README 末尾 bullet（別 commit）。

## honest 記録

- 採番は全程で一度も競合しなかった（宣言 push 直前の再取得 HEAD
  `4f731fb1` で対抗なし・K1299 直接 probe で空き再確認）。
  K1294 のときの 21 秒レースは不発。
- D9 の (c)–(f) アンカー再照合は K1290→K1294 と同一 box で実施
  （published claim 関数を verify 内に再記載して engine と照合）。
- explore2 の low-R hist は z11/z12 とも {0:402, 2:392}（K1294 の
  z9/z10 {0:346,2:340} の 1 box 拡張版・R<12 対象 794 cells）。
- 手証明の核 cell の再核算（z9: 核 δ=9・C 核 δ=10・z10: 核 δ=11・
  C 核 δ=10・comp 核 δ=12）は探索出力の (R,δ) 表と照合してから宣言に
  固定した（K1289 slope-trap 教訓の踏襲）。
- 有意な新しい構造: 層域横断が **2 行**（層内最終行 + seam）に広がる
  世代を初めて明示的に記述（K1294 の z7 も後から見れば同型
  〔R=7/R=8〕で本項はその平行移動だが、値の定数落ちが parity 固定で
  2 行ぶん揃うことを場合表で完備した）。

## 受入判定

- 4 定理 + 2 補題は万能記号で手証明済み（宣言ノート §2）。
  census 90,535 点は照合であり証明の代替ではない。
- sharpened C-PSF′ の全称域は **w ∈ {0..10}**。z11/z12・L-BU11G/
  L-BU12G・dedup z=11..14 は OBS のまま全称主張なし。
- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は全て UNKNOWN のまま・verdict 不消費。

## 次課題（次回 single-owner 候補）

1. **採番チェックを最初に必ず**（現在の最高番号は本項で K1299。
   次は K1300 を max+1 で直接 probe）。
2. **K1300 本命: T-PDT11/T-BDT11・T-PDT12/T-BDT12（O9‴・z11/z12
   typed 全称・層厚 L(11)=L(12)=12）** — C 子は本項 z9/z10 定理を全 R
   参照（同構文）・z11 は C 子横断 2 行（budget 10,11〔R=11 層内 +
   seam R=12〕が z10 主則域 R≥10 を読む）・z12 は横断ゼロ
   （層厚一致 (12,12)）・入力 OBS は本項 D11 に揃っている
   （z11/z12 band 4,500×2・beds 120×2・far-row 216×2・low-R hist。
   完了で sharpened C-PSF′ が w=12 まで全称化）。
3. C-PSF′ の w 帰納（O9‴ 主体: 横断型=奇数世代・横断ゼロ型=偶数世代
   の (w mod 2) 2 型定式化。層核の mex{0,1}=2/mex{2,3}=0 機構は
   w 非依存で第 5 世代まで確認済み。一般 w は (w mod 4) 分類 O11 と
   統合する見取り）。
4. L-BUzG 族の一般 w 全称形（O10‴・閉形式 region 計算・境界一致
   3 型スキーム。L-BU11G/L-BU12G OBS が入力）。
5. O12 giant 枝刈り格子（z∈{0..10} で対角下全域 k≤0 が O(1) 即値化・
   接続記録のみで採用判断はオーナー）・O13 K1287 O1 残部
   （SLB2/SLB3・L/Am frontier・本レーン未着手）。
6. 運用: K1294 の lessons 踏襲どおり README push は push 専用最小
   block で実施（今回は成功・fetch-back 3 点検で完了）。
