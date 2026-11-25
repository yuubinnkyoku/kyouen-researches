# Part EK 完了: aj030/aj039 30M reprobe — 両キー解決 (aj030 probe-level WIN 15,284,699 / aj039 fresh exact LOSS 16,549,916・いずれも verdict 不消費・11×11 UNKNOWN)

date: 2026-11-25 (long-term lane, single-owner)

宣言 `research/log/2026-11-25-part-ek-aj030aj039-reprobe30m-declaration.md`
(commit `dd448fec`・observed HEAD `e0ca8d75`) の補完。完全な protocol・
kit pin・per-file hash:
`research/experiments/n11-centralreply-closure-class30484-aj030aj039-reprobe30m-20261125/`
の README.md と MANIFEST-sha256.txt (rev2・42 entries)。

## Outcome

- batch-39 (Part EH) が 15M で EXHAUSTED (honest UNKNOWN) とした
  class 30484 境界2キーを、事前宣言済み 30M 条件 (order=0・fresh-cold・
  two-pass) で再 probe し、**両キーとも 30M 予算内で解決**:
  - **aj030 (1152922604135251976, 65536): probe-level WIN
    `30000000,1,15284699` (two-pass node-exact・wall 181s/190s)。**
    15M EXHAUSTED 履歴と整合する予算区間 (15M, 30M] で解決。
    WIN-HALT rc=45・**verdict は不消費** (scrutiny-owner C++ gate
    `9193f5b6…` 専権・本環境はコンパイラ不在)。
  - **aj039 (1152922606282735616, 65536): fresh exact LOSS
    `30000000,2,16549916` (two-pass node-exact・wall 96s/98s)。**
    15M EXHAUSTED 履歴と整合する予算区間 (15M, 30M] で解決。
    **verdict は不消費**・将来 Part の loss-only adoption 候補
    (pinned merger `90711961…`・BASE = Part EI chain head `73482be0…`
    6,712行)。
- val-gate 4/4 (2M EXH×2 = (2000000,0,2000000)・first-15m =
  (15000000,2,3651923)・second-15m = (15000000,2,5040200)・published
  baseline と wall_s 以外全列一致) = drive-start 要件。
- anchors 3/3 two-pass node-exact @30M cap: aj001 = LOSS 5,156,075
  (b39 15M 条件値 = 解決 node の cap 非依存性の再確認)・aj049 = WIN
  4,998,452 (WIN-HALT・verdict 不消費・ED の af029 anchor 前例と同一運用)・
  af039 = LOSS 19,234,232 (Part EA 30M 条件値 = budget-crossing regime
  (15M, 30M] の代表解・ED 60M cap でも同一 node を確認済み)。
- 0 MISMATCH・0 EXHAUSTED@30M・0 TRUNCATED 残置。両キーが 30M で解決した
  ため 60M ladder は不要 (宣言条件 4 の 60M 別宣言は起動せず)。
- machine audit `audit_ek.py` (CORRECTION 版 `7636def1…`) **79/79 gates
  PASS**・`output/audit_ek.json` (10,375B・sha256 `d9aa8aab…`)・
  tamper battery 3/3 fail-closed (T-EK1 raw nodes 桁 → two-pass gate・
  T-EK2 status verdict 桁 → win-line gate・T-EK3 anchor nodes 桁 →
  anchor gates)・制御 (復元後 clean) 79/79 PASS 取り直し。

## Publish chain (全 wave fetch-back byte 一致・publish-then-execute)

`dd448fec` 宣言 (observed HEAD `e0ca8d75`・対抗宣言走査 0) →
`5d54005e` kit B1 (24 files: scripts 3 / input 5 / val-gate 8 byte-clone /
sources 6 / README (pending) / MANIFEST rev1) → `e33c3526` kit B2
(canonical-cache-ei-merged-73482be0 279,805B・6,712行・fetch-back cmp PASS) →
`05e8d5bb` wave C (18 outputs: status.log 7 lines・drive outs 3・raws 10・
val-gate host sidecars 4・fetch-back 18/18) → `23621276` CORRECTION
(audit_ek.py 定数 2文字修正版 `7636def1…`) → `15ec6809` wave D
(audit_ek.json 79/79 + README run record 確定 + MANIFEST rev2 42 entries) →
本完了log。

kit-stage second-environment verification (independent lane・pre-drive・
`792c9692`): 25 kit files B2 bytes を出版 chain と byte 照合し不正なし
(jsreplay / cache / quarantine / b39-status / exh raws / 5 inputs /
val-gate 8 / runner BUDGET 行 delta / MANIFEST 23/23 / TARGETS×
batch-keys-b39 field 照合・cache 不在)。

