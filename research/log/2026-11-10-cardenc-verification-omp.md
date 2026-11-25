# 2026-11-10 W15: pysat CardEnc (seqcounter) の小規模全件検証

W10（`2026-11-10-a2647-113-candidate-b-proof-omp.md`）の前提(3)の検証。
成果物: 本log、`research/experiments/parabola-p2207-no-equality-witness-20261107/cardenc_verify.py`、
`.../output/w15-cardenc-verify.json`。既存ファイルは変更していない。commit / push なし。

## 第1部: `build()` における CardEnc の使用箇所（実読・行番号つき）

`research/experiments/parabola-p2207-no-equality-witness-20261107/search_shape_class.py`
の `build(p, edges, x, c, e)`（:34-74）より、該当箇所は次の2つのみ。

```
47:    top = 4 * h
48:    both = [v(i, "B") for i in range(1, h + 1)]
49:    none = [v(i, "N") for i in range(1, h + 1)]
50:    card_b = CardEnc.equals(lits=both, bound=c, top_id=top, encoding=EncType.seqcounter)
51:    clauses.extend(card_b.clauses)
52:    card_n = CardEnc.equals(lits=none, bound=e, top_id=card_b.nv, encoding=EncType.seqcounter)
53:    clauses.extend(card_n.clauses)
54:    aux = card_n.nv
```

すなわち:

| 変数集合 | 主変数 | 演算 | bound | EncType | top_id |
|---|---|---|---|---|---|
| `both`（B = 完全対） | `v(i,"B") = 4i-3`、i=1..h | `CardEnc.equals` | `c` | `seqcounter` | `4h` |
| `none`（N = 空対） | `v(i,"N") = 4i-2`、i=1..h | `CardEnc.equals` | `e` | `seqcounter` | `card_b.nv`（前の制約の最大変数） |

補助変数は `top_id` / `.nv` の連鎖で 4h より上に確保され、点上界の変数 `aux + t`
（:59）は `aux = card_n.nv`（:54）から始まる。つまり **CardEnc の `.nv` の値が
後続の変数番号空間の開始点を決める**（`.nv` が過小だと節の変数と点変数が衝突する）。
`atmost` / `atleast` は `build()` では直接呼ばれていない（`equals` の内部で両方が
呼ばれる。pysat 1.9.dev21 の `CardEnc.equals` 実装は
`atleast(...)` → `atmost(..., top_id=res1.nv)` の順で呼び、`nv = max(nv1, nv2)` を返す）。

### 候補B証明のどこに効くか

W10 第1部 補題1（`research/log/2026-11-10-a2647-113-candidate-b-proof-omp.md`）は
点集合のサイズを

  `|S(M)| = x + 2·#B + 1·(#L+#H) = x + 2c + (h-c-e) = x+c+h-e = size`

と計算する。ここで `#B = c` と `#N = e` は **上記2つの `CardEnc.equals` が強制する
性質そのもの**である。したがって

- `equals(both, c)` の符号化が「ちょうど c 個」を強制しない（緩い／厳しい）と
  補題1 のサイズ計算が崩れ、クラス CNF のモデル集合が「サイズ size の安全集合」
  と一致しなくなる。UC 探索のクラス列挙（`e = x+c+h-size`）と SAT/UNSAT 判定の
  意味が変わる。
- `.nv` の連鎖が誤っていると、点変数 `aux+t` や禁止四点節が CardEnc 補助変数と
  番号衝突を起こし、CNF の意味自体が壊れる（別制約への意図しない連結）。

`build()` はこの2制約以外に基数制約を使わないため、前提(3)の検証対象は
「`EncType.seqcounter` の `equals` が (i) 主変数上でちょうど bound 個を強制し、
(ii) 補助変数領域を主変数より上に正しく確保する」ことに尽きる。

（以下、第2部に続く）
## 第2部: 検証スクリプトと方法

`research/experiments/parabola-p2207-no-equality-witness-20261107/cardenc_verify.py`
（新規、既存ファイルは変更していない）。pysat 1.9.dev21、実行は
`uv run --locked --with python-sat python cardenc_verify.py --nmax 12 --joint-nmax 7`。

