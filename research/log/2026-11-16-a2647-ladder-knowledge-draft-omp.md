# 2026-11-16 候補Aラダー結果の knowledge ドラフト作成 (W27, omp)

候補A予算ラダー（完了 2026-11-13 06:31 JST、ローカルコミット f8fd6578、
統合ログ `research/log/2026-11-13-a2647-candidate-a-ladder-result-omp.md`）の結果を
knowledge 化するためのドラフト（新規項目1件・K0717 更新案1件）と統合チェックリスト。

**本ログは knowledge 項目を編集しない。** 統合は別タスクで行う。数値はすべて
原典（統合ログ本文、および
`research/experiments/parabola-ternary-selection-20261109/output/ladder-d<D>-target1322-budget<B>/result.json`
の実読）からの転記。

## 1. 原典との照合

出力ディレクトリ配下の全 45 件の `result.json` を実読し、統合ログの表と一致することを
確認した。全 45 件が `p=2647, target=1322, empty_bound=3, variables=7926, clauses=68404,
base_clauses=53886, base_cnf_source=regenerated` で、solver は Cadical195。
各段は `conflict_budget`（3,000,000 / 10,000,000 / 20,000,000）と `status` を持つ。

判定内訳: SOLVER_UNSAT 8、UNKNOWN 37、SAT 0。solve_seconds 合計 **127,328.3 秒**
（JSON の `solve_seconds` 全45件の単純和）。統合ログの 127,328.3 と一致。

### 1a. 決着した 8 d（すべて SOLVER_UNSAT、原典一致）

| d | 決着段 | conflict_budget | conflicts（統計値） | solve_seconds（JSON 実値） |
|---|---|---|---|---|
| 622 | 3M | 3,000,000 | 1,796,375 | 371.1993925330007 |
| 914 | 3M | 3,000,000 | 628,202 | 92.50687438800014 |
| 977 | 3M | 3,000,000 | 417,436 | 61.3825815830005 |
| 1040 | 3M | 3,000,000 | 447,601 | 63.10352762599996 |
| 1292 | 3M | 3,000,000 | 674 | 0.0748120709995419 |
| 1258 | 10M（3M は UNKNOWN） | 10,000,000 | 4,176,372 | 887.4729327630012 |
| 1266 | 10M（3M は UNKNOWN） | 10,000,000 | 3,945,161 | 819.24660597 |
| 820 | 20M（3M・10M は UNKNOWN） | 20,000,000 | 13,294,778 | 3813.1327922759997 |

統合ログの表（conflicts 1,796,375 / 628,202 / 417,436 / 447,601 / 674 / 4,176,372 /
3,945,161 / 13,294,778、solve_seconds 371.2 / 92.5 / 61.4 / 63.1 / 0.1 / 887.5 /
819.2 / 3,813.1）と実値が一致。秒数の差は統合ログが小数第1位までの丸めであるため。

### 1b. 全段 UNKNOWN で尽きた 11 d（原典一致）

147, 188, 194, 488, 602, 703, 717, 1003, 1103, 1166, 1229。
各 d について 3M / 10M / 20M の 3 段すべてが `status=UNKNOWN`（`conflicts` は
各予算を使い切る水準）。統合ログの列挙と一致。

### 1c. 留保（原典の記述）

- 8 件の決着はいずれも `status=SOLVER_UNSAT` であり、出力ディレクトリは
  `init.json / input.cnf.gz / result.json` の3ファイルのみ。**ladder の全 45 結果ディレクトリ
  （`.partial-*` を除く）に DRAT/proof ファイルは存在しない**（`find` で確認、0 件）。
  `result.json` の `scope` も「Solver UNSAT is unaudited and restricted to this d.」と明記。
- `result.json` 群と `init.json` は git 追跡下（`.partial-*` と `input.cnf.gz` は追跡外）。
- 本結果はクラス (1,1,3) の判定ではなく、A(2647) の範囲 1296 ≤ A ≤ 1322 を動かさない。

## 2. 新規 knowledge item ドラフト（仮番号 K0726）

**仮番号について**: main 上の最大は K0724。ただし 2026-11-12 の W20 ドラフト
（`research/log/2026-11-12-w20-knowledge-draft-omp.md`）が仮 K0725 を提案済みで未統合。
採番衝突を避けるため本ドラフトは仮 K0726 とする（AGENTS.md「K番号」のとおり両者とも
統合時に renumber される。統合担当は K0725 と本項の採番を同時に解消すること）。

ファイル名案: `research/knowledge/items/K0726-p2647-113-budget-ladder-3m-20m.md`
（統合時に採番し直す場合は slug も同時に更新）。

