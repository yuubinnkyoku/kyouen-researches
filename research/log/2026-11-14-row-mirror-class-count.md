# 2026-11-14 行鏡像正準クラス数の一般公式（高速レーン・bash 不通の間の純計算枠）

5×22 q=6 の抵抗記録を push した後も bash 実行環境が復旧しなかったため、run_typescript
サンドボックスの純計算だけで完結する課題として、class-split 機械の正準クラス数の一般化
に着手した。

- 主張: 行鏡像 y ↦ w−1−y で割った空でない行部分集合の orbit 数は
  **C(w) = 2^(w−1) + 2^(⌈w/2⌉−1) − 1**（Burnside の補題による全称証明）。
- 検証: 総当たり orbit 列挙 w=1..14 が全一致。既存 sweep の 19（w=5: K0816/K0821・
  本日 5×22 実験）・35（w=6: K0818/K0819）と一致し、7 行初の class-split は
  **71 クラス**・8 行は **135 クラス**が必要なことが確定（sweep 設計の検算用）。
- 成果物: [row-mirror-class-count-20261114](../experiments/row-mirror-class-count-20261114/report.md)
  （report・scripts/orbit_count.js・output/counts.json）+ K 項目 K0822（仮番号・統合時に
  再採番され得る）。
- 運用: K0821 と同じく K 項目単独コミット（generated/ は統合時の build.py で再生成。
  本環境は bash 不通のため check.py/build.py を実行できていない — schema・vocabulary の
  語彙（topics/roles/relations）は SCHEMA.md・VOCABULARY.yaml と突き合わせて従った）。
- counts.json はサンドボックス計算由来（bash 不通のため node を実行できず）。
  再現は scripts/orbit_count.js の再実行で可能。

次の一手: bash 復旧後は 6×22 q=7 多重欠損（dm≥2）32 クラスの高速 UNSAT 判定と
5×22 q=6 未走査 11 クラス。K0822 が build.py の項目として問題なく通るか確認。
