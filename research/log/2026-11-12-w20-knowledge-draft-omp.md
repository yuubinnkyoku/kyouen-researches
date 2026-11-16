# 2026-11-12 W20 の knowledge ドラフト作成 (W25, omp)

W20（`research/log/2026-11-12-a2647-1322-drat-audit-omp.md`）の結果を knowledge 化するための
ドラフト（新規項目1件・K0706 更新案1件）と統合チェックリスト。

**本ログは knowledge 項目を編集しない。** 統合は別タスクで行う。数値はすべて
一次資料（W20 ログ、`output/w20-drat-1322/class-*/` の init.json / solver.json /
audit.json / drat-trim-audit.json、`~/workspace/kyouen-omp/tasks/w20-*-minimal/drat-trim.log`）
からの転記。

## 1. 原典との照合

各クラスの JSON を実読し、W20 ログの表と一致することを確認した。

| クラス (x,c,e) | vars | clauses | kept_edges | solver 判定 | solve 秒 | conflicts | proof 行数 |
|---|---|---|---|---|---|---|---|
| (0,0,1) | 9,258 | 76,370 | 53,882 | SOLVER_UNSAT | 1.3189757540000073 | 1,996 | 22,379 |
| (0,1,2) | 14,544 | 85,615 | 53,882 | SOLVER_UNSAT | 1211.1709459519998 | 992,331 | 2,143,709 |
| (1,0,2) | 13,220 | 82,976 | 53,886 | SOLVER_UNSAT | 15.096087751000027 | 24,595 | 790,206 |

チェッカー領収書（audit.json / drat-trim-audit.json 実読）:

| クラス | 増分チェッカー | drat-trim |
|---|---|---|
| (0,0,1) | VERIFIED, 8.10978877399998s, returncode 0, timed_out false | VERIFIED, 0.425s, exit 0 |
| (0,1,2) | タイムアウト, seconds 3600.106987784, timed_out true, verified false | VERIFIED, 249.726s, exit 0 |
| (1,0,2) | VERIFIED, 982.8090873230001s, returncode 0, timed_out false | VERIFIED, 4.998s, exit 0 |

drat-trim の内訳（各 drat-trim.log / drat-trim-audit.json より）:

| クラス | clauses in core | lemmas in core | total lemmas | resolution steps | RAT lemmas in core | redundant literals in core |
|---|---|---|---|---|---|---|
| (0,0,1) | 7,097 / 76,370 | 1,657 / 9,733 | 9,733 | 1,045,488 | 0 | 350 |
| (0,1,2) | 35,902 / 85,615 | 582,768 / 1,072,076 | 1,072,076 | 353,040,071 | 0 | 1,910,715 |
| (1,0,2) | 18,192 / 82,976 | 37,959 / 375,161 | 375,161 | 7,753,507 | 0 | 13,177 |

チェッカーの同定:

- 増分チェッカー `drat_check_incremental.cpp`（g++ -O2 -std=c++17）、ソース SHA-256
  `34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b`、
  バイナリ SHA-256 `5c164d07d4d25954cadf4b5ab8d11393655231e212af8ac85df748bfa3030f55`。
  全3クラスの audit.json で同一。
- drat-trim（https://github.com/marijnheule/drat-trim、commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`、`gcc drat-trim.c -std=c99 -O2 -o drat-trim`）、
  バイナリ SHA-256 `92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`。
- 入力 CNF の SHA-256: (0,0,1) `b827be623a4b7b43525929e1290e2a63678a5b2dd4f0f47488e82a27061ee108`、
  (0,1,2) `22e8b0fdbb448f5ef1a7b4eef25283123be55c9861f71226aad45207120d7e65`、
  (1,0,2) `2c880375426f6847f5447296f4b2d5865245e46b279f69ca333d34daa5604530`。
- 証明 DRAT の SHA-256: (0,0,1) `bb87ddf1ccabbb39066057715d9fab660c21e43fe4b400e928d7d5ebcaa080da`、
  (0,1,2) `0cb03ac31bb558bcbb60a448cb4effd4f509478ecf0c48d51192cebe27e6248d`、
  (1,0,2) `272991142ad886f9f5d69830c37b965e2a5e173df414aba44cb1ef906235379a`。
