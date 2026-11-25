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
- path: research/experiments/rooted-core-seven-pure-triple-five-edges-20261125/proof.md
  role: proof
  note: 7点純三点辺が高々5本の完全族（raw384168件・根付き924型・閉包2948=新規2604+既知344）についての全長周期認証
- path: research/experiments/rooted-core-seven-pure-triple-five-edges-20261125/verify_enum.py
  role: verifier
  note: 型数924のBurnside独立軌道数導出と軌道安定化子総和384168照合・閉包・canonical固定点検査
- path: research/experiments/rooted-core-seven-pure-triple-five-edges-20261125/verify_values.py
  role: verifier
  note: 独立再実装による全値再計算・全2604レコード照合・窓認証・出版6点両監査との交差照合
- path: research/experiments/rooted-core-seven-pure-triple-five-edges-20261125/verify_direct.py
  role: verifier
  note: 階層化400状態×長さ0..6の原始subset mex照合（2800検査・922862安全状態）
- path: research/experiments/rooted-core-seven-pure-triple-five-edges-20261125/verify_tamper.py
  role: verifier
  note: fail-closed改変電池（T4..T10全件検出）
- path: research/experiments/rooted-core-seven-pure-triple-five-edges-20261125/output/shards/part00.json
  role: certificate
  note: 公式認証レコードshard 00/06。part00..05連結が正規official_records.json（sha256 5a1efeba...、combine_records.pyで再結合検証済み）・jointly_certified=true・開始571
- path: research/log/2026-11-25-rooted-core-seven-pure-triple-five-edges-single-owner-note.md
  role: log
  note: 単一オーナー宣言（publish-then-execute・宣言前探査の全開示）
- path: research/log/2026-11-25-rooted-core-seven-pure-triple-five-edges-run-log.md
  role: log
  note: 公式6走のbyte一致（PYTHONHASHSEED/env混在・サンドボックス障害後の別環境再現を含む）と検証電池5/5 PASSの実行記録
scope: 任意有限の合法点上のサイズ2・3のclutterと指定根を固定し、その根に長さLの二点禁止道を付ける通常ゲーム。核サイズは無界、核自体はLに依存しない。
evidence: K0682で5点以下の全6337ラベル付き核・513型を証明。6点純三点辺は高々6本の完全族732型（開始571）を経て、全型（2^20全1048576件・Burnsideで根付き10688型・10688新規閉状態）まで拡張し共同開始637で全長認証。すなわち6点の純三点辺核は全て証明済み。二点辺混在や7点以上の任意核の全称証明・反例は未確定。 7点純三点辺は高々5本の完全族（raw384168件・rooted-core-seven-pure-triple-five-edges-20261125）でも開始571で全長認証済み（新規2604状態・prefix上Grundy最大33）。
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
さらに `rooted-core-seven-pure-triple-five-edges-20261125` で7点の純三点辺が高々5本の**完全族**へ拡張した。
三点辺同士は包含を持たないため Σ_{k=0..5} C(35,k)=384168件すべてが合法核で、根付き同型は924型
（Burnside軌道数計算と軌道安定化子総和 Σ720/|Aut|=384168 の二重導出で確認）。
閉包2948状態のうち新規2604状態（7点924＝初期型・6点1680＝残留）を全長認証し、
**共同開始571・必要値1211・jointly_certified=true**。残留6点のうち301状態は純三点辺のままで
出版済み6点両監査（×6本以下・全型）と全長完全一致、**1379状態は着手による三点辺の退化で
生じる二点辺混在clutter** で出版監査のどこにも現れない新規状態（二点辺混在核の初認証）。
最悪最終破綻570を担う `[6,[3,13,22,28,49]]` と族全体のGrundy最大33を担う
`[6,[3,6,13,24,44]]`（二点辺3本＋三点辺2本・argmax L=208・33を取る唯一の状態）は
いずれも二点辺混在の残留状態で、7点初期型自身のprefix上最大は27である
（二点辺混在族が純三点辺族の全型最大29を超えるGrundy値を生成する最初の実証・観測で全称主張ではない）。
公式solveは6走（PYTHONHASHSEED=random/1・隔離tree env -i×2 を含む）すべて byte 一致、
うち2走はサンドボックス障害後の別環境での再現で sha256 も完全一致。
階層化400状態×長さ0..6の原始subset mex照合（2800検査）・fail-closed改変電池も全検出。
7点の純三点辺でも6本以上は未証明のまま。
K0682の有限窓定理は候補周期を認証するものであり、認証が必ず成功することは保証しない。

特定の長いprefixで周期が見つからないことだけでは反例にならない。
反証には、34を周期に持たない最終周期の全称認証や、非周期性・無界性等の証明が必要である。
K0683により、反例または証明は有限整数点盤の残局にも移せるが、標準全格子盤には直結しない。
