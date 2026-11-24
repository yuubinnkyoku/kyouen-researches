---
id: K1293
title: Steiner 3-設計上の共演ゲーム — Witt/アフィン幾何 7 ボードの完全 Grundy と graded 性
kind: computation
status: computed
topics: [grundy, geometry, statistics, search-methods]
aliases:
- Kyouen on Witt designs
- complete Grundy values for AG(3,2), AG(4,2), W_11, W_12, W_22, W_23, W_24
- graded Kyouen on Steiner 3-designs
relations:
- type: extends
  target: K1253
  note: 反転平面の完全 Grundy を、符号理論から構成した Steiner 3-設計ボード族へ拡張
- type: related
  target: K1274
  note: 一般上界 K_s ≤ (s−2)λ2/λ3+2 を各設計で比較し、W_22 の tight 例を与える
- type: depends_on
  target: K1058
  note: 共演ゲームの定義と出版済み Grundy エンジン（grundy_full.exe）の出典
artifacts:
- path: research/experiments/design-kyouen-witt-20261125/report.md
  role: log
  note: 構成・完全 Grundy 表・K_s 表・graded 性・限界の総括
- path: research/experiments/design-kyouen-witt-20261125/scripts/build_designs.py
  role: source
  note: GF(2^11)/GF(3^5) と QR 構成で Golay 符号・Witt 設計・AG(d,2) を構成し全パラメータを検査
- path: research/experiments/design-kyouen-witt-20261125/scripts/ks_ilp.py
  role: solver
  note: scipy HiGHS のバイナリ ILP で K_3, K_4, K_5 を独立に厳密計算
- path: research/experiments/witt-s-spectrum-20261125/report.md
  role: log
  note: W_24 の s=1..7 完全 Grundy と dodecad 同定
- path: research/experiments/witt-s-spectrum-20261125/output/spectrum.json
  role: data
  note: s 別の安全局面・極大サイズ・Grundy 分布・構造的事実
- path: research/experiments/witt-s-spectrum-20261125/independent/REPORT.md
  role: log
  note: 独立検証（2 実装、s=2..7 全数一致、s=6 の全 12-点集合走査を含む）
- path: research/experiments/witt-s-spectrum-20261125/independent/out/compare_claims.json
  role: certificate
  note: 生データと主張の照合（不一致 0）
- path: research/experiments/design-kyouen-witt-20261125/output/grundy_w24_s6.txt
  role: data
  note: s=6 の完全 Grundy（1,937,867 局面、極大 12 が 2,576）
- path: research/experiments/design-kyouen-witt-20261125/scripts/summarize.py
  role: verifier
  note: Grundy 出力の解析、λ4 の再計算、上界との比較表の生成
- path: research/experiments/design-kyouen-witt-20261125/output/designs_meta.json
  role: data
  note: 7 設計の λ2, λ3, λt 全数検査の結果
- path: research/experiments/design-kyouen-witt-20261125/output/grundy_w22.txt
  role: data
  note: W_22 の完全 Grundy 出力（safe 18,162、K=7、Grundy 分布 0:9306, 1:8856）
- path: research/experiments/design-kyouen-witt-20261125/output/ks_ilp.json
  role: data
  note: K_3, K_4, K_5 の ILP 厳密値
- path: research/experiments/design-kyouen-witt-20261125/independent/REPORT.md
  role: log
  note: 独立実装（Grundy エンジン・ILP 不使用）による全タスク PASS の検証報告
- path: research/experiments/design-kyouen-witt-20261125/independent/run_all.py
  role: verifier
  note: 設計パラメータ・K_3/K_4・graded 性・Grundy/misère の独立再計算ドライバ
- path: research/experiments/design-kyouen-witt-20261125/independent/out/task2_3_k3_graded.json
  role: certificate
  note: K_3 全列挙と graded 性の結果（W_22 の 8-集合なし証明を含む）
