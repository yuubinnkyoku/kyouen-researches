# 2026-11-15 n11 cost77a/b/c receipt audit and cost77d pre-sweep verification

監査時点のmainは `5a08dbb442905c1f4d313982fbc8113ee7719dd4`（cost77d claim公開直後）。統合時のmainは `e789146b192395729a282adf679a00c9113e8990`。`AGENTS.md`、`research/knowledge/README.md`、K0023、K0783、milestone-5実験README、cost77a/b/cのfold log・head JSON、cost77d claimを確認した。branch / PRは作成しない。

## 完了済みcost77a/b/c receiptの独立照合

- 77a/b/cの15 receipt rootsをBigInt D4変換で正準化し、3 lane間にD4重複がないことを確認。
- cost77cの8 rootはすべて `child | (1 << bit)` と一致し、7石。各rootの35個の4点部分集合、計280件をBareiss整数行列式 `det[x,y,x^2+y^2,1]` で検査し、共線・共円なし。
- 8 rootの一石削除から得るS6親は49 D4軌道。receiptのmanifest marginal 4 hexはすべてこの親lift集合に含まれる。
- cost77c foldの1286→1290はsolved +4、remaining S6 -4、remaining cost -288、open-class need -4 / cost -288で一致。第二coverable class-2 S5は14行/1095から13行/1018へ減った。

## cost77dの探索開始前監査

対象child `00000000100000801202000000200000` の6石を再抽出し、15個の4点部分集合で安全性を確認。空き121点を全列挙し、追加後の7石局面について35部分集合ずつ正確なBareiss判定を行った。

- 合法候補は77個。claimの77個のbit一覧と完全一致。
- 77候補の追加後局面、計2,695個の4点部分集合を検査し、全件安全。
- childのD4安定化群は恒等変換のみ。従って盤面対称性による候補削減はできず、77候補は77軌道のまま。
- childはcost77a/b/cの3 childいずれともD4非同値。
- 6つのS5親のうち開いているのはbit21削除の `00000000000000003800400008000000`（class2・66行/5192）とbit92削除の `00000000000000801202000000200000`（class2・13行/1018）の2つ。残る4親はhead-1290 rankingに存在せず閉鎖済み。
- top-candidates CSVのcost77d行はcost77・需要 `c1=0,c2=2,c4=0` と一致。

cost77d claimは既存レーンのIN FLIGHTのまま保持。今回、探索は起動せず、重複ジョブも作っていない。

## 信頼境界

cost77cの8 WIN7証明書（362,362行・13,055,390 bytes・457 sub-roots）は既存lane logでBigInt/Bareissの二検証器8/8 PASSと記録されているが、本監査では証明書本体を再生していない。77a/b/cの15 roots相互のD4重複は検査したが、先行557 root全体との重複は再構成していない。cost77dについては候補の幾何と親構造だけであり、探索結果・勝敗はまだない。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。manifest solved数は被覆数であって勝敗値ではない。

## 再現と実行制約

```sh
node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost77a_77b_77c_d4_geometry_independent_20261115.mjs
```

監査計算は隔離JavaScript実行環境で実行し、全検査を通した。Nodeスクリプトは再現用に保存したが、GitHub checkoutは実行環境のDNS解決失敗で取得できず、repo checkout上でのNode実行、`uv sync --locked`、knowledge check、unittest、knowledge buildは未実施。K0783はcost77cまで更新済みであり、cost77dはまだIN FLIGHTなので今回変更せず、generated viewも変更していない。
