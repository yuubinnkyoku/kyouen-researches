# 11×11 DFPN proof-DAG capture pilot (2026-10-11)

## 目的と範囲

K0372が残した「exact solverの確定値を終局まで独立に閉じる」課題に対し、冷たい`--exact-replay`中に依存辺を収集し、既存solverのWIN/LOSSから終局だけを葉とする証明DAGを生成する試作を実装した。生成DAGの位置・合法手・全子条件・勝敗・終局は、solverやそのTT/cacheを使わないK0372由来の整数幾何検証器で再検査する。

対象は既知の11×11 S6 WIN `(lo=10448351135500075008, hi=1040)`。未解決S5 probeは実施していない。作業開始時の共有main作業ツリーに別作業の未コミットS5出力が多数あったため、探索を競合させず、候補S4 `(1188950301626859520,536870912)`への適用は保留した。

開始時に`origin/main`をfetchし、remote mainは`581e72c277d05149b847d997c47a15bfc77a36c7`、共有作業ツリーHEADは`5afc56fda29255f1e2e285a1fa1d2b664efb1b3e`だった。差分はS5 cache merge用script/test/logのみで、DFPNソースとK0355/K0371/K0372/K0373には差がなかった。試作は既存の`main`作業ツリーで行い、他作業のファイルや既存探索成果物は変更していない。pushは行っていない。

## 実装

- `cpp/solvers/kyouen_dfpn_root.cpp`に任意の`--proof-dag=PATH` exact-replay出力を追加した。flagなしの探索経路は従来どおり。
- 証明記録時は冷たい単一exact replayだけを許し、複数選択行、TT共有、layer cache、residual exact shortcutを拒否する。UNKNOWN・予算打切りではtraceを書かない。
- WIN/LOSSは全層で「元の先手」に固定する。OR WIN / AND LOSSは決定的な1辺、OR LOSS / AND WINは全合法手を記録する。特に偶数S6 LOSSなら全合法S7子が元先手LOSSでなければならない。
- solver内部の探索はD4同値子をまとめるが、全称証明のtraceは具体的な合法手をすべて列挙し、canonical座標へ移した着手番号とcanonical child keyを記録する。
- C++ trace自体は最終証明書ではない。`trace_to_certificate.py`が根から到達可能な依存だけを残し、`dag_verifier.py`が合法遷移、全合法手の被覆、存在証人、固定視点AND/OR、rank増加、終局判定、循環・欠落・到達不能節点、trusted leaf 0件を検査する。`verify_saved.py`は別プロセスで圧縮証明書を検証する。
- independent re-search型のfallbackも`dag_builder.py`として残した。solver trace収集と比較でき、予算超過時にpartial DAGを返さない。

## 正確性結果

新しい形式の小盤面テスト7件が通過した。1×1終局、4×4の全子必須LOSS、6石LOSSからの全7石LOSS子、非法手、誤勝敗、欠けた子、循環/順位不正、到達不能節点、終局marker、trusted leaf、budget cutoff拒否を確認した。6石LOSSの量化テストは有限計算の小盤面fixtureであり、11×11 S6一般への計算結果ではない。

native writerも既知4×4 S0 LOSSでend-to-end検証した。初回はN<8の`legal_for`が盤外の下位bitを残しており、探索列挙は捨てるbitを証明再列挙が拾う問題を発見した。合法maskと全称証明の再列挙を盤面範囲に揃え、修正版は154 solver nodesでLOSS、166節点・230辺（rootの全16初手を含む）のDAGを生成し、別プロセス検証に成功した。終局46、trusted leaf 0。初回失敗と修正前診断も`output/native-small-s0-loss/`と`output/native-small-s0-loss-debug/`に保持した。

11×11既知S6局面ではsolverが19,445節点でWINを返した。traceから終局まで閉じた8,932節点・13,422辺のDAGを生成し、終局節点1,145、trusted leaf 0で別プロセス検証に成功した。S6はORなのでWINにはS7 WINの存在証人1辺で十分である。今回の証明書は次のSHA-256を持つ。

