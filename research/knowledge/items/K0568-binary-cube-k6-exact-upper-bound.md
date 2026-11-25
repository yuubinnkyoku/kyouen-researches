---
id: K0568
title: "二値六次元立方体の共七点禁止版の最大安全石数は K_6=9"
kind: proposition
status: closed
topics: [variants, geometry, maximum-safe]
aliases: []
relations:
- type: depends_on
  target: K0553
  note: d=6のd+3下界（9点証人）を前提とし、本項目で上界を追加する
- type: verifies
  target: K0553
  note: d=6の9点証人を前提としてK_6=9を確定する方向の上界
- type: verifies
  target: K0591
  note: censusのd=5七点GP総数309,056がK0591の全局面DPの七石安全局面数と完全一致（第三手法の独立照合）
artifacts:
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/README.md
  role: log
  note: 手法・再現手順・証拠の意味と限界
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/build_k6_cnf.cpp
  role: solver
  note: C(64,7)個の7点部分集合の依存判定とCNF生成器（二算法照合つき）。こちらは依存7点組全部を禁止する正しいCNF
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/build_k6_circuits.cpp
  role: solver
  note: 包含極小依存集合（circuit）列挙とCNF生成器。10点存在判定に限りcircuit禁止と全依存7点組禁止は同値（2026-11-14の一般補題）。d=6の列挙器の完全性は2026-11-15に二列挙器監査で確定（下記）。UNSATは未検証のまま
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/audit_frontier9.py
  role: verifier
  note: 9点証人の極大性（64頂点すべて禁止）の独立監査
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/verify_k9_witness.py
  role: verifier
  note: exactly-9 CNFのSAT証人9点の幾何学的再検証
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/results.json
  role: data
  note: 機械可読な主張・CNF統計・検証計画
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/verify_small_dimension_circuits.py
  role: verifier
  note: d=3..5の全部分集合サイズ4..qを二素数・列順反転rankで完全列挙し、circuitの上下閉包を検査
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/small_dimension_circuit_audit.md
  role: proof
  note: 小次元の有限完全監査とexactly-K同値性の適用境界
- path: research/log/2026-11-14-k6-small-d-circuit-audit.md
  role: log
  note: 独立監査・READMEの古い評価の訂正・次のd=6監査課題
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/audit_mine.js
  role: verifier
  note: 独立実装のd=6 circuit全列挙器（純整数Bareiss・全小行列式・combinadic rank全葉照合・チェックポイント再開可能）
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/audit_port.js
  role: verifier
  note: build_k6_circuits.cpp (f3868c53) の逐語移植（p=2^61-1→1,000,003 置換・Hadamard限界907で判定同値）による第二列挙器。circuits{4..7}.binがaudit_mine.jsとバイト一致
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/build_k6_cnf_stream.js
  role: solver
  note: circuit CNFのstreaming再生器。audit_port.js --cnf と合成familyでバイト同一性をcmp確認、実familyで p cnf 4160 19484942 を再生
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/eval_witness_cnf.js
  role: verifier
  note: 再生exactly-9 CNF全19,484,942節の直接評価によるSAT制御（Sinz補助変数は接頭辞カウント意味論で計算・0違反）
- path: research/experiments/binary-cube-hyperplane-k6-exact-20261025/counter_control.js
  role: verifier
  note: Sinzカウンタ意味論の孤立制御（counters-only CNF・kissat・6ケース全PASS）
- path: research/log/2026-11-15-k6-d6-circuit-family-audit.md
  role: log
  note: d=6 circuit族の二列挙器監査・環境障害とレジューム設計・CNF再生・SAT/カウンタ制御
- path: research/experiments/binary-cube-gp-census-k6-20261121/README.md
  role: log
  note: census路線の手法・完全計数表・交叉検証・再現手順・限界
- path: research/experiments/binary-cube-gp-census-k6-20261121/census2.js
  role: verifier
  note: 63ペア頂点0アンカー分割GP集合完全列挙器。二素数零検定・battery 20項目・独立bruteゲート再照合つき
- path: research/experiments/binary-cube-gp-census-k6-20261121/r6-results.jsonl
  role: data
  note: d=6全63ペアの個別計数（正本データ）
- path: research/experiments/binary-cube-gp-census-k6-20261121/results.json
  role: data
  note: census路線の機械可読な主張・計数・交叉検証値
- path: research/experiments/binary-cube-gp-census-k6-second-impl-20261125/README.md
  role: log
  note: 独立第二実装（純整数Bareiss+行置換座標+射影マイナーゲート）の手法・再現手順・限界
