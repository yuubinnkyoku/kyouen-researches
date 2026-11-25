# 11×11 exact証明体系の独立監査（2026-10-10）

開始mainは `ed75f33d9ccc1557df6143a59ec0994f46f28594`。これは実験当時の監査記録で、現在の知識はK0372、frontierの正本はK0355。既存raw/cacheを上書きせず、新規探索は独立再証明の少数pilotに限定した。

## 結果と信頼境界

固定命題は「元の先手が勝つ」。S0から終局まで偶数層OR、奇数層ANDであり、子のverdictを反転しない。子集合が空なら偶数LOSS・奇数WIN。独立実装は円の中心の整数分子と共線判定から合法性を求め、独自の8座標変換でD4正規化する。既存solver、geometry、伝播関数を呼ばない。

tracked `research/experiments/n11-*` のpositive-budget replay 3,923ファイル・15,503行を直接読んだ。unique exactはS5=2,578、S6=4,172、S7=8。UNKNOWN、budget=0のcache projectionは証明葉にしない。別途280個のhistorical S5 cacheを幾何・衝突・隔離規則でunionし、現行cacheと5,734行全て一致した（156 WIN / 5,578 LOSS）。

rawの直接exactまたは正しい完全境界・reverse propagationだけで支持できた現行S5は2,988件。残る2,746件は保存cacheへの依存として `cache-only-claims.json` に個別の出所・hashを保存した。これは勝敗の反証でも一括撤回でもない。初期Actionsのsolver cache自体が残る一次出力で、今回のpositive-budget replay条件では葉まで分解できていない。`.local/n11` の6,327 CSVも補助監査したが追加の対応exactはなかった。可搬検査は `.local` を必要としない。

全6,871 raw S4 edges、3,384 canonical S4 classと各完全S5子集合をgeometryから再生成した。結果は31 LOSS / 268 WIN / 3,085 UNKNOWN、secured 117/119、remaining `{100,108}`。単一UNKNOWN classが残る2頂点を覆い、重み100=1の有理dualは全UNKNOWN classについて制約を満たすのでminimum additional class=1、dual=1。これは不足するclass数の下界とスケジュールの証明であり、そのclassのLOSS証明ではない。119第三手の証人とUNKNOWN2件を保存した。S2 `{60,27}`、空盤はUNKNOWN。

31 LOSS classは、保存されたS5 verdictを前提とする完全全子LOSSの幾何・伝播検査を全て通る。ただしraw-rootedなS5証拠だけでは1 LOSS class・3 secured verticesしか閉じない。残る30 classは一部のcache-only葉に依存する。**117/119を全体の独立minimax証明済みとは呼ばない。** raw-rootedな2,988件についてもexact replay葉はsolverを信頼し、独立minimax証明とは別である。

## 撤回の依存関係

旧誤伝播に直接依存したS5 WINは2件。両方のtracked直接rawとlocal直接rawは15M UNKNOWNで、独立exact支持はない。旧S7 exact LOSS rawは保存し、その不正な反転を無効にする。旧manifestから6個のS6 WIN主張を再構成すると、各完全境界75〜86子のうちS7 LOSS証人は1個だけで、全て正しい推論ではUNKNOWNとなる。

撤回2 S5が混入したtracked historical cacheは48ファイル。6 S4 classが依存辺を持ち、誤証拠を戻した場合と比較すると2 classがWIN→UNKNOWNになる。他の4 classには別のWIN証人がある。31 LOSS classとその被覆はこの誤ったWINに依存しない。局面一覧、全cache path、直接観測は `withdrawal-dependencies.json`、中間S6は `legacy-intermediate-s6.json`。

K0355の現行解釈とK0371の修正範囲を補強した。他のK項目に撤回キーを使った現行の独立定理は見つからない。過去のcheckpoint記述・raw・cacheは当時の一次資料として保持し、撤回主張は新しい正本の注記から辿れるようにした。

## 実装修正

