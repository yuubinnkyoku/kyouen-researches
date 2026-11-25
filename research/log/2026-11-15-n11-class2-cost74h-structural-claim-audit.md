# 2026-11-15：cost-74h claimの独立構造監査（sweep前）

監査基準main: `105657faacc05350d16ba0abf6fe79d445e6868b`。最新の `AGENTS.md`、`research/knowledge/README.md`、K0783、cost-74h claim、merged head 1270、S6 manifest 6分割を確認した。branch / PR は作成しない。

## 対象

cost-74h claimのS6 child:

`00000000000000889002000000000800`

石bitは `[11,49,60,63,67,71]`。merged canonical headは `1270/6577/519427/4847/383150`。

## 独立再計算

repoのsolver・verdict cache・候補列挙器を呼ばず、別のBigInt実装でBareiss 4×4行列式とD4 8変換を再計算した。

- S6自体は15個の四点部分集合すべてで行列式が非零。安全性を確認。
- 空き121点から合法なS7追加点を全列挙し、**74候補**を得た。bit列はclaimの74件と完全一致。
- childはS6 manifestに一度だけ存在し、`cost=74, classes=2`。
- 6個の一石削除から得るS5親D4軌道は6個すべて異なる。
- 現在の正しいmerged-head ranking（`class-frontier-s5-ranking-after-merged-cost65l-74g-20261115.csv`）に存在する親はちょうど2個で、claimと一致:
  - bit 11: `00000000000000801222000000000000` — class 2、75軌道 / 5,705
  - bit 67: `00000000000000801202000000200000` — class 2、17軌道 / 1,325
- 残る4親軌道はrankingに存在せず、head 1270では閉鎖済み。
- よって、このchildが運ぶ未充足需要は `c1=0,c2=2,c4=0`。

注意: `class-frontier-s5-ranking-after-unified-merge-20261115.csv` は古い1154 headの表である。これを1270 headと取り違えると、第二親の行数・費用が誤って見える。今回の監査はmerged-cost65l-74g版を使用した。

## claim衝突の確認

main上のcost-74 claim群も照合した。cost-74h childは他のcost-74 claimのchildと異なる。一方、古いcost-74e claimと完了済みcost-74g claimは同じchild `00000000000000809142000000000000` を指す。74gの完了記録では74eを古い計画として扱っているため、74eを新しい作業として再開しない。今回その歴史的claim自体は変更していない。

## 信頼境界

これは**探索前の構造監査**であり、v16 depth-10 sweepは実行していない。17行すべての再構成や「全既存claimを除いた最安未探索行」であることの再証明も、この監査の範囲外。WIN/LOSS、証明書、receipt foldは一切増えていない。cost-74h claimは引き続きIN FLIGHT。

計算は同じ整数監査ロジックをV8実行環境で動かしたもの。保存したNode.js再現スクリプトは追加したが、この実行ではrepository checkout内でのNode実行はまだ行っていない。

Proxmoxも確認したが、共有サービスを使わずに投入できる専用研究実行機は確認できなかった。停止中のVM124はGPU・音声機器の直結設定を持つNixOS AIOで、研究用と確認できないため起動していない。共有LXCにも探索を投入していない。

## 成果物

- 検査器: [audit_cost74h_claim_independent_20261115.mjs](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost74h_claim_independent_20261115.mjs)
- 結果: [cost74h-claim-independent-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/cost74h-claim-independent-audit-20261115.json)

再実行: `node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost74h_claim_independent_20261115.mjs`

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1・2・4の勝敗はすべて引き続き **UNKNOWN**。K0783の勝敗・fold状態は変えていない。
