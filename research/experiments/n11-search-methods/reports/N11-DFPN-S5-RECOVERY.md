> **実験一次資料**：本文の判定・数値・計画は記録時点のものです。現在の結論・未解決・検証境界の唯一の正本は[knowledge](../../../knowledge/README.md)です。この資料を現在知識の正本として並行更新しません。

# s5 verdict cache の回収、coordinator の永続化、s4 certificate manifest

**11x11: UNKNOWN**

- base commit: `bdbcb42`
- scripts: `dfpn_s5_recover.py`, `dfpn_s5_replay_check.py`,
  `dfpn_s4_manifest_verify.py`, `dfpn_canonical_xcheck.py`
- 対象: first=60, r2=0

## 1. 発見: 前回の pilot は証明を捨てていた

`N11-DFPN-COORDINATOR.md` は class 481 を LOSS と証明し、
secured 4 → 10 と記録した。しかし **`--s5-cache-out` が当时的
`run_coord` に無かったので、その run が確定した 158 個の s5 verdict は
プロセス終了と共に消えた。**

`--coord` は `--s5-cache` を読むが **`--s5-cache-out` を受け付けず**、
`s4_cache_save()` は呼び出し元が無く、`s4_cache` には一度も要素が
入っていなかった。つまり manifest の writer は **dead code** だった。

実測（`logs/s5cache/s5_verdicts.csv` は 10月2日 12:27 で凍結、
`logs/coord/pilot.txt` は 10月3日 16:40）:

```
$ ls -la logs/s5cache/ logs/coord/
-rwxrwxrwx 2944 10月  2 12:27 s5_verdicts.csv     <- 10月3日の pilot より前
-rwxrwxrwx 35521 10月  3 16:40 pilot.txt
```

pilot.txt の `[q-done]` 行には canonical key と決定済み verdict が
残っており、**419M nodes を再実行せず証明を回収できる**。

## 2. 回収（`dfpn_s5_recover.py`）

```
log verdicts        : 158  (WIN=0 LOSS=158 UNKNOWN_dropped=0)
interrupted queries : 1  (no verdict line, dropped)
already in cache    : 0
new to the cache    : 158
MERGE_OK
```

- **158 件すべて LOSS**、`result=0`（UNKNOWN）は 0 件
- 最後の `[q-start] q=477` に対応する `[q-done]` が無い = 中断。
  **verdict 行の無い query は捨てる**（budget 切れは保存してはいけない）
- 既存 103 件と **key overlap 0**。同一 key の異 verdict はない

回収した cache を正式 file ではなく **worker file** に書く。
複数 worker が同じ CSV へ直接 append してはいけないという
`N11-DFPN-COVER-OPTIMUM.md` の手順どおり。

## 3. 独立検証：cold replay（`dfpn_s5_replay_check.py`）

回収した verdict を**信用しない**。4 shard に分けて
`--exact-replay` で**空の transposition table から 261 件すべて再証明**した
（`run_exact_replay` は行ごとに fresh solver を作る）。

```
merged replay rows: 261
cache entries    : 261
replayed         : 261
agree            : 261
DISAGREE         : 0
undecided replay : 0
not replayed     : 0
VERIFY_OK
```

**261/261 が独立に再現した。** node 数は一致しないが（warm table 対 cold）、
比較しているのは verdict だけ。

conflict 監査（重複・異 verdict・overlap）:

```
duplicates: 0
conflicting keys: 0
overlap: 0
verdict distribution: 261 LOSS
MERGE_CLEAN
```

## 4. 回収だけで到達した状態

同じ 3396 class・同じ 119 頂点で、**新規探索 0** なのに:

| cache | secured | classes used |
|---|---:|---:|
| 旧 103 件 | 4/119 | 1 |
| **回収後 261 件** | **10/119** | **2** |

`--coord-max=0`（探索しない）の class table で class 481 が
`unknown_s5=4 → 0, UNKNOWN → LOSS` に変わったことを確認した。

```
s4table,480,...,4,2,UNKNOWN,...        <- 旧 cache では 2 child 未決
s4table,481,...,6,0,LOSS,6,10,66,...  <- 回収後 0 child 未決、LOSS で確定
```

**これは 419M nodes の再計算なしで、class を閉じたことを意味する。**
coordinator の「unknown s5 が少ない class を優先」則が
<p>回収した cache に対して正しく機能した証拠でもある。

## 5. coordinator の永続化（コード変更）

`run_coord` に欠けていた 2 つを埋めた。

**(a) verdict の保存** — `--s5-cache-out` と `--s4-cache-out` を追加。
保存は class loop の**後**、`# done` の**前**に行う。
これが §1 の穴で、報告と保存の間に落ちるとまた証明を捨てる。

**(b) certificate manifest の実装** — `s4_cache_record()` を追加。
manifest は **class 単位**で、その class の全 raw edge の
合法 fifth move の canonical key を**全部**載せる：

```
s4verdict,first,r2,key_lo,key_hi,result,n_child,cov_size,child_lo,child_hi,...
```

