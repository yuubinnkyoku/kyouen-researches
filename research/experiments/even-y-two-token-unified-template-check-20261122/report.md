# 偶数y (10, 12, 14, 16) 統一テンプレート機械検証 — two-token vertical-fiber closed form

**日付**: 2026-11-22（fast lane）
**種別**: 機械検証（実験）。出版済み閉形式どうしの一致確認であり、閉形式自体の正しさの証明ではない。
**入力**: 本 repo の既出版成果のみ（下記 9 ファイル、SHA-256 は `output/audit.json` に pin）。
**検証器**: `scripts/check_even_y_unified.py`（実行 0.6 秒、再現手順は本 report 末尾）。

## 1. 問い

two-token vertical-fiber 族の偶数 y の閉形式 cand10 / cand12 / cand14 / cand16 は、
それぞれ別々のファイル・別々の表現形式（y=10 は行別明示表、y=12/14/16 は Y パラメトリック
formula 形式）で出版されている。本検証は次の問いに答える:

> **cand14 の fit コード（`vertical-fiber-two-token-y14-parametric-allz-fit-20261122/cand14.py`）のコード本体は、`Y = 14` の 1 行を除いて y 依存のリテラルを含まない。これの Y 代入だけで、偶数 y = 10, 12, 16 の全出版表（fit 版および全称 verifier 組込みの proved 版）を正確に再生できるか?**

出来れば「偶数y 4族は単一の Y パラメトリックコードで再生できる」ことが確定し、
横断法則（K1235 周辺の一般補題化レーン）への基礎データになる。

## 2. 統一テンプレートの定義

`cand14.py` から module docstring 終端〜`def main()` までを切り出し、

- `Y = 14` → `Y = <対象>`、
- `in_T14 → in_TY`, `in_P14 → in_PY`, `cand14 → candY`

の機械的置換のみを施して exec したものを `uni(Y)` と呼ぶ（置換は名前と Y 定数のみ。
式本体は `cand14.py` が全て `3 * Y + 2` 等 Y 式で書かれているため無修正）。

対照対象:
| 対象 | 出典 | 種別 |
|---|---|---|
| cand10 (fit) | `vertical-fiber-two-token-y10-parametric-allz-fit-20261120/cand10.py` | 出版 fit 表 |
| cand10 (proved) | `vertical-fiber-two-token-y10-parametric-allz-proof-20261120/verify_y10_universal.py` 組込み | 全称証明済み表 |
| cand12 (fit) | `vertical-fiber-two-token-y12-parametric-allz-fit-20261120/cand12.py` | 出版 fit 表 |
| cand12 (proved) | `vertical-fiber-two-token-y12-parametric-allz-proof-20261120/verify_y12_universal.py` 組込み | 全称証明済み表 |
| cand14 (proved) | `vertical-fiber-two-token-y14-parametric-allz-proof-20261122/verify_y14_universal.py` 組込み | 全称証明済み表 |
| cand16 (fit) | `vertical-fiber-two-token-y16-parametric-allz-fit-20261122/cand16.py` | 出版 fit 表（observed） |

fit 版と proved 版の差は y=10 ではコメントブロック 1 件のみ（`Y = 10` 〜 `def opts10`
区間の byte 差は当該コメント行のみ、コード行は意味同一、本 run で unified diff で確認済み）。

## 3. 機械検証結果（全て PASS、`output/check-run.txt`・`output/audit.json` 参照）

### 3.1 grid 掃引（価値関数 cand(z, x, R) 全体、bad = 不一致点数）

| 比較 | grid 設定 (zmax, xpad, rpad) | 点数 | bad |
|---|---|---|---|
| uni(10) vs cand10 (fit) | (30, 25, 40) | 80,600 | **0** |
| uni(10) vs cand10 (proved) | (40, 25, 44) | 143,664 | **0** |
| uni(12) vs cand12 (fit) | (30, 25, 40) | 76,539 | **0** |
| uni(12) vs cand12 (proved) | (25, 20, 35) | 41,184 | **0** |
| uni(14) vs cand14 (proved) | (22, 20, 35) | 29,877 | **0** |
| uni(16) vs cand16 (fit) | (19, 25, 40) | 30,150 | **0** |

