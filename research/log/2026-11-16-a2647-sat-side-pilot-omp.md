# 2026-11-16 W32: SAT側パイロット S1 — pair状態空間局所探索の実装と浅い段パイロット

成果物は本logと、探索器・driver（新規ファイル）および新規出力ディレクトリのみ。
既存ファイルは変更していない。既存出力ディレクトリは上書きしていない。push なし。
knowledge 項目は編集していない。長時間の heavy solver は走らせていない（並走中の
(1,1,3) の CaDiCaL に干渉しないよう、局所探索は 1 プロセス逐次で実行）。

**結論（先頭に）: 違反 0 の割当は見つからなかった。** 11 d × 2 seed × 2 初期化
（warm / random）= 44 ラン各 10^6 flips すべてで、基数制約を満たす最良状態の
不充足 base 節数は 20〜44 の範囲に留まった。したがって W29 §3.3 の
candidate 変換 → 独立幾何検査の段には進んでいない。**これは UNSAT の根拠では
ない**（W29 §3.4 の境界: 見つからなかったことは UNSAT の証明ではない）。

## 0. 出典と前提

- 設計: `research/log/2026-11-16-a2647-sat-side-attack-design-omp.md`（W29）
  §2 の S1、§3 のパイロット計画、§3.4 の境界、§3.5 の出力・管理。
- 符号化: `research/experiments/parabola-ternary-selection-20261109/ternary_general.py`
  （三値・d固定、target=1322、empty_bound=3。base 節は `clauses_for_pair` が
  生成する 53,886 本の forbidden-quadruple 節）。
- 幾何検査器（未使用、W29 §3.3 用）: `research/experiments/parabola-local-repair-20261109/verify_subset.cpp`。
- ラダー出典: `research/log/2026-11-13-a2647-candidate-a-ladder-result-omp.md`
  （全段 UNKNOWN 11 d = 147, 188, 194, 488, 602, 703, 717, 1003, 1103, 1166, 1229）。
- 数値はすべて保存した JSON / ログからの転記。`[INFERENCE]` のみ推測。

前提の再確認（W29 からの転記）:
- 残っているのは「3M/10M/20M 全段 UNKNOWN の 11 d」。ラダー全体で SAT 0 件。
  (1,1,3) は SAT かもしれないし UNSAT かもしれない。UNSAT なら A(2647) ≤ 1321、
  SAT なら A(2647) = 1322。現在の範囲 1296 ≤ A ≤ 1322 は不変。
- W29 は d=147 の base CNF がラダー資産とバイト同一に再現できることを確認済み。
  本 W32 でも下記 §1 で 11 d すべての再現を追加確認した。

## 1. 実装

新規ファイル（既存ファイルは変更していない）:

- `research/experiments/parabola-ternary-selection-20261109/walksat.cpp`
  SHA-256 `1a3036f0389b22103d22df15847e6968f1e444770a6a70c235eb075ae993e315`
- `research/experiments/parabola-ternary-selection-20261109/walksat_pilot.py`
  SHA-256 `31209695ae18d6b83e37a2601cee5bf1f0e204aa4ae970c22f1de51741775190`

新規出力ディレクトリ（既存を上書きしない）:
`research/experiments/parabola-ternary-selection-20261109/output/walksat-pilot-20261116/`
に `eval-check.json`、`pilot-results.json`、`problem-d147-sample.txt` を保存。

### 1.1 探索器（walksat.cpp）

固定 d 三値CNFに対する多値 WalkSAT。基数制約（空 pair ≤ 3）は探索には使わず
（W29 §2 の S1 仕様どおり）、ペナルティとして扱う:

- 変数: free pair（`v = min(t, p-t) ∈ 1..h`, `v != d`、`h = 1323`）を 0..N-1 に
  再マップした 1,322 個。状態値は `0 = low`, `1 = high`, `2 = empty`。
- 節: base 53,886 節のみ。各節は `(pair, side)` の列。**節は必要条件の否定節**で、
  列挙された全要求が現在の選択と一致するときのみ違反（他の解釈は §1.3 で棄却済み）。