- path: research/experiments/binary-cube-gp-census-k6-second-impl-20261125/census3.js
  role: verifier
  note: 第二実装の63ペアGP完全列挙器。素数・剰余なし純整数。selftest/brutecensus/census/pair/gatecheck全モード
- path: research/experiments/binary-cube-gp-census-k6-second-impl-20261125/r3-results.jsonl
  role: data
  note: 第二実装のd=6全63ペア個別計数（第一実装r6-results.jsonlと行単位で同一）
- path: research/experiments/binary-cube-gp-census-k6-second-impl-20261125/results3.json
  role: data
  note: 第二実装の機械可読な主張・照合結果・battery一式
- path: research/log/2026-11-21-binary-cube-gp-census-k6.md
  role: log
  note: censusの設計・実行・交叉検証・限界の研究記録
scope: 二値六次元超立方体 V_6={0,1}^6 上で、相異なる7点が一つの実アフィン超平面に載ること（退化を含む）を禁止するゲームの最大安全石数。Grundy値・misère版・d≠6は対象外。
evidence: "下界 K_6≥9 はK0553の9点証人で確定済み。上界 K_6≤9 は2026-11-21のGP-censusで確定した: {0,1}^6 の一般位置（全7点部分集合アフィン独立）集合のうちサイズ10のものの完全計数は0（63ペア頂点0アンカー分割・全走査約13分CPU・アンカー計数 s9=408,240 / s10=0）。交叉検証: d6のs4..s7が監査表依存数から独立導出される値と全桁一致、d3/d4全サイズとd5サイズ6以下が独立brute全列挙と全桁一致、d5七点GP総数309,056がK0591の全局面DPと一致、battery 20/20、ペア(0,1)先頭60万ゲートbrute再照合不一致0。2026-11-25に独立第二実装（census3.js: 素数・剰余なしの純整数Bareiss+行置換座標函数+射影マイナー・ゲート）による63ペア全走査再現が完了し、全ペア行とΣテーブル [0,63,63,1953,39410,571340,6029142,40050850,53334038,408240,0] が第一実装と完全一致（実験 binary-cube-gp-census-k6-second-impl-20261125、単一オーナー宣言 log 2026-11-25）。census上界の証拠は二重実装化された。Grundy値は未解決のまま。"
---

# 二値六次元立方体の共七点禁止版は K_6=9

$V_6=\{0,1\}^6$ の64頂点上で、相異なる7点が一つの実アフィン超平面に載ること
（退化を含む）を禁止するゲームの最大安全石数は $K_6=9$ である。
下界は K0553 の9点証人、上界は 2026-11-21 のGP-census（下記「上界」節）で確定した。

## 下界（確定）

9点証人は K0553 の d=6, m=9 レコード。整数Bareiss（全 $\binom{9}{7}=36$ 小行列式）と
mod $2^{61}-1$ 掃き出しの両検証器で完全検証済み。
さらに `audit_frontier9.py` により、この9点証人が64頂点すべてを禁止する
（極大配置である）ことを独立確認した。

## 上界（2026-11-21 GP-censusで確定）

10点の一般位置（GP、全7点部分集合アフィン独立）集合が存在しないことを、CNF 路線とは独立に
有限完全列挙（census）で確定した。詳細は
[実験README](../../experiments/binary-cube-gp-census-k6-20261121/README.md)と
[研究ログ](../../log/2026-11-21-binary-cube-gp-census-k6.md)。

- 頂点0を含むGP集合の計数にアフィン自己同型で全計数が従う（$x\mapsto x\oplus u$ は
  座標鏡映の合成で頂点推移的）。ペア $(0,v_2)$、$v_2=1..63$ の63本で木を完全分割し、
  サイズ10のGP集合を全数探索して計数0。
- アンカー計数: $s_7=40{,}050{,}850$、$s_8=53{,}334{,}038$、$s_9=408{,}240$、$s_{10}=0$。
  非アンカー総数 GP-7 $=366{,}179{,}200$（既刊の独立七点組数と一致）、GP-8 $=426{,}672{,}304$、
  GP-9 $=2{,}903{,}360$、GP-10 $=0$。
- 手法: GP前置行列のfraction-free掃き出しframeと行置換関数恒等式で全ゲート判定を疎関数の
  零検定に帰着。0/1成分7×7行列式のHadamard限界 $907<p$（二素数 $67{,}108{,}859$ / $67{,}108{,}837$）により
  有限体零検定は整数零と厳密同値。全走査は2コアで約13分。
