# 11×11 reply27: 過去のraw replay source完全性ゲート（2026-10-08）

## 背景

次の dual-tight s4 候補 `(1297036692682702976,128)` の探索8件を再開する際、raw-history監査の `requested_budget`、対象集合とcacheのハッシュだけでは、前回走査したCSVファイルが現時点で全件入っていることを保証しない。新作業木では過去の `.local/n11` が欠け、部分範囲だけを再走査した監査でも旧preflightは通過し得た。この失敗モードを修正する。

## 実装と独立入力照合

`research/experiments/n11-boundary-recovery-20261006/scripts/verify_raw_history_coverage.py` を新規作成。過去のraw-history source inventoryと新たな実測inventoryを比較する。

- 両者の完全な対象metadata、exact cacheのSHA-256、現在監査自身に保存された正の計算予算を検査する。過去の予算欠落auditを新しい `requested_budget` として再利用しない。
- `scanned_csv_sources` の全パス、サイズ、SHA-256、s5 replay行数を検査し、新しい現物ファイルのhashとサイズも独立に読み直す。
- CRLF→LFの場合のみ、現物のLFをメモリ内でCRLFへ戻したバイト列のhashが**過去のSHA-256と厳密一致**する場合に差を許容する。それ以外の内容変化は拒否する。
- 過去のファイルに欠落や内容不一致が1件でもあればFAILを返す。追加されたCSVは現在監査に含めて検査する。
- `verify_dual_tight_probe_preflight.py` に必須 `--historical-raw-audit` を追加し、coverage FAIL時は承認を生成しない。`prepare_dual_tight_probe.py` と `prepare_dual_tight_ready_subset_probe.py` にも同一の必須ゲートを追加し、候補CSV自体を出力しない。全入口で省略時にも拒否する。
- source集合を新規に監査するコードはあくまで入力の出典検査であり、履歴に保存されたsolver verdictそのものを再証明するわけではない。

## 保存済み実データによる負の統合試験

比較基準は `post-951a5619-rank1-1297036692682702976-128-probe8-next-raw-history-audit.json`（2,242 CSV）と、同rank-1の全95 UNKNOWN用 `post-951a5619-rank1-1297036692682702976-128-raw-history-audit.json`（2,241 CSV）。現在の作業木で改修済み `audit_s5_raw_history.py` を再実行し、各対象・同一cache・予算15Mで `research/experiments` の1,075 CSVを照合した。

- 過去の2,242件のうち現在1,075件。**欠落1,167件、そのうち340件にs5 replay行が各1件（340行）、827件はs5 replay行0件**。
- 現存1,075件のうち **314件がCRLF→LF正規化のみ**で旧SHA-256と厳密一致。その他の内容変化0件。
- 8対象用旧source全体との比較：`status=FAIL`、欠落1,167、s5 replay行340。改修済み `verify_dual_tight_probe_preflight.py` はexit code 1、承認ファイルなし。
- 全95対象のraw-history再監査：`cache_hits=0`、`prior_exact=0`、`same_budget_unknown=2`、`dispatch_ready=94`、`conflicts=0`（**repo内部分範囲**に限る）。
- 上記95対象、保存済みranking/cache/saved-s6監査と負の履歴完全性試験：通常版prepare、ready-subset版prepareはともにexit code 1、候補CSVなし。

## 回帰・研究状態

独立 `test_verify_raw_history_coverage.py` の16件（欠落、内容変更、同一hash、CRLF、改ざんmetadata、旧予算なし、経路逸脱、新規CSVと3入口の統合有無など）、既存 `test_audit_probe_preflight.py` の18件が実リポジトリで全成功。新規16件はCIに追加。変更scriptのcompileall成功、知識check **366 items、0 errors / 0 warnings**。mainへ直接反映しbranch/PRなし。

**出典の制約：** 欠落した1,167個の旧 `.local` の現物は今回回収できていない。過去raw auditのファイル一覧・行数は公開済み資料を参照しているが、欠落ファイル内の探索そのものの独立検査は未実施。重いsolverは起動していない。これらのsourceの復元、または独立監査できる別の厳密な証拠が揃うまでは候補をdispatchしないこと。

exact s5 cache 4,847（WIN120 / LOSS4,727）、secured 113/119、追加LOSS class最少3はいずれも**作業開始時の歴史的checkpoint**であり、今回新たに導出したものではない。二石root `{60,27}` と11×11空盤は **UNKNOWN**。
