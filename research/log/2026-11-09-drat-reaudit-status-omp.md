# 2026-11-09 p=2207 / p=3251 の修正版DRAT再監査 確定状態（OMP監査）

作業はファイル読み取りと集計のみ。検証器・ソルバ・監査ドライバは起動していない。
数値はcommit済みレシートJSONの集計であり、DRATの再生結果ではない。

## 結論

| p | 修正版VERIFIED / 全d | 計画標本 | 全数か | 残り |
|---|---:|---|---|---|
| 2207 | **12 / 1103** | 旧21点標本のうち **12/21** | いいえ | 標本9点、全数では1091 d |
| 3251 | **84 / 1625** | `d=1,26,...,1601` の **65/65 完了** | いいえ | 1541 d（標本は完了） |

両項とも status は `needs-review` のままで正しい。p=2647 の全数監査（1323/1323、K0706）と
K0101 `refuted` はこの作業で変更しない。

## 根拠（レシート実体）

checkout HEAD は `a0fcb1fb1957fdf8b6dd55be0edb791b982f330e`（2026-11-09 06:20 +0900）。
以下のレシートはHEADにcommit済みで、作業ツリーの変更ではない。

### p=2207

- ファイル: `research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_2207_34249932790a9e9d.json`
- SHA-256: `46bd7387407a8bf4605f370357a42ebd1c7f55aace858cb4496218e07ecc5689`
- ヘッダ: `p=2207`, `h=1103`, `checker_source_sha256=34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b`（K0707修正版）
- レコード 12 件、d は重複なし:
  `1, 50, 100, 150, 200, 250, 289, 297, 300, 312, 324, 400`
- 全件 `solver=UNSAT`、`checker_rc=0`、`checker_out=VERIFIED`、`verified=true`。
- 証明 16〜522,426 行、検査 1.0〜1,356.8 秒/件、合計 7,950 秒。
- 12 件はすべて旧21点標本の先頭12点。旧標本の残りは
  `500, 550, 600, 700, 800, 900, 1000, 1100, 1103` の9点。
- 全数被覆は 12/1103。旧検証器の21点記録（`output/drat_audit_full.json`）は
  K0707により独立証拠に数えない（本項の12件には加えていない）。

### p=3251

- ファイル: `research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_3251_34249932790a9e9d.json`
- SHA-256: `2c48c67eb19ed9e39812c6b675654cd3fc0f51a8e935a344f348ba9c34c09188`
- ヘッダ: `p=3251`, `h=1625`, 同じ修正版ソースSHA-256。
- レコード 84 件、d は重複なし。内訳は計画標本 `d=1,26,51,...,1601`（25間隔、65点）の
  **65点すべて** ＋ 再監査開始時の `d=2..20`（19点）。
- 全件 `solver=UNSAT`、`checker_rc=0`、`checker_out=VERIFIED`、`verified=true`。
- 証明 29〜219,183 行、検査 0.1〜849.2 秒/件、合計 28,038 秒。
- 全数被覆は 84/1625。標本65/65の完了は
  `research/log/2026-11-09-audit-strategy-stratified-samples.md` の
  「2026-11-09 04:4x p=3251 の層化標本が完了」（逐次監査 `audit_sequential.py`、残り24件）とも一致する。

### 停止理由

- p=2207: 記録されている停止は、multiprocessingプールが待ち合わせで停止した事象
  （`audit-strategy-stratified-samples.md` 03:4x、当時5件）。以後は逐次方式へ移行し、
  レシートは12件まで増えた。d=400 の次（旧標本ではd=500）以降を止めた理由・エラーは
  レシートにもlogにも記録がない。最後のレコードは `verified=true` で失敗記録はない。
  したがって「プール停止→逐次で再開→d=400まで到達後にプロセスが終了」までは確認できるが、
  終了の明示的な原因は未記録である（セッション終了と推定。logには根拠なし）。
- p=3251: 標本は完了済み。全数監査を止めているのは失敗ではなく方針
  （`2026-11-09-audit-strategy-stratified-samples.md`: K0101はp=2647で既に反証済みのため、
  2531/3251の全数監査は必須でなく、層化標本で独立検証範囲を広げる）。

