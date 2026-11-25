# 11×11 reply27 — 欠落s5 replayの局面単位での保存証拠照合（2026-10-08）

## 確認範囲

直近の保存済み8対象用全履歴監査（2,242 CSV）には、現在の作業木に存在しない `.local/n11` の1,167 CSVが記録されている。このうち827 CSVの `s5_replay_rows` は0、340 CSVは各1行（合計340行）。これらの元ファイルを復元したわけではない。

`scripts/audit_missing_s5_replay_redundancy.py` を追加し、古いファイル名から抽出できる5石D4 canonical key 340件を全件安全性・重複検査した後、`research/experiments/` に現存する1,075 CSV／s5 replay 3,173行と、SHA-256 `eee8da7e463efbc7fabfae19bab34c54a8c5d8ef1b0485749f1634c0b5d31c94` の4,847件 exact cacheを突き合わせた。

| 対象 | 局面数 |
|---|---:|
| 欠落元CSVに記録されたs5行のcanonical key | 340（全て相異なる合法5石） |
| 別の公開済みraw CSVに**同じkey**のreplayが現存 | **340** |
| そのうち保存済みraw CSV上のexact判定あり | 329（WIN 20 / LOSS 309） |
| 保存済みraw CSV上のUNKNOWNのみ | 11 |
| 現行exact cacheに登録済み | 332 |
| 保存済みrawではUNKNOWNのみだが別経路でcache exact登録済み | 3 |
| 現行cacheに無く、rawでは15M予算UNKNOWNのまま | **8** |
| 保存済みraw exactとcacheの相反する判定 | **0** |
| 対応する公開済みraw CSVが全くないs5 key | **0** |

8個のcache未登録局面はすべて15,000,000節点のUNKNOWN記録を持つ。対応sourceのパス・行番号・SHA-256と局面番号は
[hash付き監査receipt](../experiments/n11-boundary-recovery-20261006/output/post-bd547ab0-vanished-s5-key-evidence-receipt-20261008.json)
に保存した。JavaScriptの53ビット浮動小数点整数化で局面番号が丸められないよう**文字列の十進数**で保存し、各値が実CSVの列と完全一致する回帰試験を追加した。

全340件のsource対応・hash付き詳細を生成したJSONのSHA-256は
`b34c385b5062a539b0c158e4d108de19658223f5582489a3d2f11c6b537d2be0`。
標準ライブラリと既存幾何検証コードで以下を再実行すると詳細JSONを再生成できる。

```sh
python research/experiments/n11-boundary-recovery-20261006/scripts/audit_missing_s5_replay_redundancy.py \
  --historical-audit research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692682702976-128-probe8-next-raw-history-audit.json \
  --saved-raw-root research/experiments \
  --exact-cache research/experiments/n11-boundary-recovery-20261006/output/post-951a5619-rank1-1297036692683882496-0-probe8-next-collected-merged-s5.cache \
  --out /tmp/n11-missing-s5-replay-redundancy.json
```

## 重要な証拠上の境界

この結果は**局面単位での観測記録の冗長性**を示すだけである。欠落した `.local/n11` 元ファイル1,167件の**バイト列や当時の各出力行が現存保存行と同一であることは証明していない**。したがって `verify_raw_history_coverage.py` による**source完全性FAILは継続**し、現行preflightの探索許可条件は緩めていない。また保存rawのWIN/LOSSは既存solver出力であり、独立したsolverで再解決したものではない。UNKNOWNをWIN/LOSSに昇格させていない。

回帰試験は新規12件（source消失、予算不足、conflict、非正規key、64ビット保存等）、既存履歴coverage16件、既存preflight18件の **46/46成功**。知識整合性検査は366 items、errors0/warnings0。CIに新規テストを追加。mainに直接反映しbranch/PRなし。

11×11の二石root `{60,27}` と空盤は引き続き **UNKNOWN**。新規exact cache・s4 LOSS・secured coverageの増分はない。
