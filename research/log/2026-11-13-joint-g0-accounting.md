# 2026-11-13 高速レーン: joint g0会計で合同フロンティアをw≤114に延伸（K0800）— K0797のg3壁は単一法のアーティファクト

main取り直し（開始時 b8b7cfb1・並走のw=67 P(w)キャンペーン進行中・
joint g0会計は主題独立・items実参照で K0799 が max・K0800 空きを確認）。

K0797レジューム(2)「g3形 size ≥ 29 を切る非合同式手法」に着手。

## 成果（K0800・有限完全検査・3経路一致）

1. **g3壁（size 29・w=85..87・全法 classMax=17）は単一法解析のアーティファクト**。
   正しい joint 会計量は |∩_m Pass_m(a,u)|（同一 (a,u) で同じ行 t が全法通過）で、
   単一法 classMax < 17 は 1 法証明書の特別例。
2. **joint 全滅**: size 29 は法対 {19,23}（DFS nodes 17,550・depth 1）、
   size 30..38 は {19,23,29,31}（DFS 65,776..10,031,034 nodes・depth 3）。
   合同フロンティアは w ≤ 84 → **w ≤ 114** に延伸。g2/g4..g8 は w ≤ 132 まで
   単一法のまま有効。
3. **p-チェーン補題**: v ∈ QR(p^k) ⟹ v ∈ QR(p^j)。33法は34個の最大素数冪に
   無損失簡約（5,7,8,9,11,13,16,17,25,27,32,49,64,81 が冗長）。
4. **g3 size 39..44（w=115..132）は open**（DFS 120M/25M nodes・depth 6 予算内
   未解決）として記録。
5. **意味論**: P(w) は決定しない。K0785（P(83) ≥ 34）で level 17 extinction は
   w ≥ 83 で偽 → 実務的寄与は w ≤ 82。価値は方法論的（合同証明書の到達限界・
   法リスト冗長性・K0797「非合同式手法が必要」見立ての訂正）。

## 制御（全PASS）

- 3経路一致: DFS ≡ BFS（交差実装・消滅は法31直後で証明書と一致）≡
  size29直接ブルートフォース（437²=190,969対・max=16 @ (0,77)）。
- K0797 既知値再現: g3 単一法 s27:16@343(≡49)・s28:16・s29:17@31。
- K0797 失敗 witness (0,1)@31 s29 の 17 行生存を再現 → 誤殺でないことを確認。
- cm49 ≡ cm343 = [16,16,17]（p-チェーン補題の数値確認）。

## 教訓

- 単一法の classMax = L は「合同手法の限界」を意味しない。複数法の joint
  通過（同一 (a,u)・同一行集合）が正しい会計量。壁の同定には joint 証明書の
  探索（coprime CRT DFS）まで実行すべき。
- LAWS ベース（合成法込み・非互いに素）の BFS は survivor 爆発で 16MiB OOM。
  MODS coprime（最大素数冪のみ・互いに素）への切り替えで CRT 独立走査が可能に
  なり劇的に高速化。法リストの冗長性除去は単なる最適化でなく正確性の前提。
- JS の 1<<32 は wraparound する（(1<<32)-1 = -1 相当の比較誤り）。s=32 で偽の
  「単一法kill」が出た。ビットマスク幅 ≥ 32 の行集合には BigInt かビット配列
  （本スクリプトは 2×32bit 分割ビットマスク）が必須。
- 重い joint 検証は per-form / per-size の CFG 分割で 16MiB サンドボックス制限を
  回避（g3 のみ 15,286,958 ノード総計）。

## push

- research/experiments/joint-g0-accounting-20261113/scripts/joint_g0_accounting.ts
- research/experiments/joint-g0-accounting-20261113/output/joint_g0_accounting.json
- research/experiments/joint-g0-accounting-20261113/reports/joint-g0-accounting.md
- research/knowledge/items/K0800-joint-g0-accounting-w114.md
- research/knowledge/items/K0797-g0-accounting-valid-through-w84.md（更新セクション追記）
- 本ログ

## レジューム（次回の実行）

1. **g3 size 39..44 の joint 延伸**: 深い素数冪（19²=361, 23²=529, 29²=841,
   31²=961）を MODS に追加、または pairwise meet-in-the-middle
   （法対ごとの生存 (a,u) 集合の共通部分・sweep 併合）で w ≤ 132 まで狙う。
2. **(10⁷,10⁸] 34点帯掃引**（別候補・先頭素数帯分割・gainCost枝刈りの
   バグ修正要）。
3. 標準形 level 17 DFS（w=65..）の前提は K0800 で w ≤ 114 まで強化済み
   （コスト自体は長期レーン）。
4. 次の空き K 番号: **K0801**。

11×11 空盤・二石 root {49,60} は **UNKNOWN**（長期レーン）。