- edge 入力 SHA-256（全3クラス共通）: `4e17fe105f191f781192466d0775a59d3c341b16b267ebe372ba279911f67a72`。
- builder `search_shape_class.build` のソース SHA-256（全3クラス共通）:
  `989d291988992cc265a8caf77e6adf79248f4484783ec91252d5b72b31d2a611`。
- 生成器 `w20_drat_1322.py`: (0,0,1)/(1,0,2) は `5533a7430fa7950c15340508cdaf995f5475940cf44ad01c4df816e2f158c240`（両者同一）、
  (0,1,2) は `a0a0d5f03879c65f53c40a0fcc4a6a0da34aee9efcef77a0b263aa2980250eba`。

W20 ログとの相違点: W20 ログ「結果」節は (0,0,1) の増分チェッカー steps を
「audit.json に残っていないため引用しない」とするが、現存する
`class-001/audit.json` の `stdout` は `steps=9732 rup=9732 rat=0 rat_checks=0 deletions=5756 empty=1 ok=1`。
本ドラフトは JSON 実値を引用し、W20 ログ本文の当該但し書きとは食い違う点を記録する。

## 2. 新規 knowledge item ドラフト（仮番号 K0725）

ファイル名案: `research/knowledge/items/K0725-p2647-size1322-three-class-drat-audit.md`
（§3 の更新文案が張るリンクと同じ slug。統合時に採番し直す場合は slug も同時に更新）。
main 上の最大は K0724。統合時に採番し直す（AGENTS.md「K番号」）。

```markdown
---
id: K0725
title: p=2647 サイズ1322 の3形状クラス (0,0,1),(1,0,2),(0,1,2) は DRAT 監査済み
kind: verification
status: verified
topics: [maximum-safe, geometry, verification, certificates]
aliases: []
relations:
- type: verifies
  target: K0711
  note: 上界 A(2647)<=1322 のうち (1,1,3) を除く3クラスのソルバUNSAT主張
- type: depends_on
  target: K0720
  note: 禁止四点生成器の完全性（CNF構築の前提）
- type: depends_on
  target: K0706
  note: 同じ増分DRATチェッカーによる全1323 d監査の流儀
artifacts:
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/w20_drat_1322.py
  role: solver
  note: クラスごとに再開可能な solve+DRAT+監査ドライバ（Cadical195 with_proof）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/class-001/audit.json
  role: data
  note: (0,0,1) 増分チェッカー VERIFIED, returncode 0, 8.11秒。checker source/binary hash 付き
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/class-001/drat-trim-audit.json
  role: data
  note: (0,0,1) drat-trim クロスチェック VERIFIED, exit 0, 0.425秒
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/class-102/audit.json
  role: data
  note: (1,0,2) 増分チェッカー VERIFIED, 982.81秒
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/class-102/drat-trim-audit.json
  role: data
  note: (1,0,2) drat-trim クロスチェック VERIFIED, 4.998秒
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/class-012/drat-trim-audit.json
  role: data
  note: (0,1,2) drat-trim 単独監査 VERIFIED, 249.726秒（増分チェッカーは3600秒タイムアウト）
- path: research/log/2026-11-12-a2647-1322-drat-audit-omp.md
  role: log
  note: 方法・経緯・(drat-trim切替理由)・留保
scope: p=2647、size=1322 の形状クラス (x,c,e)=(0,0,1),(1,0,2),(0,1,2) の単体CNF。
各CNFの UNSAT 判定の独立DRAT監査に限る。クラス (1,1,3) と A(2647) の正確値を含まない。
evidence: 各クラスの CNF/proof の SHA-256 を JSON と照合し、増分チェッカー2クラス・drat-trim3クラスが
exit 0 と VERIFIED を返した。CNF/proof のバイト列は再生成可能（gz は mtime=0）。
---

## 検証内容

A(2647) <= 1322 を支える size-1322 の全4形状クラスのうち、(1,1,3) を除く3クラスについて、
Cadical195（with_proof）で UNSAT 判定と DRAT 証明を生成し、独立チェッカーで検査した。
証明は `output/w20-drat-1322/class-*/` に proof.drat.gz、CNF は input.cnf.gz として保持する
（バイナリのため push 対象外。SHA-256 は JSON に記録）。

- (0,0,1): 増分チェッカー `drat_check_incremental` VERIFIED（8.11秒）、
  drat-trim VERIFIED（0.425秒）。
- (1,0,2): 増分チェッカー VERIFIED（982.81秒）、drat-trim VERIFIED（4.998秒）。
- (0,1,2): 増分チェッカーは 3600 秒でタイムアウト（`timed_out: true`, `verified: false`）。
  drat-trim 単独で VERIFIED（249.726秒、exit 0）。このクラスは両チェッカーで検証したのではなく、
  drat-trim のみが領収書である。

drat-trim の backward checking はいずれも RAT lemmas in core 0（全 lemma が RUP で core に入る）。
CNF・証明の SHA-256 は audit.json / drat-trim-audit.json の記録と一致することを確認済み。

## 限界

- (0,1,2) は増分チェッカーでは未検証（タイムアウト＋VM再起動中断のみ）。領収書は drat-trim 単独。
- クラス (1,1,3) は対象外で未解決。UNSAT なら A <= 1321、SAT なら A = 1322。
- 証明バイナリは push 対象外。JSON の hash からバイト単位で再生成可能であることが前提。
- チェッカー実装（増分チェッカー、drat-trim）とコンパイラへの依存が残る。Lean 形式証明ではない。
```