### 2.1 何を作ったか

`build()` と**同じ** pysat 呼び出し形（`CardEnc.equals(..., encoding=EncType.seqcounter)` を
`top_id` 連鎖で2回）で CNF を作り、主変数の**全割当**について

  「CNF が補助変数への拡張を持つ」 ⇔ 「主変数の真の個数がちょうど bound」

を照合する。4種の variant を回した:

| variant | 主変数 | 制約 | 主割当数/ケース |
|---|---|---|---|
| `contiguous` | `1..n`、`top_id=n` | `equals(bound=k)` | `2^n` |
| `strided` | `4i-3` (i=1..n)、`top_id=4n`（`build()` の BOTH と同じ添字） | `equals(bound=k)` | `2^n` |
| `chained` | `4i-3` と `4i-2`、`top_id=4n` と `card_b.nv` | 2本の `equals(bound=k)` | `2^n`（両集合を同時固定） |
| `joint` | 同上 | `equals(both,c)` → `equals(none,e)`、**c と e を独立** | `4^n` |

`joint` が `build()` の使われ方（`c` と `e` はクラス式 `e = x+c+h-size` から別々に来る）
をそのまま写したもの。`strided`/`chained`/`joint` は、`build()` の変数番号体系
（`v(i,"B")=4i-3`、`v(i,"N")=4i-2`、補助変数は 4h より上）で同一の符号化が成り立つかを
確かめるために置いた。`c > e` と `c < e` の両方が全件に含まれる。

### 2.2 拡張可能性の判定方法（2系統・独立）

各主割当 X について、補助変数だけを自由にして充足可能性を2通りで判定した:

1. **自前 DPLL**（`cardenc_verify.py` 内の `dpll_sat`）: 単位伝播＋分岐の探索を
   このスクリプト内で実装。pysat のコードは一切使わない。
2. **Cadical195**: 主変数を `assumptions` で固定して `solve()`。ソルバは1ケースにつき
   1インスタンスを使い回す。

判定規則: 2系統が一致し、かつその値が真値 `#true == k`（`joint` では
`#both == c and #none == e`）と異なるときだけ「不一致」として記録する。
2系統が食い違った場合は `checker-disagreement` として別種に記録する（今回 0 件）。

**手法の限界を明記**: 拡張可能性を「補助変数への拡張が存在する」と判定するのは
上記2つの完全ソルバによる。DPLL は完全（全分岐を尽くす）なので、これは
「CNF の充足可能性」そのものの判定であり、近似ではない。ただし主変数の固定に
`assumptions` を使う Cadical 側は、ソルバの正しさを仮定している（相互チェックの
片翼）。DPLL 側はその仮定を共有しない。

### 2.3 ハーネス自体の負の対照

検出器が実際に誤りを捕まえるかを確かめるため、`k` の代わりに `k+1` で符号化した
CNF を真値 `#true == k` と比較する負の対照を回した（`negative_control`）。
結果は JSON の `negative_control` に記録。不一致が 0 件でないことを確認している
（＝「全件一致」はハーネスが何も見ていないだけ、ではない）。

### 2.4 結果

（末尾の実行ログを参照。数値は `output/w15-cardenc-verify.json` に一致）

（以下、第3部に続く）

## 第3部: 結論

### 3.1 検証結果の総括（`output/w15-cardenc-verify.json` の実読値）

`§2.4` が参照する「末尾の実行ログ」は本logには保存されておらず、JSON にも
stdout は含まれない。したがって以下は JSON の `records` を直接集計した値である
（`total_cases` / `total_assignments` / `total_mismatches` はトップレベル値とも一致）。

| variant | cases | n の範囲 | assignments | mismatches | 主割当の真値分割 |
|---|---|---|---|---|---|
| `contiguous` | 90 | 1..12 | 98,304 | 0 | SAT 8,190 / UNSAT 90,114 |
| `strided` | 90 | 1..12 | 98,304 | 0 | SAT 8,190 / UNSAT 90,114 |
| `chained` | 90 | 1..12 | 98,304 | 0 | SAT 8,190 / UNSAT 90,114 |
| `joint` | 203 | 1..7 | 1,293,728 | 0 | SAT 21,844 / UNSAT 1,271,884 |
| **合計** | **473** | — | **1,588,640** | **0** | SAT 46,414 / UNSAT 1,542,226 |

