---
id: K0939
title: END-SIEVE（t=0エンドゲームの約数篩）とSIEVE-PRIME全称証明・双子法則LAW1/LAW2の完全iff全称完結
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0928
- type: depends_on
  target: K0934
- type: depends_on
  target: K0935
- type: depends_on
  target: K0937
- type: related
  target: K0929
- type: related
  target: K0931
- type: related
  target: K0933
- type: related
  target: K0936
- type: related
  target: K0922
- type: related
  target: K0919
artifacts:
- path: research/experiments/remo-sieveprime-endgame-20261118/report.md
  role: proof
  note: "END-SIEVE（t=0エンドゲームの約数篩）とSIEVE-PRIME全称証明・双子法則の全称完結レポート"
- path: research/experiments/remo-sieveprime-endgame-20261118/sievegen_core.py
  role: solver
  note: "K0937実験ディレクトリ committed版のbyte同一コピー（track_gen・play_full・ピン読み込みをそのまま使用）"
- path: research/experiments/remo-sieveprime-endgame-20261118/sieveprime_verify.py
  role: verifier
  note: "7チェックの機械検証器（すべてstdlib・決定的・PIN検査を含む）"
- path: research/experiments/remo-sieveprime-endgame-20261118/audit_build.py
  role: verifier
  note: "監査アセンブラ（2回コールド実行でbyte同一）"
- path: research/experiments/remo-sieveprime-endgame-20261118/output/sieveprime_audit.json
  role: data
  note: "監査正本（監査sha256 07d844c6…）"
date: 2026-11-18
tags: [remo, uniform-board, counting-recursion, endgame, sieve, primes, twin-laws, invariant, machine-evidence]
---

## 主張（すべてK0928のpot力学上。全定理が紙上全称証明。K0937の残課題SIEVE-PRIMEを閉じる）

### 定理END-INV（エンドゲーム構造不変量・全称）

V(m)/U(m)で監視がladderを生存しt=0エンドゲームに入ったとき、入口が
family状態（ENTRY-LOC）である限り、監視が生存する限りの**すべての**
フェーズ開始状態はptr基準の円

E(P; α, β) = [P]^α + [P+1]^β （k = α+β = 人数）

の形を保つ。監視は位置 α（V・[P+1] block先頭）/ 位置 α−1（U・pot block
末尾）にあり、石数恒等式 **N = P(k+1) + β + s**（s=0: V, s=1: U）が
毎フェーズ保存される（N=2m+1+s）。フェーズ遷移は q=P//k・r=P mod k で

- r < α（pot block敗者）: E(P+q; α−r−1, β+r)
- r ≥ α（pot+1 block敗者）: E(P+1+q; β+2α−r−1, r−α)

Vは生存中β≥1、Uは生存中α≥1を保存する。V死亡⟺r=α（break直前の
監視=敗者）、U死亡⟺r=α−1。

### 定理END-SIEVE（死亡合同式・全称）

END-INV条件下で監視が1フェーズで死ぬ ⟺ **k | N**。エンドゲームの円
サイズは1フェーズに1人ずつ n, n−1, …, 2 と降下するので、監視は
**Nの約数のうち ≤ n で最大のもの**に到達したフェーズで死ぬ（遅くとも
k=spf(N)）。エンドゲームは約数篩そのものである。

### 定理ENTRY-LOC（エンドゲーム入口の位置・全称）

素数NのV/Uゲームで幅wが初めてt=0（n≤w）になったとき、入口状態
F(w,h;n)は **n ∈ {w−1, w}**・V: **1 ≤ h ≤ min(n,w)**・U:
**0 ≤ h ≤ min(n−1,w)**（family状態）を満たす（例外はV m=1のn=0退化形
のみ）。証明: ladder censusはh≤wを保存し、初t=0の幅wの直前stretchは
t′≥1すなわちn′≥wでT ≥ w²−1、一方n≤w−2ならT ≤ w²−2（V）/
w²−3（U）で矛盾。w=2はbase直接ケース（V m∈{2,3}・U m∈{1,2}）で確定。

### 定理END-SIEVE-IFF（family状態上の完全判定・全称）

family状態（V: N=w(n+1)+h・U: N=w(n+1)+h+1・w≥2・n∈{w−1,w}・
h範囲ENTRY-LOC）からエンドゲームをプレイしたとき、監視が生存する
⟺ **Nは素数**。合成側: family では N ≤ w²+2w < (w+1)² より
spf(N) ≤ w、n=w−1では w∤h（V）/w∤(h+1)（U）でspf=wが排除され
spf ≤ n、よってspf | N の死亡フェーズが必ず現れる。素数側: familyの
Nは最小5で素数なら奇数 ≥ 5、全フェーズの円サイズkは2 ≤ k ≤ n < N
でk ∤ N、監視は最後まで生存し生存者になる。

