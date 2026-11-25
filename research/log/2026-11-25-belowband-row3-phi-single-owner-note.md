# 単一オーナー宣言ノート: 下帯第3行 (m,W)-Φ ラダー幾何の凍結 battery (K1318・observation packet) — 高速レーン 2026-11-25

## §0 プリアンブル

本ノートは K1315 の次課題2「ラダー幾何の一般化」で仮採番 **K1318** を単一オーナー
宣言する。対象は凍結測定 battery (explore_k1318.py/.out) とそれが記録する観測
パケット (合成分解・2再帰・壁則・tier・深層線形・floor 観測) の出版 chain のみ
であり、標準 11×11 盤の anything は一切主張しない (全局面 UNKNOWN・verdict 不消費)。

採番は仮 (K1318)。作業は AGENTS.md 規約に従い main に直接反映し、branch / PR は
作らない。**探索一次資料は先行出版済み** (publish-then-execute: 宣言前探査の
全開示):

- 探査 log `research/log/2026-11-25-belowband-row3-phi-tables-exploration.md`
  (commit `fe9492e6`、誤記専用修正 `260abb13`)。同 log の「次回実行の凍結・出版計画」
  §が本 chain の設計書であり、測定の未完リスト 1–6 と電池設計 (i)–(vi) を申送り済み。
- 対抗確認: 最新 main (`b7f014d3` 時点) で K1318 slot・belowband-row3-phi kit の
  宣言・出版は他実行に存在しない。並走の z15-min10 predecl (`f547c174`) とは直交。

ハンドオフからの变更点を先に要約する (詳細は §6): 前セッションは電池初回走の後、
実行環境障害でローカルワークスペース (機体・出力) を喪失した。repo 出版物
(探査 log・K1315 kit) から機体を再構築し、再構築時に判明した 3 点
(tier/pair 境界条件 `>`→`>=`、D3 ペア表記の target m=10 誤記 (m=9 が正)、
深層集計の族分離) を凍結機に織り込んだ上で predry 2 走 byte-identical を確認した。
さらに predry で判明した **族公式の m'≤5 開放域** (公式は負に発散するが実測は
flat 0) も凍結仕様に昇格した (revision note (e))。

## §1 主張 (観測パケット・全称なし)

本パケットが記録するのは以下の凍結測定であり、**いずれも観測等級**
(掃引 z 窓・構成表上の測定) である。全称定理は 1 つも含まない。法則形の全称昇格は
K item で CONJ-BBL3-A (conjecture grade) として登録し、閉形式の証明は O-Φ open。

- **OBS-BBL3-PHI/D1 (合成分解・family level)**: 下り heap 多重集合 X・n=|X|・
  E:=2·max−Σ・j:=#1-heap・m:=n−j・W:=X の {2,3,4} 部分語、族アンカー行
  (窓内に単一 2 をもつ行の z2 位置 A:=E+z2) について
  **A(n,j,W) = η(n) + 2j − 2Φ(m,W)、η(n) = −5(n−4)、m = n−j** が測定行の
  全てで成立 (本凍結: WJ 合成 237 行適合・違反 0・conform_bad 0・パリティ異常 0)。
- **D3 (2再帰)**: Φ([2^a V], m) = Φ(V, m−a)、17 ペア fresh 再計算で違反 0
  (ハンドオフ誤記ペア [223]@11→[3]@9 修正後、§6 参照)。
- **D2 (tier)**: m=6: Φ≡0 (全語掃引 56 語×j0/j1、rule_bad 0)、
  m=7: c2≥1→0 / else 1 (84 語×j0/j1、rule_bad 0)。境界仕様 A_pred==E (z2=0)
  は可視行として測定 (revision note (a))。抑圧行は no-2 整合 (supp_inconsistent 0)。
- **D4/D5 (基礎族閉形式・壁則)**: 純 [3^b] 族 Φ = T_{m−6−b}+b (T_{−1}:=−1;
  κ≤−2 は線形 tier **Φ = m−6**、深層 probe 全 30 測定が線形適合) /
  純 [4^c] 族 Φ = (m−6 if m≤7 else T_{m−7}+2) − Σ_{i<c−1}(m−9−i)_+ /
  混合 [3^b 4^c] 壁則 q=c, t=8+b, Δ=Σ_{i<q}(m−t−i)_+。基礎表 51 行 fresh 再計算
  適合 0 mismatch。
- **D6 (事前予測)**: 12 行 (m12 battery + 2-strip host 3 行) 全て HIT
  (WF bad 0)。ハンドオフ掲載の予測値と全一致。
- **D7 (壁下抑圧算術)**: 予測 A<E ⇒ no-2。7 行 (D7 の 6 行 + 新規宣言行
  [4444]@12 F=7) 全て suppressed_consistent・plateau 違反 0。