- ケース集合は欠落なし: 単体3種は `{(n,k) : 1<=n<=12, 0<=k<=n}`（90 = Σ(n+1)）を
  すべて含み、`joint` は `{(n,c,e) : 1<=n<=7, 0<=c,e<=n}`（203 = Σ(n+1)²）を
  すべて含む。`incomplete` は空配列、`joint_complete` は `true`。
  `seconds` = 314.01。
- 不一致は SAT 側・UNSAT 側の**両方向**で 0: `ok` の合計が `assignments` の合計と
  一致し、真値が SAT の 46,414 件も UNSAT の 1,542,226 件も「CNF の拡張可能性」と
  一致した。片側だけの一致ではない。
- 構造不変量も全 473 ケースで 0: `aux_alias_main`（補助変数が主変数以下に落ちる件数）
  = 0、`lit_above_nv`（`.nv` を超えるリテラル）= 0。すなわち (i) 補助変数は常に主変数
  より上に確保され、(ii) 節は申告された `.nv` の範囲内に収まる。`build()` が
  `top_id=card_b.nv` で連鎖させ、`aux = card_n.nv` から点変数 `aux+t` を振る設計は、
  この2条件が成り立つ限り番号衝突しない。
- `joint` の bound 被覆: `c>e` 84 件、`c<e` 84 件、`c==e` 35 件。`build()` が
  `e = x+c+h-size` で c と e を独立に与える使い方を、両順序とも全件で覆っている。
- 最大規模: 単体 `chained` n=12,k=6 で vars 192 / clauses 288、`joint` n=7 で
  vars 76 / clauses 96。全ケースが主変数の全割当を尽くす（DPLL は完全）。

### 3.2 前提(3)はどこまで格上げできるか

W10 §1.7 の前提(3)は「pysat `CardEnc.equals`（seqcounter）の健全性・完全性は
外部ライブラリの性質であって、本証明では前提とする」だった。本検証により、
**使用している pysat 1.9.dev21 の `EncType.seqcounter` における `equals` について、
次の範囲では前提ではなく検証済み事実として扱える**:

- 単体: n <= 12、k = 0..n の全件、主変数の全 2^n 割当。
- 連鎖（`build()` の呼び出し形そのまま、c と e 独立）: n <= 7 の全件、全 4^n 割当。
- 内容は (i) 主変数上でちょうど bound 個を強制すること、(ii) 補助変数領域が主変数
  より上に確保され `.nv` が実際の最大変数以上であること、の両方。

したがって前提(3)の格上げ表現は「**小規模（単体 n<=12、joint n<=7）で全件検証済み**」
までが正確で、「検証済み」を無条件に書くのは誤り。残るギャップは次の通り。

1. **一般 n の証明ではない。** 本検証は有限個の事例の全件照合であって、任意の n に
   対する seqcounter 符号化の健全性・完全性の証明ではない。実際に `build()` が使う
   のは `h = (p-1)//2` で、対象 p=2647 では **h = 1323**。検証済みの n=12 とは
   2桁以上離れており、この外挿は「同じコード経路がより大きい n でも同じ意味を
   実装している」という一様性の仮定に立つ（[INFERENCE]、サイズ依存の分岐が
   符号化ループ以外に無いことを実装から読んだうえでの判断）。
2. **一般 n の保証はライブラリ側に依存したまま。** seqcounter（Sinz 型の逐次カウンタ）
   の正しさは pysat の実装とその文献に帰属する。本検証が縮めたのは「この版のこの
   符号化が意図どおり動くか」という不確実性であって、「任意 n で正しい」という
   命題を repo 内で証明したわけではない。W10 §1.7 の前提(3)の文言を「一般 n は
   ライブラリ依存」に書き換える必要はなく、そこに「小規模全件は検証済み」を
   併記するのが正確。