scope: 7 つの Steiner 3-設計（AG(3,2), AG(4,2), W_11, W_12, W_22, W_23, W_24）上の「各ブロックに高々3点」共演ゲームの完全 Grundy（通常・misère）、および各ブロックに高々 s 点の K_s（s=3,4,5）。
evidence: 設計は符号理論からゼロ構成し、すべての t-部分集合についてブロック数が一様（λ_t）であることを全数検査。Grundy は出版済み grundy_full.exe（64bit マスク）で全安全局面を列挙。K_s は別経路の ILP で計算し、K_3 は Grundy の最大サイズと 7 ボードすべてで一致。観察は (i) 7 ボードすべてで極大安全集合のサイズは K に一様（graded）で、Grundy(S)=(K−|S|) mod 2、Grundy 値は {0,1}、空盤は K mod 2。(ii) 任意の4点がブロックに載る4-設計（W_11,W_12,W_23,W_24）では K_3=3 で安全局面は ≤3 点の全部分集合（safe 数 = Σ_{j≤3}C(v,j)）。(iii) W_22 で K_3=7 が一般上界 (v−2)/(k−2)+2=7 を達成（非自明な tight 例）。(iv) 反転平面盤では短い極大集合が存在し Grundy ≥2 が現れるが、これらの設計では現れない。独立実装（標準ライブラリのみ、Grundy エンジン・ILP 不使用）が設計パラメータ・K_3・K_4・graded 性・完全 Grundy/misère を全 7 ボードで再検査し PASS（discrepancy 0、independent/REPORT.md）。
---

# Steiner 3-設計上の共演ゲーム — Witt/アフィン幾何 7 ボード

## 結果

| board | 設計 | v | safe | Grundy(∅) | misère | K_3 | 上界 | K_4 | K_5 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AG(3,2) | 3-(8,4,1) | 8 | 149 | **0** | 1 | 4 | 5 | 8 | 8 |
| AG(4,2) | 3-(16,4,1) | 16 | 5,513 | **0** | 1 | 6 | 9 | 16 | 16 |
| W_11 | 4-(11,5,1) | 11 | 232 | **1** | 0 | 3 | 5 | 6 | 11 |
| W_12 | 5-(12,6,1) | 12 | 299 | **1** | 0 | 3 | 4 | 4 | 6 |
| W_22 | 3-(22,6,1) | 22 | 18,162 | **1** | 0 | **7** | 7 | 10 | 15 |
| W_23 | 4-(23,7,1) | 23 | 2,048 | **1** | 0 | 3 | 6 | 8 | 11 |
| W_24 | 5-(24,8,1) | 24 | 2,325 | **1** | 0 | 3 | 5 | 4 | 6 |

上界は `K_s ≤ (s−2)λ2/λ3 + 2 = (s−2)(v−2)/(k−2) + 2`（K1274 の一般上界）。

## 発見

1. **graded 性**: 7 ボードすべてで、極大安全集合のサイズは最大値 `K` に一様。
   層別カウントの `maximal` は最大サイズ層のみ非零。よって
   `Grundy(S) = (K−|S|) mod 2`、Grundy 値は `{0,1}`、空盤の Grundy は `K mod 2`。
   反転平面盤では最小極大 `s(q) < K` の例があり（q=13 で 7<8）、Grundy 2 以上が
   現れる。この差は設計の自己同型群の強さ（延長補題）に由来すると考えられる。
2. **4-設計の退化**: 任意の 4 点がブロックに載る設計（W_11, W_12, W_23, W_24）では
   `K_3 = 3`、安全局面は `≤3` 点の全部分集合。安全局面数は
   `1+v+C(v,2)+C(v,3)` に一致（232, 299, 2048, 2325）。
3. **W_22 の tight 例**: `K_3 = 7 = (22−2)/(6−2)+2`。352 個の最大 7-集合は
   すべて Grundy 0。
