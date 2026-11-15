# (5,6) 5x22 bounded-edit witness surgery — 完全局所閉包・census 完全性・witness ジャンプ幾何

2026-11-15 高速レーン。本実験は IN FLIGHT として開始した「K0815 の 5x21 種
からの有界編集距離で 5x22 witness を探す」レーンであるが、実行中に並走
レーンが class-split SAT で m=22 witness を発見した
（K0852・five-row-q6-m22-witness-20261115・class {0} k=4 minpos=0・
24石・3,126,820 conflicts）。よって SAT 探索という主目的は不要になり、
本実験の成果は次の4点に確定した:

1. surgery 機械の q=w+1 境界における census 完全性の機械検証（C4）
2. end-to-end 陽性対照（CTRL-1）
3. m=21 種近傍の完全列挙による sd≤6 局所閉包（負）と K0852 witness との
   幾何的距離の定量（witness ジャンプ）
4. 副次発見: m=21 witness の sd≤2 球内にちょうど3つの witness（元+1-swap 変種2つ）

## 結果

### C4 — census 完全性 @ (5,6,22) と (5,6,21): PASS

q=w+1 境界では ≥q 点円が単一の2点行（2+1+1+1+1 行分布）を持ち得るため、
chord-pair 分解（2つの2点行を要求）は一般には不完全である（(8,9) で
q9-census が必要だったのと同じ境界）。そこで surgery.js の buildCensus
（chord-pair）を実験の surgery.js から機械抽出し（`sed -n '31,97p'` →
census_extract.js）、独立 all-triples 列挙（C(wm,3) 全三点組 → 直線・円の
正準整数形 → ≥6点で濾過。円は A(x²+y²)+Bx+Cy+D=0・content-1・A>0、
全て整数演算）と曲線集合を比較した。

- (5,6,22): chord-pair 902曲線 = 897円 + 5行 / all-triples 902曲線。
  双方向差集合 0 — **完全一致**。1-double-row 6点円は 5x22 に存在しない。
- (5,6,21): chord-pair 810 = 805円 + 5行 / all-triples 810。完全一致。
- 既存較正 C2（genfast.js≡sat2.js CNF バイト同一 @ (5,22,6) --deficient）
  と合わせ、5x21/5x22 の census は2系統で完全。

### CTRL-1 — end-to-end 陽性対照: PASS

5x21 盤に K0815 witness から (5,1) を除去した23石 seed から (2,2) 手術:
nRmLeaves 6,841 / nSafe 6,841 / nMaximal 3 — **元の 24石 witness を含む
3つの deficient-maximal witness を再発見**（0.1〜0.3s）。L1/L2/L3 枝刈り
を通した機械が witness を見逃さないことの end-to-end 検証。

### 5x22 完全局所列挙 — 負（不在主張ではない）

種（24石・rows [4,5,5,5,5]）を 5x22 に offX=0/1 で埋め込む。T′（種空セルの
うち 5石曲線で塞がれていないセル）は単一セル (21,0) / (0,0)。
F = seed ∪ P \ Rm、|P|≤maxP、|Rm|≤maxRm、|F|≤24=5(6−1)−1 を完全列挙:

| run | offX | (maxP,maxRm) | nRmLeaves | nSafe | nMaximal | nWitness |
|---|---|---|---|---|---|---|
| m22_off0_pp2 | 0 | (2,2) | 25,158 | 25,158 | 0 | 0 |
| m22_off1_pp2 | 1 | (2,2) | 24,976 | 24,976 | 0 | 0 |
| m22_off0_pp3 | 0 | (3,3) | 4,227,320 | 4,227,320 | 0 | 0 |
| m22_off1_pp3 | 1 | (3,3) | 4,180,654 | 4,180,654 | 0 | 0 |

sd≤4 球（(2,2)）も sd≤6 球（(3,3)）も witness なし。safe leaf が全
RmLeaf と一致することから、枝刈り L1〜L3 は safe 側で完全に保存的
（unsafe な F は探索木の途中で排除されるのみ）。

