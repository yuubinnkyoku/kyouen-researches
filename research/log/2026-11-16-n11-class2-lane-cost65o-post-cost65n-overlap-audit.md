# 2026-11-16：cost-65o行とcost-65nの2 WIN receiptのD4交差監査 — 65候補中の重複0・新規転送0・59 open維持

開始時main: `23480542c21a08bdb4e1756a0226a90586c94f73`。cost-65nはhead 1441の最安行を59候補完走し、bit 90/117から2件のWIN7-D10証明書を出版済み。cost-65oは同じS5親の次点行として別レーンがclaim v1を所有し、構造検証8/8 PASS、59候補のsweepは重複禁止のため着手しない。

## 独立交差監査

K0863の位置レベル補題を使い、cost-65oの各合法候補root `child | (1<<bit)` を11×11 D4の8変換で正準化し、cost-65nの2つのWIN7-D10 receipt rootの正準形と照合した。候補集合はclaim v1の公開bit列を固定し、cost-65nのreceipt root/coversはfold前に公開されたpreregistrationから固定した。行列式探索やゲーム木探索は実行していない。

- cost-65o legal candidates: **65**
- 既存REFUTED-D10転送: **6**
- open候補: **59**
- cost-65o候補rootのD4軌道: **65/65 distinct**
- cost-65n WIN receipt root canons:
  - bit 90: `00000000000100003800000048002000`
  - bit 117: `00000000001020003800000008080000`
- 2 receipt rootとcost-65oの全65候補rootの交差: **0**
- 既存6 REFUTED-D10転送とのWIN/REFUTED衝突: **0**
- 59 open候補への新規WIN転送: **0**
- cost-65o child自体はpreregistrationのcovered S6 row 13軌道に含まれない（raw references 14件中、D4軌道13）。

したがって、**cost-65nの2 receiptだけではcost-65o行もその候補もcoverされない**。cost-65n foldがpreregisteredどおり着地しても、cost-65o claimの候補表はこの2 receiptを理由に変更する必要がなく、59 openのままである。これは「他のreceiptも含めて最新main上でopen」と断言するものではない。後続のreceiptが追加された場合は再度全件照合する。

## 再現性・入力固定

- 監査コードは標準ライブラリのみ。候補bit列・転送root canons・2 receipt roots/coversをコード内に固定し、claimが後日v2へ更新されても監査対象の入力が変わらない。
- 入力blob pins:
  - cost-65n completed claim v2: `257e7093582f9080a551ec4ef42e1bdccee3c878`
  - cost-65o claim v1: `18c49eb010e0f464f5b7874c5ffbfb0ae34b67bb`
  - cost-65o claim structural verification 8/8: `cfff0b8087a54f3b4d327d73737f220372f34248`
  - cost-65n fold preregistration: `da2b2292a3a3436f73dc04bae266de2c01a6ef21`
  - K0863: `6b79dbcb2db0b8c34c108c1c227be139a3f1493b`
- 出力JSONには全65候補のroot/canon/status、receiptのcovered rows、全検査を保存する。

## 解釈境界

これはreceipt被覆の構造監査であり、sweep verdict・証明書・manifest headを変更しない。WIN7-D10証明書は個別7石rootの先手勝利をdepth 10以内で示すだけ。REFUTED-D10はLOSS証明ではない。cost-65o sweepは別レーンのclaim所有を尊重して未実行。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべてUNKNOWN。

## 成果物

- [監査コード](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost65o_post_cost65n_receipt_overlap_20261116.py)
- [監査JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65o-post-cost65n-overlap-audit-20261116.json)
- 根拠定理: [K0863](../knowledge/items/K0863-sterile-row-depth10-unclosability.md)