## 3. K0706 更新提案

対象: `research/knowledge/items/K0706-p2647-no-parabola-equality-witness.md`、
本文「限界」第2項の第2文（現行74行目）。

現行文（置換対象）:

```
  [K0711](K0711-p2647-safe-lower-bound-1292.md) の独立検査済み1296点証人と合わせ、現在の最良の範囲は **1296 ≤ A(2647) ≤ 1322**（上界 1322 はサイズ1323 の全4形状クラス UNSAT・サイズ1324 の形状 (b) UNSAT による**ソルバ主張**）。**DRAT 監査済みの上界は 1324**（全1323 d の receipts、1323/1323 VERIFIED）で、1322 側は DRAT 監査前。
```

更新文案（この1文を次で置換。主張の強さは変えず、監査範囲を W20 の結果に合わせる）:

```
  [K0711](K0711-p2647-safe-lower-bound-1292.md) の独立検査済み1296点証人と合わせ、現在の最良の範囲は **1296 ≤ A(2647) ≤ 1322**。**DRAT 監査済みの上界は 1322**（サイズ1322 の形状クラス (0,0,1),(1,0,2),(0,1,2) は W20 で DRAT 監査済み、[K0725](K0725-p2647-size1322-three-class-drat-audit.md)）。ただし **クラス (1,1,3) は未解決**（UNSAT なら A ≤ 1321、SAT なら A = 1322）であり、上界 1322 のうち (1,1,3) を除く全クラスが監査済みである。全1323 d の receipts（1323/1323 VERIFIED）による上界 1324 も引き続き独立監査済みである。
```

- status: `computed` のまま変更しない（W20 は A ≤ 1322 の3クラス分の監査であり、
  A(2647) の有限計算としての監査範囲を 1324 から 1322 側へ拡張するが、(1,1,3) と
  正確値は未確定のまま）。
- title / scope / evidence は変更しない。本文の当該1文のみ置換。
- 候補の分岐（統合担当が選ぶ）:
  - 案A（推奨・上記）: 1文を「1322（(1,1,3) を除く全クラス監査済み）」へ更新し、
    (1,1,3) の未解決と 1324 側の監査済みを明記する。
  - 案B: 上ですり合わせず、`DRAT 監査済みの上界は 1324` を残したまま
    「ただしサイズ1322の3クラス (0,0,1),(1,0,2),(0,1,2) は別途 DRAT 監査済み（K0725）。
    (1,1,3) が未解決のため監査済み上界は 1324 のまま」と追記のみ行う。
    これは「(1,1,3) を含む形での監査済み最良上界は依然 1324」と読む立場。
    台集合 {〜1322 の3クラス監査済み ∧ (1,1,3) 未決} からは A ≤ 1322 は
    「3クラス分は監査済み」であり、A ≤ 1322 そのものは (1,1,3) に依存しない
    （クラスは排他の網羅分割）ため、案A が読み手の誤解を招きにくい。