## 引き継ぎサマリとの差分

`research/log/2026-11-09-parabola-equality-handoff-summary.md`（作成時点）と現在のSSOT/レシート:

| 対象 | 引き継ぎサマリ / K項目の記述 | 現在のレシート（HEAD） |
|---|---|---|
| p=2207 | 「修正版で再検証中（5件）」、K0693も `d={1,50,100,200,300}` の5件・1098 d未被覆 | **12/1103**、未被覆1091 d、標本12/21 |
| p=3251 | 「層化標本50件（継続中）」 | 標本**65/65完了**、総レコード84/1625 |
| p=3251 (K0708) | 「70 d、計画標本51/65、未被覆標本 `1276,1301,...,1601` の14件」 | 84 d、標本65/65、未被覆標本0 |
| p=2531 | 層化標本143件（完了） | レシート143件で一致（変更なし） |
| p=2647 | 1323/1323 | レシート1323件で一致（変更なし） |

差分の原因:

- K0693/K0708 が引用する `commit: 87e28af...` は 2026-11-09 04:10 +0900 の固定snapshotで、
  そこでは実際に 2207=5件、3251=70件（標本51/65）だった（`git show 87e28af:<receipt>` で確認）。
- その後 HEAD `a0fcb1f`（06:20）のレシートが 12件／84件へ追記されたが、
  K0693/K0708 の本文・artifact note・`parabola-audit-coverage-20261109/inventory.json`
  （入力commit 87e28af固定）は更新されていない。
- `inventory.json` が記録する2207レシートSHA-256 `bf49a281...` は現在の `46bd7387...` と異なる。
  これは固定snapshot時点の値であり、現在の被覆件数として引用してはいけない。
- したがって「K項目の件数」と「HEADのレシート件数」は一致しない。現在値は本logの表を使い、
  K項目の是正は別作業（本タスクはlog1件のみ作成）とする。

## 残作業と再開コマンド

作業ディレクトリは `research/experiments/parabola-p2207-no-equality-witness-20261107`。
両ドライバは同一検証器ソースSHA-256のレシートから既処理dをスキップする（再開可能）。

p=2207 の旧標本の残り9点（優先）:

```sh
g++ -O2 -std=c++17 drat_check_incremental.cpp -o drat_inc
uv run --locked --with python-sat python audit_sequential.py --p 2207 \
  --ds 500,550,600,700,800,900,1000,1100,1103
```

p=2207 の全数（残り1091 d、長時間）:

```sh
uv run --locked --with python-sat python audit_all_d.py --p 2207 --from-d 1 --to-d 1103 --workers 12
```

p=3251 は標本完了。全数を追加する場合のみ（残り1541 d、任意）:

```sh
uv run --locked --with python-sat python audit_all_d.py --p 3251 --from-d 1 --to-d 1625 --workers 12
```

注意:

- `audit_all_d.py` はプール待ちで停止した前例がある。1件ずつ確実に進めるなら
  `audit_sequential.py --ds <カンマ区切り>` を使う（3251の残り24件はこの方式で完走）。
- 両ドライバの衝突予算は既定 5,000,000。旧走査の200,000とは異なる。
- p=3251 の全数監査は現在の結論（K0101反証済み・K0708は4例目候補）に必須ではない。

## checkoutの制約（sparse）

- 本checkoutで欠けている引用ファイル:
  `research/experiments/parabola-equality-extension-2143-2500-20261107/output/deep_scan_3251.json`、
  同 `deep_scan_2531.json`。K0702/K0708 が引用する全数走査の生データであり、
  本logでは未読・未検証。件数はK項目の記述をそのまま引用していない（DRAT件数には無関係）。
- 存在を確認したファイル: 上記2レシート、`p2207_d_verdicts.json`、
  `audit_all_d.py`、`audit_sequential.py`、`parabola-audit-coverage-20261109/inventory.json`。
- `inventory.json` はcommit 87e28af固定のsnapshotで、再生成していない。
- 本checkoutの `git log` はshallowで1コミットのみ。87e28af/b52faa1のオブジェクトは参照可能。
