---
id: K1150
title: 一般マルチセット マージの対角帯への還元定理（MERGE ⟺ BAND）とストライプ帯構造の有限観測
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [general multiset merge reduction, boundary mex reduction, band cascade, B(k,S) band table]
relations:
- type: depends_on
  target: K0832
  note: H の定義・単一トークン閉形式 single_token(S,z,R)（z==x 場合と z>=x+1 場合の z 非依存性）を証明に使用する
- type: depends_on
  target: K1101
  note: 生再帰セマンティクス（H_canonical）の verbatim 使用と S=z 鋭さ反例・残余72行以外の一般化フロンティア（対角線下マージの一般マルチセット化）の継承
artifacts:
- path: research/experiments/vertical-fiber-two-token-merge-general-multiset-20261120/report.md
  role: proof
  note: 還元定理と3補題（遠行転送・崩壊・mex事例）の記号証明・14チェック監査表・帯表とカスケードの有限観測・信頼境界
- path: research/experiments/vertical-fiber-two-token-merge-general-multiset-20261120/verify_merge_general.py
  role: verifier
  note: 14チェック・総6,841,612照合点・不一致0・エンジン錨（DP vs verbatim生再帰・出版閉形式・828発散再現）・BAND/L1/L2センサス・2トークン広域・深部プローブ・帯表抽出
- path: research/experiments/vertical-fiber-two-token-merge-general-multiset-20261120/output/audit.json
  role: data
  note: 決定論的監査出力（sorted keys・SHA-256 b29deb7df60a11f2325a9c44706a70a3cbf84920b372606da24c478df6d8d5c5・3実行 byte-identical）
- path: research/log/2026-11-20-general-multiset-merge-lane.md
  role: log
  note: 選定・導出・採番再確認（K1148/K1149 の並走取得とK1149二重衝突の観測）・出版記録
- path: research/log/2026-11-20-general-multiset-merge-lane-single-owner-note.md
  role: note
  note: 単一オーナー宣言（commit f7ad833c07・先行出版）
scope: >-
  κ=1 残余ゲーム H(R;X;z)。全称主張は還元定理のみ: sum X = S の全マルチセット・
  全 z>=S+1・全 R>=0 でのマージ MERGE(S) が、対角帯 D_X(m)=H(m;X;S) の
  明示的ビット条件群 BAND(S)（S 偶: D!=1 ∀m ∧ D==0 for 偶m<=S-1、
  S 奇: D==0 ⟺ (m偶∧m<=S-1) ∧ D!=1 for 奇m<=S-2）と同値であること
  （正確には各 S>=1 で MERGE(<S) を前提した二重帰納による MERGE(S) ⟺ BAND(S)、
  特に MERGE(∀S) ⟺ BAND(∀S)）。BAND 自身・レベルkストライプのカスケード
  （L1-A/L1-B/Z2/N2 など）・帯表 B(k,S) は本項の全称主張に含まれず有限証拠のみ。
  S=z 行（対角線上）には触れない（マージは K1101 の鋭さどおり失敗する）。
evidence: >-
  記号証明（report.md §2）: (1) 遠行補題 R1: z>=S+2 の全子は merged region に
  留まり、縮小子と除去子は z 非依存性により同一値に崩壊するため MERGE の
  レベル R-1 全域からレベル R の遠行領域が帰納転送される。(2) 崩壊補題 R2:
  境界 z=S+1 では token 子がすべて a(m)=single_token(S-1,S,m) に崩壊し、
  境界値 = mex({a, 1^D_X(R-1)})、単一トークン側 = mex({a, 1^e(R-1)})。
  対角線も同様に D_X(m) = mex({a(m-1), 1^U1_X(m-1)}) に分解される。
  (3) mex事例補題 R3: mex({a,1^D})==mex({a,1^e}) ⟺ a==0 では D==0 ⟺ e==0、
  a∈{1,2} では D==1 ⟺ e==1（全数表）。(4) 還元定理: a(m) と e(m) の
  帯構造（a は S の偶奇で 2/0/1 の帯、e は z==x 場合）を R3 に通すと、
  BAND(S) の各節が境界一致条件の全位置での収集と過不足なく対応する。
  ⟸ は BAND の節が全 a-帯位置でビット条件を満たすこと、⟹ は境界一致から
  節を集めること（S奇 iff 節の奇 m<=S-2 位置は対角カスケードの a(m-1)==0
  から D≠0 を得る）。機械検証は有限二重検査: C1 DP vs verbatim 生再帰
  1,512点、C2 単一トークン閉形式 92,460点、C3 鋭さ反例と828発散再現
  7,757点、C4 マージ行 z=S+1,S+2（S<=20 全分割 2,714形状・r<=200・
  z=S+3 遠行証拠込み）1,411,422点、C5 崩壊2恒等式 1,077,200点、
  C6 compat 538,600点、C7/C8 BAND（S偶/S奇）541,293点、C9 L1ストライプ
  541,293点、C10 mex事例全数表 816点、C11 Z2/N2+偶Sゼロ法則（一方向）+
  L1-A拡張 1,623,276点、C12 2トークン広域（部品<=40・S<=80・820対）
  824,100点、C13 深部プローブ8個（r<=250..600・1^25・(25,5)・(24,12)・
  (10,8,6)・(20,7,7)・(17,16)・(5,4,3,2,1)・(13,11,9)）23,490点、
  C14 帯表 B(k,S) 152行抽出 158,393点。総 6,841,612 点・不一致 0・
  同一cwd 2回＋隔離cwd 1回で監査 byte-identical。有限観測: k<=2 の帯幅は
  B(0,S)=S+2-(S mod 2)、B(1,S)=S+1-(S mod 2)、B(2,S)=S-(S mod 2) の
  閉形式、k>=3 は約1ずつ縮小し最深部で床 B=2。