- 交叉検証: s4..s7 が d=6 監査表（依存 4,816/311,360/10,663,520・独立七点組 366,179,200）から
  独立導出される値と全桁一致、d=3/d=4全サイズと d=5 サイズ6以下が独立brute全列挙と全桁一致、
  d=5七点GP総数 309,056 が [K0591](K0591-binary-cube-d5-strong-solution-verification.md)
  の全局面DPの七石安全局面数と完全一致、battery 20/20（Laplace/BigInt関数族照合・9点証人3種の
  GP再検証・6ペアのツリー内全ゲートbrute再照合・v3-スライス分割整合）、
  ペア(0,1)先頭600,000ゲートのbrute再照合で不一致0。
  下位次元も $K_3=5$、$K_4=6$、$K_5=7$ を同censusで再現。
- 証拠はもともと単一実装の有限完全列挙+多角度交叉検証だったが、2026-11-25に独立第二実装による全走査再現が完成して二重化された（下記2026-11-25節）。

K0591 の指摘（ゲーム規則の禁止集合としてのcircuit包含極小化の誤用）と矛盾しない。
本確定はcircuit CNFを使わない列挙による。exactly-10判定に限るcircuit同値性
（2026-11-14の補題）はそのまま正しい。Grundy値・misère版は対象外で未解決。

## CNF路線の記録（2026-10-25〜11-15、UNSAT未取得のまま）

10点の一般位置集合が存在しないことの証明として、以下を準備した（歴史記録）。

1. 依存7点組の完全列挙：全 $\binom{64}{7}=621{,}216{,}192$ 個の7点部分集合を
   二つの独立算法（mod $2^{61}-1$ と mod $1000000007$）で判定し完全一致。
   依存7点組は255,036,992個。これはゲーム規則を7点組で直接表現する禁止集合の全体である。
   ただし包含極小アフィン依存集合（circuit）だけを禁止する表現とは異なる。

2. 完全版CNF：4,160変数・255,045,246節（生6.9GB）。
   19GB環境のCaDiCaLではメモリ不足で未完。**UNSAT確定には至っていない。**

3. かつて作成したcircuit削減CNF（19,484,942節）でのkissat実行は、
   8h10mでSIGTERM終了しUNSAT判定は得られていない。非circuitの依存7点組を直接禁止していないが、**exactly-10制約下では**
   依存7点組の禁止とサイズ7以下のcircuit禁止は同値である（下記補題）。
   ただしUNSAT結果が得られていないため、上界証明には至っていない。

4. 制御として、exactly-9 CNFはSATであり、kissatの解
   {11, 22, 28, 37, 42, 49, 57, 58, 63} が全36小行列式非零と
   `verify_k9_witness.py` で確認済み。

## 証拠の限界

- 上界はcensus（第一実装 GF(p) 二素数系・第二実装 純整数系の二重実装による有限完全列挙）による。両者は計数レベルで一致しており、個々のGP集合の同一性検証ではない。両実装が同じ列挙規約（頂点0アンカ・63ペア分割・昇順正準木）を採る点は共有の前提として残る。
- Grundy値、misère版は対象外・未解決。

## 2026-11-14：exactly-10 のcircuit縮約の論理的正当性

有限点集合の10点部分集合がすべての7点部分集合でアフィン独立であることと、サイズ7以下の包含極小アフィン依存集合を含まないことは同値である。前者に反する7点集合は内部に極小依存集合を持ち、後者に反する極小依存集合は10点集合内で7点まで拡張できるためである。証明の詳細は `research/log/2026-11-14-k6-exact-cardinality-circuit-equivalence.md` を参照。

したがってcircuit縮約そのものを10点不存在判定に対して無効とする旧評価を訂正する。ただし、既存生成器が**すべて**のサイズ7以下のcircuitを正しく列挙したか、exactly-10符号化が正しいか、SAT solverがUNSATを証明できるかは別問題であり、いずれも本項目では新たに確定しない。ゲーム全局面（7点未満を含む）の合法性やGrundy値にはこの同値性を流用できない。


## 2026-11-14：小次元circuit列挙の独立監査

verify_small_dimension_circuits.py により d=3,4,5（q=d+1）のサイズ4..qの全部分集合を列挙した。二つの素数 1,000,003 / 1,000,033 と列順を反転した消去を照合し、Hadamard限界216未満から有理数階数と一致することを保証した。

| d | 依存集合数（サイズ4..q） | circuit数（サイズ4..q） | 依存q集合の被覆 |
|---:|---:|---:|---:|
| 3 | 12 | 12 | 12/12 |
| 4 | 100, 1,360 | 100, 160 | 1,360/1,360 |
| 5 | 720, 22,240, 350,000 | 720, 2,080, 41,760 | 350,000/350,000 |

生成circuitのq点拡張370,080件も全て依存q集合に含まれた。これはd=3..5の有限完全監査であり、d=6の列挙完全性はまだ証明していない。K_6≥9は確定、K_6≤9とK_6=9は未確定のままである。

