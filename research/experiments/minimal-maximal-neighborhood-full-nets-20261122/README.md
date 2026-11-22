# 最小極大安全配置の近傍完全走査: sit-at込み拡張nets・K1206監査・s_11/s_12/s_13近傍陰性 (2026-11-22)

標準共円盤 (q=4: 禁止手 = 4石が同一円または同一直線上) の n×n 盤における極大安全配置
(safe = 禁止4石組なし、maximal = 全空点が何らかの3石triple+曲線でblock済み) の
*witness 近傍* を、sit-at追加 (未被覆空点への直接石置き) を含む完全走査器
`scripts/ext_nets.mjs` で網羅した実験。全25走査・計 10,082,387 構成の列挙で
**非自明な witness (seedより石数の少ない safe+maximal 構成) は0件**、
K1206の壁状態 strict 局所最適性はsit-at 含みでも成立、
という有界陰性 (bounded negative) を確定した。s_11∈{8,9,10} (K0312)・
s_12≤11 (K0320, K1206)・s_13≤12 (K0320) はいずれも不変。

## 1. 中心的な方法論的発見: sit-at 候補除外の穴

先行の近傍走査機材 `hunt.mjs` (s12-s13-upper-witness-20261121 ラーンの正本) の
`localNets` / `doubleSwapComplete` は、追加候補セルを「未被覆セル p の
cnt==2 quartet の完成セル」として列挙する際に `c !== p` 条件で
**未被覆セルそのものへの直接石追加 (sit-at) を候補から除外**している。

sit-at は State 機構上は合法である (非maximal seedでも走査可能な仕様: K0031 の 7×7 7石witness から
1石除去すると uncovered=1 になり、その空点に `State.add` すると viol=0・uncovered=0
に戻る)。にもかかわらず候補列挙から抜けていたため、両関数の
「候補列挙は追加に対して完備」という意味での走査は sit-at 分だけ不完備だった。

この穴を埋めるため `scripts/ext_nets.mjs` を作成した:

- seed構成 (maximal である必要はない) から **m 石を除去し、a 石を追加**するとき、
  追加候補を「現在石でない全セル」に限定せず、盤面の全セルから走査する
  (full0 / full1 / full2 = a∈{0,1,2})。sit-at は当然含まれる。
- 各構成で State の viol / uncovered を増分計算し、
  found = (viol==0 && uncovered==0)、bestScore = min(viol*1000+uncovered) を記録。
  found のうち seed と同一石集合のものは trivial 自己再構成として isSeed 分類。
- 出力は決定的 JSONL (header + per-removal + done)。`<out>.cp` で中断再開可。
- 依存は `hunt.mjs` (Board/State)・`census.mjs` (K1204 census anchor gate)・
  `witnesses.mjs` のみで、判定系は既存機材と同一コード。

走査構成数は組合せ恒等式
`C(k0,m) × (1 if a=0 else C(n²−(k0−m), a))`
に厳密一致する (k0 = seed石数)。率直な言い方をすると: **構成数は列挙が
洩れていないことの独立検証になっている**。全走査がこの式どおりであることを
records の各 jsonl の `"totalChecked"` で検証できる。

## 2. K1206 公刊主張の sit-at 込み監査 (upgrade to complete exhaustion)

K1206 は (a) 12×12 wall 状態 (score 4, K0320 n=12 witness −1石) の
2-swap 完全走査で witness なし = strict 局所最適、(b) n=12 witness 周囲の
remove-2/add-1 完全走査 陰性、を主張する。その走査は上記のとおり sit-at を含んで
いなかった。本実験の sit-at 込みフル走査は:

