# 2026-11-18: p=3251 全量DRAT監査完了の記録と K0708 昇格ドラフト

作業: W45 (omp)。作業場所: `~/workspace/kyouen-omp/full` (full clone)。

## 結論（先に要旨）

- p=3251 の全量 DRAT 監査（残り 1,541 d、drat-trim）は **2026-11-18 12:07 JST (03:07 UTC) に ALL DONE**。
  最終的に **VERIFIED 1,541件、SAT 0件、UNKNOWN 0件**。先行監査済みサンプル 84件
  （修正版増分チェッカー、別実装）と合わせて **1,625 全 d が監査済み**。
- チェーン ALL DONE 時点で **d=781 のみ per-d 領収書が 0 バイト**（VM再起動で書き込み途中に死んだ。
  progress.log の VERIFIED 行は 1,540行）。2026-11-18 に `--ds 781 --recheck` で修復し、
  再solveが同一の `proof_gz_sha256` (9b00b701…) を再現、領収書と drat-trim.log が正常再生成。
  最終状態: progress.log 1,541行 VERIFIED、集約JSON 1,541レコード全 VERIFIED、`unknown.json` は存在しない。
- ただし集約側の d=781 レコードが「チェーン完了時点で既に存在した」は進捗記録からは直接確認できない
  （後述、§2 の注意参照）。修復後の集約レコードは recheck 実行のものと一致する。
- **K0708 の昇格条件のうち (1) 1,541件 VERIFIED・重複なし (2) 84+1,541=1,625 全被覆
  (3) unknown.json 空 は満たされた**。(4) knowledge 側チェック（check.py / unittest / build.py /
  generated diff ゼロ）は統合時に行う。ドラフトは §3・§4。

## §2 証拠（実ファイル照合、2026-11-18 時点）

すべて `research/experiments/parabola-p2207-no-equality-witness-20261107/output/` 直下と
`p3251-drat-full/` の実ファイルから照合した数値のみを記載する。

- `p3251-drat-full/progress.log`: 全 3,122 行。`VERIFIED` を含む行 **1,541**、`SAT` 0、`UNKNOWN` 0。
  チェーン完了は `2026-11-18T03:07:10+0000 driver done`、直後のサマリ行
  `2026-11-18T03:07:44+0000 p=3251 h=1625 edges=1379766 requested=1541 todo=0 budgets=[5000000, 20000000, 100000000] wall_budget=2400.0`
  → 03:07 UTC = 12:07 JST に ALL DONE。
- 集約JSON `drat_trim_audit_full_3251_92f0aa9575ed519d.json`（drat-trim 側）: **1,541 レコード**、
  d は **1,541 件ともユニーク（重複なし）**、verdict は全レコード `VERIFIED`。
- 先行サンプル側 `drat_audit_full_3251_34249932790a9e9d.json`（修正版増分チェッカー）: 84 レコード
  （d ユニーク 84）。84 + 1,541 = **1,625 全 d 被覆**。
- `unknown.json` は `output/`・`p3251-drat-full/` いずれにも存在しない（`ls` で確認、不存在）。

### d=781 の穴と `--ds 781 --recheck` による修復

- progress.log 上、`2026-11-17T23:54:25+0000` の d=781 開始行の直後に d=781 の verdict 行がなく
  （次の verdict は `00:09:37 d=796`）、d=781 の verdict は recheck 実行の
  `2026-11-18T03:16:41+0000 verdict=VERIFIED solver=cadical-native lines=341542 solve=2.67s check=2.88s`
  が最初。すなわちチェーン ALL DONE 時点では d=781 は VERIFIED 1,540 行の穴だった
  （VM再起動で書き込み途中に死んだper-d領収書 0 バイト）。
- 修復: 03:16:25 の `p=3251 h=1625 requested=1 todo=1` 行に続く recheck 実行で
  d=781 を再solve・再検証。`p3251-drat-full/d781/receipt.json` の
  `proof_gz_sha256` は **`9b00b70148bfd7db4daf3aab7923382452e19d10eb700855a50a6162a738d7a3`** で
  同一proofを再現。集約JSON `drat_trim_audit_full_3251_92f0aa9575ed519d.json` の d=781 レコードも
  同じ `proof_gz_sha256` かつ `verdict: VERIFIED` で receipt と完全一致。
- 修復後の最終状態: progress.log 1,541 行 VERIFIED・SAT 0・UNKNOWN 0。

### 注意

- 「集約JSONの d=781 レコードがチェーン完了時点（03:07 UTC）で既に存在した」かどうかは
  進捗記録（progress.log）からは直接確認できない。progress.log の d=781 verdict 行は recheck 実行の
  03:16 のみであり、03:07 時点の集約JSONのスナップショットは保存していないため。
  修復後の集約レコードは recheck 実行のものと一致する。

## §3 K0708 昇格ドラフト（needs-review → computed）

対象: `research/knowledge/items/K0708-p3251-no-parabola-equality-witness.md`

1. **status**: `needs-review` → `computed`
2. **新しい artifacts** の追記:
   - `research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_trim_audit_full_3251_92f0aa9575ed519d.json`
     (data): drat-trim による残り 1,541 d 全量監査の受理記録（全 VERIFIED・重複なし）
   - `research/experiments/parabola-p2207-no-equality-witness-20261107/output/p3251-drat-full/progress.log`
     (source): 全量監査の進捗記録と d=781 recheck 修復の記録
   - `research/log/2026-11-18-p3251-audit-completion-knowledge-omp.md`（本ログ, source）