合計 401,814 点、不一致 0。（y=16 grid は x ≥ 16 機械 assert で正当な定義域のみ掃引。）

### 3.2 行 census（in_P / in_T の行毎集合比較、offset 1..160、行固定 x = zp + d）

全 12 census（y=10 fit/proved × P/T、y=12 fit/proved × P/T、y=14 proved × P/T、
y=16 fit × P/T）で **diff 行 0**。行数は y=10: 44、y=12: 52、y=14: 60、y=16: 68。
さらに偶数 y の全行で offset ∈ [120, 160] の値が行単位で一定（I 行は区間裾で True、
base 行は有限サポートで False）であることを確認し、行型が既知
（P: b_k ∪ I[th) 型、T: 有限サポート型）であることと合わせ、行内の全 offset 同一が
成り立つ（σ は後述の行分類・L1 補題で側面からも担保）。

### 3.3 merge 領域の本文一致

4 fit ファイル全てが merge 領域（`x ≤ z − Y − 1`、単一 token 階段 `S = x + Y`、
`R ≥ q_odd(S) + 1`）について byte 同一のコード行を含む（audit `merge_identity` = true × 4、
スクリプト内 text assertion）。

## 4. y=10 出版明示表の表現分類と Lemma L1

y=10 の fit 出版表は行別の (k, th) 定数列（`(d, _bk(off, k), R ≥ z + th)`）。テンプレート
の formula（z-odd I 行 k = (d + 3Y + 2) // 4、th = 2k + [d ≡ 3Y mod 4 が 0]、z-even I 行
k = (d + 3Y − 1) // 4、th = 2k + 1 等）との行毎分類（スクリプト `parse_pub_chain` +
`tmpl_prows`、全 43 明示行）:

- **26 行: (k, th) 定数として完全同一**（I 行 10 行 + base 行 15 行 + その他）
- **15 行: alias（表現違い・集合同一）**:
  - z-even I 行 10 行（d = −9, −7, …, 9）
  - z-odd 対角・pin 行 5 行（d = −10, −6, −2, 2, 6）
- **2 行: 定型**（z-even d = −10 の `return False`（対角）と z-odd d = 11 の sweep 行
  `base10` = `_bk(off, 10)` = `_bk(off, Y)`）

alias 行の相違はすべて次の形:

**Lemma L1**（証明つき、機械検証と独立に成立）:
任意の整数 k ≥ 0 に対し
`b_{k+1} ∪ I[2k+2) = b_k ∪ I[2k+1)`
（`b_k = {奇数 offset 1, 3, …, 2k−1}`、`I[t) = {offset ≥ t}`）。
*証明*: 両辺とも [1, ∞) から偶数 {2, 4, …, 2k} を除いた集合に等しい。∎

y=10 出版表の alias 行はすべて「pub = (k+1, 2k+2)、template = (k, 2k+1)」の組で
（スクリプトがこの precondition を行毎に assert）、L1 より**全 offset** で集合同一。
よって y=10 出版表とテンプレートの in_P の同一性は「26 行の定数一致 + 15 行の L1
aliasing + 2 行の定型 + merge/tail/band 本文一致」により全 (z, x, R) で成立する
（出版表自身の正しさは y=10 全称証明レーンの成果、本検証の前提）。

## 5. y=12 / y=14 / y=16

- **y=12**: 出版 in_P12 は formula 形式そのまま。リテラル (d + 38)//4 = (d + 3·12 + 2)//4、
  th の d % 4 == 0 ⟺ (d + 3·12) % 4 == 0、(d + 37)//4 = (d + 3·12 + 1)//4、
  (d + 35)//4 = (d + 3·12 − 1)//4 を d = −12..12 で数値同一 assert（`Y12FORM`）。
  より y=12 も表現差なしで全パラメータ同一。
- **y=14**: テンプレートの由来そのもの。fit 版 = main 版（SHA-256 61782b6e…）で
  proved 組込み表とも grids 29,877 点・60 行 census で一致。
