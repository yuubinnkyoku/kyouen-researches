# 2026-11-15 class2-lane: warm multiband batch-2 lane takeover crosscheck (frontier 1109 → 1140)

Long-term lane session (2026-11-15 JST). Session前半の成果の記録。この
セッションの後半は環境リセットを挟み、並走レーンのmerged 1148と
unified fold reconciliation specの実行（chain head **1154**）へ続く
（後者の詳細は
[unified merge log](2026-11-15-n11-class2-unified-merge-recompute-1154.md)）。

## batch-2 warm multiband 31証明書の出版

- warm batch-2のWIN7証明書 **31件**をmainへ出版
  （[class2-lane-warm-multiband2-certificates-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-warm-multiband2-certificates-20261115.json)
  + 証明書本文）。first_pushed_byはthis-lane 18 / concurrent-batch2-lane 13。
- **54/54 remote entry byte-exact**: GitHub dir listingのgit blob sha1と
  ローカル生成bytesを全件照合。分割push（part境界）の再結合が行境界で
  厳密に一致し、連結md5が単一ファイル生成と一致。
- WIN/LOSS conflict **0件**（batch2とmanifest既存のLOSS掃引との整合）。
- recompute
  [recompute_frontier_warm_multiband2_20261115.py](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_warm_multiband2_20261115.py):
  1109基準に31 receiptを公開順でfoldし **frontier 1140/6707/528979/4977/392702**。
  第三class-2 coverableターゲット S5 `00000000000000809102000000000000` は
  13軌道・937 → **12軌道・871**。

## chain breakの独立発見と修理（batch-2出版の副産物）

並走のmerged_after61f_63a65e chainで、cost-65eのin-place拡張に伴う
chain breakを独立に発見・修理した: cost65e bit-107のみがfold時に
marginalを持ち、bit-7は既知のcross-child重複（bit-7 root ==
manifest内既存root、md5一致）としてassertで確認される。この修理は
後に並走レーンの68d recompute（1117）と同一の着地を与え、双方の
独立実装が一致したことの傍証となった。

## outstanding（当時）

- cost-70c warm batch-2: bit-105が未検証のまま残り、その後の調査で
  残り5件（bits 92/40/24/11/8）も含め6件すべてがcost-70c child
  `00000000000000803242000000000000` のWIN7-D10 bits 105/92/40/24/11/8
  であることが判明 → 独立検証の上、unified merge（1154）でfold。
- （追記）この31 receipt群は並走レーンのmerged 1148 recomputeにも
  foldされ、unified fold reconciliation（correction_20261115_b）で
  50 receipt体系に統合された。

## push技術メモ（他レーンの運用にも有益）

- push_files完了後にMemoryLimitErrorが出ても着地は完了している場合が
  ある。 SHA照合で着地を確認してから再pushすること（盲目的再pushは
  重複commitを生む）。
- 手でSHAを転写するとcopy missする。dir listingを機械的に取得して
  照合すること。

## 勝敗に関する明記

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 2、
class 4はすべてUNKNOWNのままである。** solved数（1,140当時、現chain
head 1,154）はmanifest被覆の帳簿上の前進であり、勝敗・距離を意味しない。