3. **等価命題の証拠を新 K 項目ドラフト（§4, 仮番号 K0872）に移し、K0708 からは depends_on / supports relation で参照**する。
4. **evidence の更新**（現行値「全数監査は未完了」を置き換える）:

   > 全 1,625 d のDRAT検証が完了（2026-11-18）。うち84 dは修正版増分チェッカー
   > （`drat_audit_full_3251_34249932790a9e9d.json`）、残り1,541 dはdrat-trim
   > （`drat_trim_audit_full_3251_92f0aa9575ed519d.json`）でVERIFIED・SAT 0・UNKNOWN 0・unknown.json 不存在。
   > d=781のper-d領収書はVM再起動で0バイトになったが `--ds 781 --recheck` で同一proof
   > （`proof_gz_sha256` 9b00b701…）を再現し修復済み。詳細は K0872。

5. **「全数監査未完了のためstatusは `needs-review`」の限界記述の削除**（§「限界」冒頭の該当文）

### 昇格条件の充足状況

- (1) **1,541 件 VERIFIED・重複なし**: 満たされた（集約JSON 1,541 レコード、d ユニーク 1,541、全 VERIFIED）。
- (2) **84 + 1,541 = 1,625 全被覆**: 満たされた（サンプル 84 + 全量 1,541 = 1,625 d、h=1625 と一致）。
- (3) **unknown.json 空**: 満たされた（ファイル自体が存在しない）。
- (4) **knowledge 側チェック**（`uv run --locked python tools/knowledge/check.py`、
  `uv run --locked python -m unittest discover -s tools/knowledge/tests`、
  `uv run --locked python tools/knowledge/build.py`、
  `git diff --exit-code -- README.md research/knowledge/generated`）:
  **統合時に行う**（本作業はドラフト作成まで。K 番号の衝突解消（§4 の仮番号 K0872 を含む）と
  generated の再生成は統合時の `tools/knowledge/build.py` で実施）。

## §4 新 K 項目ドラフト（仮番号: K0872）

W44 が K0871 を取ったため本ドラフトの仮番号は **K0872** とする。
統合時に main 上で衝突があれば付け直す（その場合、本ログ内の参照も更新する）。

```markdown
---
id: K0872
title: p=3251の全量DRAT監査が完了（drat-trim残り1541 d + 修正版サンプル84 d = 全1625 d）
kind: observation
status: needs-review
topics: [maximum-safe, verification, search-methods]
aliases: []
relations:
- type: supports
  target: K0708
  note: 全数量化の残余1,541 dの監査証拠。K0708のdrat-trim全量監査を補完し昇格を可能にする
- type: depends_on
  target: K0334
  note: 等号 ⟺ あるdについてCNFが充足可能。したがって全1625 dのUNSAT証明で等号を否定
- type: depends_on
  target: K0707
  note: 修正版DRAT検証器の削除時代入失効の修正（本観測は修正版で実施）
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_trim_audit_full_3251_92f0aa9575ed519d.json
  role: data
  note: drat-trimによる残り1,541 d全量の受理記録（全VERIFIED・d重複なし）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/p3251-drat-full/progress.log
  role: source
  note: 全量監査の進捗記録とd=781 recheck修復の一次記録
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_3251_34249932790a9e9d.json
  role: data
  note: 先行監査済みサンプル84件（修正版増分チェッカー、別実装）
- path: research/log/2026-11-18-p3251-audit-completion-knowledge-omp.md
  role: source
  note: 監査完了記録とK0708昇格ドラフト
scope: 奇素数p=3251のDRAT監査の被覆。drat-trimの健全性の一般証明を含まない。
evidence: progress.log 1,541行VERIFIED（SAT 0・UNKNOWN 0）と集約JSON 1,541レコード全VERIFIEDが一致。先行サンプル84件と合わせ1,625全d被覆。unknown.json不存在。d=781の0バイト領収書はrecheckで同一proof_gz_sha256 (9b00b701…)を再現し修復。
---

## 観測内容

p=3251（h=1625）の全量DRAT監査が2026-11-18 12:07 JST (03:07 UTC)にALL DONEした。

1. 先行監査済みサンプル84 d（修正版増分チェッカー、checkerソースSHA-256
   `34249932790a9e9d…`、別実装）。
2. 残り1,541 dをdrat-trim（checkerバイナリSHA-256 `92f0aa9575ed519d…`）で監査し、
   **VERIFIED 1,541・SAT 0・UNKNOWN 0**（`drat_trim_audit_full_3251_92f0aa9575ed519d.json`、
   dは1,541件ともユニーク）。合わせて**1,625 全 d 被覆**。

## 品質記録と注意

- チェーンALL DONE時点でd=781のper-d領収書のみ0バイトだった（VM再起動で書き込み途中に中断）。
  2026-11-18に`--ds 781 --recheck`で再solveを実施し、同一の`proof_gz_sha256`
  （9b00b701…）を再現、領収書とdrat-trim.logが正常再生成、progress.logも1,541行VERIFIEDとなった。
- 集約JSONのd=781レコードが「チェーン完了時点で既に存在した」ことは進捗記録からは直接確認できない。
  修復後の集約レコードはrecheck実行のものと一致する。
- 本観測はdrat-trimの一般健全性の証明ではない。また`A(3251)`の正確な値は未確定のまま。
```

（完）
