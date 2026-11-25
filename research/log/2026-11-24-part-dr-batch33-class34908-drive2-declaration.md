# Part DR 宣言 (2026-11-24): batch-33 (closure class 34908) 残7キー af048..af054 継続probe (drive-2) — publish-then-execute

単一オーナー: n11中央応答レーン (長期レーン・本セッション本host)。
observed HEAD `24c75cddb` (2026-11-24T18:28:09Z・q=7 cap games lane)。
対抗宣言なし: commit message機械走査 (直近120件・2026-11-24) で
`Part DR` を主張するcommit・logは存在せず・batch-33 drive-2 liver・
af048..af054 の継続probeを主張する出版物は存在しない (「af04」言及は
Part DQ自身のinput packet出版 `f57f406f` のみ)。part文字「DR」は先着順
採用。Part DQ (drive-1) は完了済み (`d8d9de24`・WIN-HALT 到達)。

## 1. スコープ

Part DQ 宣言 (`c8388b719e`) で選定・出版済みの batch-33 54キーのうち、
drive-1 WIN-HALT (distinct WIN 2行 = af029/af047) 時点で未probeのまま
正規に残された **7キー af048..af054** を同一条件 (2-pass fresh-cold・
budget 15M・同一pinned runner/solver) で probe する (batch-33 drive-2)。

- 対象キー: af048 (s5 962172) / af049 (962233) / af050 (962386) /
  af051 (962410) / af052 (962450) / af053 (962470) / af054 (962471)。
  すべて Part DQ 出版 batch-keys.json `8a863381…` 内のキー (新規キー
  生成なし・maker不使用・input CSVは出版済みのまま不変)。
- **af048 の既存p1**: drive-1 wave 12 で p1 完走 (`af048.p1.out` 出版済み・
  `# replay_done` あり)・p2 truncated。pinned runner `f591f8c2…` の
  事前登録済み guard が完走p1をskipしてp2のみ実行する (設計どおり・
  probe の skip ではなく determinism 2-pass の後段のみの実行)。
- **verdict不消費**。probe結果 (WIN/LOSS/EXHAUSTED) は honest label の
  まま・canonical adoption は別adoption Part (pinned fail-closed merger
  `90711961…` 経由) のみ。閉鎖・被覆・secured・root勝敗の主張はしない。

## 2. 継続ゲート (宣言前に本hostで機械実施済み)

1. **status.log不変**: published status.log (47キー分・inc1..inc5 +
   完了出版 `d8d9de24`) は本宣言の時点で最新であり、af048..af054 に
   対する PASS/EXHAUSTED/WIN-HALT 行は存在しない (機械確認: remaining
   keys == af048..af054 の7キー)。
2. **drive-1のWIN-HALT数の除外**: status.log は append-only で drive-1 の
   af029/af047 WIN-HALT 行を含むため、drive-2 のwave-halt判定は
   **drive-2鍵集合 (af048..af054) のみに制限**する (下記script delta)。
   機械dry-run: drive-2 windistinct at entry = 0。
3. **kit再利用 (byte不変)**: runner `runbatch.sh` `f591f8c2…`・solver
   `jsreplay.js` `84585617…`・input CSV 54 + batch-keys `8a863381…` は
   Part DQ 出版物から fetch-back byte検証済み (171ファイル MANIFEST
   `24c75cdd` 時点で差分0)。val-gate 4/4 node-exact 出版済み
   (`90732788`・同一host・同一solver条件下で再実行不要)。

## 3. kit delta (drive-2 script・最小delta規約)

- `scripts/drive2_local_step_b33.sh` sha256
  `ca5fcdd0e236751a5d346226f7327525efa52cc99a81805aee7ad21c1377d506`:
  published drive-1 `ef44a49e…` からのfork。**機能deltaはWIN計数
  regex 2箇所のみ** (`af[0-9]{3}` → `af0(?:4[89]|5[0-4])`・理由は§2-2)。
  done-set regex (PASS|EXHAUSTED / WIN-HALT const w) は不変
  (機械diff確認: コメント行を除く機能差は前述2 regexとprint文言のみ)。
  stop rules・worker設計 (2 worker上限・inner timeout 260・
  TRUNCATED-RETRY・ALL-DONE empty-key guard) は drive-1 と同一。
- 事前登録 stop rules (pinned runner `f591f8c2` 変更なし):
  WIN rc=45 / MISMATCH rc=42・wave-halt = **drive-2鍵集合内で distinct
  WIN 2行観測時** (残キーは fileless UNPROBED 維持)・EXHAUSTED (result 0)
  は honest UNKNOWN でwave継続 (same-condition再probeなし)・p1/p2 fail
  rc=43/44。
- 進捗のincrement出版 (reset耐性) は drive-1 と同様に各波後に実施
  (truncated passは再実行後に出版)。

## 4. 期待機械簿記 (事前登録)

7キーのprobe結果は batch-33 の af048..af054 行を UNPROBED から
(LOSS/EXHAUSTED/WIN いずれかの) honest label に置き換える。本宣言は
結果非予告であり、いかなる勝敗も宣言しない。WIN が2行出れば drive-2
wave halt で残キーを UNPROBED 維持、それ未満なら 7キー全て完了し
batch-33 は「54キー中 UNPROBED 0」(~EXHAUSTED 除く) に到達する。
いずれの場合も closure table membership 変動 (flips/newly_free) の
導出は probe 完了後の別 reaudit による (本Partでは deriveしない)。
nodes数は bookkeeping であり勝敗ではない。

## 5. UNKNOWN担保 (Part DQ §5の再掲・不変)

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2
{59,60}・class 1/2/4・class 8730 / 5804 / 34269・class 34908 (54キー
WIN/LOSS/EXHAUSTED行を含む) は本Partの実行・出版のどの時点でも
UNKNOWN**。nodes数・wall秒数を勝敗や距離として読まない。WIN採用は
scrutiny owner C++第二実装 gate (`9193f5b6…`) 通過後の別adoption Part
(pinned merger `90711961…` 経由) のみ。EXHAUSTED行 (af003/af023/af034/
af039・および本drive-2で生じ得る新規EXHAUSTED) の高budget再probeは
別宣言条件を要する。

## 6. 不接触 (Part DQ §6の再掲)

Part DH takeover lane・K-series fast lanes (K1300超の先行使用がある
場合そのまま)・parity/q-series検証lane・Part DP canonical merged chain
(6,502行 `1ded9a08…`・read-only不変)・batch 1..33 各published dir
(不変)・BASE caches・WIN行scrutiny・EXHAUSTED高budget再probe・19root
計画・closure pocket (rank 1..4) WIN採用 (いずれも専権者のまま)。
