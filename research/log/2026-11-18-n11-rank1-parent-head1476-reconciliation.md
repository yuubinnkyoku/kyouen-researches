# 2026-11-18 n11 rank-1 partial-STERILE parent の head1476 再照合

## 背景

head-1410 の K0865 census では、S5 parent
`00000000000000801202000040000000` は partial-STERILE（残り5行、うちSTERILE 2行）だった。
同日公開した rank-1 receipt-channel audit は29/29 checks PASSだが、summaryの
`fold_pending_bands=[cost76c,cost76d,cost77e]` は、当時のsweep記録に残る「fold pending」
を検査した値であり、後から更新された現行claimの状態ではない。

現行mainでは、cost76d/77eとcost76cのreceipt foldが既に完了している。
古い監査結果は変更せず、head1476時点の状態を別の再照合として記録する。

## 独立再照合

`reconcile_rank1_parent_head1476_20261118.mjs` は、Node標準機能とBigIntだけを使い、
worklist-1410の6,438行から、5石parentのD4像が6石行に含まれる条件を直接再計算した。
得られた5行は、旧rank-1 auditおよびK0865 censusと完全一致した。

入力はGit blob SHAで固定し、K0863/K0865/K0868、head-1410 worklist、旧rank-1 audit、
cost76c/76d/77e claimsとfold、cost66i bit19 foldを照合した。
**47/47 checks PASS、別プロセスでの2回実行はbyte-identical**。

## 現在状態への更新

- head1410では5行・edge cost 364。STERILE 2行/135、非STERILE 3行/229。
- cost76d+77e fold（head1450→1452）は4 receipts（bits 19/49/37/69）を反映し、
  対象parentは3行/211になった。
- cost76c bit61 fold（head1472→1473）は1 receiptを反映し、対象parentは2行/135になった。
  cost76c bit99はfallbackのままで、抽出・fold済みreceiptには数えていない。
- cost66i bit19 fold（head1473→1476）はこのparentに影響しない。

したがってhead1476で残る行は、K0865のSTERILE refsと完全一致する次の2行だけである。

| S6行 | edge cost | 現在分類 |
|---|---:|---|
| `00000000000000801202000040000400` | 71 | STERILE |
| `00000000000000801282000040000000` | 64 | STERILE |
| **合計** | **135** | **2行** |

このparentは、head1410でのpartial-STERILEから、head1476では
**all-remaining-STERILE（D10 receipt体系に限る）**へ変わった。
現行headは `1476/174/6372/504389/4645/368303`。S5 parent自体は未閉鎖である。

K0863により、残る2つのSTERILE行は自出・cross-coverを問わずWIN7-D10 receipt rootで閉じられない。
よって、このparentをD10 receipt目的の探索候補として再投入しない。これはLOSS判定ではなく、
depth-10 receipt経路の閉鎖不能性だけを示す。bit99の他parentへのmarginalについても、この監査は主張しない。

## 公開物

- verifier: `reconcile_rank1_parent_head1476_20261118.mjs`（Git blob `77e9fa4a8013ba42adbebbbbe24cdeeb1b928d24`）
- result: `rank1-parent-head1476-reconciliation-20261118.json`
  （Git blob `6992f2dcc8b87a5409cff31c8a87134fc4283a6a`、
  SHA-256 `feb3b42f72064ffa4ff4e931d58643645b50ef04863826a23b7d969b978e8012`）
- audit source main before this reconciliation: `0c9881826a2e25bf665a19804ba5655f14aa932e`
- publication main after result: `cb7769314a260c91ed062486b600fa98ac689ea3`

この作業は既存receiptの再照合であり、新しい探索・verdict・証明書を生成していない。
旧rank-1 audit/logは歴史資料としてそのまま保持する。

## 解釈上の制限

STERILEもREFUTED-D10もLOSS証明ではない。対象S5 parentは未解決のまま。
標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべて
**UNKNOWN**。