- **y=16**: cand16 fit は y=16 fit レーンで cand14 の Y+2 機械翻訳として出版済み
  （899 行 74,741 点 probe 完全一致、K1237）。本 run で追い打ち確認:
  コード本体の正規化差分（コメント除去・名前正規化後）は **完全一致**
  （残差は `b14` / `b16` のローカル変数名のみ、式は全て Y 式のまま）。
  すなわち y=16 も表現差なしでテンプレートと同一コード。さらに本検証は独立に
  uni(16) を再構成し grid 30,150 点で一致を再確認。y=16 は **observed**
  （全称 verifier 未出版）。

## 6. 奇数 y 陰性対照（テンプレートは偶数 y 特化）

y = 13, 15（K1231 / K1235 レーンの全称証明済み表）に対する uni(13) / uni(15) は
**一致しない**（fail-closed 設計上、「不一致ゼロ」なら逆に FAIL）:

| | y=13 | y=15 |
|---|---|---|
| T 側差分行（off ≤ 160, 行掃引） | 2 行: (z even, d=−13, off 13), (z odd, d=−11, off 14) | 2 行: (z even, d=−15, off 15), (z odd, d=−13, off 16) |
| P 側差分行 | 54 行 | 62 行 |
| 小 box (z ≤ 11) での cand 不一致点 | 4,345 点中 2,649 | 2,916 点中 1,660 |
| 最初の不一致 | (z, x, R) = (2, 13, 28)、proved 0 vs uni 1 | (4, 15, 32)、proved 0 vs uni 1 |

即ちテンプレートは偶数 y にのみ当てはまる（T 側は対角帯端の 1 token、P 側は
I/base 掃引構造そのものが odd-y では異なる）。不一致の第一点は R = 2Y−1〜帯の
偶奇差（y=13, 15 の出版表が値 0 を取る点でテンプレートが 1 を返す）で、
これは K1235 で記録された偶奇型の違いと整合する。odd-y 表の正しさは各レーンの
全称証明のまま、本検証は触れない。

## 7. 結論

1. **偶数 y = 10, 12, 14, 16 の 4 全族の出版閉形式は、cand14fit コード本体の Y 代入のみ
   （式本体無修正）で完全に再生できる**（grids 401,814 点 bad 0、行 census 640 行
   bad 0、merge 本文一致）。
2. 一致の根拠は行分類で明示された: y=10 の表現差 15 行は Lemma L1（証明つき）の
   aliasing で全 offset 集合同一、残り 26+2 行は定数・本文一致。y=12 は定数の
   数値同一、y=14 はテンプレートの由来、y=16 は正規化差分完全一致（式は同一）。
   よって「単一コードが4族を再生する」ことは**全パラメータで成立**し、
   grid の有限性が本質的な制約ではない。
3. 奇数 y = 13, 15 では不一致（陰性対照）。**テンプレートは even y 特化**。
4. 本検証は一致の検証であって、4 閉形式自身の正しさの証明ではない。y=16 は依然
   observed であり、y=16 全称 verify_y16_universal.py（テンプレート実装で書ける）
   が次段階候補。

## 8. 再現

```
cd research/experiments/even-y-two-token-unified-template-check-20261122
python3 scripts/check_even_y_unified.py > /tmp/run.txt   # exit 0 = PASS
cat output/audit.json                                     # 全数値と入力 SHA-256 pin
```

実行時間 0.6 秒（Python 3.12）。入力 9 ファイルは repo 内の兄弟実験 dir から
相対パスで読む。いずれかが更新されると audit の sha256 が変化する。

## 9. 横断法則レーンへの提供事項

- 偶数 y 4族を担う「単一 Y パラメトリックコード」が存在し、それが cand14fit
  コード本体そのものであることが機械確定した。
- 表現の揺れ（y=10 の明示表 vs formula 形式、(k+1, 2k+2) vs (k, 2k+1)）は L1
  aliasing で標準化できる。L1 は自明だが、y=10 表の machine-reproduction に
  実際に必要な構成要素である。
- 一般補題化（K1235 part 2 レーン）は本結果を前提にできる: 「テンプレートが偶数 y
  で出版表を再生する」という述語が、y 解釈上で閉じた機械検証済みの基盤となる。
