# n9-ge19 lane part2: min(S) prefix-chunk resume infrastructure for the ksearch system (2026-11-20)

単一オーナー宣言: `research/log/2026-11-20-n9-ge19-k9-upper-decision-single-owner-note.md`
(commit `21f8610464d2711f768b5764d23b21a40295dee5`)。本 part はその手法 (a)
「専用の完全探索器（… min(S) 場所分割チャンク・記録ファイルによる resume 対応）」の
実装と制御群である。part1 (`0afda0e6` / `9a1c7a98`) に続き、判定そのものへの主張は
本 part では一切しない（INDET 継続）。

## 背景

part1 の再開手順 4: ksearch 系は n7-15 を fresh 再現済みだが n8-16 は 220s/518M nodes で
INDET、単発実行では bash cap 300s の壁を越えられない。宣言方法 (a) どおり、探索空間を
「選択済み最小 m セル」の prefix で完全分割し、chunk ごとに honest cap つきで走らせ、
cap に当たった chunk は子へ展開する（子全体で親の空間の完全・素な分割）、記録は
append-only JSONL でプロセスをまたいで resume する。

## 成果物

- `scripts/ksearchp.js` (ksearch v3d): v3c と同一エンジン＋ `--prefix=p1,...,pm` 汎用化。
  chunk = 「m 個の最小選択セルがちょうど p1..pm である size-target 選択集合」の空間に
  探索を制限する。`--min=c` は `--prefix=c` と等価（1 要素 prefix）。ban/fix/飽和未来禁止
  の意味論は v3c の minc ブロックの自然な反復で、fix 時の飽和曲線チェック・cnt==2
  bucket2 積み上げも同一。
- `scripts/chunker.js`: chunker driver。run mode（FIFO frontier、cap と wall の予算管理、
  append-only 記録、capped chunk の子展開、SAT witness 記録）と audit mode
  （記録から chunk 木を走査し、全 feasible 葉が uncapped UNSAT レコードを持つこと・
  SAT レコード不在を機械検証する完了証明ゲート）。
- `results/chunk-resume-controls-20261120.json`: 制御群 V1..V6（下記）の生の出力。
- `results/n7t15-partition-records.jsonl`: n=7 target=15 の分割閉鎖に使った記録そのまま。

## 制御群（すべて PASS、`chunk-resume-controls-20261120.json` 参照）

- **V1 prefix/min 恒等性**: n8-16 `--min=0` と `--prefix=0` を `--maxnodes=10000000` で
  比較、sat/nodes/capped/boundChecks/boundPrunes 全フィールド一致（nodes=10,000,001、
  節点上限キャップは決定的）。一般化が v3c の意味論を保存することの直接検証。
- **V2 非チャンク部分の不変性**: n7-15 whole が published v3c 制御値と完全一致
  （nodes 11,880,598 / boundChecks 9,096,190 / boundPrunes 1,563,258 / UNSAT）。
- **V3 SAT chunk witness**: n7 target=14 prefix=[0] が SAT、witness 14 石（published W7
  に一致）を第三系 eval_strong.js + 独立 det4 全組再検査で WITNESS-SAT。
- **V5 n7-15 完全分割閉鎖**: min(S) chunk c=0..34（35 chunk、c≧35 は計数により不能で
  列挙範囲外）をすべて fresh 完走、全 UNSAT。audit PASS（complete, all_unsat, open_leaves 0）。
  chunk 総 nodes 11,880,562 は whole 探索 11,880,598 と一貫（差 36 = root 計上差）。
  resume 経路も実測検証（wall 25s で budget-stop した後、再開呼び出しで完走）。
- **V6 tamper ネガティブ制御**（レコード冊の改竄検出）: (a) 1 レコードを capped/sat=null
  に改変 → audit が open_leaves 28・complete:false で捕捉。(b) 偽 SAT witness 注入 →
  audit が all_unsat:false・sat_records で捕捉。audit の完了判定が fail-closed である
  ことを機械確認。
- audit の決定性: 同一 state に対する audit 2 回の出力は ts を除く全フィールドで一致。

## n8-16 への適用（本 part の次段、進行中）

n8-16 (K_8=15 上界の再現、宣言の必須較正) を同一 driver で走らせる。part1 測定の
chunk [0] ≧70.8M nodes/140s、chunk [1] ≧35.1M nodes/70s はいずれも cap 未満で未完、
driver の子展開 [0,d], [1,d] ... が対象。プロセス毎の census 再構築（n8 で ~0.5s）を
除けば、子展開は親部分木の仕事量を保存する。全葉が閉じ、audit が complete/all_unsat
を返した時点で初めて n8-16 UNSAT を lane 実験記録に反映する（それまでは INDET 記録のみ）。
n9-19 本体は n8-16 の完了後に同一 driver の n=9 拡張として別段階で着手する
（必要な prefix 段数と総工作量は n8-16 の chunk 統計から見積もる）。

## 制約の明示

- ksearchp/chunker いずれも無作為性なし・決定的。chunk verdict は cap に当たった場合
  一切採用しない（sat=null のまま破棄扱い）。
- n8-16 で1つでも SAT chunk が出た場合は whole 判定として SAT を記録し、witness を
  eval_strong + det4 で独立検証してから出版する（宣言の受入条件 2・4 どおり）。
