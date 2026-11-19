# resolve7 (residual 72-row post-fold witness recheck): single-owner declaration

- **担当レーン（単一オーナー）**: 2026-11-19T21:07Z 以降の長期レーン（K1071 seventeenth receipt fold を出版した同一レーン）。
- **目的**: 第17 receipt fold（K1071）で残余 74 → 72 行・39-root live witness 計画の当該 root が retire した後の状況を、**出版済み正本のみ**を使って厳密に再照合する。具体的には (1) 残余 72 行の出自（78 行計画から windfall4 fold の 4 行＋seventeenth fold の 2 行がちょうど除去され、残余 72 行と過不足なく一致すること）、(2) 39-root witness 割当表（39 root × 2 行 = 78 行の 1 回被覆）の retired root 除去後の 38 root × 割当の再照合（34 root × 2 行＋4 root × 1 行＝72 行）、(3) K1069 depth-10 全面掃引の判定（WIN 1 / REFUTED-D10 38）との交差で、残余 72 行の各行の割当 root がすべて REFUTED-D10 であり、**39-root 計画からの depth-10 witness 供給が残余 72 行に対してゼロになったこと**を確定する。
- **機械**: 新規スクリプト `resolve7_post_fold_witness_recheck.py`（不要な外部計算なし・repo から raw 取得した 5 正本を SHA-256 pin して読み込む）: resolve6 正本（SHA-256 `e85d4bfb…`・78 行 base_state／witness_full）、fold9 正本（`24db2352…`・windfall4 閉鎖 4 行）、fold10 正本（`bed7d331…`・閉鎖 3 行・残余 72 行・retire）、K1069 掃引正本（39 root 分類）、seventeenth 38 gate 正本（`c1073bae…`・coverage claim 2 行）。
- **並走への依頼**: 他の n11 レーンは resolve7（残余 72 行の post-fold witness 再照合）を重複実行しないこと（K1067/K1068 二重出版事故の再発防止）。resolve6.py の universe 再構築を要する fresh-safe pool のフル再照合（候補供給の本格探索）は本ノートの管轄外であり、着手する場合は別の単一オーナー宣言を先行すること。
- **管轄の限界**: 本ノートは正本ベースの再照合の単一オーナー宣言にすぎない。候補プールの再構築・新しい証明書の抽出は含まない。fold・被覆は行の簿記であり閉じた行のゲーム理論的値を主張しない。
- 解釈規約は不変: REFUTED-D10 は LOSS 証明ではない。pn/dn・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
