---
id: K1142
title: 残余26行のWIN8-D10 receipt fold root 200003800200（fold25）
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - fold25 WIN8 receipt fold root 200003800200
  - K1137証明書の五親S6 frontierへのfoldと残余26→24行
  - 第32 receipt・第15 WIN8 receipt fold
relations:
  - type: depends_on
    target: K1137
    note: root 00000000000200003800200008180000のWIN8-D10証明書（19,525戦略行・706,180 bytes・SHA-256 7bd64a47…）と19/19 gate監査正本（SHA-256 dafa177b…）。K1086掃引pin・runner v17 blob pin・独立第三方法・g19のfold23残余29内open検証を含む。
  - type: depends_on
    target: K1140
    note: fold24正本（残余26行baseline・SHA-256 c4ab76d3…）と出版機（SHA-256 f462733d…）をpristine隔離再実行してから接続した。
artifacts:
  - path: research/experiments/n11-residual26-win8-receipt-fold-root200003800200-20261120/README.md
    role: source
    note: 入力pin・fold結果・独立監査・再現手順・解釈上の制限
  - path: research/experiments/n11-residual26-win8-receipt-fold-root200003800200-20261120/scripts/reconstruct_inputs.py
    role: source
    note: 固定Git参照（60e5109efad…）から12 blob・fold25系SHA-256 pinの入力を再構成
  - path: research/experiments/n11-residual26-win8-receipt-fold-root200003800200-20261120/scripts/build_fold25.py
    role: source
    note: fold24出版機からfold25機を生成。置換アンカー・古い定数・pin件数（PINS=12・PIN256=51）・構文を検査
  - path: research/experiments/n11-residual26-win8-receipt-fold-root200003800200-20261120/scripts/fold_win8_root200003800200.py
    role: verifier
    note: 63入力pin、fold24 pristine再実行、K1137 19 gate、K1097 27 gate、D4被覆とfrontier簿記を検査
  - path: research/experiments/n11-residual26-win8-receipt-fold-root200003800200-20261120/scripts/verify_fold25_independent.py
    role: verifier
    note: 別実装による49項目の独立検査（余剰行のwin16 footprint不属検査を含む）
  - path: research/experiments/n11-residual26-win8-receipt-fold-root200003800200-20261120/output/win8-root200003800200-receipt-fold-20261120.json
    role: data
    note: fold25正本（SHA-256 5780f387…）
  - path: research/experiments/n11-residual26-win8-receipt-fold-root200003800200-20261120/output/independent-audit.json
    role: verifier
    note: 独立監査正本（49/49 PASS・SHA-256 7747afdc…）
  - path: research/experiments/n11-residual26-win8-receipt-fold-root200003800200-20261120/output/reproduction.log
    role: data
    note: 追加再実行の全pin・frontier chain・証明書・receipt geometry検査ログ
  - path: research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/README.md
    role: source
    note: WIN16 intrinsic footprintと残余候補計画の前提
  - path: research/experiments/n11-residual72-safe8-refuted50-refsolve-20261120/output/safe8-refuted50-refsolve-20261120.json
    role: data
    note: fold25が照合するWIN16 intrinsic footprint・候補計画の正本
  - path: research/log/2026-11-20-n11-fold25-win8-root00000000000200003800200008180000-receipt-fold.md
    role: log
    note: 生成・再実行・独立監査・余剰行hex訂正・frontier_after base障害の記録
  - path: research/log/2026-11-20-n11-fold25-win8-root00000000000200003800200008180000-single-owner-note.md
    role: log
    note: fold25の単一オーナー宣言と着手権確保の記録
---

# 残余26行のWIN8-D10 receipt fold root 200003800200（fold25）

## 対象と範囲

K1137の8石root `00000000000200003800200008180000` のWIN8-D10証明書を、五親S6 frontier receipt chainの第32 receiptとして適用した。K1140のfold24正本を直前入力とする。

## 結果

- 主張2行を閉鎖し、5親targetは86/112行から88/112行へ。残余は26行から**24行**へ減少。
- 同一rootのC(8,6)部分幾何に内在するtarget外open 1行（`0000000000000080120a000000008000`・cost 72）を併閉し、`extra_s6_rows_not_in_target`へ分離記録。target簿記は主張2行のみで進行。
- 閉鎖edge costは216（79+65+72）。
- S6 manifest記録数は1,725→1,728、残存S6行数は6,123→6,120、残存costは485,213→484,997。
- 親行incidenceは11,660→11,654（4親、すべてclass 2、計6減・7→6・7→6・54→52・38→36）。
- 残存S5 orbit数は173のまま。K1097 WIN16候補は1根・主張1行。

## 検証

fold機械は12 Git blob pinと51 SHA-256 pinを検査し、fold24出版機のpristine隔離再実行（fold23〜18連鎖込み）を含む上流chainを再計算した。生成器から再生成したfold25機は既存機とbyte-identical。3回のfold実行ログと固定Git参照からのend-to-end再現もすべてbyte-identicalである。

別実装のPython監査器は、D4座標変換・4×4行列式の置換展開・余剰行のwin16 intrinsic footprint不属・親行対応・cost・frontier差分を再導出し、49/49 checks PASS。receipt正本と独立監査正本は実験README記載のSHA-256に固定した。

## 限界

foldは行の閉鎖簿記であり、閉じたS6行のゲーム理論的値を主張しない。WIN8-D10は当該8石rootのゲーム木だけを証明する。solved S6の件数も簿記値であって勝敗数ではない。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4はすべてUNKNOWN。
