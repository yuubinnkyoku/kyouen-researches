# Part EG: closure class 34908 b33-win-6 残 unconsumed WIN 6行の第三実装交叉検証

- 実験dir: `research/experiments/n11-centralreply-closure-b33win6-thirdimpl-20261125/` (本dir)
- 宣言log: `research/log/2026-11-25-part-eg-b33win6-thirdimpl-declaration.md` (commit `2a46008a`)
- 完了log: `research/log/2026-11-25-part-eg-b33win6-thirdimpl-completion.md`
- scaffold (kit) 出版: commits `2a46008a → 5e7217c4 → 58750d83 → a9b5fd1d → cf74b547 → 403d8fd5 → 156f8a6f → bb661fbb` (53 files)
- outputs 出版: commit `7484f63df63a0267fe7a5bf3b71a168c609cb455` (35 files)
- ハッシュ一覧: `MANIFEST-sha256.txt` (kit 53 は `bb661fbb` 固定・outputs 35 は `7484f63d` 固定・`sha256sum -c` 互換)

## 対象

closure class 34908 のうち Part EE wave F reaudit closure table で確定した残6つの
unconsumed probe-level WIN行 (af029 / af047 / af050 / af053 @15M batch-33,
af023 / af048 @30M Part EA reprobe)。第三実装 `scripts/third_impl.js`
(非df-pn AND/OR minimax) による verdict 交叉検証と、pinned-replica 2-pass fresh-cold の
node-exact 再現を検証する。**adoption は行わない (verdict不消費)。**

## 結果 (E1-E9 の要点)

- E1 rules gate: `verify_tbl_eg.js` — quads 95,670/95,670, triples 195,044, mismatches 0 (`output/rules-gate.txt`)
- E2 val-gate fresh 4本: published baseline と node-exact (2M×2 + 15M×2)
- E3 negatives: ng1 (legal 88 vs derived 87) / ng2 (stones 6 vs bits 5) とも GATE_FAIL fail-closed 捕捉 (rc=1)
- E4 anchors: k02a exp=9,106,337 ttH=4,991,527 / l1a exp=7,660,602 ttH=3,951,175 (a/b det-pair 一致)
- E5 replica 6キー×2-pass + af029-30m 2-pass: 全て published raw と node-exact
  (af029=4,862,485 は15M/30M両条件、af047=9,841,975, af050=7,311,834, af053=5,182,129,
  af048=17,816,616@30M, af023=28,933,179@30M)
- E6 third-impl 6キー×2 run: a/b det-pair 一致・全キー WIN (third=replica=published=1)
  expansions: af029=5,672,478 / af047=11,706,195 / af050=8,719,439 / af053=6,071,614 /
  af048=21,512,908 / af023=34,912,368 (pass-one total 88,595,002)
- E7 audit ×3: ALL **213 gates PASS**・3回 byte-identical
  (`output/audit-summary.json` sha256 `73af060a4c139818e0e4625ed511945394169afca6ad704eec8c4c6b4bcfc7bf`)
- E8 tamper battery 5/5 捕捉 (t1 input改竄・t2 rows-pin・t3b replica nodes+1・t4 targets verdict flip・t5 replica result flip)
  + pristine 再実行 green (wall_s 系は設計どおり非検出)
- E9 出版: outputs 35 (`7484f63d`) + 本README + `MANIFEST-sha256.txt` + 完了log

## verdict 不消費・UNKNOWN 担保

- 対象6行は honest unconsumed probe-level WIN label のまま。adoption は
  scrutiny owner C++ 第二実装 gate `9193f5b6…` 通過後・pinned merger `90711961…` 経由の
  別 adoption Part 専権 (g++ がないため本レーンでは C++ gate 未実施)。
- **標準11×11空盤・19 central-reply roots・二石root・S2・class 1/2/4/30345/34908 は
  本実験の前後を通じてすべて UNKNOWN のまま。** nodes/expansions/ttHits を勝敗や距離として
  読まないこと。

## 独立検証 (independent verification)

1. 固定 commit の raw URL で kit (`bb661fbb`) と outputs (`7484f63d`) を取得する
   (例: `https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/<sha>/<path>`)。
2. `sha256sum -c MANIFEST-sha256.txt` で全 88 ファイルの sha256 を検証する。
3. `python3 scripts/audit_eg.py` で 213 gates を再実行する (ALL PASS・byte-identical 期待)。
4. `node scripts/verify_tbl_eg.js` で rules gate を再実行する。
5. `scripts/run_replica_eg.sh` / `scripts/run_thirdimpl.sh` は同 budget map で再現実行可能
   (af023/af048 の 15M 再実行は禁止: published verdict は 30M WIN)。

## 既知の注意点 (誠実記録)

- 宣言log (2a46008a) の `make_kit_eg.py` pin は `c2f4f88b…` (旧ローカル変異)。
  出版 byte は `faee079a62fd28926c9686dada93f03da0b746cf2c40657ade915f2213e2f5c3`。
  fail-closed maker 再実行 G1-G7 ALL PASS + rows.json byte-exact 再生成で機能同等性を確認済み。
  詳細は完了log参照。
- `output/audit-summary.run1-3.json` は `audit-summary.json` と byte-identical のため
  main には published しない (出版は 1 ファイル・3回実行の事実は status/完了logに記録)。
- af023 の replica pass 実行は bash 300s 制限のため pass 分割とし、status.log 行を
  runner 形式で追記した (詳細は完了log)。
