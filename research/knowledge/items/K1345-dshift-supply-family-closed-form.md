---
id: K1345
title: "d-shift 供給族の閉形式特征付け: すべての k>=1・d>=1・s>=1 で A=v(s,k+d,k+d) は [1..k+d−1] で s%2・以降は k+d 偶奇の定数 (奇 2・偶 0)、B=v(s,k,k+d) は [1..k−1] で s%2・s=k で (k+d 奇かつ d<=k−1 のとき 2・それ以外 k%2)・[k+1..d] で s%2・s>=max(k+1,d+1) で一様 d%2 (s 上限なし)、恒等式 A=B の成立域は [1..k−1] ∪ ({k}: k+d 偶 or d>=k) ∪ [k+1..d] ∪ 縞 zone {s∈[max(k+1,d+1)..k+d−1]: s≡d (mod 2)} ∪ (一様 tail: k・d が共に偶のとき [k+d..∞)) で完全決定され、破れは (k%2,2)@遅延破れ・((d+1)%2,d%2)@縞・一様 tail (0,1)/(2,0)/(2,1) のみ (K0832 単一トークン閉形式の枝計算 (E0)-(E4) による engine-free 証明・機械照合 1,209,600+2,660+764+98,200 点不一致 0・d=1 スライスは K1334 定理 A と同一を 98,200 点で機械確認・d=2 では even-k が全直線でただ一點 s=k+1 の破れ (1,0) の後に (0,0) が恒久成立・odd-k (k>=3) は s=k+1 に (0,0) の孤島 hold を持つ〔K番号は仮・統合時再採番予定〕)"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "d-shift two-supply family, complete closed-form characterization: for all k >= 1, d >= 1, s >= 1, the advance seat A = v(s,k+d,k+d) (published K0832 single-token closed form) equals s mod 2 on [1..k+d-1] and then the k+d-parity constant 2 (k+d odd) / 0 (k+d even) forever; the lagging seat B = v(s,k,k+d) equals s mod 2 on [1..k-1], equals 2 at s = k iff (k+d odd and d <= k-1) and k mod 2 otherwise, equals s mod 2 on [k+1..d] (iff d >= k+1), and equals d mod 2 for all s >= max(k+1,d+1) with no upper cap; hence the identity A = B holds exactly on [1..k-1], at s = k iff (k+d even or d >= k), on [k+1..d], on the striped zone points s = d (mod 2) in [max(k+1,d+1)..k+d-1], and on the whole uniform tail [k+d..infinity) iff k and d are both even; the uniform-tail break pairs are (0,1) (k,d both odd), (2,0) (k+d odd, d even), (2,1) (k+d odd, d odd). For d = 2: even k fails at exactly ONE point of the whole line (s = k+1, pair (1,0)) and holds (0,0) forever from s = k+2; odd k >= 3 holds [1..k-1] and the ISOLATED island s = k+1 with (0,0) between the (1,2) lag break and the (2,0) uniform break. Engine-free proof by branch computation on the K0832 closed form (full written case analysis in the experiment README); machine corroboration 1,209,600 grid + 2,660 large-s + 764 raw-engine seat points + 98,200 d=1-instantiation points, zero mismatches, determinism 6/6 byte-identical; the d=1 slice machine-matches K1334 Theorem A (and the published single-token theorem kit) on 98,200 points; the B-uniform piece is the K1334 Lemma S lattice fact at m = d-1 (Lemma S stays canonical in K1334). Closes open structural question (a) of research/log/2026-11-26-single-token-tail-supply-identity-theorem.md."
relations:
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)=H(R;(x);z) と q_odd、枝構造 (E0)-(E4) が本項の全基盤。証明は閉形式の枝計算のみで完結する (engine-free・実験 README に全証明収録)。"
- type: generalizes
  target: K1334
  note: "d=1 スライスは K1334 の定理 A (および 2026-11-26 出版の単一トークン恒等式定理キット) に一致することを 98,200 点で機械確認 (d1_instantiation_audit)。本項は恒等式側を d>=1 に拡張する。K1334 の補題 S は本項の B 側一様部の m=d−1 インスタンスに相当し、格子線補題の正典は K1334 に残る (K1334 側からも related 追記済み)。"
- type: related
  target: K1138
  note: "残余ゲーム H(R;X;z) 再帰。本項の主張は崩壊値 v に対する閉形式族で、H 値との一致 (engine 転写) は 764 座席の spot 検証と各 kit battery による標本確認 (正面からの再証明ではない)。"
