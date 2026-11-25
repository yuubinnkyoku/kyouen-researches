---
id: K1334
title: "供給恒等式族の完全閉形式特征付け: すべての k>=1・s>=0 で A_k(s)=v(s,k+1,k+1) は [0..k] で s%2・以降は k 偶奇で一定 (奇数 0・偶数 2)、B_k(s)=v(s,k,k+1) は [0..k−1] で s%2・B_k(k) は k 奇数 1・偶数 2・s>=k+1 では常に 1（よって恒等式 A=B の成立域は k 奇数で [0..k]・k 偶数で [0..k−1] であり、破れは k 奇数なら s>=k+1 で一様 (0,1)・k 偶数なら s=k で (0,2) の後 s>=k+1 で一様 (2,1)、uniformity は s に上限なし）（K0832 単一トークン閉形式の 4 場合分けによる engine-free 証明・機械照合 k∈{1..140}×s∈{0..300} 全 42,140 行で不一致 0・生 engine 再検証 canonical 45,000 行 + ordered 5,850 行不一致 0・出版 ninth〜fifteenth tail (k=18..24) と z17 partner (k=17) の恒等式行 614・strip spot 60・base spot 5 の全 679 行が全て定理値と一致・系 Lemma S: v(S,z,m+z+1)=(m+1)%2 (S>=max(z+1,m+2)) が K1332 base-spot 補題を m=z−5 インスタンスとして包括し、出版 strip spot・base spot の全実測値を先験確定・第16 tail (k=25) 以降の全スライスの事前計算と below-band A 側 v(s,z+1,z+1) が閉形式化・z18 kit の naive +2-shift 予測の失败は偶奇分裂の無視で説明〔K番号は仮・統合時再採番予定〕）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "Tail supply-identity family, complete closed-form characterization: for all k >= 1 and s >= 0, with A_k(s)=v(s,k+1,k+1) and B_k=v(s,k,k+1) (published K0832 single-token closed form), A_k(s)=s mod 2 on [0..k] and then constant 0 (k odd) / 2 (k even); B_k(s)=s mod 2 on [0..k-1], B_k(k)=1 (k odd) / 2 (k even), and B_k(s)=1 for ALL s>=k+1; so the identity A=B holds exactly on [0..k] (k odd) / [0..k-1] (k even), and the break is uniform in s with no upper cutoff: (0,1) forever past k+1 (k odd); (0,2) at s=k then (2,1) forever (k even). Engine-free proof by four-case branch computation on the K0832 closed form; machine cross-check 42,140 rows over k in {1..140} x s in {0..300}, zero mismatches; raw-engine re-validation 45,000 canonical + 5,850 ordered rows, zero mismatches; every published identity row (k=17..24, 614 rows), strip spot (60 rows) and base spot (5 rows) of the z18..z22 census kits sits exactly on the theorem. Corollary Lemma S: v(S,z,m+z+1)=(m+1) mod 2 for all z>=1, m>=0, S>=max(z+1,m+2), subsuming K1332 (m=z-5) and fixing the published strip/base-spot values a priori; the even/odd supply forms the census logs tally as observations (3/3, 4/4, ...) are one theorem's parity split."
relations:
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)=H(R;(x);z) と q_odd、枝構造 (z=0 / z=x / 1<=z<=x−1 / z>=x+1) が本項の全基盤。本項の定理 A・補題 S の証明は K0832 の場合分け計算のみで完結する。"
- type: related
  target: K1332
  note: "base-spot 格子パリティ補題 v(2z−10;z;2z−4)≡z (mod 2) は本項 Lemma S の m=z−5・S=2z−10 インスタンスとして包括される (条件 S>=z+1 ⟺ z>=11)。K1332 の証明済みスライス系 (T-Z15..T-Z19 の base-spot corollary) はそのまま有効。"
- type: related
  target: K1325
  note: "K1325 の補題 BB' (z17 partner 供給恒等式 v(s,18,18)=v(s,17,18) の有限域版) は本項の定数 A の k=17 インスタンス。本項は全 k・全 s に拡張した版。"
- type: related
  target: K1328
  note: "T-Z18 宣言が証明に用いた場合分け計算 (z18-note §187「K0832 の場合分け計算」で s∈{12..16} 域の ninth-tail 前計算) は本項の k=18 インスタンスの有限域版。"
- type: related
  target: K1138
  note: "残余ゲーム H(R;X;z) 再帰。本項の主張は崩壊値 v に対する閉形式族。H 値との一致 (below-band full collapse・spot 吸収) は各スライスの観測として別個に管理される。"
- type: related
  target: K1268
  note: "帯域公式 z*(m)=2m−2+(m mod 2) とは独立。Lemma S の格子線 R=m+z+1 はスライス帯域構造と直交する全称閉形式。"
