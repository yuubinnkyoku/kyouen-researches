# 2026-10-31 完全多部グラフのmisère・r人・全進行数

開始時main 877f9c43f787d41263d48f31eed5708096354bb1、AGENTS.md、knowledge README/summary、K0309、既存の complete-multipartite-split-20261027 と分割グラフr人研究を確認。通常Grundy公式との重複を避け、misèreと多人数終局を対象にした。

**全称証明**：部サイズ偶奇でmisère値と全勝ち初手を閉形式化。通常・misèreの共通勝ち初手はない。r人巡回最終着手者勝利ルールで、各初手が終局長と勝者を固定し、勝者集合、本人勝利条件、全進行数、無作為終局長・勝者分布を完全決定。

**独立検算**：818部サイズ列の二方式厳密再帰、302列の全進行数・r=2..7勝者別度数。不一致0。幾何残局への実現、11×11速度測定は対象外。knowledge正本への昇格と全体CIは未実施。

一次資料：research/experiments/game-structure/complete-multipartite-misere-rplayer-20261031/README.md と verify.py。branch/PRなし、mainへ直接反映。