artifacts:
- path: research/experiments/dshift-supply-family-theorem-20261126/verify_dshift_theorem.py
  role: verifier
  note: "機械照合機体 (sha256 15040ba4…・engine pin bd5f22e4… startup ゲート内蔵)。section 構成 (1) engine_gate (2) 閉形式 grid k∈{1..400}×d∈{1..12}×s∈{1..k+d+45} 1,209,600 点 (3) 領域分類 (I1-I5 独立 classifier) (4) 広域 2,660 点 (s は k+d+5000 まで) (5) engine spot 764 座席 (canonical+ordered 両 engine・両座席) (6) d=1 一致 98,200 点 (出版単一トークン定理の derived(s,k) verbatim 転写との照合) (7) s=0 degenerate 記録 (8) d=2 族記録。決定性 6 走 byte-identical (default x2・PYTHONHASHSEED=random・env -i 同一 cwd・env -i 隔離 dir・env -i + PYTHONHASHSEED=1 隔離 dir)、rc 0 各走。"
- path: research/experiments/dshift-supply-family-theorem-20261126/verify_dshift_theorem.out
  role: data
  commit: 254e397a57832b815f24f539ef85f24342899cf2
  note: "凍結出力 (sha256 87f0c951…・全 section の不一致 0 を含む)。"
- path: research/experiments/dshift-supply-family-theorem-20261126/engine_block.py
  role: data
  note: "出版 chain engine 単体 (sha256 582c93c1…・startup pin bd5f22e4…)。全 strip kit chain と同一バイト。"
- path: research/experiments/dshift-supply-family-theorem-20261126/README.md
  role: proof
  note: "定理・恒等式領域・全証明 ((E0)-(E4) 場合分けの紙面全記録)・d=1/d=2 の系・機械照合・caveats。"
- path: research/log/2026-11-26-dshift-supply-family-theorem.md
  role: log
  commit: 254e397a57832b815f24f539ef85f24342899cf2
  note: "本項の一次記録 (paper-first 順序・slot check・§5 handoff: open question (b) は未解決のまま登録)。"
---

# K1345: d-shift 供給族の閉形式特征付け (engine-free)

## 主張

記号: v は K0832 単一トークン閉形式 v(x,z,R)=H(R;(x);z)、
q(t)=q_odd(t)。k>=1・d>=1・s>=1 に対し A:=v(s,k+d,k+d)、
B:=v(s,k,k+d) とおく。

**定理 D-A (全称)**: A は [1..k+d−1] で s mod 2、s>=k+d では
s に依らず k+d のみで決まる定数 (k+d 奇のとき 2・偶のとき 0)。

**定理 D-B (全称)**: B は [1..k−1] で s mod 2、s=k では
「k+d が奇 かつ d<=k−1」のとき 2・それ以外は k mod 2、
[k+1..d] (d>=k+1 のとき非空) で s mod 2、s>=max(k+1,d+1) では
s に上限なく一様に d mod 2。

**恒等式領域 (全称)**: A=B の成立域は
[1..k−1] ∪ ({k}: k+d 偶 or d>=k) ∪ [k+1..d] ∪
{s∈[max(k+1,d+1)..k+d−1]: s≡d (mod 2)} ∪
([k+d..∞): k・d 共に偶) で完全決定され、成立域外の値は
遅延破れ (k%2,2)@s=k、縞破れ ((d+1)%2,d%2)、一様 tail の
(0,1) (k,d 共に奇)・(2,0) (k+d 奇・d 偶)・(2,1) (k+d 奇・d 奇)
のみで、いずれも s に依存しない。

**d=1 との関係**: d=1 スライスは K1334 定理 A (および出版
単一トークン恒等式定理) と同一であることを 98,200 点で機械照合
(定理 D-A の [1..k] hold・k 偶 (0,2) 遅延破れ・一様 (2,1)/(0,1)
tail が再現)。**d=2 (質問 (a) の文字通りの組)**: k 偶は全直線で
ただ一点 s=k+1 のみ破れ (1,0) で以後 (0,0) が恒久成立、k 奇
(k>=3) は s=k+1 に (0,0) の孤島 hold を持ち (遅延破れ (1,2) と
一様破れ (2,0) に挟まれた d=1 族には現れない hold-set 位相)、
k=1 は [1..2] hold の後 (2,0) 一様破れ。

B 側一様部は K1334 補題 S の格子線事実の m=d−1 インスタンス
(R=(d−1)+k+1) に相当する。

## 証明 (K0832 の枝計算のみ・engine-free)

閉形式の枝 (E0)-(E4) に対する場合分け。全文は実験 README
(artifact) 収録。骨子:

- A 側: s<=k+d−1 では E4 (z=k+d>=x+1) で m=q(s)<=s<R=k+d
  より A=s%2。s=k+d では E2 で R=x のため R 奇なら R<=2x−1 が
  必ず成立して 2、R 偶なら x%2=0。s>=k+d+1 では E3 で
  m=q(k+d) が (k+d 奇のとき) R と一致して第一枝 R 奇→2、
  (k+d 偶のとき) R より 1 小さく中間枝 (R+z)%2=(2(k+d))%2=0。
  いずれも s 非依存。
