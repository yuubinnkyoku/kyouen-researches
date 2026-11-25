---
id: K0675
title: 94五石子S6全集合3,868を全確定し94五石位置を78先手/16第二手に分類（先手WIN方向の転換）
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0674
  note: 修復後46証人の46/46手番WINにより方向性は先手WIN側へ転換
- type: depends_on
  target: K0003
  note: 条件付き証明義務と確定勝敗の区別
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/s5_verdicts.json
  role: data
  note: 94五石位置の勝敗集計（78先手勝ち・16第二手勝ち、各位置のLOSS/WIN子数）
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/verified.json
  role: data
  note: スイープ感受性証明書4,288件の独立監査結果（loss 887 / win 3,401 / fails 0）
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/sweep_results.json
  role: data
  note: 3,868 S6の判定記録（各S6の勝ち子・試行内訳）
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/s6_sweep.sh
  role: source
  note: early-exit スイープドライバ（3,868 S6全数、timeout 0）
- path: research/experiments/n11-central-19-cover-20261031/output/s6sweep/s5_verdicts.py
  role: source
  note: S6判定からの五石位置集計
- path: research/log/2026-11-07-n11-s6-sweep-s5-verdicts.md
  role: log
  note: スイープと五石集計の経緯
scope: 標準11x11完全指摘・通常プレイの94五石子局面の六石全集合3,868および94五石位置。領域→五石・二石root→領域・空盤→二石rootの到達可能性は含まない。
evidence: >-
  94五石位置の六石子全集合3,868について、各S6の手番WIN（WIN7子が存在）/手番LOSS（全子LOSS7）をearly-exitスイープで判定した（生成タイムアウト0件、試行回数合計29,680）。感受性証明書4,288件（14 LOSSの全子と各WINの勝ち子）を独立の 4x4 Bareiss 監査器で検証し、fails 0（不足分99件はfocus62/frontierで既監査）。結果は手番WIN 3,854、手番LOSS 14であった。この判定から94五石位置の勝敗は、第二手勝ち16（LOSS子を持つ位置）・先手勝ち78（全子手番WIN）に分類される。中央領域から先手が五石位置を選ぶ構造（計画前提）에서는、先手勝ち位置78件の存在により先手の領域勝利が示唆される。領域→五石・二石root→領域・空盤→二石rootの到達可能性は計画前提であり、本項目の監査範囲外である。
---

# S6全集合の確定と94五石位置の分類

94五石位置の六石子全集合 **3,868** について、手番WIN（WIN7 子あり）/手番LOSS（全子 LOSS7）を early-exit スイープで判定した（タイムアウト 0 件）。感受性証明書 4,288 件は独立の 4x4 Bareiss 監査器で検証済み（fails 0。不足分 99 件は K0672 系で既監査）。

結果は **手番WIN 3,854 件・手番LOSS 14 件** であった。14 件の手番 LOSS は、原始先手が敗北する第二手証人であり、本領域における真の LOSS 証人分布を示す。

94 五石位置については、LOSS 子を持つ16位置が第二手勝ち、残り **78 位置が先手勝ち** に分類された。中央領域から五石位置への到達（先手が五石を選ぶ構造）は計画の前提であり、本項目の監査範囲外であるが、78 先手勝ち位置の存在は先手の領域勝利を示唆する。
