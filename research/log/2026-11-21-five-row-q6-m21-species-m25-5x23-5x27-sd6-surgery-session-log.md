# 2026-11-21 五行 q6 m21種 / q5 m25種 5x23/5x27 sd≤6 種拡張サージェリー・セッションログ

高速レーン。宣言 `research/log/2026-11-21-five-row-q6-m21-species-m25-5x23-5x27-sd6-surgery-single-owner-note.md`
（commit `5c4cfca9`、宣言時 HEAD `c2010307`＝親実験の成果出版コミット）に基づく
単一オーナー実装・実行・公開。対応実験: `research/experiments/five-row-q6-m21-species-m25-5x23-5x27-sd6-surgery-20261121/`。

## 経緯

- 前セッション（同日 22:21-22:26Z）が宣言ノートを push してシード 24 種・鏡像 16 種・
  自己補完対照 4 種・q6 id@t0 1 実行（5,095,913 leaves・0 witness）まで進めたところで
  セッション中断（m21_m21_id_t1.jsonl が空のまま残存）。
- 本セッションが kit（`_frontier-sd6-surgery-kit/exp2/`・リセット耐性配置）から
  状態を再検証して再開: 機材 3 点は md5 ピンと一致、t0 実行は後述の再実行と完全一致
  （決定性のセッションまたぎ確認）、空の t1 は最初から実行し直した。

## 宣言からの重要な訂正（グリッド）

宣言ノートは "3 classes for 5x23 span-21 seeds" と書いたが、m=21 witness 種の実際の
bbox 幅は 18（x∈[0,17]）であり、5x23 上のフィッティング配置は offX 0..5 の **6 类**。
m=22 種（span 21・3类）との混同によるドラフト誤り。**完全 6 类グリッド**を実行して
宣言グリッドのスーパーセットとして完走させた（fail-closed: 部分グリッドで負を
出版しない）。q5 側（w25・span 20・8类）は宣言通り。
この訂正は README と manifest の `grid_correction` に明記済み。

## ゲート・対照（全 PASS・実験 output/ に記録）

1. census gates 再実行: (5,23,6)=996 / (5,27,5)=2355、双方向差 0。
2. シード健全性（宣言条件1）: 4 種 × {sat.js verifyConfig, verify_general.py
   （親実験で tamper 陰性確認済みの修正版 Fractions 検証器）, safety_only.js} = 12 PASS。
   （verifyConfig はホーム盤上の safe + maximal を含意、4 種は deficient-maximal witness。）
3. 自己補完陽性対照（条件3）: 4 種の minus-2 シード → m21_m21: 1 witness、
   varA/varB: 2 witnesses、m25: 2 witnesses、全て元種を正確に含む。
4. 来歴（provenance）: seed_w56_21.json / verify_variants_5x21.json / w25.json は
   repo 生 file と byte-identical（curl diff）。種構成・16 鏡像は機械再計算で一致。

## 主成果（全て陰性・不在主張ではない）

- **(5,6) 5x23**: m21 種 3 種（original/varA/varB）× 全 6 オフセット = 18 代表実行 +
  m21_m21 class t=0 の 4 メンバー交差確認（H@0/V@5/HV@5 = id@0 = 5,095,913）。
  合計 21 実行・108,861,233 leaves・0 maximal・0 witness。
  leaf 数は m21_m21 < varA < varB で単調、nP は全配置で 125,671 固定。
- **(5,5) 5x27**: m25 種 × 全 8 オフセット + class t=0 交差確認（4,920,056 ×4）。
  合計 11 実行・53,719,943 leaves・0 maximal・0 witness。nP 260,246 固定。
- **計 32 実行・162,581,176 leaves・全負。** M_{5,6} ∈ [23,249]、M_{5,5} ∈ [27,336] 不変
  （csv note/source 列のみ拡張）。
- **これで五行前線 2 盤（5x23/5x27）の sd≤6（deficit 制限付き）近傍は公開 witness 種
  全部（m22, m21×3 / m26, m25）で空**であることが確定したクラス命題になった。
  witness jump ≥14/≥15 石の先行観測と整合（近傍手術では前線を跨げない）。
- 対称性クラス roster を新しい span（18/20）でも全称 assertion 検証
  （`output/symmetry_classes.txt`・36 assertion PASS）。bbox 幅が盤幅−span を超える
  汎用式（class t = {id@t, H@t, V@(m−s−t), HV@(m−s−t)}）は span 20/21 に加え 18 でも成立。

## 決定論性

- m21_m21 id@0: 前セッション実行と本セッション再実行が leaf 数・全 key invariant で一致。
- m25 id@0: 2 回一致。交差クラスの 4 メンバー一致は独立再現×4。
- `output/records.jsonl` 34 行（32 実行 + 2 決定性ダブル）。

## 今後の実行可能課題（この宣言油田の枯渇判定）

- 五行前線 2 盤の「全公開種 × 全配置 × sd≤6」は本実験で完走。次の高速価値は
  (a) **sd≤(4,3)/(3,4)**: nP 125,671→約50万で単発 2-3分予想・宣言必要。
  (b) **自由削除クラス**（deficit 曲線外の削除を許す拡張）: surgery4 の設計変更が必要で、
  leaf 数が非自明に増大。リスク高・情報価値中。
  (c) 前線種に近い**新種の探索**（m21 種の 3-swap 近傍など）は別レーンの対象。

## 運用メモ

- 前セッションの中断は 1 bash に多数実行を束ねた過去の事故と同型。今回は
  1 call = 最大 3 実行で全 33 実行を分割して完走、環境リセットなし。
- 実験ツリーは knowledge 配下 kit に置いたまま実行・集計・出版原稿を作る設計で
  中断・リセット両方に耐えた（前セッションの t0 生ファイルがそのまま本出版に収録）。