- B 側: s<=k−1 は E4 で s%2。s=k は E2 で R=k+d・x=z=k:
  R<=x−1 は d>=1 で不可能、R 奇 (k+d 奇) かつ R<=2k−1
  (d<=k−1) で 2、それ以外 x%2=k%2。s>=k+1 は E3 で
  m=q(k)<R=k+d、中間枝の条件 R<s+k (s>d) から s>=d+1 で
  (R+z)%2=(2k+d)%2=d%2、k+1<=s<=d で第三枝 x%2=s%2
  (s=d では R=x+z で値は同一につなぎ目なし)。
- 恒等式: 各 zone で A・B の閉形式値を直接比較 (成立域・
  破れ組の完全決定・README の証明末尾)。

機械照合は転写ミス防禦と engine 一致の標本確認であって証明の
代替ではない。

## 機械照合 (kit verify_dshift_theorem.py)

- 閉形式 grid: k∈{1..400}×d∈{1..12}×s∈{1..k+d+45} の
  1,209,600 点、定理 D-A/D-B ペア不一致 0。
- 領域分類 (I1-I5 の zone label を定理幅主張から独立に構成した
  classifier との照合、同 grid): 不一致 0・ラベル計数
  I1 957,600 / lag_break 2,364 / I2_hold_k 2,436 / I3_hold_mid
  286 / I4_striped_hold 13,039 / I4_striped_break 13,075 /
  I5_uniform_hold 55,200 / I5_uniform_break {deven,dodd,oddodd}
  各 55,200。
- 広域: d∈{2,3,4,5,8,13,21}×k∈{1,2,3,44,45,99,100,101,199,200}
  s は k+d+5000 まで 2,660 点、不一致 0。
- engine spot (canonical・ordered 生 engine・両座席): 完全
  k∈{1..8}×d∈{1,2,3,5}×s∈{1..k+d+6} + 境界標本列、764 座席、
  不一致 0 (閉形式==engine 転写の標本確認)。
- d=1 一致: 出版単一トークン定理の derived(s,k) (verbatim 転写)
  と d=1 スライスを k∈{1..400}×s∈{1..k+45} で照合、98,200 点、
  不一致 0。
- s=0 degenerate 記録: 閉形式は x<=0 規約で両座席 0、生 engine
  は両座席 1 (engine 側でも A=B 成立) — 継承規約の記録で
  strip 系測定 (parts >= m >= 13) には無関係。
- 決定性: 6 走 byte-identical (sha256 87f0c951…)。

## 限界

- 本項の全称主張は崩壊値 v (K0832 閉形式) に対するもの。
  H 値 (engine 値) への転写は 764 座席の標本と各 kit battery に
  より支持されるが、本項では再証明しない (s=0 degenerate は
  規約差として明記済み)。
- K0832 閉形式自体の妥当性は K0832 が担う (本項はその系)。
- strip 系の separated-row / wave 構造 (m 行の H 値過程) には
  直接の主張をしない — open question (b) (separation
  life-cycle scaffold の閉形式化) は未解決のまま
  (log §5 参照)。
- 盤面 verdict とは無関係 (11×11 空盤・二石 root・S2・
  class 1/2/4 すべて UNKNOWN のまま・verdict 不消費)。

## honest 記録

- **K 番号 1345 は仮** (統合時再採番予定。採番時 probe で
  K1345..K1349 は items 空間で空き、items/ への直近 commit は
  2026-11-25 23:10Z K1344 を確認済み・push 直前の最新 main
  再取得で再確認)。
- **事前調査**: 本項の対象 (d-shift 供給族) は 2026-11-26
  06:14Z 出版の単一トークン定理 log の handoff 3(a) として
  未解決登録されていた。統合時の repo 横断調査で
  "dshift" 0 件・"d-shift"/"two-supply" は登録元 log と
  z18 kit の無関係な chain 記述のみ・K1334 は d=1 のみを
  対象とし、d>=2 の先行は不存在を確認の上で着手した。
  paper-first 順序 (K1320/K1321/K1325/K1334 と同一): 全
  場合分けを紙面導出後に凍結初走で機体接触 (d1_Instantiation
  を含む全照合が初走以降)。
- **統合環境の制約の開示**: 本項の出版は hand-written YAML
  (SCHEMA.md 準拠・必須 field 完備・relations/artifacts は
  実在 item/実在 path 限定) で行われ、実行環境の都合で
  `uv run python tools/knowledge/check.py` による機械検査は
  本実行では実施していない (統合時の通常確認工程に委ねる)。
  実験側の検証 (engine pin・決定性・fetch-back byte 照合) は
  実施済み。