| seed | 走査 | totalChecked (恒等式) | found | bestScore | 解釈 |
|---|---|---|---|---|---|
| 12×12 wall (10石, viol=0 uncovered=4) | r1a0 | 10 | 0 | 14 | |
| 〃 | r2a0 | 45 | 0 | 26 | |
| 〃 | r2a1-full | 45×136=6,120 | 0 | 14 | **9石witness なし** |
| 〃 | r2a2-full | 45×C(136,2)=413,100 | 0 | 4 (=seed) | **uncovered<4 の状態なし, strict局所最適はsit-at込みで成立** |
| K0320-n12 witness (11石) | r1a0 | 11 | 0 | 4 | |
| 〃 | r2a1-full | 55×135=7,425 | 0 | 4 | **10石witness なし (K1206 r2a1監査 PASS)** |
| 〃 | r3a1-full | 165×135=22,440 | 0 | 14 | |
| 〃 | r3a2-full | 165×C(136,2)=1,514,700 | 0 | 4 | **s_12≤10 witness はremove-3/add-2近傍にもなし** |
| K1206 W_c (11石) | r1a0 | 11 | 0 | 4 | |
| 〃 | r2a1-full | 55×135=7,425 | 0 | 4 | W_c 近傍も同様 |
| 〃 | r3a1-full | 165×135=22,440 | 0 | 14 | |
| 〃 | r3a2-full | 165×C(136,2)=1,514,700 | 0 | 4 | |
| 13×13 plateau (11石, viol=0 uncovered=6) | r2a1-full | 55×160=8,800 | 0 | 12 | **10石witness なし** |
| 〃 | r2a2-full | 55×C(160,2)=699,600 | 0 | 6 (=seed) | **plateau の strict局所最適も sit-at込みで成立** |

(plateau seed は11石なので remove-2 の残りは9石、非石セルは 169−9=160 個。
全表で totalChecked = C(k0,m)×(a=0 なら 1、それ以外は C(n²−(k0−m),a)) が成り立つ。)

**監査結論**: sit-at を含めても wall には 9石・10石 witness も uncovered<4 の
状態も1つも現れず、K1206 の「壁状態は strict 局所最適」の主張は
**完全走査の意味で昇格して維持される** (K1206 の元の走査は候補制限版であったが、
主張の内容は sit-at込みでも偽りでなかった)。W_c / K0320-n12 の 10石 witness
不存在 (r2a1) も sit-at 込みで再確認された。

## 3. s_11 決定レーン: n=11 K0320 witness (10石) 周囲の完全近傍陰性

s_11 ∈ {8,9,10} (K0312: 8≤s_11≤10)。10石 witness を 9石 (remove m/add m−1) や
8石 (remove m/add m−2) に押し込む近傍を全走査した (seed:
`[[5,0],[8,0],[1,4],[6,4],[8,4],[0,5],[3,5],[8,5],[4,9],[5,10]]`,
独立検証は records/verify/verify-k0320-n11.json: 111/111 空点 blocked):

| 走査 | totalChecked | found (non-trivial) | bestScore |
|---|---|---|---|
| r1a0 (9石) | C(10,1)=10 | 0 | 8 |
| r2a0 (8石) | C(10,2)=45 | 0 | 18 |
| r2a1-full (9石) | 45×113=5,085 | 0 | 8 |
| r3a1-full (8石) | 120×114=13,680 | 0 | 16 |
| r3a2-full (9石) | 120×C(114,2)=772,920 | 0 | 8 |
| r4a1-full (7石) | 210×115=24,150 | 0 | 23 |
| r4a2-full (8石) | 210×C(115,2)=1,376,550 | 0 | 13 |

- **9石 witness は r2a1/r3a2 近傍に存在しない。8石 witness は r2a0/r3a1/r4a2
  近傍に存在しない。** よって s_11∈{8,9,10} は不変 (この走査だけでは決定不能)。
- r4a1 (7石) の構成は K0312 の「k≤7 では極大不可」と整合して found=0 が期待値であり、
  **走査器の期待値制御** として機能する (found が非0なら走査器のバグを意味する)。
- bestScore は全走査で seed の 0 を下回らない、つまりこの近傍で
  safe+maximal に到達する構成は1つもない。