## 2026-11-15：d=6 circuit族の二列挙器監査（列挙器の完全性確定）

2026-11-14の監査課題「d=6のcircuit族を別の独立列挙器と突き合わせる」を完了した。
`audit_mine.js`（独立実装：純整数Bareiss、wide順は全 $s\times s$ 小行列式、サイズ4..6は全葉combinadic rank照合、size 7は総数照合、共線3点組0件の確認つき）と
`audit_port.js`（`build_k6_circuits.cpp` commit f3868c53 の逐語移植、唯一の置換は $p=2^{61}-1\to1{,}000{,}003$・両素数ともHadamard限界907超で判定同値）の2系統が、
サイズ4..7の全circuit族について**数値・8バイトレコードとも完全一致**した。

| サイズ | 依存数（既刊二算法と一致） | circuit数 |
|---:|---:|---:|
| 4 | 4,816 | 4,816 |
| 5 | 311,360 | 22,400 |
| 6 | 10,663,520 | 1,052,800 |
| 7 | 255,036,992 | 18,396,672 |

circuit総数 **19,476,688** は既存circuit CNF（19,484,942節 − Sinzカウンタ8,254節）の記録値と一致する。
制御として (a) 両列挙器が d=3,4,5 の既刊監査表を完全再現、(b) CNF再生器が `p cnf 4160 19484942` を再生し `audit_port.js --cnf` と合成familyでバイト同一、(c) 再生exactly-9 CNFの全19,484,942節を9点証人 {11, 22, 28, 37, 42, 49, 57, 58, 63} の直接評価で0違反（solverを介さないSAT証明・幾何再検証もPASS）、(d) Sinzカウンタの孤立制御6/6 PASS、をすべて確認した。

これにより**d=6 circuit列挙の完全性と、既存circuit CNFのcircuit節集合の正しさは確定した**（verification_plan第1項完了）。
ただしUNSAT判定は依然得られておらず、$K_6\le9$ は未確定のままである。残る作業はexactly-10 CNF（または完全版CNF）のUNSAT証明か、10点一般位置集合の発見である。

2026-11-21追記: この残る作業はcensusで解決した。サイズ10の一般位置集合は存在しないことが
全数列挙で確定し、CNFを使わずに上界 $K_6\le9$ が得られた（冒頭のcensus節参照）。

## 2026-11-25：独立第二実装による全走査再現（census上界の二重化）

census上界の残課題「独立第二実装による全走査」を完了した。第二実装 census3.js は第一実装と
同じ列挙規約のもと、演算核をすべて置き換える: 素数・剰余を一切使わない純整数演算
（Bareiss 行列式、行置換座標函数 $g_i(x):=\\det(M_B[\\text{row}\\ i\\leftarrow x])$、
k≥d+2 層の全ゲートを g 行の射影マイナー 2×2/3×3/4×4 整数行列式に還元する恒等式）。
全中間値は float64 内で厳密（|det|≤907、|g|≤1512、4×4 マイナー<1.26e14<2^53、battery B8 実測）。

結果: 全63ペアの個別計数が第一実装 r6-results.jsonl と行単位で完全一致、
Σ anchored テーブル [0,63,63,1953,39410,571340,6029142,40050850,53334038,408240,0]
（$s_9=408{,}240$、$s_{10}=0$）が公開テーブルと完全一致。battery は selftest 全PASS
（det vs BigInt Laplace 400、rank 200、gate-identity fuzz 410、9点証人3種+XOR正規化像の
GP再検証、d3/d4 fast census 全一致）、完全独立の直接行列式 brute 全列挙が d=3/4/5 の
公開 anchored テーブルを再現（d=5 は第一実装の brute より深く全サイズで完走し s8=0 を全数確認）、
ペア(0,1) 先頭600,000 child-decisions の直接再検査不一致0、軽量4ペア (v2=58,55,45,40) の
全 child-decision 再検査不一致0、重い3ペア (v2=7,13,32) 各先頭300,000 不一致0、
決定性（同一ペア再実行の整数ペイロード同一）。

honest labels: これは第一実装の有限計算の独立再現であり、数学的な新規主張はない。
両実装が同じ列挙規約を採る以上、一致は演算核の独立性を経由した計数レベルの二重確認であり、
個々のGP集合の同一性検証ではない（その点は第一実装の独立bruteゲート再照合と本実装の
gatecheck が担う、ただし全網羅ではない）。単一オーナー宣言と逐次 push の経緯は
[宣言ノート](../../log/2026-11-25-gp-census-k6-second-implementation-single-owner-note.md) と
[実験README](../../experiments/binary-cube-gp-census-k6-second-impl-20261125/README.md) 参照。