- **深層 floor 観測 (新規・凍結 predry で発見)**: 2-strip 後の標的 m'≤5 では
  族公式は**負値に発散する**が (例: [24]@6 → Φ([4],5) = −1 と公式値)、実測は
  **全族で Φ = 0 の平坦 floor** (floor probe 54/54・違反 0)。公式の適用域は
  m'≥6 で閉じ、m'≤5 は開放域 (tier 行が m=6/7 での支配則)。
- **直接測定 (前セッション OOM 未達分)**: Φ([33],12)=12 (j-shift 構成
  理由は §6)、Φ([],11)=15 (F=8)、Φ([3^7],11)=5・[3^8]@12=6・[3^6]@10=4・
  [3^7]@10=4・[3^6]@9=3 (以上、線形 tier κ≤−2 の直接 fresh 測定、全て = m−6)、
  Φ([3^6],10)=4 はハンドオフが「j-shift 構成では到達不能」と申送りした行の
  測定達成 (F=10 構成で可視)。

## §2 定義と規約

- エンジン: K1138 転写 chain と同一 bytes (埋込み pin
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`、
  単体 engine_block.py sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`、
  K1282..K1319 chain 同一 bytes)。H_canonical / H_ordered / single_token 同梱。
- 行: k = z+n−5 (下帯第3行)、値 H_canonical(S+z+n−5, X, z)、窓 [0, zwin]、
  アンカー抽出は「窓内 2 がちょうど 1 つ」の行のみ (tier grade)。窓内 2 が
  2 つ以上の行は multi2 観測として記録 (凍結走では 0 行)。
- 構成規則 (fresh freeze・決定的): 各行の filler F は予測 z2 = A_pred − E が
  [0..3] に入る最小の F ∈ [5..17] (不可なら [0..10] に拡大)。ただし WH 行と
  WG 宣言行はハンドオフ明記構成 (§6 の修正 2 件を含む)。filler≥5 inert は
  D1/WB (7 ペア: F 交差 5・j 交差 1・深層構成支持 1) で battery 内で再検証。