- 目的関数: `cost = VIOLCOUNT + λ · max(0, EMPTIES - 3)`。λ は既定 1000。
- 移動: 違反節から (違反数) の重み、または空 pair から (基数違反時 λ) の重みで
  抽選し、その pair の 3 値のうち cost 差分最小を選ぶ（noise=0.1 で一様ランダム）。
- best は penalized cost の最小で追跡（違反数のみではない）。cost 0
  (= 違反 0 かつ 空 ≤ 3) に到達したら即 stop し witness 候補を保存。

初期状態は W29 指定どおり、warm 候補（1,292点）の変換とランダム（seed 固定）を
ランごとに分けて実行（再起動ごとの交互ではなく、44 ランのうち warm 22 / random 22）。

### 1.2 出力形式

- 探索器 stdout 最終行: `{"base_violations_best", "empties_at_best", "best_step",
  "final_violations", "final_empties", "flips", "lambda", "bound", "noise",
  "seconds", "solved"}`。`--trace-every` 指定時は `trace <step> <viol> <empties>`
  行を先に出力。
- `--eval <state>` は与えた状態の (violations, empties, penalty, cost) を JSON で出す。
- best 状態は `--best-state` に保存。

### 1.3 探索器の違反意味論と設計上の訂正（重要）

初回実装では Python 側の literal 検査器が節を「どの literal も満たされないとき違反」
と解釈していたが、base 節は必要条件の否定節であり、正しくは**列挙された要求が
すべて成立するとき違反**。この取り違えにより warm 候補（幾何的に正当な 1,292 点）で
walker=0 に対し literal=384 という不一致が出た。literal 検査器を
「全要求成立で違反」に修正したところ三者一致した（§2）。決定版の意味論:

- 節 literal `+v` = 「pair v が low を要求」、`-v` = 「pair v が high を要求」。
- 節は全要求が現在の選択と一致するとき違反。walker・literal 検査器・encoded 検査器
  はこの規約で一致する。

さらに pilot 初回実行（λ=1.0）では、空 pair 化で違反を消せるため walker が
viol=0 / 空≈530（基数制約を大きく超過）へ自明に落ちた。これは有効状態ではない。
λ を 1000（ペナルティが違反数を支配）に上げ、best 追跡を penalized cost 最小に
変えたところ、全ランで 空 ≤ 3 を維持したまま違反数が 20〜44 に留まる、意味のある
局所探索になった。λ=1.0 の結果は探索として無効なので破棄した。

## 2. 評価器の正確さ検証（探索前に実施）

W29 の要求どおり、探索に進む前に探索器の違反数が対応する CNF 割当の不充足節数と
一致することを確認した。方法は 3 系統の独立計算の一致:

1. `walksat.cpp --eval` が数える base 違反数（節の全要求一致数）。
2. Python の literal 検査器 `count_violations_literal`（base 節を直接、`clauses_for_pair`
   の要求意味論で評価）。
3. Python の encoded 検査器 `count_base_unsat_encoded`（`ternary_general.encode` した
   三値 CNF の先頭 53,886 節 = base の不充足節数を、CNF 変数空間で評価）。

さらに、再生成した base 節列がラダーで保存済みの CNF と同一であること
（`clauses[:53886] == saved_cnf[:53886]`）を各 d で確認した。

- d ∈ {147, 188, 194, 488, 602, 703, 717, 1003, 1103, 1166, 1229} の 11 d。
- 各 d について warm 変換 1 状態 + ランダム seed {1,2,3} × 3 状態 = 10 状態。
- 計 110 状態で、walker 違反数 == literal 違反数 == encoded 不充足節数、かつ
  walker の空数 == Python の空数。**全 110 状態で一致（all_ok=true）**。
- 保存済み CNF との base 接頭辞一致: 11 d すべて true。
- 結果: `output/walksat-pilot-20261116/eval-check.json`。
  `{"all_ok": true, "states_total": 110, "saved_cnf_prefix_match": 全 true}`。

