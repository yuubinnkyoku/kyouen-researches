# 11×11 次の8局面の探索前監査・実データ確認（2026-10-08）

## 対象と範囲

最新のmainを読み直し、前回修正した `requested_budget` 結合を、reply27二石root `{60,27}` の次候補 `(1297036692682702976,128)` の保存済み8局面に適用した。

- 対象: `research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-probe8-next.csv`、SHA-256 `63ac37a21488794f981d4f609c57488faea0e08871e6dd46c02fc0644bb6b61b`
- 保存済み探索計画: 同prefix `-manifest.json`、SHA-256 `b38554b7f3e228a8aa88365bf12d9a889d8f7fec73ab79972abb705cb82bd049`
- s5 cache: `post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-merged-s5.cache`、SHA-256 `eee8da7e463efbc7fabfae19bab34c54a8c5d8ef1b0485749f1634c0b5d31c94`、過去checkpointで4,847件
- 保存済みs6監査: 同prefix `-saved-s6-summary.json`、SHA-256 `0695e5fb2b9119e361fa8923bd10063fe1b617194fe86b423f6a1be525ca6e3a`
- 計算予算: s5局面ごと `15,000,000` nodes

CT202でmainを新規に取得し、`audit_s5_raw_history.py` を改修後のコードで実行して、`research/experiments` 以下の **1,075 CSVファイル**を再走査。8対象に対して既知exact 0、同予算以上UNKNOWN 0、結果の衝突0、`dispatch_ready=8`。保存raw監査自身に `requested_budget=15000000` を記録した。続いて、`verify_dual_tight_probe_preflight.py` と共通 `validate_audits` が8局面のkey集合、入力/cacheハッシュ、s6監査とbudgetを照合して **`DUAL_TIGHT_PROBE_PREFLIGHT_OK`** を返した。

## 重要な制限

元の全面的なraw-history監査は `research/experiments` の1,075 CSVに加えて **`.local/n11` の1,167 CSV**を調査した。しかし今回のCT202複製にはこの `.local/n11` が存在しない。したがって今回の新形式raw監査は**保存済みリポジトリ内の部分範囲のみ**であり、「過去すべての計算履歴を再走査した」という主張ではない。元の全面監査には当時、対象8件の過去exact/同予算UNKNOWNが0と記録されているが、その非永続ローカルファイルを今回独立再確認したわけではない。

この部分監査成功だけを根拠に重いsolverをdispatchしてはならない。実行直前に、元の全履歴に相当する保存・回収済み原始記録を揃えたうえで予算付きraw監査を再生成し、最新のexact cacheに対して再度s6監査・preflightを行うこと。旧予算欠落監査に後付けで値を入れない。

本回の追加コード変更はCIへの18件の監査回帰試験組込み。CT202の最新main作業木で18/18成功、Python構文検査成功、知識基盤33/33成功・362項目0エラー。新しいsolver実行、WIN/LOSS判定、s4 LOSS被覆増加はない。二石root `{60,27}` と標準11×11空盤は引き続き **UNKNOWN**。
