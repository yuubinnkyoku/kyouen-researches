# 2026-11-17 n11 class2-lane cost73k concurrent-record consistency audit

## Source state

作業開始時の最新 main は `8803a3b01ef5932a246ead2f67f31b1438c768ac`。作業前に `AGENTS.md`、`research/knowledge/README.md)、K0023、K0863、K0865、K0868、およびcost73kのclaim・census v7・concurrent-session record・既存ログを再取得した。

- canonical claim: `class2-lane-cost73k-inflight-20261117.json`、Git blob `a24d3557ef23a279cc08c2d578e420f676f28f05`（commit `a0987c37`）
- census v7: Git blob `68246f3263fe6cbb49ffafa866f73b49cf3c2ebb`（commit `bdd394a9`）
- concurrent-session sweep record: Git blob `0cba988e2a65e9195b0a0e6a3168a518e27079fb`（commit `8803a3b0`）
- candidate convention K0868: Git blob `b097210d0b49d7cf014cc6a554298b1e49e83384`

同じS6 childをcensus v6 runner-upとして別sessionが先にclaimし、その約10分後にcensus v7 rank-1としてcanonical claimが上書きされた。先行sessionはv6の67 open + 6 confirmationで全73候補を探索済みだが、raw batchは公開せず、canonical v7 claimを変更しない方針で集計recordだけを保存している。

## Independent record-level checks

K0868のdet4展開を用い、既存 `legal_candidates.py` とは別のPython整数演算で6石配置から候補を再導出した。

- child: `00000000000000801206000000000400`
- 石bit: [10, 49, 50, 57, 60, 71]
- survival moves: **73**
- completing / blocked moves: **42**
- 全空セル115個を73 + 42に完全分割
- 73候補はcanonical v7 claimのlegal_candidatesとbit-exact一致し、公開concurrent recordのper_bit 73 keysともbit-exact一致

concurrent recordのper-bit表も再集計した。

- **25 WIN7-D10 / 48 REFUTED-D10 / 0 capped**
- per-bit node合計 **128,861,941** はrecordのcandidate_nodes_totalと完全一致
- total_nodes_including_pilotsとの差 **30,618 = 9 × 3,402**
- batch 1〜7は各9候補、batch 8は4候補、batch 9は6確認候補
- batch 7のnode合計は **24,968,847** でrecord記載値と一致
- v6の6確認bitはbatch 9と一致。v6ではopenだったbit 14はbatch 1で実行され、v7 overlayのWIN7-D10予測と一致

canonical v7 claimの7確認bit [14, 23, 26, 34, 53, 55, 107] は、claim transfer・census v7予測・concurrent recordのfresh outcomesがすべて一致（7/7）。v6の6確認bitも6/6一致した。

## Evidence boundary

この監査が独立に確認したのは、公開per-bit summaryの集合・件数・node総和・batch区分・claim/census整合、および候補幾何である。探索器そのものを再実行したものではない。

- raw batch bytes: 未公開（MD5一覧のみ）
- raw batch監査JSON: 未公開
- certificate manifest: 未公開
- batch determinismの主張: raw再実行データがないため独立再検証していない
- v15 cross-engine 25/25: concurrent recordに記録された集計値であり、個別raw記録は未取得

したがって、25 WIN7-D10は公開recordに記録された探索結果であり、今回の監査だけで証明書の正しさまで確認したわけではない。canonical v7 claimの `actual_execution.batches_run` は引き続き0、結果nullであり、claiming laneによるraw audit・claim更新・証明書抽出を待つ。

再現コマンド（claim更新後はcommit `a0987c37`からclaim v1を復元して渡す）:

```sh
python3 research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost73k_concurrent_record_20261117.py
```

## Interpretation guard

WIN7-D10は個々の7石rootに対する深さ10以内の先手勝ちだけを示す。REFUTED-D10はLOSS証明ではない。今回のrecord-level auditはmanifest行を一つも閉じない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はすべて **UNKNOWN**。
