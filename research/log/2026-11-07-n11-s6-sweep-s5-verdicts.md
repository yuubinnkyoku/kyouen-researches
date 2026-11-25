# 2026-11-07 S6全集合スイープと94五石位置の分類

- 対象: 94五石位置の六石子全集合 3,868（`base.reconstruct` の incidence キー）および94五石位置。
- 方法: early-exit スイープ（`s6_sweep.sh`、8並列）。各 S6 は子を順に生成し、WIN7 子で早期終了（手番 WIN）；全子 LOSS7 で手番 LOSS。生成タイムアウトは 0 件。
- 結果: **手番WIN 3,854・手番LOSS 14**。試行回数の合計 29,680。
- 検証: 感受性証明書 4,288 件（14 LOSS の全子＋各 WIN の勝ち子）を独立 Bareiss 監査器（`verify_classify.py`）で全件 PASS（fails 0。不足分 99 件は K0672 系で既監査）。
- 五石集計: 94 位置中、**第二手勝ち 16・先手勝ち 78**（14 LOSS S6 が16位置を被覆）。
- 含意: 中央領域から先手が五石を選ぶ構造（計画前提）では、先手が78先手勝ち位置のいずれかに到達できる限り先手の領域勝利が示唆される。領域→五石・二石root→領域・空盤→二石root の到達可能性は計画前提であり、別途監査が必要である。
- 出力: `s6_sweep/` の verified.json・s5_verdicts.json・sweep_results.json（repo 内は `output/s6sweep/` に複写）。
