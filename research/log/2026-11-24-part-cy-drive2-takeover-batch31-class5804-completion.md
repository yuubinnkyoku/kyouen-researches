# Part CY drive-2 takeover 完了log: batch-31 (closure class 5804) 残27キー ad029..ad055 WIN-CONTINUE probe完遂 — 55キー全てprobe-level label確定 (LOSS 51・WIN 3・EXHAUSTED 1)・verdict不消費・11×11 UNKNOWN担保不変 (2026-11-24)

## 実行の経緯 (takeover)

- 原宣言 `21fef631` (Part CY drive-2 単一オーナー宣言・2026-11-24T02:10:13Z): drive-1
  WIN-HALT により未probeの残27キー ad029..ad055を WIN-CONTINUE設計・2-pass
  fresh-cold (budget 15M) でprobeするもの。
- 原session: drive-2 val-gate fresh 4 (`.d2-host.out`・`68f80a85`・02:11:39Z) →
  wave開始 → 02:16Z ad033/ad034 dispatch中にインフラ障害 (zombie-race) →
  incident amendment `7ff09bb8` (02:20:27Z・診断 + drive2b_local_step.sh
  事前登録 + ad033/ad034 honest label LOSS(2) 3-pass一致の記録) — 以降4時間超
  停滞・drive-2 wave成果は一切未出版 (published output/ は drive-1分のみ:
  raw/ ad001..ad028 + status.log 30行) を機械確認。
- **takeover宣言 `5855e3f8`** (earliest_takeover = 02:10:13Z + 3.5h =
  05:40:13Z 通過・対抗宣言なし機械確認・observed HEAD `b5a7ce1a`):
  `research/log/2026-11-24-part-cy-drive2-takeover-batch31-class5804.md`。
  pin・protocol は原宣言 + amendment から一切変更せず継承。

## 誠実開示: 実行環境リセット事故 (1回・出版データには影響なし)

takeover実行中に1度の実行環境リセットが発生。原因は本takeover host側の設計違反:
**1回の bash 実行に val-gate + 初-wave (2 step) を連結した**こと (CP事故の
再発・2回目)。当該分はローカル喪失・**未出版につき evidence とせず**、
kit再復元 (published bytes・pin再照合: runbatch.sh `f591f8c2…` /
jsreplay.js `84585617…` / drive2b_local_step.sh `4fcb5775…` /
batch-keys.json `d058fddc…` 他) からやり直した。**出版されたのは再実行分のみ**
(A `9f021706` のcommit messageに当時開示済み)。以降は「1 bash実行 = 1 wave」を
厳守し、再発なく27キーを完走した。

## 実行結果 (val-gate + drive2b 27キー完走)

- **val-gate**: takeover host fresh 4/4 node-exact (`.tk-host.out`・published
  baselinesと wall_s 以外全field一致: 2M×2 result 0 / 15M×2 result 2 nodes
  3,651,923・5,040,200)。原session分 `.d2-host.out` (published) と併存。
- **drive2b (budget 15M・2-pass fresh-cold・1 invocation 2キー×2 worker・
  27キー ad029..ad055 完走)**:
  - **PASS 26行 (うち LOSS 25行・WIN 1行)**: nodes 1,644,957 (ad054) 〜
    11,268,913 (ad032)。全行 p1==p2 (determinism・genuine MISMATCH 0・
    artifact MISMATCH 0・TRUNCATED-RETRY 0)。
  - **WIN 1行 ad055 (result 1・nodes 3,364,655)**: runnerは正規の WIN-HALT
    status行をappendし、WIN-CONTINUE設計 (宣言事前登録) どおりwaveを継続して
    batch完走。
  - **EXHAUSTED 1行 ad043 (budget 15M×2完走後消費・nodes 15,000,000)**: honest UNKNOWN・同一条件での再probeはしていない
    (高budget再probeは別Partの対象)。PASS行とEXHAUSTED行の二重記録は
    runnerの事前登録設計どおり。
  - ad033/ad034: fresh再probeで amendment診断値 (LOSS・nodes 5,883,887 /
    4,885,748) と node-exact 一致 = 独立追試成立。
  - status.log 59行 (drive-1 30行 prefix 不変 + drive-2 29行 append-only・
    最終行 ALL-DONE確認)。

## batch-31 (class 5804) 集計 — 55キー全てprobe-level label確定

- drive-1 (Part CY 原session・published): WIN 2 (ad024 nodes 4,360,661 /
  ad028 12,803,283)・LOSS 26・対象 ad001..ad028。