### 3.1 他項目との整合（統合時に同時確認。K0706 以外は必須ではない）

W20 は「DRAT 監査済み上界」の数値を 1324 から 1322 側へ動かすため、
同じ語を引用する項目に食い違いが生じる。統合時に次の扱いを確認する。

- `K0097-integer-residue-parabola-bounds.md` 90・92行: `1296<=A(2647)<=1324`。
  92行を `1296<=A(2647)<=1322`（(1,1,3) を除く全クラス監査済み）へ更新するか、
  「DRAT 監査済み上界 1324、最良既知上界 1322」の二段表記にする。
- `K0711-p2647-safe-lower-bound-1292.md` 80・113・118行: 上界 1324 を
  「本項で独立監査済みとして採用した上界は 1324。単一CNFのDRAT監査による強化は今後の課題」
  と述べる。W20 がその「今後の課題」の一部（3クラス）を実施したため、
  118行の記述に K0725 への参照を追加し、「1322 側は (1,1,3) を除き DRAT 監査済み」と補う。
  title / scope / evidence の 1322/1296 は変更不要。status は `computed` のまま。
- `K0101-prime-parabola-equality-open.md` 84・101・117行: `A(2647)<=1324<1325` は
  A ≤ 1322 ≤ 1324 なので真。変更不要（反例の成立に 1324 で足りる）。
- `K0717-p2647-113-full-d-sweep-100k.md` 57-58行: 「1296 ≤ A ≤ 1322（ソルバ主張）、
  DRAT 監査済み上界は 1324 のまま」。(1,1,3) の掃引は範囲を動かさないため、
  「上界 1322 は (1,1,3) を除き DRAT 監査済み（K0725）」へ更新する。
- `K0724-assumption-unsat-drat-gap.md`: 変更不要（候補B の assumption-UNSAT を
  単体 DRAT へ落とす問いは、W20 のクラス CNF とは別経路）。

## 4. 統合チェックリスト

knowledge 構造を変更したため、AGENTS.md「統合前の確認」に従い統合後に実行する。

```sh
uv sync --locked
uv run --locked python tools/knowledge/check.py
uv run --locked python -m unittest discover -s tools/knowledge/tests
uv run --locked python tools/knowledge/build.py
git diff --exit-code -- README.md research/knowledge/generated
```

手順:

1. main の最新を fetch し、K0724 を超える新規項目と採番衝突を解消する
   （仮 K0725 と 3.1 の参照リンク・relation target を同時に更新）。
2. K0706 は §3 の1文置換のみ行う（title/scope/evidence/status 不変）。
   §3.1 の整合は統合担当の判断で最小限だけ実施し、変更した項目を記録する。
3. `check.py` で schema（必須 field・status_by_kind・relation の自己辺/循環禁止・
   artifact の実在 path）を検証する。
4. unittest と build.py を通し、`README.md` と `research/knowledge/generated` の
   diff が空（生成物が正本と一致）であることを確認する。
5. W20 の成果物自体（`w20-drat-1322/class-*/` の JSON、`w20_drat_1322.py`、
   W20 ログ、commit `549ce94b` の W20 監査コミット）が repo に存在することを
   artifact path として再確認する。input.cnf.gz / proof.drat.gz は push 対象外のため
   artifact にはせず、JSON の hash のみを参照する（本ドラフトの K0725 案はそう構成）。

## 5. 留保

- 本ドラフトの数値はすべて §1 のファイル実読による転記。W20 ログの秒数表示は
  小数第2位までの丸めであり、本ドラフトは JSON 実値（float 全桁）を引用した。
- K0725 案の artifact は repo 内に実在する追跡ファイルのみを指す。
  `class-012/` 配下の一時ディレクトリ（`w20-012-*`）と gz バイナリは未追跡のため
  artifact に含めない。
- 本ログは knowledge 項目を変更していない。統合作業は別タスク。

（完）
