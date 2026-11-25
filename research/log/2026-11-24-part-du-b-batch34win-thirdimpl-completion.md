# Part DU-b 完了log (2026-11-24): batch-34 WIN 2行の第三実装交叉検証 (publish-then-execute) 完了 — verdict一致 2/2 (verdict不消費・11×11 UNKNOWN)

- 事前登録宣言: `research/log/2026-11-24-part-du-b-b34win-thirdimpl-declaration.md` (commit `7141772d`, observed HEAD-before-push `ca42291b`)。宣言前探査 (kit pins照合・maker 3×byte-identical・audit合成kit 117 gates×3・battery 10/10) を全開示したうえでsolver未実行のまま宣言した。
- 実験dir: `research/experiments/n11-centralreply-closure-b34win-thirdimpl-20261124/` (kit 39 + results 30 = データ69ファイル, README + MANIFEST-sha256別掲)。

## 出版連sha (publish-then-execute)

1) 宣言 `7141772d` → 2) kit 39ファイル (scaffold 5分割: `c4edaa78` 1/3, `d045195d` 2/3 scripts, 3/3a sources an/bk, 3/3b canonical cache, 3/3c sources残り, `adc6143a` 3/3d val-gate最終; fetch-back 39/39 byte-identical) → 3) B1 outputs → B2 outputs + battery修正script → B1-fix (mojibake修正, `c12f3ed9`時点 39/39確認) → D7 fetch-back 31/31 byte-identical (HEAD `f1187f4f`) → D8 README + MANIFEST-sha256 (commit `cf46dbfa`, fetch-back byte-identical: README 5,619 bytes git-blob `323d45d1…`, MANIFEST 10,388 bytes git-blob `3c15102f…`)。

## 実行・検証結果

- **D2 val-gate fresh 4/4 node-exact**: at2m×2 (2M, result 0, nodes 2,000,000) ・first-15m (15M, result 2, nodes 3,651,923) ・second-15m (15M, result 2, nodes 5,040,200)。published baselineとreplay行全字段一致。
- **D3 pinned-replica 2-pass node-exact (両WIN行)**: `ag001` `15000000,1,9149084` (47s/46s), `ag002` `15000000,1,4893014` (24s/24s)。runbatch.shのWIN-HALT (rc=45) は宣言どおり。P1-FAIL 2行 (output/raw未作成時のlayout手順ミス) はstatus.logに誠実記録され、結果欄に影響しない。
- **D4 第三実装** (`third_impl.js` pin `08ea958f…` byte-clone) 全て事前登録どおり: targets **third = replica = 1 (WIN) verdict一致 2/2** — `ag001` expansions 10,728,035 / ttHits 5,758,042 (30.56s/30.80s), `ag002` 5,646,148 / 3,187,475 (16.69s/16.57s)。a/b deterministic pair完全一致。anchors k02a (1, 9,106,337/4,991,527) ・l1a (2, 7,660,602/3,951,175) はpublished値を完全再現。negatives ng1/ng2は期待どおり`GATE_FAIL` (行byte一致)。rules gate (verify_tbl_b34.js): quads 95,670/95,670, triples 195,044 mismatches 0。
- **D5 fail-closed audit** (`audit_dv.py` pin `2cecf421…`) ×3回: rc=0, stdout byte-identical (sha256 `29b948a2…`×3), **ALL 117 GATES PASS**, verdict agreements 2/2 (WIN), inconclusive 0, targets pass-one expansions 合計 16,374,183。canonical cache `973bcd19…` (6,547 s5verdict行) unadopted gates: 両WIN行ともcacheに不在 (採用ゼロの機械保証)。
- **D6 tamper battery**: 10/10 pre-registered変異を事前登録gateで検出 (rc=1) + control ALL-PASS (rc=0)。実kit上でbattery scriptとして実行。
- **D7 outputs出版・fetch-back 31/31 byte-identical**。
- **D8 README + MANIFEST-sha256 出版**: MANIFEST 69エントリ (sha256・bytes・git-blob-sha1; READMEとMANIFEST自身はself-exclusion)。

## Honest deviations (3件・READMEにも記録)

1. kit pushはpayload・memory上限により5分割コミット。うち1回はK-lane競合によるnon-fast-forward (`1d75b371`) に遭遇したが、最新main再取得後に再pushで解消した。
2. `sources/du-batch34-declaration.md` の初回pushでASCII簡易デコーダ由来のmojibakeが発生。fetch-back byte検証で検出し、B1-fixとしてbyte-exact修正push (`c12f3ed9`時点で39/39 byte-identical確認)。
3. battery T2は合成kit用placeholder定数 (7777000) が実kitにマッチせず初回UNEXPECTED (rc=0)。CV buggy-grep先例に準拠し汎用increment変異に修正 (script sha `0445e56f…` をB2コミットで再出版)。buggy実行は `output/tamper-battery-t2-buggy-record.txt` にverbatim保存。検証ツール自体は両実行とも全変異を検出した。

## verdict不消費・採用の専権

本Partはbatch-34のWIN 2行 (class 23101・1849) のverdictを**消費しない**。honest label = 採用候補の記録にすぎず、WIN採用はscrutiny owner C++第二実装 gate `9193f5b6…` を通過した別adoption Part (pinned merger `90711961…` 専権) のみが行う。第三実装一致は採用ではない。closure表 rank 1 (class 23101) ・rank 2 (class 1849) は採用待ちのため本時点でもunknownのまま。C++ gateは本実行環境では実行不能 (コンパイラなし・パッケージ導入禁止) であり、Part DU宣言§4のとおりscrutiny ownerが専権を保持する。

## UNKNOWN担保

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 10968・class 23964・class 2251 (54キー全部)・class 34269・class 23101・class 1849・その他すべてのキーは本Partの実行・出版のどの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数・wall秒数を勝敗として読まない。閉鎖・被覆・securedCoverage・root勝敗の主張はしない。