`first`/`r2` が要るのは、canonical key だけだと
**どの edge class なのか分からず**、検証側が coverage も合法手も
再計算できないため。`cov_size` は「その class が refute する第三手の数」で、
再計算した coverage と一致するかを確認できるようにした。

**(c) class table の dump** — `--coord-max=0` でも全 3396 class の
key・coverage・raw edge を出力する（探索はしないのでfree）。
これがないと検証側は「その run がたまたま決定した class」しか検査できず、
canonical key の規約を照合する手段がない。

## 6. canonical key 規約の照合（`dfpn_canonical_xcheck.py`）

Python 検証側が C++ と**同じ key 値**を出せることは自明ではない。
`canonical()` は 8 個の bitmask の最小値を `(hi, lo)` 順で取るので、
**ソート済み index 列の min を取る D4 正規化とは別の値**になる。

`build_maps()` の 8 変換表を Python 側に再現して照合した：

```
root                 : {60,0}
classes in dump      : 3396
classes recomputed   : 3396
key mismatches       : 0
coverage mismatches  : 0
edge-list mismatches : 0
CANONICAL_AGREE
```

key・coverage・edge list すべてが一致。この照合が成立するので、
検証器は C++ が書いた manifest をそのまま検査できる。

## 7. s4 certificate manifest の独立検証（`dfpn_s4_manifest_verify.py`）

class 481（LOSS）と class 482（WIN）の manifest を、
盤面から再計算した子集合と s5 cache で検査：

```
manifest entries : 2
  s4 key=1152921504606848001,4 root={60,0} result=LOSS cov=6 children=106 edges=4 win_edges=0 loss_edges=4
  s4 key=1152921504606848001,8 root={60,0} result=WIN  cov=6 children=111 edges=4 win_edges=4 loss_edges=0
classes verified  : LOSS=1 WIN=1
children checked  : 217
MANIFEST_VERIFIED
```

検証内容：

- `cov_size` が再計算と一致
- **`n_child` が再計算と一致**（短いと未証明の child を隠せるため）
- manifest に多余な child ゼロ
- cache から各 edge の verdict を復元し、
  `class LOSS ⇔ 全 edge がLOSS` / `class WIN ⇔ 1 edge でもWIN` を満たすこと

**LOSS class（class 481）は 4 edge すべてが LOSS**、
**WIN class（class 482）は 4 edge すべてが WIN** であることを
cache から独立に復元した。

### 検証器が実際に見つけた欠陥2件

**(1) key の `hi` を比較していなかった**
検証側が `lo` だけ比較していたところ、lo が一致する無関係な class を
1個の class と誤認した（正しくは cov 6 / 106 children が
cov 77 / 2002 に見えた）。`hi` も比較するよう修正した。

**(2) class verdict と edge verdict の区別がなかった**
最初は manifest の全 child を class verdict と照合していた。
しかし **class verdict は class 全体のものではなく
edge ごとに決まる判定の集約**である：

```
edge  LOSS ⇔ その edge の合法 fifth move がすべて LOSS
edge  WIN  ⇔ 1つでも WIN fifth move がある
class LOSS ⇔ 全 edge が LOSS
class WIN  ⇔ 1 edge でも WIN
```

class 482 は 4 edge すべてが WIN なのに manifest には
LOSS child が 110 個含まれる（他の edge の LOSS child も全部列挙している
ため）。この区別を実装するまでは **WIN class が全て不正と判定される**。
なお `cov=6` と `children=111` の再計算は修正前から一致していた。

**この 2 件はどちらも「検証器が過度に厳密」「検証器が緩い」ではなく、
manifest が何を主張しているかを取り違えていたため。**
class 481 と 482 は s4 key が `hi` の 1 bit だけ違う
（`...8001,4` と `...8001,8`）のに verdict が正反対であることも、
(1) が致命的であることの証拠になっている。

## 8. 回帰（verdict 不変の確認）

修正前の binary (`git show HEAD:cpp/...` からビルド) と修正後を並走比較：

```
n=4  A:[empty] LOSS expansions=239   B:[empty] LOSS expansions=239
n=5  A:[empty] WIN  expansions=847   B:[empty] WIN  expansions=847
n=6  A:[empty] WIN  expansions=55561 B:[empty] WIN  expansions=55561
n=7  A:[empty] LOSS expansions=2123417 B:[empty] LOSS expansions=2123417
REGRESSION_AGREE
```

4 盤すべて verdict も expansion 数も一致（既存の記録値とも一致）。
既知の 11x11 state でも、旧 cache / 回収後 cache で `--cover` が
同じ既知 class 480 相当を duplicate せず、回収分だけ増えることを確認。

**変更は永続化と manifest 出力のみ。探索アルゴリズムには手を入れていない。**

## 9. worker cache merge の実装と、発見した欠陥

`N11-DFPN-COVER-OPTIMUM.md` が要求していた merge 手順は**手順だけが
書かれて実装が存在しなかった**。`dfpn_s5_merge.sh` として実装した：