---

## 命題・範囲

κ=1 残余ゲームで、sum X=S・z>=S+1・R>=0 のマージ全称命題 MERGE(S) を、
対角帯値 D_X(m)=H(m;X;S) への明示的ビット条件群 BAND(S) に還元する:

```
S 偶数: D_X(m) != 1 for all m;  D_X(m) == 0 for all even m <= S-1
S 奇数: D_X(m) == 0  iff  (m even and m <= S-1);
        D_X(m) != 1 for all odd m <= S-2
```

**定理（還元）**: 各 S>=1 について（MERGE(<S) を前提して）
MERGE(S) ⟺ BAND(S)。特に MERGE(∀S) ⟺ BAND(∀S)。
K1101 の残務「y>=3・マルチトークンへの一般化」は BAND への還元に置き換わった。

## 証明の構成

1. **遠行補題 R1**: z>=S+2 の子は全て merged region 内で、token 子は
   z 非依存性で同一値に落ちる。MERGE(R−1) 全域（と MERGE(<S)）から遠行領域が
   レベル帰納で転送される。
2. **崩壊補題 R2**: 境界 z=S+1 の token 子は全て a(m)=single_token(S−1,S,m)、
   境界値=mex({a, 1^D})。対角線も D(m)=mex({a(m−1), 1^U1(m−1)}) に分解。
3. **mex事例補題 R3**: 値表（a=0: D==0 依存、a∈{1,2}: D==1 依存）。
4. a(m)/e(m) の帯構造を R3 に通して、⟸（BAND⟹境界一致）と
   ⟹（境界一致から BAND 収集; S奇 iff 節の奇 m≤S−2 は対角カスケードの
   a(m−1)==0 ⟹ D≠0 で閉じる）を二重帰納で確立。

## 有限証拠（全称主張ではない）

- BAND: S<=20 全分割・r<=200（C7/C8）、2トークン部品<=40（C12）、
  深部 r<=600（C13）で違反 0。
- レベル1・2カスケード主張（L1-A/L1-B, Z2/N2）と偶S対角帯ゼロ法則
  （一方向: 偶 m または m>=2S で D==0）: 同ドメインで違反 0。
- 帯表 B(k,S): k<=2 は閉形式 B=S+2-(S mod 2), S+1-(S mod 2), S-(S mod 2)、
  k>=3 は約1ずつの縮小で最深部 B=2。第2帯の開始位置含め全 152 行は
  監査 JSON にある（観測）。

## 限界・残務

- 還元定理の全称性は記号証明による（K0832 閉形式と生再帰セマンティクスに
  依存。Lean 形式化ではない）。C1〜C14 は有限二重検査であり証明の代わりではない。
- **BAND(∀S) は未解決**（したがって一般マルチセットマージの全称成立も未解決）。
  次段はレベルkカスケードの一般化（L_k 主張族と帯幅縮小則、k での打ち切り）
  により BAND の全称証明へ収束すること。
- 帯表の構造（閉形式・第2帯）は観測であり全称主張ではない。
- r 人対戦・d 次元版への還元の同型は未着手。