**系（導出・全称有限）**: 任意の F（|F|≤24）が seed の埋め込み
（offX=0 または 1）と対称差 ≤6 なら |P|≤3 かつ |Rm|≤3（|F|≤24 ⟹
|P|≤|Rm|）であり上記列挙に含まれる。よって **5x22 上のすべての
24石以下 deficient-maximal 配置は m=21 種の両埋め込みから対称差 ≥7**
である。これは K0852 witness を含む。

### witness ジャンプ幾何 — K0852 witness との対称差

K0852 m=22 witness（24石・rows (4,5,5,5,5)）と m=21 種の全8埋め込み
（H/V/HV 鏡像 × offX 0/1）の対称差を直接測定（scripts/sd_k0852.js）:

- 最小 28（id@0 と H@0）。全埋め込みで 28, 28, 34, 38, 38, 40, 40, 42。

すなわち m=21 witness → m=22 witness の遷移は**最低14石の移動**を要する
大きなジャンプである。これは (5,5) の m=24→25 precedent（≥10石）、K0852 の
5x23 surgery 負（m=22 種から2石移動以内に witness なし）と一貫する
「連続幅間で witness が大きく跳ぶ」パターンを (5,6) にも持ち込む。
5x23 探索では m=22 witness の近傍（2石以内は K0852 が完全列挙済み・0）と
m=21 種由来の構造の両方が使えるが、遠距離ジャンプが予想される点で
surgery の見積りは保守的にならざるを得ない。

### 副次発見 — m=21 witness は孤立していない

CTRL-1 の完全列挙（23石 ctrl seed の sd≤4 球・|F|≤24 は m=21 witness の
sd≤2 球を含む）により、K0815 5x21 witness の sd≤2 球内の deficient-maximal
配置は**ちょうど3つ**: 元 witness と 1-swap 変種 (10,2)→(11,2)、
(10,2)→(12,2)（いずれも 24石・rows [4,5,5,5,5]）。2変種は独立 all-triples
census 系（surgery.js と方法独立・C4 により 5x21 census も完全）で安全・
極大を検証済み（verify_variants_5x21.json）。m=21 witness の 1-swap が
witness であり続ける事実は、witness 多様体の局所構造の非自明な陽性例で
ある（(5,5) m=24 の「22個の witness」報告と対比して、(5,6) m=21 では
sd≤2 近傍は狭い）。

## 記録と再現

- output/records.jsonl: 5 run の集計。生 JSONL は output/*.jsonl
  （witness 行 + summary 行・決定論的）。
- output/c4_census_check.json / c4_census_check_5x21.json: C4 PASS。
- output/sd_k0852.json: 対称差測定。output/verify_variants_5x21.json: 変種検証。
- seeds/seed_w56_21.json: K0815 5x21 witness（seeds_w56_21）。seeds/ctrl1_seed.json: CTRL-1 seed。
- 機械: surgery.js は eight-row-q9-m29-surgery-20261115/scripts/surgery.js
  と verbatim 同一（md5 94baa517b788efa02dc761b892fc8440）。L1/L2/L3
  枝刈り補題の証明は同実験 README。census_extract.js は buildCensus の
  機械抽出（`sed -n '31,97p' surgery.js` + module.exports）。
- 決定論性: 全 run は環境リセットを跨いで同一 counts（nRmLeaves/nSafe/
  nMaximal/nWitness/Tprime）を再現（事前実行と本再生成で bit-exact）。

## スコープ

- 本実験の負は m=21 種近傍の局所命題であり、5x22 不在主張ではない
  （m=22 は K0852 により SAT・witness band m=15..22）。m=23 は open。
- 対称差≥7 は offX=0/1 両埋め込みに関する完全列挙による主張。鏡像埋め込み
  を含む距離は sd_k0852.json の直接測定（min 28）による。
- 24石以下という |F| 制約は witness 定義（|F| ≤ w(q−1)−1）からくる。
  25石以上の maximal 配置は本実験の対象外（witness ではあり得ない）。