3. **対象は `equals` + `seqcounter` のみ。** `atmost` / `atleast` の直接呼び出し、
   他の `EncType`、bound が負・n 超の異常入力は本検証の範囲外（`build()` は
   `equals` しか呼ばないため実害はない）。`chained` variant は両集合に同じ k を
   置いた補助形で、c と e が独立な本番形は `joint`（n<=7）が担う。
4. **前提(4)（ソルバの健全性）は本検証で縮まない。** Cadical 側は assumption の
   意味論を仮定しており、DPLL との一致は「2つの完全判定器が同じ結論を出した」
   ことしか保証しない。UNSAT 側の監査可能性は依然 W10 第2部の DRAT 計画に依存する。

### 3.3 負の対照が保証するもの（および本 JSON での欠落）

負の対照は「ハーネスが誤りを見逃さないか」の確認である。`cardenc_verify.py:269` の
`negative_control` は、真値 `#true == k` に対して **`bound=k+1` で符号化した CNF** を
照合する。符号化が正しければこの2つは食い違うので、**不一致が 1 件以上出ること**
自体が「照合器が符号化の誤りを検出できる」ことの証拠になる。逆に不一致 0 件なら、
「全件一致」は符号化の正しさではなく照合器が何も見ていないことの反映かもしれない。
つまり負の対照が保証するのは**検出力**であって、符号化の正しさではない。両者は
独立で、負の対照が通らなければ 3.1 の 0 件は意味を持たない。

**ただし、保存済み JSON にこの証拠は無い。** `w15-cardenc-verify.json` の
トップレベルキーは

  `script, pysat_encoding, verified_encoder, method, nmax, joint_nmax, joint_complete,
   variants, scope_note, total_cases, total_assignments, total_mismatches, incomplete,
   seconds, records`

であり、`negative_control` キーは存在しない（ファイル内に "negative" の文字列も 0 回）。
`cardenc_verify.py` の `main()` は `neg = negative_control(min(args.joint_nmax, 6))` を
計算し `report["negative_control"] = neg` として書き出す実装になっているので、
保存物はこのキーを持つ版より前に生成されたか、キーが落ちた版で上書きされたと
考えられる（[INFERENCE]）。いずれにせよ **`detected_mismatches` の実値を本logに
書くことはできない**。§2.3 の「結果は JSON の `negative_control` に記録」は
現存ファイルについては成立していない。

したがって現状の証拠状態は:

- 符号化の正しさ（3.1）: JSON に実値あり、2系統の完全判定器で裏づけ。
- ハーネスの検出力（3.3）: **保存された証拠なし**。主張だけが §2.3 に残っている。

この欠落は「新しい計算をしない」という本タスクの制約下では埋められない。
埋めるには同じ `--joint-nmax 7` で再実行し `negative_control` を含む JSON を
残す必要がある（スクリプトは既にその形で書かれている）。本タスクでは
再実行せず、欠落として記録するに留める。

### 3.4 結論

- `CardEnc.equals(..., encoding=EncType.seqcounter)` は、`build()` と同一の呼び出し形・
  同一の変数番号体系のもとで、単体 n<=12・連鎖 n<=7 の**全主割当**について
  「CNF が補助変数へ拡張可能 ⟺ ちょうど bound 個」を満たした（不一致 0 / 1,588,640 割当、
  473 ケース、SAT・UNSAT 両側）。補助変数の主変数への混入と `.nv` 超過も 0。
- よって W10 前提(3)は「外部ライブラリの性質として前提」から
  **「小規模全件（単体 n<=12、joint n<=7）で検証済み」** へ格上げできる。
  一般 n（実用の h=1323 を含む）の正しさは依然として pysat 実装とその文献に依存し、
  本検証はその外挿を支持するが証明しない。前提(4)（ソルバ健全性）は変化なし。
- 負の対照は「ハーネスが誤りを検出できること」を保証するもので、符号化の正しさを
  保証しない。そしてその証拠は現存 JSON に保存されていないため、§2.3 の主張は
  現物に裏づけられていない。これは本logの残欠陥として明示する。

（完）