artifacts:
- path: research/experiments/supply-identity-closedform-20261125/verify_k1334.py
  role: verifier
  note: "定理 A・補題 S の機械照合機体 (sha256 d0c751a2…・engine pin bd5f22e4… startup ゲート内蔵・出版 5 kit 凍結出力の pin を実行時に再検証)。section 構成 (a) engine_gate (b) lemmaA_grid 42,140 行 (c) lemmaS_grid (小域全列挙 31,850 行 + 広域 72,600 行 + 条件必要性 2,915 失敗記録) (d) k0832_revalidate (canonical 45,000・ordered 5,850 行) (e) cross_artifact 679 行 (f) 予測 k∈{25..32}。決定性 6 走 byte-identical (default x2・PYTHONHASHSEED=1・env -i 同一 cwd・env -i 隔離 dir・改番後再走)、rc 0 各走。"
- path: research/experiments/supply-identity-closedform-20261125/verify_k1334.out
  role: data
  note: "凍結出力 (sha256 63f7730f…・全 section の不一致 0 を含む)。"
- path: research/experiments/supply-identity-closedform-20261125/engine_block.py
  role: data
  note: "出版 chain engine 単体 (sha256 582c93c1…・startup pin bd5f22e4…)。K1282..K1332 chain と同一バイト。"
- path: research/experiments/supply-identity-closedform-20261125/README.md
  role: doc
  note: "kit README (section 説明・入力 pin manifest・決定性・caveats)。"
- path: research/experiments/strip-z18-min13-20261125/explore_z18f13.out
  role: data
  commit: f152a6f5
  note: "出版 z18 census 凍結出力 (sha256 c4e7757c…・k=17 z17-partner recheck 45 行・k=18 ninth precalc 45 行・strip spots m18..21 12 行・base spot 13 行の一次出典)。"
- path: research/experiments/strip-z19-min14-20261125/explore_z19f14.out
  role: data
  commit: 6a6832ce
  note: "出版 z19 census 凍結出力 (sha256 3354dfc6… 実測記録・k=19 tenth recheck 46 行・k=20 eleventh precalc 46 行・strip spots・base spot)。"
- path: research/experiments/strip-z20-min15-20261125/explore_z20f15.out
  role: data
  commit: 2cc16d34
  note: "出版 z20 census 凍結出力 (sha256 09e9026a…・k=20/21/22 の 47 行 x3・strip spots・base spot z=20)。"
- path: research/experiments/strip-z21-min16-20261125/explore_z21f16.out
  role: data
  commit: 8a106233
  note: "出版 z21 census 凍結出力 (sha256 10f94100…・k=21/22/23 の 48 行 x3・strip spots・base spot z=21)。"
- path: research/experiments/strip-z22-min17-20261125/explore_z22f17.out
  role: data
  commit: 115c0bb9
  note: "出版 z22 census 凍結出力 (sha256 f16a87d4…・k=22/23/24 の 49 行 x3・strip spots・base spot z=22)。"
- path: research/log/2026-11-25-supply-identity-family-closedform.md
  role: log
  note: "本項の一次記録 (手計算先行の順序記録・定理と証明概略・機械照合結果・出版観測との整合表・k=25 以降の予測・事前調査と K 番号仮の開示)。"
---

# K1334: 供給恒等式族の完全閉形式特征付け (engine-free)

## 主張

記号: v は K0832 単一トークン閉形式 v(x,z,R)=H(R;(x);z)、
q(t)=q_odd(t)。各 k>=1・s>=0 に対し A_k(s):=v(s,k+1,k+1)、
B_k(s):=v(s,k,k+1) とおく (スライス z の census kit は組
v(s,z+1,z+1)=?v(s,z,z+1) を「tail 供給恒等式」として掃引する;
z=k なので組は (A_k,B_k) に一致する)。

**定理 A (全称、k>=1・s>=0)**:

- A_k(s) = s mod 2 (0<=s<=k)。s>=k+1 では A_k(s) は s に依らず
  k のみで決まり、k 奇数のとき 0、k 偶数のとき 2。
- B_k(s) = s mod 2 (0<=s<=k−1)。B_k(k) = 1 (k 奇数) / 2 (k 偶数)。
  s>=k+1 では B_k(s) = 1 (k 偶奇によらず、s に上限なし)。

**帰結 (恒等式の成立域)**: A_k=B_k の成立域は k 奇数なら
[0..k] (共通値 s mod 2)、k 偶数なら [0..k−1] (共通値 s mod 2)。
成立域の外では k 奇数: (A,B)=(0,1) がすべての s>=k+1 で一定、
k 偶数: s=k で (0,2)、s>=k+1 で (2,1) が一定 — すなわち
「tail 平坦部」の定数は全称かつ無限遠まで確定する。

