---
id: K1140
title: 残余29行のWIN8-D10 receipt fold root 438000000818（fold24）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold24 WIN8 receipt fold root 438000000818
  - K1136証明書の五親S6 frontierへのfoldと残余29→26行
  - 第31 receipt・第14 WIN8 receipt fold
relations:
  - type: depends_on
    target: K1136
    note: root 00000000000000043800000008180010のWIN8-D10証明書（34,843戦略行・1,260,393 bytes・SHA-256 dbcb0bae…）と19/19 gate監査正本（SHA-256 d0653834…）。K1091掃引pin・runner v17 blob pin・独立第三方法を含む。
  - type: depends_on
    target: K1133
    note: fold23正本（残余29行baseline・SHA-256 04f334ff…）と出版機（SHA-256 c908f6c0…）をpristine隔離再実行してから接続した。
  - type: depends_on
    target: K1097
    note: WIN16 intrinsic footprintの主張3行とreceipt対象の一致、およびfold後に残る候補数・主張行数の照合。
artifacts:
  - path: research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/README.md
    role: source
    note: 入力pin・fold結果・独立監査・再現手順・解釈上の制限
  - path: research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/scripts/reconstruct_inputs.py
    role: source
    note: 固定Git参照から12 blob・49 SHA-256 pinの入力を再構成
  - path: research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/scripts/build_fold24.py
    role: generator
    note: fold23出版機からfold24機を生成。置換回数・古い定数・pin件数・構文を検査
  - path: research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/scripts/fold_win8_root438000000818.py
    role: verifier
    note: 61入力pin、fold23 pristine再実行、K1136 19 gate、K1097 27 gate、D4被覆とfrontier簿記を検査
  - path: research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/scripts/verify_fold24_independent.py
    role: verifier
    note: 別実装による46項目の独立検査
  - path: research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/output/win8-root438000000818-receipt-fold-20261120.json
    role: data
    note: fold24正本（SHA-256 c4ab76d3…・25,666 bytes）
  - path: research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/output/independent-audit.json
    role: verifier
    note: 独立監査正本（46/46 PASS・SHA-256 49f330c6…）
  - path: research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/output/reproduction.log
    role: data
    note: 追加再実行の全pin・frontier chain・証明書・receipt geometry検査ログ
  - path: research/log/2026-11-20-n11-fold24-win8-root438000000818-receipt-fold.md
    role: log
    note: 生成・再実行・独立監査・結果・初回環境障害の記録
  - path: research/log/2026-11-20-n11-fold24-win8-root438000000818-single-owner-note.md
    role: log
    note: fold24の単一オーナー宣言と先行試行の環境障害記録
---

# 残余29行のWIN8-D10 receipt fold root 438000000818（fold24）

## 対象と範囲

K1136の8石root `00000000000000043800000008180010` のWIN8-D10証明書を、五親S6 frontier receipt chainの第31 receiptとして適用した。K1133のfold23正本を直前入力とする。

## 結果

- 主張3行を閉鎖し、5親targetは83/112行から86/112行へ。残余は29行から**26行**へ減少。
- 閉鎖edge costは225。余分な行の閉鎖は0。
- S6 manifest記録数は1,722→1,725、残存S6行数は6,126→6,123、残存costは485,438→485,213。
- 親行incidenceは11,666→11,660（4親、全てclass 2、計6減）。
- 残存S5 orbit数は173のまま。K1097 WIN16候補は2根・主張3行。

## 検証

fold機械は12 Git blob pinと49 SHA-256 pinを検査し、fold23出版機のpristine隔離再実行を含む上流chainを再計算した。生成器から再生成したfold24機は既存機とbyte-identical。5回のfold実行ログもbyte-identicalである。

別実装のPython監査器は、D4座標変換・4×4行列式の置換展開・親行対応・cost・frontier差分を再導出し、46/46 checks PASS。receipt正本と独立監査正本は実験README記載のSHA-256に固定した。

## 限界

foldは行の閉鎖簿記であり、閉じたS6行のゲーム理論的値を主張しない。WIN8-D10は当該8石rootのゲーム木だけを証明する。solved S6の件数も簿記値であって勝敗数ではない。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4はすべてUNKNOWN。