4. **アフィン幾何は P 位置**: AG(3,2), AG(4,2) は `Grundy(∅)=0`（K が偶数）。
   Witt 設計は `Grundy(∅)=1`（K が奇数）。

## 方法

- 設計構成: 2元 Golay 符号 [23,12,7] と [24,12,8]、3元 Golay 符号 [12,6,6] を
  QR 構成（`GF(2^11)` の 23 分根、`GF(3^5)` の 11 分根）で作り、重さ k の語の台を取る。
  派生設計 W_11, W_22 は 1 点での派生。AG(d,2) は F_2^d のアフィン平面。
- 全パラメータを全数検査（λ2, λ3, λ4, λ5）。
- Grundy は出版済み `grundy_full.exe`（n≤64）で完全計算。
- K_s は scipy HiGHS のバイナリ ILP（各ブロック ≤s 制約）で独立計算。

## s-スペクトル（W_24、追記 2026-11-25）

W_24 で s=1..7 の完全 Grundy を計算（s 可変エンジン、`witt-s-spectrum-20261125`）。

| s | 安全局面 | 極大サイズ（個数） | パリティ | G(∅) | misère | Grundy 最大 |
|---:|---:|---|---:|---:|---:|---:|
| 1 | 25 | 1 (24) | 奇数 | 1 | 0 | 1 |
| 2 | 301 | 2 (276) | 偶数 | 0 | 1 | 1 |
| 3 | 2,325 | 3 (2,024) | 奇数 | 1 | 0 | 1 |
| 4 | 12,951 | 4 (10,626) | 偶数 | 0 | 1 | 1 |
| 5 | 168,799 | 6 (113,344) | 偶数 | 0 | 1 | 1 |
| 6 | 1,937,867 | 12 (2,576) | 偶数 | 0 | 1 | 1 |
| 7 | 7,932,035 | 12 (1,020,096), 13 (30,912) | 混在 | 0 | 0 | 2 |
| 8 | 16,777,216 | 24 (1) | 偶数 | 0 | 1 | 1 |

- s=2..6 は graded（極大サイズ一様）で Grundy `{0,1}`、s=7 のみパリティ混在で
  Grundy 2 が 2,606,912 局面に出現（K1298 の予測どおり）。
- s=2,3,4 の極大集合はすべての s-点集合（W_24 が 5-設計で任意の (s+1)-点集合が
  octad に含まれるため）。
- s=5 の極大集合はどの octad にも含まれない 6-点集合（113,344）。
- **s=6 の極大集合は 2,576 個の dodecad**（Golay 符号の重み 12 語）と同定。
- 他の設計盤の s-スペクトル（同じエンジン）:
  W_11 s=3/4、W_12 s=3/4/5 は graded で `{0,1}`。
  W_23 s=5 は極大 9/11（奇数一様）で `{0,1}`、s=6 は 12/16（偶数一様）で `{0,1}`。
  W_22 s=4 は 8/10（偶数一様）で `{0,1}`、s=5 は極大 11/12/15 でパリティ混在、
  **Grundy 3 が 101,640 局面**に出現（設計盤で初の 3）。
- 独立検証（別実装 2 系統、5/5 PASS）: s=2..7 の全データ一致。とくに s=6 は
  C(24,12)=2,704,156 個の全 12-点集合を走査して極大＝dodecad 2,576 個を確定、
  s=7 も 7,932,035 局面を 2 実装で一致確認。dodecad は各 octad と {2,4,6} 個で交わり
  （プロファイル 2:132, 4:495, 6:132）、各 dodecad は 66 個の octad 対から生じる。
- 実験: [witt-s-spectrum-20261125](../../experiments/witt-s-spectrum-20261125/report.md)。

## 限界

- ≤4/≤5 点版の Grundy は未計算（エンジンは ≤3 専用）。
- graded 性の一般証明は未取得（7 例の観察）。
- W_22 の最大集合の軌道分解・構造は未調査。
- 「短い極大集合」を持つ 3-設計の例は未発見。
