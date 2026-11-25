# fold10 (seventeenth WIN7 receipt fold): single-owner declaration

- **担当レーン（単一オーナー）**: 2026-11-19T21:00Z 開始の長期レーン（K1069 の単一オーナー掃引 と連続稼働の同一レーン）。
- **目的**: 第17 WIN7-D10 証明書（root `00004000000000821082000000000100`・証明書 SHA-256 `21dd2f0e…7c8`・38 gate 正本 `n11-residual78-seventeenth-win7-cert-extract-20261120`）を第17 receipt として fold し、残余 74 行のうち被覆 2 行（`00000000000000821082000000000001`・`00000000000000821082000000000004`・幾何再導出で gate 確認する）を閉じる receipt-fold 正本（fold10）を publish する。成立すれば残余 74 → 72 行・frontier 6,209/491,722 → 6,207。
- **機械**: fold9（thirteenth-sixteenth）の fold 機械 `n11-windfall4-receipt-fold-thirteenth-sixteenth-20261120/fold/fold_thirteenth_sixteenth.py` の pin 差し替え版（fold9 正本 SHA-256 `24db2352…`・seventeenth 38 gate 正本 SHA-256 `c1073bae…`・証明書 SHA-256 `21dd2f0e…` を入力に追加）。チェーン再構築（base 6,259/495,507 → … → post-ninth-twelfth 6,213/492,021）は windfall4 版と同一の pinned 入力から再現する。
- **並走への依頼**: 他の n11 レーンは fold10（seventeenth receipt fold）を重複実行しないこと（K1067/K1068 二重出版事故の再発防止）。並走は seventeenth 実験名の item 化・README 弾丸など fold 以外の作業を継続してよい。fold10 を越える次の receipt は未登録の証明書が出た場合のみ。
- **管轄の限界**: 本ノートは fold10 の単一オーナー宣言にすぎず、証明書・掃引の正本の座は既存の出版済み実験のままである。
- 解釈規約は不変: REFUTED-D10 は LOSS 証明ではない。fold は行の閉鎖簿記である。標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