- drive-2 (本takeover): LOSS 25・WIN 1 (ad055 3,364,655)・EXHAUSTED 1 (ad043)。
- **計55 = LOSS 51 + WIN 3 + EXHAUSTED 1。ただし verdict不消費 (honest label)**。
  canonical adoption は全55キー確定を受けての reaudit を経て pinned
  fail-closed merger `90711961…` での別adoption Part 専権 (本レーンは
  代行しない)。WIN 3行の採用は scrutiny owner C++第二実装 gate
  `9193f5b6…` 通過後のみ。

## 出版 chain (全push fast-forward成功・競合なし)

- A `9f021706` (val-gate `.tk-host.out` 4・observed HEAD `c075b512`)
  → checkpoint1 `49e6fa3f` (ad029..ad036・8/8 PASS・observed HEAD `52939752`)
  → checkpoint2 `9ede0202` (ad037..ad052・15 PASS + ad043 EXHAUSTED・
  observed HEAD `ce5cf7c9`)
  → B3 `a9dba61e` (ad053..ad055 + status.log 59行・observed HEAD `9ede0202`)
  → C `70d79714` (README drive-2節追記 8,783B + MANIFEST-sha256 194 entries
  path-sorted・observed HEAD `a9dba61e`) → 本完了log。
- **B3 commit message 計数誤記の訂正**: B3 message内「EXHAUSTED 0...」は
  正しくは「EXHAUSTED 1 (ad043)」(同message内で自己訂正文言
  「(正: EXHAUSTED 1 ad043)」付き)。本logで正式に明記する。誤記はcommit
  messageのみで、status.log・README・MANIFEST の実データは初めから正しく
  EXHAUSTED 1 (ad043) を記録している (status.log 59行・README集計節
  機械確認済み)。
- **C fetch-back byte検証 (完了)**: push直後の raw.githubusercontent fetch が
  旧版 (README 5,744B 80行・MANIFEST 旧130行) を返したため raw CDN stale
  (既知事象) と記録し、API (get_file_contents ref=main) で実状態検証:
  README sha256 `e365699e…` (8,783B・121行・touching commit `70d79714`
  06:58:27Z)・MANIFEST 194行 (先頭entry = README `e365699e…` = local
  README の sha256sum と一致)。遅延解消後の再 raw fetch で README/MANIFEST
  とも新版配信を確認 (open_url 抽出の折返し差異を除き内容一致)。
  よって C 出版の fetch-back 検証は完了。

## 並走状況 (本Part完了時点・非接触確認)

Part DF/DG (batch-28 P2/P3・aa*キー) / K1282 fast lane (`33cb9306` 完了) /
K1283 出版 (`84d74dc3` + addendum `49f8f19a`) / K1284 宣言 (`66f06ad2` +
訂正 `c5709b87` + 専用機体 `35706ae6`・z1ラダー) / Part CP drive-3 takeover
(batch-30・宣言 `3f0aeb55` + A val-gate `ce5cf7c9`・ac030..ac054) は
いずれも対象キー・実験dir 完全分離。

## レジューム (着手前に必ず最新main再取得・hourly並走注意)

次回候補: (a) batch-31 55キー確定を受けての reaudit/adoption は merger
`90711961…` 別Part専権 (本レーンnon-authoritative)・WIN 3行は scrutiny
gate `9193f5b6…` 待ち。(b) **ad043 高budget再probe (別Part・単一オーナー
宣言が必要)**: budget 15M×2 で完走消費 (p1 wall ≈108s @15M → 30M は
1pass ≈216s で 290s wrap 内)。結果が EXHAUSTED の場合は再び honest UNKNOWN。
(c) batch-28 queue registry P4 パッケージ (CS/CT解決4行 + 5行・
est≈373.8M) の第三実装交叉検証 (cross-invocation step設計の宣言が必要・
対抗宣言チェック必須)。(d) batch-30 drive-3 は Part CP takeoverが進行中
のため対抗宣言チェック必須。5343・2251・5804・34269等全class・root・
空盤は全時点UNKNOWNのまま。

## verdict不消費・UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 5804 (55キーすべて・WIN/LOSS/EXHAUSTED行を
含む) は本takeoverの実行・出版のどの時点でもUNKNOWNのまま。** nodes数・
wall秒数を勝敗や距離として読まない。被覆・secured・root勝敗の主張を
しない。