**補題 S (strip 格子線、全称)**: z>=1・m>=0・トークン和
S>=max(z+1, m+2) ならば v(S, z, m+z+1) = (m+1) mod 2
(R=m+z+1 は T-Zz 番号の格子線)。値は S に依らず R と z のみで
決まる ((R+z)%2 の S 独立性)。

## 証明 (K0832 の場合分けのみ・engine-free)

K0832 の枝を (E0) x<=0 または R=0 → 0。(E1) z=0 → min(R,x)%2。
(E2) z=x → R 偶かつ R<=x−1 で 0、R 奇かつ R<=2x−1 で 2、
それ以外 x%2。(E3) 1<=z<=x−1 → m=q(z)、R<=m で R 偶 0/奇 2、
m<R<x+z で (R+z)%2、R>=x+z で x%2。(E4) z>=x+1 → m=q(x)、
R<=m で R 偶 0/奇 2、それ以外 x%2、と置く。

**定理 A**。A_k(s)=v(x=s, z=k+1, R=k+1)、B_k(s)=v(x=s, z=k,
R=k+1) の 4 場合:

(I) 0<=s<=k−1: A は E4 (q(s)<=s<=k−1<k+1=R なので R>q(s))
より x%2=s%2。B も E4 (z=k>=s+1、q(s)<=s<k+1) より s%2。
ゆえに A=B=s%2。

(II) s=k: A は E4 (z=k+1>=x+1=k+1、q(k)<=k<R) より k%2。
B は x=z=k で E2: R=k+1。k 奇数なら R 偶で R<=k−1 は偽 →
x%2=1。k 偶数 (k>=2) なら R 奇で R<=2k−1 ⟺ k>=2 → 2。
ゆえに (A,B)=(k%2,1) (k 奇) / (0,2) (k 偶)。k 奇のとき
両者とも 1=s%2 なので成立域は s=k まで伸びる。

(III) s=k+1: A は x=z=k+1 で E2: R=k+1。k 奇 → R 偶、R<=k
は偽 → x%2=0。k 偶 → R 奇、R<=2k+1 成立 → 2。B は
z=k<=x−1=k で E3: m=q(k) (<R=k+1、k 偶なら m=k−1<R、
k 奇なら m=k<R)、R<x+z=2k+1 (k>0) → (R+z)%2=(2k+1)%2=1。
ゆえに (A,B)=(0,1) (k 奇) / (2,1) (k 偶)。

(IV) s>=k+2: A は E3 (z=k+1<=x−1=s−1): k 奇なら m=q(k+1)=k<R
かつ R<x+z → (R+z)%2=(k+1+k+1)%2=0。k 偶なら m=q(k+1)=k+1>=R
なので第一分枝、R=k+1 奇 → 2。B は E3 (z=k<=x−1): m=q(k)<R
かつ R<x+z=k+s → (R+z)%2=(k+1+k)%2=1。

(II)(III)(IV) を併せ、s>=k+1 での (A,B) が s に依存しない
定数であることが各場合で枝選択が s によらず確定することから
従う (いずれの枝条件も s>=k+2 で s の増加によってしか変わら
ず、R・z は固定)。∎

**補題 S**: x=S とおく。S>=z+1 より 1<=z<=x−1 (E3)。q(z)<=z<
z+m+1=R (m>=0)。R<S+x=S+z ⟺ m+1<S ⟺ S>=m+2。ゆえに E3 の
中間枝 m<R<x+z が選ばれ v=(R+z)%2=(m+z+1+z)%2=(m+2z+1)%2=
(m+1)%2。∎

(z15/z16 世代の kit に k=15, k=16 の恒等式行も出版されている
が、それらの行も本定理の成立域内にあり、機械照合グリッド
(k=1..140) が同一の評価関数を全列挙している。)

## 系 (出版観測の位置づけ)

1. **K1332 の包括**: 補題 S の m=z−5、S=2z−10 インスタンス
   (条件 S>=z+1 ⟺ z>=11) として v(2z−10;z;2z−4)=(z−4)%2=
   z%2 が再現される。K1332 の証明済みスライス系・観測の
   位置づけは変更なし。
2. **出版恒等式の全行一致**: ninth〜fifteenth tail (k=18..24)
   と z17 partner (k=17) の全恒等式行 614 行 (出版 5 kit の
   13 セクション) が定理値と完全一致 (機械照合・入力は sha
   pin 検証済み)。各 kit が記録してきた「even-z form 3/3・
   4/4」「odd-z form 3/3」の計数は本定理の偶奇分裂の有限
   観測にすぎず、z18 kit の naive「+2-shift・1v0」予測の
   失敗も分裂の無視で説明される。
3. **strip spot・base spot の先験確定 (崩壊側)**: 出版 60
   strip spot 行・5 base spot 行の collapse 値は成立域内で
   定理により (m+1)%2 と先験確定され、全行一致。H 側の
   一致 (match) は各スライスの観測。
