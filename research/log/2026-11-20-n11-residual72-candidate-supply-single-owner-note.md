# n11 残余72行 候補供給フル再照合（full cache join rebuild）: single-owner declaration

並走 resolve7 単一オーナー宣言（`research/log/2026-11-20-n11-resolve7-single-owner-note.md`）が「resolve6.py の universe 再構築を要する fresh-safe pool のフル再照合（候補供給の本格探索）は本ノートの管轄外であり、着手する場合は別の単一オーナー宣言を先行すること」と明記したため、当該宣言を先行する。

- **担当レーン（単一オーナー）**: 2026-11-19T21:12Z 台に開始した長期レーン（本実行）。
- **目的**: fold10（K1071）後の残余72行について、resolve6 正本機械と同じ fail-closed 手法で
  (1) K0863 cache corpus（1,279 file manifest・7 file は main 上不在の既知差分）から engine verdict map を再構築し、
  resolve6 正本（SHA-256 `e85d4bfb…`）との byte-identical 再現を third-environment で gate する。
  (2) 残余78行→72行の出自（windfall4 4 行＋seventeenth 3 行閉鎖の幾何再導出含む）を gate した上で、
  残余72行の add-one-stone universe を再構築し、full cache join（engine + transfers + post-K0863 sweeps + receipts 1〜17 + sweep39_live WIN 1/REFUTED 38）で judged/fresh を分類する。
  (3) corpus/sweep 由来の judged WIN で残余72行を被覆し未だ receipt 化されていない root（第18証明書候補・windfall 型）を raw provenance（pilot_d6 制御行・loss=true uncapped andclose・terminalStoneRange）つきで列挙する。
  (4) corpus judged を除いた fresh-safe live pool と pair 構造を候補供給データとして出版する（次の witness 計画選定のための材料。計画自体の掃引着手は別途宣言する）。
- **機械**: `resolve6.py`（正本 SHA-256 pin `e85d4bfb…`）の拡張版。入力 pin は resolve6 と同一の corpus manifest（1,279）＋5 正本（resolve6・fold9 `24db2352…`・fold10 `bed7d331…`・sweep39_live `22953ae1…`・seventeenth 38 gate 正本 `c1073bae…`・resolve5 `5a2f4815…`）。fail-closed・WIN/REFUTED 衝突 0 を要求。
- **並走への依頼**: 他の n11 レーンは本フル再照合（corpus 依存の fresh-safe pool 再構築・windfall 候補列挙）を重複実行しないこと。出版済み正本のみを使う resolve7（post-fold witness recheck）は並走の管轄のままである。
- **管轄の限界**: 本ノートは候補供給データの出版までを管轄する。witness 計画の掃引・証明書抽出・fold11 は含まない。fold・被覆は行の簿記であり、閉じた行のゲーム理論的値を主張しない。
- 解釈規約は不変: REFUTED-D10 は LOSS 証明ではない。pn/dn・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
