# Part CY drive-2 宣言 (2026-11-24): batch-31 (closure class 5804) 残27キー ad029..ad055 — WIN-CONTINUE・publish-then-execute

単一オーナー: n11中央応答レーン (長期レーン・本セッション本host)。Part CY
drive-1 (宣言 `afc1bcc5`・完了log `81bdf46a`) の直接後続。対抗宣言なし
(push直前の最新mainコミット列に batch-31 drive-2 / class 5804継続 probeへの言及
ゼロを機械確認済み・observed HEAD `81bdf46a`・2026-11-24T02:08:07Z)。

## 1. スコープ

drive-1 WIN-HALT (distinct WIN 2行 ad024/ad028でwave halt) により未probeのまま
停止していた **残27キー ad029..ad055** を、**WIN-CONTINUE設計**で2-pass
fresh-cold probeする。WIN行が出ても停止せず、27キーすべてが
PASS (WIN/LOSS) / EXHAUSTED の honest labelを得るまで (または誠実打ち切りまで)
続行する。EXHAUSTED (budget消費未解決) はhonest UNKNOWNのまま記録のみ。

**verdict不消費** (WIN/LOSSはhonest label、canonical adoptionは別adoption Part
(pinned fail-closed merger `90711961…` 経由) のみ・WIN行scrutinyはC++第二実装
gate (`9193f5b6…`) 専権)。閉鎖・被覆・secured・root勝敗の主張はしない。

## 2. kit (変更点は1ファイルのみ)

- 実験dir・input・runner・solverはすべてdrive-1と同一 (published・不変):
  `input/batch-keys.json` `d058fddc…`・`scripts/runbatch.sh` `f591f8c2…`
  (byte-clone・stop rules内蔵: WIN rc=45 / MISMATCH rc=42・budget 15M・
  2-pass fresh-cold・TRUNCATED-RETRY・EXHAUSTEDはhonest UNKNOWN)・
  `scripts/jsreplay.js` `84585617…` (byte-clone)。
- **新規 `scripts/drive2_local_step.sh` (sha256
  `8baf929b0400cf3fffac0bba250f385bdb9dfe59ea2da82e60c42f175de92f8b`)**:
  published `drive1_local_step.sh` (`26347816…`) からの最小delta。変更は
  機械diff確認済みの EXACTLY 2 gates: (1) start gate「status.logにdistinct WIN 2行
  あれば即時WAVE-HALTED」を削除 (drive-1終了状態で即haltするため・drive-2は
  batch完走がpre-registered wave-end)、(2) end gate「wins>=2でexit 45」を
  informational WIN-CONTINUE lineに変更。**pinned runnerはbyte不変**でWIN検出時の
  「adNNN WIN-HALT」status lineはrunner自身がappendし続ける (honest label・
  drive-2 orchestrationはlabelとして読むだけ)。ほかのguard
  (worker `timeout 260`・空remainingキーALL-DONE・done-set dedup・EXHAUSTED continue・
  MISMATCH hard-stop rc=42) はすべてverbatim。
- val-gate: 宣言後に本host fresh 4 (sanctioned同一キー・同一基準
  budget/result/nodes比較 (wall_s除く)・sidecar suffix `.d2-host.out`) を必須と
  する。published baselines (`6e902ab1…`/`eeafe3ac…`/`8035fe54…`/`91dffdec…`)
  と一致しなければhard-stop。

## 3. 事前登録

- drive-2の実行は script `timeout 290 bash scripts/drive2_local_step.sh` 反復
  (1 invocation最大2キー×2 worker)。status.logはappend-only (drive-1の30行は
  published prefix不変)。
- 結果は行ごとにhonest記録し、nodes数/wall秒数はbookkeepingであり勝敗ではない。
  期待機械簿記: probe済み全55キー確定後の drive-1結果 (LOSS 26 / WIN 2) との
  合算でclass 5804のunknown_now 55からの減算・closure table再導出はreaudit
  (別Part) が機械実施する。
- 誠実打ち切り時は成果分のみ出版・未probeキーはfileless UNPROBEDのまま
  次driveに委ねる。

## 4. UNKNOWN担保 (最優先)

**標準11×11空盤・19 central-reply roots・二石root・S2・class 5804 (55キー
すべて) は本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数・wall秒数を
勝敗として読まない。

## 5. 非接触

- Part CZ (batch-29 drive-2 WIN行 ab028第三実装交叉検証・宣言 `4c741798`・
  scaffold A `161373f9`・進行中) 非接触。
- Part CP (batch-30 class 34269 drive-2 WIN-CONTINUE・宣言 `87e19b5a`・進行中)
  非接触。
- Part CI batch-29完結出版物 (`dc93e5d6`/`c608660e`/`141cf80c`) read-only参照のみ。
- CU canonical chain (6,317行 `30ddad9d…`) read-only不変 (本driveはcanonical cache
  へ一切書き込まない)。
