# Part DU-b: batch-34 WIN 2行の第三実装交叉検証 (2026-11-24)

- 事前登録宣言: `research/log/2026-11-24-part-du-b-b34win-thirdimpl-declaration.md` (commit `7141772d`)
- 対象: Part DU (batch-34 small-pockets) で出版された WIN 2行
  - `ag001`: key (1152921505747697664, 1032), legal 85, 幾何class 23101, published df-pn replica rows `15000000,1,9149084` (p1/p2 node-exact)
  - `ag002`: key (1153485622925590528, 0), legal 88, 幾何class 1849, published df-pn replica rows `15000000,1,4893014` (p1/p2 node-exact)
- 本Partは計算再現性と三実装 (published df-pn replica + this-host replica + third implementation) のverdict一致のみを検証する。**verdictを消費しない**。cache には書かない。勝敗・閉鎖・被覆・secured・root勝敗の主張は一切行わない。

## 構成

| dir | 内容 |
| --- | --- |
| `input/` | runner入力 7ファイル (rows.json + 対象2 + anchors k02a/l1a + negatives ng1/ng2) |
| `sources/` | 出版済み証拠pins: raw 2x2, anchors/negatives input 4, batch-keys-b34.json, du-batch34宣言 (B1-fixでbyte-exact修正済み), read-only canonical cache `973bcd19…` (6,547 s5verdict行), status-b34.log |
| `scripts/` | third_impl.js (第三実装, pin `08ea958f…`), jsreplay.js, runbatch.sh, run_thirdimpl.sh, run_valgate_dv.sh, make_inputs_dv.py, audit_dv.py, verify_tbl.js, verify_tbl_b34.js, tamper_battery_dv.sh (汎用化修正版, pin `0445e56f…`) |
| `output/` | status.log, replica raw 4, third-impl targets 4 (a/b det-pair), anchors 4, negatives 2, rules-gate.txt, audit-run1/2/3.txt (byte-identical), audit-summary.json + run変種 6, tamper-battery.txt, T2-buggy記録, machinery-synthetic-audit-run.txt |
| `val-gate/` | hosted gates 8ファイル (4 gate keys x {dv-host.out, input.csv, published-baseline.out}) |

## 主要結果

- **D2 val-gate fresh 4/4 node-exact**: at2m×2 (budget 2,000,000, result 0, nodes 2,000,000) ・first-15m (budget 15,000,000, result 2, nodes 3,651,923) ・second-15m (budget 15,000,000, result 2, nodes 5,040,200)。全てpublished baselineとreplay行全字段一致。
- **D3 pinned-replica 2-pass node-exact (両WIN行)**: `ag001` `15000000,1,9149084` (p1 47s / p2 46s), `ag002` `15000000,1,4893014` (p1 24s / p2 24s)。runbatch.sh の WIN-HALT (rc=45) は宣言どおりの挙動。P1-FAIL 2行 (output/raw 未作成時のlayout手順ミス) はstatus.logに記録のとおりで、結果欄には影響しない。
- **D4 第三実装 (byte-clone pin `08ea958f…`) 全て事前登録どおり**: targets **third = replica = 1 (WIN) verdict一致 2/2** — `ag001` expansions 10,728,035 / ttHits 5,758,042 (30.56s / 30.80s), `ag002` expansions 5,646,148 / ttHits 3,187,475 (16.69s / 16.57s)。a/b deterministic pair 完全一致。anchorsはpublished値を完全再現 (k02a: result=1, 9,106,337 / 4,991,527; l1a: result=2, 7,660,602 / 3,951,175)。negatives ng1/ng2 は期待どおりの `GATE_FAIL` でfail-closed (行byte一致)。rules gate (verify_tbl_b34.js): quads 95,670 / 95,670, triples 195,044 mismatches 0。
- **D5 fail-closed audit (audit_dv.py) × 3回**: rc=0, stdout byte-identical (sha256 `29b948a2…` x3), **ALL 117 GATES PASS**, verdict agreements 2/2 (WIN), inconclusive 0, targets pass-one expansions 合計 16,374,183。
- **D6 tamper battery**: 10/10 pre-registered変異を事前登録どおりのgateで検出 (rc=1) + control ALL-PASS (rc=0)。
- **D7 outputs出版・fetch-back 31/31 byte-identical** (HEAD `f1187f4f` 時点)。

## Honest deviations (プロトコルに基づく記録)

1. kit push はpayload・memory上限のため5分割コミットとなった (`c4edaa78` 1/3, `d045195d` 2/3 scripts, 3/3a sources an/bk, 3/3b canonical cache, 3/3c sources残り, 3/3d val-gate)。うち1回はK-lane由来のnon-fast-forward (`1d75b371`) に遭遇したが、最新main再取得後に再pushで解消した。
2. `sources/du-batch34-declaration.md` の初回pushでASCII簡易デコーダ由来のmojibakeが発生した。fetch-back byte検証で検出し、直ちにB1-fixとしてbyte-exact修正pushを行った (`c12f3ed9` 時点で39/39 byte-identical確認)。
3. tamper battery T2は合成kit用のplaceholder定数 (7777000) が実kitにマッチせず初回UNEXPECTED (rc=0) となった。CV buggy-grep先例に準拠し汎用increment変異に修正 (script sha `0445e56f…` をB2コミットで再出版)。buggy実行は `output/tamper-battery-t2-buggy-record.txt` にverbatim保存した。検証ツール自体は両実行とも全変異を検出した。

## 検証

`MANIFEST-sha256.txt` はkit 39 + results 30 の全69データファイル (sha256, bytes, git-blob-sha1) を列挙する。全エントリをGitHub main 側のtree (size / git-blob-sha1) と2026-11-24に相互照合した。`README.md` と `MANIFEST-sha256.txt` 自身はlistingから除外 (self-exclusion)。

## UNKNOWN担保 (不変)

標準11×11空盤、19 central-reply roots、二石roots {49,60}/{59,60}、S2 {59,60}、class 1/2/4、class 10968、class 23964、class 2251 (54キー全部)、class 34269、class 23101・class 1849 (本2キーを含む)、その他すべてのキーは**常にUNKNOWN**である。nodes数・expansions数・ttHits数・wall秒数を勝敗として読むことは決してない。本Partはbatch-34のWIN 2行のverdictを消費しない (honest label = 採用候補にすぎず、採用は別途宣言されるadoption Partがscrutiny owner C++ gate `9193f5b6…` 経由でのみ行う)。第三実装一致は採用ではない。閉鎖・被覆・securedCoverage・root勝敗の主張は行わない。