`proof-dag.json.gz`: `e1fabd8f98210286acaacb43f56b437cdb67e6f1b6aae8eaf44dfd8d343d5f8a`

他のS6決定子、S7境界、S5未解決局面の検証はしていない。

## 性能と容量

### 同一solver queryのcapture overhead

Windows 11 Home、AMD Ryzen 7 5800HS、MSYS2 g++ 15.2.0、`-O3 -std=c++20 -DNDEBUG`。同じS6局面、count-asc、100,000 node budget、各5回のpaired run。baselineは開始HEADのDFPNソースSHA `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`から同じflagsでbuildした。

| variant | verdict | nodes (5 runs) | median wall | median peak RSS | proof trace |
|---|---:|---:|---:|---:|---:|
| capture off | WIN 5/5 | 19,445 each | 0.375 s | 173,805,568 B | 0 B |
| capture on | WIN 5/5 | 19,445 each | 0.438 s | 176,631,808 B | 3,228,421 B |

capture有効化による測定値は壁時計で約16.8%増、最大RSS約2.70 MiB増だった。Traceを含む圧縮JSON証明書は259,955 B（展開JSON 2,046,071 B）。証明DAGの座標・遷移独立検証には約7.41 sかかり、solver・trace変換・検証までの記録された総時間は15.38 s。CPU負荷を伴うこの一標本では高速化を主張しない。

### 探索順序と状態共有

同じ11×11 S6・100,000 budgetでcount-ascは19,445 nodesでWIN。count-descとkey順は各100,000 nodesでUNKNOWNとなり、証明を出さなかった。従ってこの局面では既定count-ascを維持するのが有効だったが、一標本だけの結果で他局面へ一般化しない。

4×4空盤の有限証明生成ではD4 memo共有あり/なしと3順序を比較した。count-ascは共有あり231評価・179節点DAG、共有なし3,985評価・同じ179節点DAG。count-descは357対16,777評価、key順は259対6,833評価。これは小盤面だけの状態共有コスト比較で、S5/S6/S7の速度比には外挿しない。

再探索型fallbackは同じ11×11 S6を26,577評価・10,407節点DAGで約23.9 sかけて生成した。native trace方式ではsolver探索中に依存を保持し、変換後8,932節点へ刈り込めた。`output/`には両方式のraw、trace、証明、独立検査receipt、order/shared pilotとSHA manifestを保存している。

## 結論と未解決点

最優先条件の一つである「確定局面から終局のみを葉とする独立検証可能な証明DAGを自動生成」は、冷たいexact replayに限り実現した。D4共有・子順序の効果も有限測定した。一方、未知11×11境界に対する新しい探索節点削減は示しておらず、候補S4や未解決S5へ適用していない。

主な技術的境界は、既存exact replayのソルブ済み依存を捕捉する方式なので、外部のsolver cache、DFPN本体の中間PnTT値、別runで復元したtrust-only leafをproof dependencyとして使えない点である。solverの通常状態/DFPN rootから全子境界を直接記録し、複数root間でcertificate DAGを共有する部分は未実装。Capture flagでこれらを拒否する。

## 再現

`uv sync --locked`後にrepo rootから実行する。比較baselineは`input/dfpn-baseline.cpp`に保存してある。最新の試作は次のように再現できる。

```powershell
g++ -O3 -std=c++20 -DNDEBUG cpp/solvers/kyouen_dfpn_root.cpp -o .local/n11-proof-dag-engine-20261011/dfpn-native-boardmask.exe
python -m unittest discover -s research/experiments/n11-proof-dag-engine-20261011/tests -v
python research/experiments/n11-proof-dag-engine-20261011/scripts/certify.py `
  --solver .local/n11-proof-dag-engine-20261011/dfpn-native-boardmask.exe --n 11 `
  --root-lo 10448351135500075008 --root-hi 1040 --solver-budget 100000 `
  --solver-order count-asc --native-proof-capture `
  --out-dir research/experiments/n11-proof-dag-engine-20261011/output/reproduction
python research/experiments/n11-proof-dag-engine-20261011/scripts/verify_saved.py `
  research/experiments/n11-proof-dag-engine-20261011/output/reproduction/proof-dag.json.gz
