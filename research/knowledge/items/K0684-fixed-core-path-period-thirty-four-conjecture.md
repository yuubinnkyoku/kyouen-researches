---
id: K0684
title: 任意の固定rank3残余核に長道を付けたGrundy列は最終的に34周期になるか
kind: proposition
status: conjectured
topics: [residual-games, grundy, geometry, variants]
aliases: []
relations:
- type: depends_on
  target: K0108
  note: 固定残余clutterと通常Grundyの定義
- type: depends_on
  target: K0683
  note: 全rank3核と長道は有限整数点盤の残局として実現できる
artifacts:
- path: research/experiments/rooted-core-tail-periodicity-20261107/proof.md
  role: source
  note: 任意核の正確な再帰と有限周期認証規則。周期の必然的存在までは証明しない
- path: research/experiments/rooted-core-tail-periodicity-20261107/output/audit.json
  role: certificate
  note: 5点以下全513型については全長の34周期が証明済み。一般核の証明ではない
- path: research/experiments/rooted-core-larger-periods-20261107/proof.md
  role: proof
  note: 6点の純三点辺3本以下全1351件と追加67件の指定有限入力族についての全長周期認証
- path: research/experiments/rooted-core-larger-periods-20261107/verify.py
  role: verifier
  note: 既証明の小核表を再利用し、101新規閉状態の有限窓と別subset mex700条件を照合
- path: research/experiments/rooted-core-larger-periods-20261107/output/audit.json
  role: certificate
  note: 指定6・7点族の100入力型と101新規閉状態の全0..1069整数値。6点全体の網羅ではない
- path: research/experiments/rooted-core-six-pure-triple-six-edges-20261107/proof.md
  role: proof
  note: 6点純三点辺が高々6本の全60460件（根付き732型）についての全長周期認証。共同開始571
- path: research/experiments/rooted-core-six-pure-triple-six-edges-20261107/verify.py
  role: verifier
  note: 既証明の小核表を再利用し732新規状態の有限窓を認証。全732型長さ0..6の独立subset mex5124条件で照合
- path: research/experiments/rooted-core-six-pure-triple-six-edges-20261107/output/audit.json
  role: certificate
  note: 6点純三点辺六本以下の完全族732状態の全0..1211整数値と有限窓証明書。jointly_certified=true
- path: research/experiments/rooted-core-six-pure-triple-full-20261108/proof.md
  role: proof
  note: 6点純三点辺の全型（2^20全1048576件・Burnsideで根付き10688型）についての全長周期認証。共同開始637
- path: research/experiments/rooted-core-six-pure-triple-full-20261108/verify.py
  role: verifier
  note: 高速orbit列挙と既証明小核表の再利用・適応有限窓認証。7本以上400型長さ0..6の独立subset mex2800条件で照合
- path: research/experiments/rooted-core-six-pure-triple-full-20261108/output/audit.json
  role: certificate
  note: 6点純三点辺の全10688状態の全0..1343整数値と有限窓証明書。jointly_certified=true・Grundy最大29
- path: research/log/2026-11-07-rooted-core-and-rank-three-universality.md
  role: log
  note: 有限の核サイズで閉じた定理と、無界核に関する予想を分離した経緯
scope: 任意有限の合法点上のサイズ2・3のclutterと指定根を固定し、その根に長さLの二点禁止道を付ける通常ゲーム。核サイズは無界、核自体はLに依存しない。
evidence: K0682で5点以下の全6337ラベル付き核・513型を証明。6点純三点辺は高々6本の完全族732型（開始571）を経て、全型（2^20全1048576件・Burnsideで根付き10688型・10688新規閉状態）まで拡張し共同開始637で全長認証。すなわち6点の純三点辺核は全て証明済み。二点辺混在や7点以上の任意核の全称証明・反例は未確定。
---

## 予想

任意の固定rank3以下の残余核Cと指定合法根に対し、核に依存する整数N_Cが存在して

\[
 \boxed{f_C(L+34)=f_C(L)\quad\text{for all }L\ge N_C}
\]

となる。核に長道を付ける辺は二点禁止辺だけとし、通常プレイを考える。
「最小周期が常に34」「核によらない開始上界」「核によらないGrundy上界」は予想に含めない。

## 現在の根拠と限界

K0682により5点以下の全核は証明済みで、一様開始500、最小周期34、Grundy最大23。
これより大きい任意の核への拡張は未証明。
追加の有限族として、6点の純三点辺が高々3本の全1351件と、固定seed混合64件・構造例3件を調べた。
100入力型・101新規閉状態は500以降34周期の証明窓を満たし、この指定族の全長も認証済み。
別subset mex700条件・154762安全状態でも一致した。6点核全体の網羅ではない。
さらに6点の純三点辺が高々6本の**完全列挙**（raw60460件・根付き732型・732新規閉状態）を
`rooted-core-six-pure-triple-six-edges-20261107` で全長認証した。共同開始は571（最悪状態の
最終周期破綻570）、必要値1211、prefix上Grundy最大27。全732型・長さ0..6の独立subset mex
5124条件・1345310安全状態で再帰値と一致。これは有限族の完全な定理であり、無界核の全称証明ではない。
さらに `rooted-core-six-pure-triple-full-20261108` で6点純三点辺の**全型**へ拡張した。
三点辺同士は包含を持たないので全部分族がclutterであり、raw 2^20=1048576件すべてが合法核。
Burnsideの補題で根付き同型型数は厳密に10688。全10688新規状態（閉包11201＝新規10688＋既知513）を
全長認証し、共同開始637（最悪最終周期破綻636）・必要値1343・prefix上Grundy最大29。
7本以上の型から無作為400型・長さ0..6の独立subset mex2800条件・596850安全状態でも一致。
これで**6点の純三点辺核は全て**証明済みとなった（二点辺混在・7点以上は未証明）。
K0682の有限窓定理は候補周期を認証するものであり、認証が必ず成功することは保証しない。

特定の長いprefixで周期が見つからないことだけでは反例にならない。
反証には、34を周期に持たない最終周期の全称認証や、非周期性・無界性等の証明が必要である。
K0683により、反例または証明は有限整数点盤の残局にも移せるが、標準全格子盤には直結しない。