## 4. s_13 上界の近傍拡張

K0320 n=13 12石 witness 周囲も sit-at 込みで拡張した:

| 走査 | totalChecked | found | 内容 |
|---|---|---|---|
| r2a1-full | 66×159=10,494 | 0 | 11石 witness なし |
| r2a2-full | 66×C(159,2)=829,026 | 66 (全て isSeed=true) | found=66 は全て trivial 自己再構成 (=seed)。非自明0 |
| r3a1-full | 220×160=35,200 | 0 | 10石 witness なし |
| r3a2-full | 220×C(160,2)=2,798,400 | 0 | 11石 witness なし (bestScore 6) |

r2a2 の66件は ext_nets の isSeed 分類機構が正しく機能することの
**陽性対照**を兼ねる (found に seed が入る経路が存在し、それが排除されている)。
s_13≤12 は不変・s_13≤11 witness はこれらの近傍にはない。

## 5. SAT側・SLS側の honest negatives (値主張なし)

**単一オーナー規約の継承** ([71408dda54](
../../log/2026-11-22-s12-s13-sat-stabilization-single-owner-note.md) の受入条件:
較正ラダー・UNSATはshuffle 2ショット一致・witnessは3系統検証+tamper・値更新は片側のみ・誤りは訂正記録)。
本レーンは SAT/SLS で値を一切主張しない。conflicts 数は勝敗ではない。

- **較正**: `enc_sat2.mjs` (v2.1, K1221規約の修正lex-leader鎖) で CNF を再生成し、
  7件全部が前セッション記録の sha256 接頭辞と一致
  (n7k6=`0aecb030…` は kit の cnf3 アンカーと完全一致,
  n11k8=`4d73d322…`, n11k9=`42c88905…`, n11k10=`822fd7ac…`,
  n8k7=`2b9a2d76…`, n9k8=`55307510…`, n10k9=`ca981f54…`;
  正本 = records/kissat-indet/cnf3gen-sha256.txt)。
  kissat 4.0.4 で n7k6 v2.1 は **UNSAT・174,155 conflicts・13〜14s で
  K1220 公刊ログの conflicts 数と完全一致** (records/kissat-indet/v3n7k6-regen.log)。
- **INDET**: n11k8 / n11k9 / n11k10 (v2.1, default, --time=240) は3件とも
  UNKNOWN (k8: 386,330 conflicts・k9: 184,869・k10: 198,812 を重ねても決着せず)。
  n11k10 は K0320 の10石witnessにより充足可能と分かっているのに
  240秒では到達できない、というのが最も強い注釈である
  (witness が存在すると分かっていても CDCL では 240秒で届かない、という注釈)。
- **SLS (v2, 60s、transplant seeding、n=11)**: k=10 (seed 7) は既知 witness
  を再発見できず bestScore 5 (=5 uncovered; 陰性対照で分離不能であることを
  明示)、k=9 (seed 11) bestScore 7、k=8 (seed 23) bestScore 15。
  k=8/9 の不発見は SLS の探索力不足と分離できない。

## 6. 10×10 五類 witness の pairwise shape 距離 (K1220 クラスの補完)

K1220 が格子同型意味で確定した 10×10 十石 witness の5類
(K0038・K0034-another・draft primary・draft sh7・v2.1) の
2類間の「shape距離」を機械計算した (records/pairwise-shape-dist-n10.json):
両岸の bounding-box を原点揃えし、片側の8つの D4 像で最小の
対称差 |A Δ g(B)| を取ると、**全10組で ∈ {14,16}、最小14**。
つまりどの2類も3手 (swap は石2個を動かすので7手) 以内では互いに移行できない
幾何学的な離隔がある。witness jump 現象 (SLSが既知 witness 間を少ないステップで
往復できないこと) と整合する数値的裏付け。
v2.1 類の座標は再生成 CNF (sha `95a5c4c9…`) を kissat 4.0.4 で解いた SAT モデル
から決定的に復号し、K1220 公刊の v2.1 witness と非順序集合として一致した
(kissat 4.0.4 の決定性の追加対照も兼ねる)。