python research/experiments/n11-proof-dag-engine-20261011/scripts/certify.py `
  --solver .local/n11-proof-dag-engine-20261011/dfpn-native-boardmask.exe --n 4 `
  --root-lo 0 --root-hi 0 --solver-budget 100000 --native-proof-capture `
  --out-dir research/experiments/n11-proof-dag-engine-20261011/output/reproduction-s0
```

比較baselineのsource snapshotは`input/dfpn-baseline.cpp`に保存し、SHA-256は開始HEADのDFPN sourceと一致する。baselineを同じcompilerで再buildし、capture overheadを再計測する例:

```powershell
g++ -O3 -std=c++20 -DNDEBUG -I cpp/solvers research/experiments/n11-proof-dag-engine-20261011/input/dfpn-baseline.cpp -o .local/n11-proof-dag-engine-20261011/dfpn-baseline.exe
python research/experiments/n11-proof-dag-engine-20261011/scripts/bench_capture_overhead.py `
  --baseline-solver .local/n11-proof-dag-engine-20261011/dfpn-baseline.exe `
  --native-solver .local/n11-proof-dag-engine-20261011/dfpn-native-boardmask.exe `
  --input research/experiments/n11-proof-dag-engine-20261011/output/s6-native-capture-boardmask-final/solver-input.csv `
  --n 11 --stones 6 --order count --budget 100000 --repeats 5 --poll-ms 5 `
  --out-dir research/experiments/n11-proof-dag-engine-20261011/output/reproduction-overhead
```

## 最終検証

- 実験fixture: `python -m unittest discover -s research/experiments/n11-proof-dag-engine-20261011/tests -v` — 7件成功。6石LOSSで全合法7石子を要求する検査、欠落・循環・非法手・誤勝敗・trusted leaf・予算切れを含む。
- native 4×4 S0 LOSS: 154 solver nodesから166節点・230辺を生成。別プロセスが全16初手、終局46、trusted leaf 0でLOSSを検証。
- native 11×11 S6 WIN: 19,445 solver nodesから8,932節点・13,422辺を生成。別プロセスが終局1,145、trusted leaf 0でWINを検証。
- capture overhead: 同一binary/replay条件5回ずつでnodesは各19,445。capture off/onの中央値は0.375/0.438 s、peak RSS 173,805,568/176,631,808 B、trace 0/3,228,421 B。
- 2行のexact-replay入力は終了コード1で拒否され、proof traceを出力しない。再現入力とreceiptは`input/proof-trace-multirow.csv`と`output/multirow-guard-test/guard-result.json`。
- Python compileと`g++ -std=c++20 -fsyntax-only cpp/solvers/kyouen_dfpn_root.cpp`が成功。
- repo指定チェック: `uv sync --locked`、knowledge check（369 items、0 errors/warnings）、knowledge unittest（33件成功）、knowledge build（6 views生成）、`git diff --exit-code -- README.md research/knowledge/generated`が成功。
- SHA-256全件目録は`output/final-sha256.json`。`python research/experiments/n11-proof-dag-engine-20261011/scripts/hash_artifacts.py --check`で検査できる。

S5を再開するときは、まず現在のS5探索担当の対象/solver binary/budgetを確認し、同じ対象で競合させない。初回pilotは解決済みS6か小盤面で通し、UNKNOWN/予算切れの証明出力がないことを確認してから新しい未解決対象を小budgetで選ぶ。候補S4への適用は、K0355の現行frontierとK0371/K0372の先手固定・信頼境界を再確認してから行う。
