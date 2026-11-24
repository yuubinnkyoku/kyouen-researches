# z0-front-h1-proof-20261124 — K1282 専用機体（宣言ノート 89a8b438 の protocol 実行用・公式実行の前に凍結）

z0 面の確定パッケージ K1282（H1 全称証明 ⟹ T-B0 無条件昇格・LAW-C 定理化・
δ3-high-gap / δ4-C4 / クラスII / クラスE 定理）の機械検証キット。

## 構成

- `verify_k1282.py` — 公式 verifier（sha256
  `7b70993aea68e80ef27dd4f059727427ea048c0e40015bd240f3841abc44354f`）。
  engine block は出版 K1138 pin（`bd5f22e4…`）を埋め込み・起動時 sha assert。
  電池 D1–D10・宣言総計 42,725 比較 bad 0 期待・fail-closed (rc1)。
  tamper: `--tamper-engine` (rc2)、`--tamper=h1|q|lawc|lawc-arm2|l3|e|ii` (rc1)。
  stdout は決定的（揮発情報は stderr のみ）。
- `engine_block.py` — K1138 出版 block と byte 一致（pin と同一 sha）。
- `exploration/census1.py` / `census1.out` — 宣言前探査①: 法則断片 census
  6,239 点 bad 0（H1/L3/C4/E/A2/II/Q/Qallm + 行1基底 R4/L3(1)/H1(1)）。
  2026-11-24 再実行の記録。
- `exploration/explore_ladder.py` / `explore_ladder.out` — 宣言前探査②:
  δ-ladder 生値表（m=2..4・k=1..8・1,236 行）。(2,3)@k3=1・(2,3,3)@k3=0・
  (2,4)@k4=0・(2,4,4)@k4=1 など、宣言ノート §2.5 の open 登録
  （C-II2・allm-δk・pure-count ladder）の根拠観測。
- `output/dryrun*.json` / `output/dryrun-note.txt` — honest dryrun 記録
  （後述）。

## dryrun 記録（honest・全段階を公開）

1. **dry0 (記録なし・fail)**: ENGINE_SHA pin 定数の転写 typo
   （`…c9b79829bc…` ← 正 `…c9b798296bc…`）により sha gate が
   AssertionError で正しく fail。pin 修正。sha gate が改変を検出する
   ことの実証にもなった。
2. **dryrun1**: D9 β3z1 の期待値誤り（β3c: min>=2 multi @3 z1 → 0 は
   既刊 K1269 側の分類なのに、コードが「max>=2 なら一律 2」と誤期待）。
   bad 1,087 を机器が正しく検出（fail-closed rc1）。床分類を F4 の
   とおり修正。
3. **dryrun2**: singles-v-ord の照合タプル構築バグ（`(x,)[:1]+(x,)` =
   `(x,x)` を single として検査していた）。bad 601 を検出（rc1）。
   `(x,)` に修正。
4. **dryrun3**: 全 green・42,725 点 bad 0・stdout sha256
   `b2600e453a2a78e0a92e47f7591d79379dd074a3f5c19a86538d6afc9a8f85c8`
   ＝ 宣言ノート §3 の想定と一致。PYTHONHASHSEED preach variation
   （1 / 99）でも stdout byte 一致を確認。

## 公式実行 protocol（宣言ノート §4 どおり）

1. 同一 cwd で 2 走（PYTHONHASHSEED=random, PYTHONHASHSEED=1）
2. 隔離 tree + `env -i` で 2 走（PYTHONHASHSEED=random, 99）
3. 4 走の stdout byte 一致確認（sha256 b2600e45… 想定）
4. 変異電池 8 種の rc と bad を記録（engine→rc2、他7種→rc1）
5. すべての stdout/stderr を `output/audit_run{i}.json` / `run{i}.info`
   として出版・MANIFEST-sha256 を作成。

publish-then-execute: この kit は宣言ノート出版後に変更なく凍結する。