```markdown
---
id: K0726
title: p=2647 サイズ1322 形状クラス(1,1,3) の層別19 d は 3M/10M/20M ラダーで 8 件 UNSAT に到達し、11 件は 20M でも UNKNOWN である
kind: computation
status: computed
topics: [geometry, maximum-safe, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0712
  note: 固定原点・一完全対の三値還元（d 固定 CNF）の上での予算ラダー
- type: depends_on
  target: K0723
  note: d を引数化した一般 d 符号化（各段は再生成 CNF）
- type: supports
  target: K0717
  note: 100k 掃引の「決まる d の地図」に対する予算軸の拡張
artifacts:
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-d914-target1322-budget3000000/result.json
  role: data
  note: void 内部 d=914 の SOLVER_UNSAT、conflicts 628,202、92.507 秒
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-d820-target1322-budget20000000/result.json
  role: data
  note: 20M 段まで掛かった d=820 の SOLVER_UNSAT、conflicts 13,294,778、3,813.133 秒
- path: research/experiments/parabola-ternary-selection-20261109/output/ladder-d147-target1322-budget20000000/result.json
  role: data
  note: 全段 UNKNOWN で尽きた 11 d の代表（d=147、3段すべて UNKNOWN）
- path: research/log/2026-11-13-a2647-candidate-a-ladder-result-omp.md
  role: log
  note: 方法・45 件の判定表・留保（DRAT 未保存）
scope: p=2647、size=1322、形状クラス (x,c,e)=(1,1,3)。層別 19 d（147,188,194,488,602,622,703,717,820,914,977,1003,1040,1103,1166,1229,1258,1266,1292）を conflict 予算 3,000,000→10,000,000→20,000,000 で段階実行した有限計算（全 45 実行）。各 d は決着段で停止。
evidence: 45 件の result.json を実読集計。判定 SOLVER_UNSAT 8・UNKNOWN 37・SAT 0、solve_seconds 合計 127,328.3 秒を確認した。
---

## 結果

層別サンプル 19 d を単一の固定 d 三値 CNF（K0712）に対して conflict 予算
3M→10M→20M と段階的に上げ、全 45 実行を得た。判定は SOLVER_UNSAT 8・
UNKNOWN 37・SAT 0、solve_seconds 合計 127,328.3 秒。

決着した 8 d はすべて SOLVER_UNSAT で、段ごとに次のとおり
（d: 決着段 / conflicts）:

- 3M 段で決着（5 件）: 622 / 1,796,375、914 / 628,202、977 / 417,436、
  1040 / 447,601、1292 / 674。
- 10M 段で決着（2 件、3M は UNKNOWN）: 1258 / 4,176,372、1266 / 3,945,161。
- 20M 段で決着（1 件、3M・10M は UNKNOWN）: 820 / 13,294,778。

全段 UNKNOWN で尽きた 11 d: 147, 188, 194, 488, 602, 703, 717, 1003,
1103, 1166, 1229（3M / 10M / 20M のいずれも UNKNOWN）。

## 解釈

予算増は決着数に対して実際に効く。100k 予算の掃引（K0717）で UNKNOWN だった d のうち
8 件が 20M 以下で SOLVER_UNSAT に到達した。特に 914, 977, 1040 は、K0717 が
「中盤 d=852..1278 の 427 件はすべて UNKNOWN（UNSAT 0 件）」とした区間の内部に
ありながら 3M 段で速く決着した。

したがって中央区間 d=852..1278 の「UNSAT 0 件」は、
**「決着する d が存在しない区間」ではなく「100k 予算では届かない区間」**として
読み替えるのが適切である（この読み替えは本有限計算のみを根拠とし、
区間内の残り d が決着可能であることを含意しない）。

1292 は K0717 の尾部連続 UNSAT 帯（d=1279..1316）の直後の近傍で、674 conflicts の
即時決着はその尾部パターンと整合する。

一方、11 d は 20M でも決着せず、この予算帯では予算ラダーを伸ばすだけでは
残り全 d の決着は見通せない。

## 限界

- **8 件の SOLVER_UNSAT はソルバの主張のみで、単体の DRAT 証明は保存されていない。**
  出力ディレクトリに proof は無く、`scope` も unaudited と明記する。
  領収書付きの UNSAT ではない（K0724 の問いと同種の未監査）。監査には該当 d を
  DRAT 付きで再実行する必要がある。
- これは**クラス (1,1,3) の判定ではなく**、A(2647) の範囲 1296 ≤ A ≤ 1322 を動かさない。
  UNKNOWN 37 件は UNSAT でも SAT でもない。
- 各段は独立の再生成 CNF での実行であり、段間で学習節は共有されない
  （K0717 の単一インスタンス昇順掃引とは履歴の扱いが異なる）。
- 標本は層別 19 d に限る。「予算増が効く」はこの 19 d の範囲での観測であり、
  非標本の d への外挿は主張しない。
```

## 3. 新規 item を分離した理由（数学的証明との混同回避）

repo AGENTS.md の規約（有限計算・観測・独立検証・数学的証明を混同しない）に従い、
本項を次に分離した。

- 本項（kind `computation`, status `computed`）が担うのは、明示した有限範囲
  （層別 19 d × 3 予算、全 45 実行）の完了計算の記録のみ。
- 「100k では届かず高予算では届く d が存在する」という**観測**は 914, 977, 1040
  （および 1258, 1266, 820）という標本に限る。区間全体の命題としては主張しない。