### 定理SIEVE-PRIME（K0937予想の全称証明）

N=2m+1が素数なら **V(m)=0**。N=2m+3が素数なら **U(m)=m−1**。
組立: K0937素数側ladder生存定理（ladder死亡⟺(w+1)|Nで、N素数では
w+1=NがT恒等式と矛盾）→ trackerはt=0エンドゲームに到達 →
ENTRY-LOC → END-SIEVE-IFF素数方向 → 監視生存。

### 定理LAW1/LAW2（双子法則の完全iff全称化・C≥2）

- **P(C)=1 ⟺ Cが素数**（すべてのC≥2）。
- **P(C)=C−1 ⟺ C+1が素数**（すべてのC≥2）。

組立: K0928定理RED・系（偶数C≥4: P≥3・奇数C≥3: P≤C−2）+
K0937 TWIN-COMPOSITE-GEN（合成側: N合成なら監視死亡でV(m)≠0・
U(m)≠m−1）+ 本項SIEVE-PRIME（素数側）+ 有限ピン P(2)=1。C=1は
両法則の外（P(1)=1だが1は素数でない）。これによりK0929の予想
LAW1/LAW2とK0931のSIEVE予想（素数側生存を含む全体）が全称定理化し、
K0933/K0936のmod 30・mod 210類別版をすべて回収してmod類制限を除去。

## 機械的証拠（sieveprime_verify.py・audit_build.py）

sievegen_core.pyはK0937実験dirのcommitted版のbyte同一コピー
（sha256 a69f916c…・track_gen・play_full・ピン読み込みをそのまま使用）。
7チェック全合格:

- **PIN**: K0929コミット表のsha256・形式・P(1..40)ピン照合。
- **REDRECON**: 証明済みREDでコミットU/V表とP表を相互再構成
  （m≤3,999・7,998比較・0不一致・添字規約 P_pin[i]=P(i+1) 等を固定）。
- **FAMILY**: 全family状態（w≤60・V 3,553 + U 3,645 = 7,198状態・
  175,086フェーズ）をリテラル位置エンジンで完全プレイし、毎フェーズ
  構造E(P;α,β)・監視位置α/α−1・恒等式N=P(k+1)+β+s・transition公式
  （168,922照合）・死亡⟺k|N・最終判定生存⟺N素数・Eモデル（純算術
  再実装）との完全一致、すべて違反0。
- **ENTRY**: 素数N・m≤200,000両側67,716ゲーム: trackerがエンドゲーム
  到達・入口がfamily形（n∈{w−1,w}・h範囲・a=h/h+1・N=w(n+1)+h(+1)）・
  Eモデルで生存（最大入口幅632・違反0）。
- **PINREPRO**: 全m≤8,000両側16,000ゲーム: 純算術予測
  （tracker死亡 or エンドゲームEモデル生存）が「N素数」とコミットU/V表
  （K0929・JS engine産出）の両方と完全一致。**コミット済み全16,000値が
  tracker+ENTRY-LOC+E-modelの純算術から完全再構成**された。
- **ENGINE**: 新鮮python engine（play_full）m≤600両側1,200ゲーム:
  deathなし・生存者==監視 ⟺ N素数・ピン一致（違反0）。
- **PINSIEVE**: コミット表の完全iff: P(C)=1⟺C素数（C=2..8,000）・
  P(C)=C−1⟺C+1素数（C=2..8,000）・V(m)=0⟺2m+1素数・
  U(m)=m−1⟺2m+3素数（m=1..8,000）・違反0。

audit_build.pyはrun_checksをin-process 2回実行して一致を確認し
output/sieveprime_audit.jsonを書く（監査sha256
07d844c62df54014d8b720a98dbcd51e44dd6e50b52d74c8b05a3e2d03f6a0b3）。
2回のcold実行でbyte同一を確認済み。全称性は紙上証明による
（機械証拠は有限アンカー）。

## 範囲と限界

- 一様盤・ゼロリセット・K0859計数再帰（K0928定理RED経由）の設定のみ。
  非一様盤・11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class1/2/4には一切言及しない（**UNKNOWN不変**）。
- ENTRY-LOCは「監視がladderを生存した場合」の入口位置の定理。
  family外のエンドゲーム状態が他の経路で現れる可能性は排除しない
  （END-INVは入口がfamily状態である限りの主張で、END-SIEVE-IFFは
  family状態上の判定として適用される）。
- P(C)の閉形式（C→P(C)の直接式）は主張しない。本項は素数性との
  特徴付け（iff）の全称証明である。
- 合成NでのV(m)/U(m)の値そのもの（どのラベルが生存するか）は本項では
  決定しない。素数ケースの値確定（V=0/U=m−1）とiffが本項の成果。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （K0937と同じ扱い）。generated/とroot READMEは未編集。