## 7. 独立検証

- 6 seed 全件を `verify_witness.py` (整数 4×4 行列式・quartetカタログ非依存の公開検証器)
  で検証 (records/verify/):
  K0320-n11 (111/111 blocked)・n12 (133/133)・n13 (157/157)・W_c (133/133) は
  SAFE+MAXIMAL、wall12 は SAFE・uncovered=[(4,11),(5,11),(8,11),(11,11)]、
  plateau13 は SAFE・uncovered 6点 [(4,0),(12,0),(12,3),(12,8),(12,10),(12,11)]。
  wall の uncovered 集合は K1206/State の記録と完全一致する。
- ext_nets の決定性: 同一走査の再実行が (時間フィールド `ms` と
  ヘッダの `argv` を除いて) **byte一致** (wall r2a1 で検証済み)。
  また、25走査全部の totalChecked が §1 の組合せ恒等式と一致する。
- 環境リセット事故: 前セッション (〜06:00Z) の初回実行で得た全出力を
  実行環境の infra failure で喪失した。本 README の数値はすべて
  リセット後の再実行による (走査は決定的で、初回観測値の記録
  (構成数の全件一致・witness 0件) とも整合する)。事故の詳細は
  session log に正直に記録した。

## 8. 主張の範囲と限界

- 本実験の陰性はすべて「有界近傍 (remove ≤ 4 / add ≤ 2), sit-at込み」での
  不存在である。**非存在証明ではない**。特に s_11=9/8 の全域・
  s_12≤10・s_13≤11 の全域には一切言及しない。
- bestScore は状態の良さの指標であり、勝敗・探索費用ではない。
- "found=0" は「その近傍にwitnessがない」ことの完全証明 (有限列挙) であるが、
  checked 数そのものを成果として主張しない。
- r4a3 (remove-4/add-3) や10石→8石の深い近傍、n=11の全域探索は
  heavy lane の債務として残す (本実験の枝刈り: 構成数が恒等式
  C(k0,m)·C(n²−k0+m,a) で予測可能であることが chunked 実行の計画に効く)。

## 9. 再現

```sh
node scripts/ext_nets.mjs <n> <m> <full0|full1|full2> <out.jsonl> seeds/<seed>.json
# 例: n=11 K0320 witness 周囲の r3a2-full
node scripts/ext_nets.mjs 11 3 full2 out.jsonl seeds/k0320-n11.json
# 検証
python3 scripts/verify_witness.py witness.json
```

Node.js 22 で全25走査は約5分 (2コア・並列)。CNF 再生成は
`node enc_sat2.mjs <n> <k> --out=... --meta=...` (enc_sat2.mjs は s12-s13 SAT lane
kit / repo の s12-s13-sat-stabilization-20261122 実験に正本がある)。

## 10. ファイル一覧

- `scripts/`: ext_nets.mjs (本実験・新規) + hunt.mjs / census.mjs / witnesses.mjs /
  verify_witness.py (s12-s13 lane 正本と byte同一)
- `seeds/`: 6 seed (k0320-n11/n12/n13・wall12・plateau13・Wc12)
- `records/ext_*.jsonl`: 25走査の正本 (header: seed と恒等式、per-removal、done)
- `records/verify/`: verify_witness.py 出力 6件 (全空点証人つき)
- `records/sls/`: SLS honest negatives 3件
- `records/kissat-indet/`: 較正ログ (v3n7k6 UNSAT) + INDET 3ショット (240s) +
  cnf3gen-sha256.txt + CNF meta 7件
- `records/pairwise-shape-dist-n10.json`: 10×10 五類のpairwise対称差
- `MANIFEST-sha256.txt`: 上記全ファイルの sha256