4. **below-band A 側の閉形式化**: スライス z の below-band
   供給源 v(s,z+1,z+1) は定理 A の A_z そのもの: s%2
   (s<=z)、以降 k=z の偶奇で 0 (z 奇) / 2 (z 偶)。出版
   5 kit の below-band「完全崩壊 0 deviants」観測
   (H(z+1;Y;z+1)=A_z(s)) と整合し、以後のスライスの
   below-band 列挙は A 側を閉形式で確定した上で H 側一致
   の確認のみとなる。
5. **将来の census 事前計算の先験確定**: 第16 tail 以降
   (k>=25) の全対 (hold 域・破れ位置・破れ定数・平坦部
   定数) は定理により機械実行前に確定する (k=25: hold
   [0..25]、s>=26 で一様 (0,1)。k=26: (0,2)@26、(2,1)@27+。
   k∈{25..32} の表は凍結出力 section (f) 収録)。

## 機械照合 (kit verify_k1334.py)

- 定理 A: k∈{1..140} × s∈{0..300} 全 42,140 行、不一致 0。
- 補題 S: 小域全列挙 (z,m∈{0..20}、S∈{1..90}) 成立域内
  31,850 行不一致 0・広域 (z,m∈{0..120}) 境界点 72,600 行
  不一致 0・成立域外 5,950 行中 2,915 行で公式が破れ、
  2 条件が必要性を持つことを記録 (成立域外は無主張)。
- K0832 転写再検証: 生 canonical engine に対し
  x∈{1..30}×z∈{0..24}×R∈{1..60} 全 45,000 行・ordered
  engine 部分域 5,850 行、不一致 0。
- 出版キット横断: 5 kit 凍結出力 (z18 c4e7757c…/z20
  09e9026a…/z21 10f94100…/z22 f16a87d4… は実行時に sha
  pin 再検証、z19 は 3354dfc6… を記録) の恒等式 614 行・
  strip spot 60 行 (collapse 再計算含め全一致)・base spot
  5 行、合計 679 行、不一致 0。
- 決定性: 改番前 5 走 + 改番後 1 走の計 6 走 byte-identical
  (default x2・PYTHONHASHSEED=1・env -i 同一 cwd・env -i 隔離
  dir・名称変更後再走)、rc 0。

## 限界

- 本項の全称主張は崩壊値 v に対するもの。H 値への主張
  (恒等式それ自体は v の性質だが、census における below-band
  崩壊や spot 吸収の H=v 一致) は各スライスの観測のまま。
- K0832 閉形式自体の妥当性は K0832 が担う (本項はその系;
  転写は生 engine との 45,000+5,850 行再検証で防禦)。
- z15/z16 世代 kit の恒等式行は本実行では再解析していない
  (同一評価関数を k=1..140 で全列挙した機械照合が覆う)。
- 盤面 verdict とは無関係 (11×11 空盤・二石 root・S2・
  class 1/2/4 すべて UNKNOWN のまま・verdict 不消費)。

## honest 記録

- **K 番号 1334 は仮** (統合時再採番予定。repo には既に
  K1330 の二重採番が存在)。
- **採番の経緯 (push 直前再取得での競合発見)**: 当初 K1333 を
  採番した。執筆時点の確認では code search (K1333: 0 件)、
  list_commits、items/ 実パス probe いずれも空きを示したが、
  push 直前の最新 main 再取得で、並走レーン (PG(2,9) cap
  Grundy・commit 3ce3dda5・19:39:44Z) が同じ番号 K1333 を別
  内容 (.localized parity theorem) で採番済みと判明した
  (その直後に YAML 修復 8c5fa531 も存在)。番号を K1334 に
  変更した。K1331 の索引遅延 (K1332 の経緯) と同様、分単位
  の並走出版との採番競合は常態であり、push 直前の最新 main
  再取得が唯一の防禦であることを再確認する事例となった。
  なお内容面の重複はなし (供給恒等式族の閉形式特征付けは
  本項が初出)。
- **事前調査**: 2026-11-25 時点で repo 全域 code search
  ("supply identity" in research/knowledge/) は K1328 と
  K1330 の 2 項目のみを返し、いずれも恒等式を宣言内部の
  有限域前計算・観測として記録する。知識項目としての
  族全称特征付け (偶奇分裂・無限遠 uniformity・成立域の
  完全決定) は本項が初出。
- **導出順序**: K1320/K1321/K1325 式の手計算先行順序に
  従い、定理 A と補題 S の紙面導出 (K0832 の 4 場合分け)
  が機械照合・キット横断解析の前に完了している。
- 証明は K0832 が出版済みの全称閉形式への純代数計算であり、
  機械照合は手計算の転写ミス防禦と生 engine 一致の再確認で
  あって証明の代替ではない。