- UNSAT の**数学的確定**（DRAT 監査や Lean 証明）は本項の範囲外。よって
  status は `proved` や `verified` ではなく `computed`。DRAT 未保存という留保は
  §限界 に独立項目として明記した。

## 4. 既存項目への更新提案

### 4a. K0717 への追記案（更新提案あり）

対象: `research/knowledge/items/K0717-p2647-113-full-d-sweep-100k.md`。

K0717 は「100k 予算で決まる d の地図」を与え、結果節で
「中盤 d=852..1278 の 427 件はすべて UNKNOWN」と述べる。本ラダーは
この区間内部の d（914, 977, 1040）が 3M で決着することを示したため、
当該記述が**予算軸を欠いた地図**であることを明示する追記を提案する。

- title / scope / evidence / status は変更しない（K0717 の有限計算は 100k のまま）。
- 本文の変更候補（新規 K0726 を参照する1文の追記。K0717 の主張の強さは変えない）:
  「中盤 d=852..1278 の 427 件はすべて UNKNOWN」の直後に次を追加する:

  ```
  この区間の UNSAT 0 件は「決着不能」ではなく「100k 予算では届かない」である:
  層別 19 d の予算ラダー（3M/10M/20M）で、区間内部の d=914,977,1040 が 3M、
  d=1258,1266 が 10M で SOLVER_UNSAT に到達した（K0726）。本項の地図は
  conflict 予算 100k 固定の写像であり、予算依存は K0726 が担う。
  ```

- 判断の根拠: K0717 の限界節は既に「100k 予算で決まる d の地図」と限定しているため、
  本追記はその限定を読み手に具体的な反例付きで示すもので、命題の変更ではない。

### 4b. K0724 は変更提案なし

`K0724-assumption-unsat-drat-gap.md`（候補B の assumption-UNSAT を単体 DRAT へ
落とす問い、status `open`）は候補B 経路の未解決問いであり、本ラダー（候補A・固定 d CNF）
とは経路が異なる。ただし両者は同じ「ソルバ主張と DRAT 領収書の乖離」を共有するため、
K0726 から `depends_on` ではなく本文で参照することが望ましい（relation を張る場合は
方向を統合担当が判断）。**K0724 の本文は変更不要**。

### 4c. その他の関連項目

- `K0097-integer-residue-parabola-bounds.md`（A(2647) の上下界表記）: 本項は範囲
  1296 ≤ A ≤ 1322 を動かさないため**更新不要**。
- `K0711-p2647-safe-lower-bound-1292.md`: 同様に**更新不要**（本項は上界側を動かさない）。
- `K0712` / `K0723`: 本項が依存する還元・実装の正本であり**更新不要**。

## 5. 統合チェックリスト

knowledge 構造を変更したため、AGENTS.md「統合前の確認」に従い統合後に実行する。

```sh
uv sync --locked
uv run --locked python tools/knowledge/check.py
uv run --locked python -m unittest discover -s tools/knowledge/tests
uv run --locked python tools/knowledge/build.py
git diff --exit-code -- README.md research/knowledge/generated
```

手順:

1. main の最新を fetch し、仮 K0725（W20 ドラフト）と仮 K0726（本ドラフト）の
   採番衝突を解消する。新しい main の最大番号に応じて両者を採番し直し、
   ファイル名 slug と他項目からの参照リンク・relation target を同時に更新する。
2. §2 の新規項目を `research/knowledge/items/` に作成する。artifact path が
   追跡下で実在することを確認する（`ladder-d914-target1322-budget3000000/result.json`,
   `ladder-d820-target1322-budget20000000/result.json`,
   `ladder-d147-target1322-budget20000000/result.json` は git 追跡下。
   `input.cnf.gz` と `.partial-*` は追跡外のため artifact に含めない）。
3. §4a の K0717 追記案を適用する場合は、K0726 の採番確定後に本文中の
   「K0726」を最終番号へ置換する。適用しない場合は理由を記録する
   （AGENTS.md「現在の結論を複数の場所で並行管理しない」に留意し、
   K0717 が予算軸を K0726 に委ねる形にする）。
4. `check.py` で schema（必須 field・status_by_kind・relation の自己辺/循環禁止・
   artifact の実在 path）を検証する。新規項目は kind `computation` /
   status `computed` を VOCABULARY.yaml の `status_by_kind` と照合する。
5. unittest と build.py を通し、`README.md` と `research/knowledge/generated` の
   diff が空（生成物が正本と一致）であることを確認する。

## 6. 留保

- 本ドラフトの数値はすべて §1 の result.json 実読と統合ログ本文からの転記。
  秒数は JSON の float 実値（統合ログは小数第1位丸め）を引用した。
- 新規 item 案の artifact は repo 内に実在する追跡ファイルのみを指す。
  DRAT 証明は存在しない（全 ladder ディレクトリで確認）ため artifact に含めない。
- void の読み替え（§2「解釈」）は 914, 977, 1040 という標本を根拠とする観測であり、
  区間 852..1278 全体の命題ではない。この限定を本文に明記した。
- 本ログは knowledge 項目を変更していない。統合作業は別タスク。

（完）