主要helperの極性は開始mainで修正済みだった。一方、C++永続cache loader、追加のPython reader、10個の手動workflow内のinline mergerに隔離漏れがあった。全てregistryに従ってcache祖先の再流入を止める。C++のコンパイル済み2-key policyとJSON registryの一致を回帰検査し、再認定には両方の明示更新を要する。Python policyはregistry欠落時にfail closedとした。

汎用mergeのreplay経路にもpositive-budgetを要求し、budget=0のcache projectionによる隔離迂回を拒否する。active quarantineにある局面のexact raw再認定はregistryの明示解除を要する。UNKNOWN観測はexact証拠にしない。この2経路も実入力で回帰検査した。

各層の量化条件に残ったnonemptyガードも除去した。今回の実境界は空でないためfrontier値には影響しないが、終局の一般規則としては必要な修正である。C++のcache入力に盤外bit、5石以外、不安全、非canonical、不正数値、UNKNOWN、矛盾の拒否を加え、exact replayにも盤外・不安全の入力検査を加えた。修正一覧は `implementation-repair-files.json` と `workflow-repair-files.json`。workflowの起動条件は変えず、CIに有限回帰だけを追加した。

## 独立minimax証明書

C++ coverとの照合中に追加の不具合を発見した。`run_cover` は119 legal verticesの個数でcoverage配列を確保し、実際にはcell ID 0..120で参照していた。未被覆表示でもcompact slotとcell IDを混同した。修正前出力 `cpp-cache-cover-before-fix.csv` は31 LOSS / 268 WINが一致しながら116/119、誤ったremainingを出した。121-cell配列とcell IDでの表示に修正し、117/119と `{100,108}` をC++実行回帰に固定した。

S5 WIN/LOSS、S6 WIN/LOSSの代表4件を各2,000 unique-state上限で試し、各約1.7〜2.1秒でUNKNOWNだった。軽いS6 WIN `(10448351135500075008,1040)` だけ30,000上限へ増額し、26,577状態・約23.90秒でWINを独立再計算した。保存した10,407-node DAGはterminal以外の信頼葉を持たず、別の証明書検査経路で合法親子、存在証人、全子集合、石数のrank、循環なしを確認する。

1×1〜4×4の全安全状態（2、15、298、5,811）を独立な手番側Boolean DPとも照合した。空盤証明書4件と11×11の両極性terminal証明書2件も保存した。S5全件や31境界全体の独立minimaxは未完了。拡張にはsolverの各確定局面について、OR WIN / AND LOSSでは決定子、OR LOSS / AND WINでは完全全子を記録し、TTで省略された依存もterminalまで回収する仕組みが必要である。全5,734 rootsの共有DAG化・容量計測・段階的検査を先に設計すべきで、今回の一標本コストを全件へ外挿しない。

## 再現

```powershell
uv sync --locked
uv run --locked python research/experiments/n11-independent-exact-audit-20261010/scripts/audit.py
uv run --locked python research/experiments/n11-independent-exact-audit-20261010/scripts/legacy_audit.py
uv run --locked python research/experiments/n11-independent-exact-audit-20261010/scripts/verify.py
uv run --locked python research/experiments/n11-independent-exact-audit-20261010/scripts/artifacts.py --check
uv run --locked --with scipy python -m unittest discover -s research/experiments/n11-independent-exact-audit-20261010/tests
g++ -std=c++20 -O2 research/experiments/n11-independent-exact-audit-20261010/tests/test_cache_policy.cpp -o .local/n11-independent-cache-test.exe
.local/n11-independent-cache-test.exe .local/n11-independent-cache-fixture.cache
```

`pilot.py` は少数の独立再計算、`local_recovery.py` は任意のlocal補助監査。独立S6 WIN増額の生成コマンドと結果はlog参照。通常の可搬検査は保存certificateを読み、再探索しない。入力manifestはraw/cacheのhashを固定する。修正後のソースhashは旧manifestの当時のソースhashと異なるため、過去のコードsnapshotのbyte一致と現在の修正コードを混同しない。過去raw/cacheのbyteは保存している。