注: warm 候補（1,292 点）の変換はそのままでは 空 = 33 で target=1322 に足りない
（1,292 + 33 = 1325 = h + 2）。これは仕様どおり warm は初期状態（位相ヒント）であり、
最終 witness 候補ではない（§3）。

## 3. パイロット実行（浅い段）

- 対象: 難所 11 d（147, 188, 194, 488, 602, 703, 717, 1003, 1103, 1166, 1229）。
- 各 d: warm × seed{1, 20261109} と random × seed{1, 20261109} の 4 ラン、各 10^6 flips。
- 合計 44 ラン。λ=1000, noise=0.1, bound=3。
- 結果: `output/walksat-pilot-20261116/pilot-results.json`（trace 込み）。

### 3.1 実測速度

- flips/s: 最小 128,684 / 中央値 166,991 / 最大 216,955（44 ラン）。
  Python 単体ではなく C++ 実装なので実行可能。1 ラン 10^6 flips は約 5〜8 秒。
- 44 ラン合計で約 283 秒（wall）。

### 3.2 d ごとの最良違反数（基数制約 空 ≤ 3 を満たす状態での最小）

| d | warm best | random best | d の最良 |
|---|---|---|---|
| 147 | 22 | 27 | 22 |
| 188 | 27 | 33 | 27 |
| 194 | 24 | 24 | 24 |
| 488 | 25 | 21 | 21 |
| 602 | 20 | 24 | 20 |
| 703 | 28 | 28 | 28 |
| 717 | 21 | 25 | 21 |
| 1003 | 27 | 27 | 27 |
| 1103 | 28 | 30 | 28 |
| 1166 | 20 | 29 | 20 |
| 1229 | 28 | 31 | 28 |

全 44 ランで `solved = false`。違反数の全体分布: 最小 20 / 中央値 28 / 最大 44。

### 3.3 収束の観察

- best_step（最良 cost に到達した step）: 最小 257,964 / 中央値 714,676 /
  最大 982,983。44 ラン中 8 ランで best_step > 900,000。
- trace の平均違反数は 100k step 時点で ≈ 55、1M step 時点で ≈ 48。
  つまり 10^6 flips の範囲では探索は収束しきっておらず、予算を増やす余地がある
  `[INFERENCE]`。ただし残差（20〜44）は baseline（ランダム状態の代表値）より
  はるかに小さいので、探索は有効に効いている。
- 空数は常に 3（bound ちょうど）に張り付き、基数制約が実効的な拘束として働いた。

### 3.4 解釈（W29 §3.4 の境界）

- 違反 0 の割当は見つからなかった。**これは UNSAT の根拠ではない**（W29 §3.4）。
- 得られた「最良違反数 20〜44」は探索が到達した局所最良の値であり、幾何的量でも
  到達不能性の証拠でもない（W13 §2.4 の留保の継承）。
- したがって (1,1,3) の status は依然 UNKNOWN。A(2647) の範囲 1296 ≤ A ≤ 1322 は不変。
- W29 §3.3 の candidate 変換 → 独立幾何検査には進んでいない（違反 0 が出ていないため）。

## 4. まとめと次への材料

- S1 の探索器を実装し、評価器を 110 状態 × 3 系統で検証（全一致、保存 CNF とも
  11 d で接頭辞一致）。探索器の違反意味論の誤りと λ=1.0 の自明解問題を特定・修正
  （§1.3）。
- 11 d × 2 seed × 2 初期化、各 10^6 flips のパイロットで違反 0 は得られなかった。
  最良違反数は 20〜44、速度は ≈ 1.3〜2.2×10^5 flips/s。
- 10^6 flips では収束途中（best_step が上限付近のランが多い）。深い段（10^8 flips
  級）に進めるなら、λ・noise の調整と再起動戦略の検討が次の材料になる `[INFERENCE]`。
- 本パイロットは浅い段であり、成功（違反 0）も UNSAT も主張しない。ラダーと同様、
  SAT 0 件の追加に留まる。
(完)