## Honest incidents (記録)

1. **実行環境 reset**: anchors 同期並走の最初の呼び出しが 300s shell cap
   を超過し実行環境が reset・工作 dir 消滅。**kit bytes が全て出版済み
   fetch-back 検証済み**だったため、B2 bytes からの再構成 (MANIFEST 23/23
   pin) で完全復旧 (Part EE wave F `dda65bbb` と同じ pattern の再実証 =
   「再現不能なローカル状態だけに重要証拠を残さない」原則)。以後の長時間
   pass は detached (nohup+disown) + cross-invocation 監視 + truncated
   guard で実行し全 pass 完走。val-gate 4/4 を reset 前後で 2 回再現
   (両回とも node-exact)。
2. **audit_ek.py 定数転記ミス (fail-closed 検出)**: wave B1 版
   (`0e06d210…`) の JSREPLAY_SHA 定数に 2文字 typo (`…3f1c…` を
   `…3d1c…`)。初回 audit が `pin:scripts/jsreplay.js` で即 fail-closed
   検出。実 jsreplay bytes (84585617…)・MANIFEST・全実測値は正しく無影響。
   修正版を CORRECTION `23621276` で出版・その bytes から 79/79 を再取得
   (Part EE 第52条①(a)「fail-closed pin 設計が pins 転写ミスを工程内で
   捕捉する」の再実例)。
   - 附带記録 (verification depth の honest 観察): 並走 second-env log
     `792c9692` の K2 は「`audit_ek` internal pins all match」と要約
     しているが、JSREPLAY_SHA 定数については実際には typo が存在した
     (彼らの照合は定数↔実 file の hash 比較レベルまでは到達しておらず
     検出されなかった)。**期待値 pin の妥当性は kit-stage の静的照合のみ
     では確定せず、drive 時の fail-closed 実行で確定する**ことの再確認。
3. **non-FF push 競合 1回** (wave D の push 直前に並走 commit 挟入):
     最新 HEAD 再取得のうえ同一内容を再 push で解決 (内容変化なし)。

## class 30484 の会計 (本 Part 後・verdict 不消費のため SSOT は不変)

- Part EI 後の class 30484 unknown 構成 (6) = EXH {aj030, aj039} + 不消費
  WIN {aj049, aj050} + claim-reserved {ai044, ai048 (EF 所有)}。
  本 Part の honest label は「probe-level の観測」であり canonical
  採用を伴わないため closure-classes 上の unknown 会計は変わらない。
  aj039 の LOSS 行は次の loss-only adoption Part で canonical 採用され
  うる (採用後 unknown 6→5 になる見込み・aji044/ai048 と WIN 行は残る)。
  aj030 の WIN 行は不消費 WIN 行 (aj049/aj050・af系 6行 等) と同じ
  scrutiny 待ちの位置に移る。
- **class 30484 自体・標準 11×11 空盤・19 central-reply roots・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4・30118 はすべて全時点
  UNKNOWN のまま。** nodes は bookkeeping であり勝敗・被覆・距離の
  主張ではない。verdict は 1行も消費していない。

## Resume (次の実行: 着手前に必ず最新 main 再取得・hourly 並走注意)

1. **aj039 LOSS 行の loss-only adoption Part が次の自然な Part**
   (Part EL 仮): EI パターンの maker/merger (`90711961…` byte-clone)・
   BASE `73482be0…` (6,712行) + 1 行 → refresh reaudit wave (EE/EI 型
   refresh fork を新 BASE pin `73482be0…` に向けて作り直し) → extractor
   delta。入力 raw は本 Part wave C の aj039 p1 `529b3efe…` / p2
   `930d0b48…` (two-pass node-exact `30000000,2,16549916`)。
   aj030 の WIN 行は採用対象外 (scrutiny 専権)。
2. closure 上の probe 可能残作業 (">fresh") は Part EJ (batch-40,
   class 30118) が並走で drive 中。本 Part の keys (aj030/aj039) は
   30M 条件で解決済みとなり、以後の「同一条件 (30M) 再probe」は不要
   (EXHAUSTED でなく resolved 行であるため再実行禁止規約の対象外だが、
   他条件再probeの必要性もない)。
3. Part EJ が 50/50 完走した場合、その46+ LOSS 行 (inc 毎) の adoption
   Part・EXHAUSTED 行の ladder が次の前線 (EJ 完了log に従う)。
4. 標準 11×11 空盤は UNKNOWN のまま。勝敗・被覆・secured coverage の
   主張は本 Part のどこにもない。