- Φ法則の適用域宣言: strip (m'=m−a) 後 m'≥6 のみ closed-form 有効、
  m'≤5 は開放域 (flat 0 floor 観測)。tier 規則は非 strip の m∈{6,7} 行を支配。

## §3 凍結探索 (explore_k1318.py / .out)

- `explore_k1318.py` sha256 `58b9c71e7b88070cb919bd900aaf6541329055aa29397b26c1f916168274c47f`
- `explore_k1318.out` sha256 `cac6024207c91881960410def67930d29b890dea20431b9e719d0dd469902459` (140,634 bytes・決定的 JSON)
- 波と宣言行数 (ハンドオフ設計 (i)–(vi) + pending + 深層):
  **WA** engine sanity 150 セル PASS / **WB** F・j 不変 7 ペア (bad 0) /
  **WC** tier 掃引 m=6・112 行 + m=7・168 行 (rule_bad 0・supp 0・jshift 0・
  multi2 0) + 証人 n=10,j=4 7 語 (6 測定 A=−22、[333] は z2=−1 の
  suppressed_consistent) / **WD** 2再帰 17 ペア fresh (bad 0) /
  **WE** 基礎族表 D4+D5 全 51 行 (mismatch 0) / **WF** D6 事前予測 12 行
  (bad 0) / **WG** 抑圧 7 行 (bad 0) / **WH** ハンドオフ未完 p1–p6b 7 行
  (bad 0・p5 が線形 tier κ=−2 の直接測定 Φ=5=11−6) / **WI** 深層 probe 10 行
  (bad 0、[3^6]@10 測定達成、[]@11=15、[]floor/[4]@[6,7] 含む) /
  **WJ** 合成一致: 行 415・測定 291・agree 237・violations 0・conform_bad 0・
  parity 0・law_open 140・suppressed 38 / **WZ** 深層集計 (族分離):
  純 [3^b] probe 38 中測定 30 全て線形適合 (κ=−1..−4)、floor probe 140 中
  測定 54 全て Φ=0。
- 凍結前 predry: 再構築機体 2 走 (走1: cwd・走2: env -i 隔離 +
  PYTHONHASHSEED=12345) byte-identical (上記 .out sha)。約 4 分/走
  (ulimit -v 900000)。

## §4 機体宣言 (publish-then-execute)

- kit `research/experiments/belowband-row3-phi-20261125/` に
  `engine_block.py` (byte-clone・sha 上記) + `explore_k1318.py` + 凍結
  `explore_k1318.out` + `README.md` を出版 (本宣言の直後の commit)。
- `verify_k1318.py` (別 commit): engine pin ゲート + 埋込み pin 定数 +
  全電池 fresh 再計算 witness ~25 行 (重い行 pending1/6a/5・[3^8]@12 F=14・
  [3^6]@10 F=10・[]@11 F=8・WG []@12 no-2 含む) + .out sha・内容照合 +
  tamper 電池 (--tamper-engine rc 2 / --tamper=* rc 1 系・fail-closed)。
  宣言点数・期待 bad は機体 docstring に全文宣言。
- 公式実行: explore 4 走 (同一 cwd 2 走 + env -i 隔離 2 走・別
  PYTHONHASHSEED、出版社 .out と byte 一致必須) + tamper 電池実行。
  記録を `output/detcheck.json` + `MANIFEST-sha256.txt` として出版。

## §4.5 主張の区別

- D1–D7・深層・floor はすべて**凍結構成表・掃引窓上の観測**。構成外
  (F>17・z>zwin・語外 W (heap ≥5 の種類違い mix を含む)・n>13) への射影は
  **CONJ-BBL3-A の予想のみ** (K item で登録)。
- 閉形式 (T/壁/線形) の証明や floor の一般測定は本 chain の範囲外 (O-Φ open)。
- 11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・verdict 不消費 (定型)。

## §5 open 登録・次課題

1. **O-Φ (閉形式昇格)**: 純 [3^b] T式+線形 tier・[4^c] 底式・混合壁則の全称
   証明 (typed-children 帰納の row3 版・K1314 row2 との接続)。
2. **m'≤5 floor の一般化**: flat 0 floor が全語族で成り立つかの追加測定
   (本凍結は m=6/7 tier 掃引由来の 54 行)。負公式値との食い違いの構造説明。
3. **multi2 プロトコル**: 窓内複数 2 行の族分類 (凍結走では出現 0 行、
   再構築前の走では境界偽陽性由来のみ)。出現条件の調査。
4. **F 大値の慣性検証拡大**: F∈{13..17} 構成への直接依拠 (WB/FLOOR 行は
   F 交差対で battery 内支持) を F 交差対の追加で強化。
5. **11×11 接続 (別レーン)**: Φ表+壁則が下帯 row-3 の family 別安定化長の
   パラメータ化を与える。枝刈り利用メモは K item に含める。

## §6 honest 経緯

1. **ハンドオフ誤記 2 件の検出と修正**: (1) D3 ペア表記 [223]@11→[3]@10:
   2再帰則と同 log の "( =4)" 注記から m=9 が正 (Φ([3],9)=T_2+1=4)。
   初回走が忠実に m=10 で再計算して違反を検出、凍結仕様は m=9。(2) 未完 #3 の
   E=−57 は X=(8^7,3^5) の真の E=−55 の誤記 (z2=3 で可視、測定は E=−55 で
   実施)。なお D4 [4] 行の m8/m9 A 注記は先行の誤記修正 commit `260abb13`
   (typo-only) で既に正本化済み。
2. **未完 #6a 構成の不整合**: log 掲載 X=(7^7,4,4,4,3,3) は要素数 12 (n=12)
   だが (m=11, j=0) の主張と整合しない。正構成 X=(8^6,4,4,4,3,3) (n=11,
   F=8) で測定し予測 Φ=7 に HIT。battery 内で明示訂正して記録。
3. **ワークスペース喪失と再構築**: ハンドオフ元セッション同様、本 chain の
   準備中にも実行環境リセットによりローカル機体・出力を喪失した。repo 出版物
   (探査 log・K1315 kit) から再取得・再構築 (engine sha/pin 一致を確認) し、
   凍結正本は再構築後に全て作成。喪失したのは中間産物のみで、repo 側は無影響。
   **初回再構築走そのものは出版していない** (revision note (a)–(c) 適用後の
   機体が凍結正本)。
4. **revision note (凍結機体 docstring に全文宣言)**: (a) tier/pair/WG の
   可視判定を `A > E` から `A >= E` に修正 (A==E は z2=0 の可視境界行;
   旧仕様の supp_inconsistent 22・jshift_bad 23 は境界偽陽性);
   (b) D3 ペア spec 修正 (上記・§6.1); (c) WZ 集計の族分離; (d) 再構築の
   全開示; (e) m'≤5 開放域の凍結 (predry で 44 rule 行 + 12 jshift 行が
   全て「公式負値 vs 実測 0」だったことが確定根拠); (f) multi2 プロトコルと
   証人 [333] z2=−1 の抑制整合記録。
5. **WB []@11 F=9 の OOM**: F 不変ペアの第 2 脚 F=9 が sandbox (~1GB)
   で OOM。同値主張の等価表現として j-shift 脚 (j=1, F=8, A=−68→Φ=15)
   に差し替え (D1 の j 不変性主張の fresh 検証を兼ねる)。slot F=9 の直接
   再挑戦はしない (Actions 7GB 環境は後続課題)。
6. **[33]@12 は j=1 構成で測定**: 未完 #1 の通り X=(8^10,3,3,1) (n=13,
   E=−71, A=−67, z2=4)。j=0 構成 (X=(8^10,3,3)) も公式上可視 (z2=6) だが
   ハンドオフ宣言構成を尊重し j-shift 行を採用・記録した。
7. **predry 2 走の時点**: 本ノート push 時点で既に完了・byte-identical
   確認済み (sha §3)。公式 4 走は kit 出版後に出版 bytes に対して実行する。

以上