- worker は自分のファイルにだけ書く（共有 cache へ append しない）
- canonical key ごとに deterministic merge（到着順ではない）
- **同一 key に異 verdict が 1 件でもあれば即停止し何も書かない**
- UNKNOWN（result が 1,2 以外）は決して merge しない
- atomic rename

3 ケースのテスト（`dfpn_s5_merge_test.sh`）で `MERGE_GUARD_OK`：
clean merge 成功 / conflict 拒否かつファイル未生成 / UNKNOWN 除去。

### 実装直後に見つけた自分の欠陥

`MERGE_GUARD_OK` の第三个 case が**落ちた**。
Python は正しく UNKNOWN を捨てているのに、
出力ファイルに `result=0` の行が残っていた。

原因は `mv -f "$TMP" "$OUT"` 1 行だった。
Python は既に `$OUT` に**フィルタ済みの結果**を書いており、
`mv` がそれを**未フィルタの staging file で上書き**していた。
つまり **UNKNOWN をちょうど棄却した直後に復活させる**経路である。

この欠陥はテスト入力でしか露見しないが、
実害は大きい：保存済み cache に「未確定」が混ざり、
後続の class 判定を誤らせる。`mv` を削除して修正した
（Python の出力が既に最終形なので移動は不要）。

**同じ失敗を3回再現し、staging file を `od` で16進ダンプし、
抽出した Python を単独実行して shell 経由でのみ壊れることを確認**して
特定した。Python 本体は単体で正しく動作していた。

## 10. coordinator 1 class 実行（永続化の実証）

回収 cache 261件を使って coordinator を1 class 実行：

```
# COVER optimistic=35 in_cover=119 secured=10/119 min_additional=33 forbidden=0 worked=0
# s4 certificate: class=482 result=1 n_child=111 edges=4
coord,482,6,4,WIN,313904753,2415097,win=4 loss=440 unk=0
# cache_loaded=261 cache_size=319 cache_saved=58 cache_rejected=0 cache_hits=386 queries=444
# s4_classes_decided=1 s4_out=logs/w1/s4-worker-1.csv
# done classes_worked=1 wall_s=2415
```

| 指標 | 値 |
|---|---:|
| 対象 class | 482 |
| verdict | **WIN**（refutation には使えない）|
| unknown s5（着手前）| 4 |
| 新規 s5 verdict | 58 |
| exact nodes | 313,904,753 |
| wall | 2,415 s（約 40 分）|
| cache hit | **386 / 444 queries（87%）** |
| cache saved | **58**（永続化が実動作）|

**cache hit 87% は回収 261 件がなければ成立しない数字である。**
class 482 は4 edge 各々で WIN fifth move を持つため
secured は増えないが、58 件の verdict が永続化された。
**§5 の穴を実際に埋めた証拠である**
（この run は verdict を worker file に残すので、
interrupt しても失われない）。

**WIN class は cover の除外対象になる。** coordinator が
再最適化した結果、class 482 はどの certificate にも使えない。
これは退行の進行ではなく、
cover の選択却下という coordinator の正しい挙動である。

## 11. 現状

| 指標 | before | after |
|---|---:|---:|
| s5 verdict cache | 103 | **319**（WIN 1 / LOSS 318）|
| 回収した verdict | — | **158**（すべて独立再証明済み）|
| coordinator 新規 verdict | — | **58**（cold replay 検証中）|
| 判定済み s4 class | 1 LOSS | **2**（LOSS 1 / WIN 1）|
| secured coverage | 4/119 | **10/119** |
| min_additional | 34 | **33** |
| 新規 exact nodes | — | **419,287,160 回収分 + 313,904,753 新規** |
| 未解決 class | 3395 | **3393**（LOSS 1 / WIN 1 を判定）|
| 検証済み s4 certificate | 無し（dead code） | **2 class / 217 children** |
| cache conflict | — | **0**（重複0・異verdict 0）|
| cache hit 率 | — | **386/444 = 87%** |

OPT = 31 に対し **LOSS** class は 2 個、残り 29 個。
`min_additional` は 33 のままで、WIN class を 1 件確定させたことで
cover 選択の候補が 1 件減った。

**secured は 10/119 のまま進っていない。**
回収による 4→10 が今回の実質的な進捗であり、
class 482 は WIN なのでcover には寄与しない。

## 12. 制約と未解決

- **二石 root は 1 個も閉じていない。** secured 10/119 は
  reply r2=0 の cover 31 class のうち LOSS 2 件であり、
  空盤の refutation ではない。
- 1 class の証明は約 40 分。class 選択は
  「coverage 広い順」ではなく「**unknown s5 が少ない順**」が実測で効いた。
- **WIN class を先に確定すると cover の可能性が狭まる。**
  coordinator は cover 最適化で避けるが、
  判定順序によっては refutation 不能な class に時間を払う。
- **11×11 の空盤勝敗は UNKNOWN のまま。**

**11x11: UNKNOWN**